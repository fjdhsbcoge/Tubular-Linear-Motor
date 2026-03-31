# Building Instructions

## BOM

### Stator
- Steel tube: OD 24 mm, ID 20 mm
- N40 magnets: 20× (dia 19 mm, thickness 3-4 mm)
- 1006 steel disks: 20× (dia 19 mm, thickness 0.5-1 mm)
- Field shapers: 20× (dia 19 mm, rounded OD)

### Mover
- Core laminations: 1006 steel
- Wire: 0.4 mm Litz copper (~120 m)
- Housing: Aluminum/plastic

### Electronics
- 3-phase inverter (48V, 10A)
- FOC controller (SimpleFOC/ODrive)
- Position encoder (1000+ CPR)

---

## Assembly

### 1. Stator Stack
Order inside tube:
```
[Magnet N] - [Steel] - [Field Shaper] - [Magnet S] - [Steel] - ...
```
Bond with Loctite 638. Verify alternating polarity with compass.

### 2. Mover Winding
Pattern: **A-b-C-a-B-c** (18 coils)
- Coil width: 5 mm
- 6 coils per phase
- Alternate winding directions
- Star connection

Target resistance: 5.6 Ω per phase

### 3. Electronics
- Connect phases A, B, C to inverter
- Install encoder
- Run FOC commissioning

---

## Commissioning

1. **DC test**: Apply 12V to Phase A → mover locks
2. **Shift test**: Phase B → shifts 10 mm (1/3 pole pitch)
3. **Encoder align**: Set offset so zero electrical angle matches mechanical zero
4. **FOC tune**: Tune current PI controllers

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No force | Check phase sequence |
| Weak force | Increase current limit |
| Cogging | Recalibrate encoder offset |
| Heating | Reduce current or add cooling |

---

*For winding details, see WINDING_CONFIG.md. For theory, see PRINCIPLE.md.*
