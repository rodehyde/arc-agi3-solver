"""ft09 L6: test 12-click solution (click each green-target tile once)."""
import logging
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1 = [(38,38),(38,46),(54,46),(38,54)]
L2 = [(22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48)]
L3 = [(22,6),(30,6),(38,6),(22,14),(14,22),(30,22),(14,30),
      (46,30),(30,38),(46,38),(22,46),(22,54),(30,54),(38,54)]
L4 = [(15,17),(23,17),(23,17),(31,17),(47,17),(15,25),(31,25),
      (47,25),(15,33),(23,33),(23,33),(31,33),(39,33),(23,41),
      (39,41),(23,49),(23,49),(31,49),(31,49),(39,49),(39,49)]
L5 = [(25,15),(25,31),(41,47),(33,7),(17,23),(33,23),(49,23),
      (17,39),(33,39),(49,39),(17,55),(33,55),(25,7),(17,15),
      (33,15),(17,31),(33,31),(41,39),(33,47),(49,47),(41,55)]
PRE = L1+L2+L3+L4+L5

ROW_STARTS = [6, 14, 22, 30, 38, 46]
COL_STARTS = [4, 12, 20, 28, 36, 44, 52]


def tc(ri, ci):
    return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)


# Green targets: click once each
GREEN = [(1,0),(1,1),(1,4),(2,2),(2,3),(2,5),(3,1),(3,3),(3,4),(4,2),(4,5),(4,6)]
L6 = [tc(ri,ci) for ri,ci in GREEN]
print(f"L6 clicks ({len(L6)}): {L6}")

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
for x,y in PRE:
    r = env.step(GameAction.ACTION6, data={"x":x,"y":y})
print(f"Starting at level {r.levels_completed+1}")

for i,(x,y) in enumerate(L6, 1):
    r = env.step(GameAction.ACTION6, data={"x":x,"y":y})
    if r.levels_completed >= 6:
        print(f">>> LEVEL 6 COMPLETE after {i} clicks!")
        break

print(f"End: levels={r.levels_completed}/{r.win_levels} state={r.state.name}")
