"""ft09 L6: inspect state after 12 clicks, then try all-22-green."""
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

def grid(r): return np.array(r.frame[-1])
def dom(blk):
    v,c=np.unique(blk,return_counts=True); return int(v[np.argmax(c)])
def tc(ri,ci): return (COL_STARTS[ci]+3,ROW_STARTS[ri]+3)

def to_l6():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for x,y in PRE:
        r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
    return env,r

# Plain tile slots (from earlier scan)
PLAIN=[(0,0),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
       (2,1),(2,2),(2,3),(2,5),
       (3,1),(3,3),(3,4),(3,5),
       (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(5,6)]

def tile_colour(g,ri,ci):
    rs,cs=ROW_STARTS[ri],COL_STARTS[ci]
    blk=g[rs:rs+6,cs:cs+6]
    vals=blk[(blk!=BG)&(blk!=6)]   # exclude bg and pink notch
    if len(vals)==0: return None
    v,c=np.unique(vals,return_counts=True)
    return int(v[np.argmax(c)])

NAMES={11:'yel',14:'grn',4:'bg'}

# --- Show state after 12 clicks (the original hypothesis) ---
GREEN12=[(1,0),(1,1),(1,4),(2,2),(2,3),(2,5),(3,1),(3,3),(3,4),(4,2),(4,5),(4,6)]
env,r=to_l6()
for ri,ci in GREEN12:
    r=env.step(GameAction.ACTION6,data={"x":tc(ri,ci)[0],"y":tc(ri,ci)[1]})
g=grid(r)
print("State after 12-click hypothesis:")
for ri,ci in PLAIN:
    col=tile_colour(g,ri,ci)
    print(f"  ({ri},{ci}): {NAMES.get(col,col)}")
print(f"  levels_completed={r.levels_completed}")

# --- Try all 22 plain tiles green ---
print()
env,r=to_l6()
for ri,ci in PLAIN:
    r=env.step(GameAction.ACTION6,data={"x":tc(ri,ci)[0],"y":tc(ri,ci)[1]})
print(f"All-22-green: levels={r.levels_completed}  {'WIN' if r.levels_completed>=6 else 'no win'}")

# --- Try only the 10 previously-yellow tiles (inverse hypothesis) ---
print()
YELLOW10=[(0,0),(1,2),(1,3),(1,5),(2,1),(3,5),(4,1),(4,3),(4,4),(5,6)]
env,r=to_l6()
for ri,ci in YELLOW10:
    r=env.step(GameAction.ACTION6,data={"x":tc(ri,ci)[0],"y":tc(ri,ci)[1]})
print(f"Click-10-yellows-only: levels={r.levels_completed}  {'WIN' if r.levels_completed>=6 else 'no win'}")
