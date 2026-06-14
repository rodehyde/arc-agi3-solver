"""ar25 L7: replay to level 7, describe + render the scene."""
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
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']
COLOR = {0: 'white', 1: 'lt-grey', 2: 'md-grey', 3: 'dk-grey', 4: 'vdk-grey',
         5: 'black', 6: 'pink', 7: 'lt-pink', 8: 'red', 9: 'blue', 10: 'lt-blue',
         11: 'yellow', 12: 'orange', 13: 'maroon', 14: 'green', 15: 'purple'}


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3 + L4 + L5 + L6:
    r = env.step(A[a], data={})
print(f"levels_completed={r.levels_completed} state={r.state.name}")
print(f"available_actions={r.available_actions}")
g = grid(r)

vals, counts = np.unique(g, return_counts=True)
bg = vals[np.argmax(counts)]
print(f"\ngrid {g.shape}, background={bg} ({COLOR.get(bg)})")
for v, c in sorted(zip(vals, counts), key=lambda x: -x[1]):
    if v == bg:
        print(f"   {v:2d} {COLOR.get(v,'?'):8s}: {c} cells (BG)")
        continue
    ys, xs = np.where(g == v)
    print(f"   {v:2d} {COLOR.get(v,'?'):8s}: {c:4d} cells  rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")

print("\nASCII (hex per cell, '.'=bg):")
for y in range(g.shape[0]):
    row = g[y]
    if np.all(row == bg):
        continue
    print(f"{y:2d} " + ''.join('.' if v == bg else format(int(v), 'x') for v in row))

cmap = ListedColormap(PALETTE)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
ax.grid(True, color='#888', linewidth=0.3); ax.set_title("ar25 Level 7 start")
plt.savefig("scripts/l7_start.png", dpi=80, bbox_inches='tight')
print("\nsaved scripts/l7_start.png")
