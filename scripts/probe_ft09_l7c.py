"""ft09 L7: check if level is already won at start, and probe the win mechanic."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

SOLUTIONS = {
    1: [(38,38),(38,46),(54,46),(38,54)],
    2: [(22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48)],
    3: [(22,6),(30,6),(38,6),(22,14),(14,22),(30,22),(14,30),
        (46,30),(30,38),(46,38),(22,46),(22,54),(30,54),(38,54)],
    4: [(15,17),(23,17),(23,17),(31,17),(47,17),(15,25),(31,25),
        (47,25),(15,33),(23,33),(23,33),(31,33),(39,33),(23,41),
        (39,41),(23,49),(23,49),(31,49),(31,49),(39,49),(39,49)],
    5: [(25,15),(25,31),(41,47),(33,7),(17,23),(33,23),(49,23),
        (17,39),(33,39),(49,39),(17,55),(33,55),(25,7),(17,15),
        (33,15),(17,31),(33,31),(41,39),(33,47),(49,47),(41,55)],
    6: [(7,9),(7,17),(23,17),(39,17),(15,25),(23,25),
        (15,33),(31,33),(39,33),(47,33),(23,41),(47,41),(55,41)],
}

ROW_STARTS=[6,14,22,30,38,46]
COL_STARTS=[4,12,20,28,36,44,52]

def tc(ri,ci): return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)

def to_l7():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for lvl in range(1,7):
        for x,y in SOLUTIONS[lvl]:
            r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
    return env,r

# Check state at L7 start (before any clicks)
env,r=to_l7()
print(f"L7 start: levels_completed={r.levels_completed} state={r.state.name} win_levels={r.win_levels}")
print(f"  frame empty? {len(r.frame)==0}")

# Now just take one RESET and see what happens
env2,r2=to_l7()
r2=env2.step(GameAction.RESET)
print(f"\nAfter RESET: levels_completed={r2.levels_completed} state={r2.state.name}")

# Try clicking (1,0) and check if it wins
env3,r3=to_l7()
cx,cy=tc(1,0)
r3=env3.step(GameAction.ACTION6,data={"x":cx,"y":cy})
print(f"\nAfter click (1,0) at ({cx},{cy}): levels_completed={r3.levels_completed} state={r3.state.name}")
print(f"  frame empty? {len(r3.frame)==0}")
if r3.levels_completed >= 7:
    print("  >>> LEVEL 7 WON after 1 click!")

# Try just taking NO action (wait) — use action1 on empty space
env4,r4=to_l7()
cx2,cy2=tc(1,2)  # click on (1,2) - a yellow plain tile
r4=env4.step(GameAction.ACTION6,data={"x":cx2,"y":cy2})
print(f"\nAfter click (1,2) at ({cx2},{cy2}): levels_completed={r4.levels_completed} state={r4.state.name}")
print(f"  frame empty? {len(r4.frame)==0}")
