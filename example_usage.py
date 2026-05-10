"""
Example usage of the Bone Mineralization Model library

This script demonstrates how to use the model programmatically
without the Streamlit UI.
"""

import numpy as np
import matplotlib.pyplot as plt
from bone_mineralization import (
    BoneMineralizationModel,
    ModelParameters,
    LagTimeAnalyzer,
)


def example_1_basic_isf_calculation():
    """Example 1: Basic ISF equilibrium calculation"""
    print("\n" + "="*60)
    print("EXAMPLE 1: ISF Equilibrium Calculation")
    print("="*60)

    model = BoneMineralizationModel()

    # Define ISF composition (blood-like)
    master_conc = np.array([
        7.4,          # pH
        24e-3,        # TCO3 (mol/L)
        1e-3,         # TPO4 (mol/L)
        2.5e-3,       # TCa (mol/L)
        0.85e-3,      # TMg (mol/L)
        140e-3,       # TNa (mol/L)
        100e-3,       # TCl (mol/L)
        5e-3          # TK (mol/L)
    ])

    print("\nInput ISF Composition:")
    print(f"  pH: {master_conc[0]:.1f}")
    print(f"  Total CO3: {master_conc[1]*1e3:.2f} mM")
    print(f"  Total PO4: {master_conc[2]*1e3:.2f} mM")
    print(f"  Total Ca: {master_conc[3]*1e3:.2f} mM")

    # Run calculation
    results = model.run_isf_simulation(master_conc, iterations=100)

    print("\nResults:")
    print(f"  Initial pH: {results['pH_initial']:.3f}")
    print(f"  Final pH: {results['pH_final']:.3f}")
    print(f"  pH Change: {results['pH_final'] - results['pH_initial']:+.3f}")
    print(f"  HAP Saturation Ratio: {results['saturation_ratio']:.2f}")

    if results['saturation_ratio'] > 1:
        print(f"  Status: ✓ SUPERSATURATED (HAP will precipitate)")
    else:
        print(f"  Status: ✗ UNDERSATURATED (No precipitation)")

    print(f"  Precipitation Rate: {results['precipitation_rate']:.2e} mol/(L·s)")
    print(f"  Convergence Iterations: {results['iterations']}")

    return results


def example_2_acidic_vs_neutral():
    """Example 2: Compare acidic vs neutral pH"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Effect of pH on Mineralization")
    print("="*60)

    model = BoneMineralizationModel()

    pH_values = [6.8, 7.0, 7.2, 7.4, 7.6]
    saturation_ratios = []
    precipitation_rates = []

    master_conc_template = np.array([7.4, 24e-3, 1e-3, 2.5e-3, 0.85e-3, 140e-3, 100e-3, 5e-3])

    print("\nTesting pH range 6.8-7.6:")
    for pH in pH_values:
        master_conc = master_conc_template.copy()
        master_conc[0] = pH

        results = model.run_isf_simulation(master_conc)
        saturation_ratios.append(results['saturation_ratio'])
        precipitation_rates.append(results['precipitation_rate'])

        status = "✓ Supersaturated" if results['saturation_ratio'] > 1 else "✗ Undersaturated"
        print(f"  pH {pH:.1f}: Sat.Ratio = {results['saturation_ratio']:6.2f}  {status}")

    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(pH_values, saturation_ratios, 'o-', linewidth=2, markersize=8)
    ax1.axhline(y=1, color='r', linestyle='--', label='Saturation threshold')
    ax1.set_xlabel('pH')
    ax1.set_ylabel('Saturation Ratio')
    ax1.set_title('HAP Saturation vs pH')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.semilogy(pH_values, precipitation_rates, 's-', linewidth=2, markersize=8, color='orange')
    ax2.set_xlabel('pH')
    ax2.set_ylabel('Precipitation Rate (mol/(L·s))')
    ax2.set_title('HAP Precipitation Rate vs pH')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('example_2_ph_effect.png', dpi=150, bbox_inches='tight')
    print("\n✓ Plot saved as: example_2_ph_effect.png")

    return fig


def example_3_ode_simulation():
    """Example 3: Run ODE model simulation"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Biomineralization ODE Model")
    print("="*60)

    model = BoneMineralizationModel()

    # Define parameters
    params = ModelParameters(
        k1=0.1,    # Progenitor transition rate
        k2=0.05,   # Osteoclast recruitment rate
        k3=0.02,   # Mineralization rate
        v1=0.3,    # Inhibitor production
        r1=0.01,   # Inhibitor removal
        r2=0.001,  # Mineral resorption
        a=2.0,     # Hill exponent
        b=1.0,     # Hill coefficient
        t2=0.5     # Temporal factor
    )

    # Initial conditions
    initial_values = np.array([
        10.0,   # x1: Progenitor osteoblasts
        0.0,    # x2: Active osteoblasts
        0.1,    # I: Inhibitor
        1.0,    # N: Osteoclasts
        0.0     # y: Mineral
    ])

    print("\nParameters:")
    print(f"  k1 (transition): {params.k1}")
    print(f"  k2 (recruitment): {params.k2}")
    print(f"  k3 (mineralization): {params.k3}")

    print("\nInitial Conditions:")
    print(f"  x1 (progenitors): {initial_values[0]:.1f}")
    print(f"  x2 (active): {initial_values[1]:.1f}")
    print(f"  I (inhibitor): {initial_values[2]:.1f}")
    print(f"  N (osteoclasts): {initial_values[3]:.1f}")
    print(f"  y (mineral): {initial_values[4]:.1f}")

    # Run simulation
    print("\nRunning ODE simulation for 100 time units...")
    t, solution = model.run_ode_simulation(params, initial_values, duration=100)

    print("\nFinal Values:")
    print(f"  x1 (progenitors): {solution[-1, 0]:.2f}")
    print(f"  x2 (active): {solution[-1, 1]:.2f}")
    print(f"  I (inhibitor): {solution[-1, 2]:.2f}")
    print(f"  N (osteoclasts): {solution[-1, 3]:.2f}")
    print(f"  y (mineral): {solution[-1, 4]:.2f}")

    # Plot results
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    labels = ['Progenitor Osteoblasts (x1)', 'Active Osteoblasts (x2)',
              'Inhibitor (I)', 'Osteoclasts (N)', 'Mineral (y)']

    for i in range(5):
        axes[i].plot(t, solution[:, i], linewidth=2, color=f'C{i}')
        axes[i].set_xlabel('Time')
        axes[i].set_ylabel('Concentration')
        axes[i].set_title(labels[i])
        axes[i].grid(True, alpha=0.3)

    axes[5].remove()

    plt.tight_layout()
    plt.savefig('example_3_ode_dynamics.png', dpi=150, bbox_inches='tight')
    print("\n✓ Plot saved as: example_3_ode_dynamics.png")

    return t, solution


def example_4_parameter_sensitivity():
    """Example 4: Parameter sensitivity analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Mineralization Rate Sensitivity")
    print("="*60)

    model = BoneMineralizationModel()

    k3_values = [0.005, 0.01, 0.02, 0.04, 0.08]
    final_minerals = []

    initial_values = np.array([10.0, 0.0, 0.1, 1.0, 0.0])

    print("\nTesting k3 (mineralization rate) from 0.005 to 0.08:")

    for k3 in k3_values:
        params = ModelParameters(
            k1=0.1, k2=0.05, k3=k3, v1=0.3, r1=0.01, r2=0.001, a=2, b=1, t2=0.5
        )
        t, solution = model.run_ode_simulation(params, initial_values, duration=100)
        final_minerals.append(solution[-1, 4])
        print(f"  k3 = {k3:.3f}: Final mineral = {solution[-1, 4]:.2f}")

    # Plot sensitivity
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(k3_values, final_minerals, 'o-', linewidth=2, markersize=10, color='darkblue')
    ax.set_xlabel('Mineralization Rate (k₃)', fontsize=12)
    ax.set_ylabel('Final Mineral Content', fontsize=12)
    ax.set_title('Sensitivity Analysis: Effect of k₃ on Final Mineral', fontsize=14)
    ax.grid(True, alpha=0.3)

    # Add annotations
    for k3, mineral in zip(k3_values, final_minerals):
        ax.annotate(f'{mineral:.2f}', xy=(k3, mineral), xytext=(0, 10),
                   textcoords='offset points', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('example_4_sensitivity.png', dpi=150, bbox_inches='tight')
    print("\n✓ Plot saved as: example_4_sensitivity.png")

    return fig


def example_5_lag_time_analysis():
    """Example 5: Lag time analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Lag Time Analysis")
    print("="*60)

    model = BoneMineralizationModel()

    params = ModelParameters(k1=0.1, k2=0.05, k3=0.02, v1=0.3, r1=0.01, r2=0.001, a=2, b=1, t2=0.5)
    initial_values = np.array([10.0, 0.0, 0.1, 1.0, 0.0])

    t, solution = model.run_ode_simulation(params, initial_values, duration=100)

    # Analyze lag time
    analyzer = LagTimeAnalyzer()
    peaks, transition_point = analyzer.calculate_lag_time(t, solution[:, 4])

    print(f"\nMineral accumulation analysis:")
    print(f"  Initial mineral: {solution[0, 4]:.4f}")
    print(f"  Final mineral: {solution[-1, 4]:.4f}")

    if not np.isnan(transition_point):
        print(f"  Lag time (transition point): {transition_point:.2f}")
        print(f"  This is when mineralization significantly accelerates")
    else:
        print(f"  No clear transition point detected")

    # Plot with transition point
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(t, solution[:, 4], linewidth=2, label='Mineral Accumulation')

    if not np.isnan(transition_point):
        ax.axvline(x=transition_point, color='r', linestyle='--', linewidth=2, label=f'Lag Time = {transition_point:.2f}')
        idx = np.argmin(np.abs(t - transition_point))
        ax.plot(transition_point, solution[idx, 4], 'ro', markersize=10)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Mineral Content (y)', fontsize=12)
    ax.set_title('Lag Time Analysis: Mineral Deposition Dynamics', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig('example_5_lag_time.png', dpi=150, bbox_inches='tight')
    print("\n✓ Plot saved as: example_5_lag_time.png")

    return fig


def main():
    """Run all examples"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  BONE MINERALIZATION MODEL - USAGE EXAMPLES".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)

    # Run examples
    example_1_basic_isf_calculation()
    example_2_acidic_vs_neutral()
    example_3_ode_simulation()
    example_4_parameter_sensitivity()
    example_5_lag_time_analysis()

    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("="*60)
    print("\n📊 Generated plots:")
    print("  - example_2_ph_effect.png")
    print("  - example_3_ode_dynamics.png")
    print("  - example_4_sensitivity.png")
    print("  - example_5_lag_time.png")
    print("\n💡 Tip: Open these PNG files to see the visualizations")
    print("🌐 For interactive exploration, run: streamlit run app.py\n")


if __name__ == "__main__":
    main()
