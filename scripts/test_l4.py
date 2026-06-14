"""ar25 L4 test: assemble A+B on upper trident, drop band to axis."""
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
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']

SEQ = [5] + [4]*7 + [5] + [1]*7 + [4]*7 + [5] + [2]*6


def grid(f):
    return np.array(f.frame[-1])


def interior(g, v):
    m = (g == v); m[63, :] = False; m[:, 63] = False
    return m


def comps(g, v=5):
    m = interior(g, v); seen = np.zeros_like(m, dtype=bool); out = []
    H, W = m.shape
    for sy in range(H):
        for sx in range(W):
            if m[sy, sx] and not seen[sy, sx]:
                st = [(sy, sx)]; seen[sy, sx] = True; cs = []
                while st:
                    y, x = st.pop(); cs.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx]=True; st.append((ny,nx))
                ys=[c[0] for c in cs]; xs=[c[1] for c in cs]
                out.append((min(ys),min(xs),len(cs)))
    return sorted(out)


def band(g):
    ys, _ = np.where(interior(g, 10))
    return (int(ys.min()), int(ys.max())) if len(ys) else None


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3:
    r = env.step(A[a], data={})
g_before = grid(r)
print(f"L4 start levels={r.levels_completed} black={comps(g_before)} band={band(g_before)}")

for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 4:
        print(f">>> LEVEL 4 COMPLETE after {i} actions (planned {len(SEQ)})")
        break
print(f"after: levels={r.levels_completed}/{r.win_levels} black={comps(grid(r))} band={band(grid(r))}")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l4_test.png", dpi=70, bbox_inches='tight')
print("saved scripts/l4_test.png")
