"""ls20 L1: test lateral entry into slot; enumerate reachable positions from start."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE = ['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
           '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']

A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r

def grid(r): return np.array(r.frame[-1])
def obbox(g):
    ys,xs=np.where(g==12)
    return (int(ys.min()),int(xs.min())) if len(ys) else None

# BFS to enumerate all distinct orange positions reachable from start
from collections import deque

print("BFS over reachable orange positions:")
env,r=fresh()
g0=grid(r)
start_pos=obbox(g0)
visited={start_pos}
queue=deque([([], start_pos)])
positions={}  # pos -> shortest action sequence

while queue:
    path, pos = queue.popleft()
    if pos not in positions:
        positions[pos]=path
    if len(path)>=10: continue
    for act, name in [(A1,'U'),(A2,'D'),(A3,'L'),(A4,'R')]:
        env2,r2=fresh()
        for a in path:
            env2.step(a if isinstance(a,GameAction) else [A1,A2,A3,A4][['U','D','L','R'].index(a)])
        r2=env2.step(act)
        g=grid(r2)
        npos=obbox(g)
        if npos and npos not in visited:
            visited.add(npos)
            queue.append((path+[act], npos))

print(f"Total distinct orange top-left positions: {len(positions)}")
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}
for pos in sorted(positions.keys()):
    seq=''.join(ANAMES[a] for a in positions[pos])
    print(f"  {pos} via {seq}")

# Now test: up3 then left to see if piece enters slot
print("\nTest UP3 then LEFT actions:")
for nleft in range(1,5):
    env2,r2=fresh()
    for _ in range(3): r2=env2.step(A1)
    for _ in range(nleft): r2=env2.step(A3)
    g=grid(r2)
    pos=obbox(g)
    print(f"  up3 + left{nleft}: orange_top_left={pos}")

# Also: save images for a few combos including up3+left1
combos=[
    ("up3_then_L1",[A1,A1,A1,A3]),
    ("up3_then_L2",[A1,A1,A1,A3,A3]),
    ("up6_then_L1",[A1,A1,A1,A1,A1,A1,A3]),
]
cmap=ListedColormap(PALETTE)
fig,axes=plt.subplots(1,3,figsize=(21,8))
for ax,(label,moves) in zip(axes,combos):
    env2,r2=fresh()
    for a in moves: r2=env2.step(a)
    g=grid(r2)
    ax.imshow(g,cmap=cmap,vmin=0,vmax=15)
    ax.set_title(label)
    ax.set_xticks(range(0,64,8)); ax.set_yticks(range(0,64,8))
    ax.grid(True,color='#888',linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_combos.png",dpi=80,bbox_inches='tight')
print("saved scripts/ls20_combos.png")
