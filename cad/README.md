# CAD Files

This directory contains CAD models for manufacturing the tubular linear motor.

## Files

| File | Format | Description |
|------|--------|-------------|
| `24mm eine Achse SIM.step` | STEP | Universal CAD format, importable in most CAD software |
| `24mm eine Achse SIM.f3z` | Fusion 360 | Native Fusion 360 archive with full history |

## Contents

The CAD model includes:

### Stator Components
- Steel tube (housing)
- Magnet disks
- Steel flux return disks
- Ferromagnetic field shapers
- Complete stack assembly

### Mover Components
- Laminated core with slots
- Coil winding regions
- Housing/mounting structure
- End caps

### Assembly
- Mover positioned over stator
- Air gap clearance visible
- Overall dimensions

## Dimensions

| Parameter | Value |
|-----------|-------|
| Tube outer diameter | 24 mm |
| Tube inner diameter | 20 mm |
| Pole pitch | 15 mm |
| Air gap | ~0.5-1 mm |
| Mover outer diameter | ~28 mm |

## Usage

### Viewing
- **Fusion 360**: Open `.f3z` file for full parametric model
- **Any CAD**: Import `.step` file
- **Free viewers**: Use eDrawings, FreeCAD, or similar

### Manufacturing
- Export individual parts from the assembly
- Generate 2D drawings with tolerances
- Create toolpaths for CNC/lathe

### Modification
- Change pole pitch, diameter, or length
- Adjust magnet/steel thickness
- Modify slot geometry

## Exporting Parts

From Fusion 360:
1. Open `.f3z` archive
2. Navigate to component in browser
3. Right-click → "Export as STL/STEP"
4. Use for 3D printing or machining

## Notes

- Model is parametric — change dimensions in Fusion 360
- STEP file is static geometry for reference
- Some features may be simplified for manufacturing
- Verify critical dimensions before production

---

*See [docs/BUILDING.md](../docs/BUILDING.md) for assembly instructions.*
