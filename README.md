# Tubular Linear Motor

**Fully Open Source** tubular linear motor with FOC control. High force density, smooth motion, magnetic gearing principle.

![Design View 1](images/design_view_1.png)
*3D model showing the complete assembly*

![Design View 2](images/design_view_2.png)
*Cross-section view showing internal structure*

---

## How It Works

This motor uses **magnetic gearing** — two sine-wave magnetic fields interlock like gear teeth to produce force without contact.

**The Stator (inside the tube):**
- Alternating permanent magnets
- Steel flux return paths
- Rounded ferromagnetic discs shape the field into a sine wave
- Creates an **outward** sine-wave magnetic field

**The Mover (surrounds the stator):**
- 3-phase electromagnetic coils
- Ferromagnetic slots
- Creates a **traveling** sine-wave field pointing inward

**The Result:**
The two fields "mesh" like gear teeth. As the mover's field travels (driven by 3-phase currents), it pulls the mover along the stator.

```
Stator field:  ~~~ ~~~ ~~~ ~~~  (static, outward)
                    ↕ ↕ ↕ ↕
Mover field:   ~~~ ~~~ ~~~ ~~~  (traveling, inward)
                    ↑ ↑ ↑ ↑
                  Force direction
```

**Key insight:** Coil width = Pole pitch / 6. This ensures the magnetic "teeth" align perfectly.

---

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Diameter | 24 mm |
| Pole Pitch (N-to-N) | 30 mm |
| Peak Force | ~4.8 N @ 2A (per phase) |
| Phases | 3 (Star-connected) |
| Control | FOC (Field-Oriented Control) |

---

## Documentation Structure

This repository is organized into **three main documents** plus **technical references**:

### 1. [Principle of Operation](docs/PRINCIPLE.md)
**The physics behind the motor.**
- Magnetic gearing concept
- How sine-wave fields interlock
- Force production mechanism
- Synchronous operation
- Field visualizations from FEMM

**Read this if:** You want to understand *why* it works.

---

### 2. [Design Principles](docs/DESIGN_PRINCIPLES.md)
**The engineering decisions.**
- Pole pitch selection rationale
- Material choices (N40 magnets, 1006 steel, Litz wire)
- Coil geometry calculations
- Electrical parameters (R, L, M)
- Thermal design considerations
- Scaling guidelines

**Read this if:** You want to *modify* or *optimize* the design.

---

### 3. [Building Instructions](docs/BUILDING.md)
**Step-by-step construction.**
- Complete BOM
- Machining procedures
- Magnet handling and assembly
- Coil winding guide
- Electronics setup
- FOC commissioning
- Troubleshooting

**Read this if:** You want to *build* the motor.

---

### Technical Reference: [Winding Configuration](docs/WINDING_CONFIG.md)
**Deep dive into the 3-phase winding.**
- 18-coil distributed winding pattern
- Phase shifts (150°, 90°) explained
- Kirchhoff's law application
- Magnetic field synthesis
- How currents create traveling waves
- Excel sheet walkthrough

**Read this if:** You want to understand *how the phases work together* or *implement custom FOC*.

---

## Repository Structure

```
Tubular-Linear-Motor/
├── docs/
│   ├── PRINCIPLE.md          ← Physics and theory
│   ├── DESIGN_PRINCIPLES.md  ← Engineering decisions
│   ├── BUILDING.md           ← Construction guide
│   └── WINDING_CONFIG.md     ← 3-phase winding deep dive
├── images/                   # 3D model renders
├── cad/                      # CAD files for manufacturing
│   ├── 24mm eine Achse SIM.step
│   ├── 24mm eine Achse SIM.f3z
│   └── README.md
├── simulations/              # FEMM electromagnetic analysis
│   ├── config1_20mm.FEM/.ans     # Phase A simulation
│   ├── config1_20mm_phaseB.FEM   # Phase B simulation
│   ├── config1_20mm_phaseC.FEM   # Phase C simulation
│   ├── linearMotorThreephase.mo  # Modelica circuit model
│   ├── Config1_forceripple.lua   # Force analysis scripts
│   ├── images/                   # Field visualizations
│   └── FILE_GUIDE.md             # File descriptions
├── data/                     # Force profile CSV data
│   └── 260331 Coil Config and Force Profile.xlsx  # Source Excel
├── LICENSE
└── README.md                 # This file
```

---

## Simulation Results

### FEMM Electromagnetic Analysis

**Field Line Distribution:**
![Field Lines](simulations/images/femm_field_lines.png)
*Magnetic flux from stator (blue) to mover (green). The rounded ferromagnetic discs create the sine-wave field shape.*

**Tangential Field Profile:**
![Field Profile](simulations/images/femm_field_lines_mover.png)
*Clean sine wave (~0.02 T peak) — the "magnetic gear teeth" pattern that enables smooth force.*

### Force Characteristics

From FEMM simulations at 2A:
- **Peak force:** ~4.8 N per phase
- **Force ripple:** Sinusoidal variation with position
- **Period:** 3.75 mm (90° electrical)

See `/data/` for detailed force vs. position curves.

### Electrical Model

Modelica circuit simulation includes:
- R = 5.6 Ω (phase resistance)
- L = 1.15 mH (self-inductance)
- M = -0.46 mH (mutual inductance)
- 3-phase star-connected

See `simulations/linearMotorThreephase.mo`

---

## Key Features

✅ **No Contact** — Magnetic gearing eliminates friction and wear
✅ **High Precision** — Position determined by field alignment
✅ **Smooth Motion** — Sine-wave fields produce continuous force
✅ **FOC Control** — Field-oriented control for optimal performance
✅ **Open Source** — Full documentation and simulation files
✅ **Scalable** — Design scales to different sizes and forces

---

## Getting Started

### I want to understand the concept
→ Read [docs/PRINCIPLE.md](docs/PRINCIPLE.md)

### I want to understand the winding/phase theory
→ Read [docs/WINDING_CONFIG.md](docs/WINDING_CONFIG.md)

### I want to modify the design
→ Read [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md)

### I want to build one
→ Read [docs/BUILDING.md](docs/BUILDING.md)

### I want to run simulations
→ See [simulations/FILE_GUIDE.md](simulations/FILE_GUIDE.md)

---

## Software Used

| Software | Purpose | Link |
|----------|---------|------|
| **FEMM** | Electromagnetic simulation | https://www.femm.info/ |
| **OpenModelica** | Circuit/system simulation | https://openmodelica.org/ |
| **Fusion 360** | CAD design | https://www.autodesk.com/ |
| **SimpleFOC** | Motor control (optional) | https://simplefoc.com/ |

---

## Contributing

This is open-source hardware. Contributions welcome:
- Build reports and photos
- Design improvements
- Additional simulations
- Control firmware
- Documentation improvements

---

## License

See [LICENSE](LICENSE) for details.

**Build it. Improve it. Share it.**

---

*This design uses the magnetic gearing principle with sine-wave fields. Peak force ~4.8N at 2A per phase, 24mm diameter, 30mm pole pitch (N-to-N).*

