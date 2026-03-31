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
