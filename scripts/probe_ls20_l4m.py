"""ls20 L4: probe (19,45) exits, (34,25) exits, and find if shape cluster connects to color toggle area."""
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
    print(f"\n=== {label} [at {pp_from_path(path_to)}] ===")
    for act, dname in [(A1,'UP'),(A2,'DOWN'),(A3,'LEFT'),(A4,'RIGHT')]:
        env,r=fresh()
        go(env, path_to)
        if expected:
            got=pp(env)
            if got!=expected:
                print(f"  SKIP {dname}: expected {expected} but at {got}")
                continue
        prev=pp(env); r=env.step(act); pos=pp(env)
        col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
        notes=[]
        if pos==prev: notes.append('BLOCKED')
        elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
        if col!=2: notes.append(f'COL->{col}')
        if shape not in (4,5): notes.append(f'SHAPE->{shape}')
        n='  ['+' | '.join(notes)+']' if notes else ''
        print(f"  {dname}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
        if pos in [(34,30),(44,30),(54,20)]: print(f"      *** {pos} — color toggle route! ***")

def pp_from_path(p):
    env,r=fresh(); go(env, p); return pp(env)

# (19,45) — reached via: LLLDDLLLLDLDDDDDR (col-14 corridor + R) or via teleport
PATH_19_45 = 'LLLDDLLLLDLDDDDDR'
print(f"After {PATH_19_45}: {pp_from_path(PATH_19_45)}")
probe4("(19,45) exits", PATH_19_45, (19,45))

print("\n=== From (19,45): trace UP chain ===")
env,r=fresh(); go(env, PATH_19_45)
assert pp(env)==(19,45)
for i in range(10):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos in [(34,30),(44,30),(54,20),(34,25)]: print(f"      *** {pos} — color toggle route! ***")

print("\n=== From (19,45): trace DOWN chain ===")
env,r=fresh(); go(env, PATH_19_45)
for i in range(6):
    prev=pp(env); r=env.step(A2); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break

# (34,25) — junction on color toggle path
# Reached via LLLDDDLDDLLU (12 moves): UP from (44,30) teleports here
PATH_34_25 = 'LLLDDDLDDLLU'
print(f"\nAfter {PATH_34_25}: {pp_from_path(PATH_34_25)}")
probe4("(34,25) exits", PATH_34_25, (34,25))

print("\n=== From (34,25): trace LEFT chain ===")
env,r=fresh(); go(env, PATH_34_25)
assert pp(env)==(34,25)
for i in range(10):
    prev=pp(env); r=env.step(A3); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(24,45): print(f"      *** REACHED (24,45) — shape toggle via UUU ***")

print("\n=== From (34,25): trace UP chain ===")
env,r=fresh(); go(env, PATH_34_25)
for i in range(8):
    prev=pp(env); r=env.step(A1); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  UP {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(24,45): print(f"      *** REACHED (24,45) ***")

# Also probe (44,30) exits (on color toggle path — arrived via LL from (54,30))
PATH_44_30 = 'LLLDDDLDDLL'
print(f"\nAfter {PATH_44_30}: {pp_from_path(PATH_44_30)}")
probe4("(44,30) exits", PATH_44_30, (44,30))

print("\n=== From (44,30): trace LEFT chain ===")
env,r=fresh(); go(env, PATH_44_30)
for i in range(8):
    prev=pp(env); r=env.step(A3); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  LEFT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
    if pos==(24,45): print(f"      *** REACHED (24,45) ***")

# Most critical: probe (54,20) exits — this is the hub node
PATH_54_20 = 'LLLDDDL'
print(f"\nAfter {PATH_54_20}: {pp_from_path(PATH_54_20)}")
probe4("(54,20) exits [hub]", PATH_54_20, (54,20))

print("\n=== From (54,20): DOWN chain ===")
env,r=fresh(); go(env, PATH_54_20)
for i in range(10):
    prev=pp(env); r=env.step(A2); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  DOWN {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break

print("\n=== From (54,20): RIGHT chain ===")
env,r=fresh(); go(env, PATH_54_20)
for i in range(8):
    prev=pp(env); r=env.step(A4); pos=pp(env)
    col=env._game.hiaauhahz; shape=env._game.fwckfzsyc; steps=env._game._step_counter_ui.current_steps
    notes=[]
    if pos==prev: notes.append('BLOCKED')
    elif abs(pos[0]-prev[0])>5 or abs(pos[1]-prev[1])>5: notes.append('TELEPORT')
    n='  ['+' | '.join(notes)+']' if notes else ''
    print(f"  RIGHT {i+1}: {prev}->{pos}  col={col} shape={shape} steps={steps}{n}")
    if pos==prev: break
