"""ar25 L6: find the vertical axis about which the yellow figure is most symmetric."""
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
Y = (g == 11); Y[:, 63] = False
ys, xs = np.where(Y)
print(f"yellow cols {xs.min()}-{xs.max()} rows {ys.min()}-{ys.max()} total {Y.sum()}")

print("\nVertical-axis symmetry search (axis col -> match fraction of yellow):")
results = []
for ax2 in range(2*5, 2*45):           # 2*axis col, half-integer allowed
    match = 0; tot = 0
    for rr in range(64):
        for cc in range(64):
            if Y[rr, cc]:
                tot += 1
                mc = ax2 - cc
                if 0 <= mc < 64 and Y[rr, mc]:
                    match += 1
    results.append((ax2/2, match/tot))
results.sort(key=lambda t: -t[1])
for axc, frac in results[:8]:
    print(f"  axis col {axc:5.1f}: match {frac:.3f}")

# also report symmetry specifically at the band columns of interest
for axc in [12, 22]:
    match = 0; tot = 0
    for rr in range(64):
        for cc in range(64):
            if Y[rr, cc]:
                tot += 1
                mc = 2*axc - cc
                if 0 <= mc < 64 and Y[rr, mc]:
                    match += 1
    print(f"  [check] axis col {axc}: match {match/tot:.3f}")
