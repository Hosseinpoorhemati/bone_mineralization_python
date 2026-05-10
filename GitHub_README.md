# 🦴 Bone Mineralization Integrated Model - Python Edition

**A complete Python implementation of the bone mineralization mathematical model** with an interactive Streamlit web interface.

[![Open in Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bone-mineralization.streamlit.app)

## 📖 Overview

This is a **faithful Python translation** of the MATLAB bone mineralization simulator developed at McGill University (Poorhemati & Komarova, 2024). The model combines physicochemical and biological factors that regulate bone mineralization.

**Key Features:**
- ✅ Complete Newton-Raphson solver for ionic equilibrium (ISF)
- ✅ 5-variable coupled ODE system for biomineralization dynamics
- ✅ Dimensionalized and non-dimensionalized model modes
- ✅ Support for scientific notation (10^-300 to 10^300)
- ✅ Interactive web interface (no MATLAB required!)
- ✅ 9-panel visualization of all dynamics
- ✅ Real-time parameter adjustment
- ✅ CSV data export

## 🚀 Quick Start

### Online (Streamlit Cloud - No Installation)
Click the badge above to open in your browser instantly!

### Local Installation

**Requirements:**
- Python 3.8+
- pip

**Install and run:**
```bash
# Clone repository
git clone https://github.com/Hosseinpoorhemati/bone_mineralization_python.git
cd bone_mineralization_python

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_single.py
```

Opens at: **http://localhost:8501**

## 📊 How It Works

### Two Main Components

**1. ISF Equilibrium Module**
- Calculates ionic equilibrium in interstitial fluid
- Uses Newton-Raphson solver with activity corrections
- Determines HAP saturation state
- Predicts precipitation rates

**2. Biomineralization ODE Model**
- Tracks 5 biological variables:
  - x₁: Progenitor osteoblasts
  - x₂: Active osteoblasts
  - I: Inhibitor concentration
  - N: Osteoclasts
  - y: Mineral content
- Supports two model modes: Primary and Enhanced
- Full non-dimensionalization capability

## 🎯 Single-Page Interface

Everything on one page for maximum usability:

1. **ISF Equilibrium** (Section 1)
   - Input ion concentrations
   - Automatic conversion to ODE units
   - View saturation ratio and precipitation rate

2. **ODE Parameters** (Section 2)
   - All rate constants (k1, k2, k3, v1, r1, r2, a, b, t1)
   - Initial conditions (x1, x2, I, N, y)
   - Model mode selection (Primary/Enhanced)
   - Dimensionalization toggle

3. **Characteristics** (Section 3, conditional)
   - Scaling factors for non-dimensionalization
   - Only shows when needed

4. **Results & Visualization** (Sections 4-6)
   - Live result metrics (final values, lag time)
   - 9-panel plot grid
   - All variables shown normalized and raw
   - CSV export

## 📈 Example Workflow

```
1. Enter ISF parameters (pH, ion concentrations)
   ↓
2. Click "Run ISF" → see saturation ratio
   ↓
3. k₃ auto-fills in ODE section
   ↓
4. Adjust ODE parameters as needed
   ↓
5. Click "Run ODE Simulation"
   ↓
6. View all 9 plots and metrics
   ↓
7. Download CSV with results
```

## 🧪 Scientific Features

### ISF Equilibrium
- **Solver:** Newton-Raphson with iterative activity correction
- **Equilibrium Constants:** 22 ion equilibria at 37°C
- **Activity Model:** Davies equation for ionic strength corrections
- **Saturation:** HAP saturation ratio (Ksp = 2.03×10⁻⁵⁹)
- **Kinetics:** Precipitation rate based on saturation

### ODE System
```
dx₁/dt = -k₁·x₁
dx₂/dt = k₁·x₁
dI/dt = v₁·x₁ - r₁·x₂·I - t₂·(k₃·H(I)·N)·I
dN/dt = k₂·(k₁·x₁) - r₂·N·(k₃·H(I)·N)
dy/dt = k₃·H(I)·N

where H(x) = b/(b+x^a) is the Hill function
```

### Non-Dimensionalization
- Automatic scaling by characteristic values
- Maintains physical meaning of variables
- Improves numerical stability

## 📊 Default Values

### ISF (Blood-like)
```
pH = 7.4
TCO3 = 0.027 mol/L
TPO4 = 0.001 mol/L
TCa = 0.0016 mol/L
TMg = 0.001 mol/L
TNa = 0.142 mol/L
TCl = 0.103 mol/L
TK = 0.005 mol/L
```

### ODE (Manuscript Values)
**Primary Mode:**
- k₁ = 0.3, k₂ = 0.005, k₃ = 292,855
- v₁ = 0.005, r₁ = 1e-7, r₂ = 5e-10
- a = 10, b = 1e57, t₁ = 0

**Enhanced Mode:** Same except r₁ = 0, t₁ = 8e-9

### Characteristics
- x₁_c = 1e6
- x₂_c = 1e6
- I_c = 1e6
- N_c = 1e6
- y_c = 1e9

## 🔬 Verification

Results **numerically identical** to original MATLAB:
- ✅ ISF equilibrium calculations
- ✅ ODE integration
- ✅ Parameter non-dimensionalization
- ✅ Lag time detection
- ✅ All intermediate values

## 📚 Documentation

- **START_HERE.md** - Quick overview (5 min)
- **QUICKSTART.md** - Getting started (10 min)
- **README.md** - Full technical docs
- **FEATURES_COMPLETE.md** - Feature parity checklist
- **SINGLE_PAGE_LAYOUT.md** - UI layout guide
- **BUGFIX_SUMMARY.md** - Implementation details

## 🎓 Scientific Background

This model mathematically describes:
- Physicochemical regulation (ion equilibrium, saturation)
- Biological regulation (cell populations, inhibitors)
- Mineralization kinetics (hydroxyapatite precipitation)

The implementation is based on:
> **Poorhemati, H., & Komarova, S. V. (2024)**
> Mathematical model capturing physicochemical and biological regulation of bone mineralization
> *Scientific Reports*, 14(1)
> https://www.nature.com/articles/s41598-024-81472-1

## 💻 Technology Stack

- **Python 3.8+** - Core language
- **NumPy** - Numerical computing
- **SciPy** - Scientific algorithms (ODE solver, optimization)
- **Matplotlib** - Visualization
- **Streamlit** - Web interface

All open-source, free, and cross-platform!

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. **Fork this repository** on GitHub
2. Go to [streamlit.io/cloud](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file: `app_single.py`
6. Click "Deploy"

Done! Your app is live and shareable via URL.

### Self-Hosted

```bash
# Install streamlit
pip install streamlit

# Run anywhere
streamlit run app_single.py --server.port 8501
```

## 📋 System Requirements

- **Minimum:** Python 3.8, 200MB RAM, 50MB disk
- **Recommended:** Python 3.10+, 512MB RAM, 100MB disk
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)
- **Network:** No internet required (fully local)

## ✨ Advantages Over MATLAB Version

| Feature | MATLAB | Python |
|---------|--------|--------|
| Installation | ✅ (but expensive) | ✅ (free) |
| Learning curve | ⚠️ (complex) | ✅ (simpler) |
| Web interface | ❌ | ✅ |
| Cross-platform | ⚠️ (Windows/Mac) | ✅ (all) |
| Open source | ❌ | ✅ |
| Community | ⚠️ (academic) | ✅ (large) |
| Sharing | ❌ (files) | ✅ (cloud link) |
| Customization | ⚠️ (AppDesigner) | ✅ (Streamlit) |

## 🤝 Contributing

Found a bug? Want to add a feature? 
- Open an issue
- Submit a pull request
- Share suggestions

## 📄 License

This Python implementation maintains the same spirit as the original MATLAB code. 

**Please cite the original work:**
```bibtex
@article{Poorhemati2024,
  author = {Poorhemati, H. and Komarova, S. V.},
  year = {2024},
  title = {Mathematical model capturing physicochemical and biological regulation of bone mineralization},
  journal = {Scientific Reports},
  volume = {14},
  number = {1}
}
```

## 📧 Contact

**Original MATLAB Developer:**
- Hossein Poorhemati (hossein.poorhemati@mail.mcgill.ca)
- McGill University

**Python Port:**
- Faithfully converted with full mathematical verification
- All features from original MATLAB app included

## 🎉 Try It Now!

### Online (No Installation):
[![Open in Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bone-mineralization.streamlit.app)

### Local:
```bash
git clone <repo>
cd bone_mineralization_python
pip install -r requirements.txt
streamlit run app_single.py
```

**Happy exploring!** 🦴

---

**Version:** 2.0 (Single-Page Layout)
**Status:** ✅ Production Ready
**Last Updated:** 2026-05-05
**Python:** 3.8+
**License:** Academic/Research Use
