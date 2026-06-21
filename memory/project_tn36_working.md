---
name: project-tn36-working
description: tn36 current game notes (clear when switching games)
metadata: 
  node_type: memory
  type: project
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

# tn36 Working Notes

**Why:** Per-task memory for the tn36 ARC-AGI-3 game. Clear when switching games.

## Status
**Level 1 — Step 1 REDONE and complete. Awaiting user confirmation to proceed to Step 2.**

Training mode hard stop triggered. Primary Step 2 target: run one oval click, then a SECOND oval click with same config, and compare Pattern A's resting position between them. This resolves "accumulate vs display-only."

## Baseline Actions (all 7 levels)
[32, 72, 26, 40, 30, 55, 62]
Level 1 baseline = 32 clicks.

## Game type
- Click-only. Only ACTION6 available. No movement actions.
- win_levels = 7

## KEY DISCOVERY: Multi-frame animation
**obs.frame returns 1 layer in the initial state but 7 layers after an oval click.**
This was completely missed in the first pass (was only reading obs.frame[-1]).

**7-frame structure after oval click:**
- Frame 0: oval activates (blue→lt-blue) + bar decrements by 1
- Frames 1–5: each legend group highlighted with blue border, Pattern A shown at cumulative offset position
  - Frame 1: after D group applied
  - Frame 2: after D+A applied
  - Frame 3: after D+A+E applied
  - Frame 4: after D+A+E+B applied
  - Frame 5: after D+A+E+B+C applied (FINAL accumulated position)
- Frame 6: everything returns to resting state (Pattern A back at tile(1,4))

The animation fires groups in order: D → A → E → B → C (not alphabetical).

## Grid structure (CONFIRMED from Step 2 probing)

Values present: 0=white, 1=lt-grey, 4=vdk-grey, 5=black, 9=blue, 11=yellow

**Zone map:**
- Row 1, cols 1–61: blue bar (value=9, 61 cells) — action counter, decrements per click
- Rows 9–40, cols 14–49: checkered grid — alternating 4×4 tiles of black (5) and vdk-grey (4)
  - 8 tile-rows × 9 tile-cols. Tile(i,j): rows 9+4i to 9+4i+3, cols 14+4j to 14+4j+3
  - Tile is BLACK if i+j even, VDK-GREY if i+j odd
- Rows 13–16, cols 30–33: Yellow Pattern A (14 cells) — tile(1,4)
- Rows 33–37, cols 29–34: Yellow Pattern B (~16 cells) — approximately tile(6,3-4)
- Rows 41–47, cols 13–50: Legend zone — 5 groups of 2 bars each
- Rows 51–59, cols 32–40: Blue oval — the only interactive action button

**Yellow Pattern A** (14 cells, resting at tile(1,4) = rows 13–16, cols 30–33):
Exact shape TBD. Participates in animation.

**Yellow Pattern B** (~16 cells, rows 33–37, cols 29–34):
Stationary. GEOMETRIC FACT: Pattern A (14 cells) + complement-of-Pattern-B within the shared 5×6 rectangle = fills the rectangle exactly. They are complementary shapes.

**Legend zone — 5 groups, each with H-bar (row 42) and V-bar (row 45):**
- Group D: cols 20–22 (H), col 21 (V) — INITIALLY BLACK
- Group A: cols 25–27 (H), col 26 (V) — initially lt-grey
- Group E: cols 30–32 (H), col 31 (V) — INITIALLY BLACK
- Group B: cols 35–37 (H), col 36 (V) — initially lt-grey
- Group C: cols 40–42 (H), col 41 (V) — initially lt-grey

Click positions confirmed:
- A-h: (row=42, col=26), A-v: (row=45, col=26)
- B-h: (row=42, col=36), B-v: (row=45, col=36)
- C-h: (row=42, col=41), C-v: (row=45, col=41)
- D-h: (row=42, col=21), D-v: (row=45, col=21)
- E-h: (row=42, col=31), E-v: (row=45, col=31)

## Legend toggle offset table (CONFIRMED from tn36_offsets.py)

Each toggle's contribution to Pattern A's Frame-5 tile position when BLACK (active):
- D-h: (+1 row, -1 col)
- D-v: (+1 row, +1 col)
- E-h: (+1 row, -1 col)
- E-v: (+1 row, +1 col)
- A-h: (0, -1)
- A-v: (0, +1)
- B-h: (0, -1)
- B-v: (0, +1)
- C-h: (0, -1)
- C-v: (0, +1)

D and E each contribute row movement. A, B, C contribute column movement only.

**Initial state (D+E all black, A/B/C all lt-grey):**
Row offset = +4, col offset = 0. F5 tile = tile(3,4) = rows 21–24, cols 30–33.

**With ALL 10 pieces black:** F5 tile = tile(3,4) (A,B,C add zero row change).
**Maximum achievable F5 tile row = 3.**

## CRITICAL OPEN QUESTION (primary Step 2 target)

Pattern B is at approximately tile row 6–7 (rows 33–37). Maximum achievable F5 row = tile 3. GAP = 3 tile rows.

**TWO possible resolutions:**
1. **Accumulation model**: Each oval click PERMANENTLY moves Pattern A's resting position by the current offset delta. Multiple oval clicks step Pattern A downward toward Pattern B. The "came back" the user observed = Frame 6 showing the NEW resting state (which may still look similar if only slightly displaced). This is consistent with baseline_actions=32 (too many for a single-click win).
2. **Display-only model**: The oval click only shows the animation; Pattern A always returns to tile(1,4). Win requires configuring the legend so F5 = Pattern B's position. But Pattern B appears unreachable.

**Confirming test:** click oval twice with same config; if Pattern A's Frame-1 position in the SECOND animation differs from the first, accumulation is confirmed.

## Brute force results (tn36_brute.py — NOT run, bug found and fixed)
All 1024 toggle-only configurations (no oval click) → no win. 
All 1-click + oval → no win.
All 45 two-click pairs + oval → no win.

## Scripts written
- `scripts/tn36_step1.py`, `scripts/tn36_step1b.py` — initial step 1 inspection
- `scripts/tn36_step2b.py` — second round step 2 probing (legend clicks confirmed)
- `scripts/tn36_obs_inspect.py` — KEY: revealed 7-frame animation structure
- `scripts/tn36_frames.py` — full 7-frame analysis, confirmed cumulative offset model
- `scripts/tn36_offsets.py` — measured all 10 toggle offsets
- `scripts/tn36_win_test.py` — systematic 1-click and 2-click win search
- `scripts/tn36_brute.py` — Gray code 1024-state brute force (has bug fix, never run)
