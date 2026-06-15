"""ls20 L4: probe all exits from (24,30) after shape toggle, and path to color toggle x3."""
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

def trace(label, path_str):
    env,r=fresh()
    print(f"\n=== {label}: '{path_str}' ===")
    prev_col=env._game.hiaauhahz; prev_shape=env._game.fwckfzsyc
    for i,c in enumerate(path_str):
        prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
        if shape!=prev_shape: notes.append(f'SHAPE {prev_shape}->{shape}')
        if steps==42 and prev!=(54,5): notes.append('PICKUP/RESET')
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if col==1 and shape==5: print(f"      *** READY TO WIN (col=1=blue, shape=5) ***")
        prev_col=col; prev_shape=shape
    print(f"  Final: {pp(env)}  {st(env)}")
    return env

# Path to (24,30) after shape toggle = LLLDDLLLLDLDDDRRUUU (19 moves)
# This uses pickup at (19,15) on move 8 (counter=35)
# After 19 moves: steps = 42-19 = 23

# Probe all 4 exits from (24,30)
BASE='LLLDDLLLLDLDDDRRUUU'

for direction, action, dname in [(A1,'U','UP'),(A2,'D','DOWN'),(A3,'L','LEFT'),(A4,'R','RIGHT')]:
    env,r=fresh()
    go(env, BASE)
    print(f"\nAt (24,30) after {BASE}: {pp(env)}  {st(env)}")
    assert pp(env)==(24,30), f"Expected (24,30), got {pp(env)}"
    for i in range(10):
        prev=pp(env); r=env.step(action); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape!=5: notes.append(f'SHAPE->{shape}')
        if steps==42 and prev!=(54,5): notes.append('PICKUP/RESET')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(34,30): print(f"      *** REACHED COLOR TOGGLE (34,30)! ***")

# Now trace: can we reach color toggle from (24,30) efficiently?
print("\n\n=== After shape toggle, path to color toggle? ===")
# Color toggle at (34,30). From (24,30) go RIGHT?
# Or we can go via the known route: UP+DOWN teleport + known path?
# Let's try: from (24,30) D to (24,35), then trace RIGHT
trace("From (24,30) D then R", BASE+'DR')
trace("From (24,30) D then L", BASE+'DL')
trace("From (24,30) D then DDD", BASE+'DDDDD')

# Also: from (24,35) where do the teleporters lead?
print("\n=== From (24,35): all directions ===")
for direction, action, dname in [(A1,'U','UP'),(A2,'D','DOWN'),(A3,'L','LEFT'),(A4,'R','RIGHT')]:
    env,r=fresh()
    go(env, BASE+'D')
    print(f"At {pp(env)} after {BASE}D:")
    assert pp(env)==(24,35), f"Expected (24,35), got {pp(env)}"
    prev=pp(env); r=env.step(action); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    if col!=2: notes.append(f'COL->{col}')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  {dname}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")

# Try: from (9,40) what directions?
print("\n=== From (9,40): all directions ===")
# Navigate to (9,40): LLLDDLLLLDLDDDRRUULD (from (24,35) going left twice?)
# After BASE, at (24,30). D gives (24,35). L gives (19,35)? or from (24,45) UP gives (9,40)
# Simpler: from (24,45) UP → (9,40). So path = LLLDDLLLLDLDDDRRU = 17 steps to (24,45), then U = (9,40)
for direction, action, dname in [(A1,'U','UP'),(A2,'D','DOWN'),(A3,'L','LEFT'),(A4,'R','RIGHT')]:
    env,r=fresh()
    go(env, 'LLLDDLLLLDLDDDRRU')
    print(f"At {pp(env)}: {dname}")
    assert pp(env)==(9,40), f"Expected (9,40), got {pp(env)}"
    prev=pp(env); r=env.step(action); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    if col!=2: notes.append(f'COL->{col}')
    if shape!=4: notes.append(f'SHAPE->{shape}')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  {dname}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")

# KEY QUESTION: from (24,30) can we efficiently reach (34,30) for the color toggle?
# Then after 3 hits: col goes 2→3→0→1 (blue)
# Then from col=1, shape=5, navigate to target (9,5)

# Let's try reaching the color toggle 3 times starting from shape toggle
print("\n\n=== Attempt: hit color toggle 3 times after shape toggle ===")
# Hypothesis: from (24,30), go RIGHT to reach (34,30) via some path
# Let's check what's RIGHT from (24,30): it might be open path to (29,30)→(34,30) color toggle!
env,r=fresh()
go(env, BASE)
print(f"At (24,30) after shape: {pp(env)} col={env._game.hiaauhahz} shape={env._game.fwckfzsyc} steps={env._game._step_counter_ui.current_steps}")
# Probe RIGHT extensively
for i in range(6):
    prev=pp(env); r=env.step(A4); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    if col!=2: notes.append(f'COL->{col}')
    if pos==(34,30): notes.append('COLOR TOGGLE!')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
