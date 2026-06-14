"""Dump the explicit L4 click list under the winning rule (white->center, grey->red)."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]
PRE = L1 + L2 + L3
ROWS = [14, 22, 30, 38, 46]
COLS = [12, 20, 28, 36, 44]
CF = {9: 0, 8: 1, 12: 2}

ar = Arcade(operation_mode=OperationMode.OFFLINE)
env = ar.make('ft09')
r = env.observation_space
for (x, y) in PRE:
    r = env.step(GameAction.ACTION6, data={'x': x, 'y': y})
g = np.array(r.frame[-1])


def dom(b):
    v, c = np.unique(b, return_counts=True)
    return int(v[np.argmax(c)])


present = {}
keys = {}
for ri, rr in enumerate(ROWS):
    for ci, cc in enumerate(COLS):
        blk = g[rr:rr+6, cc:cc+6]
        if np.all(blk == 4):
            continue
        present[(ri, ci)] = True
        if (blk == 0).any():
            mini = [[dom(g[rr+2*i:rr+2*i+2, cc+2*j:cc+2*j+2]) for j in range(3)] for i in range(3)]
            keys[(ri, ci)] = {'center': mini[1][1], 'mini': mini}
wv = {}
gv = {}
for (kr, kc), kd in keys.items():
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                continue
            s = (kr-1+i, kc-1+j)
            if s not in present:
                continue
            if kd['mini'][i][j] == 0:
                wv.setdefault(s, set()).add(kd['center'])
            else:
                gv.setdefault(s, set()).add(8)
clicks = []
for s in present:
    if s in keys:
        continue
    col = sorted(wv[s])[0] if s in wv else (sorted(gv[s])[0] if s in gv else 9)
    for _ in range(CF[col]):
        clicks.append((COLS[s[1]]+3, ROWS[s[0]]+3))
print("L4 =", clicks)
print("n =", len(clicks))
