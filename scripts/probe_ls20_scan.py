"""ls20: full grid scan for non-background cells, ref toggle tests, and position comparison."""
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
    c={}
    for ri,r_ in enumerate([55,57,59]):
        for ci,c_ in enumerate([3,5,7]):
            blk=[g[r_+dr,c_+dc] for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return c
def ref_str(c): return '/'.join(''.join('B' if c[(r,ci)]==9 else '.' for ci in range(3)) for r in range(3))

env,r=fresh()
g0=grid(r)

# 1. All distinct non-black cells in the play area (rows 0-63, excluding piece and boxes)
print("=== Non-background cells in play area (value != 5 and != piece) ===")
piece_rows=range(45,50); piece_cols=range(34,39)
for row in range(0,64):
    for col in range(0,64):
        v=int(g0[row,col])
        if v not in (5,9,12) and not (35<=row<=64 and col in range(2,10)) and not (9<=row<=16 and col in range(33,40)):
            print(f"  ({row},{col})=color{v}")

# 2. Scan background cell values specifically at rows 30-39, cols 10-29
print("\n=== Background at rows 30-39, cols 10-29 (before piece arrives) ===")
for row in range(30,40):
    vals=[int(g0[row,c]) for c in range(10,30)]
    unique_non5=[(c+10,v) for c,v in enumerate(vals) if v!=5]
    if unique_non5:
        print(f"  row {row}: special cells = {unique_non5}")
    else:
        print(f"  row {row}: all background (5)")

# 3. Compare grid when piece at (30,19) vs (30,24) — what's different besides piece cells?
print("\n=== Grid diff: piece at (30,19) vs (30,24) ===")
env2,r2=fresh()
for a in [A3,A3,A3,A1,A1,A1]: r2=env2.step(a)  # → (30,19)
g_19=grid(r2)

env3,r3=fresh()
for a in [A1,A1,A1,A1,A3,A3,A2]: r3=env3.step(a)  # → (30,24)
g_24=grid(r3)

# Find cells that differ (excluding the piece cells themselves and ref box)
piece19=set((r,c) for r in range(30,35) for c in range(19,24))
piece24=set((r,c) for r in range(30,35) for c in range(24,29))
diffs=[]
for row in range(0,64):
    for col in range(0,64):
        if (row,col) in piece19 or (row,col) in piece24: continue
        if g_19[row,col]!=g_24[row,col]:
            diffs.append((row,col,int(g_19[row,col]),int(g_24[row,col])))

print(f"  Cells different (excl. piece): {len(diffs)}")
for row,col,v19,v24 in diffs:
    print(f"    ({row},{col}): at_19={v19}  at_24={v24}")

# 4. Test if visiting (30,19) TWICE toggles the ref back
print("\n=== Toggle test: (30,19) then back to start then (30,19) again ===")
env4,r4=fresh()
for a in [A3,A3,A3,A1,A1,A1]: r4=env4.step(a)  # → (30,19)
c1=ref_cells(grid(r4))
print(f"  After first visit (30,19): ref={ref_str(c1)}")
for a in [A2,A2,A2,A4,A4,A4]: r4=env4.step(a)  # → back to (45,34)
c2=ref_cells(grid(r4))
print(f"  After returning to start: ref={ref_str(c2)}")
for a in [A3,A3,A3,A1,A1,A1]: r4=env4.step(a)  # → (30,19) again
c3=ref_cells(grid(r4))
print(f"  After second visit (30,19): ref={ref_str(c3)}  levels={r4.levels_completed}")

# 5. Test (30,14) THEN (30,19) — does second trigger anything new?
print("\n=== Sequence: (30,14) then (30,19) ===")
env5,r5=fresh()
for a in [A3,A3,A3,A1,A1,A1,A3]: r5=env5.step(a)  # → (30,14)
c5a=ref_cells(grid(r5))
print(f"  After (30,14): ref={ref_str(c5a)}")
for a in [A4]: r5=env5.step(a)  # → (30,19)
c5b=ref_cells(grid(r5))
print(f"  After (30,19): ref={ref_str(c5b)}  levels={r5.levels_completed}")

# 6. What does the piece look like when at (30,19)? Print rows 28-36, cols 17-25
print("\n=== Grid rows 28-36, cols 14-26 when piece at (30,19) ===")
env6,r6=fresh()
for a in [A3,A3,A3,A1,A1,A1]: r6=env6.step(a)
g6=grid(r6)
for row in range(28,37):
    vals=[int(g6[row,c]) for c in range(14,27)]
    print(f"  row {row}: {vals}")

# 7. What does fresh grid look like at rows 28-36, cols 14-26?
print("\n=== Fresh grid rows 28-36, cols 14-26 ===")
for row in range(28,37):
    vals=[int(g0[row,c]) for c in range(14,27)]
    print(f"  row {row}: {vals}")
