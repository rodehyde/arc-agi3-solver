"""ft09 L7: identify all present tiles, classify key vs plain, read mini-grids."""
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
BG=4

def grid(r): return np.array(r.frame[-1])

def to_l7():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for lvl in range(1,7):
        for x,y in SOLUTIONS[lvl]:
            r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
    return env,r

env,r=to_l7()
print(f"levels_completed={r.levels_completed} (should be 6)")
g=grid(r)

def dom2(sub):
    v,c=np.unique(sub,return_counts=True); return int(v[np.argmax(c)])

print("\nAll present tile slots at L7 start:")
PRESENT=[]; KEYS=[]; PLAIN=[]
for ri,rs in enumerate(ROW_STARTS):
    for ci,cs in enumerate(COL_STARTS):
        blk=g[rs:rs+6,cs:cs+6]
        if (blk!=BG).sum()<4: continue
        mini=[[dom2(g[rs+2*i:rs+2*i+2,cs+2*j:cs+2*j+2]) for j in range(3)] for i in range(3)]
        has_white=(blk==0).any()
        tag="KEY" if has_white else "plain"
        PRESENT.append((ri,ci))
        if has_white: KEYS.append((ri,ci))
        else: PLAIN.append((ri,ci))
        centre=mini[1][1]
        print(f"  ({ri},{ci}) {tag}  mini={mini}  centre={centre}")

print(f"\nPRESENT={PRESENT}")
print(f"KEYS={KEYS}")
print(f"PLAIN={PLAIN}")

# Also check top-right corner block
print("\nTop-right corner rows 0-7 cols 56-63:")
for row in range(8):
    print(f"  row {row}: {list(g[row,56:64])}")
