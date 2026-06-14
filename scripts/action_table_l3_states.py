"""ar25 L3: full action table across all 3 control states (ACTION5 cycles 0->1->2->0).

For each state s in {0,1,2} and each simple action, report per-colour bbox shift
so we can see which object each action controls in each state.
"""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 7: GameAction.ACTION7}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
COLOR = {0: 'white', 4: 'vdk-grey', 5: 'black', 9: 'blue', 10: 'lt-blue', 11: 'yellow', 12: 'orange'}
TRACK = [5, 10, 4, 11, 12]  # colours whose movement we care about


def grid(f):
    return np.array(f.frame[-1])


def fresh(n_state):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2:
        r = env.step(A[a], data={})
    for _ in range(n_state):
        r = env.step(A[5], data={})   # advance control state
    return env, r


def bbox(g, v):
    ys, xs = np.where(g == v)
    if len(ys) == 0:
        return None
    return (int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max()), len(ys))


def shift(b0, b1):
    if b0 is None or b1 is None:
        return f"{b0}->{b1}"
    dy, dx = b1[0]-b0[0], b1[2]-b0[2]
    dcount = b1[4]-b0[4]
    if dy == 0 and dx == 0 and dcount == 0:
        return "-"
    return f"dy={dy} dx={dx} dcount={dcount}"


for s in range(3):
    print("=" * 72)
    print(f"CONTROL STATE {s}  (reached by ACTION5 x{s})")
    print("=" * 72)
    for a in [1, 2, 3, 4, 7]:
        env, r = fresh(s)
        g0 = grid(r)
        r = env.step(A[a], data={})
        g1 = grid(r)
        n = int((g0 != g1).sum())
        parts = []
        for v in TRACK:
            sh = shift(bbox(g0, v), bbox(g1, v))
            if sh != "-":
                parts.append(f"{COLOR[v]}:{sh}")
        moved = "  ".join(parts) if parts else "(no tracked-colour shift)"
        print(f"  ACTION{a}: cells={n:4d}  {moved}")
    print()
