"""ls20 L4: probe RIGHT from col-14 corridor to find shape toggle path."""
import logging
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

def pp(env): return (env._game.gudziatsk.x, env._game.gudziatsk.y)
def st(env): g=env._game; return f"col={g.hiaauhahz} shape={g.fwckfzsyc} steps={g._step_counter_ui.current_steps}"

def trace(path_str):
    env,r=fresh()
    print(f"Tracing: {path_str}")
    for i,c in enumerate(path_str):
        prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): notes.append('TELEPORT')
        if shape!=4: notes.append(f'SHAPE->{shape}');
        if col!=2: notes.append(f'COL->{col}')
        if steps==42 and prev!=(54,5): notes.append('PICKUP')
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if shape==5 and col==1: print(f"  *** BOTH shape=5 AND col=1 — ready for target! ***")
    return env,r

# Path to (14,35): LLLDDLLLLDLDDD
# Then go RIGHT from (14,35) to find shape toggle
print("=== Path to (14,35) then RIGHT ===")
trace('LLLDDLLLLDLDDDDR')

print()
print("=== Path to (14,30) then RIGHT ===")
trace('LLLDDLLLLDLDDR')

print()
print("=== Path to (14,25) then RIGHT ===")
trace('LLLDDLLLLDLDR')

print()
print("=== Path to (14,20) then RIGHT ===")
trace('LLLDDLLLLDLR')

print()
print("=== Path to (14,40) then RIGHT ===")
trace('LLLDDLLLLDLDDDDR')

print()
print("=== Path to (14,45) then RIGHT ===")
trace('LLLDDLLLLDLDDDDDR')

print()
# What about going UP from col 14?
print("=== From (14,20): go UP ===")
env,r=fresh()
for c in 'LLLDDLLLLDL': r=env.step(AMAP[c])
print(f"At (14,20): {pp(env)}")
for i in range(5):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# Try going from (14,5) going DOWN
print("=== Path to (14,5): ===")
env,r=fresh()
# (14,5) is in BFS list. How to reach it?
# From BFS, (19,5) going LEFT → (14,5)?
# Navigate to (19,5):
# (19,5) ... from (39,5) going LEFT is BLOCKED. From (24,5) going LEFT → (19,5)?
# (24,5) is in BFS list. Navigate to (24,5)?
# From (34,10) going UP → (34,5)?
# (34,5) is in BFS list. From (34,5) going LEFT → (29,5)?
# Wait (29,5) is in the sprite list as ihdgageizm -- wall at (29,5)!
# Let me try from (24,10) going UP
# (24,10) is in BFS list.
# From (34,10) going LEFT → (29,10)? (29,10) is in ihdgageizm list.
# Try directly:
print("From (34,10): going LEFT:")
env,r=fresh()
for c in 'LLLDD': r=env.step(AMAP[c])  # to (39,15), one D to (39,10)
r=env.step(A2)  # wait no, LLLD gives (39,10)
env,r=fresh()
for c in 'LLLDD': r=env.step(AMAP[c])
print(f"After LLLDD: {pp(env)}")
# Try to navigate to col 24 row 5
env,r=fresh()
for c in 'LLLDLLL': r=env.step(AMAP[c])
print(f"After LLLDLLL: {pp(env)}")
for c in 'UU': r=env.step(AMAP[c])
print(f"After UU: {pp(env)}")

print()
# Navigate upward from (19,15) or (24,15) to get to row 5
print("=== From (24,15): trace UP ===")
env,r=fresh()
for c in 'LLLDDLLL': r=env.step(AMAP[c])  # to (24,15) via row 15
print(f"At: {pp(env)}")
for i in range(4):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
