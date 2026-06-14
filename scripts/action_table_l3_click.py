"""ar25 L3: probe ACTION6 (click) against every distinct target, in each control state."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6, 7: GameAction.ACTION7}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8

# (name, x=col, y=row)
TARGETS = [
    ("blackL-center", 17, 26),
    ("blackR-center", 50, 29),
    ("ltblue-band", 20, 49),
    ("yellow-top-pedestal", 14, 11),
    ("yellow-center-divider", 34, 25),
    ("empty-bg", 5, 5),
]


def grid(f):
    return np.array(f.frame[-1])


def fresh(n_state):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2:
        r = env.step(A[a], data={})
    for _ in range(n_state):
        r = env.step(A[5], data={})
    return env, r


def diff(g0, g1):
    changed = np.argwhere(g0 != g1)
    trans = {}
    for (y, x) in changed:
        # exclude counter cells on right border col 63
        if x == 63:
            continue
        k = f"{g0[y,x]}->{g1[y,x]}"
        trans[k] = trans.get(k, 0) + 1
    return len(changed), trans


for s in range(3):
    print(f"==== STATE {s} : ACTION6 clicks ====")
    for name, x, y in TARGETS:
        env, r = fresh(s)
        g0 = grid(r)
        r = env.step(A[6], data={"x": x, "y": y})
        g1 = grid(r)
        n, trans = diff(g0, g1)
        print(f"  click {name:24s} (x={x:2d},y={y:2d}): cells={n:4d} trans={trans}")
    print()
