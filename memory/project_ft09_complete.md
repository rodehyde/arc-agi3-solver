---
name: project-ft09-complete
description: "ft09 game fully solved — 6 levels, mechanics confirmed, RHAE ~6.76"
metadata: 
  node_type: memory
  type: project
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

ft09 is COMPLETE (all 6 levels solved, win_levels=6).

**Why:** All levels solved analytically using the 4-step process. Total agent actions=80 vs human baseline=208.

**How to apply:** Skip ft09 if revisiting — already solved. Mechanics below are candidates for cross-game research (see [[project-arc3-research]]).

## Confirmed mechanics

- **Grid:** 6×6 tile slots; ROW_STARTS and COL_STARTS vary per level
- **KEY tiles:** contain white(0) cells, centre=green(14), frozen/unclickable
- **PLAIN tiles:** yellow(11) ↔ green(14) cycle on click, pink(6) notch top-right
- **Key rule (all 6 levels):** white position → neighbour target = centre (green); grey (md=2 OR dk=3) position → neighbour target = opposite (yellow)
- **Group toggle (confirmed L6):** clicking (ri,ci) also toggles (ri-1,ci) if that slot is a plain tile; keys and absent slots block the coupling
- **Level start state:** each level may start with tiles in a non-all-yellow state (L7/victory screen started in L6's solution state)

## Per-level solutions (stored in scripts/ft09_level.py SOLUTIONS dict)

| Level | Clicks | Human baseline | Notes |
|-------|--------|----------------|-------|
| L1 | 4 | 43 | solo clicks |
| L2 | 7 | 12 | |
| L3 | 14 | 23 | |
| L4 | 21 | 28 | some tiles clicked twice (cycle back) |
| L5 | 21 | 65 | pink-cross group toggle (self + 4 orthogonal) |
| L6 | 13 | 37 | domino-pair toggle (self + tile above); solved GF(2) linear system |

RHAE = (208/80)² ≈ 6.76
