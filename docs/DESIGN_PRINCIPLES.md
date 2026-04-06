# Tubular Linear Motor - Design Principles

This document describes the **general parametric design** that can be scaled, and the **specific test setup** used for initial verification.

---

## General Design (Parametric)

The motor design is parametric — dimensions can be changed while maintaining proportional relationships that ensure proper operation.

### Stator Design

**Magnets and Spacers (tightly stacked inside a thin tube):**

| Parameter | Guideline | Rationale |
|-----------|-----------|-----------|
| Magnet Pattern | NS=SN=NS=SN... | Alternating poles for sinusoidal field |
| Spacer Material | C15 or similar low-carbon steel | High permeability, easy to machine |
| Spacer Edge Rounding | ~5 × disk diameter | Shapes field into clean sine wave |
| Spacer Width | 90-120% of magnet width | Optimizes flux shaping |
| **Pole Pitch (λ)** | **NS=SN=** (one full period) | Fundamental design unit |

**Pole Pitch Definition:**
The pole pitch λ is the distance from one N pole to the next N pole (N→S→N). One pole pitch = two magnets + two spacers.

### Mover Design

**Winding Pattern:**
```
AbCaBc AbCaBc AbCaBc ... (repeated X times)
```

| Parameter | Guideline | Rationale |
|-----------|-----------|-----------|
| Pattern | AbCaBc | 3-phase, 6 coils per pole pitch |
| Coil Width | λ/6 (pole pitch ÷ 6) | 60° electrical spacing |
| Total Mover Length | X × λ | X = number of AbCaBc repeats |
| Phases | 3, star-connected | Standard BLDC configuration |

**Coil Layout per Pole Pitch:**
```
Position:  0      λ/6    2λ/6   3λ/6   4λ/6   5λ/6    λ
           [A]    [b]    [C]    [a]    [B]    [c]
           │      │      │      │      │      │
Phase:     U      V      W      U      V      W
Direction: +      -      +      -      +      -
```

### Electrical Parameters

Choose based on **driver capability** and **force requirements**:

| Driver Spec | Influences | Typical Range |
|-------------|-----------|---------------|
| Max Voltage | Max speed, back-EMF handling | 12-48V |
| Max Current | Peak force, thermal limits | 2-10A |
| PWM Resolution | Current control precision | 8-12 bit |

**Design Equations:**
```
V_back_EMF = N × B × v × l  (speed voltage)
R_phase    = V_driver / I_max (for thermal limit)
L_phase    = τ_electrical × R (for current bandwidth)
```

Where:
- N = turns per coil
- B = peak air-gap flux density
- v = max velocity
- l = active conductor length
- τ_electrical = electrical time constant (typically 1-5 ms)

---

## Test Setup (Specific Implementation)

This is the specific configuration being built and simulated for initial verification.

### Physical Dimensions

| Parameter | Value | Notes |
|-----------|-------|-------|
| Outer Diameter | 24 mm | Tube OD |
| Pole Pitch (λ) | 30 mm | N-to-N distance |
| Magnet Diameter | 18 mm | Stator magnets |
| Coil Inner Diameter | 25 mm | Mover bore |
| Coil Outer Diameter | 35 mm | Mover OD |
| Coil Width | 5 mm | λ/6 = 30/6 |
| Mover Length | 90 mm | 3 × λ (three AbCaBc repeats) |

### Materials

| Component | Material | Specification |
|-----------|----------|---------------|
| Magnets | N40 | Br = 1.3 T, Hc = 970 kA/m |
| Spacers | Steel 1006 | μr = 1404, rounded edges |
| Wire | 0.4 mm Litz | σ = 58 MS/m, 18 coils total |
| Tube | Thin-wall stainless | Contains magnet stack |

### Electrical (Measured/Simulated)

| Parameter | Value | Source |
|-----------|-------|--------|
| Phase Resistance | 4.0 Ω | Design target |
| Phase Inductance | ~1.15 mH | FEMM simulation |
| Mutual Inductance | ~-0.46 mH | FEMM simulation |
| Nominal Current | 2 A | Thermal limited |
| **Simulated Force** | **60 N at 2 A** | FEMM + Excel |

### Coil Configuration Detail

**18 coils total: A-b-C-a-B-c repeated 3 times**

```
Position (mm):  0   5   10  15  20  25  30  35  40  45  50  55  60  65  70  75  80  85
Coil:           A   b   C   a   B   c   A   b   C   a   B   c   A   b   C   a   B   c
Phase:          U   V   W   U   V   W   U   V   W   U   V   W   U   V   W   U   V   W
Block:          └──────── Block 1 ────────┘   └──────── Block 2 ────────┘   └──────── Block 3 ────────┘
```

### Driver Configuration

| Parameter | Value |
|-----------|-------|
| Driver | SimpleFOC-compatible |
| Supply Voltage | 12-24V (configurable) |
| PWM Output | 0-4V unipolar (bipolar currents via floating neutral) |
| Control | FOC (Field-Oriented Control) |
| Current Limit | 2A continuous |

---

## Scalability Notes

The design can be scaled while maintaining these **invariant ratios**:

```
Coil width / Pole pitch = 1/6
Spacer width / Magnet width = 0.9-1.2
Pole pitch / Tube diameter ≈ 1-2 (for good field geometry)
```

**Scaling effects:**
- **Larger pole pitch**: Lower electrical frequency for same velocity, higher voltage for same speed
- **More coil blocks**: Higher force density, longer mover
- **Thicker magnets**: Stronger field, higher force, more expensive

---

## Verification Plan

| Step | Method | Status |
|------|--------|--------|
| 1. FEMM simulation | Static field + force calculation | ✓ Complete |
| 2. Python dynamics | MMK traveling wave simulation | ✓ Complete |
| 3. Static force test | Measure force vs current | Pending |
| 4. Dynamic test | Velocity control with FOC | Pending |
| 5. Performance validation | Force, efficiency, thermal | Pending |

---

*For winding theory details, see WINDING_CONFIG.md. For build instructions, see BUILDING.md.*
