"""ft09 L6: click every plain tile individually, record which slots change."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1=[(38,38),(38,46),(54,46),(38,54)]
L2=[(22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48)]
L3=[(22,6),(30,6),(38,6),(22,14),(14,22),(30,22),(14,30),
    (46,30),(30,38),(46,38),(22,46),(22,54),(30,54),(38,54)]
L4=[(15,17),(23,17),(23,17),(31,17),(47,17),(15,25),(31,25),
    (47,25),(15,33),(23,33),(23,33),(31,33),(39,33),(23,41),
    (39,41),(23,49),(23,49),(31,49),(31,49),(39,49),(39,49)]
L5=[(25,15),(25,31),(41,47),(33,7),(17,23),(33,23),(49,23),
    (17,39),(33,39),(49,39),(17,55),(33,55),(25,7),(17,15),
    (33,15),(17,31),(33,31),(41,39),(33,47),(49,47),(41,55)]
PRE=L1+L2+L3+L4+L5

ROW_STARTS=[6,14,22,30,38,46]
COL_STARTS=[4,12,20,28,36,44,52]
BG=4

PRESENT=[(0,0),(0,1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
         (2,1),(2,2),(2,3),(2,4),(2,5),
         (3,1),(3,2),(3,3),(3,4),(3,5),
         (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(5,5),(5,6)]

def grid(r): return np.array(r.frame[-1])
def tc(ri,ci): return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)

def to_l6():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for x,y in PRE:
        r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
    return env,r

def changed_slots(g0, g1):
    out=[]
    for ri,rs in enumerate(ROW_STARTS):
        for ci,cs in enumerate(COL_STARTS):
            if (ri,ci) not in PRESENT: continue
            if not np.array_equal(g0[rs:rs+6,cs:cs+6], g1[rs:rs+6,cs:cs+6]):
                out.append((ri,ci))
    return out

print("Clicking each tile; recording which slots change:")
for slot in PRESENT:
    env,r=to_l6()
    g0=grid(r).copy()
    cx,cy=tc(*slot)
    r=env.step(GameAction.ACTION6,data={"x":cx,"y":cy})
    g1=grid(r)
    affected=changed_slots(g0,g1)
    multi = " <-- GROUP TOGGLE" if len(affected)>1 else ""
    print(f"  click {slot}: affects {affected}{multi}")
