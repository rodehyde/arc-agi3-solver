"""ar25 L6: template-match the combined black pieces (rigid) onto the yellow figure,
to find which quadrant they cover (axes col 19, row 34)."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
L3 = [5] + [4]*7 + [2]*7 + [5] + [3]*12 + [2]*5 + [5] + [1]*7
L4 = [5] + [4]*7 + [5] + [1]*7 + [4]*7 + [5] + [2]*6
L5 = [5, 5] + [1]*7 + [3]*10 + [5] + [2]*4 + [5] + [4]*5


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in L1 + L2 + L3 + L4 + L5:
    r = env.step(A[a], data={})
g = grid(r)
Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
Yc = set(zip(*np.where(Y)))
Bc = set(zip(*np.where(B)))
print(f"yellow={len(Yc)} black={len(Bc)}")

# rigid shift of all black, maximise coverage of yellow (black lands on yellow)
best = None
for dy in range(-40, 41, 3):
    for dx in range(-60, 21, 3):
        sh = {(y+dy, x+dx) for (y, x) in Bc}
        on = len(sh & Yc); off = len(sh - Yc)
        score = on - 2*off
        if best is None or score > best[0]:
            best = (score, on, off, dy, dx)
sc, on, off, dy, dx = best
print(f"best rigid shift dy={dy} dx={dx}: on_yellow={on} off_yellow={off}")
print(f"  => UPPER+LOWER move: {'down' if dy>0 else 'up'} {abs(dy)//3}, "
      f"{'right' if dx>0 else 'left'} {abs(dx)//3}")

# show where black lands and which quadrant (axis col 19, row 34)
sh = {(y+dy, x+dx) for (y, x) in Bc}
rs = [p[0] for p in sh]; cs = [p[1] for p in sh]
print(f"  landed bbox rows {min(rs)}-{max(rs)} cols {min(cs)}-{max(cs)}")
print(f"  (axis col 19, row 34): rows {'<34' if max(rs)<34 else 'span'} "
      f"cols {'<19' if max(cs)<19 else ('>19' if min(cs)>19 else 'span')}")

# verify: does black-shifted ⊆ yellow form exactly one quadrant?
# quadrant top-left of (19,34): rows 9-33 cols 3-18
qtl = {(rr, cc) for (rr, cc) in Yc if rr < 34 and cc < 19}
qtr = {(rr, cc) for (rr, cc) in Yc if rr < 34 and cc > 19}
qbl = {(rr, cc) for (rr, cc) in Yc if rr > 34 and cc < 19}
qbr = {(rr, cc) for (rr, cc) in Yc if rr > 34 and cc > 19}
print(f"\nyellow quadrant sizes: TL={len(qtl)} TR={len(qtr)} BL={len(qbl)} BR={len(qbr)}")
