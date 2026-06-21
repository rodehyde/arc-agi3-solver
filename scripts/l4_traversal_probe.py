"""Probe whether blocks can traverse all intermediate positions needed in L4.
Tests multiple consecutive UP/DOWN steps from starting positions.
Renders each intermediate state to expose any red/blocked cells.
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
    for a in NAV3:
        obs = env.step(AMAP[a])
    return env, obs

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    lp = (int(left[:, 0].min()), int(left[:, 1].min())) if len(left) else None
    rp = (int(right[:, 0].min()), int(right[:, 1].min())) if len(right) else None
    return lp, rp

def grid_diff(g_before, g_after):
    diff = np.where(g_before != g_after)
    if not len(diff[0]): return 0, {}
    rows, cols = diff
    transitions = {}
    for r, c in zip(rows, cols):
        key = f"{char.get(int(g_before[r,c]),'?')}({g_before[r,c]})->{char.get(int(g_after[r,c]),'?')}({g_after[r,c]})"
        transitions[key] = transitions.get(key, 0) + 1
    return len(rows), transitions

def render_full_row(g, r):
    """Render cols 7-55 for a given row."""
    row = "".join(char.get(int(g[r, c]), '?') for c in range(7, 56))
    return f"  {r:2d}: {row}"

# ── Render full grid rows 9-53 showing checkerboard layout ────────────────────
print("=== Full grid rows 9-53, cols 7-55 (to see checkerboard extent) ===")
env0, obs0 = setup_l4()
g0 = np.array(obs0.frame[-1])
print("     " + "".join(f"{c%10}" for c in range(7, 56)))
for r in range(9, 54):
    row = "".join(char.get(int(g0[r, c]), '?') for c in range(7, 56))
    red_cols = [c for c in range(64) if g0[r, c] == 8]
    ann = f"  <- RED at {red_cols}" if red_cols else ""
    print(f"{r:3d}  {row}{ann}")

# ── Test UP steps: how far can each block go UP? ──────────────────────────────
print("\n\n=== Consecutive UP steps from start ===")
env1, obs1 = setup_l4()
g = np.array(obs1.frame[-1])
lp, rp = block_pos(g)
print(f"Start: L={lp}, R={rp}")

for i in range(1, 10):
    g_before = np.array(obs1.frame[-1])
    obs1 = env1.step(GameAction.ACTION1)  # UP
    g_after = np.array(obs1.frame[-1])
    n, trans = grid_diff(g_before, g_after)
    lp, rp = block_pos(g_after)
    moved = "MOVED" if n > 0 else "*** BLOCKED ***"
    print(f"  UP {i}: L={lp}, R={rp}  [{moved}]  cells_changed={n}  {trans}")
    if n == 0:
        print(f"       *** NEITHER BLOCK MOVED - AT WALL ***")
        break
    # Check for any non-black/non-ltblue transitions (red cells involved?)
    for k in trans:
        if 'R(8)' in k:
            print(f"       *** RED CELL INVOLVED: {k} x{trans[k]} ***")

# ── Test DOWN steps: how far can each block go DOWN? ─────────────────────────
print("\n\n=== Consecutive DOWN steps from start ===")
env2, obs2 = setup_l4()
g = np.array(obs2.frame[-1])
lp, rp = block_pos(g)
print(f"Start: L={lp}, R={rp}")

for i in range(1, 10):
    g_before = np.array(obs2.frame[-1])
    obs2 = env2.step(GameAction.ACTION2)  # DOWN
    g_after = np.array(obs2.frame[-1])
    n, trans = grid_diff(g_before, g_after)
    lp, rp = block_pos(g_after)
    moved = "MOVED" if n > 0 else "*** BLOCKED ***"
    print(f"  DOWN {i}: L={lp}, R={rp}  [{moved}]  cells_changed={n}  {trans}")
    if n == 0:
        break
    for k in trans:
        if 'R(8)' in k:
            print(f"       *** RED CELL INVOLVED: {k} x{trans[k]} ***")

# ── Test horizontal movement at each row level (for CONVERGE in corridor) ────
print("\n\n=== CONVERGE steps from corridor position (after 1 DOWN) ===")
env3, obs3 = setup_l4()
obs3 = env3.step(GameAction.ACTION2)  # 1 DOWN: R enters corridor
g = np.array(obs3.frame[-1])
lp, rp = block_pos(g)
print(f"After 1 DOWN: L={lp}, R={rp}")

for i in range(1, 12):
    g_before = np.array(obs3.frame[-1])
    obs3 = env3.step(GameAction.ACTION4)  # CONVERGE
    g_after = np.array(obs3.frame[-1])
    n, trans = grid_diff(g_before, g_after)
    lp, rp = block_pos(g_after)
    moved = "MOVED" if n > 0 else "BLOCKED"
    print(f"  CONVERGE {i}: L={lp}, R={rp}  [{moved}]  {trans if n else ''}")
    for k in trans:
        if 'R(8)' in k:
            print(f"       *** RED CELL INVOLVED: {k} x{trans[k]} ***")
    if n == 0:
        break
