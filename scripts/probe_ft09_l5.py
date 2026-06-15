"""ft09 L5: probe the click cycle and verify action effects."""
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


def to_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    assert r.levels_completed == 4, f"Expected L5, got {r.levels_completed+1}"
    return env, r


def color_at(g, x, y):
    return int(g[y, x])


# 1. Click cycle on a plain green tile
print("=== Click cycle on plain green tile at (ri=2, ci=0) ===")
env, r = to_l5()
cx, cy = tile_center(2, 0)
seq = [color_at(grid(r), cx, cy)]
for k in range(5):
    r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
    seq.append(color_at(grid(r), cx, cy))
print(f"  colours after 0..5 clicks: {seq}")

# 2. Click cycle on a key tile (ri=0, ci=1) — does clicking change it?
print("\n=== Click cycle on KEY tile at (ri=0, ci=1) ===")
env, r = to_l5()
cx, cy = tile_center(0, 1)
seq = [color_at(grid(r), cx, cy)]
for k in range(3):
    r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
    seq.append(color_at(grid(r), cx, cy))
print(f"  centre colours after 0..3 clicks: {seq}")

# 3. Click cycle on a pink-cross tile (ri=1, ci=2)
print("\n=== Click cycle on PINK-CROSS tile at (ri=1, ci=2) ===")
env, r = to_l5()
cx, cy = tile_center(1, 2)
g0 = grid(r).copy()
seq = [color_at(grid(r), cx, cy)]
for k in range(5):
    g_before = grid(r).copy()
    r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
    g_after = grid(r)
    changed = int((g_before != g_after).sum())
    seq.append(color_at(g_after, cx, cy))
    if k == 0:
        print(f"  click 1: {changed} cells changed")
        ys, xs = np.where(g_before != g_after)
        if len(ys):
            for yy, xx in zip(ys[:10], xs[:10]):
                print(f"    ({xx},{yy}): {g_before[yy,xx]}->{g_after[yy,xx]}")
print(f"  centre colours after 0..5 clicks: {seq}")

# 4. Click background (empty slot) — no-op check
print("\n=== Background click at (5, 5) ===")
env, r = to_l5()
g0 = grid(r).copy()
r = env.step(GameAction.ACTION6, data={"x": 5, "y": 5})
print(f"  cells changed: {int((g0 != grid(r)).sum())}")

# 5. Available actions check
print("\n=== Available actions ===")
env, r = to_l5()
print(f"  {r.available_actions}")
