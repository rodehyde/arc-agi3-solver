"""tn36 L5 Step 2c — two targeted probes:
1. CONTRACT intermediate frames: does piece shape change?
2. DOWN x5/x6: does piece land on purple target?
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
RC = [34, 39, 44, 49, 54, 59]

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

def show_piece_detail(frame, tag=''):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    if yc:
        ry = sorted(set(r for r,c in yc)); cy = sorted(set(c for r,c in yc))
        # Show shape row by row
        if len(ry) <= 6:
            for r in ry:
                row_y = sorted(c for rc,c in yc if rc==r)
                print(f"    r{r}: Y at cols={row_y}")
        else:
            print(f"  [{tag}] Yellow: rows={ry} cols={cy} count={len(yc)}")
    else:
        print(f"  [{tag}] No yellow piece in right panel")

sep = lambda t: print(f"\n{'='*60}\n{t}\n{'='*60}")

# ── 1. CONTRACT (H33+V41, 1 group) + oval: ALL intermediate frames ────────────
sep("CONTRACT (H33+V41, 1 group) + oval — ALL frames piece detail")
env, obs = make_l5()
click(env, 33, RC[0]); click(env, 41, RC[0])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    if yc:
        ry = sorted(set(r for r,c in yc)); cy = sorted(set(c for r,c in yc))
        print(f"  [f{i}] rows={ry} cols={cy} count={len(yc)}")
        if i in [0,1,2,7]:  # show detail for first few and last
            show_piece_detail(frame, f'f{i}-detail')

# ── 2. DOWN x3 + oval — does piece reach rows 20-23? ─────────────────────────
sep("DOWN x3 (H33+V35, 3 groups) + oval: all frames")
env, obs = make_l5()
for i in range(3):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}  levels={result.levels_completed}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    ry = sorted(set(r for r,c in yc)) if yc else []
    cy = sorted(set(c for r,c in yc)) if yc else []
    print(f"  [f{i}] rows={ry} cols={cy}")

# ── 3. DOWN x4 + oval ─────────────────────────────────────────────────────────
sep("DOWN x4 (H33+V35, 4 groups) + oval: all frames")
env, obs = make_l5()
for i in range(4):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}  levels={result.levels_completed}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    ry = sorted(set(r for r,c in yc)) if yc else []
    cy = sorted(set(c for r,c in yc)) if yc else []
    print(f"  [f{i}] rows={ry} cols={cy}")

# ── 4. DOWN x5 + oval ─────────────────────────────────────────────────────────
sep("DOWN x5 (H33+V35, 5 groups) + oval: all frames")
env, obs = make_l5()
for i in range(5):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}  levels={result.levels_completed}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    ry = sorted(set(r for r,c in yc)) if yc else []
    cy = sorted(set(c for r,c in yc)) if yc else []
    print(f"  [f{i}] rows={ry} cols={cy}")
# Show purple cells state
if result.levels_completed > 4 or len(result.frame) > 8:
    print("  *** POSSIBLE WIN ***")

# ── 5. DOWN x6 + oval ─────────────────────────────────────────────────────────
sep("DOWN x6 (H33+V35, 6 groups) + oval: all frames")
env, obs = make_l5()
for i in range(6):
    click(env, 33, RC[i]); click(env, 35, RC[i])
result = click(env, 58, 58)
print(f"  Total frames: {len(result.frame)}  levels={result.levels_completed}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if 3<=r<=31 and c>=32]
    ry = sorted(set(r for r,c in yc)) if yc else []
    cy = sorted(set(c for r,c in yc)) if yc else []
    print(f"  [f{i}] rows={ry} cols={cy}")
if result.levels_completed > 4 or len(result.frame) > 8:
    print("  *** POSSIBLE WIN ***")
