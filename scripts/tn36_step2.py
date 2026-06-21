"""tn36 Step 2 — probe ACTION6 (click) on every distinct element type.
Full cell-change instrument: compare entire grid before/after each click.
Coordinate convention: ACTION6(x=col, y=row).
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

colour = {0:'white',1:'lt-grey',4:'vdk-grey',5:'black',9:'blue',11:'yellow'}
char = {0:'.',1:'f',4:'v',5:'#',9:'B',11:'Y'}

def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    return env, obs, np.array(obs.frame[-1])

def diff(g0, g1, label):
    changed = np.argwhere(g0 != g1)
    if not len(changed):
        print(f"  {label}: NO CHANGE")
        return
    interior = [(int(r),int(c)) for r,c in changed if 1<=r<=62 and 1<=c<=62]
    trans = {}
    for r,c in changed:
        k = (int(g0[r,c]), int(g1[r,c]))
        trans[k] = trans.get(k,0) + 1
    rows_ch = [r for r,c in interior]; cols_ch = [c for r,c in interior]
    print(f"  {label}: {len(interior)} cells changed, "
          f"bbox rows {min(rows_ch)}–{max(rows_ch)} cols {min(cols_ch)}–{max(cols_ch)}")
    for (v0,v1),n in sorted(trans.items()):
        print(f"    {v0}({colour.get(v0,'?')}) → {v1}({colour.get(v1,'?')}): {n} cells")

def render_region(g, r0, r1, c0, c1, label=''):
    if label: print(f"\n  [{label}]")
    for r in range(r0, r1+1):
        row = ''.join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        print(f"  {r:3d}: {row}")

def probe(target_name, row, col, render_r0=None, render_r1=None, render_c0=None, render_c1=None):
    env, obs, g0 = fresh()
    print(f"\n{'='*60}")
    print(f"PROBE: {target_name}  click(x={col}, y={row})")
    obs2 = env.step(GameAction.ACTION6, {'x': col, 'y': row})
    g1 = np.array(obs2.frame[-1])
    diff(g0, g1, "click 1")
    print(f"  levels={obs2.levels_completed}/{obs2.win_levels}  actions={obs2.available_actions}")
    if render_r0 is not None:
        render_region(g1, render_r0, render_r1, render_c0, render_c1, "after click 1")
    # Second click same cell — does it toggle?
    obs3 = env.step(GameAction.ACTION6, {'x': col, 'y': row})
    g2 = np.array(obs3.frame[-1])
    diff(g1, g2, "click 2 (same)")
    return env, obs2, g0, g1

def probe_then_second(target_name, r1, c1, r2, c2):
    """Click target, then click a second location."""
    env, obs, g0 = fresh()
    print(f"\n{'='*60}")
    print(f"PROBE SEQUENCE: {target_name}")
    print(f"  Click 1: (x={c1}, y={r1})")
    obs2 = env.step(GameAction.ACTION6, {'x': c1, 'y': r1})
    g1 = np.array(obs2.frame[-1])
    diff(g0, g1, "click 1")
    print(f"  Click 2: (x={c2}, y={r2})")
    obs3 = env.step(GameAction.ACTION6, {'x': c2, 'y': r2})
    g2 = np.array(obs3.frame[-1])
    diff(g1, g2, "click 2")
    diff(g0, g2, "net change (vs start)")
    print(f"  levels={obs3.levels_completed}/{obs3.win_levels}")

# ── Probe each distinct element type ──────────────────────────

# 1. Blue oval (rows 51–59, cols 32–40) — click centre
probe("BLUE OVAL centre", row=55, col=36, render_r0=48, render_r1=62, render_c0=28, render_c1=44)

# 2. Blue bar (row 1) — click centre
probe("BLUE BAR", row=1, col=31, render_r0=0, render_r1=3, render_c0=0, render_c1=63)

# 3. Lt-grey legend cell (group A, horiz, row 42 col 26)
probe("LT-GREY LEGEND (horiz)", row=42, col=26, render_r0=40, render_r1=48, render_c0=13, render_c1=50)

# 4. Lt-grey legend cell (group A, vert, row 45 col 26)
probe("LT-GREY LEGEND (vert)", row=45, col=26, render_r0=40, render_r1=48, render_c0=13, render_c1=50)

# 5. Black legend cell (group D, horiz, row 42 col 21)
probe("BLACK LEGEND (horiz)", row=42, col=21, render_r0=40, render_r1=48, render_c0=13, render_c1=50)

# 6. Vdk-grey tile in checkered grid (rows 9–12, cols 18–21)
probe("VDK-GREY TILE (checkered)", row=10, col=19, render_r0=8, render_r1=20, render_c0=14, render_c1=35)

# 7. Black tile in checkered grid (rows 9–12, cols 14–17)
probe("BLACK TILE (checkered)", row=10, col=15, render_r0=8, render_r1=20, render_c0=14, render_c1=35)

# 8. Yellow cell (zone 1, row 13 col 30)
probe("YELLOW CELL (zone 1)", row=13, col=30, render_r0=10, render_r1=20, render_c0=22, render_c1=42)

# 9. Yellow cell (zone 2, row 37 col 30)
probe("YELLOW CELL (zone 2)", row=37, col=30, render_r0=30, render_r1=42, render_c0=22, render_c1=42)

# 10. White space in legend zone
probe("WHITE SPACE (legend)", row=44, col=30, render_r0=40, render_r1=48, render_c0=13, render_c1=50)

# 11. White border channel (row 47 col 30)
probe("WHITE CHANNEL (below grid)", row=47, col=30)

# 12. Test: legend click then grid click (sequence)
print("\n" + "="*60)
print("SEQUENCE TEST: lt-grey legend (horiz) → vdk-grey tile")
probe_then_second("lt-grey horiz → vdk-grey tile", r1=42, c1=26, r2=10, c2=19)

print("\n" + "="*60)
print("SEQUENCE TEST: lt-grey legend (vert) → vdk-grey tile")
probe_then_second("lt-grey vert → vdk-grey tile", r1=45, c1=26, r2=10, c2=19)

print("\n" + "="*60)
print("SEQUENCE TEST: blue oval → vdk-grey tile")
probe_then_second("blue oval → vdk-grey tile", r1=55, c1=36, r2=10, c2=19)
