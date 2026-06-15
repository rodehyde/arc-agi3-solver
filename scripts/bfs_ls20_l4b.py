"""ls20 L4: BFS with full state (pos, col_idx, shape_idx, pickups) — find winning path."""
import logging, numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']
L3=[AMAP[c] for c in 'UUUUUUUULDDDDDDDDUUULLURRRRRRRUUULUDURD']

def fresh_l4():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2+L3: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)

def get_state(env):
    g=env._game
    pkups=frozenset(
        (sp.x,sp.y) for sp in env._game.current_level.get_sprites()
        if sp.tags and 'npxgalaybz' in sp.tags
    )
    return (pp(env), g.hiaauhahz, g.fwckfzsyc, pkups)

env0,r0=fresh_l4()
init=get_state(env0)
print(f"Start: pos={init[0]}  col={init[1]}  shape={init[2]}  pickups={init[3]}")
print(f"Goal: pos=(9,5)  col=1(blue)  shape=5")
print()

visited={init: []}
queue=deque([([], init)])
wins=[]
shape_toggle_events=[]
col_toggle_events=[]
MAX_DEPTH=130

while queue:
    path, state = queue.popleft()
    if len(path) >= MAX_DEPTH: continue

    for a in [A1,A2,A3,A4]:
        env2,r2=fresh_l4()
        for m in path: r2=env2.step(m)
        r2=env2.step(a)

        if r2.levels_completed > 3:
            wins.append(path+[a])
            print(f"WIN in {len(path)+1} moves: {''.join(ANAMES[m] for m in path+[a])}")
            continue

        ns=get_state(env2)
        npos=ns[0]
        if npos is None: continue

        # Detect reset (player back at start with starting col_idx=2, shape_idx=4)
        if npos==(54,5) and ns[1]==2 and ns[2]==4 and state[0]!=(54,5):
            continue  # dead end — counter reset

        # Track events
        if ns[2] != state[2]:
            shape_toggle_events.append((path+[a], ns))
            if len(shape_toggle_events) <= 10:
                print(f"SHAPE toggle at step {len(path)+1}: pos={npos}  shape={ns[2]}  path={''.join(ANAMES[m] for m in path+[a])}")
        if ns[1] != state[1] and (ns[1]==1 or len(col_toggle_events)<=5):
            print(f"COL toggle at step {len(path)+1}: pos={npos}  col={ns[1]}  path={''.join(ANAMES[m] for m in path+[a])}")

        if ns not in visited:
            visited[ns] = path+[a]
            queue.append((path+[a], ns))

print(f"\nTotal states explored: {len(visited)}")
print(f"Shape toggle events: {len(shape_toggle_events)}")
print(f"Color toggle events: {len(col_toggle_events)}")

all_pos=set(s[0] for s in visited)
print(f"Unique positions: {len(all_pos)}")
print("\nAll reachable positions (sorted):")
for pos in sorted(all_pos):
    print(f"  {pos}")

if wins:
    best=min(wins,key=len)
    print(f"\nBest solution: {len(best)} moves: {''.join(ANAMES[a] for a in best)}")
else:
    print("\nNo win found within depth limit")
    win_ready=[s for s in visited if s[1]==1 and s[2]==5]
    print(f"States with col=1(blue) AND shape=5: {len(win_ready)}")
    if win_ready:
        print("Positions with correct col+shape:")
        for s in sorted(set(s[0] for s in win_ready)):
            print(f"  {s}")
