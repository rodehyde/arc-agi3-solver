"""ls20 L1: visual states — piece in various positions, understand slot/target."""
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
def do(env, acts):
    r = env.observation_space
    for a in acts:
        r = env.step(a)
    return r

A1, A2, A3, A4 = GameAction.ACTION1, GameAction.ACTION2, GameAction.ACTION3, GameAction.ACTION4

cmap = ListedColormap(PALETTE)

# Generate key states
states = [
    ("start",        []),
    ("up1",          [A1]),
    ("up3",          [A1,A1,A1]),
    ("up6_top",      [A1]*6),
    ("left1_up6",    [A3,A1,A1,A1,A1,A1,A1]),   # align with slot then rise
    ("left1_up3",    [A3,A1,A1,A1]),              # in slot partway
    ("left2_up3",    [A3,A3,A1,A1,A1]),           # further left
]

fig, axes = plt.subplots(3, 3, figsize=(21, 21))
for ax, (label, moves) in zip(axes.flat, states):
    env, r = fresh()
    r2 = do(env, moves)
    g = grid(r2)
    ax.imshow(g, cmap=cmap, vmin=0, vmax=15)
    ax.set_title(label)
    ax.set_xticks(range(0,64,8)); ax.set_yticks(range(0,64,8))
    ax.grid(True, color='#888', linewidth=0.3)
    # mark orange bbox
    ys,xs = np.where(g==12)
    if len(ys): ax.plot([xs.min()-0.5,xs.max()+0.5,xs.max()+0.5,xs.min()-0.5,xs.min()-0.5],
                       [ys.min()-0.5,ys.min()-0.5,ys.max()+0.5,ys.max()+0.5,ys.min()-0.5], 'r-', lw=2)

# leave remaining axes blank
for ax in axes.flat[len(states):]:
    ax.axis('off')

plt.tight_layout()
plt.savefig("scripts/ls20_states.png", dpi=80, bbox_inches='tight')
print("saved scripts/ls20_states.png")

# Also print what's in the slot (cols 29-33) for each state, to find where piece passes through
print("\nSlot column contents (cols 29-38) for key states:")
for label, moves in states:
    env, r = fresh()
    r2 = do(env, moves)
    g = grid(r2)
    ys,xs = np.where(g==12)
    if len(ys):
        obbox = (int(ys.min()),int(xs.min()),int(ys.max()),int(xs.max()))
    else:
        obbox = None
    print(f"  {label}: orange_bbox={obbox}")

# Check if ACTION2 IS down: move piece up 3, then apply ACTION2
print("\nTest ACTION2 as DOWN: after up3, apply A2 x5:")
env, r = fresh()
for _ in range(3): r = env.step(A1)
g = grid(r)
ys,xs = np.where(g==12)
print(f"  after up3: orange_bbox=({ys.min()},{xs.min()},{ys.max()},{xs.max()})")
for i in range(5):
    r = env.step(A2)
    g = grid(r)
    ys,xs = np.where(g==12)
    print(f"  A2 step {i+1}: orange_bbox=({ys.min()},{xs.min()},{ys.max()},{xs.max()})")
