"""Step 4 test: ar25 L2 = (Mode H) 2x LEFT[A3], toggle[A5], (Mode V) 8x DOWN[A2]."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5, 2, 2, 2, 2, 2, 2, 2, 2]   # 2xLEFT(H), toggle, 8xDOWN(V)


def grid(f):
    return np.array(f.frame[-1])


def bbox(g, v):
    ys, xs = np.where(g == v)
    return None if len(ys) == 0 else (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()))


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1:
    r = env.step(A[a], data={})
print(f"at L2 start: vdk(4)={bbox(grid(r),4)} target yellow expected top-left (42,3)")
print(f"             levels={r.levels_completed}/{r.win_levels}")

for i, a in enumerate(L2, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 2:
        print(f"  >>> LEVEL 2 COMPLETED after {i} actions (last={A[a].name})")
        break

print(f"end: vdk(4)={bbox(grid(r),4)} levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
