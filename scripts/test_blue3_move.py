"""Move Blue-3 RIGHT once (my proposed move), then BFS to check if right block can reach Blue-1."""
import numpy as np
from collections import deque
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

def find_blocks(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if not len(cells): return None, None
    left  = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    if not len(left) or not len(right): return None, None
    return (int(left[:,0].min()), int(left[:,1].min())), (int(right[:,0].min()), int(right[:,1].min()))

# ── Step 1: Move Blue-3 RIGHT once (my proposed move) ──────────────────────
env, obs = make_l3()
grid0 = np.array(obs.frame[-1])
blue3 = [(r,c) for r,c in np.argwhere(grid0==9) if r>=30]
b3r, b3c = min(r for r,c in blue3), min(c for r,c in blue3)
print(f"Blue-3 initial position: rows {b3r}-{b3r+1}, cols {b3c}-{b3c+1}")

# Freeze Blue-3
obs = env.step(GameAction.ACTION6, {"x": int(b3c), "y": int(b3r)})
grid_f = np.array(obs.frame[-1])
yellow = np.argwhere(grid_f == 11)
if len(yellow):
    yr, yc = int(yellow[:,0].min()), int(yellow[:,1].min())
    print(f"Frozen: Yellow at rows {yr}-{yr+1}, cols {yc}-{yc+1}")

# Move RIGHT once (ACTION3 = DIVERGE = right for horizontal marker)
obs = env.step(GameAction.ACTION3)
grid_m = np.array(obs.frame[-1])
yellow2 = np.argwhere(grid_m == 11)
if len(yellow2):
    yr2, yc2 = int(yellow2[:,0].min()), int(yellow2[:,1].min())
    print(f"After RIGHT: Yellow at rows {yr2}-{yr2+1}, cols {yc2}-{yc2+1}")

# Restore: click a black wall cell (use row=46, col=14 which is accessible #)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
grid_r = np.array(obs.frame[-1])
blue3_new = [(r,c) for r,c in np.argwhere(grid_r==9) if r>=30]
if blue3_new:
    b3r2, b3c2 = min(r for r,c in blue3_new), min(c for r,c in blue3_new)
    print(f"Blue-3 after move: rows {b3r2}-{b3r2+1}, cols {b3c2}-{b3c2+1}")
else:
    print("ERROR: Blue-3 not found after restore")

# Blue-1 position
blue1 = [(r,c) for r,c in np.argwhere(grid_r==9) if r<20]
if blue1:
    b1r, b1c = min(r for r,c in blue1), min(c for r,c in blue1)
    print(f"Blue-1 position: rows {b1r}-{b1r+1}, cols {b1c}-{b1c+1}")

# ── Step 2: BFS — find all reachable right-block positions ──────────────────
print("\n─── BFS: all reachable states after Blue-3 moved ───")

# Save the state by capturing current env — need to replay from scratch
# We'll simulate Blue-3 move inline in make_and_move_blue3()
def make_and_move_blue3():
    env2, obs2 = make_l3()
    g = np.array(obs2.frame[-1])
    blue3_cells = [(r,c) for r,c in np.argwhere(g==9) if r>=30]
    r3, c3 = min(r for r,c in blue3_cells), min(c for r,c in blue3_cells)
    obs2 = env2.step(GameAction.ACTION6, {"x": int(c3), "y": int(r3)})  # freeze
    obs2 = env2.step(GameAction.ACTION3)                                  # RIGHT once
    obs2 = env2.step(GameAction.ACTION6, {"x": 14, "y": 46})             # restore
    return env2, obs2

def get_state4(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if not len(cells): return None
    left  = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:,0].min()), int(left[:,1].min()),
            int(right[:,0].min()), int(right[:,1].min()))

def replay_from_b3moved(path):
    env2, obs2 = make_and_move_blue3()
    for a in path:
        obs2 = env2.step(AMAP[a])
    return env2, obs2

_, obs_start = make_and_move_blue3()
init = get_state4(obs_start)
print(f"Start state: left=({init[0]},{init[1]}) right=({init[2]},{init[3]})")

queue = deque([(init, [])])
visited = {init}
right_cols_reached = set()
central_passage_states = []  # states where right block is at rows 14-17

n = 0
while queue:
    state, path = queue.popleft()
    n += 1
    lr, lc, rr, rc = state
    right_cols_reached.add((rr, rc))

    # Track if right block reaches central passage rows 14-17
    if 14 <= rr <= 17:
        central_passage_states.append(state)

    if n > 5000:
        print(f"  BFS limit reached at {n} states")
        break

    for name in ['U', 'D', 'X', 'C']:
        e2, o2 = replay_from_b3moved(path)
        o3 = e2.step(AMAP[name])
        if o3.levels_completed > 2:
            print(f"  WIN found! path={''.join(path+[name])}")
            break
        ns = get_state4(o3)
        if ns and ns not in visited:
            visited.add(ns)
            queue.append((ns, path + [name]))

print(f"BFS explored {n} states, {len(visited)} unique")
print(f"\nRight block rows reached: {sorted(set(r for r,c in right_cols_reached))}")
print(f"Right block min row reached: {min(r for r,c in right_cols_reached)}")

if central_passage_states:
    print(f"\nRight block reached central passage (rows 14-17) in {len(central_passage_states)} states:")
    for s in sorted(central_passage_states)[:10]:
        print(f"  L({s[0]},{s[1]}) R({s[2]},{s[3]})")
    # Check if Blue-1 position (rows 15-16, cols 31-32) is reachable
    b1_reachable = any(14 <= s[2] <= 17 and 31 <= s[3] <= 32 for s in central_passage_states)
    print(f"\nRight block can reach Blue-1 position (rows 14-17, cols 31-32): {b1_reachable}")
else:
    print("\nRight block CANNOT reach central passage (rows 14-17)")
    print("→ Blue-1 is NOT on the right block's path with this Blue-3 move")
