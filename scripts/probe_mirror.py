"""ar25 L3: understand the lt-blue band as a mirror. Render several states."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2:
        r = env.step(A[a], data={})
    return env, r


def ltblue_rows(g):
    ys, _ = np.where(g == 10)
    return (int(ys.min()), int(ys.max())) if len(ys) else None


panels = []
# 1: start
env, r = fresh(); panels.append(("start", grid(r)))
# 2-5: band moved up 2,4,6,8 steps (state 0 is default; ACTION1 = up)
for k in [3, 6, 9]:
    env, r = fresh()
    for _ in range(k):
        r = env.step(A[1], data={})
    panels.append((f"band up x{k} rows={ltblue_rows(grid(r))}", grid(r)))

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, len(panels), figsize=(7*len(panels), 7))
for ax, (t, gg) in zip(axs, panels):
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 6)); ax.set_yticks(range(0, 64, 6))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t, fontsize=10)
plt.savefig("scripts/l3_mirror.png", dpi=60, bbox_inches='tight')
print("saved scripts/l3_mirror.png")
for t, _ in panels:
    print(" ", t)
