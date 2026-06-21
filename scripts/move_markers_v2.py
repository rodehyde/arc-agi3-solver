"""Corrected marker moves. Blue-1 goes LEFT×2 then UP×1 to cul-de-sac at rows 19-20, cols 43-44."""
import numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
char = {0:'.', 1:'a', 5:'#', 8:'R', 9:'B', 10:'L', 11:'Y', 15:'V'}

def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs

def yellow_pos(obs):
    g = np.array(obs.frame[-1])
    y = np.argwhere(g == 11)
    if not len(y): return None
    return (int(y[:,0].min()), int(y[:,1].min()))

env, obs = make_l3()
g = np.array(obs.frame[-1])

# ── BLUE-1: RIGHT×1, UP×1, RIGHT×4, DOWN×3, LEFT×2, UP×1 ──────────────────
print("BLUE-1 sequence:")
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})  # freeze at (15,31)
print(f"  frozen: {yellow_pos(obs)}")
for label, act in [
    ("RIGHT", GameAction.ACTION4),
    ("UP",    GameAction.ACTION1),
    ("RIGHT", GameAction.ACTION4), ("RIGHT", GameAction.ACTION4),
    ("RIGHT", GameAction.ACTION4), ("RIGHT", GameAction.ACTION4),
    ("DOWN",  GameAction.ACTION2), ("DOWN",  GameAction.ACTION2),
    ("DOWN",  GameAction.ACTION2),
    ("LEFT",  GameAction.ACTION3), ("LEFT",  GameAction.ACTION3),
    ("UP",    GameAction.ACTION1),
]:
    obs = env.step(act)
    print(f"  {label}: {yellow_pos(obs)}")
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
g = np.array(obs.frame[-1])
b1_cells = np.argwhere(g == 9)
b1_in_range = b1_cells[(b1_cells[:,0] >= 18) & (b1_cells[:,0] <= 22)]
print(f"  Blue-1 restored. Cells at rows 18-22: {sorted((int(r),int(c)) for r,c in b1_in_range)}")

# ── BLUE-2: UP, RIGHT, UP ──────────────────────────────────────────────────
print("\nBLUE-2 sequence:")
g = np.array(obs.frame[-1])
bxy2 = next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9), None)
print(f"  found at {bxy2}")
obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
for label, act in [("UP", GameAction.ACTION1), ("RIGHT", GameAction.ACTION4),
                   ("UP", GameAction.ACTION1)]:
    obs = env.step(act)
    print(f"  {label}: {yellow_pos(obs)}")
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
g = np.array(obs.frame[-1])
b2 = np.argwhere(g == 9)
b2_top = b2[b2[:,0] <= 14]
print(f"  Blue-2 restored at rows 10-14: {sorted((int(r),int(c)) for r,c in b2_top)}")

# ── BLUE-3: RIGHT×3 ────────────────────────────────────────────────────────
print("\nBLUE-3 sequence:")
g = np.array(obs.frame[-1])
bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
print(f"  found at {bxy3}")
obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
for i in range(3):
    obs = env.step(GameAction.ACTION4)
    print(f"  RIGHT {i+1}: {yellow_pos(obs)}")
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
g = np.array(obs.frame[-1])
b3 = np.argwhere(g == 9)
b3_area = b3[(b3[:,0] >= 29) & (b3[:,0] <= 34)]
print(f"  Blue-3 restored: {sorted((int(r),int(c)) for r,c in b3_area)}")

# ── GRID RENDER (central + divider area) ───────────────────────────────────
print("\n=== Grid rows 10-25 (cols 35-55) ===")
print("     " + "".join(f"{c%10}" for c in range(35,56)))
for r in range(10, 26):
    row_str = "".join(char.get(int(g[r,c]),'?') for c in range(35,56))
    print(f"{r:3d}  {row_str}")

# Central passage check
blue_in_passage = [(r,c) for r in range(14,18) for c in range(26,38) if g[r,c]==9]
print(f"\nBlue markers in central passage (rows 14-17, cols 26-37): {blue_in_passage}")
print(f"Central passage clear: {len(blue_in_passage)==0}")

# ── QUICK BFS ──────────────────────────────────────────────────────────────
print("\n=== BFS from post-marker state ===")
def get_state(obs):
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    if not len(cells): return None
    left  = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:,0].min()), int(left[:,1].min()),
            int(right[:,0].min()), int(right[:,1].min()))

def setup():
    env2, obs2 = make_l3()
    g2 = np.array(obs2.frame[-1])
    # Blue-1
    obs2 = env2.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3,
                GameAction.ACTION1]:
        obs2 = env2.step(act)
    obs2 = env2.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-2
    g2 = np.array(obs2.frame[-1])
    bxy = next(((c,r) for r in range(18,23) for c in range(10,15) if g2[r,c]==9), None)
    obs2 = env2.step(GameAction.ACTION6, {"x": bxy[0], "y": bxy[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs2 = env2.step(act)
    obs2 = env2.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-3
    g2 = np.array(obs2.frame[-1])
    bxy = next(((c,r) for r in range(30,35) for c in range(38,43) if g2[r,c]==9), None)
    obs2 = env2.step(GameAction.ACTION6, {"x": bxy[0], "y": bxy[1]})
    for _ in range(3): obs2 = env2.step(GameAction.ACTION4)
    obs2 = env2.step(GameAction.ACTION6, {"x": 14, "y": 46})
    return env2, obs2

def replay(path):
    e, o = setup()
    for a in path: o = e.step(AMAP[a])
    return e, o

_, obs_start = setup()
init = get_state(obs_start)
print(f"Start: L({init[0]},{init[1]}) R({init[2]},{init[3]})")

queue = deque([(init, "")])
visited = {init}
win_found = False
central_right = set()
n = 0

while queue and n < 2000:
    state, path = queue.popleft()
    n += 1
    lr, lc, rr, rc = state
    if rr <= 17: central_right.add((rr, rc))

    for name in ['U','D','X','C']:
        e2, o2 = replay(path)
        o3 = e2.step(AMAP[name])
        if o3.levels_completed > 2:
            print(f"\n*** WIN! path={path+name} ({len(path+name)} actions) ***")
            win_found = True
            break
        ns = get_state(o3)
        if ns and ns not in visited:
            visited.add(ns)
            queue.append((ns, path+name))
    if win_found: break

print(f"BFS: {n} states, {len(visited)} unique")
if central_right:
    print(f"Right block in rows ≤17: cols reached = {sorted(set(c for r,c in central_right))}")
    print(f"Right block rows in central area: {sorted(set(r for r,c in central_right))}")
if not win_found:
    all_lc = sorted(set(lc for lr,lc,rr,rc in visited if 14<=lr<=17))
    all_rc = sorted(set(rc for lr,lc,rr,rc in visited if 14<=rr<=17))
    print(f"Left block cols in central passage: {all_lc}")
    print(f"Right block cols in central passage: {all_rc}")
