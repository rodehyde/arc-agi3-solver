"""ar25 L6: template-match each black piece against the right-side gap to find placement.
Also test whether the gap's TOP half alone is fillable by the pieces (hband at row 34 reflects)."""
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
axis = 22
Ymir = np.zeros_like(Y)
for rr in range(64):
    for cc in range(64):
        mc = 2*axis - cc
        if 0 <= mc < 64 and Y[rr, cc]:
            Ymir[rr, mc] = True
gap = Ymir & (~Y)
gap[:, :axis+1] = False  # right side only

# split black into upper (rows<24) and lower (rows>=24) pieces
upper = B.copy(); upper[24:, :] = False
lower = B.copy(); lower[:24, :] = False


def cells(mask):
    return set(zip(*np.where(mask)))


gapc = cells(gap)


def best_shift(piece):
    pc = cells(piece)
    best = None
    for dy in range(-60, 61, 3):
        for dx in range(-60, 61, 3):
            shifted = {(y+dy, x+dx) for (y, x) in pc}
            on = len(shifted & gapc)
            off = len(shifted - gapc)
            score = on - off  # reward landing on gap, penalise spill
            if best is None or score > best[0]:
                best = (score, on, off, dy, dx)
    return best


for name, piece in [("UPPER", upper), ("LOWER", lower)]:
    ys, xs = np.where(piece)
    sz = piece.sum()
    sc, on, off, dy, dx = best_shift(piece)
    print(f"{name}: tl=({ys.min()},{xs.min()}) size={sz}  best shift dy={dy} dx={dx} "
          f"-> on_gap={on} off_gap={off}")
    print(f"   => move: {'down' if dy>0 else 'up'} {abs(dy)//3}, "
          f"{'right' if dx>0 else 'left'} {abs(dx)//3}")

print(f"\ngap total cells={gap.sum()}  upper size={upper.sum()} lower size={lower.sum()} "
      f"sum={upper.sum()+lower.sum()}")
