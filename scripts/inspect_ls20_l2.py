"""ls20 L2: full scene inspection — every object, its colour, size, and position."""
import logging, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE=['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
         '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']
COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
             6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
             12:'orange',13:'maroon',14:'green',15:'purple'}

A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make("ls20")
r=env.observation_space
for a in L1: r=env.step(a)

# Get ALL layers
print(f"Number of layers: {len(r.frame)}")
for li, layer in enumerate(r.frame):
    g=np.array(layer)
    unique=np.unique(g)
    print(f"  Layer {li}: unique values={unique}")

# Work with the top (visible) layer
g=np.array(r.frame[-1])
print(f"\nFull grid shape: {g.shape}")
print(f"Levels completed: {r.levels_completed}")
print(f"Available actions: {r.available_actions}")

# Dominant background
from collections import Counter
counts=Counter(g.flatten().tolist())
print(f"\nColour distribution (top 8):")
for v,cnt in counts.most_common(8):
    print(f"  {v} ({COLOR_NAMES.get(v,'?')}): {cnt} cells")

# All non-background-ish colours: identify every object
# Background seems to be vdk-grey(4) based on L1 inspection
BG={4}  # vdk-grey is the background

print(f"\n--- ALL OBJECTS (non-background colours) ---")
from collections import defaultdict
by_color=defaultdict(list)
for row in range(64):
    for col in range(64):
        v=int(g[row,col])
        if v not in BG:
            by_color[v].append((row,col))

for v in sorted(by_color.keys()):
    cells=by_color[v]
    rows=[r_ for r_,c_ in cells]
    cols=[c_ for r_,c_ in cells]
    print(f"\nColour {v} ({COLOR_NAMES.get(v,'?')}): {len(cells)} cells")
    print(f"  Row range: {min(rows)}–{max(rows)}   Col range: {min(cols)}–{max(cols)}")
    # Show the shape as a grid snippet
    rmin,rmax=min(rows),max(rows)
    cmin,cmax=min(cols),max(cols)
    print(f"  Bounding box: rows {rmin}-{rmax}, cols {cmin}-{cmax} ({rmax-rmin+1}×{cmax-cmin+1})")
    # Print a compact map of just this colour
    for row in range(rmin,rmax+1):
        line=''.join('X' if (row,col) in set(cells) else '.' for col in range(cmin,cmax+1))
        print(f"    row{row:2d}: {line}")
    if rmax-rmin>20:
        print("  (large region — first few and last few rows shown above)")

# Extra: print raw grid in blocks to see structure
print("\n--- RAW GRID (by region, bg=4 shown as ' ', walls=5 as '#') ---")
def show_region(label, r0,r1,c0,c1):
    print(f"\n{label} rows {r0}-{r1}, cols {c0}-{c1}:")
    for row in range(r0,r1+1):
        line=''
        for col in range(c0,c1+1):
            v=int(g[row,col])
            if v==4: line+=' '
            elif v==5: line+='#'
            elif v==12: line+='O'  # orange player
            elif v==9: line+='B'   # blue player
            elif v==11: line+='Y'  # yellow
            elif v==10: line+='b'  # lt-blue
            elif v==8: line+='R'   # red
            elif v==0: line+='W'   # white
            elif v==3: line+='d'   # dk-grey
            else: line+=str(v)
        print(f"  {row:2d}: {line}")

show_region("TOP LEFT",0,20,0,30)
show_region("TOP RIGHT",0,20,30,63)
show_region("MIDDLE LEFT",20,45,0,30)
show_region("MIDDLE RIGHT",20,45,30,63)
show_region("BOTTOM",45,63,0,63)

# Save labelled image
fig,ax=plt.subplots(figsize=(12,12))
cmap=ListedColormap(PALETTE)
ax.imshow(g,cmap=cmap,vmin=0,vmax=15)
ax.set_title("ls20 Level 2 — full scene")
ax.set_xticks(range(0,64,5))
ax.set_yticks(range(0,64,5))
ax.set_xticklabels(range(0,64,5),fontsize=7)
ax.set_yticklabels(range(0,64,5),fontsize=7)
ax.grid(True,color='#ccc',linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_l2_inspect.png",dpi=100)
print("\nSaved: scripts/ls20_l2_inspect.png")
