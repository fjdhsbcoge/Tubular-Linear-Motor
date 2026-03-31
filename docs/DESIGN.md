# Tubular Linear Motor - Design Documentation

## Overview

This is a **fully open-source tubular linear motor** designed for high force, low power consumption, and precise control. The design uses a unique magnetic gearing approach where the stator and mover fields interlock like gear teeth.

**Key Features:**
- FOC (Field-Oriented Control) actuated
- 3-phase star-connected mover
- Sine-wave magnetic field topology
- High force-to-power ratio

---

## Working Principle

### The Magnetic Gear Concept

The motor operates on a magnetic gearing principle where:
- The **stator** creates a sine-wave magnetic field pointing **outward**
- The **mover** creates a sine-wave magnetic field pointing **inward**
- These fields interlock like gear teeth, producing linear force

### Stator Configuration

The stator consists of:
1. **Alternating disk magnets** arranged inside a tube
2. **Steel disks** between the magnets
3. **Ferromagnetic discs** with rounded outer diameter placed between opposing magnets

This configuration generates a **sinusoidal magnetic field** that radiates outward from the tube.

![Stator Field Lines](../simulations/images/femm_field_lines.png)
*FEMM simulation showing magnetic field lines from stator (blue) to mover (green). The rounded ferromagnetic discs create the characteristic field bulging.*

### Magnetic Field Profile

The tangential magnetic flux density (B-field) along the stator surface shows a clean sine wave:

![Field Profile](../simulations/images/femm_field_lines_mover.png)
*Tangential B-field (B.t) vs. position. Peak field ~0.02 T, showing ideal sinusoidal distribution.*

This sine-wave field is the key to the "magnetic gear teeth" — smooth, continuous variations that mesh with the mover's field.

### Mover Configuration

The mover surrounds the stator and consists of:
1. **3-phase winding** (A, B, C phases)
2. **Ferromagnetic slots** between each phase
3. **Star connection** on one side

The phases are driven with FOC (Field-Oriented Control) to create a rotating magnetic field that appears as a traveling sine wave along the tube.

### Coil Geometry

**Critical dimension:**
```
Coil width = Stator pole pitch / 6
```

This means the coil and slot width equals one-sixth of the stator's magnetic pole pitch, ensuring proper field alignment.

---

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| Circumference | 87.976 mm |
| Phases | 3 (Star-connected) |
| Control | FOC (Field-Oriented Control) |
| Stator Field | Outward sine-wave |
| Mover Field | Inward sine-wave |

---

## Force Characteristics

The motor produces force through the interaction of the stator's permanent magnet field and the mover's electromagnetic field.

### Force Components

From the simulation data:
- **Fx** - Force in the primary direction of motion (N)
- **Fy** - Force perpendicular to motion (N)
- Total force varies with position, showing the periodic nature of the magnetic gearing

### Simulation

Force profiles were calculated using **FEMM (Finite Element Method Magnetics)**.

**Simulation Methodology:**
To speed up computation, a **2D axisymmetric slice** approach was used:
1. Model a 1mm axial slice of the motor
2. Simulate 2D field distribution
3. Multiply force results by circumference (87.976 mm) for total force

This approach is valid for cylindrical motors with uniform cross-section and negligible end effects.

**Simulation Results:**
- Peak tangential B-field: ~0.02 Tesla
- Clean sine-wave field distribution confirms design
- See `/simulations/` for field visualizations
- See `/data/` for force profile CSV data

See `/data/` for detailed force profile data for different configurations.

---

## Bill of Materials (BOM)

### Stator Components
- [ ] Steel tube (housing)
- [ ] Disk magnets (alternating polarity)
- [ ] Steel disks (flux paths)
- [ ] Ferromagnetic discs (rounded profile)

### Mover Components
- [ ] 3-phase winding wire
- [ ] Ferromagnetic core material
- [ ] Mounting structure
- [ ] Position sensor (for FOC)

### Electronics
- [ ] 3-phase inverter
- [ ] FOC controller
- [ ] Position encoder

---

## Assembly Notes

1. **Stator Assembly**: Stack magnets and steel disks alternately inside the tube
2. **Mover Winding**: Wind 3-phase coils with proper spacing (pole pitch / 6)
3. **Alignment**: Ensure mover can slide freely around stator
4. **Sensors**: Install position feedback for FOC operation

---

## Control Strategy

The motor requires **Field-Oriented Control (FOC)**:

1. **Park/Clarke transforms** convert 3-phase currents to rotor reference frame
2. **Current control** maintains Iq (torque-producing) and Id (flux-producing) components
3. **Commutation** tracks mover position to maintain optimal force angle

Without FOC, the motor cannot achieve smooth motion or optimal efficiency.

---

## Simulation Files

FEMM simulation files will be added to document the electromagnetic analysis.

**Force Profile Data**: See `/data/force_profiles.csv`

---

## License

See [LICENSE](../LICENSE) for usage terms.

This design is open-source — build it, improve it, share it.
