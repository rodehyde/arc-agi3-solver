"""ls20 L2: load and inspect the scene."""
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

# L1 solution
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make("ls20")
r=env.observation_space
for a in L1: r=env.step(a)

g=np.array(r.frame[-1])
print(f"Level: {r.levels_completed}, state: {r.state.name}, avail: {r.available_actions}")

# Find player piece
ys,xs=np.where(g==12); px,py=int(xs.min()),int(ys.min())
print(f"Player (orange) top-left: x={px}, y={py}  (col={px}, row={py})")
print(f"Player occupies rows {py}-{py+4}, cols {px}-{px+4}")

# Scan entire grid for non-background cells (exclude bg=4, walls=5, player=12, player=9)
print("\nNon-background special cells in play area:")
special={}
for row in range(0,64):
    for col in range(0,64):
        v=int(g[row,col])
        if v not in (3,4,5,12,9):
            special[(row,col)]=v

# Group by colour
from collections import defaultdict
by_color=defaultdict(list)
for (r_,c_),v in special.items():
    by_color[v].append((r_,c_))

COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',6:'pink',7:'lt-pink',8:'red',
             10:'lt-blue',11:'yellow',13:'maroon',14:'green',15:'purple'}
for v,cells in sorted(by_color.items()):
    print(f"  color {v} ({COLOR_NAMES.get(v,'?')}): {len(cells)} cells — {cells[:8]}{'...' if len(cells)>8 else ''}")

# Reference box (bottom-left)
print("\nRef box (rows 55-60, cols 3-8) — current rotation state:")
for row in range(54,62):
    vals=[int(g[row,c]) for c in range(2,10)]
    print(f"  row {row}: {vals}")

# Top box (target display, rows 9-15)
print("\nTop box (rows 9-15, cols 33-39) — target state:")
for row in range(9,16):
    vals=[int(g[row,c]) for c in range(33,40)]
    print(f"  row {row}: {vals}")

# Print key zone around player
print(f"\nGrid rows {py-5}-{py+10}, cols {px-5}-{px+10}:")
for row in range(max(0,py-5), min(64,py+10)):
    vals=[int(g[row,c]) for c in range(max(0,px-5), min(64,px+10))]
    print(f"  row {row}: {vals}")

# Save image
cmap=ListedColormap(PALETTE)
fig,ax=plt.subplots(figsize=(10,10))
ax.imshow(g,cmap=cmap,vmin=0,vmax=15)
ax.set_title("ls20 Level 2 start")
ax.set_xticks(range(0,64,5)); ax.set_yticks(range(0,64,5))
ax.grid(True,color='#888',linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_l2_start.png",dpi=80)
print("\nsaved scripts/ls20_l2_start.png")
