"""ls20 L4: action table probe — all actions from start, characterise teleporters and toggles."""
import logging, numpy as np
from collections import Counter
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
             6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
             12:'orange',13:'maroon',14:'green',15:'purple'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']
L3=[AMAP[c] for c in 'UUUUUUUULDDDDDDDDUUULLURRRRRRRUUULUDURD']

def fresh_l4():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2+L3: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)

def cell_changes(g0, g1):
    diff=(g0!=g1); total=int(diff.sum())
    if total==0: return total,None,{}
    rows,cols=np.where(diff)
    bbox=(int(rows.min()),int(rows.max()),int(cols.min()),int(cols.max()))
    tr=Counter()
    for r_,c_ in zip(rows,cols): tr[(int(g0[r_,c_]),int(g1[r_,c_]))]+=1
    return total,bbox,dict(tr)

def state_str(env):
    g=env._game
    col_val=g.tnkekoeuk[g.hiaauhahz]
    return f"rot={g.cklxociuu}  col_idx={g.hiaauhahz}({COLOR_NAMES.get(col_val,'?')})  steps={g._step_counter_ui.current_steps}"

env0,r0=fresh_l4()
g0=np.array(r0.frame[-1])
print(f"=== Level 4 Action Table ===")
print(f"Start: pos={pp(env0)}  {state_str(env0)}")
print(f"  decrement={env0._game._step_counter_ui.efipnixsvl}")
print()

# Basic action table from start
for a,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=fresh_l4()
    r2=env2.step(a)
    g1=np.array(r2.frame[-1])
    total,bbox,tr=cell_changes(g0,g1)
    moved=(pp(env2)!=pp(env0))
    col_changed=(env2._game.hiaauhahz!=env0._game.hiaauhahz)
    rot_changed=(env2._game.cklxociuu!=env0._game.cklxociuu)
    print(f"--- ACTION {name} ---")
    print(f"  pos: {pp(env0)} -> {pp(env2)}  moved={moved}")
    print(f"  {state_str(env2)}")
    print(f"  cells_changed={total}")
    if col_changed: print(f"  *** COLOR CHANGED ***")
    if rot_changed: print(f"  *** ROTATION CHANGED ***")
    print()

# Probe the ttfwljgohq at (24,30) — what happens when player enters it?
print("=== Probing ttfwljgohq at (24,30) ===")
print("Trying to navigate to (24,30) from (54,5)...")
# Need to find a path. Try going left and down.
test_paths = [
    ('LLLLLLLDDDDDD', 'left 7 down 6'),
    ('DDDDDDLLLLLLL', 'down 6 left 7'),
    ('LLLLLLDDDDDDL', 'left 6 down 6 left'),
    ('DDDLLLLLLLDDD', 'down 3 left 7 down 3'),
]
for path_str, desc in test_paths:
    env2,r2=fresh_l4()
    for c in path_str:
        r2=env2.step(AMAP[c])
    pos=pp(env2)
    col=env2._game.hiaauhahz
    rot=env2._game.cklxociuu
    steps=env2._game._step_counter_ui.current_steps
    print(f"  {desc}: pos={pos}  col={col}  rot={rot}  steps={steps}")
print()

# Explore from start step by step to map reachable corridors
print("=== Stepping from (54,5): map 10 moves each direction ===")
for direction, action, limit in [('UP', A1, 15), ('DOWN', A2, 15), ('LEFT', A3, 15)]:
    env2,r2=fresh_l4()
    prev_pos=pp(env2)
    print(f"\n{direction} from start (stop on no-movement):")
    for i in range(limit):
        r2=env2.step(action)
        pos=pp(env2)
        col=env2._game.hiaauhahz
        rot=env2._game.cklxociuu
        steps=env2._game._step_counter_ui.current_steps
        if pos==prev_pos:
            print(f"  {direction} {i+1}: BLOCKED at {pos}")
            break
        # Reset detection
        if pos==(54,5) and steps==42 and prev_pos!=(54,5):
            print(f"  {direction} {i+1}: RESET back to start!")
            break
        print(f"  {direction} {i+1}: {prev_pos}->{pos}  col={col}  rot={rot}  steps={steps}")
        prev_pos=pos
print()

# Path to color toggle at (34,30) from start (54,5)
print("=== Path to color toggle (34,30) ===")
env2,r2=fresh_l4()
# Try: LEFT to col 34, DOWN to row 30
test='LLLLDDDDDD'
for i,c in enumerate(test):
    prev=pp(env2)
    r2=env2.step(AMAP[c])
    pos=pp(env2)
    col=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    note=f'  *** COL CHANGE {col}' if col!=env2._game.hiaauhahz else ''
    note_c = f'  *** COL CHANGED -> {col}' if (i>0 and col != [env2._game.hiaauhahz,env2._game.hiaauhahz][0]) else ''
    print(f"  {i+1} {c}: {prev}->{pos}  col={col}  steps={steps}")
