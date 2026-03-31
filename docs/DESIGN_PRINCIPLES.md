# Design Principles

## System Specs

| Parameter | Value | Source |
|-----------|-------|--------|
| Outer Diameter | 24 mm | CAD |
| Pole Pitch (N-to-N) | 30 mm | Excel |
| Pole Width (N-to-S) | 15 mm | Excel |
| Circumference | 81.68 mm | FEMM |
| Coil Width | 5 mm (30/6) | Design rule |

## Materials

| Component | Material | Key Properties |
|-----------|----------|----------------|
| Magnets | N40 | Hc = 970 kA/m, Br = 1.3 T |
| Steel | 1006 | μr = 1404, B-H curve in FEMM |
| Wire | 0.4 mm Litz | σ = 58 MS/m |

## Electrical

From FEMM/Excel:
- R = 5.6 Ω
- L = 1.15 mH  
- M = -0.46 mH

## Coil Configuration

18 coils total: **A-b-C-a-B-c** repeating pattern
- Uppercase = clockwise
- Lowercase = counter-clockwise
- 6 coils per phase

Phase shifts: 150° (A→B), 90° (A→C) — optimized for this winding

## Force Data

From Excel calculations (`data/260331 Coil Config and Force Profile.xlsx`):
- **Config1**: Peak Fx ~0.6 N per phase
- **Config2**: Peak Fx ~0.5 N per phase
- Period: 30 mm (matches pole pitch)

See `/data/` for CSV exports.

---

*For full winding theory, see WINDING_CONFIG.md. For build instructions, see BUILDING.md.*
