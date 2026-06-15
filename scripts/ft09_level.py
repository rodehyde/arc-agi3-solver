"""ft09: replay known per-level click solutions, then render + ASCII-dump the current level."""
import sys
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE = ['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
           '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']

# per-level solutions as lists of (x,y) ACTION6 clicks
SOLUTIONS = {
    1: [(38, 38), (38, 46), (54, 46), (38, 54)],
    2: [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)],
    3: [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
        (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)],
    4: [(15, 17), (23, 17), (23, 17), (31, 17), (47, 17), (15, 25), (31, 25),
        (47, 25), (15, 33), (23, 33), (23, 33), (31, 33), (39, 33), (23, 41),
        (39, 41), (23, 49), (23, 49), (31, 49), (31, 49), (39, 49), (39, 49)],
    5: [(25, 15), (25, 31), (41, 47), (33, 7), (17, 23), (33, 23), (49, 23),
        (17, 39), (33, 39), (49, 39), (17, 55), (33, 55), (25, 7), (17, 15),
        (33, 15), (17, 31), (33, 31), (41, 39), (33, 47), (49, 47), (41, 55)],
    6: [(7, 9), (7, 17), (23, 17), (39, 17), (15, 25), (23, 25),
        (15, 33), (31, 33), (39, 33), (47, 33), (23, 41), (47, 41), (55, 41)],
}


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 2  # level to reach/inspect
for lvl in range(1, TARGET):
    for (x, y) in SOLUTIONS.get(lvl, []):
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
print(f"now at level {r.levels_completed+1} (levels_completed={r.levels_completed}) state={r.state.name}")
g = grid(r)
bg = 5
print("ASCII (hex, '.'=black):")
for y in range(g.shape[0]):
    row = g[y]
    if np.all(row == bg):
        continue
    print(f"{y:2d} " + ''.join('.' if v == bg else format(int(v), 'x') for v in row))

# locate vdk-grey (4) framed region
ys, xs = np.where(g == 4)
if len(ys):
    print(f"\nframe(4) bbox rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")

cmap = ListedColormap(PALETTE)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
ax.grid(True, color='#888', linewidth=0.3); ax.set_title(f"ft09 level {r.levels_completed+1}")
plt.savefig("scripts/ft09_level.png", dpi=80, bbox_inches='tight')
print("saved scripts/ft09_level.png")
