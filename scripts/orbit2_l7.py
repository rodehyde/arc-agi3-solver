"""ar25 L7: 2-fold (180-rotation) orbit search about centroid (row22,col37).
Box rotation: (br,bc) -> (42-br, 72-bc). Find piece shifts whose rot-orbits tile yellow."""
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


def orbit2(boxes):           # 180-rotation about (row22,col37): br->42-br, bc->72-bc
    out = set()
    for (br, bc) in boxes:
        out.add((br, bc)); out.add((42-br, 72-bc))
    return out


Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
Yb = boxset(Y)
right = B.copy(); right[:, :40] = False
left = B.copy(); left[:, 40:] = False
Rb, Lb = boxset(right), boxset(left)
print(f"yellow boxes={len(Yb)} right={len(Rb)} left={len(Lb)}")

shifts = [(dy, dx) for dy in range(-60, 61, 3) for dx in range(-60, 61, 3)]


def fits(piece):
    return [(dy, dx) for dy, dx in shifts
            if orbit2({(b[0]+dy, b[1]+dx) for b in piece}) <= Yb]


rf, lf = fits(Rb), fits(Lb)
print(f"right placements (orbit2 ⊆ yellow): {len(rf)}; left: {len(lf)}")
sol = None
for (rdy, rdx) in rf:
    rorb = orbit2({(b[0]+rdy, b[1]+rdx) for b in Rb})
    for (ldy, ldx) in lf:
        lorb = orbit2({(b[0]+ldy, b[1]+ldx) for b in Lb})
        if rorb | lorb == Yb:
            sol = (rdy, rdx, ldy, ldx, len(rorb), len(lorb), len(rorb & lorb))
            break
    if sol:
        break
if sol:
    rdy, rdx, ldy, ldx, ro, lo, ov = sol
    print(f"\nSOLUTION: right dy={rdy} dx={rdx}; left dy={ldy} dx={ldx}; "
          f"orbits {ro}+{lo} overlap={ov}")
    print(f"  right move: {'down' if rdy>0 else 'up'} {abs(rdy)//3}, {'right' if rdx>0 else 'left'} {abs(rdx)//3}")
    print(f"  left  move: {'down' if ldy>0 else 'up'} {abs(ldy)//3}, {'right' if ldx>0 else 'left'} {abs(ldx)//3}")
else:
    print("\nno tiling found. right fits sample:", rf[:5], " left:", lf[:5])
