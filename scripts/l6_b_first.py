"""Step 4: Test B-first hypothesis for m0r0 L6.
Phase 0: Freeze → DIV×3, UP×6, unfreeze  (marker to rows 19, col 19 — pins A)
Navigate: UP×2 (blocks to rows 14)
Phase 1: DOWN×7  (A pinned, B through orange band to rows 42 → green object)
Phase 2: Freeze → CON×1, unfreeze  (marker to col 23 — unpin A)
Phase 3: DOWN×7  (A through green band to rows 42, B pinned by green object)
Phase 4: CONVERGE×3  (overlap at col 30 → WIN)
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
char = {0: '.', 1: 'f', 5: '#', 6: 'p', 7: 'q', 8: 'R', 9: 'M',
        10: 'L', 11: 'Y', 12: 'O', 13: 'm', 14: 'G', 15: 'V'}

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

def render(g, r0, r1, c0, c1, label=''):
    if label: print(f'\n{label}')
    print('      ' + ''.join(f'{c % 10}' for c in range(c0, c1 + 1)))
    for r in range(r0, r1 + 1):
        row = ''.join(char.get(int(g[r, c]), '?') for c in range(c0, c1 + 1))
        print(f'{r:3d}   {row}')

def diff_summary(g0, g1):
    changed = np.argwhere(g0 != g1)
    interior = [(int(r), int(c)) for r, c in changed if 1 <= r <= 62 and 1 <= c <= 62]
    trans = {}
    for r, c in changed:
        k = (int(g0[r, c]), int(g1[r, c]))
        trans[k] = trans.get(k, 0) + 1
    return len(interior), trans

# ─────────────────────────────────────────────────────────
env, obs = make_l6()
g = np.array(obs.frame[-1])
A, B = block_pos(g)
M = find_val(g, 9)
print(f"L6 start: A={A}, B={B}, marker={M}")
render(g, 12, 50, 6, 57, "L6 initial")

# ── Phase 0: reposition marker to (row=19, col=19) ──
print("\n=== PHASE 0: Freeze → DIV×3 → UP×6 → unfreeze ===")
obs = env.step(GameAction.ACTION6, {'x': 31, 'y': 43})  # freeze (col=31, row=43)
g = np.array(obs.frame[-1])
Y = find_val(g, 11)  # yellow marker
print(f"  Frozen. yellow marker={Y}  (frozen blocks at 1={np.sum(g==1)} cells)")

for i in range(3):
    obs = env.step(GameAction.ACTION3)  # DIV
    g = np.array(obs.frame[-1])
    Y = find_val(g, 11)
    print(f"  DIV {i+1}: yellow={Y}")

for i in range(6):
    obs = env.step(GameAction.ACTION1)  # UP
    g = np.array(obs.frame[-1])
    Y = find_val(g, 11)
    print(f"  UP  {i+1}: yellow={Y}")

obs = env.step(GameAction.ACTION6, {'x': 10, 'y': 10})  # unfreeze
g = np.array(obs.frame[-1])
A, B = block_pos(g)
M = find_val(g, 9)
print(f"  Unfrozen. A={A}, B={B}, blue marker={M}")
render(g, 14, 48, 6, 57, "After Phase 0")

# ── Navigate UP×2 → rows 14 ──
print("\n=== NAVIGATE UP×2 → rows 14 ===")
for _ in range(2): obs = env.step(GameAction.ACTION1)
g = np.array(obs.frame[-1])
A, B = block_pos(g)
print(f"  A={A}, B={B}")

# ── Phase 1: DOWN×7 (A pinned, B through orange band) ──
print("\n=== PHASE 1: DOWN×7 — A pinned, B descends ===")
for i in range(7):
    g0 = np.array(obs.frame[-1])
    obs = env.step(GameAction.ACTION2)
    g = np.array(obs.frame[-1])
    A, B = block_pos(g)
    n, trans = diff_summary(g0, g)
    lvl = obs.levels_completed
    print(f"  DOWN {i+1}: A={A}, B={B}  cells_changed={n}  lvl={lvl}")
    if lvl > 5:
        print("  *** LEVEL COMPLETE! ***")
        break
    if A is None or B is None:
        print("  *** RESET — blocks not found ***")
        break

render(g, 12, 50, 6, 57, "After Phase 1")

# Check what B is sitting on
print("\nCells at rows 42-45, cols 38-49 (B's side lower zone):")
for r in range(42, 46):
    vals = [(c, int(g[r, c])) for c in range(38, 50)]
    print(f"  row {r}: {vals}")

# ── Phase 2: unpin A ──
print("\n=== PHASE 2: Freeze → CON×1 → unfreeze (move marker col 19→23) ===")
M = find_val(g, 9)
print(f"  Blue marker at {M}, clicking (x={M[1]}, y={M[0]})")
obs = env.step(GameAction.ACTION6, {'x': M[1], 'y': M[0]})  # freeze
g = np.array(obs.frame[-1])
Y = find_val(g, 11)
print(f"  Frozen. yellow={Y}")

obs = env.step(GameAction.ACTION4)  # CON×1
g = np.array(obs.frame[-1])
Y = find_val(g, 11)
print(f"  CON×1: yellow={Y}")

obs = env.step(GameAction.ACTION6, {'x': 10, 'y': 10})  # unfreeze
g = np.array(obs.frame[-1])
A, B = block_pos(g)
M = find_val(g, 9)
print(f"  Unfrozen. A={A}, B={B}, blue marker={M}")

# ── Phase 3: DOWN×7 (A through green band, B pinned) ──
print("\n=== PHASE 3: DOWN×7 — A descends, B should stay pinned ===")
for i in range(7):
    g0 = np.array(obs.frame[-1])
    obs = env.step(GameAction.ACTION2)
    g = np.array(obs.frame[-1])
    A, B = block_pos(g)
    n, trans = diff_summary(g0, g)
    lvl = obs.levels_completed
    print(f"  DOWN {i+1}: A={A}, B={B}  cells_changed={n}  lvl={lvl}")
    if lvl > 5:
        print("  *** LEVEL COMPLETE! ***")
        break
    if A is None or B is None:
        print("  *** RESET ***")
        break

render(g, 38, 50, 6, 57, "After Phase 3")

# ── Phase 4: CONVERGE×3 ──
print("\n=== PHASE 4: CONVERGE×3 → overlap ===")
for i in range(3):
    obs = env.step(GameAction.ACTION4)
    g = np.array(obs.frame[-1])
    A, B = block_pos(g)
    lvl = obs.levels_completed
    print(f"  CON {i+1}: A={A}, B={B}  lvl={lvl}")
    if lvl > 5:
        print(f"  *** LEVEL {lvl} COMPLETE! WIN! ***")
        break

print(f"\nFinal: levels_completed={obs.levels_completed}, win_levels={obs.win_levels}")
render(g, 38, 50, 6, 57, "Final state")
