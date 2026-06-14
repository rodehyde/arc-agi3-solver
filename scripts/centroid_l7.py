"""ar25 L7: the centroid trick. Centroid of yellow = crossing of its symmetry axes.
Test V/H mirror + 180-rotation symmetry about the centroid."""
import logging
import numpy as np
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
L6 = ([5,5,5] + [2]*12 + [3]*7 + [5,5,5] + [2]*4 + [3]*15 + [5,5] + [2]*11 + [5] + [3]*1)
PRE = L1 + L2 + L3 + L4 + L5 + L6


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in PRE:
    r = env.step(A[a], data={})
g = grid(r)
Y = (g == 11); Y[:, 63] = False
ys, xs = np.where(Y)
Yc = set(zip(ys.tolist(), xs.tolist()))
cy, cx = ys.mean(), xs.mean()
print(f"yellow cells={len(Yc)}  centroid=(row {cy:.3f}, col {cx:.3f})")


def vmatch(axis_col):
    a2 = 2*axis_col
    m = sum(1 for (r2, c2) in Yc if (r2, a2-c2) in Yc)
    return m/len(Yc)


def hmatch(axis_row):
    a2 = 2*axis_row
    m = sum(1 for (r2, c2) in Yc if (a2-r2, c2) in Yc)
    return m/len(Yc)


def rot180(cr, cc):
    a2r, a2c = 2*cr, 2*cc
    m = sum(1 for (r2, c2) in Yc if (a2r-r2, a2c-c2) in Yc)
    return m/len(Yc)


# test exact integer axes nearest centroid (cells are 0..63; an axis through cell
# centres is integer; through a boundary is half-integer)
for ac in [round(cx), round(cx*2)/2]:
    print(f"  V mirror about col {ac}: match {vmatch(ac):.3f}")
for ar in [round(cy), round(cy*2)/2]:
    print(f"  H mirror about row {ar}: match {hmatch(ar):.3f}")
print(f"  180-rotation about centroid (row {round(cy)}, col {round(cx)}): match {rot180(round(cy), round(cx)):.3f}")
print(f"  180-rotation about (row {cy:.1f}, col {cx:.1f} -> nearest .5): "
      f"{rot180(round(cy*2)/2, round(cx*2)/2):.3f}")
