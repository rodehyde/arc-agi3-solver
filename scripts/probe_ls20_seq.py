"""ls20 L1: track ref box changes across sequences of moves."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r
def grid(r): return np.array(r.frame[-1])

def ref_cells(g):
    """Return 3x3 ref cell grid (each cell = dominant value in 2x2 block)."""
    cells={}
    for ri,r_ in enumerate([55,57,59]):
        for ci,c_ in enumerate([3,5,7]):
            blk=[g[r_+dr,c_+dc] for dr in range(2) for dc in range(2)]
            cells[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return cells

def ref_str(cells):
    return '/'.join(''.join('B' if cells[(r,c)]==9 else '.' for c in range(3)) for r in range(3))

def obbox(g):
    ys,xs=np.where(g==12); return (int(ys.min()),int(xs.min())) if len(ys) else None

# Check ref at every step across a long exploration sequence
env,r=fresh()
g=grid(r)
cells0=ref_cells(g)
print(f"Start ref: {ref_str(cells0)}  piece={obbox(g)}")

# Explore systematically: cover different sub-regions
# Each position in the 3x3 play super-grid:
# (0,2)=up/stem  (1,0)=upper-left  (1,1)=upper-mid  (1,2)=upper-right
# (2,0)=lower-left  (2,2)=lower-right
test_sequences = [
    # Visit all unique sub-regions
    [A1,A1,A1,A1,A1,A1],              # → (15,34) = top/stem
    [A3,A3,A3,A1,A1,A1],              # → (30,19) = upper-left
    [A1,A1,A1,A1,A3,A3,A2],           # → (30,24) = upper-mid
    [A1,A1,A1],                        # → (30,34) = upper-right
    [A3,A3,A3,A1,A1],                  # → (35,19) = lower-left
    [A1,A1],                           # → (35,34) = lower-right
]
names=["stem(15,34)","upper-L(30,19)","upper-M(30,24)","upper-R(30,34)","lower-L(35,19)","lower-R(35,34)"]
for seq,name in zip(test_sequences,names):
    env2,r2=fresh()
    for a in seq: r2=env2.step(a)
    g2=grid(r2)
    cells2=ref_cells(g2)
    changed = (cells2!=cells0)
    print(f"  {name}: ref={ref_str(cells2)}  changed={changed}  levels={r2.levels_completed}")

# Now: multi-step sequence — visit positions that triggered ref changes and continue
# Step 1: visit upper-left (30,19) → ref changes
# Step 2: visit different region → see if ref changes again
print("\nChain exploration (visit each sub-region in turn):")
env,r=fresh()
prev_cells=ref_cells(grid(r))
moves_done=0

step_seqs=[
    ([A3,A3,A3,A1,A1,A1], "→(30,19) upper-L"),
    ([A4,A4,A4], "(30,34)→(30,49) upper-R"),
    ([A1,A1,A1], "(30,34)→(25,34)→up to stem"),
    ([A1,A1,A1], "→(15,34) stem"),
    ([A2,A2,A2,A2,A2,A2], "→(45,34) back to start"),
    ([A1,A1], "→(35,34) lower-R"),
    ([A3,A3,A3], "→(35,19) lower-L"),
]

for step_seq,label in step_seqs:
    for a in step_seq:
        r=env.step(a)
        moves_done+=1
        g=grid(r)
        new_cells=ref_cells(g)
        if new_cells!=prev_cells:
            print(f"  move {moves_done} ({label}): pos={obbox(g)}  ref={ref_str(new_cells)}  levels={r.levels_completed}")
            prev_cells=new_cells
            if r.levels_completed>=1:
                print("  *** LEVEL COMPLETE ***")
                break
    if r.levels_completed>=1: break

# Also: test if visiting (30,14) then IMMEDIATELY wins by visiting some known position
print("\nAfter upper-left, try each other sub-region:")
for pos_seq,posname in [
    ([A1,A1,A1,A1,A1,A1], "stem(15,34)"),
    ([A1,A1,A1,A1,A3,A3,A2], "upper-M(30,24)"),
    ([A1,A1,A1], "upper-R(30,34)"),
    ([A3,A3,A3,A1,A1], "lower-L(35,19)"),
    ([A1,A1], "lower-R(35,34)"),
]:
    env2,r2=fresh()
    for a in [A3,A3,A3,A1,A1,A1]: r2=env2.step(a)  # → (30,19)
    g_mid=grid(r2)
    cells_mid=ref_cells(g_mid)
    for a in pos_seq: r2=env2.step(a)
    g2=grid(r2)
    cells2=ref_cells(g2)
    print(f"  (30,19) then {posname}: ref={ref_str(cells2)}  levels={r2.levels_completed}")
