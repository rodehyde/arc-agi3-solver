"""ls20 L4: probe col-9 corridor and gbvqrjtaqo at (8,35) teleporter; find path to target (9,5)."""
import logging, numpy as np
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
def st(env): g=env._game; return f"col={g.hiaauhahz} steps={g._step_counter_ui.current_steps}"

def go_to(path_str):
    env,r=fresh()
    for c in path_str:
        r=env.step(AMAP[c])
    return env,r

def note_jump(prev, pos):
    if pos==prev: return ' BLOCKED'
    if abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: return f' TELEPORT'
    return ''

# First: find a path to reach col 9 positions
# From BFS: (9,25), (9,30), (9,40) are reachable
# Find paths to these

# From the BFS COL toggle path: LLLDDDLDDLLUD reaches (34,30) in 13 moves
# Let me trace this path first and understand the maze
print("=== Tracing BFS first COL toggle path: LLLDDDLDDLLUD ===")
env,r=fresh()
print(f"Start: {pp(env)}  {st(env)}")
for i,c in enumerate('LLLDDDLDDLLUD'):
    prev=pp(env)
    r=env.step(AMAP[c])
    pos=pp(env)
    print(f"  {i+1:2d} {c}: {prev}->{pos}  {st(env)}{note_jump(prev,pos)}")

print()
print("=== From (34,30) after 1st toggle (col=3): trace all directions ===")
for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=go_to('LLLDDDLDDLLUD')
    prev=pp(env2)
    r2=env2.step(action)
    pos=pp(env2)
    col=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    print(f"  {name}: {prev}->{pos}  col={col}  steps={steps}{note_jump(prev,pos)}")

# Now try to find path to col 9 from the toggle at (34,30)
print()
print("=== From (34,30): go toward col 9 ===")
# After 1 toggle hit (col=3), need 2 more hits (col=0, col=1)
# But first let's see how to get to col 9 from (34,30)
# Going LEFT from (34,30):
env,r=go_to('LLLDDDLDDLLUD')
print(f"At: {pp(env)}  {st(env)}")
for i in range(10):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    if col!=3: note+=f' COL->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
# Going UP from (34,30):
env,r=go_to('LLLDDDLDDLLUD')
print(f"At: {pp(env)}  {st(env)} — going UP:")
for i in range(8):
    prev=pp(env)
    r=env.step(A1)  # UP
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    if col!=3: note+=f' COL->{col}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
# From BFS reachable positions at col 9: (9,25), (9,30), (9,40)
# Find what happens going UP from each
for target_pos, nav_path, label in [
    ((9,25), None, 'target (9,25) - find via BFS trace'),
    ((9,30), None, 'target (9,30)'),
    ((9,40), None, 'target (9,40)'),
]:
    print(f"\n=== Finding path to {target_pos} ===")

# The BFS found (9,25): let's find what path gets there
# Try: from LLLDDDLDDLLUD→UP direction chain
print("=== Trace: LLLDDDLDDLLUDUDUDUD (3 toggle hits → col=1) then explore ===")
env,r=go_to('LLLDDDLDDLLUDUDUD')
print(f"After 3 toggles: {pp(env)}  col={env._game.hiaauhahz}  steps={env._game._step_counter_ui.current_steps}")
print("Going UP from here:")
for i in range(8):
    prev=pp(env)
    r=env.step(A1)  # UP
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    print(f"  UP {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break
print("Going LEFT from there:")
for i in range(8):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# Probe from (9,40) - a reachable position
# Find a path that reaches (9,40)
# Navigate: LLLDDD R [teleport to 44,45] UP [teleport to 34,40]
# No: (44,45) UP → (34,40), then explore
print()
print("=== From (34,40) [via LLLDDDRUP]: probe all directions ===")
for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=go_to('LLLDDDRUP')
    assert pp(env2)==(34,40), f"Expected (34,40), got {pp(env2)}"
    prev=pp(env2)
    r2=env2.step(action)
    pos=pp(env2)
    col=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    print(f"  {name}: {prev}->{pos}  col={col}  steps={steps}{note_jump(prev,pos)}")

print()
print("=== Tracing from (34,40): find path to col 9 ===")
env,r=go_to('LLLDDDRUP')
print(f"At: {pp(env)}  {st(env)}")
# Going LEFT from (34,40)
for i in range(12):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

print()
print("=== Probing (9,40): what happens going UP? ===")
# Need to find a path to (9,40) first
# From (34,40) going LEFT: let's see if we reach (9,40)
env,r=go_to('LLLDDDRUP')
# go left from (34,40) until reaching col 9
path_used = ''
for i in range(10):
    prev=pp(env)
    r=env.step(A3)
    pos=pp(env)
    path_used+=ANAMES[A3]
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=note_jump(prev,pos)
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos[0]==9:  # reached col 9
        print(f"  ** Reached col 9 at {pos}! Now going UP: **")
        for j in range(8):
            prev2=pp(env)
            r=env.step(A1)  # UP
            pos2=pp(env)
            col2=env._game.hiaauhahz
            steps2=env._game._step_counter_ui.current_steps
            note2=note_jump(prev2,pos2)
            print(f"    UP {j+1}: {prev2}->{pos2}  col={col2}  steps={steps2}{note2}")
            if pos2==prev2: break
        break
    if pos==prev:
        print("  BLOCKED before reaching col 9")
        break

print()
print("=== ttfwljgohq at (24,30): what is it? ===")
# The BFS found (24,30) is reachable. Find a path to it.
# Looking at BFS toggle path LLLDDDLDDLLUD: after LLL we're at (39,5), DDD→(39,20), L→teleport(54,20)...
# let me try to approach (24,30) from nearby positions
# (24,30) is near (24,25) and (24,35) which are also reachable
# From (34,30) go LEFT
env,r=go_to('LLLDDDLDDLLUD')  # at (34,30) col=3
print(f"At: {pp(env)}  {st(env)}")
prev=pp(env)
r=env.step(A3)  # LEFT
pos=pp(env)
print(f"  LEFT from (34,30): {prev}->{pos}  col={env._game.hiaauhahz}  steps={env._game._step_counter_ui.current_steps}")
# Check if we're at (29,30)
r=env.step(A3)  # LEFT again
pos2=pp(env)
print(f"  LEFT again: {pos}->{pos2}  col={env._game.hiaauhahz}  steps={env._game._step_counter_ui.current_steps}")
# Check grid changes at ttfwljgohq
