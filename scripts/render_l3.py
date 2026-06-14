"""Render ar25 L3 start scene to a PNG for visual inspection."""
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

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2:
    r = env.step(A[a], data={})
g = np.array(r.frame[-1])
cmap = ListedColormap(PALETTE)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
ax.grid(True, color='#888', linewidth=0.3)
ax.set_title("ar25 Level 3 start")
plt.savefig("scripts/l3_start.png", dpi=80, bbox_inches='tight')
print("saved scripts/l3_start.png")
