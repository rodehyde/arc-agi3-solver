"""ar25 L6 solution: place upper & lower so their 4-fold orbits tile the figure,
then move bands onto axes (vband col19, hband row34)."""
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


# states: 0=hband 1=vband 2=lower 3=upper ; cycle 0->1->2->3->0
# upper: down12 left7 ; lower: down4 left15 ; hband down11 ; vband left1
SEQ = []
SEQ += [5, 5, 5]                 # 0->3 upper
SEQ += [2]*12 + [3]*7
SEQ += [5, 5, 5]                 # 3->2 lower (3->0->1->2)
SEQ += [2]*4 + [3]*15
SEQ += [5, 5]                    # 2->0 hband (2->3->0)
SEQ += [2]*11
SEQ += [5]                       # 0->1 vband
SEQ += [3]*1
print(f"sequence length={len(SEQ)}")

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3 + L4 + L5:
    r = env.step(A[a], data={})
g_before = grid(r)
print(f"L6 start levels={r.levels_completed}")

for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 6:
        print(f">>> LEVEL 6 COMPLETE after {i} actions (planned {len(SEQ)})")
        break
print(f"after: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l6_test_v2.png", dpi=70, bbox_inches='tight')
print("saved scripts/l6_test_v2.png")
