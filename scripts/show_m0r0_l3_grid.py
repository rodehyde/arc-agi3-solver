"""Show grid at key stages: initial, at row=26 freeze, marker moved, restored."""
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

def render(obs, label, r0=10, r1=55):
    grid = np.array(obs.frame[-1])
    s = get_state(obs)
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"  state={s}  levels={obs.levels_completed}")
    vals = {}
    for v in np.unique(grid):
        if v not in (5, 8, 15):  # skip black, red, purple (most common)
            vals[int(v)] = int(np.sum(grid == v))
    if vals:
        names = {0:'white',1:'lt-grey',2:'md-grey',9:'blue',10:'lt-blue',11:'yellow',14:'green'}
        print("  special cells: " + ", ".join(f"{names.get(k,k)}={v}" for k,v in sorted(vals.items())))
    print(f"{'='*70}")
    print("     " + "".join(f"{c%10}" for c in range(64)))
    print("     " + "".join(f"{c//10}" for c in range(64)))
    for r in range(r0, r1+1):
        row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
        print(f"{r:3d}  {row_str}")

# ── Find path to row=26 ──────────────────────────────────────────────────────
print("Finding path to row=26...")
env0, obs0 = make_l3()
init = get_state(obs0)
queue = deque([(init, [])])
visited = {init}
path_to_26 = None

while queue:
    state, path = queue.popleft()
    if state[0] == 26:
        path_to_26 = path
        break
    for name in ['U', 'D', 'X', 'C']:
        env, obs = replay_to(path)
        obs2 = env.step(AMAP[name])
        ns = get_state(obs2)
        if ns and ns not in visited:
            visited.add(ns)
            queue.append((ns, path + [name]))

if not path_to_26:
    print("Cannot reach row=26"); exit(1)

env26, obs26 = replay_to(path_to_26)
print(f"Path to row=26: {''.join(path_to_26)}")

# ── Stage 1: Initial Level 3 state ──────────────────────────────────────────
env_init, obs_init = make_l3()
render(obs_init, "STAGE 1 — Initial Level 3 state")

# ── Stage 2: At row=26 (before freeze) ──────────────────────────────────────
render(obs26, "STAGE 2 — Blocks at row=26")

# ── Stage 3: Freeze blocks at row=26, click blue-2 ──────────────────────────
env26b, obs26b = replay_to(path_to_26)
obs_frozen = env26b.step(GameAction.ACTION6, {"x": 11, "y": 19})
render(obs_frozen, "STAGE 3 — Blocks frozen at row=26, blue-2 clicked (yellow at rows 19-20)")

# ── Stage 4: Move yellow DOWN (should go to rows 23-24) ─────────────────────
obs_down1 = env26b.step(GameAction.ACTION2)
render(obs_down1, "STAGE 4 — After ACTION2 DOWN (yellow should move to rows 23-24)")

# ── Stage 5: Restore blocks ──────────────────────────────────────────────────
# Click on a black wall cell (not background) to restore
obs_restored = env26b.step(GameAction.ACTION6, {"x": 14, "y": 26})
render(obs_restored, "STAGE 5 — After restore (click black wall at col=14, row=26)")

# ── Stage 6: Try ACTION1 (UP) from row=26 — should reach row=22 ─────────────
obs_up1 = env26b.step(GameAction.ACTION1)
render(obs_up1, "STAGE 6 — After ACTION1 UP (row=26 -> should reach row=22)")

# ── Stage 7: Continue UP to row=18 ──────────────────────────────────────────
obs_up2 = env26b.step(GameAction.ACTION1)
render(obs_up2, "STAGE 7 — After another ACTION1 UP (should reach row=18, past blue-2)")
