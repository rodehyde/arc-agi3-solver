"""ft09 L2 action table: probe ACTION6 on distinct targets (from a fresh replay to L2 each time)."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]


def grid(f):
    return np.array(f.frame[-1])


def to_l2():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in L1:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


def diff(g0, g1):
    ch = np.argwhere(g0 != g1)
    trans = {}
    for (y, x) in ch:
        k = f"{g0[y,x]}->{g1[y,x]}"
        trans[k] = trans.get(k, 0) + 1
    bbox = None
    if len(ch):
        ys, xs = ch[:, 0], ch[:, 1]
        bbox = (int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max()))
    return len(ch), trans, bbox


targets = [
    ("blue tile (top-left of block)", 22, 16),
    ("blue tile (middle col, row1)", 30, 16),
    ("key1 tile center", 30, 24),
    ("key2 tile center", 30, 40),
    ("grey background", 8, 8),
    ("legend blue (top-right)", 61, 2),
    ("legend orange (top-right)", 61, 6),
]
for name, x, y in targets:
    env, r = to_l2()
    g0 = grid(r)
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    n, trans, bbox = diff(g0, grid(r))
    print(f"click {name:32s}(x{x:2d},y{y:2d}): cells={n:3d} bbox={bbox} trans={trans} "
          f"lvl={r.levels_completed}")
