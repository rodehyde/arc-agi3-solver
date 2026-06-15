"""ls20 L4: find path to ttfwljgohq at (24,30), and from there to target (14,5)→(9,5)."""
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

def trace(path_str, label=''):
    env,r=fresh()
    if label: print(f"\n=== {label}: {path_str} ===")
    print(f"Start: {pp(env)}  {st(env)}")
    prev_col=env._game.hiaauhahz
    prev_shape=env._game.fwckfzsyc
    for i,c in enumerate(path_str):
        prev=pp(env)
        r=env.step(AMAP[c])
        pos=pp(env)
        col=env._game.hiaauhahz
        shape=env._game.fwckfzsyc
        steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): notes.append('TELEPORT')
        if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
        if shape!=prev_shape: notes.append(f'SHAPE {prev_shape}->{shape}')
        if steps==42 and prev!=(54,5): notes.append('PICKUP')
        if r.levels_completed>3: notes.append('*** WIN ***')
        note_str=('  ['+' | '.join(notes)+']') if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note_str}")
        prev_col=col; prev_shape=shape
    return env,r

# The color toggle path is: LLLDDDLDDLLUD (13 steps)
# Let me explore from key positions to find (24,30)

# From (44,30) [reached via LLLDDDLDDLL = step 11]
trace('LLLDDDLDDLL', 'Navigate to (44,30)')

print()
# From (44,30): probe DOWN
print("=== From (44,30): probe DOWN ===")
env,r=fresh()
for c in 'LLLDDDLDDLL': r=env.step(AMAP[c])
print(f"At: {pp(env)}  {st(env)}")
for i in range(6):
    prev=pp(env)
    r=env.step(A2)
    pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=0: note+=f' SHAPE->{shape}'
    if col!=2: note+=f' COL->{col}'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# From (44,30): probe LEFT
print("=== From (44,30): probe LEFT ===")
env,r=fresh()
for c in 'LLLDDDLDDLL': r=env.step(AMAP[c])
for i in range(8):
    prev=pp(env)
    r=env.step(A3)
    pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=0: note+=f' SHAPE->{shape}'
    if col!=2: note+=f' COL->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos[0]==24: print(f"  ** REACHED col 24 at {pos}! **")

print()
# From (44,35): probe LEFT
print("=== Navigate to (44,35) and probe LEFT ===")
# (44,35) is reachable — how?
# From (54,35): (54,35) is in the BFS list, going LEFT
env,r=fresh()
# Get to (54,35): from (54,20) go DOWN
for c in 'LLLDDDLDDLLU': r=env.step(AMAP[c])  # → (34,25) teleport
print(f"After LLLDDDLDDLLU: {pp(env)}")
# Hmm, let me just try a direct trace to (54,35)
env,r=fresh()
# From start: LEFT 3 → (39,5), DOWN → (39,10), (39,15), (39,20), LEFT → teleport (54,20), DOWN x3
for c in 'LLLDDDLDDDD': r=env.step(AMAP[c])
print(f"After LLLDDDLDDDD: {pp(env)}  {st(env)}")

print()
# Let me try: find path to (24,30) by going through col 24 from below
# From (24,45) going UP
print("=== Navigate to (24,45) and go UP ===")
# (24,45) is reachable. From (14,45) going RIGHT, or from (29,45) going LEFT?
# Let me find a path to (24,45)
env,r=fresh()
# From start, go LEFT x3, DOWN to (39,20), RIGHT teleport to (44,45), RIGHT to (49,45)→(54,45)?
# Wait we found (44,45) via teleport from (39,20)+RIGHT, and then RIGHT goes to (49,45)→(54,45)
# From (44,45): can we go LEFT? No (blocked). Go UP→teleport (34,40).
# Let me try from (34,40): go LEFT
for c in 'LLLDDDRU': r=env.step(AMAP[c])  # to (34,40) via teleport
print(f"After LLLDDDRU: {pp(env)}  {st(env)}")
for i in range(8):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=0: note+=f' SHAPE->{shape}'
    if col!=2: note+=f' COL->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos[0]<=24: print(f"  ** Reached col ≤24 at {pos}! **")

print()
# From (34,40): go DOWN
env,r=fresh()
for c in 'LLLDDDRU': r=env.step(AMAP[c])
print(f"At (34,40): {pp(env)}")
for i in range(8):
    prev=pp(env)
    r=env.step(A2)  # DOWN
    pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=0: note+=f' SHAPE->{shape}'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# Navigate toward (14,5): the target approach
# (14,5) is reachable. Let me find a path.
# From (19,5) going RIGHT → (24,5)?
# (19,5) and (24,5) are in the BFS list!
# From (14,5) going RIGHT gives (19,5). So going LEFT from (19,5) gives (14,5).
# And from (14,5) going LEFT gives (9,5) when win conditions met.

# Find path to (14,5):
# BFS positions near top: (14,5), (19,5), (24,5), (34,10), (34,15), (39,5)
# From (39,5) going LEFT? Let's try...
print("=== From (39,5): trace LEFT ===")
env,r=fresh()
for c in 'LLL': r=env.step(AMAP[c])  # to (39,5)
print(f"At: {pp(env)}")
for i in range(5):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# From (34,10): going LEFT
print("=== Navigate to (34,10) and go LEFT ===")
env,r=fresh()
# (34,10) is at col 34 row 10. From (39,10) going LEFT?
for c in 'LLLD': r=env.step(AMAP[c])  # LLL: (39,5), D: (39,10)
print(f"At: {pp(env)}")
r=env.step(A3)  # LEFT from (39,10)
print(f"LEFT from (39,10): {pp(env)}")
for i in range(5):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    steps=env._game._step_counter_ui.current_steps
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=0: note+=f' SHAPE->{shape}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos[0]<=14: print(f"  ** Reached col ≤14 at {pos}! **")
