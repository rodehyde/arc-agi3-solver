"""ls20 L3: full BFS to map all reachable positions and find both toggles."""
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

def fresh_l3():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)

def get_state(env):
    g=env._game
    sp_set=frozenset(
        (sp.x,sp.y) for sp in env._game.current_level.get_sprites()
        if sp.tags and 'npxgalaybz' in sp.tags
    )
    return (pp(env), g.cklxociuu, g.hiaauhahz, sp_set)

# BFS tracking (pos, rot, color, pickups) — no step counter (infinite budget assumed for exploration)
env0,r0=fresh_l3()
init=get_state(env0)
print(f"Start: pos={init[0]}  rot={init[1]}  col={init[2]}  pickups={init[3]}")

visited={init: []}
queue=deque([([], init)])
wins=[]
toggle_rot_events=[]
toggle_col_events=[]
MAX_DEPTH=80

while queue:
    path, state = queue.popleft()
    if len(path) >= MAX_DEPTH: continue

    for a in [A1,A2,A3,A4]:
        env2,r2=fresh_l3()
        for m in path: r2=env2.step(m)
        r2=env2.step(a)

        if r2.levels_completed > 2:
            wins.append(path+[a])
            print(f"WIN in {len(path)+1} moves: {''.join(ANAMES[m] for m in path+[a])}")
            continue

        ns=get_state(env2)
        npos=ns[0]
        if npos is None: continue

        # Detect resets (counter depleted — player back at start with rot/col reset)
        if npos==(9,45) and ns[1]==0 and ns[2]==0 and state[0]!=(9,45):
            continue  # dead end — counter reset

        # Track toggle events
        if ns[1] != state[1]:
            toggle_rot_events.append((path+[a], ns))
            print(f"ROT toggle at step {len(path)+1}: pos={npos}  rot={ns[1]}  path={''.join(ANAMES[m] for m in path+[a])}")
        if ns[2] != state[2]:
            toggle_col_events.append((path+[a], ns))
            print(f"COL toggle at step {len(path)+1}: pos={npos}  col={ns[2]}  path={''.join(ANAMES[m] for m in path+[a])}")

        if ns not in visited:
            visited[ns] = path+[a]
            queue.append((path+[a], ns))

print(f"\nTotal states explored: {len(visited)}")
print(f"Rotation toggle events: {len(toggle_rot_events)}")
print(f"Color toggle events: {len(toggle_col_events)}")

# Print unique positions reachable
all_pos=set(state[0] for state in visited)
print(f"Unique positions: {len(all_pos)}")
print("\nAll reachable positions (sorted):")
for pos in sorted(all_pos):
    print(f"  {pos}")

if wins:
    best=min(wins,key=len)
    print(f"\nBest solution: {len(best)} moves: {''.join(ANAMES[a] for a in best)}")
