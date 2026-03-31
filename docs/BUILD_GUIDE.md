# Build Guide - Tubular Linear Motor

This guide walks you through recreating the tubular linear motor.

---

## Prerequisites

### Tools Needed
- Lathe or CNC for machining steel parts
- Winding jig for coils
- Calipers for precise measurements
- FEMM (for custom simulations) - https://www.femm.info/

### Skills Required
- Basic machining
- Motor winding
- Electronics assembly
- FOC control implementation

---

## Step 1: Stator Construction

### 1.1 Prepare the Tube
- Machine steel tube to desired length
- Inner diameter must accommodate magnet stack
- Ensure straightness (critical for smooth motion)

### 1.2 Cut Magnet Disks
- Cut permanent magnets into disks
- Magnetize through thickness (axial magnetization)
- Alternate polarity: N-S-N-S-...

### 1.3 Cut Steel Disks
- Match outer diameter to tube inner diameter
- Thickness: typically 0.5-2mm (see simulation for optimal)

### 1.4 Ferromagnetic Discs
- These go between opposing magnets
- Rounded outer diameter profile (critical for field shaping)
- Material: soft iron or similar high-permeability material

### 1.5 Assembly
```
Stack order inside tube:
[Magnet N] - [Steel Disk] - [Ferromagnetic Disc] - [Magnet S] - [Steel Disk] - ...
```

**Note:** The ferromagnetic discs with rounded profiles create the sinusoidal field distribution.

---

## Step 2: Mover Construction

### 2.1 Calculate Dimensions

**Measure your stator:**
- Measure the distance between equivalent magnet positions = **Pole Pitch (τp)**

**Calculate coil width:**
```
Coil Width = τp / 6
Slot Width = τp / 6
```

### 2.2 Core Material
- Cut ferromagnetic core laminations
- Shape to fit around stator tube (cylindrical or split design)
- Slots for windings at calculated pitch

### 2.3 Winding the Coils

**Configuration:** 3-phase, star-connected

**Steps:**
1. Wind Phase A coils in slots 1, 4, 7, 10...
2. Wind Phase B coils in slots 2, 5, 8, 11...
3. Wind Phase C coils in slots 3, 6, 9, 12...

**Slot spacing** = τp / 3 (120 electrical degrees)

**Wire selection:**
- Current rating based on force requirements
- Fill factor typically 40-60%

### 2.4 Star Connection
- Connect one end of all three phases together
- The other ends go to the 3-phase inverter (A, B, C)

---

## Step 3: Electronics

### 3.1 Position Sensing
Options:
- **Incremental encoder** on mover
- **Hall sensors** detecting stator magnets
- **Linear encoder** along stroke length

### 3.2 3-Phase Inverter
Requirements:
- Voltage: sufficient for your coil design (typically 12-48V)
- Current: 2-3x rated current for peak force
- PWM frequency: 20kHz+ for quiet operation

### 3.3 FOC Controller
Implement or use existing FOC firmware:
- **SimpleFOC** (Arduino-based)
- **ODrive**
- **Custom implementation**

**Key parameters:**
- Pole pairs = number of magnet pole pairs in stator
- Encoder resolution (counts per electrical cycle)
- Current limits

---

## Step 4: Commissioning

### 4.1 Initial Testing (Open Loop)
1. Apply DC to phase A only → mover should lock to position
2. Apply DC to phase B only → mover should shift by 1/3 pole pitch
3. Apply DC to phase C only → mover should shift by 2/3 pole pitch

### 4.2 Encoder Alignment
1. Command zero electrical angle
2. Measure actual position
3. Set encoder offset in firmware

### 4.3 FOC Tuning
1. Start with conservative current limits
2. Tune current PI controllers
3. Tune velocity loop (if applicable)
4. Tune position loop (if applicable)

---

## Step 5: Optimization

### Force Optimization
- Adjust coil current (Iq reference)
- Optimize advance angle (if needed)
- Minimize Id (flux-weakening if operating above base speed)

### Efficiency
- Reduce switching losses (lower PWM freq if acceptable)
- Optimize coil resistance (wire gauge)
- Consider litz wire for high-frequency operation

---

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No force | Wrong phasing | Check phase sequence (A-B-C) |
| Cogging | FOC not aligned | Check encoder offset |
| Low force | Insufficient current | Increase current limit |
| Heating | High resistance | Use thicker wire, reduce load |
| Vibration | PWM too low | Increase PWM frequency |

---

## Design Variations

### More Force
- Increase stator diameter (more magnet area)
- More pole pairs (more magnetic gearing points)
- Higher current (with cooling)

### Longer Stroke
- Extend stator tube length
- Add more magnet/steel pairs
- Ensure mover can accommodate full stroke

### Higher Speed
- Reduce mover mass
- Higher voltage (for faster current rise)
- Field weakening (negative Id)

---

## Next Steps

1. Review simulation data in `/data/`
2. Customize dimensions for your application
3. Run FEMM simulations for your specific geometry
4. Share your build!

---

## Resources

- **FEMM**: https://www.femm.info/
- **SimpleFOC**: https://simplefoc.com/
- **ODrive**: https://odriverobotics.com/

---

*Good luck with your build!*
