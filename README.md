# Tubular Linear Motor

Open-source tubular linear motor with FOC control. **Parametric design** — scalable dimensions with invariant ratios.

## Design Overview

This project provides a **general parametric design** for tubular linear motors that can be scaled to different sizes while maintaining proper field geometry. The repository also documents a **specific test setup** being built for initial verification.

### Parametric Design Principles

The motor follows these invariant relationships:

| Ratio | Value | Description |
|-------|-------|-------------|
| Coil width / Pole pitch | 1/6 | 6 coils per pole pitch (AbCaBc) |
| Spacer width / Magnet width | 0.9–1.2 | Flux shaping optimization |
| Edge rounding | ~5 × disk diameter | Sinusoidal field formation |

**General Formula:**
```
Mover: AbCaBc repeated X times
Width of one AbCaBc block = Pole pitch (λ)
Total mover length = X × λ
```

### Test Setup (Being Verified)

The simulations and CAD files in this repository represent a specific test configuration:

| Parameter | Value |
|-----------|-------|
| Outer Diameter | 24 mm |
| Pole Pitch (λ) | 30 mm |
| Coil Width | 5 mm (λ/6) |
| Mover Length | 90 mm (3× λ) |
| Simulated Force | 60 N at 2 A |

See [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) for complete scaling guidelines and how to choose electrical parameters (resistance, inductance) based on driver capabilities and force requirements.

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

## BLDC Star-Connected Motor Simulation (Test Setup)

This simulation demonstrates how unipolar 0-4V PWM voltages from a SimpleFOC driver create bipolar currents and force. It models the **test setup** configuration (30mm pole pitch, 6 coils spanning one pole pitch). The general parametric design allows scaling — see [DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md).

Unlike a rotating motor where coils are angularly distributed, here the 6 coils are spaced **along the motor length** (0, 5, 10, 15, 20, 25 mm), each interacting with the **local** sinusoidal B-field from the stator magnets.

![Linear Motor Overview](simulations/images/linear_motor_overview.png)
*Top-left: Static sinusoidal B-field from stator magnets (period = 30 mm pole pitch). Top-right: Bipolar phase currents (±0.5A). Bottom-left: Traveling MMK wave moving along motor length. Bottom-right: Resultant force on mover.*

![Linear Motor Snapshots](simulations/images/linear_motor_snapshots.png)
*MMK distribution (red bars) interacting with stator B-field (blue curve) at different electrical angles. Force = Σ(MMK × B) at each coil position. At ωt=0°, force peaks at +0.750 N; at ωt=180°, it reverses to -0.750 N. With FOC, the mover tracks the field to maintain continuous force.*

**Key insight:** In a linear motor, each coil produces force proportional to its MMK × local B-field. The sum of all 6 coil forces drives the mover. The floating neutral mechanism converts unipolar 0-4V PWM into bipolar ±0.5A currents, creating the traveling MMK wave that "locks" into the stator field.

- **Stator**: Permanent magnets create outward sine-wave B-field (static)
- **Mover**: 6 coils in AbCaBc pattern create traveling MMK wave
- **Force**: Sum of local MMK × B interactions at each coil position

## Documentation

| Document | Content |
|----------|---------|
| [docs/PRINCIPLE.md](docs/PRINCIPLE.md) | Physics explanation |
| [docs/WINDING_CONFIG.md](docs/WINDING_CONFIG.md) | 3-phase winding theory |
| [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) | **Parametric design & test setup specs** |
| [docs/BUILDING.md](docs/BUILDING.md) | Construction guide |

## Repository

```
├── docs/               # Documentation
├── cad/                # CAD files (.step, .f3z)
├── simulations/        # FEMM + Python simulations
├── data/               # Force profiles (Excel + CSV)
└── images/             # 3D renders & plots
```

## Verification Plan

| Step | Method | Status |
|------|--------|--------|
| 1. FEMM simulation | Static field + force | ✓ Complete |
| 2. Python dynamics | MMK traveling wave | ✓ Complete |
| 3. Static force test | Measure F vs I | Pending |
| 4. Dynamic test | FOC velocity control | Pending |
| 5. Performance | Efficiency, thermal | Pending |

## License

See [LICENSE](LICENSE).

---

*Parametric tubular linear motor. Pole pitch λ = 30mm, 24mm diameter, 3-phase FOC.*
