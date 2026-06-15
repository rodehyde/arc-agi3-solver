"""ls20 L1: inspect what happens when piece covers the white cross."""
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

# Navigate to (30,19): LLLUUU from start
# LLL = left3 to (45,19), UUU = up3 to (30,19)
env,r=fresh()
g0=grid(r).copy()

# Confirm cross position at start
print("Cross area at start (rows 29-35, cols 18-25):")
for row in range(29,35):
    vals=list(g0[row,18:26])
    print(f"  row {row}: {vals}")

# Navigate to (30,19)
for _ in range(3): r=env.step(A3)  # LLL → (45,19)
for _ in range(3): r=env.step(A1)  # UUU → (30,19)
g1=grid(r)
ys,xs=np.where(g1==12); ob=(int(ys.min()),int(xs.min()))
print(f"\nAt position: orange_top_left={ob}")
print(f"levels_completed={r.levels_completed} state={r.state.name}")
print(f"available_actions={r.available_actions}")

print("\nCross area when piece at (30,19) (rows 29-35, cols 18-25):")
for row in range(29,35):
    vals=list(g1[row,18:26])
    print(f"  row {row}: {vals}")

# Did anything change in the cross cells?
cross_cells=[(31,21),(32,20),(32,21),(32,22),(33,21)]
print("\nCross cell values before vs during overlap:")
for r_,c_ in cross_cells:
    print(f"  ({r_},{c_}): before={g0[r_,c_]}  during={g1[r_,c_]}")

# Now move away and check if cross changed
env2,r2=fresh()
for _ in range(3): r2=env2.step(A3)
for _ in range(3): r2=env2.step(A1)
r2=env2.step(A4)  # move right away from cross
g2=grid(r2)
ys,xs=np.where(g2==12); ob2=(int(ys.min()),int(xs.min()))
print(f"\nAfter moving right from cross pos: orange_top_left={ob2}")
print("\nCross cell values AFTER moving away:")
for r_,c_ in cross_cells:
    print(f"  ({r_},{c_}): after={g2[r_,c_]}")

# Also test: does pressing each action FROM (30,19) win or change available_actions?
print("\nPress each action from (30,19):")
for act,name in [(A1,'U'),(A2,'D'),(A3,'L'),(A4,'R')]:
    env3,r3=fresh()
    for _ in range(3): r3=env3.step(A3)
    for _ in range(3): r3=env3.step(A1)
    r3=env3.step(act)
    g3=grid(r3)
    ys,xs=np.where(g3==12); ob3=(int(ys.min()),int(xs.min()))
    diff=(g3!=g1).sum()
    print(f"  {name}: pos={ob3}  cells_changed={diff}  levels={r3.levels_completed}  avail={r3.available_actions}")

# Save image at cross overlap
cmap=ListedColormap(PALETTE)
fig,axes=plt.subplots(1,2,figsize=(16,8))
axes[0].imshow(g0,cmap=cmap,vmin=0,vmax=15)
axes[0].set_title("start"); axes[0].grid(True,color='#888',linewidth=0.3)
axes[0].set_xticks(range(0,64,4)); axes[0].set_yticks(range(0,64,4))
axes[1].imshow(g1,cmap=cmap,vmin=0,vmax=15)
axes[1].set_title("piece at (30,19) — over cross"); axes[1].grid(True,color='#888',linewidth=0.3)
axes[1].set_xticks(range(0,64,4)); axes[1].set_yticks(range(0,64,4))
plt.tight_layout()
plt.savefig("scripts/ls20_cross.png",dpi=80,bbox_inches='tight')
print("\nsaved scripts/ls20_cross.png")
