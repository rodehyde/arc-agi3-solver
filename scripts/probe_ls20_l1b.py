"""ls20 L1: detailed probe — track orange+blue stack position after each action."""
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

def piece_bbox(g, colour):
    ys, xs = np.where(g == colour)
    if len(ys) == 0: return None
    return (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()))

def piece_info(g):
    ob = piece_bbox(g, 12)  # orange
    bb = piece_bbox(g, 9)   # blue
    wb = piece_bbox(g, 0)   # white
    return f"orange={ob}  blue={bb}  white={wb}"

# Baseline
env, r = fresh()
g0 = grid(r)
print(f"Start: {piece_info(g0)}")

# Apply each action and see full sequence of moves
actions = [
    ('ACTION1', GameAction.ACTION1),
    ('ACTION2', GameAction.ACTION2),
    ('ACTION3', GameAction.ACTION3),
    ('ACTION4', GameAction.ACTION4),
]

for name, act in actions:
    env, r = fresh()
    g_prev = grid(r).copy()
    print(f"\n{name} sequence (10 steps):")
    for i in range(10):
        r = env.step(act)
        g = grid(r)
        info = piece_info(g)
        changed = (g != g_prev).sum()
        print(f"  step {i+1}: {info}  cells_changed={changed}")
        g_prev = g.copy()
        if r.levels_completed >= 1:
            print(f"  *** LEVEL COMPLETE at step {i+1} ***")
            break

# Save 4 images showing state after each action once
fig, axes = plt.subplots(2, 2, figsize=(16, 16))
cmap = ListedColormap(PALETTE)
act_list = [GameAction.ACTION1, GameAction.ACTION2, GameAction.ACTION3, GameAction.ACTION4]
act_names = ['ACTION1','ACTION2','ACTION3','ACTION4']
for ax, act, aname in zip(axes.flat, act_list, act_names):
    env2, r2 = fresh()
    r2 = env2.step(act)
    g2 = grid(r2)
    ax.imshow(g2, cmap=cmap, vmin=0, vmax=15)
    ax.set_title(aname)
    ax.set_xticks(range(0,64,8)); ax.set_yticks(range(0,64,8))
    ax.grid(True, color='#888', linewidth=0.3)
plt.tight_layout()
plt.savefig("scripts/ls20_actions.png", dpi=80, bbox_inches='tight')
print("\nsaved scripts/ls20_actions.png")
