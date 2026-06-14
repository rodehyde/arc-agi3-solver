"""ar25 L6 test: cover BR quadrant with upper+lower pieces, set bands on axes (col19,row34)."""
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
PALETTE = ['#FFFFFF', '#D3D3D3', '#A9A9A9', '#696969', '#404040', '#000000',
           '#FFC0CB', '#FFB6C1', '#FF0000', '#0000FF', '#ADD8E6', '#FFFF00',
           '#FFA500', '#800000', '#008000', '#800080']


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2 + L3 + L4 + L5:
        r = env.step(A[a], data={})
    return env, r


def boxset(mask):
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


# ---- compute placements ----
env, r = fresh()
g = grid(r)
Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
upper = B.copy(); upper[24:, :] = False
lower = B.copy(); lower[:24, :] = False
Yb, Ub, Lb = boxset(Y), boxset(upper), boxset(lower)
BR = {(br, bc) for (br, bc) in Yb if br > 34 and bc > 19}

# upper -> BR perfect fit found earlier: dy=36 dx=-21
udy, udx = 36, -21
upper_placed = {(r2+udy, c2+udx) for (r2, c2) in Ub}
assert upper_placed <= BR, f"upper not in BR: {upper_placed - BR}"
remaining = BR - upper_placed
print(f"BR boxes={len(BR)} upper covers={len(upper_placed)} remaining for lower={len(remaining)}")

# find lower shift so Lb -> remaining exactly
best = None
for dy in range(-60, 61, 3):
    for dx in range(-60, 61, 3):
        sh = {(r2+dy, c2+dx) for (r2, c2) in Lb}
        if sh == remaining:
            best = (dy, dx); break
    if best:
        break
print(f"lower exact shift to remaining BR boxes: {best}")
ldy, ldx = best if best else (0, 0)

# ---- build sequence ----
# states: 0=hband,1=vband,2=lower,3=upper ; cycle 0->1->2->3->0
def moves(dy, dx):
    seq = []
    seq += [2]*(dy//3) if dy > 0 else [1]*(-dy//3)   # down/up
    seq += [4]*(dx//3) if dx > 0 else [3]*(-dx//3)   # right/left
    return seq

SEQ = []
SEQ += [5, 5, 5]            # state0 -> state3 (upper)
SEQ += moves(udy, udx)
SEQ += [5, 5, 5]            # state3 -> state2 (lower)  (3->0->1->2)
SEQ += moves(ldy, ldx)
SEQ += [5, 5]               # state2 -> state0 (hband)  (2->3->0)
SEQ += [2]*11               # hband down to rows 33-35 (center row 34)
SEQ += [5]                  # state0 -> state1 (vband)
SEQ += [3]*1                # vband left to cols 18-20 (center col 19)

print(f"sequence length={len(SEQ)}")

env, r = fresh()
g_before = grid(r)
done = None
for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 6:
        done = i
        print(f">>> LEVEL 6 COMPLETE after {i} actions")
        break
print(f"after: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], g_before, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l6_test.png", dpi=70, bbox_inches='tight')
print("saved scripts/l6_test.png")
