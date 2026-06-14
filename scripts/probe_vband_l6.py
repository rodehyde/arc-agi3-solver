"""ar25 L6: move the vertical (L-R) band left/right and render to see the reflection."""
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
L3 = [5] + [4]*7 + [2]*7 + [5] + [3]*12 + [2]*5 + [5] + [1]*7
L4 = [5] + [4]*7 + [5] + [1]*7 + [4]*7 + [5] + [2]*6
L5 = [5, 5] + [1]*7 + [3]*10 + [5] + [2]*4 + [5] + [4]*5
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2 + L3 + L4 + L5:
        r = env.step(A[a], data={})
    return env, r


def vband(g):
    m = (g == 10); m[63, :] = False; m[:, 63] = False
    cols = [x for x in range(64) if m[:, x].sum() > 30]
    return (min(cols), max(cols)) if cols else None


panels = []
env, r = fresh(); panels.append(("start (vband col 22)", grid(r), r.levels_completed))
# enter state 1 (vband control): ACTION5 x1; ACTION3 = left
for k in [2, 4, 6]:
    env, r = fresh()
    r = env.step(A[5], data={})        # -> state 1
    for _ in range(k):
        r = env.step(A[3], data={})    # left
    g = grid(r)
    panels.append((f"vband LEFT x{k} -> cols {vband(g)} lvl={r.levels_completed}", g, r.levels_completed))

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, len(panels), figsize=(7*len(panels), 7))
for ax, (t, gg, lv) in zip(axs, panels):
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 6)); ax.set_yticks(range(0, 64, 6))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t, fontsize=9)
plt.savefig("scripts/l6_vband.png", dpi=60, bbox_inches='tight')
print("saved scripts/l6_vband.png")
for t, _, lv in panels:
    print(" ", t)
