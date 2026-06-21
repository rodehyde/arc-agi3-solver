"""Probe: freeze at rows 14 (bands open) then move marker UP through band zone.
Also checks where the marker can reach on B's side (col 43) to pin B.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
L5 = 'XXUUUUUUXUCCCCUUXXXXXXUUUUUUUUCCCCCCXXXUUUUUXXXX'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}

def make_l6():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2: obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {'x': 31, 'y': 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {'x': 14, 'y': 46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {'x': bxy2[0], 'y': bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {'x': 14, 'y': 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {'x': bxy3[0], 'y': bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {'x': 14, 'y': 46})
    for a in NAV3: obs = env.step(AMAP[a])
    for a in 'UU': obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {'x': 30, 'y': 30})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {'x': 9, 'y': 40})
    for a in 'DDCDCC': obs = env.step(AMAP[a])
    for a in L5: obs = env.step(AMAP[a])
    assert obs.levels_completed == 5
    return env, obs

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    lp = (int(left[:, 0].min()), int(left[:, 1].min())) if len(left) else None
    rp = (int(right[:, 0].min()), int(right[:, 1].min())) if len(right) else None
    return lp, rp

def find_val(g, val):
    cells = np.argwhere(g == val)
    return (int(cells[0, 0]), int(cells[0, 1])) if len(cells) else None

char = {0: '.', 1: 'f', 5: '#', 6: 'p', 7: 'q', 8: 'R', 9: 'M',
        10: 'L', 11: 'Y', 12: 'O', 13: 'm', 14: 'G', 15: 'V'}

def render(g, r0, r1, c0, c1, label=''):
    if label: print(f'\n{label}')
    print('      ' + ''.join(f'{c % 10}' for c in range(c0, c1 + 1)))
    for r in range(r0, r1 + 1):
        row = ''.join(char.get(int(g[r, c]), '?') for c in range(c0, c1 + 1))
        print(f'{r:3d}   {row}')

# ─────────────────────────────────────────────────────────
env, obs = make_l6()
g = np.array(obs.frame[-1])
A, B = block_pos(g)
print(f"L6 start: A={A}, B={B}, marker={find_val(g, 9)}")

# Navigate to rows 14 FIRST (bands open)
for _ in range(2): obs = env.step(GameAction.ACTION1)
g = np.array(obs.frame[-1])
A, B = block_pos(g)
print(f"After UP×2: A={A}, B={B}")
print(f"  Bands open? green-band sample: {[int(g[30,c]) for c in range(14,26)]}")
print(f"  orange-band sample: {[int(g[30,c]) for c in range(38,50)]}")

# Freeze at rows 14 (bands open)
obs = env.step(GameAction.ACTION6, {'x': 31, 'y': 43})  # click marker
g = np.array(obs.frame[-1])
Y = find_val(g, 11)
print(f"\nFrozen at rows 14. yellow marker={Y}")
print(f"  Bands during freeze? green: {[int(g[30,c]) for c in range(14,26)]}")

# Test: CON×3 then UP×8 (try to reach rows 15-19 via orange side)
print("\n--- CON×3 (col 31→43, B side) then UP×8 ---")
for i in range(3):
    obs = env.step(GameAction.ACTION4)  # CON
    g = np.array(obs.frame[-1])
    Y = find_val(g, 11)
    print(f"  CON {i+1}: yellow={Y}")

for i in range(8):
    obs = env.step(GameAction.ACTION1)  # UP
    g = np.array(obs.frame[-1])
    Y = find_val(g, 11)
    print(f"  UP  {i+1}: yellow={Y}")

# Unfreeze
obs = env.step(GameAction.ACTION6, {'x': 10, 'y': 22})
g = np.array(obs.frame[-1])
A, B = block_pos(g)
M = find_val(g, 9)
print(f"\nAfter unfreeze: A={A}, B={B}, blue marker={M}")
render(g, 12, 48, 6, 57, "State after freeze-at-14 repositioning")

# Now test: does DOWN with marker at this position pin B?
print("\n--- Test pinning: press DOWN and watch ---")
for i in range(8):
    obs = env.step(GameAction.ACTION2)  # DOWN
    g = np.array(obs.frame[-1])
    A, B = block_pos(g)
    lvl = obs.levels_completed
    print(f"  DOWN {i+1}: A={A}, B={B}  lvl={lvl}")
    if lvl > 5:
        print("  *** WIN ***"); break
    if A is None or B is None:
        print("  *** RESET ***"); break
    if A != B:  # different positions = one was pinned
        print(f"  *** ASYMMETRIC MOVEMENT: A≠B ***")
