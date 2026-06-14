"""ar25 L6: find shifts for each piece so its 4-fold orbit (reflect about col19,row34)
lands on the yellow figure; union of both orbits should == yellow."""
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


def boxset(mask):
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
upper = B.copy(); upper[24:, :] = False
lower = B.copy(); lower[:24, :] = False
Yb, Ub, Lb = boxset(Y), boxset(upper), boxset(lower)


def orbit(boxes):
    out = set()
    for (br, bc) in boxes:
        out.add((br, bc))
        out.add((br, 36 - bc))
        out.add((66 - br, bc))
        out.add((66 - br, 36 - bc))
    return out


shifts = [(dy, dx) for dy in range(-60, 61, 3) for dx in range(-60, 61, 3)]


def fits(piece):
    res = []
    for dy, dx in shifts:
        sh = {(r2+dy, c2+dx) for (r2, c2) in piece}
        orb = orbit(sh)
        if orb <= Yb:
            res.append((dy, dx, len(orb)))
    return res


uf = fits(Ub)
lf = fits(Lb)
print(f"upper: {len(uf)} placements whose 4-orbit ⊆ yellow")
print(f"lower: {len(lf)} placements whose 4-orbit ⊆ yellow")

# find a pair whose orbits union to exactly Yb
sol = None
for (udy, udx, uo) in uf:
    uorb = orbit({(r2+udy, c2+udx) for (r2, c2) in Ub})
    for (ldy, ldx, lo) in lf:
        lorb = orbit({(r2+ldy, c2+ldx) for (r2, c2) in Lb})
        if uorb | lorb == Yb:
            sol = (udy, udx, ldy, ldx, len(uorb), len(lorb), len(uorb & lorb))
            break
    if sol:
        break
if sol:
    udy, udx, ldy, ldx, uo, lo, ov = sol
    print(f"\nSOLUTION: upper shift dy={udy} dx={udx} (orbit {uo}); "
          f"lower shift dy={ldy} dx={ldx} (orbit {lo}); overlap={ov}")
    print(f"  upper move: {'down' if udy>0 else 'up'} {abs(udy)//3}, "
          f"{'right' if udx>0 else 'left'} {abs(udx)//3}")
    print(f"  lower move: {'down' if ldy>0 else 'up'} {abs(ldy)//3}, "
          f"{'right' if ldx>0 else 'left'} {abs(ldx)//3}")
else:
    print("\nno exact orbit-union solution found")
    if uf:
        print("sample upper fits:", uf[:5])
    if lf:
        print("sample lower fits:", lf[:5])
