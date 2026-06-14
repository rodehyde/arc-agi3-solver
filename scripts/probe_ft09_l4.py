"""ft09 L4: probe click cycle on a blue tile (1..4 times) + keys, to learn the colour cycle."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]
PRE = L1 + L2 + L3


def grid(f):
    return np.array(f.frame[-1])


def to_l4():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


def color_at(g, x, y):
    return int(g[y, x])


# click a blue tile repeatedly; report its colour after each click
env, r = to_l4()
seq = [color_at(grid(r), 14, 16)]  # tile (rows14-19, cols12-17) center ~ (14,16)
for k in range(6):
    r = env.step(GameAction.ACTION6, data={"x": 14, "y": 16})
    seq.append(color_at(grid(r), 14, 16))
print(f"blue tile colour after 0..6 clicks: {seq}")

# keys / bg no-op check
for name, x, y in [("key1(orange c)", 22, 24), ("key2(blue c)", 38, 24),
                   ("key3(orange c)", 30, 40), ("bg", 5, 5)]:
    env, r = to_l4()
    g0 = grid(r)
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    print(f"click {name:16s}: changed cells={int((g0!=grid(r)).sum())}")
