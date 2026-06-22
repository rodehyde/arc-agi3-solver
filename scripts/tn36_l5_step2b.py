"""tn36 L5 Step 2b — targeted follow-up probes:
1. Intermediate frames for DOWN+oval (does piece actually travel?)
2. Where do the 14 new cells land after Zone 2?
3. Zone 2 + right oval — does anything change for right panel?
4. Left oval alone: show the resulting piece location
5. Zone 1 role — what happens to the right panel after Zone 1?
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
RC = [34, 39, 44, 49, 54, 59]  # right legend H-bar centers

CMAP = {0:'.',1:'f',2:'m',3:'d',4:'v',5:'#',6:'K',7:'k',
        8:'r',9:'B',10:'L',11:'Y',12:'O',13:'M',14:'G',15:'P'}

def make_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    for r, c in L1 + L2 + L3 + L4:
        obs = env.step(GameAction.ACTION6, {'x': c, 'y': r})
    assert obs.levels_completed == 4
    return env, obs

def click(env, row, col):
    return env.step(GameAction.ACTION6, {'x': col, 'y': row})

def show_panel(frame, label, r0, r1, c0, c1):
    g = np.array(frame)
    print(f"  [{label}] rows {r0}-{r1} cols {c0}-{c1}:")
    for r in range(r0, r1+1):
        s = ''.join(CMAP.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        vals = set(int(g[r,c]) for c in range(c0, c1+1))
        non_bg = vals - {0,2,3}
        if non_bg:
            print(f"    r{r:2d}: {s}  {sorted(non_bg)}")

def show_yellow_right(frame, tag=''):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    if yc:
        ry = sorted(set(r for r,c in yc)); cy = sorted(set(c for r,c in yc))
        print(f"  [{tag}] Yellow: rows={ry} cols={cy} count={len(yc)}")
    else:
        print(f"  [{tag}] Yellow piece: NOT in right panel rows 3-31")

def show_vdkg_left(frame, tag=''):
    """Show where vdkgrey cells are in left panel (the piece)."""
    g = np.array(frame)
    vc = [(int(r),int(c)) for r,c in np.argwhere(g==4) if 0<=c<=31]
    if vc:
        rv = sorted(set(r for r,c in vc)); cv = sorted(set(c for r,c in vc))
        print(f"  [{tag}] Left piece (v=4): rows={rv} cols={cv} count={len(vc)}")
    else:
        print(f"  [{tag}] Left piece: NONE")

sep = lambda t: print(f"\n{'='*60}\n{t}\n{'='*60}")

# ── 1. DOWN+oval: check ALL intermediate frames ───────────────────────────────
sep("H33+V35 (DOWN, 2 groups) + oval: ALL FRAMES yellow position")
env, obs = make_l5()
for i in range(2):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_yellow_right(frame, f"f{i}")

# ── 2. Zone 2: show WHERE the 14 new cells appear ────────────────────────────
sep("Zone 2 (58,25): full left panel after click")
env, obs = make_l5()
print("BEFORE Zone 2:")
show_vdkg_left(obs.frame[-1], 'before')
result = click(env, 58, 25)
print(f"  frames={len(result.frame)}")
print("AFTER Zone 2:")
show_vdkg_left(result.frame[-1], 'after')
show_panel(result.frame[-1], 'left-panel', 0, 31, 0, 31)

# ── 3. Zone 3: show left panel after click ────────────────────────────────────
sep("Zone 3 (58,35): full left panel after click")
env, obs = make_l5()
result = click(env, 58, 35)
print(f"  frames={len(result.frame)}")
show_vdkg_left(result.frame[-1], 'after Zone3')

# ── 4. Left oval ALONE: show left panel + all frames ─────────────────────────
sep("Left oval (58,5) ALONE: all frames + left panel after")
env, obs = make_l5()
result = click(env, 58, 5)
print(f"  frames={len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_vdkg_left(frame, f"f{i}")
show_panel(result.frame[-1], 'left-after', 0, 20, 0, 32)

# ── 5. Zone 2 + right oval: does RIGHT panel change? ─────────────────────────
sep("Zone 2 + right oval (no legend): all frames")
env, obs = make_l5()
click(env, 58, 25)  # Zone 2
result = click(env, 58, 58)  # right oval
print(f"  frames={len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_yellow_right(frame, f"f{i}")

# ── 6. Zone 1 + right oval: check all frames ─────────────────────────────────
sep("Zone 1 + right oval (no legend): all frames")
env, obs = make_l5()
click(env, 58, 15)  # Zone 1
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_yellow_right(frame, f"f{i}")

# ── 7. Zone 1 + H33+V35 (DOWN, 1 group) + right oval ─────────────────────────
sep("Zone 1 + DOWN(1 group) + right oval")
env, obs = make_l5()
click(env, 58, 15)  # Zone 1
click(env, 33, RC[0]); click(env, 35, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_yellow_right(frame, f"f{i}")

# ── 8. Zone 2 + H33+V35 (DOWN, 1 group) + right oval ─────────────────────────
sep("Zone 2 + DOWN(1 group) + right oval: all frames")
env, obs = make_l5()
click(env, 58, 25)  # Zone 2
click(env, 33, RC[0]); click(env, 35, RC[0])
result = click(env, 58, 58)
print(f"  frames={len(result.frame)}")
for i, frame in enumerate(result.frame):
    show_yellow_right(frame, f"f{i}")

# ── 9. Zone 4: show FULL GRID changes (right + left panel) ─────────────────
sep("Zone 4 (58,45): full grid diff - what turns purple?")
env, obs = make_l5()
g_before = np.array(obs.frame[-1])
result = click(env, 58, 45)
g_after = np.array(result.frame[-1])
print(f"  frames={len(result.frame)}")
# Show where new purple cells appear
purple_new = np.argwhere((g_before != 15) & (g_after == 15))
print(f"  New purple cells: {len(purple_new)}")
if len(purple_new) > 0:
    pr = sorted(set(int(r) for r,c in purple_new))
    pc = sorted(set(int(c) for r,c in purple_new))
    print(f"  Purple rows={pr}")
    print(f"  Purple cols={pc}")
# Show right panel rows 3-31
print("Right panel after Zone 4:")
show_panel(result.frame[-1], 'right-Zone4', 3, 31, 32, 63)

# ── 10. Legend state after Zone 1, 2, 3 ─────────────────────────────────────
sep("Legend state after each zone click")
for zone_r, zone_c, label in [(58,15,'Zone1'), (58,25,'Zone2'), (58,35,'Zone3')]:
    env, obs = make_l5()
    result = click(env, zone_r, zone_c)
    g = np.array(result.frame[-1])
    print(f"\n  After {label}:")
    for row_r in [33, 35, 39, 41, 45, 47]:
        left_active = [c for c in range(0,32) if int(g[row_r,c])==5 and c not in [0,31]]
        right_active = [c for c in range(32,64) if int(g[row_r,c])==5 and c not in [62,63]]
        print(f"    r{row_r}: left_active={left_active}  right_active={right_active}")
