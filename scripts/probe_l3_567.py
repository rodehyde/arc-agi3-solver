"""ar25 L3: characterise ACTION5/6/7 in detail, both modes."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6,
     7: GameAction.ACTION7}
PRIOR = {1: [2]*10 + [3]*5, 2: [3, 3, 5, 2, 2, 2, 2, 2, 2, 2, 2]}


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for lvl in sorted(PRIOR):
        for a in PRIOR[lvl]:
            r = env.step(A[a], data={})
    return env, r


def diff(before, after):
    d = before != after
    if not d.any():
        return "no change"
    ys, xs = np.where(d)
    trans = {}
    for y, x in zip(ys, xs):
        k = (int(before[y, x]), int(after[y, x]))
        trans[k] = trans.get(k, 0) + 1
    ts = ", ".join(f"{a}->{b}:{n}" for (a, b), n in sorted(trans.items()))
    return f"{d.sum()} cells, rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}; {ts}"


# Reference cells (from L3 scene): black piece ~ (25,13); yellow ~ (4,36); divider ~ (49,30); empty ~ (18,5)
CLICKS = {"black_piece(25,13)": (13, 25), "yellow(4,36)": (36, 4),
          "divider(49,30)": (30, 49), "empty(18,5)": (5, 18), "white_dot(49,1)": (1, 49)}

for mode, pre in [("Mode-A (start)", []), ("Mode-B (after A5)", [5])]:
    print(f"\n===== {mode} =====")
    # ACTION5
    env, r = fresh()
    for p in pre:
        r = env.step(A[p], data={})
    b = grid(r); avail = r.available_actions
    r2 = env.step(A[5], data={})
    print(f"ACTION5: {diff(b, grid(r2))}  avail {avail}->{r2.available_actions}")
    # ACTION7
    env, r = fresh()
    for p in pre:
        r = env.step(A[p], data={})
    b = grid(r)
    r2 = env.step(A[7], data={})
    print(f"ACTION7: {diff(b, grid(r2))}")
    # ACTION6 clicks
    for name, (x, y) in CLICKS.items():
        env, r = fresh()
        for p in pre:
            r = env.step(A[p], data={})
        b = grid(r); lc = r.levels_completed
        r2 = env.step(A[6], data={"x": x, "y": y})
        comp = "  LEVEL+" if r2.levels_completed > lc else ""
        print(f"ACTION6 click {name}: {diff(b, grid(r2))}{comp}")
