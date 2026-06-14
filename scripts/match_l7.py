"""ar25 L7: match each black piece onto the yellow figure (box level), and check that
covering those boxes + reflecting about (22,37) completes the figure's symmetry."""
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
L6 = ([5,5,5] + [2]*12 + [3]*7 + [5,5,5] + [2]*4 + [3]*15 + [5,5] + [2]*11 + [5] + [3]*1)
PRE = L1 + L2 + L3 + L4 + L5 + L6


def grid(f):
    return np.array(f.frame[-1])


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
for a in PRE:
    r = env.step(A[a], data={})
g = grid(r)


def boxset(mask):
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


def vref(b):  # about col 37
    return (b[0], 72 - b[1])
def href(b):  # about row 22
    return (42 - b[0], b[1])
def orbit(boxes):
    out = set()
    for b in boxes:
        out |= {b, vref(b), href(b), href(vref(b))}
    return out


Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
Yb = boxset(Y)
Fb = orbit(Yb)
gap = Fb - Yb
right = B.copy(); right[:, :40] = False
left = B.copy(); left[:, 40:] = False
Rb, Lb = boxset(right), boxset(left)
print(f"yellow={len(Yb)} closure={len(Fb)} gap={len(gap)} right={len(Rb)} left={len(Lb)}")
print(f"gap boxes: {sorted(gap)}")

shifts = [(dy, dx) for dy in range(-60, 61, 3) for dx in range(-60, 61, 3)]


def best_onto(piece, target):
    best = None
    for dy, dx in shifts:
        sh = {(b[0]+dy, b[1]+dx) for b in piece}
        on = len(sh & target); off = len(sh - target)
        if best is None or (on - 5*off) > best[0]:
            best = (on - 5*off, on, off, dy, dx)
    return best


for nm, P in [("right", Rb), ("left", Lb)]:
    # match onto full yellow, and onto gap
    sy = best_onto(P, Yb)
    sg = best_onto(P, gap)
    print(f"\n{nm} ({len(P)} boxes):")
    print(f"  onto YELLOW: on={sy[1]}/{len(P)} off={sy[2]} shift dy={sy[3]} dx={sy[4]}")
    print(f"  onto GAP   : on={sg[1]}/{len(P)} off={sg[2]} shift dy={sg[3]} dx={sg[4]}")
