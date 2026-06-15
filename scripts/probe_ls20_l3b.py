"""ls20 L3: probe from (34,5) after teleport; probe second gbvqrjtaqo; find toggle paths."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']

def fresh_l3():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)
def st(env): g=env._game; return f"rot={g.cklxociuu} col={g.hiaauhahz} steps={g._step_counter_ui.current_steps}"

# GET TO (34,5) via teleport: 7 UPs
def to_teleport():
    env,r=fresh_l3()
    for _ in range(7): r=env.step(A1)  # UP to (9,10)
    r=env.step(A1)  # UP 8: teleport to (34,5)
    return env,r

env,r=to_teleport()
print(f"After teleport: pos={pp(env)}  {st(env)}")
print()

# From (34,5): probe all 4 directions
print("From (34,5) — probe all 4 directions:")
for a,name in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
    env2,r2=to_teleport()
    r2=env2.step(a)
    print(f"  {name}: pos={pp(env2)}  {st(env2)}")
print()

# Navigate from (34,5) rightward toward rotation toggle at (49,10)
print("From (34,5): explore RIGHT path toward toggle (49,10):")
env2,r2=to_teleport()
path='RRDDDDDD'  # right to col 49, down to row 10?
prev=pp(env2)
for i,c in enumerate(path):
    r2=env2.step(AMAP[c])
    pos=pp(env2)
    rot=env2._game.cklxociuu
    col_idx=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    note=' *** ROT CHANGED' if rot!=0 else ''
    note+=' *** COLOR CHANGED' if col_idx!=0 else ''
    print(f"  {i+1} {c}: pos={pos}  rot={rot}  col={col_idx}  steps={steps}{note}")
    prev=pos
print()

# Try reaching (49,10) from (34,5) more directly
print("From (34,5): try RRRDDDDDDDDDDD to reach toggle area:")
env2,r2=to_teleport()
path2='RRRDDDDDDDDDDDD'
for i,c in enumerate(path2):
    r2=env2.step(AMAP[c])
    pos=pp(env2)
    rot=env2._game.cklxociuu
    col_idx=env2._game.hiaauhahz
    steps=env2._game._step_counter_ui.current_steps
    note=' *** ROT' if rot!=0 else ''
    note+=' *** COL' if col_idx!=0 else ''
    print(f"  {i+1} {c}: pos={pos}  rot={rot}  col={col_idx}  steps={steps}{note}")
print()

# Check second gbvqrjtaqo at (54,4): approach from below
print("Testing second gbvqrjtaqo at (54,4): go UP from (54,5):")
env2,r2=to_teleport()
# From (34,5), go RIGHT to col 54?
for _ in range(4): r2=env2.step(A4)  # try right x4
print(f"  After 4 RIGHT from (34,5): pos={pp(env2)}")
# Try going UP from wherever we are
r2=env2.step(A1)
print(f"  Then UP: pos={pp(env2)}  {st(env2)}")
print()

# Can we reach color toggle at (29,45) from above?
print("Searching for path to color toggle (29,45):")
print("From (34,5), go LEFT to col 29, then DOWN to row 45?")
env2,r2=to_teleport()
# Try: left 1 to (29,5), then down
r2=env2.step(A3)  # LEFT
print(f"  LEFT from (34,5): pos={pp(env2)}")
for i in range(9):
    r2=env2.step(A2)  # DOWN
    col_idx=env2._game.hiaauhahz
    pos=pp(env2)
    print(f"  DOWN {i+1}: pos={pos}  col={col_idx}  steps={env2._game._step_counter_ui.current_steps}")
    if col_idx != 0:
        print(f"    *** COLOR TOGGLE HIT at {pos} ***")
        break
