# 🚀 Quick Start Guide

## 30 Seconds to Running

### Option 1: Automated Launch (Recommended)

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

### Option 2: Manual Launch

```bash
# Install dependencies (one time only)
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## What Happens Next

1. A web browser will open automatically
2. Navigate to **http://localhost:8501** if it doesn't
3. You'll see the simulator interface

## Basic Workflow

### 1️⃣ ISF Equilibrium Tab
- Enter blood-like ion concentrations (defaults already set)
- Click **Run ISF Equilibrium**
- View results: pH, saturation ratio, precipitation rate

### 2️⃣ ODE Model Tab
- Adjust biological parameters (or use defaults)
- Set simulation duration (100 time units recommended)
- Click **Run ODE Simulation**
- Watch cells and mineral dynamics unfold

### 3️⃣ Analysis Tab
- View lag time analysis
- Explore phase space plots
- Calculate mineralization efficiency

## 📊 Example Scenarios

**Scenario 1: Normal Bone Mineralization**
- Keep default parameters
- Run ISF: saturation ratio ~49 (highly supersaturated)
- Run ODE: observe mineral accumulation

**Scenario 2: Slow Mineralization**
- Decrease k₃ (mineralization rate) to 0.005
- Run ODE to see reduced mineral deposition

**Scenario 3: Acidic Conditions**
- Decrease pH to 7.0 in ISF tab
- Observe how acidity affects saturation

## 🆘 Troubleshooting

**"Command not found: streamlit"**
```bash
pip install streamlit
```

**"ModuleNotFoundError: No module named..."**
```bash
pip install -r requirements.txt
```

**Browser won't open**
- Manually visit: http://localhost:8501

**Slow computations**
- Reduce simulation duration
- Use fewer time points (1000 instead of 5000)

## 📚 Next Steps

1. Read the **About** tab in the app for detailed theory
2. Check **README.md** for comprehensive documentation
3. Explore parameter sensitivity
4. Compare ISF results with different pH values

## ✨ Key Insights

- **Saturation Ratio > 1** = HAP will precipitate (mineralization occurs)
- **k₃ parameter** = Controls how fast mineralization happens
- **Inhibitor (I)** = Regulates the process (high I slows mineralization)
- **Lag time** = When mineralization transitions to rapid phase

---

**Having issues?** Check README.md for detailed troubleshooting and system requirements.
