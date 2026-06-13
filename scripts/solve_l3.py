"""ar25 L3: in Mode-B, search translation that best maps black footprint onto yellow, then execute."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
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


env, r = fresh()
g = grid(r)
g[63, :] = -1
g[:, 63] = -1
black = set(zip(*np.where(g == 5)))
yellow = set(zip(*np.where(g == 11)))
print(f"black cells={len(black)} yellow cells={len(yellow)}")

# search offsets in multiples of 3
best = None
for dy in range(-60, 61, 3):
    for dx in range(-60, 61, 3):
        shifted = {(y+dy, x+dx) for (y, x) in black}
        overlap = len(shifted & yellow)
        if best is None or overlap > best[0]:
            best = (overlap, dy, dx)
print(f"best overlap={best[0]} at dy={best[1]} dx={best[2]} (of {len(black)} black cells)")

# build action sequence in Mode-B: A5 to enter Mode-B, then moves
ov, dy, dx = best
seq = [5]
seq += [2]*(dy//3) if dy > 0 else [1]*(-dy//3)   # ACTION2 down(+), ACTION1 up(-)
seq += [4]*(dx//3) if dx > 0 else [3]*(-dx//3)   # ACTION4 right(+), ACTION3 left(-)
print(f"sequence (action nums): {seq}")

env, r = fresh()
for i, a in enumerate(seq, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 3:
        print(f"  >>> LEVEL 3 COMPLETED after {i} actions")
        break
print(f"end: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
