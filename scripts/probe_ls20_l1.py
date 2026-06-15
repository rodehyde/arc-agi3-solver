"""ls20 L1: probe all 4 actions — measure full cell changes and player movement."""
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

def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ls20")
    r = env.observation_space
    return env, r

def grid(r): return np.array(r.frame[-1])

def diff_summary(g0, g1):
    diff = np.where(g0 != g1)
    if len(diff[0]) == 0:
        return "NO CHANGE"
    rows, cols = diff[0], diff[1]
    transitions = {}
    for y, x in zip(rows, cols):
        k = (int(g0[y,x]), int(g1[y,x]))
        transitions[k] = transitions.get(k, 0) + 1
    return (f"{len(rows)} cells changed; "
            f"bbox rows {rows.min()}-{rows.max()} cols {cols.min()}-{cols.max()}; "
            f"transitions={transitions}")

# Probe each action once
actions = {
    'ACTION1': GameAction.ACTION1,
    'ACTION2': GameAction.ACTION2,
    'ACTION3': GameAction.ACTION3,
    'ACTION4': GameAction.ACTION4,
}

for name, act in actions.items():
    env, r = fresh()
    g0 = grid(r).copy()
    r2 = env.step(act)
    g1 = grid(r2)
    avail = r2.available_actions
    print(f"{name}: {diff_summary(g0, g1)}  avail={avail}")

# Apply each action 3 times and track player position (white cells)
print("\nPlayer position (white=0 cells) after repeated actions:")
def white_bbox(g):
    ys, xs = np.where(g == 0)
    if len(ys) == 0: return None
    return (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()))

env, r = fresh()
g0 = grid(r).copy()
print(f"  Start: white_bbox={white_bbox(g0)}")
for name, act in actions.items():
    env2, r2 = fresh()
    g = grid(r2).copy()
    for i in range(5):
        r2 = env2.step(act)
        g = grid(r2)
        wb = white_bbox(g)
        if i == 0:
            print(f"  {name} x1: white_bbox={wb}  avail={r2.available_actions}")
    print(f"  {name} x5: white_bbox={wb}")

# Save image after one ACTION1
env, r = fresh()
r = env.step(GameAction.ACTION1)
g = grid(r)
cmap = ListedColormap(PALETTE)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
ax.set_xticks(range(0, 64, 4)); ax.set_yticks(range(0, 64, 4))
ax.grid(True, color='#888', linewidth=0.3)
ax.set_title("ls20 after ACTION1")
plt.savefig("scripts/ls20_after_a1.png", dpi=80, bbox_inches='tight')
print("\nsaved scripts/ls20_after_a1.png")
