"""ar25 L7: print box-shapes of the two pieces and the existing/gap blocks for direct comparison."""
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


def boxgrid(mask):
    bg = {}
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                bg[(br//3, bc//3)] = 1
    return bg


def show(bg, title):
    if not bg:
        print(title, "(empty)"); return
    rs = [k[0] for k in bg]; cs = [k[1] for k in bg]
    print(f"{title}  box-rows {min(rs)}-{max(rs)} box-cols {min(cs)}-{max(cs)}  ({len(bg)} boxes)")
    for br in range(min(rs), max(rs)+1):
        print("   " + ''.join('#' if (br, bc) in bg else '.' for bc in range(min(cs), max(cs)+1)))


B = (g == 5); B[63, :] = False
right = B.copy(); right[:, :40] = False
left = B.copy(); left[:, 40:] = False
show(boxgrid(right), "RIGHT piece")
show(boxgrid(left), "LEFT piece")

Y = (g == 11); Y[:, 63] = False
show(boxgrid(Y), "YELLOW figure")
