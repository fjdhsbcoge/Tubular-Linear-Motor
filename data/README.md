# Force Profile Data

This directory contains FEMM simulation results for different coil configurations.

## Files

### force_profile_6_layer.csv
Force profile for 6-layer coil configuration.
- Position range: 0-20 mm
- Shows Fx, Fy force components for each phase (A, B, C)

### force_profile_1_layer.csv
Force profile for single-layer coil configuration.
- Position range: 0-400 mm (detailed analysis)
- Complete force waveform data

### force_profile_4_layer.csv
Force profile for 4-layer coil configuration.
- Position range: 0-222 mm
- Intermediate layer count analysis

## Data Format

All CSV files contain:
- **Position_mm**: Linear position along motor axis (mm)
- **Fx_N** / **Fy_N**: Force components in X/Y directions (Newtons)
- Columns A, B, C: Individual phase contributions
- **Insgesamt** / **Umfang [mm]**: Total/circumference data

## Usage

These files can be used to:
1. Plot force vs. position curves
2. Analyze cogging torque
3. Verify design calculations
4. Compare different layer configurations

## Visualization

Example Python code to plot:
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("force_profile_1_layer.csv")
plt.plot(df["Position_mm"], df["Fx_N"])
plt.xlabel("Position [mm]")
plt.ylabel("Force Fx [N]")
plt.title("Force Profile")
plt.show()
```

## Source

Data generated using FEMM (Finite Element Method Magnetics) simulations.
