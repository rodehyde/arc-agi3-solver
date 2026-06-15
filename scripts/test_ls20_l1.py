"""ls20 L1: test solution sequence and find shortest path."""
import logging
from collections import deque
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r

def obpos(r):
    g=np.array(r.frame[-1])
    ys,xs=np.where(g==12)
    return (int(xs.min()), int(ys.min())) if len(ys) else None  # (x, y) sprite coords

# Test hypothesis: LLL UUU DDD RRR UUUUUU = 19 moves
print("=== Test sequence: LLL UUU DDD RRR UUUUUU ===")
seq=[A3,A3,A3, A1,A1,A1, A2,A2,A2, A4,A4,A4, A1,A1,A1,A1,A1,A1,A1]
env,r=fresh()
print(f"Start: pos={obpos(r)}  rot_idx=?  levels={r.levels_completed}")
for i,a in enumerate(seq):
    r=env.step(a)
    pos=obpos(r)
    print(f"  step {i+1} {ANAMES[a]}: pos={pos}  levels={r.levels_completed}  state={r.state.name}")
    if r.levels_completed>=1:
        print("  *** LEVEL 1 COMPLETE ***")
        break

# Try all orderings that hit toggle then target
# Know: toggle at (19,30), target at (34,10), start (34,45)
# rotation must be cycled exactly once (270→0)
# Direct route: LLL (to x=19), UUU (to y=30 trigger), ??? (to 34,10 without re-triggering)

# BFS with rotation state to find shortest path
print("\n=== BFS with rotation state ===")
# State: (x, y, rot_idx)  rot_idx=0..3 (dhksvilbb=[0,90,180,270])
# Start: x=34, y=45, rot_idx=3 (270°)
# Toggle: at (19,30) — fires when player bbox [x,x+5)×[y,y+5) contains (19,30)
# i.e. x in [15,20) and y in [26,31), but player x/y are multiples of 5 from 34 (so x∈{19,14,24,...}, y∈{45,40,35,30,...})
# So trigger fires when player pos = (19,30) [x=19 in [19,24), y=30 in [30,35)]

# Walls from level 1: known positions
# Rather than listing all walls, use the game to check movement validity
def get_neighbors(x, y, rot, toggle_pos=(19,30)):
    neighbors=[]
    for dx,dy,a in [(0,-5,A1),(0,5,A2),(-5,0,A3),(5,0,A4)]:
        nx,ny=x+dx,y+dy
        env2,r2=fresh()
        # Build path to (x,y) state — too complex, use simulation
        neighbors.append((nx,ny,a))
    return neighbors

# Better: BFS that simulates moves
# We'll do a proper BFS using game simulation but cache (x,y,rot_idx) states
from functools import lru_cache

# Simulate from state: build a map
START=(34,45,3)  # (x, y, rot_idx)
TARGET_X,TARGET_Y=34,10
TOGGLE=(19,30)
TOGGLE_ROT_DELTA=1  # cycles +1

# To avoid game re-instantiation overhead, build adjacency by testing from fresh
# with known path
# State: (x, y, rot_idx)
# Transition: test each action from current state

visited={START: None}
queue=deque([(START, [])])
found=None

# Precompute: test movement from each state using game simulation
# Since we need to know if a wall blocks, just use game

# Approach: BFS where state = (x, y, rot_idx)
# Build moves by simulating from fresh + path reconstruction

from collections import defaultdict
cache={}  # (state_tuple) -> {action: new_state_tuple}

def simulate_state(path):
    """Given action path, return final (x, y, rot_idx)."""
    env2,r2=fresh()
    rot=3  # start rot_idx=3 (270°)
    prev_pos=(34,45)
    for a in path:
        r2=env2.step(a)
        g=np.array(r2.frame[-1])
        ys,xs=np.where(g==12)
        if len(ys)==0: return None,None,rot
        pos=(int(xs.min()),int(ys.min()))
        # Check if toggle was hit (player moved to or through (19,30))
        # Toggle fires when player NEW position bbox contains (19,30)
        # = pos[0] in [19,24) and pos[1] in [30,35)
        # BUT: rot changes are tracked by cklxociuu in game, we detect via grid
        prev_pos=pos
    # Read actual rotation from game state
    # The ref box shows current rotation: read it
    ref_c={}
    for ri,r_ in enumerate([55,57,59]):
        for ci,c_ in enumerate([3,5,7]):
            blk=[int(g[r_+dr,c_+dc]) for dr in range(2) for dc in range(2)]
            ref_c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    ref=''.join('B' if ref_c[(r2_,c2)]==9 else '.' for r2_ in range(3) for c2 in range(3))
    # rot_idx: 0=0°=BBB/..B/B.B, 1=90°=B.B/..B/BBB, 2=180°=B.B/B../BBB, 3=270°=BBB/B../B.B
    rotmap={'BBB..BB.B':0,'B.B..BBBB':1,'B.BB..BBB':2,'BBBBB..BB.B':3}
    # Simplified: count toggle hits
    return prev_pos,r2

# Simple BFS capped at 25 moves
print("BFS searching for shortest win sequence...")
queue=deque([([], (34,45), 3)])  # (moves, pos, rot_idx)
seen={(34,45,3)}
best=None

while queue:
    moves,pos,rot=queue.popleft()
    if len(moves)>22: continue

    # Try each action
    for a in [A1,A2,A3,A4]:
        env2,r2=fresh()
        for m in moves: r2=env2.step(m)
        r2=env2.step(a)
        if r2.levels_completed>=1:
            win_seq=moves+[a]
            print(f"  WIN in {len(win_seq)} moves: {''.join(ANAMES[m] for m in win_seq)}")
            best=win_seq
            break
        g=np.array(r2.frame[-1])
        ys,xs=np.where(g==12)
        if len(ys)==0: continue
        npos=(int(xs.min()),int(ys.min()))
        if npos==pos: continue  # didn't move (blocked)
        # Read rotation from ref box
        ref_cells={}
        for ri,rr in enumerate([55,57,59]):
            for ci,cc in enumerate([3,5,7]):
                blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
                ref_cells[(ri,ci)]=9 if blk.count(9)>=2 else 5
        ref_key=''.join('B' if ref_cells[(rr,cc)]==9 else '.' for rr in range(3) for cc in range(3))
        # Map ref to rot_idx
        rotmap={'BBB...B.B':3,'BBB..BB.B':0,'B.B..BBBB':1,'B.BB..BBB':2}
        nrot=rotmap.get(ref_key, rot)
        state=(npos,nrot)
        if state not in seen:
            seen.add(state)
            queue.append((moves+[a], npos, nrot))
    if best: break

if not best:
    print("  No win found in 22 moves")
