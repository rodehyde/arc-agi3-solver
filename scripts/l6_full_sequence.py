"""Full L6 attempt:
Phase 0: UP×2, freeze-at-14, CON×3+UP×6, unfreeze  → marker (19,43), B pinned
Phase 1: DOWN×7                                      → A at rows 42 (green object), B at rows 14
Phase 2: freeze, DOWN×7+DIV×6, unfreeze             → marker (47,19), A pinned, B free
Phase 3: DOWN×7                                      → B through orange band to rows 42
Phase 4: CONVERGE×3                                  → overlap at col 30, WIN
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
char = {0:'.', 1:'f', 5:'#', 6:'p', 7:'q', 8:'R', 9:'M',
        10:'L', 11:'Y', 12:'O', 13:'m', 14:'G', 15:'V'}

def make_l6():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1+L2: obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {'x':31,'y':15})
    for act in [GameAction.ACTION4,GameAction.ACTION1,GameAction.ACTION4,GameAction.ACTION4,
                GameAction.ACTION4,GameAction.ACTION4,GameAction.ACTION2,GameAction.ACTION2,
                GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION3,GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {'x':14,'y':46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {'x':bxy2[0],'y':bxy2[1]})
    for act in [GameAction.ACTION1,GameAction.ACTION4,GameAction.ACTION1]: obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {'x':14,'y':46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {'x':bxy3[0],'y':bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {'x':14,'y':46})
    for a in NAV3: obs = env.step(AMAP[a])
    for a in 'UU': obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {'x':30,'y':30})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {'x':9,'y':40})
    for a in 'DDCDCC': obs = env.step(AMAP[a])
    for a in L5: obs = env.step(AMAP[a])
    assert obs.levels_completed == 5
    return env, obs

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left = cells[cells[:,1]<32]; right = cells[cells[:,1]>=32]
    lp = (int(left[:,0].min()), int(left[:,1].min())) if len(left) else None
    rp = (int(right[:,0].min()), int(right[:,1].min())) if len(right) else None
    return lp, rp

def find_val(g, val):
    cells = np.argwhere(g == val)
    return (int(cells[0,0]), int(cells[0,1])) if len(cells) else None

def render(g, r0, r1, c0, c1, label=''):
    if label: print(f'\n{label}')
    print('      '+''.join(f'{c%10}' for c in range(c0,c1+1)))
    for r in range(r0, r1+1):
        row = ''.join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f'{r:3d}   {row}')

def step_report(env, act, obs, label):
    g0 = np.array(obs.frame[-1])
    obs2 = env.step(act)
    g = np.array(obs2.frame[-1])
    A, B = block_pos(g)
    Y = find_val(g, 11); M = find_val(g, 9)
    marker_info = f"Y={Y}" if Y else f"M={M}"
    print(f"  {label}: A={A}, B={B}  {marker_info}  lvl={obs2.levels_completed}")
    return obs2, g

env, obs = make_l6()
g = np.array(obs.frame[-1])
print(f"L6 start: A={block_pos(g)[0]}, B={block_pos(g)[1]}, marker={find_val(g,9)}")

# ── Phase 0: navigate to rows 14, freeze, CON×3 UP×6, unfreeze ──
print("\n=== PHASE 0 ===")
obs = env.step(GameAction.ACTION1); obs = env.step(GameAction.ACTION1)  # UP×2
g = np.array(obs.frame[-1])
print(f"After UP×2: A={block_pos(g)[0]}, B={block_pos(g)[1]}")

obs = env.step(GameAction.ACTION6, {'x':31,'y':43})  # freeze
g = np.array(obs.frame[-1]); print(f"Frozen: Y={find_val(g,11)}")

for i in range(3):
    obs = env.step(GameAction.ACTION4)
    g = np.array(obs.frame[-1]); print(f"  CON {i+1}: Y={find_val(g,11)}")
for i in range(6):
    obs = env.step(GameAction.ACTION1)
    g = np.array(obs.frame[-1]); print(f"  UP  {i+1}: Y={find_val(g,11)}")

obs = env.step(GameAction.ACTION6, {'x':10,'y':10})  # unfreeze
g = np.array(obs.frame[-1])
A, B = block_pos(g); M = find_val(g, 9)
print(f"Unfrozen: A={A}, B={B}, marker={M}")

# ── Phase 1: DOWN×7 (A through green band, B pinned) ──
print("\n=== PHASE 1: DOWN×7 ===")
for i in range(7):
    obs, g = step_report(env, GameAction.ACTION2, obs, f"DOWN {i+1}")
    A, B = block_pos(g)
    if obs.levels_completed > 5: print("WIN!"); break
    if A is None or B is None: print("RESET"); break

render(g, 12, 50, 6, 57, "After Phase 1")
print(f"\nOrange band cells at rows 30-33 cols 38-49 (open=5, closed=12):")
for r in range(30, 34):
    vals = [int(g[r,c]) for c in range(38, 50)]
    print(f"  row {r}: {vals}")

# ── Phase 2: freeze (A at 42, B at 14), DOWN×7+DIV×6, unfreeze → marker (47,19) ──
print("\n=== PHASE 2: reposition marker to rows 47, col 19 ===")
M = find_val(g, 9)
print(f"Blue marker at {M}, clicking x={M[1]}, y={M[0]}")
obs = env.step(GameAction.ACTION6, {'x':M[1],'y':M[0]})  # freeze
g = np.array(obs.frame[-1]); print(f"Frozen: Y={find_val(g,11)}")
print(f"  Bands during freeze: green={[int(g[30,c]) for c in range(14,26)]}")
print(f"                      orange={[int(g[30,c]) for c in range(38,50)]}")

for i in range(7):
    obs = env.step(GameAction.ACTION2)  # DOWN
    g = np.array(obs.frame[-1]); print(f"  DOWN {i+1}: Y={find_val(g,11)}")
for i in range(6):
    obs = env.step(GameAction.ACTION3)  # DIV
    g = np.array(obs.frame[-1]); print(f"  DIV  {i+1}: Y={find_val(g,11)}")

obs = env.step(GameAction.ACTION6, {'x':10,'y':10})  # unfreeze
g = np.array(obs.frame[-1])
A, B = block_pos(g); M = find_val(g, 9)
print(f"Unfrozen: A={A}, B={B}, marker={M}")
render(g, 12, 52, 6, 57, "After Phase 2")

# ── Phase 3: DOWN×7 (B through orange band, A pinned) ──
print("\n=== PHASE 3: DOWN×7 (B descends, A pinned) ===")
for i in range(7):
    obs, g = step_report(env, GameAction.ACTION2, obs, f"DOWN {i+1}")
    A, B = block_pos(g)
    if obs.levels_completed > 5: print("WIN!"); break
    if A is None or B is None: print("RESET"); break

render(g, 38, 52, 6, 57, "After Phase 3")

# ── Phase 4: CONVERGE×3 ──
print("\n=== PHASE 4: CONVERGE×3 ===")
for i in range(3):
    obs, g = step_report(env, GameAction.ACTION4, obs, f"CON {i+1}")
    if obs.levels_completed > 5: print("WIN!"); break

print(f"\nFinal: levels={obs.levels_completed}/{obs.win_levels}")
render(g, 38, 52, 6, 57, "Final")
