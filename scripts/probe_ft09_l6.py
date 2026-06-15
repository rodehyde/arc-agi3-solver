"""ft09 L6: scan all slots, probe click cycle and scope."""
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

BG = 4


def grid(r): return np.array(r.frame[-1])
def dom(blk):
    v,c = np.unique(blk,return_counts=True); return int(v[np.argmax(c)])


def to_l6():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for x,y in PRE:
        r = env.step(GameAction.ACTION6, data={"x":x,"y":y})
    assert r.levels_completed == 5, f"Expected L6, got level {r.levels_completed+1}"
    return env, r


env, r = to_l6()
g = grid(r)

# --- Scan ALL possible 6x6 slots on a 64x64 grid at spacing 8, offset varies ---
# Detect occupied slots dynamically
print("=== Available actions ===")
print(r.available_actions)
print()

# Find all 6x6 non-background blocks
occupied = []
for rs in range(0, 58, 2):       # row starts 0..57
    for cs in range(0, 58, 2):   # col starts 0..57
        blk = g[rs:rs+6, cs:cs+6]
        if blk.shape == (6,6) and not np.all(blk == BG):
            # check it's a clean 6x6 tile (mostly non-bg)
            non_bg = (blk != BG).sum()
            if non_bg >= 12:  # at least 1/3 non-bg
                occupied.append((rs, cs))

# Deduplicate overlapping detections
def dedupe(slots):
    keep = []
    for s in slots:
        if not any(abs(s[0]-k[0]) < 6 and abs(s[1]-k[1]) < 6 and s != k for k in keep):
            keep.append(s)
    return keep

occupied = dedupe(occupied)
print(f"Occupied slots ({len(occupied)}):")
for rs,cs in sorted(occupied):
    blk = g[rs:rs+6,cs:cs+6]
    has_white = (blk == 0).any()
    has_pink  = (blk == 6).any()
    centre = dom(g[rs+2:rs+4, cs+2:cs+4])
    tag = "KEY" if has_white else ("pink" if has_pink else "plain")
    print(f"  rows {rs}-{rs+5} cols {cs}-{cs+5}  tag={tag}  centre={centre}")

# --- Print key mini-grids ---
print()
print("=== Key mini-grids ===")
for rs,cs in sorted(occupied):
    blk = g[rs:rs+6,cs:cs+6]
    if not (blk == 0).any():
        continue
    mini = [[dom(g[rs+2*i:rs+2*i+2, cs+2*j:cs+2*j+2]) for j in range(3)] for i in range(3)]
    centre = mini[1][1]
    print(f"Key rows {rs}-{rs+5} cols {cs}-{cs+5}  centre={centre}")
    for row in mini: print("  ", row)
    print()

# --- Click cycle: plain tile ---
print("=== Click cycle on first plain tile ===")
env, r = to_l6()
# find first plain tile
first_plain = next((s for s in sorted(occupied) if not (g[s[0]:s[0]+6,s[1]:s[1]+6]==0).any()), None)
rs, cs = first_plain
cx, cy = cs+3, rs+3
seq = [int(grid(r)[cy,cx])]
for _ in range(5):
    r = env.step(GameAction.ACTION6, data={"x":cx,"y":cy})
    seq.append(int(grid(r)[cy,cx]))
print(f"  slot rows {rs} cols {cs}, centre clicks 0..5: {seq}")

# --- Click scope: how many cells/slots change? ---
print()
print("=== Click scope: plain tile ===")
env, r = to_l6()
g0 = grid(r).copy()
r = env.step(GameAction.ACTION6, data={"x":cx,"y":cy})
g1 = grid(r)
changed = int((g0 != g1).sum())
print(f"  cells changed: {changed}  (6x6=36 = self only)")

# Which slots changed?
def changed_slots(g0, g1, occ):
    out = []
    for rs,cs in occ:
        if not np.array_equal(g0[rs:rs+6,cs:cs+6], g1[rs:rs+6,cs:cs+6]):
            out.append((rs,cs))
    return out

cs_list = changed_slots(g0, g1, occupied)
print(f"  changed slots: {cs_list}")

# --- Click scope: key tile (does clicking it do anything?) ---
print()
print("=== Click on a key tile ===")
env, r = to_l6()
key_slot = next((s for s in sorted(occupied) if (g[s[0]:s[0]+6,s[1]:s[1]+6]==0).any()), None)
rs, cs = key_slot
cx2, cy2 = cs+3, rs+3
g0 = grid(r).copy()
r = env.step(GameAction.ACTION6, data={"x":cx2,"y":cy2})
g1 = grid(r)
print(f"  slot rows {rs} cols {cs}: {int((g0!=g1).sum())} cells changed")
