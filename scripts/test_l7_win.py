"""ar25 L7: place pieces onto the figure (reflections on-grid) + bands at centroid (22,37).
Probe: does covering yellow with black, with bands at the centroid, win?"""
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


def run(seq, label):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in PRE:
        r = env.step(A[a], data={})
    g_before = grid(r)
    won = None
    for i, a in enumerate(seq, 1):
        r = env.step(A[a], data={})
        if r.levels_completed >= 7:
            won = i; break
    print(f"[{label}] win={'YES @'+str(won) if won else 'no'} levels={r.levels_completed}")
    return g_before, grid(r), r.levels_completed


# states 0=hband 1=vband 2=right 3=left ; cycle 0->1->2->3->0
# left piece up14 right2 ; right piece up8 left7 ; hband down2 ; vband right9
SEQ = ([5,5,5] + [1]*14 + [4]*2        # state3 left
       + [5,5,5] + [1]*8 + [3]*7       # state2 right
       + [5,5] + [2]*2                 # state0 hband down2
       + [5] + [4]*9)                  # state1 vband right9
gb, ga, lv = run(SEQ, "pieces-on-figure + bands@centroid")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], gb, "before"), (axs[1], ga, "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l7_win.png", dpi=70, bbox_inches='tight')
print("saved scripts/l7_win.png")
