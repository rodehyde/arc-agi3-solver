"""ar25 L7: print the yellow grid (cells), with row/col labels, for visual symmetry check."""
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
r0, r1, c0, c1 = ys.min(), ys.max(), xs.min(), xs.max()
print(f"yellow bbox rows {r0}-{r1} cols {c0}-{c1}  (centroid row {ys.mean():.1f}, col {xs.mean():.1f})")

# column header
hdr = "    " + "".join(str(c % 10) for c in range(c0, c1+1))
print(hdr)
for rr in range(r0, r1+1):
    line = "".join("#" if Y[rr, cc] else "." for cc in range(c0, c1+1))
    mark = "  <== row 22 (mirror)" if rr == 22 else ""
    print(f"{rr:3d} {line}{mark}")

print("\n--- BOX VIEW (3x3 box = '#' if any yellow) ---")
def boxocc(br, bc):
    return Y[br:br+3, bc:bc+3].any()
br0 = (r0//3)*3; bc0 = (c0//3)*3
print("    " + "".join(str((bc)%10) for bc in range(bc0, c1+1, 3)))
for br in range(br0, r1+1, 3):
    line = "".join("#" if boxocc(br, bc) else "." for bc in range(bc0, c1+1, 3))
    print(f"{br:3d} {line}")
