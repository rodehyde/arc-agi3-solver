"""ar25 L2: test whether ACTION5 toggles horizontal-only -> vertical-enabled control."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 7: GameAction.ACTION7}
L1 = [2]*10 + [3]*5


def grid(f):
    return np.array(f.frame[-1])


def bbox(g, val):
    ys, xs = np.where(g == val)
    return None if len(ys) == 0 else (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()))


def fresh_at_l2():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1:
        r = env.step(A[a], data={})
    return env, r


def vdk(g):
    return bbox(g, 4)


# Probe: ACTION5 then each direction
print("baseline vdk-grey(4) bbox at L2 start:")
env, r = fresh_at_l2()
print(" ", vdk(grid(r)))

for pre in [[], [5], [5, 5]]:
    for n in [1, 2, 3, 4]:
        env, r = fresh_at_l2()
        for p in pre:
            r = env.step(A[p], data={})
        before = vdk(grid(r))
        r = env.step(A[n], data={})
        after = vdk(grid(r))
        dy = after[0] - before[0] if before and after else None
        dx = after[1] - before[1] if before and after else None
        pre_s = "+".join(f"A5" for _ in pre) or "none"
        print(f"  pre=[{pre_s}] then ACTION{n}: vdk dy={dy:+d} dx={dx:+d}" if dy is not None else f"  pre=[{pre_s}] ACTION{n}: lost shape")
