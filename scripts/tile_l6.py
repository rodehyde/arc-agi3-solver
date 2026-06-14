"""ar25 L6: search for quadrant + (upper shift, lower shift) that disjointly tile it.
Also try: do the two pieces tile a HALF (left or right, 26 boxes) or the WHOLE figure?"""
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
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
upper = B.copy(); upper[24:, :] = False
lower = B.copy(); lower[:24, :] = False
Yb, Ub, Lb = boxset(Y), boxset(upper), boxset(lower)

# regions to try to tile with upper+lower
regions = {}
regions['Q-TL'] = {b for b in Yb if b[0] < 34 and b[1] < 19}
regions['Q-TR'] = {b for b in Yb if b[0] < 34 and b[1] > 19}
regions['Q-BL'] = {b for b in Yb if b[0] > 34 and b[1] < 19}
regions['Q-BR'] = {b for b in Yb if b[0] > 34 and b[1] > 19}
regions['H-left'] = {b for b in Yb if b[1] < 19}
regions['H-right'] = {b for b in Yb if b[1] > 19}
regions['V-top'] = {b for b in Yb if b[0] < 34}
regions['V-bot'] = {b for b in Yb if b[0] > 34}
regions['WHOLE'] = Yb

shifts = [(dy, dx) for dy in range(-60, 61, 3) for dx in range(-60, 61, 3)]
for name, R in regions.items():
    found = None
    for udy, udx in shifts:
        up = {(r2+udy, c2+udx) for (r2, c2) in Ub}
        if not up <= R:
            continue
        need = R - up
        if len(need) != len(Lb):
            continue
        for ldy, ldx in shifts:
            lo = {(r2+ldy, c2+ldx) for (r2, c2) in Lb}
            if lo == need:
                found = (udy, udx, ldy, ldx)
                break
        if found:
            break
    print(f"{name} ({len(R)} boxes): {'TILED by ' + str(found) if found else 'no exact tiling'}")
