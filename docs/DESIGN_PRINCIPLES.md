# Design Principles

This document covers the design decisions, calculations, and trade-offs in the tubular linear motor.

---

## System Specifications

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Outer Diameter** | 24 mm | Standard tube size, manageable force |
| **Pole Pitch** | 15 mm | Balance between force density and speed |
| **Phases** | 3 | Standard for FOC, good utilization |
| **Connection** | Star | Simpler wiring, no circulating currents |
| **Peak Force** | ~4.8 N @ 2A | Per phase, from FEMM simulation |
| **Circumference** | 87.976 mm | π × 28 mm (stator diameter) |

---

## Magnetic Design

### Pole Pitch Selection

**Pole pitch (τp) = 15 mm**

**Trade-offs:**
- **Smaller τp**: Higher force density, but more poles needed for same stroke
- **Larger τp**: Lower electrical frequency for given speed, but lower force density

**Speed consideration:**
At 50 Hz drive frequency:
- Mechanical speed = (15 mm × 50 Hz) / 2 = **0.375 m/s**

For most applications, 0.3-0.5 m/s is a practical speed range.

### Magnet Selection

**Material: N40 Neodymium**

| Property | Value | Significance |
|----------|-------|--------------|
| Hc (coercivity) | 969,969 A/m | High resistance to demagnetization |
| Br (remanence) | ~1.3 T | Strong magnetic field |
| μr | 1.05 | Behaves like air magnetically (after magnetization) |
| Operating temp | Up to 80°C | Standard grade |

**Why N40?**
- Cost-effective high-performance magnet
- Good availability
- Sufficient for ~0.02 T working field at mover

**Magnet dimensions:**
From FEMM and CAD, typical sizes:
- Thickness: 3-5 mm
- Diameter: ~20 mm (fits inside 24 mm tube)

### Steel Selection

**Material: 1006 Low-Carbon Steel**

| Property | Value | Significance |
|----------|-------|--------------|
| μr (initial) | 1,404 | High permeability for flux conduction |
| Saturation | ~2 T | Won't saturate at operating flux |
| Conductivity | 5.8 MS/m | Moderate (eddy current consideration) |

**Why 1006?**
- High permeability guides flux efficiently
- Low carbon = low coercivity = low hysteresis loss
- Common, inexpensive
- Easy to machine

**Nonlinear B-H curve:**
FEMM includes full B-H data, accounting for saturation at high flux.

### Field Shaping

**The Problem:**
Raw alternating magnets produce a square-wave field with sharp transitions.

**The Solution:**
Rounded ferromagnetic discs between magnets smooth the field.

**Optimal profile:**
- Partial circular arc on outer diameter
- Extends ~1/3 of pole pitch
- Material: Same as flux return (1006 steel)

**Result:**
- Harmonic content reduced
- Sine wave purity improved
- Smoother force production

---

## Electrical Design

### Coil Geometry

**Critical formula:**
```
Coil Width = Pole Pitch / 6 = 15 mm / 6 = 2.5 mm
```

**Why 1/6th?**
- 3 phases × 2 slots per phase = 6 slots per pole pair
- Each slot occupies 60 electrical degrees
- 360° / 6 = 60° = 1/6 of pole pitch

**Slot fill factor:**
- Target: 40-60%
- Higher fill = more copper = lower resistance, but harder to wind
- Litz wire helps with high-frequency losses

### Wire Selection

**Material: Copper Litz Wire (0.4 mm strands)**

| Property | Value | Significance |
|----------|-------|--------------|
| Strand diameter | 0.4 mm | Reduces skin effect at operating frequency |
| Bundle diameter | ~1.5-2 mm | Fits in slot |
| Conductivity | 58 MS/m | High efficiency |

**Why Litz?**
- Skin depth at 50 Hz: ~9 mm (copper)
- Skin depth at 500 Hz: ~3 mm
- 0.4 mm strands ensure uniform current distribution
- Critical for PWM switching frequencies (5-20 kHz)

**Alternative:** Solid wire for low-frequency operation (simpler, cheaper)

### Electrical Parameters

From FEMM simulations and measurements:

| Parameter | Value | Source |
|-----------|-------|--------|
| **R (phase resistance)** | 5.6 Ω | Measured |
| **L (self-inductance)** | 1.15 mH | FEMM simulation |
| **M (mutual inductance)** | -0.46 mH | FEMM simulation |

**Time constant:**
```
τ = L/R = 1.15 mH / 5.6 Ω = 0.205 ms
```

Fast response allows high-bandwidth current control.

**Back-EMF constant:**
From force constant (4.8 N @ 2A = 2.4 N/A) and velocity:
```
Ke = Force Constant / (Pole Pitch/2) = 2.4 / 0.0075 = 320 V/(m/s)
```

At 0.375 m/s: Back-EMF = 120 V (theoretical, per phase)

---

## Thermal Design

### Losses

**Copper losses:**
```
Pcu = I² × R = (2A)² × 5.6Ω = 22.4 W per phase (peak)
```

**Iron losses (estimated):**
- Hysteresis: ~5-10 W (depends on frequency)
- Eddy currents: ~2-5 W (reduced by Litz wire)

**Total losses:** ~30-40 W at 2A continuous

### Cooling

Options:
1. **Natural convection**: For intermittent duty
2. **Forced air**: Fan blowing over mover
3. **Liquid cooling**: Tube integrated in mover (high-performance)

**Temperature rise (natural convection):**
```
ΔT = Power × Rth
```
Typical thermal resistance: 2-5 K/W
ΔT ≈ 40W × 3 K/W = 120°C (too hot!)

**Recommendation:** Limit continuous current to ~1A without cooling.

---

## Mechanical Design

### Tube Dimensions

**Outer diameter: 24 mm**

**Wall thickness:** 1-2 mm
- Thicker = stiffer, but heavier
- Thinner = lighter, but may deflect

**Material options:**
- Steel: Magnetic shielding, strong
- Aluminum: Light, non-magnetic (external fields)
- Plastic: Lightest, no shielding

**Recommendation:** Steel for magnetic containment.

### Air Gap

**Typical air gap: 0.5-1 mm**

**Trade-offs:**
- Smaller gap: Higher force (field stronger), tighter tolerances
- Larger gap: Easier assembly, lower force

From FEMM: Gap is included in the 1 mm slice model.

### Bearing System

Not shown in current files, but critical:

Options:
1. **Linear bearings** (ball bushings): Low friction, standard
2. **Air bearings**: Zero friction, requires air supply
3. **Flexure bearings**: No friction, limited stroke
4. **Magnetic bearings**: No contact, complex control

**Recommendation:** Linear ball bearings for general use.

---

## Simulation-Driven Design

### FEMM Workflow

1. **Geometry**: Define stator and mover in 2D
2. **Materials**: Assign N40, 1006 Steel, Air, Copper
3. **Mesh**: Adaptive meshing for accuracy
4. **Solve**: Static magnetic field
5. **Analyze**: Block integrals for force
6. **Iterate**: Adjust geometry, repeat

### Force Ripple Analysis

**Script**: `Config1_forceripple.lua`

**Method:**
- Move mover in 1 mm steps
- Solve field at each position
- Calculate force via Maxwell stress tensor
- Record Fx, Fy vs. position

**Results:**
- Peak force: ~4.8 N at 2A
- Ripple period: 3.75 mm (90° electrical)
- Average force: ~3.5 N

### Modelica System Model

**Purpose:** Electrical circuit simulation

**Use cases:**
- Current controller design
- Thermal analysis (I²R losses)
- Voltage requirements
- Transient response

---

## Design Trade-offs Summary

| Decision | Option A | Option B | Choice | Reason |
|----------|----------|----------|--------|--------|
| Magnet grade | N40 | N52 | N40 | Cost, sufficient performance |
| Steel type | 1006 | 1010 | 1006 | Lower hysteresis |
| Wire type | Litz 0.4mm | Solid 1mm | Litz | High-frequency operation |
| Pole pitch | 15 mm | 10 mm | 15 mm | Speed/force balance |
| Phases | 3 | 2 | 3 | Standard FOC |
| Connection | Star | Delta | Star | No circulating currents |

---

## Scaling the Design

### More Force

Options:
1. **Larger diameter**: Force ∝ diameter²
2. **More pole pairs**: More force peaks per revolution
3. **Higher current**: Up to thermal limit
4. **Better magnets**: N52 instead of N40 (+20% force)

### Longer Stroke

Simply extend the stator tube:
- Add more magnet/steel pairs
- Ensure mover covers full stroke
- Consider sag for long tubes

### Higher Speed

Options:
1. **Higher voltage**: Faster current rise
2. **Lower inductance**: Fewer turns, larger wire
3. **Field weakening**: Negative Id at high speed

---

## Files Reference

| File | Purpose |
|------|---------|
| `simulations/config1_20mm.FEM` | FEMM geometry |
| `simulations/linearMotorThreephase.mo` | Circuit model |
| `cad/24mm eine Achse SIM.step` | CAD geometry |
| `cad/24mm eine Achse SIM.f3z` | Fusion 360 source |

---

## Next Steps

See [BUILDING.md](BUILDING.md) for construction details.
