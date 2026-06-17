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
Level 1 complete. Ready for Level 2.

## Baseline Actions (all 6 levels)
[30, 111, 203, 26, 500, 237]

## Game mechanics (confirmed from Level 1)

**Game type:** Two coupled 5×5 lt-blue blocks navigating a maze. No visible player.

**Key mechanic:** Blocks navigate WITHIN black wall cells. Yellow/orange background cells cannot be occupied. The black structure IS the track.

**State representation:** (row, left_col, right_col) — both blocks always share the same row. Columns and rows move in steps of 5.

**Actions:**
- ACTION1: both blocks move UP 5 rows
- ACTION2: both blocks move DOWN 5 rows
- ACTION3: blocks DIVERGE — left block moves left 5, right block moves right 5
- ACTION4: blocks CONVERGE — left block moves right 5, right block moves left 5
- ACTION5: no effect (observed)
- ACTION6 (click): no effect from initial state (observed)

**BFS approach works:** State space is small (~144 states for L1). Replay-from-scratch BFS over real game states finds optimal solutions.

## Level Solutions

### Level 1
- Solution: `UUXUUUUUCUCCCCCDDDCDDDDDXD`
- Our moves: 26
- Baseline: 30
- RHAE: (30/26)² ≈ 1.33
