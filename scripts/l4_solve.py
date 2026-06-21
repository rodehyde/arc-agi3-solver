"""Step 4: Test L4 hypothesis for m0r0.
Sequence: U, U, A6(freeze), X, X, X, A6(restore), D, D, C, D, C, C
Expected: 13 actions, RHAE = (26/13)^2 = 4.0
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
char = {0: '.', 1: 'a', 5: '#', 8: 'R', 9: 'B', 10: 'L', 11: 'Y', 15: 'V'}

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

def step(env, obs, action, label, kwargs=None):
    g_before = np.array(obs.frame[-1])
    lp0, rp0 = block_pos(g_before)
    if kwargs:
        obs2 = env.step(action, kwargs)
    else:
        obs2 = env.step(action)
    g_after = np.array(obs2.frame[-1])
    lp1, rp1 = block_pos(g_after)
    n = int(np.sum(g_before != g_after))
    win = obs2.levels_completed > 3
    print(f"  {label:35s}  L:{lp0}->{lp1}  R:{rp0}->{rp1}  changed={n}  {'*** WIN ***' if win else ''}")
    return obs2, win

env, obs = setup_l4()
g0 = np.array(obs.frame[-1])
lp, rp = block_pos(g0)
print(f"L4 start: L={lp}, R={rp}  levels_completed={obs.levels_completed}")
print()

print("Executing hypothesis sequence:")
win = False

obs, win = step(env, obs, GameAction.ACTION1, "1. UP")
obs, win = step(env, obs, GameAction.ACTION1, "2. UP")

# Find black cell for restore (left corridor, rows 40-45 are black)
g_cur = np.array(obs.frame[-1])
restore_cell = next(((c, r) for r in range(40, 46) for c in range(9, 24)
                     if g_cur[r, c] == 5), None)
print(f"   [restore cell: x={restore_cell[0]}, y={restore_cell[1]}]")

obs, win = step(env, obs, GameAction.ACTION6, "3. A6 freeze (30,30)", {"x": 30, "y": 30})
obs, win = step(env, obs, GameAction.ACTION3, "4. DIVERGE")
obs, win = step(env, obs, GameAction.ACTION3, "5. DIVERGE")
obs, win = step(env, obs, GameAction.ACTION3, "6. DIVERGE")

# Verify marker position before restore
g_frozen = np.array(obs.frame[-1])
yellow = np.argwhere(g_frozen == 11)
yellow_corridor = [(int(r), int(c)) for r, c in yellow if 29 <= r <= 33]
if not yellow_corridor:
    yellow_corridor = [(int(r), int(c)) for r, c in yellow if 25 <= r <= 40]
print(f"   [marker (yellow) in corridor after 3 DIVERGEs: {yellow_corridor[:5]}]")

obs, win = step(env, obs, GameAction.ACTION6, "7. A6 restore", {"x": restore_cell[0], "y": restore_cell[1]})

# Verify marker and block positions after restore
g_restore = np.array(obs.frame[-1])
blue = np.argwhere(g_restore == 9)
blue_corridor = [(int(r), int(c)) for r, c in blue if 28 <= r <= 34]
lp_r, rp_r = block_pos(g_restore)
print(f"   [after restore: L={lp_r}, R={rp_r}, marker(blue) in corridor: {blue_corridor[:5]}]")

obs, win = step(env, obs, GameAction.ACTION2, "8. DOWN (L blocked, only R)")
obs, win = step(env, obs, GameAction.ACTION2, "9. DOWN (L blocked, only R)")
obs, win = step(env, obs, GameAction.ACTION4, "10. CONVERGE")
obs, win = step(env, obs, GameAction.ACTION2, "11. DOWN (both enter corridor)")
obs, win = step(env, obs, GameAction.ACTION4, "12. CONVERGE")
obs, win = step(env, obs, GameAction.ACTION4, "13. CONVERGE -> WIN?")

print()
print(f"levels_completed={obs.levels_completed}  win_levels={obs.win_levels}")
if obs.levels_completed > 3:
    print("SUCCESS — Level 4 complete!")
else:
    g_final = np.array(obs.frame[-1])
    lp_f, rp_f = block_pos(g_final)
    print(f"FAILED — final positions L={lp_f}, R={rp_f}")
