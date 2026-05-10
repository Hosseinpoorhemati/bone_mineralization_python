# 📄 Single Page Layout - Complete Guide

## Overview
The new `app_single.py` provides a **single-page interface** where users can see everything they need without switching between tabs. All controls, parameters, and results are organized in collapsible sections.

---

## Layout Structure

### **Section 1: ISF Equilibrium (Physicochemical)**
**Location:** Top of page, expandable section
**4-Column Layout:**

**Column 1:** Ion Concentrations
- pH input
- TCO₃ input
- TPO₄ input
- TCa input

**Column 2:** More Ions
- TMg input
- TNa input
- TCl input
- TK input

**Column 3:** ISF Settings
- Newton-Raphson Tolerance selector
- Max Iterations slider
- "🚀 Run ISF" button
- "Reset ISF" button

**Column 4:** ISF Results (Live)
- Initial pH metric
- Final pH metric
- Saturation Ratio metric
- Precipitation Rate metric
- Shows "Click 'Run ISF' to calculate" until results available

---

### **Section 2: Biomineralization ODE Model Parameters**
**Location:** Below ISF, expandable section
**5-Column Layout:**

**Column 1:** Rate Parameters
- k₁ input
- k₂ input
- k₃ input (auto-filled from ISF if available)
- v₁ input

**Column 2:** Removal Parameters
- r₁ input
- r₂ input
- t₁ input

**Column 3:** Hill Function
- a (exponent) input
- b (coefficient) input

**Column 4:** Initial Conditions
- x₁ (progenitors) input
- x₂ (active) input
- I (inhibitor) input
- N (osteoclasts) input
- y (mineral) input

**Column 5:** Mode & Settings
- Model Type radio (Primary/Enhanced)
- Dimensionalization radio (Yes/No)
- Duration number input
- Time Points slider

---

### **Section 3: Characteristic Values (Conditional)**
**Location:** Below parameters, only appears when "Dimensionalization = Yes"
**5-Column Layout:**

- x₁_c (characteristic x₁)
- x₂_c (characteristic x₂)
- I_c (characteristic I)
- N_c (characteristic N)
- y_c (characteristic y)

---

### **Section 4: Control Buttons**
**Location:** Below characteristics
**3-Column Layout:**

- **Column 1:** "🚀 RUN ODE SIMULATION" button (full width)
- **Column 2:** "Reset ODE" button
- **Column 3:** "Clear All" button

---

### **Section 5: Results Metrics**
**Location:** Below buttons, only shows after ODE runs
**6-Column Layout (metrics):**

- x₁ (Final) metric
- x₂ (Final) metric
- I (Final) metric
- N (Final) metric
- y (Final) metric
- Lag Time metric (detected or "Smooth growth")

---

### **Section 6: Complete Visualization (9 Panels)**
**Location:** Bottom of page, expandable section
**Layout:** 3×3 grid of plots

**Row 1:**
- Panel 1: Mineral accumulation with lag time marked
- Panel 2: Normalized mineral
- Panel 3: Normalized inhibitor

**Row 2:**
- Panel 4: Normalized osteoclasts
- Panel 5: Raw osteoclasts
- Panel 6: Raw inhibitor

**Row 3:**
- Panel 7: Osteoblasts (x₁ and x₂)
- Panel 8: All variables together
- Panel 9: Mineralization rate (dy/dt)

**Below Plots:**
- "📥 Download CSV" button
- "✅ Results ready for export" info box

---

## User Workflow

### Typical Usage Flow:
1. **Scroll to Section 1** - Enter ISF ion concentrations
2. **Click "Run ISF"** - Get saturation ratio and precipitation rate
3. **Scroll to Section 2** - ODE parameters auto-fill k₃ from ISF
4. **Adjust parameters** as needed
5. **Choose Model Type** (Primary/Enhanced)
6. **Toggle Dimensionalization** if needed (shows Section 3)
7. **Enter Characteristics** if dimensionalized
8. **Click "Run ODE Simulation"** at the bottom of Section 2
9. **View Results** automatically appear in Sections 5 & 6
10. **Download CSV** from the export button

---

## Benefits of Single-Page Layout

✅ **Unified View:** See ISF inputs, ODE parameters, and all results at once
✅ **Expandable Sections:** Collapse sections you don't need to focus on what matters
✅ **Live Results:** ISF and ODE results appear right next to their inputs
✅ **Better Workflow:** No tab-switching - everything flows naturally
✅ **Responsive:** Auto-fills k₃ from ISF into ODE section
✅ **Compact:** Uses Streamlit columns for efficient space usage
✅ **Clear Organization:** 6 logical sections in order of workflow

---

## Visual Organization

```
┌─────────────────────────────────────────────────────────────┐
│ 🦴 Bone Mineralization Integrated Model (Single Page)        │
└─────────────────────────────────────────────────────────────┘

┌─ SECTION 1: ISF EQUILIBRIUM (Expandable) ──────────────────┐
│ [Col1: Ions] [Col2: More Ions] [Col3: Settings] [Col4: Results]
└─────────────────────────────────────────────────────────────┘

┌─ SECTION 2: ODE PARAMETERS (Expandable) ──────────────────┐
│ [Col1: Rates] [Col2: Removal] [Col3: Hill] [Col4: Init] [Col5: Mode]
└─────────────────────────────────────────────────────────────┘

┌─ SECTION 3: CHARACTERISTICS (Conditional, Expandable) ──────┐
│ [x1_c] [x2_c] [I_c] [N_c] [y_c]
└─────────────────────────────────────────────────────────────┘

┌─ CONTROL BUTTONS ──────────────────────────────────────────┐
│ [🚀 RUN ODE SIMULATION] [Reset ODE] [Clear All]
└─────────────────────────────────────────────────────────────┘

┌─ SECTION 5: RESULTS METRICS (When ODE runs) ──────────────┐
│ [x₁] [x₂] [I] [N] [y] [Lag Time]
└─────────────────────────────────────────────────────────────┘

┌─ SECTION 6: VISUALIZATION (9 Panels, Expandable) ─────────┐
│                      ┌─────────────┬─────────────┬─────────────┐
│                      │ Panel 1     │ Panel 2     │ Panel 3     │
│                      ├─────────────┼─────────────┼─────────────┤
│                      │ Panel 4     │ Panel 5     │ Panel 6     │
│                      ├─────────────┼─────────────┼─────────────┤
│                      │ Panel 7     │ Panel 8     │ Panel 9     │
│                      └─────────────┴─────────────┴─────────────┘
│ [📥 Download CSV]
└─────────────────────────────────────────────────────────────┘

┌─ FOOTER ──────────────────────────────────────────────────┐
│ Citation | Source | Version Info
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Smart Features:
- ✅ **Auto-fill k₃:** ISF result automatically populates k₃ field
- ✅ **Conditional UI:** Characteristics only appear when "Dimensionalization = Yes"
- ✅ **Live Updates:** Results update immediately when ODE finishes
- ✅ **Expandable:** Collapse sections to reduce clutter
- ✅ **Error Handling:** Graceful handling of invalid inputs
- ✅ **Export:** Easy CSV download of all results

### Visual Improvements:
- ✅ **Color-coded plots:** Each variable has distinct color
- ✅ **Normalized & Raw:** Side-by-side comparisons
- ✅ **Lag time visualization:** Marked with star and dashed line
- ✅ **Filled areas:** Showing accumulation/depletion
- ✅ **High resolution:** 18×14 figure size for clarity
- ✅ **Grid lines:** Subtle grid for easier reading

---

## User Experience Improvements

### Before (Multi-Tab):
- Had to switch between ISF, ODE, Analysis, About tabs
- Results far from inputs
- Harder to relate ISF results to ODE parameters
- Needed to go back and forth to adjust values

### After (Single Page):
- Everything visible (with smart collapse)
- Results right next to inputs
- Easy to adjust any parameter and re-run
- Natural top-to-bottom workflow
- Perfect for presentations or teaching

---

## Running the Single-Page App

```bash
./run.sh              # macOS/Linux
# or
run.bat              # Windows
# or
streamlit run app_single.py
```

Then open: **http://localhost:8501**

---

## Tips for Users

1. **Start with ISF:** Run ISF first to get accurate k₃ from precipitation rate
2. **Check defaults:** Primary mode has different r₁ and t₁ than Enhanced
3. **Use scientif notation:** Any field accepts 1e-10, 5e-3, 1e56, etc.
4. **Collapse when done:** Collapse ISF section after running if you want to focus on ODE
5. **Watch k₃ auto-fill:** When you run ISF, it automatically updates k₃
6. **Export early:** Download CSV before making new changes
7. **Try both modes:** Run with Primary and Enhanced to compare

---

**Version:** Single Page Layout v1.0
**Status:** ✅ Production Ready
**Better for:** Usability, workflow, presentations
