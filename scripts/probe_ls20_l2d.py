"""ls20 L2: after 3 toggle hits (rotation=270°), BFS from (49,45) to target (14,40)."""
import logging, numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
# 3 toggle hits: URUUUUURRDRDDDDDDUDUD
TOGGLE3='URUUUUURRDRDDDDDDUDUD'
TOGGLE3_ACTIONS=[{'U':A1,'D':A2,'L':A3,'R':A4}[c] for c in TOGGLE3]
PREAMBLE=L1+TOGGLE3_ACTIONS

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    for a in PREAMBLE: r=env.step(a)
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

# Verify state after toggle sequence
env0, r0 = fresh()
pos0 = ppos(r0)
ref0 = ref_str(r0)
print(f"After 3 toggle hits: pos={pos0}  ref={ref0}  levels={r0.levels_completed}")
print(f"Expected: pos=(49,45)  ref=BBB/B../B.B (rotation=270)")
print()

# Step-by-step trace: try to go LEFT 7 then UP 1
print("Tracing LLLLLLLLU from (49,45):")
env2, r2 = fresh()
for step, (action, name) in enumerate([(A3,'L')]*7 + [(A1,'U')]*1):
    r2 = env2.step(action)
    pos = ppos(r2)
    print(f"  Step {step+1} {name}: pos={pos}  levels={r2.levels_completed}")
    if r2.levels_completed > 1:
        print("  *** LEVEL COMPLETE! ***")
        break

print()

# BFS from post-toggle state to (14,40)
print("BFS from post-toggle state, looking for (14,40) or WIN:")
visited={pos0: []}
queue=deque([([], pos0)])
MAX_DEPTH=30

wins=[]
target_paths=[]

while queue:
    path, pos = queue.popleft()
    if len(path) >= MAX_DEPTH: continue

    for a in [A1,A2,A3,A4]:
        env2, r2 = fresh()
        for m in path: r2 = env2.step(m)
        r2 = env2.step(a)

        if r2.levels_completed > 1:
            wins.append(path+[a])
            seq=''.join(ANAMES[m] for m in path+[a])
            print(f"  WIN at step {len(path)+1}: {seq}")
            continue

        npos = ppos(r2)
        if npos is None: continue

        if npos not in visited:
            visited[npos] = path+[a]
            queue.append((path+[a], npos))

        if npos == (14,40) and npos not in [p for p,_ in target_paths]:
            target_paths.append((npos, path+[a]))
            seq=''.join(ANAMES[m] for m in path+[a])
            print(f"  REACHED TARGET (14,40) at step {len(path)+1}: {seq}")

print(f"\nTotal positions reachable from post-toggle: {len(visited)}")
if wins:
    best=min(wins, key=len)
    print(f"Shortest win: {len(best)} steps: {''.join(ANAMES[a] for a in best)}")
    print(f"FULL SOLUTION (L1 + toggle + win): {''.join(ANAMES[a] for a in L1+TOGGLE3_ACTIONS+best)}")
elif target_paths:
    best=min(target_paths, key=lambda x: len(x[1]))
    print(f"Reached (14,40) in {len(best[1])} steps: {''.join(ANAMES[a] for a in best[1])}")
else:
    print("Neither (14,40) nor WIN found within BFS depth.")
    print("\nAll reachable positions (sorted by col):")
    for pos in sorted(visited.keys()):
        seq=''.join(ANAMES[a] for a in visited[pos])
        print(f"  {pos}  via {seq}")
