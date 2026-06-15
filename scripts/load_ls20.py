"""ls20: load level 1 and dump ASCII + image."""
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

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ls20")
r = env.observation_space
g = np.array(r.frame[-1])

print(f"levels_completed={r.levels_completed} win_levels={r.win_levels} state={r.state.name}")
print(f"available_actions={r.available_actions}")
print(f"grid shape={g.shape}")

bg = int(np.bincount(g.flatten()).argmax())
print(f"background colour={bg}")

print("\nASCII (hex, bg='.'):")
for y in range(g.shape[0]):
    row = g[y]
    if np.all(row == bg): continue
    print(f"{y:2d} " + ''.join('.' if v == bg else format(int(v), 'x') for v in row))

cmap = ListedColormap(PALETTE)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
ax.set_xticks(range(0, 64, 4)); ax.set_yticks(range(0, 64, 4))
ax.grid(True, color='#888', linewidth=0.3)
ax.set_title(f"ls20 level {r.levels_completed+1}")
plt.savefig("scripts/ls20_l1.png", dpi=80, bbox_inches='tight')
print("saved scripts/ls20_l1.png")
