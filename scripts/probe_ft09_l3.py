"""ft09 L3 action table: what does clicking a RED tile do (once/twice/thrice)? keys? bg?"""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]


def grid(f):
    return np.array(f.frame[-1])


def to_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in L1 + L2:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


def trans(g0, g1):
    ch = np.argwhere(g0 != g1)
    t = {}
    for (y, x) in ch:
        k = f"{g0[y,x]}->{g1[y,x]}"
        t[k] = t.get(k, 0) + 1
    return {k: v for k, v in t.items() if not k.startswith('12->')}  # hide counter


# click a red tile N times at same spot
for n in (1, 2, 3, 4):
    env, r = to_l3()
    g0 = grid(r)
    for _ in range(n):
        r = env.step(GameAction.ACTION6, data={"x": 22, "y": 6})  # red tile top
    print(f"red tile clicked x{n}: {trans(g0, grid(r))}")

# click keys and bg
for name, x, y in [("keyA(orange c)", 30, 14), ("keyB(red c)", 22, 30),
                   ("keyC(red c)", 38, 30), ("keyD(orange c)", 30, 46), ("bg", 5, 5)]:
    env, r = to_l3()
    g0 = grid(r)
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    print(f"click {name:16s}(x{x},y{y}): {trans(g0, grid(r))}")
