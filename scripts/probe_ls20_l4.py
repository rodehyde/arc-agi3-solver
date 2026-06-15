"""ls20 L4: probe specific paths and investigate unknown sprite ttfwljgohq."""
import logging, numpy as np
from collections import Counter
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']
L3=[AMAP[c] for c in 'UUUUUUUULDDDDDDDDUUULLURRRRRRRUUULUDURD']

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2+L3: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)
def st(env):
    g=env._game
    return f"col={g.hiaauhahz} rot={g.cklxociuu} steps={g._step_counter_ui.current_steps}"

def cell_changes(g0, g1):
    diff=(g0!=g1); total=int(diff.sum())
    if total==0: return total,{}
    rows,cols=np.where(diff)
    tr=Counter()
    for r_,c_ in zip(rows,cols): tr[(int(g0[r_,c_]),int(g1[r_,c_]))]+=1
    return total,dict(tr)

def trace_path(path_str, label):
    env,r=fresh()
    g0=np.array(r.frame[-1])
    print(f"\n{label}: {path_str}")
    prev_col=env._game.hiaauhahz
    for i,c in enumerate(path_str):
        prev_pos=pp(env)
        r=env.step(AMAP[c])
        pos=pp(env)
        col=env._game.hiaauhahz
        steps=env._game._step_counter_ui.current_steps
        notes=[]
        if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
        if pos==prev_pos: notes.append('BLOCKED')
        if pos==(54,5) and steps==42 and prev_pos!=(54,5): notes.append('RESET!')
        note_str=('  '+' | '.join(notes)) if notes else ''
        print(f"  {i+1:2d} {c}: {prev_pos}->{pos}  {st(env)}{note_str}")
        prev_col=col
    return env, r

# Key question: how to navigate to different parts of the maze.
# From initial probing: LEFT 3 → (39,5), then DOWN loops via teleporter.
# Need to find paths going DOWN from (49,5) or (44,5)

print("=== Probing DOWN from (49,5) ===")
env,r=fresh()
for _ in range(1): r=env.step(A3)  # 1 LEFT to (49,5)
print(f"At: {pp(env)}")
for i in range(12):
    prev=pp(env)
    r=env.step(A2)  # DOWN
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    note+=' TELEPORT' if (pos!=prev and abs(pos[0]-prev[0])>5 or (pos!=prev and abs(pos[1]-prev[1])>5)) else ''
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
print("=== Probing DOWN from (44,5) ===")
env,r=fresh()
for _ in range(2): r=env.step(A3)  # 2 LEFT to (44,5)
print(f"At: {pp(env)}")
for i in range(12):
    prev=pp(env)
    r=env.step(A2)  # DOWN
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
print("=== Probing DOWN from (39,5) then RIGHT ===")
env,r=fresh()
for _ in range(3): r=env.step(A3)  # LEFT x3 to (39,5)
r=env.step(A2); print(f"DOWN 1: {pp(env)}")  # to (39,10)
r=env.step(A2); print(f"DOWN 2: {pp(env)}")  # to (39,15)
r=env.step(A2); print(f"DOWN 3: {pp(env)}")  # to (39,20) or teleport
# Now try RIGHT from here
for i in range(8):
    prev=pp(env)
    r=env.step(A4)  # RIGHT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
print("=== Probing from (39,15): all 4 directions ===")
for direction, action in [('UP',A1),('DOWN',A2),('LEFT',A3),('RIGHT',A4)]:
    env,r=fresh()
    # Navigate to (39,15): LEFT x3, DOWN x2
    for _ in range(3): r=env.step(A3)
    for _ in range(2): r=env.step(A2)
    assert pp(env)==(39,15), f"Expected (39,15) got {pp(env)}"
    prev=pp(env)
    r=env.step(action)
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' TELEPORT' if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5) else ''
    note+=' BLOCKED' if pos==prev else ''
    print(f"  {direction}: {prev}->{pos}  col={col}  steps={steps}{note}")

print()
print("=== Finding path to ttfwljgohq at (24,30) ===")
# Try from (39,15): go LEFT
env,r=fresh()
for _ in range(3): r=env.step(A3)  # to (39,5)
for _ in range(2): r=env.step(A2)  # to (39,15)
print(f"At: {pp(env)}")
# Try going LEFT from (39,15)
for i in range(10):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    steps=env._game._step_counter_ui.current_steps
    col=env._game.hiaauhahz
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    print(f"  LEFT {i+1}: {prev}->{pos}  steps={steps} col={col}{note}")
    if pos==prev: break

print()
print("=== From (44,5): DOWN then explore ===")
trace_path('LL'+'DDDDDD', '(54,5) → 2L then 6D')

print()
print("=== What does ttfwljgohq at (24,30) DO? Probe cell changes ===")
# First get the grid at (24,30) — find approach
env,r=fresh()
for _ in range(3): r=env.step(A3)  # (39,5)
for _ in range(2): r=env.step(A2)  # (39,15)
for _ in range(3): r=env.step(A3)  # explore left
pos=pp(env)
print(f"After LLL LLL DD: pos={pos}  col={env._game.hiaauhahz}  steps={env._game._step_counter_ui.current_steps}")
