# Tubular Linear Motor

Open-source tubular linear motor with FOC control.

## CAD Design

Cross-sectional view showing the internal structure with stator magnets and coil arrangement:

![Design View 1 - Cross Section](images/design_view_1.png)

3D render showing the complete mover assembly with copper windings and carbon fiber housing:

![Design View 2 - 3D Render](images/design_view_2.png)

## Magnetic Field Simulations

The motor operates on a magnetic gearing principle where two sine-wave fields interlock like gear teeth. FEMM simulations visualize this interaction: field lines show the flux paths from the stator magnets, while the B-field plots demonstrate the sinusoidal pattern that creates the "magnetic gear rack" the mover engages with.

![Field Lines](simulations/images/femm_field_lines.png)
*Magnetic field lines from the stator permanent magnets*

![B-Field Plot](simulations/images/femm_field_lines_mover.png)
*Flux density along the mover length*

![Stator Field](simulations/images/stator_field_sinusoidal.jpg)
*Sinusoidal B-field along the stator — each period corresponds to one pole pair (N-S), forming the "teeth" of the magnetic gear*

## BLDC Star-Connected Motor Simulation

This simulation demonstrates how unipolar 0-4V PWM voltages from a SimpleFOC driver create bipolar currents and a rotating magnetic field in a star-connected motor. The floating neutral point mechanism allows unipolar driver outputs to generate the bipolar currents necessary for proper motor operation.

![MMK Overview](simulations/images/mmk_overview.png)
*Overview of driver voltages, neutral point voltage, phase currents, and the resulting traveling MMK wave. Note how the 0-4V unipolar output creates ±0.5A bipolar currents through the floating neutral mechanism.*

![Spatial MMK Distribution](simulations/images/mmk_spatial_with_bars.png)
*Spatial MMK distribution at different electrical angles (0° to 180°). The six coils (A-b-C-a-B-c) create a traveling wave that rotates the magnetic field. Individual coil contributions (dashed) sum to form the resultant MMK (solid black line). Red stars mark the sum at θ=0°, verifying the calculation (e.g., +0.724 at ωt=30°, +1.500 at ωt=90°).*

- **Stator**: Permanent magnets create outward sine-wave field
- **Mover**: 3-phase coils create traveling inward field  
- **Result**: Fields mesh, producing linear force

## Specs

### General Parameters

| Parameter | Value |
|-----------|-------|
| Diameter | 24 mm |
| Pole Pitch | 30 mm (N-to-N) |
| Circumference | 81.68 mm |
| Phases | 3, star-connected |
| Control | FOC |

### Mover (Test Setup)

| Parameter | Value |
|-----------|-------|
| Magnet Diameter | 18 mm |
| Coil Diameter | 25 mm - 35 mm |
| Coil Configuration | 15 × 5 mm segments |
| Total Coil Length | 90 mm |
| **Simulated Force** | **60 N at 2 A** |

> **Note:** With higher financial effort (better magnetic materials, optimized coil winding, enhanced cooling), the design can be pushed to achieve significantly higher forces.

## Documentation

| Document | Content |
|----------|---------|
| [docs/PRINCIPLE.md](docs/PRINCIPLE.md) | Physics explanation |
| [docs/WINDING_CONFIG.md](docs/WINDING_CONFIG.md) | 3-phase winding theory |
| [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) | Design parameters |
| [docs/BUILDING.md](docs/BUILDING.md) | Construction guide |

## Repository

```
├── docs/               # Documentation
├── cad/                # CAD files (.step, .f3z)
├── simulations/        # FEMM files
├── data/               # Force profiles (Excel + CSV)
└── images/             # 3D renders
```

## Key Files

- `data/260331 Coil Config and Force Profile.xlsx` — Winding config & force calculations
- `cad/24mm eine Achse SIM.step` — CAD geometry
- `simulations/config1_20mm.FEM` — FEMM project

## License

See [LICENSE](LICENSE).

---

*Pole pitch 30mm, 24mm diameter, 3-phase FOC control.*
