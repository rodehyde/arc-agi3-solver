"""ls20 L2: deep BFS to find toggle and target, print full reachable map."""
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
    g=np.array(r.frame[-1])
    ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

def ref_str(r):
    g=np.array(r.frame[-1])
    c={}
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return '/'.join(''.join('B' if c[(ri,ci)]==9 else '.' for ci in range(3)) for ri in range(3))

# Deep BFS tracking (pos, ref) state
start_r = fresh_l2()[1]
start_pos = ppos(start_r)
start_ref = ref_str(start_r)
print(f"Start: pos={start_pos}  ref={start_ref}")

visited={(start_pos, start_ref): []}
queue=deque([([], start_pos, start_ref)])
found_toggle=[]
found_target=[]

MAX_DEPTH=22

while queue:
    path, pos, ref = queue.popleft()
    if len(path)>=MAX_DEPTH: continue

    for a in [A1,A2,A3,A4]:
        env2,r2=fresh_l2()
        for m in path: r2=env2.step(m)
        r2=env2.step(a)

        if r2.levels_completed > 1:
            print(f"WIN: {len(path)+1} moves: {''.join(ANAMES[m] for m in path+[a])}")
            break

        npos=ppos(r2)
        if npos is None: continue
        nref=ref_str(r2)

        if nref != ref:
            # toggle fired!
            found_toggle.append((path+[a], npos, nref))
            print(f"  TOGGLE at step {len(path)+1}: pos={npos}  ref={nref}  path={''.join(ANAMES[m] for m in path+[a])}")

        if npos == start_pos and ref == start_ref and npos == pos:
            continue  # didn't move AND no state change

        state=(npos, nref)
        if state not in visited:
            visited[state]=path+[a]
            queue.append((path+[a], npos, nref))

print(f"\nTotal states explored: {len(visited)}")
print(f"Toggle trigger events found: {len(found_toggle)}")

# Also: check if target (14,40) is reachable with any ref state
print("\nAll reachable positions at col=14:")
for (pos, ref), path in sorted(visited.items()):
    if pos[0]==14:
        print(f"  pos={pos}  ref={ref}  in {len(path)} moves: {''.join(ANAMES[a] for a in path)}")
