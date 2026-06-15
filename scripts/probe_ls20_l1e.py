"""ls20 L1: test all 36 reachable positions for win; print exact piece shape."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE=['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
         '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r

def grid(r): return np.array(r.frame[-1])

# All reachable positions and their sequences (from BFS)
POSITIONS = [
    ((15,34),[A1,A1,A1,A1,A1,A1]),
    ((20,34),[A1,A1,A1,A1,A1]),
    ((25,14),[A1,A1,A1,A1,A3,A3,A3,A3]),
    ((25,19),[A1,A1,A1,A1,A3,A3,A3]),
    ((25,24),[A1,A1,A1,A1,A3,A3]),
    ((25,29),[A1,A1,A1,A1,A3]),
    ((25,34),[A1,A1,A1,A1]),
    ((25,39),[A1,A1,A1,A1,A4]),
    ((25,44),[A1,A1,A1,A1,A4,A4]),
    ((25,49),[A1,A1,A1,A1,A4,A4,A4]),
    ((30,14),[A3,A3,A3,A1,A1,A1,A3]),
    ((30,19),[A3,A3,A3,A1,A1,A1]),
    ((30,24),[A1,A1,A1,A1,A3,A3,A2]),
    ((30,34),[A1,A1,A1]),
    ((30,39),[A1,A1,A1,A4]),
    ((30,44),[A1,A1,A1,A4,A4]),
    ((30,49),[A1,A1,A1,A4,A4,A4]),
    ((35,14),[A3,A3,A3,A1,A1,A3]),
    ((35,19),[A3,A3,A3,A1,A1]),
    ((35,24),[A3,A3,A3,A1,A1,A4]),
    ((35,34),[A1,A1]),
    ((35,39),[A1,A1,A4]),
    ((35,44),[A1,A1,A4,A4]),
    ((35,49),[A1,A1,A4,A4,A4]),
    ((40,19),[A3,A3,A3,A1]),
    ((40,34),[A1]),
    ((40,39),[A1,A4]),
    ((40,44),[A1,A4,A4]),
    ((40,49),[A1,A4,A4,A4]),
    ((45,19),[A3,A3,A3]),
    ((45,24),[A3,A3]),
    ((45,29),[A3]),
    ((45,34),[]),
    ((45,39),[A4]),
    ((45,44),[A4,A4]),
    ((45,49),[A4,A4,A4]),
]

print("Testing all reachable positions for win:")
for pos, seq in POSITIONS:
    env,r=fresh()
    for a in seq: r=env.step(a)
    won=(r.levels_completed>=1)
    if won:
        print(f"  {pos} via {len(seq)} moves: *** WIN ***")
    else:
        print(f"  {pos}: no win")

# Print the exact piece shape (what colours are in cols 34-38 at start)
print("\nExact piece columns at start (cols 29-43, rows 43-51):")
env,r=fresh()
g=grid(r)
for row in range(43,52):
    vals=list(g[row,29:44])
    print(f"  row {row}: {vals}")

# Print the top box contents in detail
print("\nTop box interior (rows 9-15, cols 33-39):")
for row in range(9,16):
    vals=list(g[row,33:40])
    print(f"  row {row}: {vals}")

# Print bottom-left box
print("\nBottom-left box interior (rows 54-61, cols 2-9):")
for row in range(54,62):
    vals=list(g[row,2:10])
    print(f"  row {row}: {vals}")

# Save image showing piece at top + bottom detail
cmap=ListedColormap(PALETTE)
env2,r2=fresh()
for _ in range(6): r2=env2.step(A1)
g2=grid(r2)
fig,axes=plt.subplots(1,2,figsize=(14,8))
axes[0].imshow(g2,cmap=cmap,vmin=0,vmax=15)
axes[0].set_title("up6 (piece at top)")
axes[0].set_xticks(range(0,64,4)); axes[0].set_yticks(range(0,64,4))
axes[0].grid(True,color='#888',linewidth=0.3)
# Zoom on top box
axes[1].imshow(g2[6:22,26:44],cmap=cmap,vmin=0,vmax=15)
axes[1].set_title("top box zoom (rows 6-21, cols 26-43)")
axes[1].set_xticks(range(0,18,2)); axes[1].set_yticks(range(0,16,2))
axes[1].grid(True,color='#888',linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_topbox.png",dpi=100,bbox_inches='tight')
print("\nsaved scripts/ls20_topbox.png")
