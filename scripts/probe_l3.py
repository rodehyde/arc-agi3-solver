"""ar25 L3: mask borders (row 63, col 63) and report what each object actually does."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
PRIOR = {1: [2]*10 + [3]*5, 2: [3, 3, 5, 2, 2, 2, 2, 2, 2, 2, 2]}


def grid(f):
    g = np.array(f.frame[-1])
    g[63, :] = -1   # mask bottom border
    g[:, 63] = -1   # mask counter column
    return g


def bbox(g, v):
    ys, xs = np.where(g == v)
    return None if len(ys) == 0 else (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()), int(len(ys)))


def report(before, after):
    out = []
    for v, name in [(5, "black"), (4, "vdk"), (11, "yellow"), (10, "divider"), (0, "white")]:
        b, a = bbox(before, v), bbox(after, v)
        if b and a and (b[0] != a[0] or b[1] != a[1] or b[4] != a[4]):
            out.append(f"{name}({v}) dy={a[0]-b[0]:+d} dx={a[1]-b[1]:+d} n{b[4]}->{a[4]}")
    return "; ".join(out) if out else "no masked-object movement"


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for lvl in sorted(PRIOR):
        for a in PRIOR[lvl]:
            r = env.step(A[a], data={})
    return env, r


print("L3 masked object bboxes at start:")
_, r0 = fresh()
g0 = grid(r0)
for v, n in [(5, "black"), (11, "yellow"), (10, "divider")]:
    print(f"  {n}({v}): {bbox(g0, v)}")

for pre in [[], [5]]:
    tag = "Mode-A (start)" if not pre else "Mode-B (after A5)"
    print(f"\n--- {tag} ---")
    for n in [1, 2, 3, 4]:
        env, r = fresh()
        for p in pre:
            r = env.step(A[p], data={})
        before = grid(r)
        r = env.step(A[n], data={})
        after = grid(r)
        print(f"  ACTION{n}: {report(before, after)}")
