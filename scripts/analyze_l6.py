"""ar25 L6: analyse yellow symmetry and black-piece shapes to locate gaps."""
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

Y = (g == 11)
Y[:, 63] = False  # drop right border
B = (g == 5)
B[63, :] = False

# vertical band center = col 22
axis = 22
print("Yellow L-R symmetry about col 22 — cells present on right but missing mirror on left (and vice versa):")
asym = []
for rr in range(64):
    for cc in range(64):
        if Y[rr, cc]:
            mc = 2*axis - cc
            if 0 <= mc < 64 and not Y[rr, mc]:
                asym.append((rr, cc))
print(f"  asymmetric yellow cells about col {axis}: {len(asym)}")
if asym:
    ys = [a[0] for a in asym]; xs = [a[1] for a in asym]
    print(f"  bbox of asymmetry: rows {min(ys)}-{max(ys)} cols {min(xs)}-{max(xs)}")

# yellow extent each side
ys, xs = np.where(Y)
print(f"\nyellow rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}, total {Y.sum()} cells")
left = Y[:, :axis].sum(); right = Y[:, axis+1:].sum()
print(f"yellow left-of-axis={left}  right-of-axis={right}")

# Try horizontal symmetry: find axis row r0 maximizing match within cols 3-41
print("\nHorizontal-symmetry search for yellow (best mirror row):")
best = None
for r0x2 in range(2*9, 2*63):  # 2*axis_row
    match = 0; tot = 0
    for rr in range(64):
        mr = r0x2 - rr
        if 0 <= mr < 64:
            for cc in range(64):
                if Y[rr, cc]:
                    tot += 1
                    if Y[mr, cc]:
                        match += 1
    if tot and (best is None or match/tot > best[1]):
        best = (r0x2/2, match/tot, tot)
print(f"  best mirror row ~{best[0]} with match fraction {best[1]:.3f}")

# Black pieces bbox
print("\nBlack cells bbox:", end=" ")
bys, bxs = np.where(B)
print(f"rows {bys.min()}-{bys.max()} cols {bxs.min()}-{bxs.max()} total {B.sum()}")
print("\nBlack ASCII (B=black):")
for rr in range(bys.min(), bys.max()+1):
    line = ''.join('B' if B[rr, cc] else '.' for cc in range(bxs.min(), bxs.max()+1))
    print(f"{rr:2d} {line}")
