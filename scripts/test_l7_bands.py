"""ar25 L7: do the bands reflect the YELLOW? Move both bands onto the figure axes
(vband->col37, hband->row22) WITHOUT moving black, and render + check win."""
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
L6 = ([5,5,5] + [2]*12 + [3]*7 + [5,5,5] + [2]*4 + [3]*15 + [5,5] + [2]*11 + [5] + [3]*1)
PRE = L1 + L2 + L3 + L4 + L5 + L6
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in PRE:
        r = env.step(A[a], data={})
    return env, r


# vband col10->37: right 9 (state1 A4). hband row16->22: down 2 (state0 A2).
SEQ = [5] + [4]*9 + [5, 5, 5] + [2]*2   # state0->1 (vband right9); 1->...->0 (hband down2)
# cycle 0->1->2->3->0 ; after state1 do 3 A5 to reach state0
env, r = fresh()
g_before = grid(r)
for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 7:
        print(f">>> LEVEL 7 COMPLETE after {i}")
        break
print(f"after bands-to-axes: levels={r.levels_completed}/{r.win_levels}")

g = grid(r)
vals, counts = np.unique(g, return_counts=True)
print("colours now:", {int(v): int(c) for v, c in zip(vals, counts) if v not in (9,)})

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], g, "after bands->axes")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l7_bands.png", dpi=70, bbox_inches='tight')
print("saved scripts/l7_bands.png")
