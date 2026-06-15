"""ls20 L4: targeted probe — RIGHT from (14,35), and find path to (24,30)."""
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

def trace(path_str, stop_at=None):
    env,r=fresh()
    print(f"Tracing: {path_str}")
    for i,c in enumerate(path_str):
        prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): notes.append('TELEPORT')
        if shape!=4: notes.append(f'SHAPE->{shape}')
        if col!=2: notes.append(f'COL->{col}')
        if steps==42 and prev!=(54,5): notes.append('PICKUP')
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if shape==5 and col==1: print(f"    *** READY TO WIN ***")
        if stop_at and pos==stop_at: print(f"  ** REACHED {stop_at} **")
    return env,r

# Path to (14,35): LLLDDLLLLDLDDD (14 steps)
# Then R from (14,35)
print("=== RIGHT from (14,35): LLLDDLLLLDLDDDR ===")
trace('LLLDDLLLLDLDDDR')

print()
# Continue from (14,35)+R: keep going RIGHT
print("=== From (14,35): trace RIGHT then continue ===")
env,r=fresh()
for c in 'LLLDDLLLLDLDDD': r=env.step(AMAP[c])
assert pp(env)==(14,35), f"Expected (14,35), got {pp(env)}"
print(f"At (14,35): {st(env)}")
for i in range(8):
    prev=pp(env); r=env.step(A4); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    if col!=2: note+=f' COL->{col}'
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# Probe the area near (24,30) - try going from (19,40) upward
print("=== From (19,40) [via LLLDDLLLLDLDDDDR]: trace UP ===")
env,r=fresh()
for c in 'LLLDDLLLLDLDDDDR': r=env.step(AMAP[c])
print(f"At: {pp(env)}  {st(env)}")
for i in range(8):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# Try: from (19,40) going LEFT
print("=== From (19,40): trace LEFT ===")
env,r=fresh()
for c in 'LLLDDLLLLDLDDDDR': r=env.step(AMAP[c])
for i in range(6):
    prev=pp(env); r=env.step(A3); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos[0]<=24: print(f"    ** Col ≤24 reached: {pos}")

print()
# Probe from (19,45): go UP
print("=== From (19,45) [via LLLDDLLLLDLDDDDDR]: trace UP ===")
env,r=fresh()
for c in 'LLLDDLLLLDLDDDDDR': r=env.step(AMAP[c])
print(f"At: {pp(env)}  {st(env)}")
for i in range(10):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break

print()
# New approach: from (24,20) going DOWN - maybe teleporter at (25,40) redirects to (24,30)?
print("=== From (24,20): trace DOWN (through teleporter territory) ===")
env,r=fresh()
for c in 'LLLDDLLLLDR': r=env.step(AMAP[c])  # LLLDDLLLL to (19,15)+pickup, D to (19,20), R to (24,20)
print(f"At: {pp(env)}  {st(env)}")
for i in range(8):
    prev=pp(env); r=env.step(A2); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos==(24,30): print(f"    *** SHAPE TOGGLE AT (24,30)! ***")

print()
# Try from (29,15) going DOWN:
print("=== From (29,15): trace DOWN ===")
env,r=fresh()
for c in 'LLLDDLL': r=env.step(AMAP[c])  # LLLD→(39,5)→(39,10), DD→(39,15), LL→(29,15) wait...
# Actually LLLDDLL: LLL→(39,5), D→(39,10), D→(39,15), L→(34,15), L→(29,15)
print(f"At: {pp(env)}  {st(env)}")
for i in range(10):
    prev=pp(env); r=env.step(A2); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if shape!=4: note+=f' SHAPE->{shape}'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{note}")
    if pos==prev: break
    if pos[0]<=24: print(f"    ** Reached col ≤24 at {pos}")
