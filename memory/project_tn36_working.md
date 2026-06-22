---
name: project-tn36-working
description: tn36 L1-L5 solved; zone demonstration system confirmed; L6 next
metadata: 
  node_type: memory
  type: project
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

# tn36 Working Notes

**Why:** Per-task memory for the tn36 ARC-AGI-3 game. Clear when switching games.

## Status
**Levels 1–5 COMPLETE. Ready for L6.**

## Baseline Actions (all 7 levels)
[32, 72, 26, 40, 30, 55, 62]

## Game type
- Click-only. Only ACTION6 available. No movement actions.
- win_levels = 7

---

## LEVEL 1 (baseline=32) — COMPLETE

### Solution
```python
L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
```
7 clicks.

### Key mechanics
- 5-group legend, each group has H-bar (row 42) and V-bar (row 45)
- Clicking a mark TOGGLES it BLACK (active) or lt-grey (inactive)
- Pre-activated at L1 start: D group (cols 21) both bars black
- Blue oval (row 55, col 36) fires animation — 7 frames
- Pattern A moves in steps determined by active H/V marks; reaches Pattern B position when correct
- D and E groups control row movement; A, B, C control column movement
- Groups fire in order: D → A → E → B → C

### Legend offset table
- D-h: (+1 row, -1 col), D-v: (+1 row, +1 col)
- E-h: (+1 row, -1 col), E-v: (+1 row, +1 col)
- A/B/C-h: (0, -1), A/B/C-v: (0, +1)

---

## LEVEL 2 (baseline=72) — COMPLETE

### Solution
```python
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
```
14 clicks.

### Key mechanics (CONFIRMED)
- LEFT panel (cols 0-31): 4 left legend groups, left oval, left piece (vdk-grey=4)
  - Left legend row structure: H33 (row 33), V35 (row 35), H39 (row 39), V41 (row 41), H45 (row 45), V47 (row 47)
  - Pre-activated at L2 start: left legend V47 at all 4 groups = UP direction
  - Left oval at row 58, col 21
  - 4 left legend groups at cols 8, 13, 18, 23 (V-bar col) / 9, 14, 19, 24 (H-bar center)
  - H33+V47 = UP; H33+V35 = DOWN
- RIGHT panel (cols 32-63): 6 right legend groups, right oval, right piece (yellow=11)
  - Right legend groups at cols 33-59 (V-bar) / 34-59 (H-bar center)
  - Right oval at row 55, col 47
  - 4 active groups = 4 steps UP → piece reaches right cup
- Pre-activated element at L2 start = left legend V47 (UP config) = first thing to execute

---

## LEVEL 3 (baseline=26) — COMPLETE

### Solution
```python
L3 = [(58, 5), (33, 34), (47, 33), (35, 38), (35, 43), (35, 48), (35, 53), (33, 59), (47, 58), (58, 58)]
```
10 clicks.

### L3 grid structure
- LEFT panel: piece at rows 8-11, cols 14-17 (initial). Cup at rows 24-27.
- RIGHT panel: piece split across rows 20-23 cols 37-40 AND rows 11-15 cols 52-57 (initial).
  - Right cup: rows 8-15 (top of right panel, merged area).
- Pink column (value=6): cols 45-48, rows 4-15 and 20-31. GAP at rows 16-19 (black/vdk-grey) — the passage.

### L3 path (right panel)
1. Btn1 (LEFT panel DOWN): piece rows 8-11 → 24-27
2. Right group 1 (H33+V47): 1 UP step (lower piece rows 20-23 → 16-19, through pink gap)
3. Right groups 2-5 (V35 only): 4 RIGHT steps (cols 37-40 → 41-44 → 45-48 → 49-52 → merge)
4. Right group 6 (H33+V47): 1 UP step (rows 16-19 → 11-15, into cup)
5. Right oval (row 58, col 58)

### L3 confirmed mechanics
- **Left buttons (row 58):** Btn1=col5 (DOWN), Btn2=col15 (UP), Btn3=col25 (LEFT), Btn4=col35 (RIGHT)
  - Btn1 moves left piece: rows 8-11 → 24-27 (DOWN, 6-frame animation)
  - Btn2 moves left piece: UP
- **Right legend:** 6 groups (vs 4 groups in L2)
  - Group col positions: V-bar at cols 33,38,43,48,53,58; H33-bar centers at cols 34,39,44,49,54,59
  - Right oval at row 58, col 58

### Direction mappings (CONFIRMED from L3/L4)
| Legend config | Direction |
|---|---|
| H33 + V47 | UP |
| H33 + V35 | DOWN |
| V35 + V47 (both, no H) | LEFT (CONFIRMED L4) |
| V35 only (no H) | RIGHT (CONFIRMED L3) |
| H33 + V41 | CONTRACT |
| V41 only | EXPAND |

**STRUCTURAL RELATIONSHIP — re-derive each level, don't assume values carry forward:**
The left legend's pre-activated bars at level start encode the right legend's direction configurations for that level. Read the left legend's initial state at the start of each new level and use it to derive which right legend bar combinations correspond to which directions. Do not assume the mapping from the prior level is unchanged — confirm it from the current level's observed state.

---

## Frame count semantics
- 1 frame = no animation (no-op click)
- 6 frames = animation triggered (button press / left panel animation)
- 8 frames = oval-triggered animation (right panel)
- 9+ frames = level completion flash (11 frames confirmed for L3)

---

## Scripts written
- `scripts/tn36_l2_step4.py` — L2 solution
- `scripts/tn36_l3_step1.py`, `scripts/tn36_l3_step2.py` — L3 probing
- `scripts/tn36_l3_step4.py` — L3 solution (SUCCESS)
- `scripts/tn36_l4_step1.py` — L4 scene description
- `scripts/tn36_l4_step2.py` — L4 action table probing
- `scripts/tn36_l4_step2b.py` — L4 element audit targeted probes

---

## LEVEL 4 (baseline=40) — COMPLETE

### Solution
```python
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),(33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]
```
13 clicks. RHAE ≈ 9.47.

### Sequence (right legend only, one oval fire)
- g1: H33+V41 = CONTRACT (piece shrinks to 4 wide at rows 8-11, c45-48)
- g2: V35+V47 = LEFT (piece slides to c41-44, aligned with gap and cup)
- g3-g6: H33+V35 = DOWN ×4 (piece drops through pink gap at rows 20-23, lands in cup rows 24-27)
- Left piece: NO ACTION needed

### Key L4 findings
- LEFT = V35+V47 (both V-bars active, no H-bar) — NOT V47-only
- Background cells (vdk-grey=4) are TRAVERSABLE: pieces slide through them to next boundary
- Pink band gap at c41-44, rows 20-23
- Right piece cup interior: c41-44, rows 24-27
- Left piece (rows 16-19, c22-25) is irrelevant to L4 win

### L4 grid structure
- LEFT panel (cols 1–30, rows 3–31): entirely dk-grey background — NO visible cup/target
  - Left piece (vdk-grey=4): rows 16–19, cols 22–25 (4×4 block)
  - Left piece canonical animation origin: rows 4–7, cols 2–5
- RIGHT panel (cols 33–62, rows 3–31): checkerboard path (vvvv/#### tiles)
  - Upper yellow piece (agent): rows 8–15, cols 46–53 (8-wide, U-shape opening downward with hole at r14–15 c48–51)
  - Pink band (obstacle): rows 20–23. Gap at c42–45 (black=####). Pink everywhere else.
  - Lower yellow cup (target): rows 24–28, cols 41–46. U-shape opening upward. Interior c42–45 rows 24–27, floor at r28 c41–46.

### CRITICAL STRUCTURAL MISMATCH (open question)
Pink band gap is c42–45 (4 cells wide). Right piece is c46–53 (8 cells wide). They DON'T ALIGN.
The right piece cannot currently pass through the gap. How it gets there is UNKNOWN.

### L4 Button area (rows 54–62, right panel cols 39–62 = Right Oval)
| Button | Click pos | Legend config set | Direction/Effect | Frames |
|--------|-----------|-------------------|-----------------|--------|
| Left Blue Box | r58c5 | reads current config | LEFT ×3 (with V35+V47 default) | 5 |
| Box-A | r58c15 | V41-only | EXPAND animation (canonical, NOT persistent) | 5 |
| Box-B | r58c25 | H33+V35 | DOWN ×3 | 5 |
| Box-C | r58c35 | H33+V41 | CONTRACT animation + piece teleports to r4–7 c2–5 | 5 |
| Right Oval | r58c58 | reads right legend | fires right piece movement | 8 |

### Left legend state (L4 start)
- V35–37: ACTIVE (black=5), V41–43: INACTIVE (lt-grey=1), V47–49: ACTIVE (black=5)
- H-bars (rows 33, 39, 45): all INACTIVE
- Default config V35+V47 = LEFT direction for left piece

### Direction mappings confirmed at L4
| Config | Left piece effect |
|--------|------------------|
| V35+V47 (default) | LEFT ×3 |
| H33+V35 (Box-B) | DOWN ×3 |
| V41-only (Box-A) | LEFT ×3 (same as default!) |
| H33+V41 (Box-C) | LEFT ×3 (same as default!) |

### Right legend observations
- V47-only (right legend, 1 group) + oval: NO movement (piece blocked by wall on left)
- H33+V35 (right legend, 1 group) + oval: DOWN 4 rows, BOUNCES BACK
- H33+V47 (right legend, 1 group) + oval: UP (confirmed earlier)
- V35-only (right legend, 1 group) + oval: RIGHT (confirmed earlier)
- Right piece always BOUNCES unless it lands on its target

### EXPAND/CONTRACT findings
- Box-A: EXPAND animation only — shows piece growing to 224 cells at canonical r4–19 c2–17 — NOT persistent (piece returns to actual position r16–19 c22–25)
- Box-C: CONTRACT animation — IS persistent — piece TELEPORTS to canonical contracted position r4–7 c2–5

### V-bar structure change from L3 to L4
- L3: single-row V-bars
- L4: 3-row V-bar units (rows 35–37, 41–43, 47–49 per type). Toggle as unit.
- Sub-row count does NOT affect step count

### OPEN QUESTIONS for Step 3
1. How does the 8-wide right piece pass through the 4-wide pink band gap? (Main unsolved puzzle)
2. Why does Box-A EXPAND if it's not persistent? What game-state change does it produce?
3. The left piece has no visible cup — what is its win condition?
4. Frame count changed: L4 buttons = 5 frames (L3 was 6). Semantic difference?

---

## LEVEL 5 (baseline=30) — COMPLETE

### Solution
```python
L5_actions = [
    (33,34),(39,34),          # g1: ROTATE  (H33+H39)
    (33,39),(35,39),          # g2: DOWN    (H33+V35)
    (33,44),(35,44),          # g3: DOWN
    (33,49),(35,49),          # g4: DOWN
    (41,54),                  # g5: EXPAND  (V41)
    (33,59),(35,59),(39,59),(41,59),(45,59),(47,59),  # g6: TURN PURPLE (ALL 6 bars)
    (58,58),                  # fire right oval
]
```
16 clicks. RHAE = (30/16)² ≈ 3.52.

### L5 key mechanics

**Zone demonstration system (confirmed):**
The LEFT panel zone buttons (row 58, cols 5/15/25/35/45) demonstrate what to configure in the RIGHT legend:
- Zone 1 (col 5): blue box — CONTRACTS piece (14→56→126→224→ back via animation only; not persistent)
- Zone 2 (col 15): EXPANDS piece (14→56→126→224 cells); encoding = V41
- Zone 3 (col 25): piece moves DOWN 3 steps (rows 8-11→20-23); encoding = H33+V35
- Zone 4 (col 35): piece ROTATES (shape changes: hole moves CCW bottom→left→top→right); encoding = H33+H39
- Zone 5 (col 45): piece TURNS PURPLE (yellow → value 15, fills left target); encoding = all 6 bars: H33+V35+H39+V41+H45+V47

**CRITICAL: "Turn purple" requires ALL 6 bar types.** Zone 5's final legend state = H33+V35+H39+V41+H45+V47 all active. Pre-activated bars (H33+V41 from level start) still need to be clicked in for each new group — they are NOT inherited.

**Rotation mechanic:**  
Zone 4 animation shows bounding box stays fixed but piece shape rotates CCW across frames:
- f0: hole at BOTTOM (row 19)
- f1: hole at LEFT (rows 17-18 left col)
- f2: hole at TOP (row 16)  
- f3/f4: hole at RIGHT (rows 17-18 right col) — matches the right panel's target piece orientation
One ROTATE click = one 90° CCW step. To match target: 1 rotate.

**Direction encodings confirmed (L5):**
| Config | Effect |
|--------|--------|
| H33+H39 | ROTATE 90° CCW |
| H33+V35 | DOWN |
| V41 | EXPAND |
| H33+V35+H39+V41+H45+V47 (all 6) | TURN PURPLE (place in target) |

### L5 grid structure
- Left panel: blue-bordered box at rows 8-11 cols 14-17 (initial, 14 cells, L-shape with hole at bottom)
- Left zone buttons: row 58 at cols 5,15,25,35,45
- Right panel: yellow piece at rows 8-11 cols 49-52; purple target area around rows 12-27 cols 49-60
- Right legend: 6 groups at RC=[34,39,44,49,54,59]; right oval at (58,58)

### Pre-activated bars at L5 start
- H33 and V41 active for all 3 pre-existing groups → Contract config
- Structural relationship still holds: pre-activated state = clue about level's operative configs
