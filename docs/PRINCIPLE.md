# Principle of Operation

## The Magnetic Gear Concept

This tubular linear motor operates on a **magnetic gearing** principle — two magnetic fields interlock like gear teeth to produce linear motion, but without physical contact.

---

## How It Works

### The Core Idea

Imagine two sets of gear teeth that never touch:
- One set is fixed inside a tube (**stator**)
- One set surrounds it and can slide (**mover**)

Instead of physical teeth, we use **magnetic fields shaped like sine waves**:

```
Stator field (outward):  ~~~ ~~~ ~~~ ~~~
                              ↕ ↕ ↕ ↕
Mover field (inward):    ~~~ ~~~ ~~~ ~~~
                              ↑ ↑ ↑ ↑
                         Force direction
```

When the mover's field aligns with the stator's field, they "mesh" and create force. When the mover's field is shifted by the right amount, the force propels the mover forward.

---

## The Physics

### 1. Stator — Creating the Outward Sine Wave

The stator uses **permanent magnets** to create a static magnetic field:

**Structure inside the tube:**
```
[N Magnet] — [Steel Disk] — [Ferromagnetic Disc] — [S Magnet] — [Steel Disk] — ...
```

**Key insight**: The rounded ferromagnetic discs between opposing magnets shape the field from a square wave (raw magnets) into a **smooth sine wave**.

**Magnetic field shape:**
- Without shaping: Sharp peaks at magnet edges
- With shaping: Smooth sinusoidal variation
- Result: Clean sine wave radiating outward

### 2. Mover — Creating the Inward Traveling Wave

The mover is a **3-phase electromagnet** surrounding the stator:

**Structure:**
- Three coil groups (phases A, B, C)
- Ferromagnetic slots between phases
- Star-connected windings

**How the traveling wave is created:**

With 3-phase currents (120° apart):
```
Phase A: I · sin(θ)
Phase B: I · sin(θ - 120°)
Phase C: I · sin(θ - 240°)
```

Each phase creates a magnetic field proportional to its current. The sum of three shifted sine waves creates a **traveling wave** that moves along the stator.

**Critical geometry:**
```
Coil Width = Stator Pole Pitch / 6
```

This 1/6th relationship ensures the mover's field "teeth" align perfectly with the stator's field "teeth."

### 3. Force Production

**Force arises from field interaction:**

The force between two magnetic fields follows:
```
F ∝ ∫(B₁ · B₂) dV
```

Where:
- B₁ = Stator field (static, outward sine wave)
- B₂ = Mover field (traveling, inward sine wave)

**When fields align:** Maximum force
**When fields are 90° apart:** Zero force  
**When fields oppose:** Negative (braking) force

**The "gear ratio":**
- Electrical angle: 360° = 1 pole pitch (N-to-N)
- Mechanical distance: 1 pole pitch = 30 mm (in this design)
- Force peaks every 90° electrical = 3.75 mm

### 4. Synchronous Operation

The motor is **synchronous**:
- The mover's field must travel at the same speed as the mechanical motion
- If the mover moves too fast, the fields slip and force drops
- FOC (Field-Oriented Control) ensures the fields stay optimally aligned

**Speed relationship:**
```
Velocity = (Pole Pitch × Electrical Frequency) / 2
```

For 50 Hz electrical frequency and 30 mm pole pitch:
```
Velocity = (0.030 m × 50 Hz) / 2 = 0.75 m/s
```

---

## Why This Works

### Advantages of Magnetic Gearing

1. **No Contact** — No friction, no wear, no lubrication
2. **High Precision** — Position determined by field alignment, not mechanical tolerances
3. **Smooth Motion** — Sine waves produce continuous force, no cogging (with proper design)
4. **Bidirectional** — Force direction reverses by reversing phase sequence
5. **Scalable** — Force scales with magnet area and current

### Key Physical Constraints

**Force limit:**
- Limited by saturation of steel (typically 1.5-2 T)
- Limited by demagnetization of permanent magnets
- Limited by heating in coils

**Speed limit:**
- Back-EMF reduces effective voltage at high speed
- Inductive reactance: XL = 2πfL increases with frequency
- Eddy currents in conducting materials

**Efficiency:**
- Iron losses (hysteresis + eddy currents)
- Copper losses (I²R in windings)
- No friction losses (unlike mechanical gears)

---

## Field Visualization

### FEMM Simulation Results

The magnetic field lines show the sine-wave pattern:

![Field Lines](../simulations/images/femm_field_lines.png)

**What you see:**
- Blue region: Stator (magnets + steel)
- Green region: Mover (coils)
- Lines: Magnetic flux paths
- Bulging: Characteristic sine-wave field shape

### Tangential Field Profile

The tangential B-field along the mover surface:

![Field Profile](../simulations/images/femm_field_lines_mover.png)

**What you see:**
- Clean sine wave
- Peak: ~0.02 Tesla
- Period: 30 mm (pole pitch, N-to-N distance)
- This is the "magnetic gear tooth" profile

---

## Summary

1. **Stator** creates a static outward sine-wave field using shaped permanent magnets
2. **Mover** creates a traveling inward sine-wave field using 3-phase currents
3. **Fields interlock** like gear teeth, producing force
4. **FOC control** keeps fields optimally aligned for smooth motion
5. **Result**: Linear motion without contact, with precise position control

The magnetic gearing principle enables high force density and smooth operation that would be difficult to achieve with conventional mechanical gears.

---

## Further Reading

- [Design Principles](DESIGN_PRINCIPLES.md) — How the geometry is calculated
- [Building Instructions](BUILDING.md) — How to construct the motor
- [FEMM Simulations](../simulations/) — Detailed electromagnetic analysis
