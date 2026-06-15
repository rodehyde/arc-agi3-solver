"""ls20 L2: complete action table — every action probed with full cell-change instrument."""
import logging, numpy as np
from collections import Counter
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'ACTION1(UP)',A2:'ACTION2(DOWN)',A3:'ACTION3(LEFT)',A4:'ACTION4(RIGHT)'}
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]

COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
             6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
             12:'orange',13:'maroon',14:'green',15:'purple'}

def fresh_l2():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    for a in L1: r=env.step(a)
    return env, r

def ppos(r):
    g=np.array(r.frame[-1])
    ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

def ref_str(r):
    g=np.array(r.frame[-1])
    c={}
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return '/'.join(''.join('B' if c[(ri,ci)]==9 else '.' for ci in range(3)) for ri in range(3))

def step_counter_val(r):
    """Read step counter from game object — use the 8 red cells bottom-right as proxy."""
    # The step counter UI renders somewhere. Read game state directly.
    return None  # will use game object instead

def cell_changes(g0, g1):
    """Full cell-change report: count, bounding box, every value transition."""
    diff = (g0 != g1)
    total = int(diff.sum())
    if total == 0:
        return total, None, {}
    rows, cols = np.where(diff)
    bbox = (int(rows.min()), int(rows.max()), int(cols.min()), int(cols.max()))
    transitions = Counter()
    for r,c in zip(rows, cols):
        transitions[(int(g0[r,c]), int(g1[r,c]))] += 1
    return total, bbox, dict(transitions)

def format_transitions(tr):
    parts=[]
    for (a,b),n in sorted(tr.items()):
        an=COLOR_NAMES.get(a,str(a)); bn=COLOR_NAMES.get(b,str(b))
        parts.append(f"{an}→{bn}:{n}")
    return ', '.join(parts)

# Get baseline
env0, r0 = fresh_l2()
g0 = np.array(r0.frame[-1])
pos0 = ppos(r0)
ref0 = ref_str(r0)
avail0 = r0.available_actions
sc0 = env0._game._step_counter_ui.osgviligwp

print(f"=== Level 2 Action Table ===")
print(f"Start: pos={pos0}  ref={ref0}  avail_actions={avail0}  step_counter_max={sc0}")
print()

for a in [A1,A2,A3,A4]:
    env2, r2 = fresh_l2()
    sc_before = env2._game._step_counter_ui.osgviligwp
    r2 = env2.step(a)
    sc_after = env2._game._step_counter_ui.osgviligwp
    g1 = np.array(r2.frame[-1])
    npos = ppos(r2)
    nref = ref_str(r2)
    navail = r2.available_actions
    total, bbox, tr = cell_changes(g0, g1)
    moved = npos != pos0
    ref_changed = nref != ref0
    avail_changed = navail != avail0

    print(f"--- {ANAMES[a]} ---")
    print(f"  Position: {pos0} → {npos}  (moved={moved})")
    print(f"  Ref state: {ref0} → {nref}  (changed={ref_changed})")
    print(f"  Available actions: {avail0} → {navail}  (changed={avail_changed})")
    print(f"  Step counter: {sc_before} → {sc_after}")
    print(f"  Cells changed: {total}")
    if bbox:
        print(f"  Bounding box of changes: rows {bbox[0]}-{bbox[1]}, cols {bbox[2]}-{bbox[3]}")
    if tr:
        print(f"  Transitions: {format_transitions(tr)}")
    if r2.levels_completed > 1:
        print(f"  *** LEVEL COMPLETED ***")
    print()

# Also probe step counter decrement: take multiple steps and track counter
print("=== Step counter tracking (10 UP moves from start) ===")
env2, r2 = fresh_l2()
prev_sc = env2._game._step_counter_ui.osgviligwp
print(f"Initial counter: {prev_sc}")
for i in range(10):
    r2 = env2.step(A1)
    cur_sc = env2._game._step_counter_ui.osgviligwp
    pos = ppos(r2)
    print(f"  Move {i+1} UP: pos={pos}  counter={cur_sc}  (delta={cur_sc-prev_sc})")
    prev_sc = cur_sc
