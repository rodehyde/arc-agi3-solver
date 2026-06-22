"""tn36 L5 — Zone 3 (58,35) frame-by-frame detailed inspection."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]

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

env, obs = make_l5()
g_before = np.array(obs.frame[-1])

result = env.step(GameAction.ACTION6, {'x': 35, 'y': 58})
print(f"Zone 3 click: {len(result.frame)} frames\n")

frames = [g_before] + [np.array(f) for f in result.frame]

for i in range(len(result.frame)):
    g0 = frames[i]
    g1 = frames[i+1]
    changed = np.argwhere(g0 != g1)
    label = f"f{i-1}->f{i}" if i > 0 else f"before->f0"
    print(f"=== {label}: {len(changed)} cells changed ===")
    if len(changed) == 0:
        print("  (no change)")
        continue
    # Group by transition type
    trans = {}
    for r,c in changed:
        k = (int(g0[r,c]), int(g1[r,c]))
        trans.setdefault(k, []).append((int(r),int(c)))
    for (v0,v1), cells in sorted(trans.items()):
        print(f"  {v0}->{v1} ({len(cells)} cells): {cells[:8]}{'...' if len(cells)>8 else ''}")

# Show full left panel piece shape in each frame
print("\n=== Left piece shape per frame (rows 14-21, cols 12-19) ===")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    print(f"\nf{i}:")
    for r in range(14, 22):
        row = ''.join(CMAP.get(int(g[r,c]),'?') for c in range(12,20))
        print(f"  r{r}: {row}")

# Show right panel in each frame
print("\n=== Right panel piece (yellow=11) per frame ===")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if c>=32 and 3<=r<=31]
    if yc:
        rs = sorted(set(r for r,c in yc)); cs = sorted(set(c for r,c in yc))
        print(f"  f{i}: rows={rs} cols={cs} n={len(yc)}")
    else:
        print(f"  f{i}: no yellow in right panel")
