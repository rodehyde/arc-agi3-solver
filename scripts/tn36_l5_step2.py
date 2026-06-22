"""tn36 L5 Step 2 — action table probing.
Genuine unknowns:
1. 4 button zones (cols 13-17, 22-28, 32-38, 42-48, row 58) — function unknown
2. What CONTRACT does to the 4-wide piece at rows 8-11
3. Does DOWN + oval move the piece at all?
4. Left oval (58,5) — what does it trigger?
Full cell-change instrument on every probe.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]
RC = [34, 39, 44, 49, 54, 59]  # right legend H-bar centers (groups 1-6)

CMAP = {0:'.',1:'f',2:'m',3:'d',4:'v',5:'#',6:'K',7:'k',
        8:'r',9:'B',10:'L',11:'Y',12:'O',13:'M',14:'G',15:'P'}

def make_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    for r, c in L1 + L2 + L3 + L4:
        obs = env.step(GameAction.ACTION6, {'x': c, 'y': r})
    assert obs.levels_completed == 4, f"Expected 4, got {obs.levels_completed}"
    return env, obs

def click(env, row, col):
    return env.step(GameAction.ACTION6, {'x': col, 'y': row})

def grid_diff(g1, g2, tag=''):
    """Full cell-change instrument: counts, bounding box, value transitions."""
    a1, a2 = np.array(g1), np.array(g2)
    changed = np.argwhere(a1 != a2)
    if len(changed) == 0:
        print(f"  [{tag}] NO CHANGE")
        return
    rows_c = changed[:,0]; cols_c = changed[:,1]
    print(f"  [{tag}] {len(changed)} cells changed  bbox r{rows_c.min()}-{rows_c.max()} c{cols_c.min()}-{cols_c.max()}")
    transitions = {}
    for r,c in changed:
        k = (int(a1[r,c]), int(a2[r,c]))
        transitions[k] = transitions.get(k,0) + 1
    for (v1,v2),cnt in sorted(transitions.items()):
        print(f"    {v1}->{v2}: {cnt} cells")

def show_piece(frame, tag=''):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    if yc:
        ry = sorted(set(r for r,c in yc)); cy = sorted(set(c for r,c in yc))
        print(f"  [{tag}] Yellow piece: rows={ry} cols={cy} count={len(yc)}")
    else:
        print(f"  [{tag}] No yellow piece in right panel rows 3-31")

def show_rows(frame, r0, r1, tag=''):
    g = np.array(frame)
    for r in range(r0, r1+1):
        s = ''.join(CMAP.get(int(g[r,c]),'?') for c in range(32,64))
        if any(x in s for x in ['Y','K','P','B','#']) or any(int(g[r,c]) not in [0,2,3] for c in range(32,64)):
            print(f"  [{tag}] r{r:2d}: {s}")

separator = lambda t: print(f"\n{'='*60}\n{t}\n{'='*60}")

# ── 1. Button zone clicks — full cell diff ────────────────────────────────────
for zone, (row, col, label) in enumerate([
    (58, 5,  "Left oval (58,5)"),
    (58, 15, "Zone 1 (58,15) - full yellow rect"),
    (58, 25, "Zone 2 (58,25) - partial yellow"),
    (58, 35, "Zone 3 (58,35) - diamond yellow"),
    (58, 45, "Zone 4 (58,45) - 3x3 purple"),
    (58, 58, "Right oval (58,58)"),
], 0):
    separator(f"Click: {label}")
    env, obs = make_l5()
    g_before = obs.frame[-1]
    result = click(env, row, col)
    print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
    grid_diff(g_before, result.frame[-1], 'diff')
    show_piece(result.frame[-1], 'after')

# ── 2. Right legend DOWN (H33+V35, 1 group) + oval ───────────────────────────
separator("H33+V35 (DOWN, 1 group) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
click(env, 33, RC[0]); click(env, 35, RC[0])  # g1: H33+V35
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')

# ── 3. Right legend UP (H33+V47, 1 group) + oval ─────────────────────────────
separator("H33+V47 (UP, 1 group) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
click(env, 33, RC[0]); click(env, 47, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')

# ── 4. Right legend CONTRACT (H33+V41, 1 group) + oval ───────────────────────
separator("H33+V41 (CONTRACT, 1 group) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
click(env, 33, RC[0]); click(env, 41, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')

# ── 5. Right legend CONTRACT (H33+V41, 3 groups) + oval ──────────────────────
separator("H33+V41 (CONTRACT, 3 groups) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
for i in range(3):
    click(env, 33, RC[i]); click(env, 41, RC[i])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')
print("Right panel rows 4-30 after:")
show_rows(result.frame[-1], 4, 30, 'g3xCONTRACT')

# ── 6. Legend single bar clicks — characterise each bar type ─────────────────
separator("Single legend bar clicks (right legend): H33 only, V35 only, V41 only, V47 only")
for row_label, row_val in [("H33", 33), ("V35", 35), ("V41", 41), ("V47", 47)]:
    env, obs = make_l5()
    g_before = obs.frame[-1]
    result = click(env, row_val, RC[0])
    n_changed = np.sum(np.array(g_before) != np.array(result.frame[-1]))
    print(f"  Click r{row_val}c{RC[0]} ({row_label}): frames={len(result.frame)} changed={n_changed}")

# ── 7. Right legend V35 only (1 group) + oval → RIGHT ────────────────────────
separator("V35 only (RIGHT, 1 group) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
click(env, 35, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')

# ── 8. Right legend V35+V47 (LEFT, 1 group) + oval ───────────────────────────
separator("V35+V47 (LEFT, 1 group) + right oval")
env, obs = make_l5()
g_before = obs.frame[-1]
click(env, 35, RC[0]); click(env, 47, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')

# ── 9. DOWN x4 groups + oval — try to push piece past the pink gap ─────────────
separator("H33+V35 (DOWN, 4 groups) + right oval — try to reach purple")
env, obs = make_l5()
g_before = obs.frame[-1]
for i in range(4):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
show_piece(result.frame[-1], 'after')
print("Rows 8-30 after:")
show_rows(result.frame[-1], 8, 30, 'D4')

# ── 10. Check what the left panel piece does ─────────────────────────────────
separator("Left legend H33+V41 (3 groups) + LEFT OVAL (58,5)")
env, obs = make_l5()
g_before = obs.frame[-1]
# Left legend groups — left legend has groups at cols 11,16,21 (V-bars)
# H-bar centers at cols 11,16,21 for left legend
LC = [11, 16, 21]  # left legend group V-bar cols (and H-bar centers)
for c in LC:
    click(env, 33, c); click(env, 41, c)  # H33+V41 = CONTRACT on left legend
result = click(env, 58, 5)  # fire left oval
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
print("Left panel rows 4-20 after:")
g = np.array(result.frame[-1])
for r in range(3, 21):
    s = ''.join(CMAP.get(int(g[r,c]),'?') for c in range(0,32))
    if '#' in s or 'v' in s:
        print(f"  r{r:2d}: {s}")

# ── 11. Just fire left oval with no extra clicks ──────────────────────────────
separator("Left oval (58,5) ALONE — no legend clicks")
env, obs = make_l5()
g_before = obs.frame[-1]
result = click(env, 58, 5)
print(f"  frames={len(result.frame)}  levels={result.levels_completed}")
grid_diff(g_before, result.frame[-1], 'diff')
