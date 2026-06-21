"""Targeted probe: navigate to row=22, move blue-2 out of corridor, see if blocks can reach row=18."""
from collections import deque
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
        8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs

def get_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if not len(cells): return None
    rows, cols = cells[:, 0], cells[:, 1]
    return (int(rows.min()), int(cols.min()), int(cols.max()) - 3)

def replay_to(path):
    env, obs = make_l3()
    for a in path:
        obs = env.step(AMAP[a])
    return env, obs

def render_rows(grid, r0, r1):
    print("     " + "".join(f"{c%10}" for c in range(64)))
    for r in range(r0, r1+1):
        row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
        print(f"{r:3d}  {row_str}")

# ── Step 1: BFS to find path to first state at row=22 ───────────────────────
print("Finding path to row=22...")
env0, obs0 = make_l3()
init = get_state(obs0)
queue = deque([(init, [])])
visited = {init}
path_to_22 = None

while queue:
    state, path = queue.popleft()
    if state[0] == 22:
        path_to_22 = path
        break
    for name in ['U', 'D', 'X', 'C']:
        env, obs = replay_to(path)
        obs2 = env.step(AMAP[name])
        ns = get_state(obs2)
        if ns and ns not in visited:
            visited.add(ns)
            queue.append((ns, path + [name]))

if not path_to_22:
    print("ERROR: could not reach row=22")
    exit(1)

env, obs = replay_to(path_to_22)
s = get_state(obs)
print(f"At row=22: state={s}  path={''.join(path_to_22)}")

# ── Step 2: Try ACTION1 from here (baseline — should be blocked) ─────────────
env_test, obs_test = replay_to(path_to_22)
obs_up = env_test.step(GameAction.ACTION1)
s_up = get_state(obs_up)
print(f"\nACTION1 (UP) without moving marker: {s} -> {s_up}")
print(f"  (blocked = {s_up == s})")

# ── Step 3: Click blue-2, check frozen state, render ─────────────────────────
print("\nClicking blue-2 (11, 19) to freeze blocks and make marker yellow...")
env2, obs2 = replay_to(path_to_22)
obs_frozen = env2.step(GameAction.ACTION6, {"x": 11, "y": 19})
grid_frozen = np.array(obs_frozen.frame[-1])
yellow = np.argwhere(grid_frozen == 11)
grey  = np.argwhere(grid_frozen == 10)  # should be 0
grey2 = np.argwhere(grid_frozen == 1)   # lt-grey = frozen blocks
if len(yellow):
    yr, yc = yellow[:,0], yellow[:,1]
    print(f"  Yellow marker: rows {yr.min()}-{yr.max()}, cols {yc.min()}-{yc.max()}")
if len(grey2):
    gr, gc = grey2[:,0], grey2[:,1]
    print(f"  Frozen blocks (lt-grey): rows {gr.min()}-{gr.max()}, cols {gc.min()}-{gc.max()}")
print(f"  available_actions={obs_frozen.available_actions}")

print("\nGrid around marker area (rows 10-28):")
render_rows(grid_frozen, 10, 28)

# ── Step 4: Move yellow DOWN once (ACTION2) and check new position ────────────
print("\n--- Moving yellow DOWN (ACTION2) once ---")
obs_moved1 = env2.step(GameAction.ACTION2)
grid_m1 = np.array(obs_moved1.frame[-1])
yellow1 = np.argwhere(grid_m1 == 11)
if len(yellow1):
    yr, yc = yellow1[:,0], yellow1[:,1]
    print(f"  Yellow after 1x DOWN: rows {yr.min()}-{yr.max()}, cols {yc.min()}-{yc.max()}")
print("\nGrid rows 10-28 after 1x DOWN:")
render_rows(grid_m1, 10, 28)

# ── Step 5: Move yellow DOWN again ───────────────────────────────────────────
print("\n--- Moving yellow DOWN (ACTION2) again ---")
obs_moved2 = env2.step(GameAction.ACTION2)
grid_m2 = np.array(obs_moved2.frame[-1])
yellow2 = np.argwhere(grid_m2 == 11)
if len(yellow2):
    yr, yc = yellow2[:,0], yellow2[:,1]
    print(f"  Yellow after 2x DOWN: rows {yr.min()}-{yr.max()}, cols {yc.min()}-{yc.max()}")

# Also try moving UP instead (from fresh frozen state)
print("\n--- Moving yellow UP (ACTION1) once (from fresh freeze) ---")
env3, obs3 = replay_to(path_to_22)
env3.step(GameAction.ACTION6, {"x": 11, "y": 19})  # freeze
obs_up1 = env3.step(GameAction.ACTION1)
grid_up1 = np.array(obs_up1.frame[-1])
yellow_up = np.argwhere(grid_up1 == 11)
if len(yellow_up):
    yr, yc = yellow_up[:,0], yellow_up[:,1]
    print(f"  Yellow after 1x UP: rows {yr.min()}-{yr.max()}, cols {yc.min()}-{yc.max()}")

# ── Step 6: Restore blocks after moving DOWN once, then try UP ───────────────
print("\n--- Restoring blocks after 1x DOWN, then trying ACTION1 (UP) ---")
env4, obs4 = replay_to(path_to_22)
env4.step(GameAction.ACTION6, {"x": 11, "y": 19})   # freeze
env4.step(GameAction.ACTION2)                         # move yellow DOWN once
obs_restore = env4.step(GameAction.ACTION6, {"x": 11, "y": 46})  # restore (click block area)
grid_r = np.array(obs_restore.frame[-1])

# Check where blue-2 is now
blue_cells = np.argwhere(grid_r == 9)
lt_blue = np.argwhere(grid_r == 10)
if len(blue_cells):
    br, bc = blue_cells[:,0], blue_cells[:,1]
    print(f"  Blue cells after restore: rows {br.min()}-{br.max()}, cols {bc.min()}-{bc.max()}")
if len(lt_blue):
    lr, lc = lt_blue[:,0], lt_blue[:,1]
    print(f"  Blocks after restore: rows {lr.min()}-{lr.max()}, cols {lc.min()}-{lc.max()}")

s_restored = get_state(obs_restore)
print(f"  Block state: {s_restored}")

# Now try ACTION1 (UP)
obs_up2 = env4.step(GameAction.ACTION1)
s_after_up = get_state(obs_up2)
print(f"\n  ACTION1 after restore: {s_restored} -> {s_after_up}")
if s_after_up and s_after_up[0] < s_restored[0]:
    print("  *** BLOCKS MOVED UP! Blue-2 was an obstacle. ***")
else:
    print("  (still blocked)")

print("\nGrid rows 10-28 after restore:")
render_rows(grid_r, 10, 28)
