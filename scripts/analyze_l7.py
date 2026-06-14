"""ar25 L7: find yellow's true symmetry axes, box-count, run 4-fold orbit search for piece placement.
Also confirm ACTION6 is just the object-selector (gate)."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
L3 = [5] + [4]*7 + [2]*7 + [5] + [3]*12 + [2]*5 + [5] + [1]*7
L4 = [5] + [4]*7 + [5] + [1]*7 + [4]*7 + [5] + [2]*6
L5 = [5, 5] + [1]*7 + [3]*10 + [5] + [2]*4 + [5] + [4]*5
L6 = ([5,5,5] + [2]*12 + [3]*7 + [5,5,5] + [2]*4 + [3]*15 + [5,5] + [2]*11 + [5] + [3]*1)
PRE = L1 + L2 + L3 + L4 + L5 + L6


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in PRE:
        r = env.step(A[a], data={})
    return env, r


def boxset(mask):
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


env, r = fresh()
g = grid(r)
Y = (g == 11); Y[:, 63] = False
Yc = set(zip(*np.where(Y)))
ys = [p[0] for p in Yc]; xs = [p[1] for p in Yc]
print(f"yellow cells={len(Yc)} rows {min(ys)}-{max(ys)} cols {min(xs)}-{max(xs)}")


def vaxis_search():
    best = []
    for ax2 in range(2*min(xs), 2*max(xs)+1):
        m = t = 0
        for (rr, cc) in Yc:
            t += 1
            mc = ax2 - cc
            if (rr, mc) in Yc: m += 1
        best.append((ax2/2, m/t))
    return sorted(best, key=lambda z: -z[1])[:4]


def haxis_search():
    best = []
    for ax2 in range(2*min(ys), 2*max(ys)+1):
        m = t = 0
        for (rr, cc) in Yc:
            t += 1
            mr = ax2 - rr
            if (mr, cc) in Yc: m += 1
        best.append((ax2/2, m/t))
    return sorted(best, key=lambda z: -z[1])[:4]


print("best vertical axes (col):", [(f'{a:.1f}', f'{f:.3f}') for a, f in vaxis_search()])
print("best horizontal axes (row):", [(f'{a:.1f}', f'{f:.3f}') for a, f in haxis_search()])

# box counts
B = (g == 5); B[63, :] = False
Yb = boxset(Y)
# split pieces: right zigzag comp tl (39,51); left blob tl (48,15)
right = B.copy(); right[:, :40] = False   # cols>=40 -> right zigzag
left = B.copy(); left[:, 40:] = False      # cols<40 -> left blob
print(f"\nyellow boxes={len(Yb)}  right-piece boxes={len(boxset(right))}  left-piece boxes={len(boxset(left))}")
print(f"sum pieces boxes={len(boxset(right))+len(boxset(left))}")

# quick ACTION6 gate check: click each piece / band / empty in state 0
def click(x, y, s=0):
    e, rr = fresh()
    for _ in range(s):
        rr = e.step(A[5], data={})
    g0 = grid(rr)
    rr = e.step(A[6], data={"x": x, "y": y})
    d = (g0 != grid(rr)); d[:, 63] = False
    return int(d.sum())
print("\nACTION6 gate (state 0): click rightpiece=%d leftpiece=%d band=%d yellow=%d empty=%d" % (
    click(55, 45), click(22, 53), click(10, 30), click(33, 33), click(60, 25)))
