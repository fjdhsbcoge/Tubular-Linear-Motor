# Force Profile Data

This directory contains FEMM simulation results for different coil configurations.

## Files

### Force Profile CSVs

| File | Description |
|------|-------------|
| `force_profile_1_layer.csv` | Single-layer coil configuration (detailed) |
| `force_profile_4_layer.csv` | 4-layer coil configuration |
| `force_profile_6_layer.csv` | 6-layer coil configuration |

### Source Data

| File | Description |
|------|-------------|
| `260331 Coil Config and Force Profile.xlsx` | Original Excel data (3 sheets) |

**Excel Sheets:**
1. **Sheet 1**: 6-layer config - Position, Fx, Fy, Phase contributions
2. **Sheet 2**: 1-layer config - Detailed force vs. position
3. **Sheet 3**: 4-layer config - Intermediate analysis

## Data Format

All CSV files contain:
- **Position_mm**: Linear position along motor axis (mm)
- **Fx_N** / **Fy_N**: Force components in X/Y directions (Newtons)
- Columns A, B, C: Individual phase contributions
- **Insgesamt** / **Umfang [mm]**: Total/circumference data

## Key Findings

### 1-Layer Configuration
- **Most detailed data**: 202 data points
- **Position range**: 0-400 mm
- Shows complete force waveform

### 6-Layer Configuration
- Position range: 0-20 mm
- 20 data points
- Shows 3-phase contributions clearly

### 4-Layer Configuration
- Position range: 0-222 mm
- 27 data points
- Intermediate configuration analysis

## Usage

### Quick Plot (Python)
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("force_profile_1_layer.csv")
plt.plot(df["Position_mm"], df["Fx_N"])
plt.xlabel("Position [mm]")
plt.ylabel("Force Fx [N]")
plt.title("Force Profile - 1 Layer")
plt.grid(True)
plt.show()
```

### Excel Analysis
Open `260331 Coil Config and Force Profile.xlsx` for:
- Original data formatting
- Multiple configuration comparison
- Phase contribution analysis

## Source

Data generated using **FEMM (Finite Element Method Magnetics)** simulations.

Simulation methodology:
1. Model 1mm axial slice in 2D
2. Calculate forces via Maxwell stress tensor
3. Multiply by circumference (87.976 mm) for total force
4. Vary mover position to generate ripple profile

See `/simulations/` for FEMM project files and Lua automation scripts.
