"""ft09 L5: map exactly which tile-slots change when a pink-cross is clicked."""
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


def tile_center(ri, ci):
    return (COL_STARTS[ci] + 3, ROW_STARTS[ri] + 3)


def grid(r):
    return np.array(r.frame[-1])


def slot_of(row, col):
    for ri, rs in enumerate(ROW_STARTS):
        if rs <= row < rs + 6:
            for ci, cs in enumerate(COL_STARTS):
                if cs <= col < cs + 6:
                    return (ri, ci)
    return None


def to_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


# Click pink-cross at (ri=1, ci=2) and map which slots changed
env, r = to_l5()
g0 = grid(r).copy()
cx, cy = tile_center(1, 2)
r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r)
diff = g0 != g1
print(f"Total cells changed: {diff.sum()}")

changed_slots = {}
ys, xs = np.where(diff)
for yy, xx in zip(ys, xs):
    s = slot_of(yy, xx)
    if s:
        changed_slots[s] = changed_slots.get(s, 0) + 1

print("Changed slots:")
for s in sorted(changed_slots):
    print(f"  slot {s}: {changed_slots[s]} cells  centre={int(g0[ROW_STARTS[s[0]]+2, COL_STARTS[s[1]]+2])}->",
          int(g1[ROW_STARTS[s[0]]+2, COL_STARTS[s[1]]+2]))

# Also: what does clicking the OTHER pink-cross at (ri=3, ci=2) change?
print()
env, r = to_l5()
g0 = grid(r).copy()
cx, cy = tile_center(3, 2)
r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r)
diff = g0 != g1
print(f"Pink-cross (3,2): {diff.sum()} cells changed")
changed_slots = {}
ys, xs = np.where(diff)
for yy, xx in zip(ys, xs):
    s = slot_of(yy, xx)
    if s:
        changed_slots[s] = changed_slots.get(s, 0) + 1
print("Changed slots:")
for s in sorted(changed_slots):
    print(f"  slot {s}: {changed_slots[s]} cells")

# And the third pink-cross at (ri=5, ci=4)
print()
env, r = to_l5()
g0 = grid(r).copy()
cx, cy = tile_center(5, 4)
r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r)
diff = g0 != g1
print(f"Pink-cross (5,4): {diff.sum()} cells changed")
changed_slots = {}
ys, xs = np.where(diff)
for yy, xx in zip(ys, xs):
    s = slot_of(yy, xx)
    if s:
        changed_slots[s] = changed_slots.get(s, 0) + 1
print("Changed slots:")
for s in sorted(changed_slots):
    print(f"  slot {s}: {changed_slots[s]} cells")
