"""ft09 L6: correct grid scan (ROW_STARTS=[6,14,22,30,38,46], COL_STARTS=[4,12,20,28,36,44,52])."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1 = [(38,38),(38,46),(54,46),(38,54)]
L2 = [(22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48)]
L3 = [(22,6),(30,6),(38,6),(22,14),(14,22),(30,22),(14,30),
      (46,30),(30,38),(46,38),(22,46),(22,54),(30,54),(38,54)]
L4 = [(15,17),(23,17),(23,17),(31,17),(47,17),(15,25),(31,25),
      (47,25),(15,33),(23,33),(23,33),(31,33),(39,33),(23,41),
      (39,41),(23,49),(23,49),(31,49),(31,49),(39,49),(39,49)]
L5 = [(25,15),(25,31),(41,47),(33,7),(17,23),(33,23),(49,23),
      (17,39),(33,39),(49,39),(17,55),(33,55),(25,7),(17,15),
      (33,15),(17,31),(33,31),(41,39),(33,47),(49,47),(41,55)]
PRE = L1+L2+L3+L4+L5

ROW_STARTS = [6, 14, 22, 30, 38, 46]
COL_STARTS = [4, 12, 20, 28, 36, 44, 52]
BG = 4


def grid(r): return np.array(r.frame[-1])
def dom(blk):
    v,c = np.unique(blk,return_counts=True); return int(v[np.argmax(c)])
def tc(ri, ci): return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)


def to_l6():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for x,y in PRE:
        r = env.step(GameAction.ACTION6, data={"x":x,"y":y})
    assert r.levels_completed == 5
    return env, r


env, r = to_l6()
g = grid(r)

# --- Scan all slots ---
present = {}
keys = {}
for ri,rs in enumerate(ROW_STARTS):
    for ci,cs in enumerate(COL_STARTS):
        blk = g[rs:rs+6, cs:cs+6]
        if np.all(blk == BG): continue
        non_bg = (blk != BG).sum()
        if non_bg < 6: continue          # skip tiny indicator overlap
        present[(ri,ci)] = True
        if (blk == 0).any():
            mini = [[dom(g[rs+2*i:rs+2*i+2, cs+2*j:cs+2*j+2]) for j in range(3)] for i in range(3)]
            keys[(ri,ci)] = {'center': mini[1][1], 'mini': mini}

print(f"Present: {sorted(present)}")
print(f"Keys:    {sorted(keys)}")
print()

for k in sorted(keys):
    kd = keys[k]
    print(f"Key {k}  centre={kd['center']}")
    for row in kd['mini']: print("  ", row)
    white_nbrs, grey_nbrs = [], []
    for i in range(3):
        for j in range(3):
            if (i,j)==(1,1): continue
            nr,nc = k[0]-1+i, k[1]-1+j
            if (nr,nc) not in present: continue
            if kd['mini'][i][j] == 0: white_nbrs.append((nr,nc))
            else: grey_nbrs.append((nr,nc))
    print(f"  white→{kd['center']}: {white_nbrs}")
    print(f"  grey→??:              {grey_nbrs}")
    print()

# --- Click cycle on a real plain tile ---
print("=== Click cycle on plain tile (0,0) ===")
env, r = to_l6()
cx,cy = tc(0,0)
seq = [int(grid(r)[cy,cx])]
for _ in range(5):
    r = env.step(GameAction.ACTION6, data={"x":cx,"y":cy})
    seq.append(int(grid(r)[cy,cx]))
print(f"  colours 0..5 clicks: {seq}")

# --- Scope: how many slots change? ---
print()
print("=== Click scope: plain tile (0,0) ===")
env, r = to_l6()
g0 = grid(r).copy()
cx,cy = tc(0,0)
r = env.step(GameAction.ACTION6, data={"x":cx,"y":cy})
g1 = grid(r)
total = int((g0!=g1).sum())
changed = [(ri,ci) for ri,rs in enumerate(ROW_STARTS) for ci,cs in enumerate(COL_STARTS)
           if (ri,ci) in present and not np.array_equal(g0[rs:rs+6,cs:cs+6], g1[rs:rs+6,cs:cs+6])]
print(f"  cells changed: {total}  slots: {changed}")

# --- Does clicking a "pink notch" tile toggle neighbours? ---
# Try tile (1,2) (plain yellow, no white cells)
print()
print("=== Click scope: plain tile (1,2) ===")
env, r = to_l6()
g0 = grid(r).copy()
cx,cy = tc(1,2)
r = env.step(GameAction.ACTION6, data={"x":cx,"y":cy})
g1 = grid(r)
total = int((g0!=g1).sum())
changed = [(ri,ci) for ri,rs in enumerate(ROW_STARTS) for ci,cs in enumerate(COL_STARTS)
           if (ri,ci) in present and not np.array_equal(g0[rs:rs+6,cs:cs+6], g1[rs:rs+6,cs:cs+6])]
print(f"  cells changed: {total}  slots: {changed}")
