# Winding Configuration

From Excel: `260331 Coil Config and Force Profile.xlsx` — Sheet 1

## Coil Arrangement

18 coils in pattern: **A-b-C-a-B-c** repeating
- Uppercase (A,B,C): Clockwise winding (+)
- Lowercase (a,b,c): Counter-clockwise winding (-)
- 6 coils per phase

## Target Field Pattern (per phase)

Each phase creates this sinusoidal field across coils:
```
Coil:  1   2   3   4   5   6   7   8   9   10  11  12...
Field: -2  -1   1   2   1  -1  -2  -1   1   2   1  -1...
```

Pattern repeats every 6 coils (one pole pitch = 30 mm).

## Phase Shifts

- **Phase A**: Starts at coil 1
- **Phase B**: Shifted 2 coils (30°) — starts at -2
- **Phase C**: Shifted 4 coils (60°) — starts at -2

Electrical phase shifts: **150°** (A→B), **90°** (A→C)

These non-standard shifts optimize the traveling wave for this specific winding.

## Current Distribution

Per Kirchhoff (rows 5-7 in Excel):
- 6 coils at +2A
- 12 coils at -1A  
- Sum = 0 ✓

The -1A currents are return paths through other phases.

## 3-Phase Sum

When all phases active (row 20):
```
Result: -2, -6, -2, 2, 6, 2, -2, -6, -2...
```

Amplitude: **±6** (3× single phase)

This creates the traveling magnetic wave.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Pole Pitch | 30 mm |
| Coils | 18 (6 per phase) |
| Coil Width | 5 mm |
| Design Current | 2A per phase |

---

*For construction, see BUILDING.md. For theory, see PRINCIPLE.md.*
