"""ls20 L4: focused probe — from (19,15), ttfwljgohq investigation, path to target."""
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
def st(env): g=env._game; return f"col={g.hiaauhahz} rot={g.cklxociuu} steps={g._step_counter_ui.current_steps}"

def go(env, r, path_str):
    for c in path_str:
        r=env.step(AMAP[c])
    return r

def at(path_str):
    """Navigate to a position and return env,r."""
    env,r=fresh()
    r=go(env,r,path_str)
    return env,r

def probe_all4(env, r, label):
    """Probe all 4 directions from current position."""
    pos=pp(env)
    print(f"\nFrom {pos} [{label}]  {st(env)}:")
    for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
        env2,r2=fresh()
        # replay state then probe
        path_to_here=[]  # we'll do it differently
        # use a simple approach: clone via path stored externally
        break
    # alternative: just probe from current env by saving/restoring
    # simplest: do each direction from a freshly navigated state
    return pos

def probe4(path_to, label):
    pos_check=None
    print(f"\nFrom {label}: probe all 4 directions")
    for action,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
        env2,r2=at(path_to)
        prev=pp(env2)
        r2=env2.step(action)
        pos=pp(env2)
        col=env2._game.hiaauhahz
        steps=env2._game._step_counter_ui.current_steps
        note=' BLOCKED' if pos==prev else ''
        if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
        if col!=2: note+=f' COL CHANGED->{col}'
        print(f"  {name}: {prev}->{pos}  col={col}  steps={steps}{note}")
    return

# Path to (19,15): LEFT x3 + DOWN x2 + LEFT x4
PATH_19_15 = 'LLLDDLLLL'

print("=== Probe from (19,15) (after pickup at 20,16 collected) ===")
probe4(PATH_19_15, '(19,15)')

# Path to continue down from (19,15)
print("\n=== From (19,15): trace DOWN ===")
env,r=at(PATH_19_15)
print(f"Start: {pp(env)}  {st(env)}")
for i in range(15):
    prev=pp(env)
    r=env.step(A2)  # DOWN
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    if steps==42 and prev!=(54,5): note+=' PICKUP/RESET'
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# Probe from (19,15): trace LEFT
print("\n=== From (19,15): trace LEFT ===")
env,r=at(PATH_19_15)
print(f"Start: {pp(env)}  {st(env)}")
for i in range(6):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# Navigate to the color toggle at (34,30) — approach from above
print("\n=== Finding path to color toggle (34,30) ===")
# From (39,15): go down to (39,20), then try LEFT
env,r=fresh()
r=go(env,r,'LLLDD')  # to (39,15)
print(f"At: {pp(env)}")
r=env.step(A2); print(f"DOWN: {pp(env)}")  # (39,20) or teleport
# try LEFT from (39,20)
for i in range(8):
    prev=pp(env)
    r=env.step(A3)
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# What about from (44,45) — teleport destination?
print("\n=== From (44,45) [teleport destination from (39,20)+RIGHT] ===")
probe4('LLLDDDR', '(44,45)')

# And from (44,45): trace UP
print("\n=== From (44,45): trace UP ===")
env,r=at('LLLDDDR')
print(f"Start: {pp(env)}  {st(env)}")
for i in range(15):
    prev=pp(env)
    r=env.step(A1)  # UP
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    if steps>env._game._step_counter_ui.osgviligwp-2: note+=' PICKUP'
    print(f"  UP {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# From (44,45): trace LEFT
print("\n=== From (44,45): trace LEFT ===")
env,r=at('LLLDDDR')
print(f"Start: {pp(env)}  {st(env)}")
for i in range(15):
    prev=pp(env)
    r=env.step(A3)  # LEFT
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break

# Navigate toward target at (9,5) via left corridor
print("\n=== Tracing toward target (9,5) from (19,15) going UP ===")
env,r=at(PATH_19_15)
print(f"Start: {pp(env)}  {st(env)}")
for i in range(5):
    prev=pp(env)
    r=env.step(A1)  # UP
    pos=pp(env)
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    note=' BLOCKED' if pos==prev else ''
    if pos!=prev and (abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5): note+=' TELEPORT'
    if col!=2: note+=f' COL CHANGED->{col}'
    print(f"  UP {i+1}: {prev}->{pos}  col={col}  steps={steps}{note}")
    if pos==prev: break
