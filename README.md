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

This simulation demonstrates how unipolar 0-4V PWM voltages from a SimpleFOC driver create bipolar currents and force in a star-connected **tubular linear motor**. Unlike a rotating motor where coils are angularly distributed, here the 6 coils are spaced **along the motor length** (0, 5, 10, 15, 20, 25 mm), each interacting with the **local** sinusoidal B-field from the stator magnets.

![Linear Motor Overview](simulations/images/linear_motor_overview.png)
*Top-left: Static sinusoidal B-field from stator magnets (period = 30 mm pole pitch). Top-right: Bipolar phase currents (±0.5A). Bottom-left: Traveling MMK wave moving along motor length. Bottom-right: Resultant force on mover.*

![Linear Motor Snapshots](simulations/images/linear_motor_snapshots.png)
*MMK distribution (red bars) interacting with stator B-field (blue curve) at different electrical angles. Force = Σ(MMK × B) at each coil position. At ωt=0°, force peaks at +0.750 N; at ωt=180°, it reverses to -0.750 N. With FOC, the mover tracks the field to maintain continuous force.*

**Key insight:** In a linear motor, each coil produces force proportional to its MMK × local B-field. The sum of all 6 coil forces drives the mover. The floating neutral mechanism converts unipolar 0-4V PWM into bipolar ±0.5A currents, creating the traveling MMK wave that "locks" into the stator field.

- **Stator**: Permanent magnets create outward sine-wave B-field (static)
- **Mover**: 6 coils in AbCaBc pattern create traveling MMK wave
- **Force**: Sum of local MMK × B interactions at each coil position

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
