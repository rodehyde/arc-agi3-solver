"""Step 2: Action probe for m0r0 Level 4.
Full grid diff for every action. Auto second-pass on any toggle.
ACTION6 tested on every distinct object.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
char = {0: '.', 1: 'a', 5: '#', 8: 'R', 9: 'B', 10: 'L', 11: 'Y', 12: 'O', 15: 'V'}

def setup_l4():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    # L3 marker moves
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3):
        obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # L3 navigation
    for a in NAV3:
        obs = env.step(AMAP[a])
    return env, obs

def grid_diff(g_before, g_after):
    diff = np.where(g_before != g_after)
    if not len(diff[0]):
        return 0, None, []
    rows, cols = diff
    bbox = (int(rows.min()), int(cols.min()), int(rows.max()), int(cols.max()))
    transitions = {}
    for r, c in zip(rows, cols):
        key = f"{int(g_before[r,c])}->{int(g_after[r,c])}"
        transitions[key] = transitions.get(key, 0) + 1
    return len(rows), bbox, transitions

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    lp = (int(left[:, 0].min()), int(left[:, 1].min())) if len(left) else None
    rp = (int(right[:, 0].min()), int(right[:, 1].min())) if len(right) else None
    return lp, rp

def render_zone(g, r0, r1, c0, c1):
    print(f"     " + "".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r, c]), '?') for c in range(c0, c1+1))
        print(f"{r:3d}  {row}")

def probe_action(env_fn, label, action, kwargs=None):
    env, obs = env_fn()
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
    win = obs2.levels_completed > 3

    print(f"\n{'='*60}")
    print(f"ACTION: {label}")
    print(f"  Cells changed: {n}  bbox: {bbox}")
    print(f"  Transitions: {trans}")
    print(f"  Left:  {lp0} -> {lp1}  (delta rows={lp1[0]-lp0[0] if lp0 and lp1 else '?'}, cols={lp1[1]-lp0[1] if lp0 and lp1 else '?'})")
    print(f"  Right: {rp0} -> {rp1}  (delta rows={rp1[0]-rp0[0] if rp0 and rp1 else '?'}, cols={rp1[1]-rp0[1] if rp0 and rp1 else '?'})")
    print(f"  available_actions changed: {avail_changed}  {avail_before if avail_changed else ''}")
    print(f"  WIN: {win}")
    return obs2, g_after, avail_changed

print("Setting up L4...")
env0, obs0 = setup_l4()
g0 = np.array(obs0.frame[-1])
lp, rp = block_pos(g0)
print(f"L4 start: Left={lp}, Right={rp}")
print(f"Available actions: {obs0.available_actions}")
print(f"Blue marker: {sorted((int(r),int(c)) for r,c in np.argwhere(g0==9))}")

print("\n=== Rendering start state (rows 22-40, cols 7-55) ===")
render_zone(g0, 22, 40, 7, 55)

# Probe all basic actions
print("\n\n=== STEP 2: ACTION TABLE ===")

for label, act in [
    ("ACTION1 (UP)", GameAction.ACTION1),
    ("ACTION2 (DOWN)", GameAction.ACTION2),
    ("ACTION3 (DIVERGE)", GameAction.ACTION3),
    ("ACTION4 (CONVERGE)", GameAction.ACTION4),
    ("ACTION5", GameAction.ACTION5),
]:
    probe_action(setup_l4, label, act)

# ACTION6: test on each distinct object
print("\n\n=== ACTION6 CLICK TARGETS ===")
targets = [
    ("A6: blue marker centre (30,30)", GameAction.ACTION6, {"x": 30, "y": 30}),
    ("A6: blue marker corner (31,31)", GameAction.ACTION6, {"x": 31, "y": 31}),
    ("A6: left block centre (15,35)", GameAction.ACTION6, {"x": 15, "y": 35}),
    ("A6: right block centre (45,25)", GameAction.ACTION6, {"x": 45, "y": 25}),
    ("A6: corridor black (20,31)", GameAction.ACTION6, {"x": 20, "y": 31}),
    ("A6: corridor black (45,31)", GameAction.ACTION6, {"x": 45, "y": 31}),
    ("A6: checkerboard cell black (25,35)", GameAction.ACTION6, {"x": 25, "y": 35}),
    ("A6: yellow wall (5,5)", GameAction.ACTION6, {"x": 5, "y": 5}),
]
toggle_found = False
for label, act, kwargs in targets:
    obs2, g2, avail_changed = probe_action(setup_l4, label, act, kwargs)
    if avail_changed:
        toggle_found = True
        print(f"  *** TOGGLE DETECTED — probing all actions from this state ***")

# If ACTION6 on blue marker triggers freeze: probe all actions in frozen state
print("\n\n=== FROZEN STATE PROBE (after click on blue marker) ===")
env_f, obs_f = setup_l4()
g_f0 = np.array(obs_f.frame[-1])
obs_f = env_f.step(GameAction.ACTION6, {"x": 30, "y": 30})
g_f1 = np.array(obs_f.frame[-1])
n, bbox, trans = grid_diff(g_f0, g_f1)
print(f"After click on marker: {n} cells changed, transitions={trans}")
print(f"Yellow cells: {sorted((int(r),int(c)) for r,c in np.argwhere(g_f1==11) if 25<=r<=40)}")
print(f"Lt-grey cells: {sorted((int(r),int(c)) for r,c in np.argwhere(g_f1==1) if 20<=r<=45)}")

print("\nRendering frozen state (rows 22-40, cols 7-55):")
render_zone(g_f1, 22, 40, 7, 55)

if np.any(g_f1 == 11):  # yellow marker present = freeze happened
    print("\nFreeze confirmed! Probing movements of yellow marker:")
    y_pos_before = tuple(np.argwhere(g_f1 == 11)[0])
    for label, act in [
        ("UP (frozen)", GameAction.ACTION1),
        ("DOWN (frozen)", GameAction.ACTION2),
        ("DIVERGE (frozen)", GameAction.ACTION3),
        ("CONVERGE (frozen)", GameAction.ACTION4),
    ]:
        env_f2, obs_f2 = setup_l4()
        obs_f2 = env_f2.step(GameAction.ACTION6, {"x": 30, "y": 30})
        g_before_f = np.array(obs_f2.frame[-1])
        obs_f2 = env_f2.step(act)
        g_after_f = np.array(obs_f2.frame[-1])
        n, bbox, trans = grid_diff(g_before_f, g_after_f)
        y_after = np.argwhere(g_after_f == 11)
        y_pos_after = tuple(y_after[0]) if len(y_after) else None
        print(f"  {label}: {n} cells changed, yellow: {y_pos_before} -> {y_pos_after}, trans={trans}")

    # Test restore after moving marker
    print("\nTest restore (click black wall after moving marker):")
    # Move marker UP then restore
    env_f3, obs_f3 = setup_l4()
    obs_f3 = env_f3.step(GameAction.ACTION6, {"x": 30, "y": 30})  # freeze
    obs_f3 = env_f3.step(GameAction.ACTION1)  # move UP
    g_before_restore = np.array(obs_f3.frame[-1])
    y_pos = np.argwhere(g_before_restore == 11)
    print(f"  Yellow at: {sorted((int(r),int(c)) for r,c in y_pos)}")
    obs_f3 = env_f3.step(GameAction.ACTION6, {"x": 20, "y": 20})  # restore click (black cell)
    g_after_restore = np.array(obs_f3.frame[-1])
    n, bbox, trans = grid_diff(g_before_restore, g_after_restore)
    print(f"  After restore click (20,20): {n} cells changed, trans={trans}")
    print(f"  Blue marker: {sorted((int(r),int(c)) for r,c in np.argwhere(g_after_restore==9) if 20<=r<=40)}")
    print(f"  Lt-blue blocks: {sorted((int(r),int(c)) for r,c in np.argwhere(g_after_restore==10))}")
