# Principle of Operation

## Magnetic Gearing

Two sine-wave magnetic fields interlock like gear teeth to produce linear force without contact.

**Stator (inside tube):**
- Alternating N-S magnets with steel disks
- Rounded ferromagnetic discs shape the field into a sine wave
- Creates outward sine-wave field (static)

**Mover (surrounds stator):**
- 3-phase coils in ferromagnetic slots
- Creates traveling sine-wave field (inward)

**Force:** Fields mesh like gear teeth. When mover field travels (driven by 3-phase currents), it pulls the mover along.

```
Stator:  ~~~ ~~~ ~~~ ~~~  (static outward)
             ↕ ↕ ↕ ↕
Mover:   ~~~ ~~~ ~~~ ~~~  (traveling inward)
             ↑ ↑ ↑ ↑
           Force
```

**Key:** Coil width = Pole pitch / 6 = 5 mm (for 30 mm pole pitch)

---

## Specifications

| Parameter | Value |
|-----------|-------|
| Pole Pitch (N-to-N) | 30 mm |
| Pole Width (N-to-S) | 15 mm |
| Circumference | 81.68 mm (from FEMM) |
| Peak Force | ~0.6 N (Fx per phase, from Excel) |
| Phases | 3, star-connected |

---

## Field Profile

FEMM simulation shows:
- Peak B-field: ~0.02 T
- Period: 30 mm (pole pitch)
- Clean sine wave confirms field shaping works

See `simulations/images/` for field visualizations.

---

*For construction details, see BUILDING.md. For winding configuration, see WINDING_CONFIG.md.*
