"""ls20 L2: probe all actions, find toggle and target positions visually."""
import logging, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE=['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
         '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]

def fresh_l2():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    for a in L1: r=env.step(a)
    return env, r

def grid(r): return np.array(r.frame[-1])
def ppos(r):
    g=grid(r); ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

def ref_str(r):
    g=grid(r)
    c={}
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return '/'.join(''.join('B' if c[(ri,ci)]==9 else '.' for ci in range(3)) for ri in range(3))

env,r=fresh_l2()
g0=grid(r)
ref0=ref_str(r)
print(f"Start: pos={ppos(r)}  ref={ref0}  levels={r.levels_completed}")
print()

print("Action table (from start):")
for a,name in [(A1,'U'),(A2,'D'),(A3,'L'),(A4,'R')]:
    env2,r2=fresh_l2()
    r2=env2.step(a)
    g2=grid(r2)
    npos=ppos(r2)
    diff=int((g2!=g0).sum())
    ref2=ref_str(r2)
    moved = npos!=ppos(r)
    print(f"  {name}: pos={npos}  moved={moved}  cells_changed={diff}  ref={ref2}")

# BFS reachable positions
from collections import deque
print("\nBFS reachable positions:")
start=ppos(fresh_l2()[1])
visited={start}
queue=deque([([], start)])
positions={start:[]}

while queue:
    path, pos = queue.popleft()
    if len(path)>=12: continue
    for a in [A1,A2,A3,A4]:
        env2,r2=fresh_l2()
        for m in path: r2=env2.step(m)
        r2=env2.step(a)
        npos=ppos(r2)
        if npos and npos!=pos and npos not in visited:
            visited.add(npos)
            queue.append((path+[a], npos))
            positions[npos]=path+[a]

print(f"Total reachable: {len(positions)}")
for pos in sorted(positions.keys()):
    seq=''.join(ANAMES[a] for a in positions[pos])
    print(f"  {pos} via {seq}")

# Check which positions change the ref
print("\nPositions that change ref:")
ref0_raw=ref_str(fresh_l2()[1])
for pos, seq in positions.items():
    env2,r2=fresh_l2()
    for a in seq: r2=env2.step(a)
    r2_ref=ref_str(r2)
    if r2_ref != ref0_raw:
        print(f"  {pos}: ref={r2_ref}")

# Check target position: source says rjlbuycveu at (14,40)
# At pos (14,40): player top-left col=14, row=40
print("\nTest target position (14,40):")
if (14,40) in positions:
    env2,r2=fresh_l2()
    for a in positions[(14,40)]: r2=env2.step(a)
    print(f"  levels={r2.levels_completed}  ref={ref_str(r2)}")
else:
    print("  Not reachable with current rotation")

# Save image
cmap=ListedColormap(PALETTE)
env,r=fresh_l2(); g=grid(r)
fig,ax=plt.subplots(figsize=(10,10))
ax.imshow(g,cmap=cmap,vmin=0,vmax=15)
ax.set_title("ls20 Level 2")
ax.set_xticks(range(0,64,5)); ax.set_yticks(range(0,64,5))
ax.grid(True,color='#aaa',linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_l2_map.png",dpi=80)
print("\nsaved scripts/ls20_l2_map.png")
