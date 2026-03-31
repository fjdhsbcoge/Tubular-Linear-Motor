# FEMM Simulations

This directory contains FEMM simulation files.

## Files

| File | Description |
|------|-------------|
| `config1_20mm.FEM/.ans` | Phase A excited |
| `config1_20mm_phaseB.FEM/.ans` | Phase B excited |
| `config1_20mm_phaseC.FEM/.ans` | Phase C excited |
| `linearMotorThreephase.mo` | Modelica circuit model (R=5.6Ω, L=1.15mH) |
| `Config1_forceripple.lua` | Force ripple automation scripts |

## Method

1mm slice simulated in 2D, forces multiplied by circumference (81.68 mm).

## Results

- Peak B-field: ~0.02 T
- Field pattern: Sine wave, 30 mm period
- See `images/` for field visualizations

## Materials

- N40 magnets: Hc = 970 kA/m
- 1006 Steel: μr = 1404
- 0.4 mm Litz wire

See `FILE_GUIDE.md` for detailed file descriptions.
