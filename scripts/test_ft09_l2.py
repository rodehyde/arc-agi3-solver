"""ft09 L2 test: click the 7 tiles the two keys mark white, expect level 2 complete."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
for (x, y) in L1:
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
print(f"at L2: levels={r.levels_completed}")
for i, (x, y) in enumerate(L2, 1):
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    print(f"click {i} (x{x},y{y}): levels={r.levels_completed} state={r.state.name}")
    if r.levels_completed >= 2:
        print(f">>> LEVEL 2 COMPLETE after {i} clicks")
        break
