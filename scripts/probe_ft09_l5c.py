"""ft09 L5: full key map + plain-tile scope check."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]
L4 = [(15, 17), (23, 17), (23, 17), (31, 17), (47, 17), (15, 25), (31, 25),
      (47, 25), (15, 33), (23, 33), (23, 33), (31, 33), (39, 33), (23, 41),
      (39, 41), (23, 49), (23, 49), (31, 49), (31, 49), (39, 49), (39, 49)]
PRE = L1 + L2 + L3 + L4

ROW_STARTS = [4, 12, 20, 28, 36, 44, 52]
COL_STARTS = [6, 14, 22, 30, 38, 46, 54]
BG = 4  # vdk-grey background


def tile_center(ri, ci):
    return (COL_STARTS[ci] + 3, ROW_STARTS[ri] + 3)


def grid(r):
    return np.array(r.frame[-1])


def dom(block):
    v, c = np.unique(block, return_counts=True)
    return int(v[np.argmax(c)])


def slot_of(row, col):
    for ri, rs in enumerate(ROW_STARTS):
        if rs <= row < rs + 6:
            for ci, cs in enumerate(COL_STARTS):
                if cs <= col < cs + 6:
                    return (ri, ci)
    return None


def to_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


env, r = to_l5()
g = grid(r)

# --- Scan all slots ---
present = {}   # (ri,ci) -> True
keys = {}      # (ri,ci) -> {center, mini}
pink_cross = {}  # (ri,ci) -> True

for ri, rs in enumerate(ROW_STARTS):
    for ci, cs in enumerate(COL_STARTS):
        blk = g[rs:rs+6, cs:cs+6]
        if np.all(blk == BG):
            continue
        present[(ri, ci)] = True
        if (blk == 0).any():   # has white → key
            mini = [[dom(g[rs+2*i:rs+2*i+2, cs+2*j:cs+2*j+2])
                     for j in range(3)] for i in range(3)]
            keys[(ri, ci)] = {'center': mini[1][1], 'mini': mini}
        elif 6 in blk and not (blk == 0).any():
            pink_cross[(ri, ci)] = True

print(f"Present slots: {len(present)}")
print(f"Keys: {sorted(keys.keys())}")
print(f"Pink-cross tiles: {sorted(pink_cross.keys())}")
print()

# --- Print each key's mini-grid ---
for k in sorted(keys):
    kd = keys[k]
    print(f"Key {k}  center={kd['center']}({'green' if kd['center']==14 else 'purple'})")
    for row in kd['mini']:
        print("  ", row)
    white_nbrs = []
    grey_nbrs = []
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                continue
            nr, nc = k[0]-1+i, k[1]-1+j
            if (nr, nc) not in present:
                continue
            if kd['mini'][i][j] == 0:
                white_nbrs.append((nr, nc))
            else:
                grey_nbrs.append((nr, nc))
    print(f"  white→{kd['center']}: {white_nbrs}")
    print(f"  grey→??:              {grey_nbrs}")
    print()

# --- Check plain tile click scope (does it affect only itself?) ---
print("=== Plain tile click scope ===")
env, r = to_l5()
g0 = grid(r).copy()
# click plain tile at (ri=2, ci=0) — known plain green
cx, cy = tile_center(2, 0)
r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r)
diff = g0 != g1
changed_slots = {}
ys, xs = np.where(diff)
for yy, xx in zip(ys, xs):
    s = slot_of(yy, xx)
    if s:
        changed_slots[s] = changed_slots.get(s, 0) + 1
print(f"Plain tile (2,0): {diff.sum()} cells changed, slots: {list(changed_slots.keys())}")

# Try another plain tile (ri=2, ci=3)
env, r = to_l5()
g0 = grid(r).copy()
cx, cy = tile_center(2, 3)
r = env.step(GameAction.ACTION6, data={"x": cx, "y": cy})
g1 = grid(r)
diff = g0 != g1
changed_slots = {}
ys, xs = np.where(diff)
for yy, xx in zip(ys, xs):
    s = slot_of(yy, xx)
    if s:
        changed_slots[s] = changed_slots.get(s, 0) + 1
print(f"Plain tile (2,3): {diff.sum()} cells changed, slots: {list(changed_slots.keys())}")
