"""ar25 L6: box-level matching. Convert yellow + each black piece to 3x3-box occupancy,
then find each piece's shift so its boxes land on yellow boxes (covering one quadrant)."""
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


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3 + L4 + L5:
    r = env.step(A[a], data={})
g = grid(r)


def boxset(mask):
    """boxes (br,bc) on a grid aligned to multiples of 3, present if block intersects mask."""
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


Y = (g == 11); Y[:, 63] = False
Yb = boxset(Y)
print(f"yellow boxes={len(Yb)}")

B = (g == 5); B[63, :] = False
upper = B.copy(); upper[24:, :] = False
lower = B.copy(); lower[:24, :] = False
Ub, Lb = boxset(upper), boxset(lower)
print(f"upper boxes={len(Ub)} lower boxes={len(Lb)} sum={len(Ub)+len(Lb)}")

# quadrant box-sets (axis col 19 between box-cols 18 and 21? boxes are at multiples of 3:
#   cols 3..18 are LEFT of axis 19; cols 21..33 are RIGHT)
#   rows 9..33 ABOVE row 34; rows 36..59 BELOW
def quad(rowsel, colsel):
    return {(br, bc) for (br, bc) in Yb if rowsel(br) and colsel(bc)}

QTL = quad(lambda r: r < 34, lambda c: c < 19)
QTR = quad(lambda r: r < 34, lambda c: c > 19)
QBL = quad(lambda r: r > 34, lambda c: c < 19)
QBR = quad(lambda r: r > 34, lambda c: c > 19)
print(f"quadrant boxes: TL={len(QTL)} TR={len(QTR)} BL={len(QBL)} BR={len(QBR)}")


def best_shift_to(boxes, target):
    best = None
    for dy in range(-60, 61, 3):
        for dx in range(-60, 61, 3):
            sh = {(r+dy, c+dx) for (r, c) in boxes}
            on = len(sh & target); off = len(sh - target)
            if best is None or (on - 3*off) > (best[1] - 3*best[2]):
                best = (None, on, off, dy, dx)
    return best


for qn, Q in [("TL", QTL), ("TR", QTR), ("BL", QBL), ("BR", QBR)]:
    # try to cover Q with upper+lower; report each piece's best fit into Q
    _, uon, uoff, udy, udx = best_shift_to(Ub, Q)
    _, lon, loff, ldy, ldx = best_shift_to(Lb, Q)
    print(f"\nquadrant {qn}: upper fit on={uon}/{len(Ub)} off={uoff} (dy={udy},dx={udx})"
          f"  lower fit on={lon}/{len(Lb)} off={loff} (dy={ldy},dx={ldx})")
