"""ar25 L3 v2: place both pieces on bottom targets, then raise mirror band to axis (row 28)."""
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

SEQ = ([5] + [4]*7 + [2]*7        # state1: piece L right7, down7
       + [5] + [3]*12 + [2]*5     # state2: piece R left12, down5
       + [5] + [1]*7)             # state0: band up7 to axis


def grid(f):
    return np.array(f.frame[-1])


def ltblue_rows(g):
    ys, _ = np.where(g == 10)
    return (int(ys.min()), int(ys.max())) if len(ys) else None


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2:
    r = env.step(A[a], data={})
g_before = grid(r)
print(f"L3 start: levels={r.levels_completed} band={ltblue_rows(g_before)}")

done_at = None
for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 3 and done_at is None:
        done_at = i
        print(f">>> LEVEL 3 COMPLETE after {i} actions (planned {len(SEQ)})")
        break
print(f"After seq: levels={r.levels_completed}/{r.win_levels} state={r.state.name} band={ltblue_rows(grid(r))}")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l3_test_v2.png", dpi=70, bbox_inches='tight')
print("saved scripts/l3_test_v2.png")
