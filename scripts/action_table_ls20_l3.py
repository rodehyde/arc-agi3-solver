"""ls20 L3: complete action table probe — all actions from start, plus toggle characterisation."""
import logging, numpy as np
from collections import Counter
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
             6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
             12:'orange',13:'maroon',14:'green',15:'purple'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']

def fresh_l3():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2: r=env.step(a)
    return env, r

def player_pos(env):
    # Use sprite position directly, not pixel scan (avoids ref-box confusion)
    sp=env._game.gudziatsk
    return (sp.x, sp.y)

def ref_str(r):
    g=np.array(r.frame[-1]); c={}
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if (blk.count(9)>=2 or blk.count(12)>=2) else 5
    return '/'.join(''.join('B' if c[(ri,ci)]!=5 else '.' for ci in range(3)) for ri in range(3))

def cell_changes(g0, g1):
    diff=(g0!=g1); total=int(diff.sum())
    if total==0: return total,None,{}
    rows,cols=np.where(diff)
    bbox=(int(rows.min()),int(rows.max()),int(cols.min()),int(cols.max()))
    tr=Counter()
    for r_,c_ in zip(rows,cols): tr[(int(g0[r_,c_]),int(g1[r_,c_]))]+=1
    return total,bbox,dict(tr)

def fmt_tr(tr):
    return ', '.join(f"{COLOR_NAMES.get(a,a)}->{COLOR_NAMES.get(b,b)}:{n}" for (a,b),n in sorted(tr.items()))

def state_str(env):
    game=env._game
    return f"rot={game.cklxociuu}  color={game.hiaauhahz}({COLOR_NAMES.get(game.tnkekoeuk[game.hiaauhahz],'?')})  steps={game._step_counter_ui.current_steps}"

# Baseline
env0,r0=fresh_l3()
g0=np.array(r0.frame[-1])
print(f"=== Level 3 Action Table ===")
print(f"Start: pos={player_pos(env0)}  {state_str(env0)}  avail={r0.available_actions}")
print()

for a,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=fresh_l3()
    r2=env2.step(a)
    g1=np.array(r2.frame[-1])
    total,bbox,tr=cell_changes(g0,g1)
    moved=(player_pos(env2)!=player_pos(env0))
    ref_changed=(ref_str(r2)!=ref_str(r0))
    avail_changed=(r2.available_actions!=r0.available_actions)
    print(f"--- ACTION {name} ---")
    print(f"  pos: {player_pos(env0)} -> {player_pos(env2)}  moved={moved}")
    print(f"  {state_str(env2)}")
    print(f"  cells_changed={total}  bbox={bbox}")
    print(f"  transitions: {fmt_tr(tr)}")
    print(f"  ref_changed={ref_changed}  avail_changed={avail_changed}")
    print()

# Probe the color toggle: navigate to (29,45) and hit it
print("=== Color toggle probe: navigate RIGHT x4 to (29,45) ===")
env2,r2=fresh_l3()
for i in range(4):
    r2=env2.step(A4)  # RIGHT
    pos=player_pos(env2)
    print(f"  Move {i+1} R: pos={pos}  {state_str(env2)}  avail={r2.available_actions}")
print(f"  Color toggle hit! rot={env2._game.cklxociuu}  color={env2._game.hiaauhahz}")
print()

# After color toggle: probe all 4 actions again
print("=== Actions AFTER color toggle (pos=(29,45), color changed) ===")
env_ct,r_ct=fresh_l3()
for _ in range(4): r_ct=env_ct.step(A4)
g_ct=np.array(r_ct.frame[-1])
pos_ct=player_pos(env_ct)
for a,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=fresh_l3()
    for _ in range(4): r2=env2.step(A4)
    r2=env2.step(a)
    g1=np.array(r2.frame[-1])
    total,bbox,tr=cell_changes(g_ct,g1)
    print(f"  {name}: pos={player_pos(env2)}  cells={total}  avail={r2.available_actions}  color={env2._game.hiaauhahz}  ref_changed={ref_str(r2)!=ref_str(r_ct)}")

# Probe the rotation toggle: navigate to (49,10) and check effect
print()
print("=== Rotation toggle at (49,10): approach from above via upper corridor ===")
# From (9,45): need to get to (49,10). Try going up then right.
# Quick test: go UP a lot then RIGHT
env2,r2=fresh_l3()
test_path='UUUUUUURRRRRRRRRD'  # up 7 to row ~10, right 8 to col ~49, down 1
prev_state=(player_pos(env2),env2._game.cklxociuu,env2._game.hiaauhahz)
for i,c in enumerate(test_path):
    a=AMAP[c]
    r2=env2.step(a)
    pos=player_pos(env2)
    rot=env2._game.cklxociuu
    color=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    if rot!=prev_state[1] or color!=prev_state[2]:
        print(f"  Step {i+1} {c}: pos={pos}  rot={rot}  color={color}  steps={steps}  *** STATE CHANGED ***")
    else:
        print(f"  Step {i+1} {c}: pos={pos}  rot={rot}  color={color}  steps={steps}")
    prev_state=(pos,rot,color)

# Check the gbvqrjtaqo sprites effect
print()
print("=== gbvqrjtaqo sprites: what are they? (walk into them) ===")
# Sprite at (8,5): player at (9,45), go UP to row~5 and check left wall
env2,r2=fresh_l3()
print("Going UP 8 from (9,45):")
for i in range(9):
    r2=env2.step(A1)
    print(f"  UP {i+1}: pos={player_pos(env2)}  steps={env2._game._step_counter_ui.current_steps}  avail={r2.available_actions}")
