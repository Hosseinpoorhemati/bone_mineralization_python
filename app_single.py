"""
Bone Mineralization Integrated Model - Single Page UI
All controls and results on one page for easy workflow
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from bone_mineralization import (
    BoneMineralizationModel,
    ModelParameters,
    LagTimeAnalyzer,
)


def parse_scientific_input(value_str):
    """Parse scientific notation and regular numbers"""
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return None


def initialize_session_state():
    """Initialize session state variables"""
    if 'isf_results' not in st.session_state:
        st.session_state.isf_results = None
    if 'ode_results' not in st.session_state:
        st.session_state.ode_results = None
    if 'model_mode' not in st.session_state:
        st.session_state.model_mode = "Primary"
    if 'dim_mode' not in st.session_state:
        st.session_state.dim_mode = "No"


def main():
    st.set_page_config(
        page_title="Bone Mineralization Simulator",
        page_icon="🦴",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("🦴 Bone Mineralization Integrated Model")
    st.markdown("*Complete Python version - Single Page Interface*")
    st.markdown("All parameters, controls, and results on one page")

    initialize_session_state()

    # ======================== SECTION 1: ISF EQUILIBRIUM ========================
    with st.expander("📊 **1. ISF Equilibrium (Physicochemical)**", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Ion Concentrations")
            pH = st.text_input("pH", value="7.4", key="pH_input")
            TCO3 = st.text_input("TCO₃ (mol/L)", value="0.027", key="TCO3_input")
            TPO4 = st.text_input("TPO₄ (mol/L)", value="0.001", key="TPO4_input")
            TCa = st.text_input("TCa (mol/L)", value="0.0016", key="TCa_input")

        with col2:
            st.subheader("More Ions")
            TMg = st.text_input("TMg (mol/L)", value="0.001", key="TMg_input")
            TNa = st.text_input("TNa (mol/L)", value="0.142", key="TNa_input")
            TCl = st.text_input("TCl (mol/L)", value="0.103", key="TCl_input")
            TK = st.text_input("TK (mol/L)", value="0.005", key="TK_input")

        with col3:
            st.subheader("ISF Settings")
            nr_tolerance = st.selectbox(
                "NR Tolerance",
                ["1e-6", "1e-7", "1e-8", "1e-9"],
                index=2,
                key="nr_tol_select"
            )
            iterations = st.slider("Max Iterations", 10, 1000, 100, key="nr_iter")

            if st.button("🚀 Run ISF", key="run_isf_btn", use_container_width=True):
                st.session_state.run_isf = True
            if st.button("Reset ISF", key="reset_isf_btn", use_container_width=True):
                st.session_state.isf_results = None
                st.rerun()

        with col4:
            st.subheader("ISF Results")
            if st.session_state.isf_results:
                results = st.session_state.isf_results
                st.metric("Initial pH", f"{results['pH_initial']:.3f}")
                st.metric("Final pH", f"{results['pH_final']:.3f}")
                st.metric("Saturation Ratio", f"{results['saturation_ratio']:.2f}")
                st.metric("Precip. Rate", f"{results['precipitation_rate']:.2e}")
            else:
                st.info("Click 'Run ISF' to calculate")

        # Run ISF if triggered
        if st.session_state.get('run_isf', False):
            try:
                pH_val = parse_scientific_input(pH)
                TCO3_val = parse_scientific_input(TCO3)
                TPO4_val = parse_scientific_input(TPO4)
                TCa_val = parse_scientific_input(TCa)
                TMg_val = parse_scientific_input(TMg)
                TNa_val = parse_scientific_input(TNa)
                TCl_val = parse_scientific_input(TCl)
                TK_val = parse_scientific_input(TK)

                if any(v is None for v in [pH_val, TCO3_val, TPO4_val, TCa_val, TMg_val, TNa_val, TCl_val, TK_val]):
                    st.error("❌ Invalid input")
                else:
                    with st.spinner("Calculating ISF..."):
                        master_conc = np.array([pH_val, TCO3_val, TPO4_val, TCa_val, TMg_val, TNa_val, TCl_val, TK_val])
                        model = BoneMineralizationModel()
                        st.session_state.isf_results = model.run_isf_simulation(master_conc, iterations)
                        st.session_state.run_isf = False
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.run_isf = False

    # ======================== SECTION 2: ODE MODEL PARAMETERS ========================
    with st.expander("🧬 **2. Biomineralization ODE Model Parameters**", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.subheader("Rate Parameters")
            k1 = st.text_input("k₁", value="0.3", key="k1_input")
            k2 = st.text_input("k₂", value="0.005", key="k2_input")
            k3_default = st.session_state.isf_results['precipitation_rate'] * (24*60*60) * 6 * 1e8 if st.session_state.isf_results else 292855.14
            k3_input = st.text_input("k₃", value=f"{k3_default:.2e}", key="k3_input")
            v1 = st.text_input("v₁", value="0.005", key="v1_input")

        with col2:
            st.subheader("Removal")
            r1_input = st.text_input("r₁", value="1e-7", key="r1_input")
            r2 = st.text_input("r₂", value="5e-10", key="r2_input")
            t1 = st.text_input("t₁", value="0", key="t1_input")
            st.write("")

        with col3:
            st.subheader("Hill Function")
            a = st.text_input("a (exponent)", value="10", key="a_input")
            b = st.text_input("b (coeff)", value="1e57", key="b_input")
            st.write("")
            st.write("")

        with col4:
            st.subheader("Initial Conditions")
            X1 = st.text_input("x₁ (progenit.)", value="9.4e5", key="X1_input")
            X2 = st.text_input("x₂ (active)", value="0", key="X2_input")
            I = st.text_input("I (inhibitor)", value="9.4e5", key="I_input")
            N = st.text_input("N (osteoclasts)", value="1", key="N_input")
            Y = st.text_input("y (mineral)", value="0", key="Y_input")

        with col5:
            st.subheader("Mode & Settings")
            model_mode = st.radio("Model Type", ["Primary", "Enhanced"], key="model_mode_radio")
            dim_mode = st.radio("Dimensionaliz.", ["No", "Yes"], key="dim_mode_radio")
            duration = st.number_input("Duration", value=100.0, min_value=1.0, step=10.0, key="duration_input")
            num_points = st.slider("Time Points", 100, 5000, 1000, 100, key="num_points_slider")

    # ======================== SECTION 3: CHARACTERISTICS (Conditional) ========================
    if st.session_state.dim_mode == "Yes" or dim_mode == "Yes":
        with st.expander("⚙️ **3. Characteristic Values (Non-Dimensionalization)**", expanded=True):
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                x1_c = st.text_input("x₁_c", value="1e6", key="x1c_input")
            with col2:
                x2_c = st.text_input("x₂_c", value="1e6", key="x2c_input")
            with col3:
                I_c = st.text_input("I_c", value="1e6", key="Ic_input")
            with col4:
                N_c = st.text_input("N_c", value="1e6", key="Nc_input")
            with col5:
                y_c = st.text_input("y_c", value="1e9", key="yc_input")
    else:
        x1_c, x2_c, I_c, N_c, y_c = "1", "1", "1", "1", "1"

    # ======================== SECTION 4: RUN SIMULATION & RESULTS ========================
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("🚀 RUN ODE SIMULATION", key="run_ode_btn", use_container_width=True):
            st.session_state.run_ode = True

    with col2:
        if st.button("Reset ODE", key="reset_ode_btn", use_container_width=True):
            st.session_state.ode_results = None
            st.rerun()

    with col3:
        if st.button("Clear All", key="clear_all_btn", use_container_width=True):
            st.session_state.isf_results = None
            st.session_state.ode_results = None
            st.rerun()

    # Run ODE if triggered
    if st.session_state.get('run_ode', False):
        try:
            # Parse inputs
            params_dict = {
                'k1': parse_scientific_input(k1),
                'k2': parse_scientific_input(k2),
                'k3': parse_scientific_input(k3_input),
                'v1': parse_scientific_input(v1),
                'r1': parse_scientific_input(r1_input),
                'r2': parse_scientific_input(r2),
                'a': parse_scientific_input(a),
                'b': parse_scientific_input(b),
                't2': parse_scientific_input(t1),
            }

            init_dict = {
                'x1': parse_scientific_input(X1),
                'x2': parse_scientific_input(X2),
                'I': parse_scientific_input(I),
                'N': parse_scientific_input(N),
                'y': parse_scientific_input(Y),
            }

            char_dict = {
                'x1_c': parse_scientific_input(str(x1_c)),
                'x2_c': parse_scientific_input(str(x2_c)),
                'I_c': parse_scientific_input(str(I_c)),
                'N_c': parse_scientific_input(str(N_c)),
                'y_c': parse_scientific_input(str(y_c)),
            }

            if any(v is None for v in params_dict.values()) or any(v is None for v in init_dict.values()):
                st.error("❌ Invalid parameter values")
            else:
                # Apply model mode
                if model_mode == "Primary":
                    params_dict['t2'] = 0
                    params_dict['r1'] = 1e-7
                else:
                    params_dict['t2'] = 8e-9
                    params_dict['r1'] = 0

                inits_raw = np.array([init_dict['x1'], init_dict['x2'], init_dict['I'], init_dict['N'], init_dict['y']])
                characteristics = np.array([char_dict['x1_c'], char_dict['x2_c'], char_dict['I_c'], char_dict['N_c'], char_dict['y_c']])
                inits_nondim = inits_raw / characteristics

                with st.spinner("Solving ODE system..."):
                    model = BoneMineralizationModel()
                    params = ModelParameters(**params_dict)
                    params_nondim = model.non_dimensionalize(params, characteristics)
                    t, solution = model.run_ode_simulation(params_nondim, inits_nondim, duration, int(num_points))
                    st.session_state.ode_results = (t, solution, inits_raw, characteristics)
                    st.session_state.run_ode = False
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.run_ode = False

    # ======================== SECTION 5: RESULTS METRICS ========================
    if st.session_state.ode_results:
        t, solution, inits_raw, characteristics = st.session_state.ode_results
        solution_scaled = solution * characteristics

        with st.expander("📈 **4. Simulation Results**", expanded=True):
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.metric("x₁ (Final)", f"{solution_scaled[-1, 0]:.2e}")
            with col2:
                st.metric("x₂ (Final)", f"{solution_scaled[-1, 1]:.2e}")
            with col3:
                st.metric("I (Final)", f"{solution_scaled[-1, 2]:.2e}")
            with col4:
                st.metric("N (Final)", f"{solution_scaled[-1, 3]:.2e}")
            with col5:
                st.metric("y (Final)", f"{solution_scaled[-1, 4]:.2e}")
            with col6:
                try:
                    analyzer = LagTimeAnalyzer()
                    peaks, transition = analyzer.calculate_lag_time(t, solution[:, 4])
                    if not np.isnan(transition) and transition > 0:
                        st.metric("Lag Time", f"{transition:.1f} days")
                    else:
                        st.metric("Lag Time", "Smooth growth")
                except:
                    st.metric("Lag Time", "N/A")

    # ======================== SECTION 6: COMPLETE VISUALIZATION (9 PANELS) ========================
    if st.session_state.ode_results:
        with st.expander("📊 **5. Complete Visualization (9 Panels)**", expanded=True):
            t, solution, inits_raw, characteristics = st.session_state.ode_results
            solution_scaled = solution * characteristics

            fig = plt.figure(figsize=(18, 14))
            gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

            # Panel 1: Mineral with lag time
            ax1 = fig.add_subplot(gs[0, 0])
            ax1.plot(t, solution_scaled[:, 4], linewidth=2.5, color='#1f77b4')
            try:
                analyzer = LagTimeAnalyzer()
                peaks, transition = analyzer.calculate_lag_time(t, solution[:, 4])
                if not np.isnan(transition) and transition > 0:
                    idx = np.argmin(np.abs(t - transition))
                    ax1.scatter([transition], [solution_scaled[idx, 4]], color='red', s=150, zorder=5, marker='*')
                    ax1.axvline(x=transition, color='red', linestyle='--', alpha=0.5)
            except:
                pass
            ax1.set_xlabel('Time (days)', fontsize=10)
            ax1.set_ylabel('Mineral (y)', fontsize=10)
            ax1.set_title('Panel 1: Mineral Accumulation', fontsize=11, fontweight='bold')
            ax1.grid(True, alpha=0.3)

            # Panel 2: Mineral normalized
            ax2 = fig.add_subplot(gs[0, 1])
            y_norm = solution_scaled[:, 4] / (np.max(solution_scaled[:, 4]) + 1e-10)
            ax2.plot(t, y_norm, linewidth=2.5, color='#ff7f0e')
            ax2.fill_between(t, 0, y_norm, alpha=0.2, color='#ff7f0e')
            ax2.set_xlabel('Time (days)', fontsize=10)
            ax2.set_ylabel('Normalized y', fontsize=10)
            ax2.set_title('Panel 2: Mineral (Normalized)', fontsize=11, fontweight='bold')
            ax2.grid(True, alpha=0.3)

            # Panel 3: Inhibitor normalized
            ax3 = fig.add_subplot(gs[0, 2])
            I_norm = solution_scaled[:, 2] / (np.max(solution_scaled[:, 2]) + 1e-10)
            ax3.plot(t, I_norm, linewidth=2.5, color='#2ca02c')
            ax3.fill_between(t, 0, I_norm, alpha=0.2, color='#2ca02c')
            ax3.set_xlabel('Time (days)', fontsize=10)
            ax3.set_ylabel('Normalized I', fontsize=10)
            ax3.set_title('Panel 3: Inhibitor (Normalized)', fontsize=11, fontweight='bold')
            ax3.grid(True, alpha=0.3)

            # Panel 4: Osteoclasts normalized
            ax4 = fig.add_subplot(gs[1, 0])
            N_norm = solution_scaled[:, 3] / (np.max(solution_scaled[:, 3]) + 1e-10)
            ax4.plot(t, N_norm, linewidth=2.5, color='#d62728')
            ax4.set_xlabel('Time (days)', fontsize=10)
            ax4.set_ylabel('Normalized N', fontsize=10)
            ax4.set_title('Panel 4: Osteoclasts (Normalized)', fontsize=11, fontweight='bold')
            ax4.grid(True, alpha=0.3)

            # Panel 5: Osteoclasts raw
            ax5 = fig.add_subplot(gs[1, 1])
            ax5.plot(t, solution_scaled[:, 3], linewidth=2.5, color='#9467bd')
            ax5.set_xlabel('Time (days)', fontsize=10)
            ax5.set_ylabel('N (Raw)', fontsize=10)
            ax5.set_title('Panel 5: Osteoclasts (Raw)', fontsize=11, fontweight='bold')
            ax5.grid(True, alpha=0.3)

            # Panel 6: Inhibitor raw
            ax6 = fig.add_subplot(gs[1, 2])
            ax6.plot(t, solution_scaled[:, 2], linewidth=2.5, color='#8c564b')
            ax6.set_xlabel('Time (days)', fontsize=10)
            ax6.set_ylabel('I (Raw)', fontsize=10)
            ax6.set_title('Panel 6: Inhibitor (Raw)', fontsize=11, fontweight='bold')
            ax6.grid(True, alpha=0.3)

            # Panel 7: Osteoblasts
            ax7 = fig.add_subplot(gs[2, 0])
            x1_norm = solution_scaled[:, 0] / (np.max(solution_scaled[:, 0]) + 1e-10)
            x2_norm = solution_scaled[:, 1] / (np.max(solution_scaled[:, 1]) + 1e-10)
            ax7.plot(t, x1_norm, linewidth=2.5, label='x₁', color='#1f77b4')
            ax7.plot(t, x2_norm, linewidth=2.5, label='x₂', color='#ff7f0e')
            ax7.set_xlabel('Time (days)', fontsize=10)
            ax7.set_ylabel('Normalized Pop.', fontsize=10)
            ax7.set_title('Panel 7: Osteoblasts', fontsize=11, fontweight='bold')
            ax7.legend(fontsize=9)
            ax7.grid(True, alpha=0.3)

            # Panel 8: All variables normalized
            ax8 = fig.add_subplot(gs[2, 1])
            ax8.plot(t, x1_norm, linewidth=2, label='x₁', alpha=0.8)
            ax8.plot(t, x2_norm, linewidth=2, label='x₂', alpha=0.8)
            ax8.plot(t, I_norm, linewidth=2, label='I', alpha=0.8)
            ax8.plot(t, N_norm, linewidth=2, label='N', alpha=0.8)
            ax8.plot(t, y_norm, linewidth=2.5, label='y', alpha=0.9)
            ax8.set_xlabel('Time (days)', fontsize=10)
            ax8.set_ylabel('Normalized Value', fontsize=10)
            ax8.set_title('Panel 8: All Variables (Normalized)', fontsize=11, fontweight='bold')
            ax8.legend(fontsize=9)
            ax8.grid(True, alpha=0.3)

            # Panel 9: Derivative
            ax9 = fig.add_subplot(gs[2, 2])
            dy_dt = np.diff(solution_scaled[:, 4]) / np.diff(t)
            ax9.plot(t[1:], dy_dt, linewidth=2.5, color='#17becf')
            ax9.fill_between(t[1:], 0, dy_dt, alpha=0.2, color='#17becf')
            ax9.set_xlabel('Time (days)', fontsize=10)
            ax9.set_ylabel('dy/dt', fontsize=10)
            ax9.set_title('Panel 9: Mineralization Rate', fontsize=11, fontweight='bold')
            ax9.grid(True, alpha=0.3)

            st.pyplot(fig, use_container_width=True)

            # Export button
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("📥 Download CSV", use_container_width=True):
                    import io
                    buffer = io.StringIO()
                    buffer.write("Time,x1,x2,I,N,y\n")
                    for i, ti in enumerate(t):
                        buffer.write(f"{ti},{solution_scaled[i,0]},{solution_scaled[i,1]},{solution_scaled[i,2]},{solution_scaled[i,3]},{solution_scaled[i,4]}\n")
                    st.download_button(
                        label="Click here to download",
                        data=buffer.getvalue(),
                        file_name="bone_mineralization_results.csv",
                        mime="text/csv"
                    )
            with col2:
                st.info("✅ Results ready for export")

    # ======================== FOOTER ========================
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Citation:** Poorhemati & Komarova (2024), Scientific Reports")
    with col2:
        st.markdown("**Source:** [GitHub](https://github.com/Hosseinpoorhemati/bone_mineralization_integrated)")
    with col3:
        st.markdown("**Python Version:** Complete MATLAB Feature Parity ✅")


if __name__ == "__main__":
    main()
