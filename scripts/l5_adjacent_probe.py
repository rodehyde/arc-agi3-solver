"""Probe ACTION6 and all actions when block is adjacent to colored walls.
Also checks frame layers and right-block approach to center.
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
    for a in L1 + L2: obs = env.step(AMAP[a])
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
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]: obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    for a in NAV3: obs = env.step(AMAP[a])
    for a in 'UU': obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})
    for a in 'DDCDCC': obs = env.step(AMAP[a])
    return env, obs

def diff_full(g_before, g_after, label=""):
    diff = np.argwhere(g_before != g_after)
    if label: print(f"\n{label}")
    print(f"  cells changed: {len(diff)}")
    for r, c in diff:
        r, c = int(r), int(c)
        print(f"  [{r},{c}]: {char.get(int(g_before[r,c]),'?')}({g_before[r,c]}) -> {char.get(int(g_after[r,c]),'?')}({g_after[r,c]})")

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

# ── 1. Check how many frame layers L5 has ────────────────────────────────────
print("=== Frame layers in L5 ===")
env0, obs0 = setup_l5()
print(f"Number of frame layers: {len(obs0.frame)}")
for i, layer in enumerate(obs0.frame):
    g = np.array(layer)
    vals = sorted(set(int(v) for v in g.flatten()))
    unique_vals = {v: int(np.sum(g==v)) for v in vals}
    print(f"  Layer {i}: shape={g.shape}  values={unique_vals}")

# ── 2. Left block adjacent to orange (above) — probe A6 on orange ────────────
# Navigate: 2 UPs → L=(42,6), block bottom at row 45, orange top at row 38.
# Block is at rows 42-45, orange at rows 38-41. Adjacent from BELOW.
print("\n\n=== Left block adjacent to orange (above) ===")
env1, obs1 = setup_l5()
for a in 'UU': obs1 = env1.step(AMAP[a])
g_nav = np.array(obs1.frame[-1])
lp, rp = block_pos(g_nav)
print(f"After 2 UPs: L={lp}, R={rp}")
render_zone(g_nav, 36, 47, 2, 29, "Left shaft — block adjacent to orange:")

# Probe A6 on every cell of the orange (rows 38-41, cols 10-21)
print("\nProbing A6 on orange cells (block at rows 42-45):")
for test_x, test_y in [(15, 39), (10, 39), (21, 39), (15, 38), (15, 41)]:
    g_before = np.array(obs1.frame[-1])
    obs_test = env1.step(GameAction.ACTION6, {"x": test_x, "y": test_y})
    g_after = np.array(obs_test.frame[-1])
    diff = np.argwhere(g_before != g_after)
    non_border = [(int(r),int(c)) for r,c in diff if 1<=r<=62 and 1<=c<=62]
    print(f"  A6({test_x},{test_y}): cells={len(diff)}, interior_changes={non_border}")
    obs1 = obs_test  # keep state for chaining

# ── 3. Left block at col 10 (DIVERGE once) then A6 on purple ─────────────────
print("\n\n=== Left block adjacent to purple (left shaft, right side) ===")
env2, obs2 = setup_l5()
obs2 = env2.step(AMAP['X'])  # DIVERGE: L→(50,10)
g_nav2 = np.array(obs2.frame[-1])
lp2, rp2 = block_pos(g_nav2)
print(f"After DIVERGE: L={lp2}")
render_zone(g_nav2, 48, 55, 2, 22, "Block adjacent to purple:")
# A6 on purple at cols 14-17 rows 50-53
for test_x, test_y in [(14, 51), (17, 51), (15, 50), (15, 53)]:
    g_before = np.array(obs2.frame[-1])
    obs_test = env2.step(GameAction.ACTION6, {"x": test_x, "y": test_y})
    g_after = np.array(obs_test.frame[-1])
    diff = np.argwhere(g_before != g_after)
    non_border = [(int(r),int(c)) for r,c in diff if 1<=r<=62 and 1<=c<=62]
    print(f"  A6({test_x},{test_y}): cells={len(diff)}, interior={non_border}")
    obs2 = obs_test

# ── 4. Right block approach to center — how close can R get? ─────────────────
print("\n\n=== Right block navigates toward center ===")
env3, obs3 = setup_l5()
g3 = np.array(obs3.frame[-1])
lp3, rp3 = block_pos(g3)
print(f"Start: L={lp3}, R={rp3}")
# DIVERGE moves R LEFT (toward center)
for i in range(1, 10):
    g_before = np.array(obs3.frame[-1])
    obs3 = env3.step(GameAction.ACTION3)  # DIVERGE
    g_after = np.array(obs3.frame[-1])
    n = int(np.sum(g_before != g_after))
    lp3, rp3 = block_pos(g_after)
    blocked = "BLOCKED" if n == 0 else ""
    print(f"  DIVERGE {i}: L={lp3}, R={rp3}  cells={n}  {blocked}")
    if n == 0: break

# ── 5. Right block navigates UP then toward center ────────────────────────────
print("\n\n=== Right block UP then DIVERGE toward center at various heights ===")
for up_count in [2, 4, 6]:
    env4, obs4 = setup_l5()
    for _ in range(up_count): obs4 = env4.step(AMAP['U'])
    g4 = np.array(obs4.frame[-1])
    lp4, rp4 = block_pos(g4)
    print(f"\nAfter {up_count} UPs: L={lp4}, R={rp4}")
    for i in range(1, 12):
        g_before = np.array(obs4.frame[-1])
        obs4 = env4.step(GameAction.ACTION3)  # DIVERGE (R goes left)
        g_after = np.array(obs4.frame[-1])
        n = int(np.sum(g_before != g_after))
        lp4, rp4 = block_pos(g_after)
        blocked = "BLOCKED" if n == 0 else ""
        print(f"  DIVERGE {i}: L={lp4}, R={rp4}  cells={n}  {blocked}")
        if n == 0: break
    # Show final state
    g_final = np.array(obs4.frame[-1])
    render_zone(g_final, 20, 45, 2, 63, f"State after {up_count} UPs + max DIVERGEs:")

# ── 6. Can R enter LEFT shaft rows from the center? ──────────────────────────
print("\n\n=== Does R block ever appear in left half (cols 0-31)? ===")
# Check after navigating R as far left as possible at rows 30-33 (corridor area)
env5, obs5 = setup_l5()
# Get to corridor row area: UP until near rows 30-33
nav = 'UUUUUU'  # 6 UPs → rows 42-45 → blocked at 2 UPs → stays at 42
for a in nav: obs5 = env5.step(AMAP[a])
# Now DIVERGE (R goes left) as far as possible
for _ in range(15): obs5 = env5.step(GameAction.ACTION3)
g5 = np.array(obs5.frame[-1])
lp5, rp5 = block_pos(g5)
print(f"After max UPs + DIVERGEs: L={lp5}, R={rp5}")
# Check if any block cells in left half
r_cells = np.argwhere(g5 == 10)
in_left = [(int(r),int(c)) for r,c in r_cells if c < 32]
in_right = [(int(r),int(c)) for r,c in r_cells if c >= 32]
print(f"  Block cells in left half (cols 0-31): {in_left[:5]}")
print(f"  Block cells in right half (cols 32-63): {in_right[:5]}")

print("\nDone.")
