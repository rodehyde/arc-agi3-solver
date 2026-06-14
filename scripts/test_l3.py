"""ar25 L3 test: overlay each black piece onto its congruent yellow target."""
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

# Proposed L3 sequence (action numbers)
SEQ = ([5] + [4]*7 + [2]*7        # state1: piece L right7, down7
       + [5] + [3]*12 + [2]*5)    # state2: piece R left12, down5


def grid(f):
    return np.array(f.frame[-1])


def interior_mask(g, v):
    m = (g == v)
    m[63, :] = False; m[:, 63] = False
    return m


def black_comps(g):
    m = interior_mask(g, 5)
    seen = np.zeros_like(m, dtype=bool)
    out = []
    H, W = m.shape
    for sy in range(H):
        for sx in range(W):
            if m[sy, sx] and not seen[sy, sx]:
                stack = [(sy, sx)]; seen[sy, sx] = True; cells = []
                while stack:
                    y, x = stack.pop(); cells.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx] = True; stack.append((ny,nx))
                ys=[c[0] for c in cells]; xs=[c[1] for c in cells]
                out.append((min(ys), min(xs), len(cells)))
    return sorted(out)


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2:
    r = env.step(A[a], data={})
print(f"At L3 start: levels={r.levels_completed} comps={black_comps(grid(r))}")
g_before = grid(r)

for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 3:
        print(f">>> LEVEL 3 COMPLETE after {i} actions ({len(SEQ)} planned)")
        break
print(f"After seq: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
print(f"black comps now: {black_comps(grid(r))}")
print("target tl: L=(42,33)  R=(42,9)")

# render before/after
cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l3_test.png", dpi=70, bbox_inches='tight')
print("saved scripts/l3_test.png")
