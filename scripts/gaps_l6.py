"""ar25 L6: compute the right-side gaps that make yellow L-R symmetric about col 22,
and render them next to the black pieces to find the placement."""
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


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3 + L4 + L5:
    r = env.step(A[a], data={})
g = grid(r)

Y = (g == 11); Y[:, 63] = False
axis = 22
Ymir = np.zeros_like(Y)
for rr in range(64):
    for cc in range(64):
        mc = 2*axis - cc
        if 0 <= mc < 64 and Y[rr, cc]:
            Ymir[rr, mc] = True

# cells needed on the RIGHT to mirror left = Ymir present, Y absent, on right side
right_gap = Ymir & (~Y)
right_gap_r = right_gap.copy(); right_gap_r[:, :axis+1] = False  # only right of axis
left_gap = Y & (~Ymir)  # left cells with no right partner (should equal mirror of right_gap)

print(f"right-side gap cells (to be filled): {right_gap_r.sum()}")
ys, xs = np.where(right_gap_r)
if len(ys):
    print(f"  bbox rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")
print("\nRIGHT-GAP ASCII (G=needed):")
if len(ys):
    for rr in range(ys.min(), ys.max()+1):
        line = ''.join('G' if right_gap_r[rr, cc] else '.' for cc in range(xs.min(), xs.max()+1))
        print(f"{rr:2d} {line}")

# Show black pieces footprint as solid 3x3 (fill holes) to compare shapes
B = (g == 5); B[63, :] = False
print("\nBLACK (solid view, B):")
bys, bxs = np.where(B)
for rr in range(bys.min(), bys.max()+1):
    line = ''.join('B' if B[rr, cc] else '.' for cc in range(bxs.min(), bxs.max()+1))
    print(f"{rr:2d} {line}")
