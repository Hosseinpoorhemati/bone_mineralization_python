"""
Bone Mineralization Integrated Model - Python Version
Based on the MATLAB implementation from Hossein Poorhemati, Svetlana Komarova, McGill University - 2024
Mathematical model of physicochemical and biological regulation of bone mineralization
"""

import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.signal import find_peaks
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, Dict, List


@dataclass
class ModelParameters:
    """ODE model parameters for biomineralization"""
    k1: float  # Transition rate from x1 to x2
    k2: float  # Progenitor recruitment rate
    k3: float  # Mineralization rate
    v1: float  # Inhibitor production rate
    r1: float  # Inhibitor removal rate (x2-dependent)
    r2: float  # Mineral removal rate
    a: float   # Hill exponent
    b: float   # Hill coefficient
    t2: float  # Temporal factor


class ISFEquilibrium:
    """Interstitial Fluid (ISF) equilibrium calculator using Newton-Raphson method"""

    # Equilibrium constants at 37°C
    K = {
        1: 10**-14,      # water
        2: 10**-6.31,    # H2CO3
        3: 10**-10.25,   # HCO3-
        4: 10**-2.196,   # H3PO4
        5: 10**-7.185,   # H2PO4 2-
        6: 10**-12.19,   # HPO4 3-
        7: 10**1.16,     # CaHCO3+
        8: 10**3.38,     # CaCO3
        9: 25.12,        # CaOH+
        10: 31.9,        # CaH2PO4+
        11: 6.81e2,      # CaHPO4
        12: 3.46e6,      # CaPO4-
        13: 10**0.62,    # MgHCO3+
        14: 10**1.87,    # MgCO3
        15: 10**2.19,    # MgOH+
        16: 10**0.4,     # MgH2PO4+
        17: 10**1.8,     # MgHPO4
        18: 10**3.3,     # MgPO4-
        19: 0.21,        # NAHPO4-
        20: 10**-6.82,   # NaH2PO4
        21: 1/29.3,      # NaCl
        22: 2.5,         # KHPO4-
    }

    def __init__(self, nr_tol: float = 1e-8, activity_tol: float = 1e-8):
        self.nr_tol = nr_tol
        self.activity_tol = activity_tol

    def calculate_activity_coefficients(self, concentrations: np.ndarray) -> Tuple[np.ndarray, float]:
        """Calculate activity coefficients using Davies equation"""
        charges = np.array([1, -1, 0, -2, -1, 0, -1, -2, -3, 2, 1, 0, 1, 1, 0,
                           -1, 2, 1, 0, 1, 1, 0, -1, 1, -1, 0, -1, 0, 1, -1])

        # Calculate ionic strength
        IS = 0.5 * np.sum(concentrations * (charges**2))

        # Davies equation parameters at 37°C
        temp = 37
        A = 0.486 + (6.07e-4 * temp) + (6.43e-6 * (temp**2))

        # Activity coefficients
        sqrt_IS = np.sqrt(IS)
        gamma = 10 ** (-A * (charges**2) * ((sqrt_IS/(1+sqrt_IS)) - (0.3*IS)))

        return gamma, IS

    def equations(self, z: np.ndarray, gamma: np.ndarray, c: np.ndarray, pH: float) -> np.ndarray:
        """System of equilibrium equations"""
        H_ion = 10**(-pH) * gamma[0]

        # Apply activity corrections
        z_corrected = z * gamma[[4, 7, 9, 16, 23, 26, 28]]

        F = np.zeros(7)

        # HCO3 mass balance
        F[0] = (self.K[3]/self.K[2]) * H_ion * z_corrected[0] / gamma[2] + \
               (self.K[3]*z_corrected[0]/H_ion) / gamma[3] + z_corrected[0] / gamma[4] - c[0]

        # HPO4 mass balance
        F[1] = ((1/(self.K[4]*self.K[5]))*(H_ion**2)*z_corrected[1]) / gamma[5] + \
               ((1/self.K[5])*H_ion*z_corrected[1]) / gamma[6] + \
               z_corrected[1] / gamma[7] + (self.K[6]*z_corrected[1]/H_ion) / gamma[8] - c[1]

        # Ca mass balance
        F[2] = z_corrected[2] / gamma[9] + \
               (self.K[7]*z_corrected[0]*z_corrected[2]) / gamma[10] - c[2]

        # Mg mass balance
        F[3] = z_corrected[3] / gamma[16] + \
               (self.K[13]*z_corrected[0]*z_corrected[3]) / gamma[17] - c[3]

        # Na mass balance
        F[4] = z_corrected[4] / gamma[23] + \
               (self.K[19]*z_corrected[1]*z_corrected[4]) / gamma[24] - c[4]

        # Cl mass balance
        F[5] = z_corrected[5] / gamma[26] + \
               (self.K[21]*z_corrected[4]*z_corrected[5]) / gamma[27] - c[5]

        # K mass balance
        F[6] = z_corrected[6] / gamma[28] + \
               (self.K[22]*z_corrected[1]*z_corrected[6]) / gamma[29] - c[6]

        return F

    def jacobian(self, z: np.ndarray, gamma: np.ndarray, c: np.ndarray, pH: float) -> np.ndarray:
        """Numerical Jacobian calculation"""
        eps = 1e-8
        J = np.zeros((7, 7))
        f0 = self.equations(z, gamma, c, pH)

        for i in range(7):
            z_plus = z.copy()
            z_plus[i] += eps * max(1, abs(z[i]))
            f_plus = self.equations(z_plus, gamma, c, pH)
            J[:, i] = (f_plus - f0) / (eps * max(1, abs(z[i])))

        return J

    def equilibrate(self, master_conc: np.ndarray, iterations: int = 100) -> Dict:
        """
        Calculate ISF equilibrium

        master_conc: [pH, TCO3, TPO4, TCa, TMg, TNa, TCl, TK]
        """
        pH = master_conc[0]
        c = master_conc[1:8]

        # Initial guess for concentrations
        z0 = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
        z = z0.copy()

        # Initial gamma
        y0 = np.ones(30) * 0.5
        gamma_prev = y0.copy()

        # Newton-Raphson iteration with activity correction
        converged = False
        iteration = 0

        while not converged and iteration < 50:
            # Newton step
            J = self.jacobian(z, gamma_prev, c, pH)
            try:
                dz = np.linalg.solve(J, self.equations(z, gamma_prev, c, pH))
                z = z - dz
                z = np.maximum(z, z0/100)  # Prevent negative concentrations
            except np.linalg.LinAlgError:
                break

            # Update activity coefficients
            eq_conc = self.get_equilibrium_concentrations(z, gamma_prev, pH)
            gamma_new, _ = self.calculate_activity_coefficients(eq_conc)

            # Check convergence
            if np.max(np.abs(gamma_new - gamma_prev)) <= self.activity_tol:
                converged = True

            gamma_prev = gamma_new
            iteration += 1

        eq_conc = self.get_equilibrium_concentrations(z, gamma_prev, pH)

        # Calculate final pH from H+ concentration
        pH_calc = -np.log10(eq_conc[0] * gamma_prev[0])

        # Calculate saturation ratio
        sat_ratio, sat_status = self.saturation_ratio(eq_conc, gamma_prev)

        # Calculate precipitation rate
        if sat_ratio > 1:
            Ca_act = eq_conc[9] * gamma_prev[9]
            P_act = eq_conc[8] * gamma_prev[8]
            k = 173.4
            s = 50
            rate = k * s * Ca_act * P_act
        else:
            rate = 0

        return {
            'eq_conc': eq_conc,
            'pH_initial': pH,
            'pH_final': pH_calc,
            'saturation_ratio': sat_ratio,
            'saturation_status': sat_status,
            'precipitation_rate': rate,
            'gamma': gamma_prev,
            'iterations': iteration
        }

    def get_equilibrium_concentrations(self, z: np.ndarray, gamma: np.ndarray, pH: float) -> np.ndarray:
        """Calculate all equilibrium concentrations from primary species"""
        H_ion = 10**(-pH)
        y = np.zeros(30)

        # Primary species
        y[0] = H_ion * gamma[0]
        y[4] = z[0] * gamma[4]
        y[7] = z[1] * gamma[7]
        y[9] = z[2] * gamma[9]
        y[16] = z[3] * gamma[16]
        y[23] = z[4] * gamma[23]
        y[26] = z[5] * gamma[26]
        y[28] = z[6] * gamma[28]

        # Secondary species (derived from equilibrium constants)
        y[1] = (self.K[1] / y[0]) / gamma[1]
        y[2] = ((self.K[3]/self.K[2]) * y[0] * y[4]) / gamma[2]
        y[3] = (self.K[3] * y[4] / y[0]) / gamma[3]
        y[5] = ((1/(self.K[4]*self.K[5])) * (y[0]**2) * y[7]) / gamma[5]
        y[6] = ((1/self.K[5]) * y[0] * y[7]) / gamma[6]
        y[8] = (self.K[6] * y[7] / y[0]) / gamma[8]
        y[10] = (self.K[7] * y[4] * y[9]) / gamma[10]

        # Normalize by gamma
        y = y / gamma

        return y

    def saturation_ratio(self, concentrations: np.ndarray, gamma: np.ndarray) -> Tuple[float, int]:
        """Calculate HAP saturation ratio and status"""
        # HAP: Ca5(PO4)3OH, Ksp = 2.03e-59
        # y[9] = Ca, y[8] = PO4, y[1] = OH

        IP = ((gamma[9]*concentrations[9])**5) * ((gamma[8]*concentrations[8])**3) * gamma[1]*concentrations[1]
        Ksp = 2.03e-59

        sat_ratio = (IP / Ksp) ** (1/9)

        if sat_ratio > 1:
            status = 1
        elif sat_ratio < 1:
            status = -1
        else:
            status = 0

        return sat_ratio, status


class BiomineralizationODE:
    """ODE model for biomineralization process"""

    def __init__(self, params: ModelParameters):
        self.params = params

    def hill_function(self, x: float) -> float:
        """Modified Hill function"""
        return self.params.b / (self.params.b + x**self.params.a)

    def derivatives(self, z: np.ndarray, t: float) -> np.ndarray:
        """
        System of ODEs for biomineralization
        z = [x1, x2, I, N, y]
        x1: Progenitor osteoblasts
        x2: Active osteoblasts
        I: Inhibitor concentration
        N: Nucleation-ready osteoclasts
        y: Mineral content
        """
        x1, x2, I, N, y = z

        dzdt = np.zeros(5)
        dzdt[0] = -self.params.k1 * x1
        dzdt[1] = self.params.k1 * x1
        dzdt[2] = self.params.v1 * x1 - self.params.r1 * x2 * I - \
                 self.params.t2 * (self.params.k3 * self.hill_function(I) * N) * I
        dzdt[3] = self.params.k2 * (self.params.k1 * x1) - self.params.r2 * N * \
                 (self.params.k3 * self.hill_function(I) * N)
        dzdt[4] = self.params.k3 * self.hill_function(I) * N

        return dzdt

    def solve(self, initial_values: np.ndarray, duration: float, num_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Solve ODE system"""
        t = np.linspace(0, duration, num_points)
        solution = odeint(self.derivatives, initial_values, t)
        return t, solution


class LagTimeAnalyzer:
    """Analyze lag time from time series data"""

    @staticmethod
    def calculate_lag_time(x: np.ndarray, y: np.ndarray) -> Tuple[List, float]:
        """
        Find lag time by identifying peak in derivative

        Returns peaks locations and transition point
        """
        # Compute derivative
        dy_dx = np.diff(y) / np.diff(x)

        # Find peaks in derivative
        # find_peaks returns (peak_indices, properties_dict)
        peak_indices, _ = find_peaks(dy_dx, prominence=np.max(np.abs(dy_dx))*0.1 if np.max(np.abs(dy_dx)) > 0 else 0.01)

        transition_point = np.nan
        if len(peak_indices) > 0:
            # The peak is at position peak_indices[0] in dy_dx array
            # which corresponds to position peak_indices[0]+1 in original x array (due to diff)
            transition_point = x[min(peak_indices[0] + 1, len(x) - 1)]

        return [peak_indices, peak_indices], transition_point


class BoneMineralizationModel:
    """Complete integrated bone mineralization model"""

    def __init__(self):
        self.isf = ISFEquilibrium()

    def run_isf_simulation(self, master_conc: np.ndarray, iterations: int = 100) -> Dict:
        """Run ISF equilibrium simulation"""
        return self.isf.equilibrate(master_conc, iterations)

    def run_ode_simulation(self, params: ModelParameters, initial_values: np.ndarray,
                          duration: float, num_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Run biomineralization ODE simulation"""
        ode_model = BiomineralizationODE(params)
        return ode_model.solve(initial_values, duration, num_points)

    def non_dimensionalize(self, params: ModelParameters, characteristics: np.ndarray) -> ModelParameters:
        """Non-dimensionalize model parameters"""
        x1_c, x2_c, I_c, N_c, y_c = characteristics
        t_c = 1

        return ModelParameters(
            k1=params.k1 * t_c,
            k2=params.k2 * x2_c / N_c,
            k3=params.k3 * N_c * t_c / y_c,
            v1=params.v1 * x1_c * t_c / I_c,
            r1=params.r1 * x2_c * t_c,
            r2=params.r2 * y_c,
            a=params.a,
            b=params.b / (I_c**params.a),
            t2=params.t2 * y_c
        )


# Utility functions for visualization
def plot_isf_results(results: Dict):
    """Plot ISF simulation results"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # pH change
    axes[0, 0].bar(['Initial pH', 'Final pH'],
                   [results['pH_initial'], results['pH_final']])
    axes[0, 0].set_ylabel('pH')
    axes[0, 0].set_title('pH Change During Equilibration')

    # Saturation ratio
    axes[0, 1].bar(['Saturation Ratio'], [results['saturation_ratio']])
    axes[0, 1].axhline(y=1, color='r', linestyle='--', label='Threshold')
    axes[0, 1].set_ylabel('Saturation Ratio')
    axes[0, 1].set_title('HAP Saturation Status')
    axes[0, 1].legend()

    # Precipitation rate
    axes[1, 0].bar(['Precipitation Rate'], [results['precipitation_rate']])
    axes[1, 0].set_ylabel('Rate (mol/(L·s))')
    axes[1, 0].set_title('HAP Precipitation Rate')

    # Ionic strength
    concentrations = results['eq_conc']
    charges = np.array([1, -1, 0, -2, -1, 0, -1, -2, -3, 2, 1, 0, 1, 1, 0,
                       -1, 2, 1, 0, 1, 1, 0, -1, 1, -1, 0, -1, 0, 1, -1])
    IS = 0.5 * np.sum(concentrations[:len(charges)] * (charges**2))
    axes[1, 1].bar(['Ionic Strength'], [IS])
    axes[1, 1].set_ylabel('Ionic Strength (mol/L)')
    axes[1, 1].set_title('Solution Ionic Strength')

    plt.tight_layout()
    return fig


def plot_ode_results(t: np.ndarray, solution: np.ndarray):
    """Plot ODE simulation results"""
    labels = ['Progenitor Osteoblasts (x1)', 'Active Osteoblasts (x2)',
              'Inhibitor (I)', 'Osteoclasts (N)', 'Mineral (y)']

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for i in range(5):
        axes[i].plot(t, solution[:, i], linewidth=2)
        axes[i].set_xlabel('Time')
        axes[i].set_ylabel('Concentration')
        axes[i].set_title(labels[i])
        axes[i].grid(True, alpha=0.3)

    # Remove extra subplot
    axes[5].remove()

    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Example usage
    model = BoneMineralizationModel()

    # ISF equilibrium example (blood-like composition)
    master_conc = np.array([7.4, 24e-3, 1e-3, 2.5e-3, 0.85e-3, 140e-3, 100e-3, 5e-3])
    print("Running ISF equilibrium calculation...")
    isf_results = model.run_isf_simulation(master_conc)
    print(f"pH initial: {isf_results['pH_initial']:.2f}, final: {isf_results['pH_final']:.2f}")
    print(f"Saturation ratio: {isf_results['saturation_ratio']:.2f}")
    print(f"Precipitation rate: {isf_results['precipitation_rate']:.2e} mol/(L·s)")

    # ODE model example
    print("\nRunning ODE simulation...")
    params = ModelParameters(k1=0.1, k2=0.05, k3=0.02, v1=0.3, r1=0.01, r2=0.001, a=2, b=1, t2=0.5)
    initial_values = np.array([10, 0, 0.1, 1, 0])
    t, solution = model.run_ode_simulation(params, initial_values, duration=100)

    print(f"Time span: {t[0]:.1f} to {t[-1]:.1f}")
    print(f"Final mineral content: {solution[-1, 4]:.2f}")
