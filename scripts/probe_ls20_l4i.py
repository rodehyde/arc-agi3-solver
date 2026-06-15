"""ls20 L4: find path to (24,30) via lower routes — probe (24,45), (24,50), (29,50)."""
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

def note_str(prev, pos, col, shape, steps):
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): notes.append('TELEPORT')
    if shape!=4: notes.append(f'SHAPE->{shape}')
    if col!=2: notes.append(f'COL->{col}')
    if steps==42 and prev!=(54,5): notes.append('PICKUP')
    return ('  ['+' | '.join(notes)+']') if notes else ''

def go(env, path_str):
    r=None
    for c in path_str: r=env.step(AMAP[c])
    return r

def trace_from(path_to, direction, action, limit=10):
    env,r=fresh()
    go(env, path_to)
    start=pp(env)
    print(f"At {start} after {path_to}:")
    for i in range(limit):
        prev=pp(env); r=env.step(action); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        n=note_str(prev,pos,col,shape,steps)
        print(f"  {direction} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(24,30): print(f"    *** REACHED SHAPE TOGGLE (24,30) ***")
        if pos==(24,35): print(f"    *** REACHED (24,35) — one UP gives shape toggle ***")

# Path to (19,45): LLLDDLLLLDLDDDR (15 steps, teleport at step 15)
# From (19,45) go RIGHT to (24,45)
print("=== From (24,45) [via teleport+R]: trace UP ===")
trace_from('LLLDDLLLLDLDDDRRR', 'UP', A1)  # LLLDDLLLLDLDDD→(14,35), R→(19,45), R→(24,45), R→(29,45)? -- let me verify
# Actually: LLLDDLLLLDLDDDR = 15 steps ends at (19,45), then RR = (24,45),(29,45)
# Let me trace LLLDDLLLLDLDDDRRR
env,r=fresh(); go(env,'LLLDDLLLLDLDDDRRR')
print(f"After LLLDDLLLLDLDDDRRR: {pp(env)}  {st(env)}")

print()
print("=== From (24,45) [via LLLDDLLLLDLDDDRR]: trace UP ===")
trace_from('LLLDDLLLLDLDDDRR', 'UP', A1)

print()
print("=== From (24,45): trace DOWN ===")
trace_from('LLLDDLLLLDLDDDRR', 'DOWN', A2)

print()
# Find path to (24,50)
# From (34,50) go LEFT twice: (34,50)→(29,50)→(24,50)
# Reach (34,50) via: LLLDDDRU+D+D (34,40)→(34,45)→(34,50)
print("=== Path to (34,50): via (34,40)→D→D ===")
env,r=fresh(); go(env,'LLLDDRUDD')
print(f"After LLLDDRUDD: {pp(env)}  {st(env)}")

print()
print("=== From (34,50): trace LEFT ===")
trace_from('LLLDDRUDD', 'LEFT', A3)

print()
print("=== From (24,50): trace UP ===")
# Need to reach (24,50) first
env,r=fresh()
go(env,'LLLDDRULDLL')  # LLLDDRULDLL: to (34,40) then ... let me calculate
# Actually: LLLDDR = LLL(39,5) D(39,10) D(39,15) D(39,20) R(44,45) -- wait LLLDDR is 6
# LLLDDRU = LLL(39,5) DD(39,15) D? wait
# Let me just trace LLLDDRULDLL
r2=env.observation_space
env2,r2=fresh()
print("Navigating to (24,50):")
steps=['L','L','L','D','D','R','U','D','D','L','L']
for c in steps:
    prev=pp(env2); r2=env2.step(AMAP[c]); pos=pp(env2)
    col=env2._game.hiaauhahz; shape=env2._game.fwckfzsyc; st_val=env2._game._step_counter_ui.current_steps
    n=note_str(prev,pos,col,shape,st_val)
    print(f"  {c}: {prev}->{pos}  {n}")
# Try reaching (24,50) via (29,50)
print()
print("From BFS: (29,50) is reachable too. LLLDDRUDDL to reach (29,50)?")
env,r=fresh(); go(env,'LLLDDRUDDL')
print(f"After LLLDDRUDDL: {pp(env)}  {st(env)}")
print("Going LEFT from (29,50):")
trace_from('LLLDDRUDDL', 'LEFT', A3)

print()
print("=== From (24,50): UP ===")
# Navigate to (24,50) properly: LLLDDRUDDLL
env,r=fresh(); go(env,'LLLDDRUDDLL')
print(f"After LLLDDRUDDLL: {pp(env)}  {st(env)}")
if pp(env)==(24,50):
    trace_from('LLLDDRUDDLL', 'UP', A1)
else:
    print(f"Not at (24,50), at {pp(env)}")
    # Continue: trace_from current pos UP
    for i in range(8):
        prev=pp(env); r=env.step(A1); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        n=note_str(prev,pos,col,shape,steps)
        print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(24,35): print(f"    *** REACHED (24,35) ***")
        if pos==(24,30): print(f"    *** REACHED SHAPE TOGGLE ***")
