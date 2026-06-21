"""tn36 Step 2b — deeper probing of grid interaction mechanics.
Testing: sequences of legend clicks + grid clicks at more locations.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

colour = {0:'white',1:'lt-grey',3:'dk-grey',4:'vdk-grey',5:'black',9:'blue',11:'yellow'}
char = {0:'.',1:'f',3:'d',4:'v',5:'#',9:'B',11:'Y'}

def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    return env, obs, np.array(obs.frame[-1])

def click(env, col, row):
    obs = env.step(GameAction.ACTION6, {'x': col, 'y': row})
    return obs, np.array(obs.frame[-1])

def diff_grid(g0, g1, label):
    changed = np.argwhere(g0 != g1)
    interior = [(int(r),int(c)) for r,c in changed if 8<=r<=47 and 13<=c<=50]
    bar = [(int(r),int(c)) for r,c in changed if r==1]
    legend = [(int(r),int(c)) for r,c in changed if 41<=r<=47]
    trans = {}
    for r,c in changed:
        k = (int(g0[r,c]), int(g1[r,c]))
        trans[k] = trans.get(k, 0) + 1
    if not len(changed):
        print(f"  {label}: NO CHANGE")
        return
    parts = []
    if interior: parts.append(f"GRID:{len(interior)}cells")
    if legend: parts.append(f"LEGEND:{len(legend)}cells")
    if bar: parts.append(f"BAR:-{len(bar)}")
    tr_str = ' '.join(f"{a}→{b}:{n}" for (a,b),n in sorted(trans.items()))
    print(f"  {label}: {' '.join(parts)}  [{tr_str}]")
    if interior:
        print(f"    *** GRID CHANGED! ***")
        for r,c in sorted(interior):
            print(f"      ({r},{c}): {int(g0[r,c])}→{int(g1[r,c])}")

def render_grid(g, label=''):
    if label: print(f"  [{label}]")
    for r in range(9, 41):
        row = ''.join(char.get(int(g[r,c]),'?') for c in range(14,50))
        if any(g[r,c]==11 for c in range(14,50)) or any(g[r,c] not in (4,5) for c in range(14,50)):
            print(f"  {r:2d}: {row}")

def render_legend(g, label=''):
    if label: print(f"  [{label}]")
    for r in range(41, 48):
        row = ''.join(char.get(int(g[r,c]),'?') for c in range(13,51))
        print(f"  {r:2d}: {row}")

# ── Test 1: Click each yellow cell in zone 1 individually ──────────────
print("="*60)
print("TEST 1: Click each yellow cell in zone 1 one at a time")
yellow_z1 = [(13,30),(13,31),(13,32),(13,33),(14,30),(14,31),(14,32),(14,33),
             (15,30),(15,31),(15,32),(15,33),(16,30),(16,33)]
env, obs, g0 = fresh()
g_prev = g0.copy()
for row, col in yellow_z1:
    obs, g = click(env, col, row)
    diff_grid(g_prev, g, f"click yellow ({row},{col})")
    g_prev = g.copy()

# ── Test 2: All legend pieces toggled — watch for grid change ──────────
print("\n"+"="*60)
print("TEST 2: Toggle all legend pieces, check grid state after each")
# Pieces: group A horiz (42,25-27), group A vert (45,26),
#         group B horiz (42,35-37), group B vert (45,36)
#         group C horiz (42,40-42), group C vert (45,41)
#         group D horiz (42,20-22), group D vert (45,21)
#         group E horiz (42,30-32), group E vert (45,31)
pieces = [
    ("A-horiz", 42, 26), ("A-vert", 45, 26),
    ("B-horiz", 42, 36), ("B-vert", 45, 36),
    ("C-horiz", 42, 41), ("C-vert", 45, 41),
    ("D-horiz", 42, 21), ("D-vert", 45, 21),
    ("E-horiz", 42, 31), ("E-vert", 45, 31),
]
env, obs, g0 = fresh()
g_prev = g0.copy()
for name, row, col in pieces:
    obs, g = click(env, col, row)
    diff_grid(g_prev, g, f"toggle {name}")
    g_prev = g.copy()
print("  Final legend state:"); render_legend(g)
print("  Final grid state:"); render_grid(g)
print(f"  levels={obs.levels_completed}")

# ── Test 3: After toggling group A horiz, click each tile type in grid ──
print("\n"+"="*60)
print("TEST 3: Select A-horiz, then click various grid positions")
env, obs, g0 = fresh()
# Toggle group A horiz (lt-grey→black = "selected")
obs, g_sel = click(env, 26, 42)
print(f"  After selecting A-horiz: legend A col 25-27 row 42 now black")
# Try clicking at various grid positions
grid_targets = [
    ("black tile (9-12,14-17)", 10, 15),
    ("vdk-grey tile (9-12,18-21)", 10, 19),
    ("yellow zone1 top-left", 13, 30),
    ("yellow zone1 col 30-32 row13 (3-cell horiz)", 13, 31),
    ("vdk-grey adj to yellow", 12, 30),
    ("black adj to yellow zone1", 13, 26),
    ("white border row 8", 8, 30),
    ("white border row 41", 41, 30),
]
for name, row, col in grid_targets:
    obs, g = click(env, col, row)
    diff_grid(g_sel, g, f"  → {name} ({row},{col})")
    g_sel = g.copy()

# ── Test 4: Click legend pieces in "natural" positions then probe ──────
print("\n"+"="*60)
print("TEST 4: Try different piece selections (black→lt-grey = 'activating' black pieces)")
env, obs, g0 = fresh()
# D is black — toggle to lt-grey
obs, g = click(env, 21, 42); diff_grid(g0, g, "D-horiz (black→lt-grey)")
g_after_D = g.copy()
# Now try clicking vdk-grey positions
for row, col in [(10,19),(13,34),(37,34),(37,30)]:
    obs, g = click(env, col, row)
    diff_grid(g_after_D, g, f"  click ({row},{col})")
    g_after_D = g.copy()

# ── Test 5: Click the yellow zone 2 cells one at a time ────────────────
print("\n"+"="*60)
print("TEST 5: Click each yellow cell in zone 2")
yellow_z2 = [(33,29),(33,34),(34,29),(34,34),(35,29),(35,34),
             (36,29),(36,31),(36,32),(36,34),
             (37,29),(37,30),(37,31),(37,32),(37,33),(37,34)]
env, obs, g0 = fresh()
g_prev = g0.copy()
for row, col in yellow_z2:
    obs, g = click(env, col, row)
    diff_grid(g_prev, g, f"click yellow ({row},{col})")
    g_prev = g.copy()

# ── Test 6: Check if clicking the border at specific cols triggers anything
print("\n"+"="*60)
print("TEST 6: Click along the inner white border (row 8) at different cols")
env, obs, g0 = fresh()
g_prev = g0.copy()
for col in [14,18,22,26,30,34,38,42,46]:
    obs, g = click(env, col, 8)
    diff_grid(g_prev, g, f"row8 col{col}")
    g_prev = g.copy()

# ── Test 7: After toggling A-horiz, click along row 8 ──────────────────
print("\n"+"="*60)
print("TEST 7: Select A-horiz THEN click along row 8")
env, obs, g0 = fresh()
obs, g_sel = click(env, 26, 42)  # select A-horiz
g_prev = g_sel.copy()
for col in [14,18,22,26,30,34,38,42,46]:
    obs, g = click(env, col, 8)
    diff_grid(g_prev, g, f"(A-horiz selected) row8 col{col}")
    g_prev = g.copy()

# ── Test 8: Try clicking in the white cells WITHIN the checkered area ──
print("\n"+"="*60)
print("TEST 8: Click white cells inside grid border (rows 41,8)")
env, obs, g0 = fresh()
g_prev = g0.copy()
for row, col in [(41,30),(41,26),(8,30),(8,26)]:
    obs, g = click(env, col, row)
    diff_grid(g_prev, g, f"white ({row},{col})")
    g_prev = g.copy()
