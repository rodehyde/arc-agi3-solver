"""ft09 L1: load and describe + render the starting scene."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode

logging.basicConfig(level=logging.ERROR)
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']
COLOR = {0: 'white', 1: 'lt-grey', 2: 'md-grey', 3: 'dk-grey', 4: 'vdk-grey',
         5: 'black', 6: 'pink', 7: 'lt-pink', 8: 'red', 9: 'blue', 10: 'lt-blue',
         11: 'yellow', 12: 'orange', 13: 'maroon', 14: 'green', 15: 'purple'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
print(f"win_levels={r.win_levels} baseline={env.info.baseline_actions}")
print(f"available_actions={r.available_actions} state={r.state.name}")
g = np.array(r.frame[-1])
print(f"frame layers={len(r.frame)} grid shape={g.shape}")

vals, counts = np.unique(g, return_counts=True)
bg = vals[np.argmax(counts)]
print(f"\nbackground={bg} ({COLOR.get(bg)})")
for v, c in sorted(zip(vals, counts), key=lambda x: -x[1]):
    ys, xs = np.where(g == v)
    tag = " (BG)" if v == bg else ""
    print(f"   {v:2d} {COLOR.get(v,'?'):8s}: {c:4d} cells  rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}{tag}")

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
ax.grid(True, color='#888', linewidth=0.3); ax.set_title("ft09 Level 1 start")
plt.savefig("scripts/ft09_start.png", dpi=80, bbox_inches='tight')
print("\nsaved scripts/ft09_start.png")
