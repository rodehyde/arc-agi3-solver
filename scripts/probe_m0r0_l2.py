"""m0r0 Level 2 — Step 2: probe all actions, produce full action table."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
colours = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
           8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

def make_l2():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1:
        obs = env.step(AMAP[a])
    return env, obs

def get_grid(obs):
    return np.array(obs.frame[-1])

def block_state(grid):
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return "NO BLOCKS"
    rows, cols = cells[:, 0], cells[:, 1]
    return f"rows {rows.min()}-{rows.max()} left_col={cols.min()} right_col={cols.max()-3}"

def diff_grids(before, after):
    changed = np.argwhere(before != after)
    if len(changed) == 0:
        return "NO CHANGE"
    r0, c0 = changed.min(axis=0)
    r1, c1 = changed.max(axis=0)
    transitions = {}
    for r, c in changed:
        key = (int(before[r, c]), int(after[r, c]))
        transitions[key] = transitions.get(key, 0) + 1
    t_str = ", ".join(
        f"{colours.get(a,'?')}{a}->{colours.get(b,'?')}{b}:{n}"
        for (a, b), n in sorted(transitions.items())
    )
    return f"{len(changed)} cells, bbox rows {r0}-{r1} cols {c0}-{c1}, transitions: {t_str}"

print("=== m0r0 Level 2 — Action Table ===\n")
env0, obs0 = make_l2()
g0 = get_grid(obs0)
print(f"Start: {block_state(g0)}  aa={obs0.available_actions}\n")

# ACTION1–ACTION5
for name, action in [('ACTION1', GameAction.ACTION1), ('ACTION2', GameAction.ACTION2),
                     ('ACTION3', GameAction.ACTION3), ('ACTION4', GameAction.ACTION4),
                     ('ACTION5', GameAction.ACTION5)]:
    env, obs_before = make_l2()
    g_before = get_grid(obs_before)
    aa_before = obs_before.available_actions
    obs_after = env.step(action)
    g_after = get_grid(obs_after)
    aa_after = obs_after.available_actions
    result = diff_grids(g_before, g_after)
    aa_note = f" | aa: {aa_before}->{aa_after}" if aa_before != aa_after else ""
    lvl = f" | LEVEL COMPLETE" if obs_after.levels_completed > 1 else ""
    print(f"{name}: {result}{aa_note}{lvl}")
    if result != "NO CHANGE":
        print(f"  → new state: {block_state(g_after)}")

# ACTION6 — click on distinct targets
print()
print("ACTION6 (click) — distinct targets:")
# Left block at rows 10-13, cols 22-25
# Right block at rows 10-13, cols 38-41
# Red cells in rows 26-37 (left), rows 38-41 (both), rows 54-57 (full)
# Black passage cols 18-21, rows 22-25
test_points = [
    (22, 10, "left block centre"),
    (38, 10, "right block centre"),
    (10, 22, "black outer ring (left)"),
    (10, 46, "black outer ring (right)"),
    (19, 22, "left interior passage"),
    (26, 26, "red cell (left, row 26)"),
    (26, 46, "black (right, row 26, no red)"),
    (39, 26, "red cell (left, row 38-41)"),
    (39, 46, "red cell (right, row 38-41)"),
    (54, 26, "red cell (full-width band)"),
    (16, 32, "central corridor"),
    (50, 32, "unified black chamber"),
]
for x, y, label in test_points:
    env, obs_before = make_l2()
    g_before = get_grid(obs_before)
    obs_after = env.step(GameAction.ACTION6, {"x": x, "y": y})
    g_after = get_grid(obs_after)
    result = diff_grids(g_before, g_after)
    lvl = f" | LEVEL COMPLETE" if obs_after.levels_completed > 1 else ""
    print(f"  ({x:2d},{y:2d}) {label}: {result}{lvl}")
