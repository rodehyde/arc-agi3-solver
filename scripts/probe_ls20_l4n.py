"""ls20 L4: trace path from (9,40) UP through col-14 corridor to target (9,5)."""
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
        if r.levels_completed>3: notes.append('*** WIN ***')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {i+1:2d} {c}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if col==1 and shape==5: print(f"      *** READY TO WIN (col=1=blue, shape=5) ***")
        prev_col=col; prev_shape=shape
    print(f"  Final: {pp(env)} col={env._game.hiaauhahz} shape={env._game.fwckfzsyc} steps={env._game._step_counter_ui.current_steps}")
    return env,r

# Path from (9,40) through col-14 UP corridor to target
# (9,40) → R→(14,40) → UP chain to (14,5) → L→(9,5)
print("=== (9,40) -> RIGHT -> UP chain through col-14 ===")
env,r=fresh()
go(env, 'LLLDDLLLLDLDDDRRU')  # to (9,40)
assert pp(env)==(9,40), f"Expected (9,40), got {pp(env)}"
print(f"At (9,40): {st(env)}")
r=env.step(A4)  # RIGHT
print(f"R: {pp(env)}")
for i in range(15):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(14,5): print(f"      *** AT (14,5) ***")

print()
# After reaching (14,5), go LEFT to target
print("=== From (14,5): go LEFT ===")
env,r=fresh()
# Navigate: LLLDDLLLLDLDDDRRU = to (9,40), R = (14,40), then 8 UPs to (14,5)
go(env, 'LLLDDLLLLDLDDDRRURUUUUUUU')
print(f"After LLLDDLLLLDLDDDRRURUUUUUUU: {pp(env)} {st(env)}")
r=env.step(A3)
print(f"LEFT: {pp(env)} {st(env)} levels={r.levels_completed}")

# Key question: what does shape toggle → (9,40) path look like?
# After shape toggle (24,30), only D exit, then D to (9,40), then R+(UP chain)
print()
trace("Shape toggle + path to target",
      'LLLDDLLLLDLDDDRRUUUDDR' + 'RUUUUUUUUL')
# Shape toggle = LLLDDLLLLDLDDDRRUUU (19), then D=(24,35), D=(9,40), R=(14,40), UP×8=(14,5), L=(9,5)
# Full = LLLDDLLLLDLDDDRRUUU + DD + RUUUUUUUUL
print()
trace("Full: shape toggle then target (ignoring col)",
      'LLLDDLLLLDLDDDRRUUUDDR' + 'UUUUUUUUL')

# Now try: shape toggle + color toggle x3 + target
# Key: from (24,30) after shape toggle, how to reach (34,30)?
# We established: (24,30) → D → (24,35) → D → (9,40) → R → (14,40) → ...
# From (14,40) → can we go UP to (14,35)? Then (14,35) → UP → (14,30) → UP → (14,25) → ...
# But the color toggle is at (34,30).
# From col-14 corridor, going RIGHT at any level?

print()
print("=== From col-14 corridor: trace RIGHT at various levels ===")
for y in [10,15,20,25,30,35,40]:
    # Navigate to (14,y) via LLLDDLLLL+D to (14,20) then more Ds
    n_d_from_20 = (y-20)//5
    if y <= 20:
        n_d_to_39_15 = 2
        n_l_to_14 = 4 + (15-y)//5 if y<=15 else 0
        # This is getting complex, let me just use a direct approach
        pass
    env,r=fresh()
    # Go to (14,y) via LLLDDLLLLD+L+D*(y-20)//5 (for y>=20)
    if y >= 20:
        path = 'LLLDDLLLLD' + 'L' + 'D'*((y-20)//5)
    else:
        path = 'LLLDD' + 'L'*((39-14)//5) + 'D'*(0) + 'U'*((20-y)//5)
        # Actually this doesn't work cleanly
        path = 'LLLDDLLLLD' + 'L' + 'U'*((20-y)//5)
    go(env, path)
    pos=pp(env)
    if pos[0]==14:
        prev=pos; r=env.step(A4); npos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        tp=' [TELEPORT]' if abs(npos[0]-prev[0])>5 or abs(npos[1]-prev[1])>5 else ''
        blk=' [BLOCKED]' if npos==prev else ''
        print(f"  From (14,{y}): RIGHT → {npos}  col={col} shape={shape} steps={steps}{tp}{blk}")
    else:
        print(f"  (14,{y}): navigation failed, at {pos} after '{path}'")

print()
# Can we reach (44,30) or (34,30) from col-14?
# Try going RIGHT from (14,25) or (14,20) multiple times
print("=== From (14,20): trace RIGHT chain ===")
env,r=fresh()
go(env, 'LLLDDLLLLDL')  # to (14,20)
assert pp(env)==(14,20), f"Expected (14,20) got {pp(env)}"
for i in range(10):
    prev=pp(env); r=env.step(A4); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(34,30): print(f"      *** COLOR TOGGLE! ***")
    if pos==(24,30): print(f"      *** SHAPE TOGGLE! ***")
