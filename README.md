# Tubular Linear Motor

**Fully Open Source** tubular linear motor design with FOC control. Optimized for high force, low power consumption, and smooth motion.

![Design View 1](images/design_view_1.png)
*3D model showing the tubular linear motor assembly*

![Design View 2](images/design_view_2.png)
*Cross-section view showing internal structure*

---

## How It Works

This motor uses a **magnetic gearing** principle where two sine-wave magnetic fields interlock to produce linear force.

### The Concept

Imagine two sets of gear teeth that don't touch — one set inside a tube (stator), one set surrounding it (mover). Instead of physical teeth, we use magnetic fields shaped like sine waves:

- **Stator field**: Points outward from the tube
- **Mover field**: Points inward toward the tube
- **Result**: The fields "mesh" like gears, creating force

### Stator Configuration

Inside the steel tube:
1. **Alternating disk magnets** (N-S-N-S...)
2. **Steel disks** (flux paths between magnets)
3. **Ferromagnetic discs** with rounded outer diameter

The rounded ferromagnetic discs between opposing magnets shape the magnetic field into a smooth **sine wave** radiating outward.

### Mover Configuration

Surrounding the stator:
1. **3-phase winding** (A, B, C)
2. **Ferromagnetic slots** between phases
3. **Star-connected** on one end

The phases are driven with **FOC (Field-Oriented Control)** to create a traveling magnetic field that matches the stator's field pattern.

### Critical Geometry

```
Coil Width = Stator Pole Pitch ÷ 6
```

This 1/6th relationship ensures the mover's field aligns perfectly with the stator's magnetic "gear teeth."

---

## Specifications

| Parameter | Value |
|-----------|-------|
| Control | FOC (Field-Oriented Control) |
| Phases | 3 (Star-connected) |
| Stator Field | Sine-wave, outward |
| Mover Field | Sine-wave, inward |
| Circumference | 87.976 mm |

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/DESIGN.md](docs/DESIGN.md) | Complete technical documentation |
| [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md) | Step-by-step build instructions |
| [data/README.md](data/README.md) | Force profile data explanation |

---

## Key Features

✅ **High Force Density** — Magnetic gearing maximizes force per unit volume  
✅ **Low Power Consumption** — Efficient FOC control  
✅ **Smooth Motion** — Sine-wave fields eliminate cogging  
✅ **Scalable** — Design scales to different sizes and forces  
✅ **Open Source** — Full documentation for replication

---

## Repository Structure

```
Tubular-Linear-Motor/
├── images/              # 3D model images
├── docs/                # Documentation
│   ├── DESIGN.md        # Technical design details
│   └── BUILD_GUIDE.md   # How to build it
├── data/                # FEMM simulation data
│   ├── force_profile_1_layer.csv
│   ├── force_profile_4_layer.csv
│   └── force_profile_6_layer.csv
├── LICENSE
└── README.md            # This file
```

---

## Simulation Data

Force profiles were calculated using **FEMM (Finite Element Method Magnetics)**.

The data shows:
- Force vs. position for different coil layer configurations
- Fx (direction of motion) and Fy (transverse) force components
- Individual phase contributions

See `/data/` directory for CSV files.

---

## Building Your Own

1. **Read** [docs/DESIGN.md](docs/DESIGN.md) to understand the principles
2. **Follow** [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md) for construction
3. **Analyze** [data/](data/) for performance expectations
4. **Build** and share your results!

---

## Contributing

This is an open-source hardware project. Contributions welcome:
- Build reports
- Design improvements
- Simulation files
- Control firmware

---

## License

See [LICENSE](LICENSE) for details.

---

**Build it. Improve it. Share it.**
