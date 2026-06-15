"""ft09 L7: probe available actions + click scope for every plain tile."""
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

PRESENT=[(0,0),(0,1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
         (2,1),(2,2),(2,3),(2,4),(2,5),
         (3,1),(3,2),(3,3),(3,4),(3,5),
         (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(5,5),(5,6)]
KEYS=[(0,1),(2,4),(3,2),(5,5)]
PLAIN=[(s) for s in PRESENT if s not in KEYS]

def grid(r): return np.array(r.frame[-1])
def tc(ri,ci): return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)

def to_l7():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for lvl in range(1,7):
        for x,y in SOLUTIONS[lvl]:
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

# --- Check available_actions ---
env,r=to_l7()
print(f"available_actions: {r.available_actions}")
g0=grid(r).copy()

# --- Probe one click and show full cell diff ---
cx,cy=tc(1,0)
r2=env.step(GameAction.ACTION6,data={"x":cx,"y":cy})
g1=grid(r2)
diff=np.where(g0!=g1)
print(f"\nClick (1,0) at ({cx},{cy}): {len(diff[0])} cells changed")
if len(diff[0])>0:
    transitions={}
    for y,x in zip(diff[0],diff[1]):
        k=(int(g0[y,x]),int(g1[y,x]))
        transitions[k]=transitions.get(k,0)+1
    print(f"  transitions: {transitions}")
    print(f"  affected slots: {changed_slots(g0,g1)}")
print(f"  available_actions after: {r2.available_actions}")

# --- Probe click scope for every plain tile ---
print("\nGroup-toggle map for every plain tile:")
for slot in PLAIN:
    env2,r2=to_l7()
    g0=grid(r2).copy()
    cx,cy=tc(*slot)
    r2=env2.step(GameAction.ACTION6,data={"x":cx,"y":cy})
    g1=grid(r2)
    affected=changed_slots(g0,g1)
    tag=" <-- GROUP TOGGLE" if len(affected)>1 else ""
    print(f"  click {slot}: affects {affected}{tag}")

# --- Probe key slots (should be no-op) ---
print("\nKey slots (expect no effect):")
for slot in KEYS:
    env2,r2=to_l7()
    g0=grid(r2).copy()
    cx,cy=tc(*slot)
    r2=env2.step(GameAction.ACTION6,data={"x":cx,"y":cy})
    g1=grid(r2)
    affected=changed_slots(g0,g1)
    print(f"  click {slot}: affects {affected}")
