# FEMM Simulation Files

This directory contains complete FEMM simulation files for the tubular linear motor.

## File Overview

| File | Description |
|------|-------------|
| `config1_20mm.FEM` | Main FEMM project - Phase A excited |
| `config1_20mm.ans` | Solution file - Phase A (binary) |
| `config1_20mm_phaseB.FEM` | FEMM project - Phase B excited |
| `config1_20mm_phaseB.ans` | Solution file - Phase B (binary) |
| `config1_20mm_phaseC.FEM` | FEMM project - Phase C excited |
| `config1_20mm_phaseC.ans` | Solution file - Phase C (binary) |
| `Config1_20mm.dxf` | CAD export of geometry |
| `Config1_force_ripple_2A.txt` | Force vs. position (Phase A, 2A) |
| `Config1_force_ripple_PhaseB_2A.txt` | Force vs. position (Phase B, 2A) |
| `Config1_force_ripple_PhaseC_2A.txt` | Force vs. position (Phase C, 2A) |

## Simulation Methodology

### Model Dimensions
- **Slice thickness**: 1 mm (2D planar simulation)
- **Model length**: 20 mm (partial stator representation)
- **Scaling**: Force results multiplied by circumference (87.976 mm)

### Materials Used

| Material | Type | Properties |
|----------|------|------------|
| **N40** | Permanent Magnet | Hc = 969,969 A/m, μr = 1.05, σ = 0.667 MS/m |
| **1006 Steel** | Ferromagnetic | μr = 1,404 (nonlinear), B-H curve included |
| **Air** | Non-magnetic | μr = 1 |
| **0.4mm** | Coil (Litz) | 0.4mm wire, σ = 58 MS/m, LamType = 3 (Litz wire) |
| **u1-u6** | Various | Permeability values for specific regions |

### Geometry Details

**Stator (inside tube):**
- Alternating N40 magnet disks
- 1006 Steel flux return disks
- Rounded ferromagnetic discs between magnets

**Mover (outside, green in images):**
- 3-phase winding slots
- Litz wire (0.4mm) for reduced eddy losses
- Air gap between stator and mover

**Boundary Conditions:**
- A = 0 (magnetic potential) at model edges
- Planar problem type
- Cartesian coordinates

## Force Results

### Phase A (2A current)
Peak force: **~4.8 N** (see `Config1_force_ripple_2A.txt`)

Force varies sinusoidally with position:
- Position 0 mm: Fx ≈ 0 N, Fy ≈ -3.2 N
- Position 10 mm: Fx ≈ 0.5 N, Fy ≈ -3.3 N  
- Position 20 mm: Fx ≈ 0.1 N, Fy ≈ -4.8 N
- Position 40 mm: Fx ≈ 0.4 N, Fy ≈ -3.3 N

The force ripple shows the periodic nature of the magnetic gearing.

### Phases B and C
Similar force profiles shifted by 120° and 240° electrical degrees.

**Note:** Fx is the useful force in the direction of motion. Fy is the normal force (attractive/repulsive).

## How to Use These Files

### Opening in FEMM
1. Download FEMM from https://www.femm.info/
2. Open `.FEM` file: File → Open
3. View geometry and materials
4. To see results: File → Open → select corresponding `.ans` file

### Viewing Force Data
The `.txt` files contain tab-separated data:
```
Position_mm    Fx_N        Fy_N
0              0           -3.22486...
1              -0.3588...  -3.21832...
...
```

Import into Excel, Python, MATLAB for plotting.

### Running New Simulations
1. Modify geometry in `.FEM` file (if desired)
2. Mesh: Operations → Mesh
3. Solve: Operations → Solve
4. Post-process: View → Field or use Lua scripts

## Simulation Parameters

From `config1_20mm.FEM`:
```
[Format]      = 4.0
[Frequency]   = 0 (DC/static)
[Precision]   = 1e-8
[MinAngle]    = 30°
[DoSmartMesh] = 1 (adaptive meshing)
[Depth]       = 1 mm
[LengthUnits] = millimeters
[ProblemType] = planar
```

## Key Insights

1. **N40 Magnets**: High-grade neodymium (Hc ≈ 970 kA/m)
2. **1006 Steel**: Low-carbon steel for flux paths (nonlinear B-H)
3. **Litz Wire**: 0.4mm strands reduce AC losses
4. **Force Ripple**: ~4.8N peak with sinusoidal variation
5. **Scaling**: 1mm slice × 87.976mm circumference = full 3D force

## Visualization

See `images/` folder for:
- Field line plots showing flux distribution
- B-field profiles confirming sine-wave shape

## DXF Export

`Config1_20mm.dxf` contains the 2D geometry suitable for:
- CAD import (AutoCAD, SolidWorks, etc.)
- Laser cutting patterns
- Manufacturing drawings

## Notes

- `.ans` files are binary and large (~170 MB each)
- They contain the mesh and field solution
- Open with corresponding `.FEM` file to view results
- FEMM is Windows-only but runs via Wine on Linux/Mac
