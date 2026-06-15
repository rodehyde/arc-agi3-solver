"""ls20 L4: full BFS to find all reachable positions, toggle events, and winning path."""
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
    return (pp(env), g.hiaauhahz, pkups)  # no rot needed (goal rot=0=start rot)

env0,r0=fresh_l4()
init=get_state(env0)
print(f"Start: pos={init[0]}  col={init[1]}  pickups={init[2]}")
print(f"Goal: pos=(9,5)  col=1 (blue)")
print()

visited={init: []}
queue=deque([([], init)])
wins=[]
col_toggle_events=[]
MAX_DEPTH=120

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

        # Detect reset (player back at start with col_idx=2)
        if npos==(54,5) and ns[1]==2 and state[0]!=(54,5):
            continue  # dead end — counter reset

        # Track color toggle events
        if ns[1] != state[1]:
            col_toggle_events.append((path+[a], ns))
            if ns[1] in (1,) or len(col_toggle_events) <= 50:  # print first arrivals at col=1
                print(f"COL toggle at step {len(path)+1}: pos={npos}  col={ns[1]}  path={''.join(ANAMES[m] for m in path+[a])}")

        if ns not in visited:
            visited[ns] = path+[a]
            queue.append((path+[a], ns))

print(f"\nTotal states explored: {len(visited)}")
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
    # Show positions that reached col=1 (blue)
    blue_states=[s for s in visited if s[1]==1]
    print(f"States with col=1 (blue): {len(blue_states)}")
    if blue_states:
        blue_pos=sorted(set(s[0] for s in blue_states))
        print("Positions reachable with col=1:")
        for pos in blue_pos:
            print(f"  {pos}")
