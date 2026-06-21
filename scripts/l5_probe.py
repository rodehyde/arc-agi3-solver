"""Step 2: Action probe for m0r0 Level 5.
Full grid diff for every action. ACTION6 on every distinct object.
Physically probes adjacent to colored objects (green, orange, purple).
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
char = {0:'.', 1:'a', 5:'#', 6:'p', 7:'q', 8:'R', 9:'B',
        10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

def setup_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3):
        obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    for a in NAV3:
        obs = env.step(AMAP[a])
    for a in 'UU':
        obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})
    for _ in range(3):
        obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})
    for a in 'DDCDCC':
        obs = env.step(AMAP[a])
    return env, obs

def grid_diff(g_before, g_after):
    diff = np.where(g_before != g_after)
    if not len(diff[0]):
        return 0, None, {}
    rows, cols = diff
    bbox = (int(rows.min()), int(cols.min()), int(rows.max()), int(cols.max()))
    transitions = {}
    for r, c in zip(rows, cols):
        k = f"{char.get(int(g_before[r,c]),'?')}({g_before[r,c]})->{char.get(int(g_after[r,c]),'?')}({g_after[r,c]})"
        transitions[k] = transitions.get(k, 0) + 1
    return len(rows), bbox, transitions

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    lp = (int(left[:,0].min()), int(left[:,1].min())) if len(left) else None
    rp = (int(right[:,0].min()), int(right[:,1].min())) if len(right) else None
    return lp, rp

def render_zone(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     " + "".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        print(f"{r:3d}  {row}")

def probe(label, setup_fn, action, kwargs=None, nav=None):
    env, obs = setup_fn()
    if nav:
        for a in nav:
            obs = env.step(AMAP[a])
    g_before = np.array(obs.frame[-1])
    lp0, rp0 = block_pos(g_before)
    avail_before = set(obs.available_actions)
    if kwargs:
        obs2 = env.step(action, kwargs)
    else:
        obs2 = env.step(action)
    g_after = np.array(obs2.frame[-1])
    lp1, rp1 = block_pos(g_after)
    n, bbox, trans = grid_diff(g_before, g_after)
    avail_after = set(obs2.available_actions)
    avail_changed = avail_before != avail_after
    win = obs2.levels_completed > 4
    dl = f"dr={lp1[0]-lp0[0]},dc={lp1[1]-lp0[1]}" if lp0 and lp1 else "?"
    dr = f"dr={rp1[0]-rp0[0]},dc={rp1[1]-rp0[1]}" if rp0 and rp1 else "?"
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  cells={n}  bbox={bbox}")
    print(f"  transitions={trans}")
    print(f"  L:{lp0}->{lp1} ({dl})  R:{rp0}->{rp1} ({dr})")
    print(f"  avail_changed={avail_changed}  {'NEW:'+str(avail_after) if avail_changed else ''}")
    print(f"  WIN={win}")
    return obs2, g_after, avail_changed

# ── Confirm L5 start ──────────────────────────────────────────────────────────
env0, obs0 = setup_l5()
g0 = np.array(obs0.frame[-1])
lp, rp = block_pos(g0)
print(f"L5 start: L={lp}, R={rp}")
print(f"Available actions: {obs0.available_actions}")
print(f"levels_completed={obs0.levels_completed}  win_levels={obs0.win_levels}")
render_zone(g0, 46, 57, 2, 29, "Left shaft lower (near left block):")
render_zone(g0, 46, 57, 34, 61, "Right shaft lower (near right block):")

# ── Basic action probes from start ────────────────────────────────────────────
print("\n\n=== BASIC ACTION PROBES (from start) ===")
for label, act in [
    ("ACTION1 UP",       GameAction.ACTION1),
    ("ACTION2 DOWN",     GameAction.ACTION2),
    ("ACTION3 DIVERGE",  GameAction.ACTION3),
    ("ACTION4 CONVERGE", GameAction.ACTION4),
    ("ACTION5",          GameAction.ACTION5),
]:
    probe(label, setup_l5, act)

# ── ACTION6 on every distinct object ─────────────────────────────────────────
print("\n\n=== ACTION6 CLICK TARGETS ===")
a6_targets = [
    ("A6: left block (7,51)",           {"x":  7, "y": 51}),
    ("A6: right block (55,51)",          {"x": 55, "y": 51}),
    ("A6: purple left-lower (15,51)",    {"x": 15, "y": 51}),
    ("A6: purple left-upper (15,7)",     {"x": 15, "y":  7}),
    ("A6: green left (19,23)",           {"x": 19, "y": 23}),
    ("A6: orange left (15,39)",          {"x": 15, "y": 39}),
    ("A6: green right (35,27)",          {"x": 35, "y": 27}),
    ("A6: orange right (59,27)",         {"x": 59, "y": 27}),
    ("A6: purple right-upper (47,23)",   {"x": 47, "y": 23}),
    ("A6: purple right-lower (47,39)",   {"x": 47, "y": 39}),
    ("A6: black wall left (10,30)",      {"x": 10, "y": 30}),
    ("A6: black wall right (45,30)",     {"x": 45, "y": 30}),
    ("A6: pink background (1,30)",       {"x":  1, "y": 30}),
]
for label, kwargs in a6_targets:
    _, _, changed = probe(label, setup_l5, GameAction.ACTION6, kwargs=kwargs)
    if changed:
        print(f"  *** TOGGLE DETECTED — re-probing all actions from this state ***")

# ── Step size and multi-step movement ────────────────────────────────────────
print("\n\n=== STEP SIZE AND MULTI-STEP MOVEMENT ===")
env_s, obs_s = setup_l5()
g_s = np.array(obs_s.frame[-1])
lp_s, rp_s = block_pos(g_s)
print(f"Start: L={lp_s}, R={rp_s}")
for i in range(1, 14):
    g_before = np.array(obs_s.frame[-1])
    obs_s = env_s.step(GameAction.ACTION1)  # UP
    g_after = np.array(obs_s.frame[-1])
    n, _, trans = grid_diff(g_before, g_after)
    lp_s, rp_s = block_pos(g_after)
    blocked = "BLOCKED" if n == 0 else ""
    special = ""
    for k in trans:
        if any(c in k for c in ['G(14)', 'O(12)', 'V(15)']):
            special = f" *** COLOR INVOLVED: {k} x{trans[k]} ***"
    print(f"  UP {i}: L={lp_s}, R={rp_s}  cells={n}  {blocked}{special}")
    if n == 0:
        break

print()
env_s2, obs_s2 = setup_l5()
lp_s2, rp_s2 = block_pos(np.array(obs_s2.frame[-1]))
print(f"Start: L={lp_s2}, R={rp_s2}")
for i in range(1, 8):
    g_before = np.array(obs_s2.frame[-1])
    obs_s2 = env_s2.step(GameAction.ACTION4)  # CONVERGE
    g_after = np.array(obs_s2.frame[-1])
    n, _, trans = grid_diff(g_before, g_after)
    lp_s2, rp_s2 = block_pos(g_after)
    blocked = "BLOCKED" if n == 0 else ""
    special = ""
    for k in trans:
        if any(c in k for c in ['G(14)', 'O(12)', 'V(15)']):
            special = f" *** COLOR INVOLVED: {k} x{trans[k]} ***"
    print(f"  CONVERGE {i}: L={lp_s2}, R={rp_s2}  cells={n}  {blocked}{special}")
    if n == 0:
        break

# ── Navigate to colored objects and probe from there ─────────────────────────
print("\n\n=== PROBES ADJACENT TO COLORED OBJECTS ===")

# Left shaft: orange at rows 38-41 cols 10-21.
# Block at (50,6). Navigate up to approach orange from below.
# Find position adjacent to orange
print("\n--- Navigate block near orange (left, rows 38-41 cols 10-21) ---")
env_o, obs_o = setup_l5()
g_o = np.array(obs_o.frame[-1])
lp_o, rp_o = block_pos(g_o)
print(f"Start: L={lp_o}")
# Move UP and CONVERGE to reach orange
# Step size TBD from above. Navigate to just below orange.
# Orange bottom edge = row 41. Block bottom edge row 53.
# Try CONVERGE to get to col 10, then UP toward orange.
for step_seq in ['C', 'UUU', 'UUUU', 'UUUUU']:
    for a in step_seq:
        obs_o = env_o.step(AMAP[a])
    g_o = np.array(obs_o.frame[-1])
    lp_o2, rp_o2 = block_pos(g_o)
    print(f"  After '{step_seq}': L={lp_o2}, R={rp_o2}")

# Full render of left shaft after navigating up
env_r, obs_r = setup_l5()
for a in 'UUUUUU':
    obs_r = env_r.step(AMAP[a])
g_r = np.array(obs_r.frame[-1])
lp_r, rp_r = block_pos(g_r)
print(f"\nAfter 6 UPs: L={lp_r}, R={rp_r}")
render_zone(g_r, 0, 57, 2, 29, "Left shaft after 6 UPs:")
render_zone(g_r, 0, 57, 34, 61, "Right shaft after 6 UPs:")

# ── ACTION5 probes from several positions ────────────────────────────────────
print("\n\n=== ACTION5 FROM VARIOUS POSITIONS ===")
for nav in ['', 'U', 'UU', 'UUU', 'C', 'CC', 'UC']:
    probe(f"ACTION5 after '{nav}'", setup_l5, GameAction.ACTION5, nav=nav if nav else None)

print("\nDone.")
