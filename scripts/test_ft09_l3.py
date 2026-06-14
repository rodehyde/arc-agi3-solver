"""ft09 L3 test: click the 14 tiles that should be orange (per the 4 keys), expect L3 complete."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
for (x, y) in L1 + L2:
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
print(f"at L3: levels={r.levels_completed}")
for i, (x, y) in enumerate(L3, 1):
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    if r.levels_completed >= 3:
        print(f">>> LEVEL 3 COMPLETE after {i} clicks")
        break
print(f"end: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
