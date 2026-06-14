"""ar25 L7: find the row for the horizontal mirror giving top/bottom symmetry of the YELLOW.
Report match fraction per row and whether the row contains yellow squares."""
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
Yc = set(zip(*np.where(Y)))
rows_with_yellow = sorted({rr for (rr, cc) in Yc})

print("row : topbottom-match : has-yellow")
results = []
for ar in range(8, 56):
    a2 = 2*ar
    m = sum(1 for (rr, cc) in Yc if (a2-rr, cc) in Yc)
    results.append((m/len(Yc), ar, ar in rows_with_yellow))
for frac, ar, hasy in sorted(results, key=lambda z: -z[0])[:8]:
    print(f" {ar:3d} :   {frac:.3f}        : {'YES' if hasy else 'no'}")
print("\nrows containing yellow:", rows_with_yellow)
