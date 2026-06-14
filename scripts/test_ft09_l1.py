"""ft09 L1 test: click the 4 framed-grid tiles the center key marks white, expect level complete."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
print(f"start levels={r.levels_completed}/{r.win_levels}")

CLICKS = [(38, 38), (38, 46), (54, 46), (38, 54)]  # (x,y) for key-white tiles
for i, (x, y) in enumerate(CLICKS, 1):
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    print(f"click {i} (x{x},y{y}): levels={r.levels_completed} state={r.state.name} avail={r.available_actions}")
    if r.levels_completed >= 1:
        print(f">>> LEVEL 1 COMPLETE after {i} clicks")
        break
