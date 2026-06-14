"""ar25 L4: probe ACTION6 click vs each distinct target, each state."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {5: GameAction.ACTION5, 6: GameAction.ACTION6}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
L3 = [5] + [4]*7 + [2]*7 + [5] + [3]*12 + [2]*5 + [5] + [1]*7
from arcengine import GameAction as G
A.update({1: G.ACTION1, 2: G.ACTION2, 3: G.ACTION3, 4: G.ACTION4})
TARGETS = [("blackA", 13, 22), ("blackB", 19, 38), ("band", 20, 10),
           ("yellow-upper", 40, 22), ("empty", 5, 55)]


def grid(f):
    return np.array(f.frame[-1])


def fresh(s):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2 + L3:
        r = env.step(A[a], data={})
    for _ in range(s):
        r = env.step(A[5], data={})
    return env, r


for s in range(3):
    print(f"== STATE {s} clicks ==")
    for name, x, y in TARGETS:
        env, r = fresh(s)
        g0 = grid(r)
        r = env.step(A[6], data={"x": x, "y": y})
        g1 = grid(r)
        d = (g0 != g1); d[:, 63] = False
        print(f"  click {name:14s}(x{x},y{y}): cells={int(d.sum())}")
