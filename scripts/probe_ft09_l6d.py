"""ft09 L6: read raw block values for all present slots at start, with no clicks."""
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

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make("ft09")
r=env.observation_space
for x,y in PRE:
    r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
print(f"levels_completed={r.levels_completed}  (should be 5 = L6 start)")

g=grid(r)

print("\nRaw 3x3 mini-grids for ALL present slots at L6 start:")
for ri,rs in enumerate(ROW_STARTS):
    for ci,cs in enumerate(COL_STARTS):
        blk=g[rs:rs+6,cs:cs+6]
        if np.all(blk==BG): continue
        if (blk!=BG).sum()<6: continue
        row0=blk[0]
        # summarise unique values
        uniq=sorted(set(blk.flatten().tolist())-{BG})
        # 3x3 mini
        def dom2(sub):
            v,c=np.unique(sub,return_counts=True); return int(v[np.argmax(c)])
        mini=[[dom2(g[rs+2*i:rs+2*i+2,cs+2*j:cs+2*j+2]) for j in range(3)] for i in range(3)]
        has_white=(blk==0).any()
        tag="KEY" if has_white else "plain"
        print(f"  ({ri},{ci}) rows{rs}-{rs+5} cols{cs}-{cs+5}  {tag}  values={uniq}  mini={mini}")
