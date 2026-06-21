"""Map each legend toggle's contribution to Pattern A's position offset.
For each toggle: fresh env → click toggle → click oval → read frame 5 position.
Default final position (frame 5, no toggles changed): (R3, C4) = rows 21-24, cols 30-33.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

char = {0:'.',1:'f',3:'d',4:'v',5:'#',9:'B',10:'L',11:'Y'}

PIECES = [
    ("A-h", 42, 26), ("A-v", 45, 26),
    ("B-h", 42, 36), ("B-v", 45, 36),
    ("C-h", 42, 41), ("C-v", 45, 41),
    ("D-h", 42, 21), ("D-v", 45, 21),
    ("E-h", 42, 31), ("E-v", 45, 31),
]

def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    return env, obs

def click(env, col, row):
    return env.step(GameAction.ACTION6, {'x': col, 'y': row})

def read_patternA_position(obs_after_oval):
    """From the 7 animation frames, extract the FINAL ACCUMULATED position of Pattern A.
    That is the NEW yellow cells in Frame 5 (the last animated frame before return).
    Returns (tile_row, tile_col) in 4x4 tile coordinates, or None if not moved.
    """
    frames = obs_after_oval.frame
    if len(frames) < 7:
        return None, None, None
    # Frame 5 vs Frame 6 (final resting): find cells that changed back
    g5 = np.array(frames[5])
    g6 = np.array(frames[6])
    # In Frame 6, Pattern A returns to initial. In Frame 5, it's at displaced position.
    # Find cells that are yellow in frame 5 but not in frame 6 (= displaced position)
    yellow_f5 = np.argwhere(g5 == 11)
    yellow_f6 = np.argwhere(g6 == 11)

    # Cells yellow in f5 but not f6 = displaced position
    displaced = set(map(tuple, yellow_f5.tolist())) - set(map(tuple, yellow_f6.tolist()))
    # Cells yellow in f6 but not f5 = original position (cleared in f5)
    original = set(map(tuple, yellow_f6.tolist())) - set(map(tuple, yellow_f5.tolist()))

    if not displaced:
        # Pattern A didn't move in frame 5 — check frame 4
        g4 = np.array(frames[4])
        yellow_f4 = np.argwhere(g4 == 11)
        displaced = set(map(tuple, yellow_f4.tolist())) - set(map(tuple, yellow_f6.tolist()))

    if not displaced:
        return None, None, None

    rows = [r for r,c in displaced]
    cols_d = [c for r,c in displaced]
    if not rows:
        return None, None, None
    r_min, c_min = min(rows), min(cols_d)
    # Convert to tile coordinates
    tile_r = (r_min - 9) // 4
    tile_c = (c_min - 14) // 4
    return tile_r, tile_c, (r_min, c_min)

def read_all_frame5_positions(obs_after_oval):
    """Read Pattern A position in EVERY frame (1-5) of animation."""
    frames = obs_after_oval.frame
    if len(frames) < 7:
        return []
    g6 = np.array(frames[6])  # resting state
    yellow_rest = set(map(tuple, np.argwhere(g6 == 11).tolist()))

    positions = []
    for fi in range(1, 6):
        gf = np.array(frames[fi])
        yellow_f = set(map(tuple, np.argwhere(gf == 11).tolist()))
        displaced = yellow_f - yellow_rest
        if displaced:
            rows = [r for r,c in displaced]
            cols_d = [c for r,c in displaced]
            r_min, c_min = min(rows), min(cols_d)
            tile_r = (r_min - 9) // 4
            tile_c = (c_min - 14) // 4
            positions.append((fi, tile_r, tile_c, r_min, c_min))
        else:
            positions.append((fi, None, None, None, None))  # pattern didn't move
    return positions

# ── Baseline: no toggles changed ──────────────────────────────────────
print("="*60)
print("BASELINE: click oval only (no toggles)")
env0, obs0 = fresh()
obs_oval = click(env0, 36, 55)
baseline_positions = read_all_frame5_positions(obs_oval)
print(f"  {len(obs_oval.frame)} frames returned")
print("  Per-frame Pattern A positions (tile_row, tile_col, pixel_row, pixel_col):")
for fi, tr, tc, pr, pc in baseline_positions:
    print(f"    Frame {fi}: tile({tr},{tc}) = pixel rows {pr}-{pr+3 if pr else '?'}, cols {pc}-{pc+3 if pc else '?'}")

print(f"\n  Frame 5 (final accumulated): tile({baseline_positions[4][1]},{baseline_positions[4][2]})")
baseline_f5_tile = (baseline_positions[4][1], baseline_positions[4][2])

# ── Probe each toggle individually ─────────────────────────────────────
print("\n" + "="*60)
print("EACH TOGGLE's EFFECT ON FRAME 5 POSITION (vs baseline)")
print("="*60)
offset_table = {}
for name, prow, pcol in PIECES:
    env, obs = fresh()
    obs_toggle = click(env, pcol, prow)
    obs_oval = click(env, 36, 55)

    if len(obs_oval.frame) < 7:
        print(f"  {name}: only {len(obs_oval.frame)} frames — no animation")
        continue

    positions = read_all_frame5_positions(obs_oval)
    f5 = positions[4] if positions else (4, None, None, None, None)
    f5_tile = (f5[1], f5[2])

    # Also get all frame positions
    all_pos = [(pos[0], pos[1], pos[2]) for pos in positions]

    delta_r = f5_tile[0] - baseline_f5_tile[0] if f5_tile[0] is not None else None
    delta_c = f5_tile[1] - baseline_f5_tile[1] if f5_tile[1] is not None else None

    offset_table[name] = (delta_r, delta_c, f5_tile)
    print(f"  {name:6s}: F5={f5_tile}  delta=({delta_r},{delta_c})  "
          f"all=[{', '.join(f'F{p[0]}:({p[1]},{p[2]})' for p in all_pos)}]")

print("\nOffset summary (delta rows, delta cols from baseline F5=(R3,C4)):")
for name, (dr, dc, tile) in offset_table.items():
    print(f"  {name}: dr={dr:+d}, dc={dc:+d}" if dr is not None else f"  {name}: N/A")

# ── Try all-zero-offset combinations ──────────────────────────────────
print("\n" + "="*60)
print("FINDING WIN: What combination gives offset = (0,0) from baseline (= zero delta)?")
print("="*60)
# Or offset that brings to R1,C4 (tile (1,4)) from baseline R3,C4 — needs dr=-2, dc=0
target_tile = (1, 4)  # initial pattern A position tile
needed_delta = (target_tile[0] - baseline_f5_tile[0], target_tile[1] - baseline_f5_tile[1])
print(f"Baseline F5 tile: {baseline_f5_tile}")
print(f"Target tile (Pattern A initial position): {target_tile}")
print(f"Needed delta: {needed_delta}")

# Simple single-toggle tests with oval click + level check
print("\n" + "="*60)
print("TEST COMBINATIONS: check levels after oval click")
print("="*60)

def test_config(toggle_names, desc):
    env, obs = fresh()
    for name in toggle_names:
        prow = next(p[1] for p in PIECES if p[0]==name)
        pcol = next(p[2] for p in PIECES if p[0]==name)
        click(env, pcol, prow)
    obs_oval = click(env, 36, 55)
    f5_pos = read_all_frame5_positions(obs_oval)
    f5_tile = (f5_pos[4][1], f5_pos[4][2]) if f5_pos else (None,None)
    won = obs_oval.levels_completed > 0
    print(f"  {desc}: F5={f5_tile}  WON={won}")
    if won:
        print(f"    *** LEVEL COMPLETE! ***")
    return won

# Based on offset table, try combinations targeting (R1,C4) = (1,4)
test_config([], "no changes (baseline)")
test_config(["D-v"], "toggle D-v off")
test_config(["E-v"], "toggle E-v off")
test_config(["D-v","E-v"], "toggle D-v and E-v off")
test_config(["D-h"], "toggle D-h off")
test_config(["E-h"], "toggle E-h off")
test_config(["D-h","E-h"], "toggle D-h and E-h off")
test_config(["D-h","D-v","E-h","E-v"], "toggle ALL D and E off (all lt-grey)")

# Also test without oval — maybe win happens just from toggles
print("\n" + "="*60)
print("TEST: win by toggle alone (no oval click)")
print("="*60)
for toggle_seq in [["D-v","E-v"], ["D-h","E-h"], ["D-h","D-v","E-h","E-v"]]:
    env, obs = fresh()
    for name in toggle_seq:
        prow = next(p[1] for p in PIECES if p[0]==name)
        pcol = next(p[2] for p in PIECES if p[0]==name)
        obs = click(env, pcol, prow)
    won = obs.levels_completed > 0
    print(f"  {toggle_seq}: WON={won}")

# Check: what does level completion look like?
print("\n" + "="*60)
print("RENDER frame 5 for baseline and key combos (grid + legend)")
print("="*60)

def render_frames_1_5(obs_oval, label):
    print(f"\n  [{label}]")
    frames = obs_oval.frame
    if len(frames) < 6:
        print("    (fewer than 6 frames)")
        return
    for fi in [5]:
        gf = np.array(frames[fi])
        print(f"  Frame {fi} grid (yellow rows):")
        for r in range(9, 41):
            if any(gf[r,c]==11 for c in range(14,51)):
                row = ''.join(char.get(int(gf[r,c]),'?') for c in range(14,51))
                print(f"    row{r:2d}: {row}")
        row42 = ''.join(char.get(int(gf[42,c]),'?') for c in range(13,51))
        print(f"  Frame {fi} legend row42: {row42}")

env0, obs0 = fresh()
obs_oval_base = click(env0, 36, 55)
render_frames_1_5(obs_oval_base, "baseline")

env1, obs1 = fresh()
click(env1, 45, 21)  # D-v off
click(env1, 45, 31)  # E-v off
obs_oval_dv_ev = click(env1, 36, 55)
render_frames_1_5(obs_oval_dv_ev, "D-v off + E-v off")
