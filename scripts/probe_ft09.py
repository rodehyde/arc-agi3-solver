"""ft09 L1: probe ACTION6 click on a framed-grid blue tile to see what it does."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)


def grid(f):
    return np.array(f.frame[-1])


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


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
g0 = grid(r)

# framed grid tile (0,0) center ~ (col 38, row 38)
for name, x, y in [("framed(0,0) blue tile", 38, 38),
                   ("framed center key", 47, 46),
                   ("unframed TL red tile", 14, 4)]:
    arcade2 = Arcade(operation_mode=OperationMode.OFFLINE)
    e2 = arcade2.make("ft09")
    rr = e2.observation_space
    b = grid(rr)
    rr = e2.step(GameAction.ACTION6, data={"x": x, "y": y})
    n, trans, bbox = diff(b, grid(rr))
    print(f"click {name:24s}(x{x},y{y}): cells={n} bbox={bbox} trans={trans} "
          f"levels={rr.levels_completed} avail={rr.available_actions}")
