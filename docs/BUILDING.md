# Building Instructions

Step-by-step guide to constructing the tubular linear motor.

---

## Prerequisites

### Tools Required

| Tool | Purpose |
|------|---------|
| Lathe or CNC | Machining steel parts to precision |
| Winding jig | Consistent coil winding |
| Calipers | Dimensional verification |
| Multimeter | Electrical testing |
| Oscilloscope | Control debugging (optional) |
| FEMM (software) | Design validation |

### Skills Needed
- Basic machining (turning, facing)
- Motor winding
- Soldering
- Basic electronics
- Programming (for FOC controller)

---

## Part List (Bill of Materials)

### Stator Components

| Qty | Part | Material | Notes |
|-----|------|----------|-------|
| 1 | Steel tube | 1006 Steel | OD 24 mm, ID 20 mm, length as needed |
| 20 | Disk magnets | N40 NdFeB | Diameter 19 mm, thickness 3-4 mm |
| 20 | Steel disks | 1006 Steel | Diameter 19 mm, thickness 0.5-1 mm |
| 20 | Field shapers | 1006 Steel | Diameter 19 mm, rounded OD |

**Tube length formula:**
```
Length = (Pole Pitch × Number of Poles) + End Clearance
Example: (15 mm × 10 poles) + 20 mm = 170 mm
```

### Mover Components

| Qty | Part | Material | Notes |
|-----|------|----------|-------|
| 1 | Core laminations | 1006 Steel | Segmented for winding |
| 100g | Magnet wire | Copper Litz 0.4mm | Or solid 1mm for low frequency |
| 1 | Housing | Aluminum/Plastic | Mounting and protection |
| 2 | End caps | 3D printed/Aluminum | Wire termination |

**Wire length estimate:**
```
Turns per coil × Number of coils × Mean circumference
Example: 100 turns × 12 coils × 100 mm = 120 m
```

### Electronics

| Qty | Part | Specification |
|-----|------|---------------|
| 1 | 3-phase inverter | 48V, 10A minimum |
| 1 | FOC controller | SimpleFOC / ODrive / Custom |
| 1 | Position encoder | 1000+ CPR linear or rotary |
| 1 | Power supply | 24-48V DC |

---

## Step 1: Prepare Steel Components

### 1.1 Steel Tube (Stator Housing)

**Operations:**
1. Cut tube to length (+5 mm for facing)
2. Face both ends square
3. Deburr inner diameter
4. Clean with solvent

**Check:**
- ID 20 mm (±0.1 mm)
- Straightness < 0.1 mm over length
- Clean, rust-free interior

### 1.2 Steel Disks (Flux Returns)

**Operations:**
1. Cut stock to rough diameter
2. Turn to 19 mm OD (slip fit in tube)
3. Face to 0.5-1 mm thickness
4. Deburr edges

**Quantity:** 1 per magnet pair

**Check:**
- OD: 19.0 mm (-0.0/+0.1 mm)
- Parallel faces
- Clean, oil-free

### 1.3 Field Shapers (Critical)

**Operations:**
1. Turn to 19 mm OD base
2. Machine rounded profile on outer edge
3. Finish: Smooth surface (Ra < 3.2 μm)

**Profile geometry:**
- Arc radius: ~5-7 mm
- Arc extends: ~1/3 of pole pitch (5 mm)
- Centered between magnet faces

**Check:**
- Consistent profile (use template)
- Smooth transitions

---

## Step 2: Prepare Magnets

### 2.1 Magnet Preparation

**Safety:**
- Wear eye protection
- Keep magnets away from electronics
- Use non-magnetic tools

**Operations:**
1. Clean magnet surfaces
2. Mark polarity (N/S)
3. Apply thin adhesive film to sides

### 2.2 Magnetization Check

**Method:**
- Use magnetic field viewer film
- Verify alternating N-S-N-S pattern
- Check field strength with gaussmeter (>1 T surface)

---

## Step 3: Assemble Stator

### 3.1 Stacking Order

```
[End Cap] - [Magnet N] - [Steel Disk] - [Field Shaper] - [Magnet S] - [Steel Disk] - ...
```

**Procedure:**
1. Insert first end cap (temporary)
2. Place first magnet (N pole up)
3. Add steel disk
4. Add field shaper (rounded side toward tube wall)
5. Place next magnet (S pole up)
6. Repeat until desired length
7. Insert final end cap

### 3.2 Bonding

**Adhesive:**
- Option 1: Loctite 638 (retaining compound)
- Option 2: Epoxy (for permanent assembly)

**Procedure:**
1. Clean all surfaces with solvent
2. Apply thin adhesive layer
3. Assemble with proper spacing
4. Cure per adhesive specifications

### 3.3 Verification

**Checks:**
- All magnets alternate polarity (use compass)
- Field shapers centered between magnets
- No gaps in stack
- Assembly slides freely in tube (if removable)

**Field test:**
- Run gaussmeter along outside of tube
- Verify sine-wave pattern
- Peak field: ~0.02-0.03 T expected

---

## Step 4: Wind the Mover

### 4.1 Prepare Core

**Operations:**
1. Cut lamination segments
2. Stack to required length
3. Insulate slots (kapton tape or varnish)
4. Install winding mandrel

### 4.2 Calculate Turns

**Target:** Fill factor 40-50%

**Example calculation:**
```
Slot width: 2.5 mm
Slot depth: 5 mm
Slot area: 12.5 mm²

Wire diameter: 0.4 mm (with insulation)
Wire area: 0.126 mm²

Max turns: 12.5 / 0.126 × 0.5 = ~50 turns
```

### 4.3 Winding Pattern

**Phase A:** Slots 1, 4, 7, 10, ...
**Phase B:** Slots 2, 5, 8, 11, ...  
**Phase C:** Slots 3, 6, 9, 12, ...

**Each phase:**
- Wind all slots for that phase in same direction
- Maintain consistent tension
- Layer evenly

### 4.4 Termination

**Procedure:**
1. Leave 100 mm lead wires
2. Strip ends
3. Label phases (A, B, C)
4. Star connection: Connect one end of all phases together
5. Insulate with heat shrink

### 4.5 Post-Winding

**Operations:**
1. Apply coil varnish (impregnation)
2. Bake per varnish instructions
3. Test resistance (should match design: ~5.6 Ω)
4. Test for shorts (megger test)

---

## Step 5: Mechanical Assembly

### 5.1 Install Bearings

**Linear bearings:**
- Install in mover housing
- Ensure smooth sliding on tube
- Preload adjustment (if applicable)

### 5.2 Mount Mover

**Procedure:**
1. Slide mover over stator tube
2. Check clearance (0.5-1 mm air gap)
3. Verify no rubbing
4. Test full stroke range

### 5.3 Install Position Sensor

**Options:**

**A) Linear encoder:**
- Install scale along stator
- Mount read head on mover
- Calibrate zero position

**B) Rotary encoder + belt:**
- Pulley on mover
- Encoder on fixed mount
- Belt connects them

**C) Hall sensors:**
- Mount 3 sensors spaced 120° electrical
- Detect stator magnet fields
- Simple but lower resolution

---

## Step 6: Electronics

### 6.1 Inverter Wiring

**Connections:**
```
Inverter A → Mover Phase A
Inverter B → Mover Phase B
Inverter C → Mover Phase C
Inverter GND → Power supply GND
```

**Check:**
- Wire gauge adequate for current (2A → 0.5 mm² minimum)
- Proper insulation
- Strain relief

### 6.2 Encoder Wiring

**Connections:**
- Power (5V or 3.3V)
- GND
- A, B, (Z) channels to controller

### 6.3 Power-Up Test

**Before connecting motor:**
1. Power controller
2. Verify logic voltages
3. Test encoder counts
4. Verify gate drive outputs (no motor connected)

---

## Step 7: Commissioning

### 7.1 Initial Motor Test (Open Loop)

**DC test:**
1. Apply 12V to Phase A only
2. Mover should lock to position
3. Apply 12V to Phase B only
4. Mover should shift by 1/3 pole pitch (5 mm)
5. Apply 12V to Phase C only
6. Mover should shift by 2/3 pole pitch (10 mm)

**Success criteria:**
- Motion in correct direction
- Consistent step size
- No excessive heating

### 7.2 Encoder Alignment

**Procedure:**
1. Command zero electrical angle (Iq = 0, Id = max)
2. Measure actual position
3. Adjust encoder offset in firmware
4. Verify at 90°, 180°, 270° positions

### 7.3 FOC Tuning

**Current loop:**
1. Set Kp small (0.1)
2. Increase until oscillation
3. Back off 50%
4. Add Ki for steady-state accuracy

**Velocity loop (if used):**
1. Start with low P gain
2. Increase for response
3. Add D gain for damping

**Position loop (if used):**
1. Similar to velocity
2. Lower bandwidth than velocity loop

### 7.4 Force Test

**Procedure:**
1. Apply increasing Iq reference
2. Measure force with scale
3. Verify linearity (F ∝ I)
4. Compare to FEMM prediction (~2.4 N/A)

---

## Step 8: Optimization

### 8.1 Force Ripple Reduction

**If ripple is excessive:**
- Check magnet spacing uniformity
- Verify field shaper alignment
- Tune FOC current controller
- Consider skewing (not in current design)

### 8.2 Thermal Management

**If overheating:**
- Reduce continuous current
- Add cooling (fan/liquid)
- Improve winding thermal path
- Use higher-temp magnet grade

### 8.3 Speed Optimization

**For higher speed:**
- Increase bus voltage
- Reduce winding turns (lower L)
- Implement field weakening

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No force | Wrong phasing | Check phase sequence |
| Weak force | Low current | Increase current limit |
| Cogging | Misaligned encoder | Recalibrate offset |
| Heating | Overcurrent | Reduce current, add cooling |
| Noise/vibration | PWM frequency | Increase to >20 kHz |
| Jerky motion | Current ripple | Tune FOC loop |

---

## Safety Notes

**Magnets:**
- Pinch hazard — handle carefully
- Can affect pacemakers — keep away
- Brittle — avoid impact

**Electrical:**
- High currents can cause burns
- Capacitors hold charge — discharge before work
- Ground all metal parts

**Mechanical:**
- Moving parts — keep clear during operation
- Pinch points between mover and mounts

---

## Files Reference

| File | Use |
|------|-----|
| `cad/24mm eine Achse SIM.step` | CAD geometry for manufacturing |
| `cad/24mm eine Achse SIM.f3z` | Fusion 360 source file |
| `simulations/config1_20mm.FEM` | Validate your build |

---

**Next:** See [PRINCIPLE.md](PRINCIPLE.md) for physics understanding and [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) for design details.
