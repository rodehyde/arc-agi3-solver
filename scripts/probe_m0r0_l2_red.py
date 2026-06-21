"""m0r0 Level 2 — probe block interaction with red cells.

Navigate blocks to rows 34-37 (just above the red zone), then test
entering rows 38-41 and probe all actions from within the red zone.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
colours = {0:'.', 5:'#', 6:'P', 8:'R', 10:'L', 12:'O', 15:'V'}

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
        f"{colours.get(a,str(a))}->{colours.get(b,str(b))}:{n}"
        for (a, b), n in sorted(transitions.items())
    )
    return f"{len(changed)} cells, bbox rows {r0}-{r1} cols {c0}-{c1}, transitions: {t_str}"

def navigate(env, obs, actions_str):
    for a in actions_str:
        obs = env.step(AMAP[a])
    return obs

# Path to rows 34-37 at left=10, right=50:
# X×3 (diverge to left=10, right=50), then D×6 (down to rows 34-37)
NAV_PATH = 'XXXDDDDDD'

print("=== Navigate to just above red zone ===")
env, obs = make_l2()
print(f"Start: {block_state(get_grid(obs))}")
obs = navigate(env, obs, NAV_PATH)
print(f"After {NAV_PATH}: {block_state(get_grid(obs))}  levels={obs.levels_completed}")

print()
print("=== Test entering red zone (ACTION2 = DOWN into rows 38-41) ===")
env, obs = make_l2()
obs = navigate(env, obs, NAV_PATH)
g_before = get_grid(obs)
obs_after = env.step(GameAction.ACTION2)
g_after = get_grid(obs_after)
result = diff_grids(g_before, g_after)
print(f"ACTION2 (down into red): {result}")
print(f"  New state: {block_state(g_after)}  levels={obs_after.levels_completed}")

# Check what colours are now under/around blocks
cells = np.argwhere(g_after == 10)
if len(cells):
    print(f"  Block cells: rows {cells[:,0].min()}-{cells[:,0].max()} cols {cells[:,1].min()}-{cells[:,1].max()}")

print()
print("=== Probe all actions FROM WITHIN red zone (rows 38-41) ===")
BASE_PATH = NAV_PATH + 'D'  # navigate to rows 38-41

for name, action in [('ACTION1(up)', GameAction.ACTION1),
                     ('ACTION2(dn)', GameAction.ACTION2),
                     ('ACTION3(div)', GameAction.ACTION3),
                     ('ACTION4(con)', GameAction.ACTION4)]:
    env, obs = make_l2()
    obs = navigate(env, obs, BASE_PATH)
    g_before = get_grid(obs)
    obs_after = env.step(action)
    g_after = get_grid(obs_after)
    result = diff_grids(g_before, g_after)
    lvl = f" | LEVEL COMPLETE" if obs_after.levels_completed > 1 else ""
    print(f"  {name}: {result}{lvl}")
    if result != "NO CHANGE":
        print(f"    → {block_state(g_after)}")

print()
print("=== Also probe from rows 26-37 (left-only red zone) ===")
# Navigate to rows 26-29 at left=10 (left side has red, right doesn't)
NAV_26 = 'XXXDDDDD'  # X×3 + D×5
env, obs = make_l2()
obs = navigate(env, obs, NAV_26)
print(f"After {NAV_26}: {block_state(get_grid(obs))}")

for name, action in [('ACTION2(dn)', GameAction.ACTION2),
                     ('ACTION3(div)', GameAction.ACTION3),
                     ('ACTION4(con)', GameAction.ACTION4)]:
    env, obs = make_l2()
    obs = navigate(env, obs, NAV_26)
    g_before = get_grid(obs)
    obs_after = env.step(action)
    g_after = get_grid(obs_after)
    result = diff_grids(g_before, g_after)
    lvl = f" | LEVEL COMPLETE" if obs_after.levels_completed > 1 else ""
    print(f"  {name}: {result}{lvl}")
    if result != "NO CHANGE":
        print(f"    → {block_state(g_after)}")
