"""ls20 L2: BFS tracking (pos, rot_idx, p1_taken, p2_taken) to find optimal win path."""
import logging, numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]

def fresh_l2():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    for a in L1: r=env.step(a)
    return env, r

def ppos(r):
    g=np.array(r.frame[-1]); ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

def rot_idx(env):
    return env._game.cklxociuu

def pickups_remaining(env):
    # returns (p1_present, p2_present) by checking if npxgalaybz sprites still exist
    sprites=list(env._game.current_level.get_sprites())
    positions=set()
    for sp in sprites:
        if sp.tags and 'npxgalaybz' in sp.tags:
            positions.add((sp.x, sp.y))
    p1=(15,16) in positions
    p2=(40,51) in positions
    return (p1, p2)

def get_state(env, r):
    pos=ppos(r)
    ri=rot_idx(env)
    p1,p2=pickups_remaining(env)
    return (pos, ri, p1, p2)

# Initial state
env0,r0=fresh_l2()
init=get_state(env0,r0)
print(f"Start: pos={init[0]}  rot={init[1]}  p1={init[2]}  p2={init[3]}")
print(f"Goal: pos=(14,40)  rot=3  (3=270 degrees)")
print()

visited={init: []}
queue=deque([([], init)])
MAX_DEPTH=60

wins=[]

while queue:
    path, state = queue.popleft()
    if len(path) >= MAX_DEPTH:
        continue

    for a in [A1,A2,A3,A4]:
        # Replay to this state
        env2,r2=fresh_l2()
        for m in path: r2=env2.step(m)
        r2=env2.step(a)

        if r2.levels_completed > 1:
            wins.append(path+[a])
            seq=''.join(ANAMES[m] for m in path+[a])
            print(f"  WIN in {len(path)+1} moves: {seq}")
            continue

        nstate=get_state(env2,r2)
        npos=nstate[0]
        if npos is None: continue

        # Check if counter hit 0 and reset (player teleported back to start)
        if npos == (29,40) and nstate[1]==0 and state[1]>0:
            # Level reset — this is a dead end path
            continue

        if nstate not in visited:
            visited[nstate]=path+[a]
            queue.append((path+[a], nstate))

print(f"\nTotal states explored: {len(visited)}")

if wins:
    best=min(wins, key=len)
    seq=''.join(ANAMES[a] for a in best)
    print(f"\nBest solution: {len(best)} moves")
    print(f"Sequence: {seq}")
    print(f"\nFull sequence (including L1):")
    full=L1+best
    print(f"  {['U','U','U','R','R','R','R','L','L','L','U','U','U'] + [ANAMES[a] for a in best]}")
else:
    print(f"\nNo solution found within {MAX_DEPTH} moves.")
    # Show interesting states reached
    print("\nStates with rot>0 reached:")
    for (pos,ri,p1,p2),path in sorted(visited.items(), key=lambda x: (-x[0][1], len(x[1]))):
        if ri > 0:
            print(f"  pos={pos}  rot={ri}  p1={p1}  p2={p2}  in {len(path)} moves: {''.join(ANAMES[a] for a in path[:20])}{'...' if len(path)>20 else ''}")
        if ri == 3 and len([x for x in visited if x[1]==3]) <= 5:
            break
