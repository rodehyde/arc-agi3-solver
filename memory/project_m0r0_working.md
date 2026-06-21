---
name: project-m0r0-working
description: m0r0 current game notes (clear when switching games)
metadata: 
  node_type: memory
  type: project
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

# m0r0 Working Notes

**Why:** Per-task memory for the m0r0 ARC-AGI-3 game. Clear when switching games.

## Status
**COMPLETE — all 6 levels solved.**

## Baseline Actions (all 6 levels)
[30, 111, 203, 26, 500, 237]
L1=30, L2=111, L3=203, L4=26, L5=500, L6=237.

## Game mechanics (confirmed)

**Game type:** Two coupled lt-blue (value=10) 4×4 blocks navigating a maze. No visible player.

**Win mechanic (confirmed L1–L6):** Navigate blocks to OVERLAP (same position). Level completes when both blocks occupy the same (row, col). Can be triggered by CONVERGE or by UP/DOWN movement landing one block on the other's position.

**Actions (confirmed L1–L6):**
- ACTION1: both blocks UP (4 rows)
- ACTION2: both blocks DOWN (4 rows)
- ACTION3: blocks DIVERGE (L→left 4, R→right 4)
- ACTION4: blocks CONVERGE (L→right 4, R→left 4)
- ACTION5: no effect (border counter only)
- ACTION6 (click): freeze mechanic when click lands on blue marker (value=9)

**Freeze mechanic (L3–L6):**
- Click ON blue marker (value=9) → blocks freeze (lt-blue→lt-grey), marker becomes yellow
- DIV/CON in frozen state move the YELLOW MARKER horizontally (step=4)
- UP/DOWN in frozen state move the YELLOW MARKER vertically (step=4) ← CONFIRMED (was wrong in earlier notes)
- Click on a NON-marker cell (any black cell) → unfreeze, blocks return to FROZEN POSITION
- After unfreeze: yellow marker permanently becomes new blue marker at new position

**Pin mechanic (L5–L6):** Blue marker placed at a block's destination row prevents that block from moving in that direction. Only the other block moves. Breaks the column invariant (A.col + B.col = 60).

**Band mechanic (L6):** Each gate/band opens when ONE block presses its corresponding marker. A presses orange marker (rows 14–17 cols 18–21) → orange band opens. B presses green marker (rows 14–17 cols 42–45) → green band opens. When BOTH blocks at rows 14 simultaneously → BOTH bands open. The lower green object (rows 42–45, cols 18–21, value=14) ALSO opens the green band when occupied.

**Independent movement:** When one block is physically blocked (wall, marker pin), only the unblocked block moves.

---

## Level Solutions

### Level 1
- Solution: `UUXUUUUUCUCCCCCDDDCDDDDDXD`
- Our moves: 26 | Baseline: 30 | RHAE: 1.33

### Level 2
- Solution: `DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU`
- Our moves: 30 | Baseline: 111 | RHAE: 13.7

### Level 3
- Marker moves: Blue-1 click(31,15)→R,U,R×4,D×3,L×2,U→restore(14,46); Blue-2 find→U,R,U→restore(14,46); Blue-3 find→R×3→restore(14,46)
- Navigation: `UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC`
- Our moves: ~58 total | Baseline: 203

### Level 4
- Key mechanic: move marker to L's column BEFORE approaching.
- Sequence: U,U,A6(30,30),X,X,X,A6(restore),D,D,C,D,C,C (13 actions)
- Our moves: 13 | Baseline: 26 | RHAE: 4.0

### Level 5
- Key mechanic: Pink gap pins L on lower switch → R navigates right shaft independently.
- Solution: `XXUUUUUUXUCCCCUUXXXXXXUUUUUUUUCCCCCCXXXUUUUUXXXX`
- Our moves: 48 | Baseline: 500 | RHAE: ~108

### Level 6
- **Key insight:** Use 3 freeze operations to sequentially pin each block while the other navigates. Win position: both blocks overlap at rows 42, col 18 (green object).
- **Sequence from L6 start (48 actions):**
  - Phase 0: UP×2 (to rows 14, both bands open), freeze@(43,31), DIV×2+UP×1+DIV×1+UP×5→(19,19), unfreeze → marker pins A from DOWN
  - Phase 1: DOWN×7 → B through orange band to (42,42). A stays at (14,18).
  - Phase 2: freeze@(19,19), CON×1+UP×1→(15,23), unfreeze → marker pins A from CONVERGE
  - Phase 3: CONVERGE×6 → B moves left (42,42)→(42,18) landing on green object. Green band opens.
  - Phase 4: freeze@(15,23), DOWN×8+DIV×1→(47,19), unfreeze → marker pins B from DOWN
  - Phase 5: DOWN×7 → A descends from (14,18) through open green band to (42,18). Overlap → WIN.
- Our moves: 48 | Baseline: 237 | RHAE: (237/48)² ≈ 24.4

---

## Key L6 learnings (keep for process improvement)

1. **The blue marker's FUNCTION as a blocker was not identified early enough.** It was probed, its behaviour observed, but its function as a "pin" was not written in the audit. This is the canonical failure that drove the CLAUDE.md restructuring.

2. **Opening one band at a time is possible** — A at orange marker (rows 14) opens orange band independently. The earlier assumption that BOTH blocks had to be at rows 14 simultaneously was wrong for single-band opening.

3. **The lower green object (rows 42–45 cols 18–21) also opens the green band** — same colour as upper green marker, same function. This was not identified from observation alone and had to be discovered experimentally.

4. **Win does not require CONVERGE** — A arrived at B's position via DOWN×7, which triggered the level complete.
