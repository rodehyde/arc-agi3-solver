"""ls20 L4: find exit from (14,45) area and route from shape cluster to color toggle."""
import logging
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}

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
    for c in path_str: env.step(AMAP[c])

def probe4(label, path_to, expected=None):
    print(f"\n=== {label} [path={path_to}] ===")
    for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
        env,r=fresh()
        go(env, path_to)
        if expected:
            assert pp(env)==expected, f"Expected {expected}, got {pp(env)}"
        cur=pp(env)
        prev=cur; r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape not in (4,5): notes.append(f'SHAPE->{shape}')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==(34,30): print(f"      *** COLOR TOGGLE (34,30) ***")

# First: probe (14,45)
# Path: LLLDDLLLLDLDDDRRUUUD (BASE + D from (24,30) to (24,35), then L teleports to (19,45), then L to (14,45))
# Actually from (24,35) LEFT → (19,45), then LEFT → (14,45):
BASE_SHAPE='LLLDDLLLLDLDDDRRUUU'  # to (24,30), shape=5
# From (24,30): D→(24,35), L→(19,45), L→(14,45)
PATH_14_45 = BASE_SHAPE + 'DLL'
probe4("exits from (14,45)", PATH_14_45, (14,45))

# (14,45) going DOWN: expected (14,50)
print("\n=== From (14,45): trace DOWN chain ===")
env,r=fresh()
go(env, PATH_14_45)
assert pp(env)==(14,45), f"Expected (14,45), got {pp(env)}"
for i in range(8):
    prev=pp(env); r=env.step(A2); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    if col!=2: notes.append(f'COL->{col}')
    if shape not in (4,5): notes.append(f'SHAPE->{shape}')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(34,50): print(f"      *** (34,50) — can go UP to color toggle area ***")

# From (14,50): trace RIGHT and UP
print("\n=== From (14,50): all directions ===")
PATH_14_50 = PATH_14_45 + 'D'
probe4("exits from (14,50)", PATH_14_50, (14,50))

# From (14,50) trace RIGHT chain
print("\n=== From (14,50): trace RIGHT chain ===")
env,r=fresh()
go(env, PATH_14_50)
for i in range(10):
    prev=pp(env); r=env.step(A4); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    if col!=2: notes.append(f'COL->{col}')
    if shape not in (4,5): notes.append(f'SHAPE->{shape}')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(34,50): print(f"      *** (34,50) ***")

# Can we reach (34,30) = color toggle from the bottom?
# From (34,50) going UP
PATH_34_50 = PATH_14_50 + 'RRRRR'  # try
print(f"\n=== After {PATH_34_50}: check position ===")
env,r=fresh(); go(env, PATH_34_50)
print(f"After {PATH_34_50}: {pp(env)} {st(env)}")

# Alternative: from the bottom row, navigate to (34,30)
# Let's trace from (29,50): all directions
# Also check (34,45)→(34,40)→(34,35)→(34,30) possible?

# Find path to (34,50):
print("\n=== Find (34,50): check various paths ===")
for path in ['LLLDDLLLLDLDDDRRUUUDLDRRRR',
             'LLLDDLLLLDLDDDRRUUUDLDRRRRR',
             'LLLDDLLLLDLDDDRRUUUDLDRRRRRRR']:
    env,r=fresh(); go(env, path)
    print(f"After {path}: {pp(env)} {st(env)}")

# What if we combine: col toggle FIRST (17 moves), then shape toggle?
# Color toggle x3: LLLDDDLDDLLUDUDUDUD? Let me check what the minimal path to col=1 is.
# Pattern: 13+2+2=17 moves: LLLDDDLDDLLUD + UD + UD
print("\n=== Color toggle x3 then navigate to shape toggle ===")
COL3 = 'LLLDDDLDDLLUDUDUDUD'
# Wait: LLLDDDLDDLLUD (13) + UD (2) + UD (2) = 17... but second UD starts from (34,30)
# LLLDDDLDDLLUD → at (34,30) col=3, step 13
# UD → at (34,30) col=0, step 15
# UD → at (34,30) col=1, step 17
# Wait, U goes to (34,25) and D comes back to (34,30). Each UD = 2 moves.
def trace_full(path_str):
    env,r=fresh()
    prev_col=env._game.hiaauhahz; prev_shape=env._game.fwckfzsyc
    for i,c in enumerate(path_str):
        prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
        if shape!=prev_shape: notes.append(f'SHAPE {prev_shape}->{shape}')
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if col==1 and shape==5: print(f"      *** READY TO WIN (col=1=blue, shape=5) ***")
        prev_col=col; prev_shape=shape
    print(f"  Final: {pp(env)} col={env._game.hiaauhahz} shape={env._game.fwckfzsyc} steps={env._game._step_counter_ui.current_steps}")

print("\n=== Path: color toggle x3 then navigate to (24,45) for shape toggle ===")
# After 3x color toggle (17 moves, at (34,30) col=1, steps=25):
# Need to get to (24,45) to then do UUU for shape toggle
# From (34,30): UP to (34,25), then navigate...
# From (34,25): what exits?
probe4("exits from (34,25) [after color toggle]", 'LLLDDDLDDLLUD', (34,30))
# wait that goes to (34,30). Let me go to (34,25)
print("\n=== exits from (34,25) ===")
for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env,r=fresh()
    go(env, 'LLLDDDLDDLLU')  # 12 moves to (34,25) via teleport
    assert pp(env)==(34,25), f"Expected (34,25), got {pp(env)}"
    prev=pp(env); r=env.step(act); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  {dname}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")

# Check: from (34,25) going UP or LEFT might open a new path
print("\n=== From (34,25): trace UP and LEFT chains ===")
for act, dname in [(A1,'UP'),(A3,'LEFT')]:
    env,r=fresh()
    go(env, 'LLLDDDLDDLLU')
    for i in range(8):
        prev=pp(env); r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(24,45): print(f"      *** REACHED (24,45) — shape toggle via UUU ***")
