"""ls20 L4: probe exits from (24,30) after shape toggle — 4 directions, then path to (34,30) x3."""
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
    print(f"\n=== {label} ===")
    prev_col=env._game.hiaauhahz; prev_shape=env._game.fwckfzsyc
    for i,c in enumerate(path_str):
        prev=pp(env); r=env.step(AMAP[c]); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
        if shape!=prev_shape: notes.append(f'SHAPE {prev_shape}->{shape}')
        if steps>42-len(path_str[:i+1])+8 and prev!=(54,5): notes.append('PICKUP?')
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if col==1 and shape==5: print(f"      *** READY TO WIN (col=1=blue, shape=5) ***")
        prev_col=col; prev_shape=shape
    return env

# Shape toggle path: LLLDDLLLLDLDDDRRUUU (19 moves, pickup at move 9, steps=32 at end)
BASE='LLLDDLLLLDLDDDRRUUU'

# 4 exits from (24,30)
print("=== Probe 4 exits from (24,30) after shape toggle ===")
for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env,r=fresh()
    go(env, BASE)
    assert pp(env)==(24,30), f"Expected (24,30), got {pp(env)}"
    for i in range(8):
        prev=pp(env); r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape!=5: notes.append(f'SHAPE->{shape}')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(34,30): print(f"      *** COLOR TOGGLE (34,30) ***")
    print()

# From (24,30) go DOWN to (24,35) then probe exits from (24,35)
print("=== 4 exits from (24,35) [after DOWN from (24,30)] ===")
for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env,r=fresh()
    go(env, BASE+'D')
    assert pp(env)==(24,35), f"Expected (24,35), got {pp(env)}"
    for i in range(8):
        prev=pp(env); r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape!=5: notes.append(f'SHAPE->{shape}')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(34,30): print(f"      *** COLOR TOGGLE (34,30) ***")
    print()

# From (9,40): all 4 exits
print("=== 4 exits from (9,40) [via LLLDDLLLLDLDDDRRU] ===")
for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env,r=fresh()
    go(env, 'LLLDDLLLLDLDDDRRU')
    assert pp(env)==(9,40), f"Expected (9,40), got {pp(env)}"
    for i in range(8):
        prev=pp(env); r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape!=4: notes.append(f'SHAPE->{shape}')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname} {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos==prev: break
        if pos==(34,30): print(f"      *** COLOR TOGGLE (34,30) ***")
    print()

# Probe color toggle 3 times: what happens to the available routes?
# Known path to (34,30): LLLDDDLDDLLUD (13 moves)
print("=== Color toggle 3 times ===")
trace("3x color toggle", 'LLLDDDLDDLLUDLLLDDDLDDLLUDLLLDDDLDDLLUD')
