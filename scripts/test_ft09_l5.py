"""ft09 L5: test hypothesised 21-click solution."""
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


def tc(ri, ci):
    return (COL_STARTS[ci] + 3, ROW_STARTS[ri] + 3)


def grid(r):
    return np.array(r.frame[-1])


# Click sequence for L5
# pink-cross group toggles (each toggles itself + 4 orthogonal slot-neighbours)
pink_cross_clicks = [tc(1,2), tc(3,2), tc(5,4)]

# plain purple targets not affected by pink-crosses
purple_clicks = [tc(0,3), tc(2,1), tc(2,3), tc(2,5),
                 tc(4,1), tc(4,3), tc(4,5), tc(6,1), tc(6,3)]

# restore-green clicks for green-target tiles accidentally toggled by pink-crosses
restore_clicks = [tc(0,2), tc(1,1), tc(1,3),   # from pink(1,2)
                  tc(3,1), tc(3,3),               # from pink(3,2)
                  tc(4,4), tc(5,3), tc(5,5), tc(6,4)]  # from pink(5,4)

L5 = pink_cross_clicks + purple_clicks + restore_clicks
print(f"L5 clicks ({len(L5)} total): {L5}")

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
for (x, y) in PRE:
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
print(f"Starting at level {r.levels_completed + 1}")

for i, (x, y) in enumerate(L5, 1):
    r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    if r.levels_completed >= 5:
        print(f">>> LEVEL 5 COMPLETE after {i} clicks!")
        break

print(f"End: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
