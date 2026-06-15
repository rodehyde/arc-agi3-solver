"""Print before/after of clicking pink-cross at (1,2)."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]
L4 = [(15, 17), (23, 17), (23, 17), (31, 17), (47, 17), (15, 25), (31, 25),
      (47, 25), (15, 33), (23, 33), (23, 33), (31, 33), (39, 33), (23, 41),
      (39, 41), (23, 49), (23, 49), (31, 49), (31, 49), (39, 49), (39, 49)]
PRE = L1 + L2 + L3 + L4

ROW_STARTS = [4, 12, 20, 28, 36, 44, 52]
COL_STARTS = [6, 14, 22, 30, 38, 46, 54]
NAMES = {14: 'grn', 15: 'pur', 4: '...'}


def tile_center(ri, ci):
    return (COL_STARTS[ci] + 3, ROW_STARTS[ri] + 3)


def grid(r):
    return np.array(r.frame[-1])


def slot_colour(g, ri, ci):
    rs, cs = ROW_STARTS[ri], COL_STARTS[ci]
    blk = g[rs:rs+6, cs:cs+6]
    vals = blk[blk != 4]
    if len(vals) == 0:
        return None
    v, c = np.unique(vals, return_counts=True)
    return int(v[np.argmax(c)])


def to_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


env, r = to_l5()
g0 = grid(r)

cx, cy = tile_center(1, 2)
r2 = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r2)

print("Effect of clicking pink-cross at slot (1,2):")
print("Slot      before  after")
for ri in range(7):
    for ci in range(7):
        rs, cs = ROW_STARTS[ri], COL_STARTS[ci]
        blk0 = g0[rs:rs+6, cs:cs+6]
        blk1 = g1[rs:rs+6, cs:cs+6]
        if np.all(blk0 == 4):
            continue
        changed = not np.array_equal(blk0, blk1)
        c0 = slot_colour(g0, ri, ci)
        c1 = slot_colour(g1, ri, ci)
        marker = " <-- CHANGED" if changed else ""
        print(f"  ({ri},{ci})      {NAMES.get(c0,c0)!s:6s}  {NAMES.get(c1,c1)!s:6s}{marker}")
