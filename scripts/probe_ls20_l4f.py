"""ls20 L4: find path to (24,35)→(24,30) via col-14 corridor."""
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

def go(env, path_str):
    r=None
    for c in path_str:
        r=env.step(AMAP[c])
    return r

def trace_dir(env, action, name, limit=12):
    for i in range(limit):
        prev=pp(env)
        r=env.step(action)
        pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        note=' BLOCKED' if pos==prev else ''
        if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
        if shape!=4 and shape!=0: note+=f' SHAPE->{shape}'
        if col!=2: note+=f' COL->{col}'
        if steps==42 and prev!=(54,5): note+=' PICKUP'
        print(f"  {name} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
        if pos==prev: break

# Path: (19,15) via LLLDDLLLL
# From (19,15): go DOWN to (19,20), check RIGHT
print("=== From (19,20): probe all directions ===")
env,r=fresh(); go(env,'LLLDDLLLLD')
print(f"At: {pp(env)}  {st(env)}")
for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=fresh(); go(env2,'LLLDDLLLLD')
    prev=pp(env2); r2=env2.step(action); pos=pp(env2)
    col=env2._game.hiaauhahz; shape=env2._game.fwckfzsyc; steps=env2._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  {name}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")

print()
print("=== From (19,20): trace DOWN ===")
env,r=fresh(); go(env,'LLLDDLLLLD')
trace_dir(env, A2, 'DOWN')

print()
print("=== Navigate to (14,20) ===")
# From (19,20) go LEFT
env,r=fresh(); go(env,'LLLDDLLLLD')  # (19,20)
r=env.step(A3)
print(f"LEFT from (19,20): {pp(env)}")
if pp(env)==(14,20):
    print("At (14,20)!")
    print("Going DOWN from (14,20):")
    trace_dir(env, A2, 'DOWN')
    print()
    env2,r2=fresh(); go(env2,'LLLDDDLLLLD')
    print("Going RIGHT from (14,20):")
    trace_dir(env2, A4, 'RIGHT')

print()
print("=== From (14,25): go DOWN chain ===")
env,r=fresh(); go(env,'LLLDDDLLLLDD')  # try: LLL to (39,5), DDD to (39,20)→L teleport(54,20)→DD→(54,30)→LL→(44,30) ...
# Actually let me navigate more carefully
# Known path to (14,20): LLLDDLLLL+D+L = LLLDDLLLLD+L = LLLDDDLLLL (no...)
# Let me just step through: L×3→(39,5), D→(39,10), D→(39,15), D→(39,20), L→teleport(54,20),
# then navigate LEFT & DOWN
env,r=fresh()
path_so_far=''
steps_done=[]
print("Trying to reach (14,20):")
for c in 'LLLDDLLLL':
    prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
    steps_done.append((c,prev,pos))
    path_so_far+=c
print(f"  After {path_so_far}: {pp(env)}  {st(env)}")
# now at (19,15): go D to (19,20)
r=env.step(A2); print(f"  D: {pp(env)}")
# go L to (14,20)?
r=env.step(A3); print(f"  L: {pp(env)}")
pos=pp(env)
if pos==(14,20):
    print("  At (14,20). Probing all dirs:")
    for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
        env2,r2=fresh(); go(env2,'LLLDDDLLLLLL')  # should be LLLDDLLLLDL
        # just try manually
        break
    print("  Going DOWN from (14,20):")
    trace_dir(env, A2, 'DOWN', limit=15)

print()
print("=== Trying to find (24,35): go from (14,35) RIGHT ===")
# Navigate to (14,35) first: from (14,20) DOWN x3
env,r=fresh(); go(env,'LLLDDLLLLLD')  # try this
print(f"After LLLDDLLLLLD: {pp(env)}  {st(env)}")
if pp(env)==(14,20):
    go(env,'DDD')
    print(f"After DDD: {pp(env)}")
    go(env,'DD')
    print(f"After DD more: {pp(env)}")

# Let me try a manual longer trace to reach (14,35)
print()
env,r=fresh()
path='LLLDDDLLLLDL'  # add one L after the D
for c in path:
    prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
    jump='' if pos==prev or (abs(pos[0]-prev[0])<=5 and abs(pos[1]-prev[1])<=5) else ' TP'
    print(f"  {c}: {prev}->{pos}  steps={env._game._step_counter_ui.current_steps}{jump}")

print()
print("=== Key: trace from start to reach shape toggle (24,30) ===")
# Try: go via col 14 corridor downward
env,r=fresh()
# Path: LLLDDLLLLD to (19,20), then L to (14,20), then DDDDD
path='LLLDDLLLLLDDDDDDD'
print(f"Tracing {path}:")
for i,c in enumerate(path):
    prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): notes.append('TELEPORT')
    if shape!=4: notes.append(f'SHAPE->{shape}')
    if col!=2: notes.append(f'COL->{col}')
    if steps==42 and prev!=(54,5): notes.append('PICKUP')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if shape==5: print(f"  *** SHAPE TOGGLE HIT! ***")
