"""
Bone Mineralization Integrated Model - Streamlit Web Interface
Runnable Python version with interactive UI
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bone_mineralization import (
    BoneMineralizationModel,
    ModelParameters,
    plot_isf_results,
    plot_ode_results,
    LagTimeAnalyzer
)


def initialize_session_state():
    """Initialize session state variables"""
    if 'isf_results' not in st.session_state:
        st.session_state.isf_results = None
    if 'ode_results' not in st.session_state:
        st.session_state.ode_results = None


def main():
    st.set_page_config(
        page_title="Bone Mineralization Simulator",
        page_icon="🦴",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🦴 Bone Mineralization Integrated Model Simulator")
    st.markdown("*A mathematical model of physicochemical and biological regulation of bone mineralization*")
    st.markdown("Based on: Poorhemati et al., Scientific Reports (2024)")

    initialize_session_state()

    # Create main tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 ISF Equilibrium", "🧬 ODE Model", "📈 Analysis", "ℹ️ About"]
    )

    # ======================== TAB 1: ISF EQUILIBRIUM ========================
    with tab1:
        st.header("Interstitial Fluid (ISF) Equilibrium Calculator")
        st.write("""
        This module calculates the equilibrium state of ions in the interstitial fluid
        using Newton-Raphson method with activity coefficient corrections.
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Blood/Fluid Composition")
            col_a, col_b = st.columns(2)

            with col_a:
                pH = st.number_input("pH", value=7.4, min_value=6.5, max_value=8.5, step=0.1)
                TCO3 = st.number_input("Total CO3 (mol/L)", value=24e-3, format="%.6f", step=1e-3)
                TPO4 = st.number_input("Total PO4 (mol/L)", value=1e-3, format="%.6f", step=0.1e-3)
                TCa = st.number_input("Total Ca (mol/L)", value=2.5e-3, format="%.6f", step=0.1e-3)

            with col_b:
                TMg = st.number_input("Total Mg (mol/L)", value=0.85e-3, format="%.6f", step=0.1e-3)
                TNa = st.number_input("Total Na (mol/L)", value=140e-3, format="%.6f", step=1e-3)
                TCl = st.number_input("Total Cl (mol/L)", value=100e-3, format="%.6f", step=1e-3)
                TK = st.number_input("Total K (mol/L)", value=5e-3, format="%.6f", step=0.1e-3)

        with col2:
            st.subheader("Simulation Settings")
            nr_tolerance = st.select_slider(
                "Newton-Raphson Tolerance",
                options=[1e-6, 1e-7, 1e-8, 1e-9],
                value=1e-8,
                format_func=lambda x: f"1e{int(np.log10(x))}"
            )
            iterations = st.slider("Max Iterations", min_value=10, max_value=1000, value=100)

            run_isf = st.button("🚀 Run ISF Equilibrium", key="run_isf", use_container_width=True)

        if run_isf:
            master_conc = np.array([pH, TCO3, TPO4, TCa, TMg, TNa, TCl, TK])

            with st.spinner("Calculating ISF equilibrium..."):
                model = BoneMineralizationModel()
                st.session_state.isf_results = model.run_isf_simulation(master_conc, iterations)

            st.success("✅ Equilibrium calculation complete!")

        if st.session_state.isf_results:
            results = st.session_state.isf_results

            # Display results in metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric(
                    "Initial pH",
                    f"{results['pH_initial']:.2f}",
                    delta=f"{results['pH_final'] - results['pH_initial']:.3f}"
                )

            with metric_col2:
                st.metric(
                    "Final pH",
                    f"{results['pH_final']:.2f}"
                )

            with metric_col3:
                sat_ratio = results['saturation_ratio']
                st.metric(
                    "Saturation Ratio",
                    f"{sat_ratio:.2f}",
                    f"{'Supersaturated' if sat_ratio > 1 else 'Undersaturated'}",
                    delta_color="off"
                )

            with metric_col4:
                rate = results['precipitation_rate']
                st.metric(
                    "Precipitation Rate",
                    f"{rate:.2e}",
                    "mol/(L·s)",
                    delta_color="off"
                )

            # Plot results
            st.subheader("Results Visualization")
            fig = plot_isf_results(results)
            st.pyplot(fig, use_container_width=True)

            # Detailed output
            with st.expander("📋 Detailed Results"):
                col_detail1, col_detail2 = st.columns(2)

                with col_detail1:
                    st.write("**Equilibrium Concentrations (first 15 species)**")
                    eq_conc = results['eq_conc'][:15]
                    for i, conc in enumerate(eq_conc):
                        st.write(f"Species {i}: {conc:.2e} mol/L")

                with col_detail2:
                    st.write("**Activity Coefficients (first 15)**")
                    gamma = results['gamma'][:15]
                    for i, g in enumerate(gamma):
                        st.write(f"γ{i}: {g:.4f}")

    # ======================== TAB 2: ODE MODEL ========================
    with tab2:
        st.header("Biomineralization ODE Model")
        st.write("""
        The ODE model describes the temporal dynamics of bone cell populations and mineral deposition:
        - x₁: Progenitor osteoblasts
        - x₂: Active osteoblasts
        - I: Inhibitor concentration
        - N: Nucleation-ready osteoclasts
        - y: Mineral content
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Cell Population Parameters")
            k1 = st.number_input("k₁ (Transition rate)", value=0.1, min_value=0.001, step=0.01)
            k2 = st.number_input("k₂ (Recruitment rate)", value=0.05, min_value=0.001, step=0.01)
            k3 = st.number_input("k₃ (Mineralization rate)", value=0.02, min_value=0.001, step=0.01)

        with col2:
            st.subheader("Regulation Parameters")
            v1 = st.number_input("v₁ (Inhibitor production)", value=0.3, min_value=0.01, step=0.05)
            r1 = st.number_input("r₁ (Inhibitor removal)", value=0.01, min_value=0.0001, step=0.001)
            r2 = st.number_input("r₂ (Mineral removal)", value=0.001, min_value=0.0001, step=0.0001)

        with col3:
            st.subheader("Hill Function Parameters")
            a = st.number_input("a (Hill exponent)", value=2.0, min_value=0.5, step=0.5)
            b = st.number_input("b (Hill coefficient)", value=1.0, min_value=0.1, step=0.1)
            t2 = st.number_input("t₂ (Temporal factor)", value=0.5, min_value=0.01, step=0.1)

        col_init1, col_init2 = st.columns(2)

        with col_init1:
            st.subheader("Initial Conditions")
            x1_init = st.number_input("Initial x₁ (progenitors)", value=10.0, min_value=0.1, step=0.5)
            x2_init = st.number_input("Initial x₂ (active)", value=0.0, min_value=0.0, step=0.5)
            I_init = st.number_input("Initial I (inhibitor)", value=0.1, min_value=0.01, step=0.01)

        with col_init2:
            st.subheader("Simulation Settings")
            N_init = st.number_input("Initial N (osteoclasts)", value=1.0, min_value=0.01, step=0.1)
            y_init = st.number_input("Initial y (mineral)", value=0.0, min_value=0.0, step=0.5)
            duration = st.number_input("Simulation Duration", value=100.0, min_value=1.0, step=10.0)
            num_points = st.slider("Number of Time Points", min_value=100, max_value=5000, value=1000, step=100)

        run_ode = st.button("🚀 Run ODE Simulation", key="run_ode", use_container_width=True)

        if run_ode:
            params = ModelParameters(
                k1=k1, k2=k2, k3=k3, v1=v1, r1=r1, r2=r2, a=a, b=b, t2=t2
            )
            initial_values = np.array([x1_init, x2_init, I_init, N_init, y_init])

            with st.spinner("Solving ODE system..."):
                model = BoneMineralizationModel()
                t, solution = model.run_ode_simulation(params, initial_values, duration, num_points)
                st.session_state.ode_results = (t, solution)

            st.success("✅ ODE simulation complete!")

        if st.session_state.ode_results:
            t, solution = st.session_state.ode_results

            # Display final values as metrics
            metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

            with metric_col1:
                st.metric("Final x₁", f"{solution[-1, 0]:.2f}")

            with metric_col2:
                st.metric("Final x₂", f"{solution[-1, 1]:.2f}")

            with metric_col3:
                st.metric("Final I", f"{solution[-1, 2]:.2f}")

            with metric_col4:
                st.metric("Final N", f"{solution[-1, 3]:.2f}")

            with metric_col5:
                st.metric("Final Mineral", f"{solution[-1, 4]:.2f}")

            # Plot results
            st.subheader("Simulation Results")
            fig = plot_ode_results(t, solution)
            st.pyplot(fig, use_container_width=True)

            # Detailed trajectory
            with st.expander("📊 Detailed Trajectory Data"):
                col_traj1, col_traj2 = st.columns(2)

                with col_traj1:
                    st.write("**Time Points**")
                    st.write(f"Total points: {len(t)}")
                    st.write(f"Time range: {t[0]:.1f} to {t[-1]:.1f}")

                    # Show key time points
                    indices = [0, len(t)//4, len(t)//2, 3*len(t)//4, -1]
                    for idx in indices:
                        if idx < len(t):
                            st.write(f"t={t[idx]:.1f}: y={solution[idx, 4]:.4f}")

                with col_traj2:
                    st.write("**Trajectory Data (every 100th point)**")
                    data_display = []
                    for i in range(0, len(t), max(1, len(t)//10)):
                        data_display.append({
                            'Time': f"{t[i]:.1f}",
                            'x₁': f"{solution[i, 0]:.4f}",
                            'x₂': f"{solution[i, 1]:.4f}",
                            'I': f"{solution[i, 2]:.4f}",
                            'N': f"{solution[i, 3]:.4f}",
                            'y': f"{solution[i, 4]:.4f}"
                        })
                    st.dataframe(data_display, use_container_width=True)

    # ======================== TAB 3: ANALYSIS ========================
    with tab3:
        st.header("Analysis & Advanced Features")

        if st.session_state.ode_results:
            t, solution = st.session_state.ode_results

            st.subheader("Lag Time Analysis")
            st.write("Identify transition points in the mineralization process:")

            # Lag time for mineral deposition
            analyzer = LagTimeAnalyzer()
            peaks, transition = analyzer.calculate_lag_time(t, solution[:, 4])

            if not np.isnan(transition):
                st.info(f"🎯 **Transition Point (Lag Time): {transition:.2f}**")
                st.write(f"This represents when the mineralization process significantly accelerates.")

            # Inhibitor dynamics analysis
            st.subheader("Inhibitor Dynamics")
            max_inhibitor = np.max(solution[:, 2])
            min_inhibitor = np.min(solution[:, 2])
            st.write(f"Maximum inhibitor concentration: {max_inhibitor:.4f}")
            st.write(f"Minimum inhibitor concentration: {min_inhibitor:.4f}")

            # Cell population analysis
            st.subheader("Cell Population Analysis")
            max_x1 = np.max(solution[:, 0])
            max_x2 = np.max(solution[:, 1])
            max_N = np.max(solution[:, 3])

            col_analysis1, col_analysis2, col_analysis3 = st.columns(3)

            with col_analysis1:
                st.metric("Peak Progenitor (x₁)", f"{max_x1:.2f}")

            with col_analysis2:
                st.metric("Peak Active Osteoblast (x₂)", f"{max_x2:.2f}")

            with col_analysis3:
                st.metric("Peak Osteoclasts (N)", f"{max_N:.2f}")

            # Mineralization efficiency
            st.subheader("Mineralization Efficiency")
            final_mineral = solution[-1, 4]
            initial_cells = solution[0, 0]
            efficiency = final_mineral / (initial_cells + 1e-10)

            st.metric("Mineral per Initial Progenitor", f"{efficiency:.4f}")

            # Custom analysis plots
            st.subheader("Custom Analysis Plots")

            analysis_option = st.selectbox(
                "Select analysis type",
                ["Phase Space (x₂ vs Mineral)", "Cell Population Trajectory", "Inhibitor Effect"]
            )

            fig, ax = plt.subplots(figsize=(10, 6))

            if analysis_option == "Phase Space (x₂ vs Mineral)":
                ax.scatter(solution[:, 1], solution[:, 4], c=t, cmap="viridis", s=20)
                ax.set_xlabel("Active Osteoblasts (x₂)")
                ax.set_ylabel("Mineral Content (y)")
                ax.set_title("Phase Space Trajectory")
                cbar = plt.colorbar(ax.collections[0], ax=ax)
                cbar.set_label("Time")

            elif analysis_option == "Cell Population Trajectory":
                ax.plot(t, solution[:, 0], label="x₁ (Progenitors)", linewidth=2)
                ax.plot(t, solution[:, 1], label="x₂ (Active)", linewidth=2)
                ax.plot(t, solution[:, 3], label="N (Osteoclasts)", linewidth=2)
                ax.set_xlabel("Time")
                ax.set_ylabel("Population")
                ax.set_title("Cell Population Dynamics")
                ax.legend()
                ax.grid(True, alpha=0.3)

            elif analysis_option == "Inhibitor Effect":
                ax.plot(t, solution[:, 2], label="Inhibitor (I)", linewidth=2, color="orange")
                ax.set_xlabel("Time")
                ax.set_ylabel("Inhibitor Concentration")
                ax.set_title("Inhibitor Dynamics")
                ax.grid(True, alpha=0.3)
                ax.fill_between(t, 0, solution[:, 2], alpha=0.3)

            st.pyplot(fig, use_container_width=True)

        else:
            st.info("💡 Run the ODE Model simulation first to enable analysis features.")

    # ======================== TAB 4: ABOUT ========================
    with tab4:
        st.header("About This Model")

        st.markdown("""
        ### Overview
        This is a Python implementation of the bone mineralization integrated model developed at McGill University.
        It combines physicochemical and biological factors that regulate bone mineralization.

        ### Key Components

        **1. ISF Equilibrium Module**
        - Calculates ionic equilibrium in the interstitial fluid using Newton-Raphson method
        - Accounts for activity coefficients using Davies equation
        - Determines hydroxyapatite (HAP) saturation state
        - Predicts precipitation rates

        **2. Biomineralization ODE Model**
        - Tracks dynamics of:
          - Osteoblast progenitors (x₁) → active osteoblasts (x₂)
          - Inhibitor production and decay
          - Osteoclast maturation and activity
          - Mineral deposition
        - Uses modified Hill function for feedback regulation

        **3. Analysis Tools**
        - Lag time analysis to identify process transition points
        - Phase space visualization
        - Population dynamics tracking
        - Efficiency calculations

        ### Mathematical Foundation
        - **ODE System**: Coupled nonlinear differential equations
        - **Equilibrium**: Newton-Raphson with iterative activity correction
        - **Kinetics**: Saturation-based precipitation models

        ### Citation
        > Poorhemati, H., Komarova, S. V., et al. (2024)
        > Mathematical model capturing physicochemical and biological regulation of bone mineralization
        > *Scientific Reports*, 14(1), xxxxx

        ### Usage Tips
        1. **ISF Equilibrium**: Adjust pH and ion concentrations to model different physiological conditions
        2. **ODE Model**: Tune parameters to explore different mineralization scenarios
        3. **Analysis**: Use lag time analysis to identify critical transition points

        ### Technical Details
        - **Language**: Python 3.x
        - **Core Libraries**: NumPy, SciPy, Matplotlib, Streamlit
        - **Computation**: Numerical integration (odeint), Root finding (Newton-Raphson)
        - **Performance**: Real-time on standard hardware for most simulations

        ### Contact
        For questions about the original MATLAB model:
        📧 hossein.poorhemati@mail.mcgill.ca
        """)

        st.divider()

        st.subheader("References")
        st.write("""
        - Poorhemati, H., Komarova, S. V. (2024). Bone mineralization model. *Nature Scientific Reports*.
        - Official MATLAB implementation: [GitHub Repository](https://github.com/Hosseinpoorhemati/bone_mineralization_integrated)
        """)


if __name__ == "__main__":
    main()
