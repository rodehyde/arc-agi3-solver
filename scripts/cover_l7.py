"""ar25 L7: find piece placements so black ∪ rot180(black) COVERS all yellow boxes
(rot180 about centroid box-map: (br,bc)->(42-br,72-bc)). Then test in-game."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
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
PALETTE = ['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
           '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in PRE:
        r = env.step(A[a], data={})
    return env, r


def boxset(mask):
    s = set()
    for br in range(0, 64, 3):
        for bc in range(0, 64, 3):
            if mask[br:br+3, bc:bc+3].any():
                s.add((br, bc))
    return s


def rot(b):           # 180 about (row22,col37): box (br,bc)->(42-br,72-bc)
    return (42 - b[0], 72 - b[1])


def orbit2(boxes):
    return set(boxes) | {rot(b) for b in boxes}


env, r = fresh()
g = grid(r)
Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
Yb = boxset(Y)
right = B.copy(); right[:, :40] = False
left = B.copy(); left[:, 40:] = False
Rb, Lb = boxset(right), boxset(left)
print(f"yellow boxes={len(Yb)} right={len(Rb)} left={len(Lb)}")


def onbox(b):
    return 0 <= b[0] <= 60 and 0 <= b[1] <= 60


def placements(piece):
    out = {}
    for dy in range(-48, 13, 3):
        for dx in range(-39, 33, 3):
            placed = {(b[0]+dy, b[1]+dx) for b in piece}
            orb = orbit2(placed)
            if all(onbox(b) for b in orb):
                out[(dy, dx)] = orb
    return out


RP, LP = placements(Rb), placements(Lb)
print(f"valid right placements={len(RP)} left={len(LP)}")

best = None
for (rdy, rdx), rorb in RP.items():
    for (ldy, ldx), lorb in LP.items():
        cover = rorb | lorb
        if Yb <= cover:
            extra = len(cover - Yb)
            if best is None or extra < best[0]:
                best = (extra, rdy, rdx, ldy, ldx)
if not best:
    print("NO covering placement found.")
    raise SystemExit
extra, rdy, rdx, ldy, ldx = best
print(f"COVER found: right dy={rdy} dx={rdx}; left dy={ldy} dx={ldx}; extra boxes outside yellow={extra}")
print(f"  right move: {'down' if rdy>0 else 'up'} {abs(rdy)//3}, {'right' if rdx>0 else 'left'} {abs(rdx)//3}")
print(f"  left  move: {'down' if ldy>0 else 'up'} {abs(ldy)//3}, {'right' if ldx>0 else 'left'} {abs(ldx)//3}")


def mv(dy, dx):
    s = []
    s += [2]*(dy//3) if dy > 0 else [1]*(-dy//3)
    s += [4]*(dx//3) if dx > 0 else [3]*(-dx//3)
    return s


# states 0=hband 1=vband 2=right 3=left
SEQ = [5,5] + mv(rdy, rdx) + [5] + mv(ldy, ldx) + [5] + [2]*2 + [5] + [4]*9
# from state0: A5x2->state2(right); A5->state3(left); A5->state0(hband down2); A5->state1(vband right9)
env, r = fresh()
gb = grid(r)
won = None
for i, a in enumerate(SEQ, 1):
    r = env.step(A[a], data={})
    if r.levels_completed >= 7:
        won = i; break
print(f"\nIN-GAME: win={'YES @'+str(won) if won else 'NO'} levels={r.levels_completed}/{r.win_levels}")

cmap = ListedColormap(PALETTE)
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, gg, t in [(axs[0], gb, "before"), (axs[1], grid(r), "after")]:
    ax.imshow(gg, cmap=cmap, vmin=0, vmax=15)
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3); ax.set_title(t)
plt.savefig("scripts/l7_cover.png", dpi=70, bbox_inches='tight')
print("saved scripts/l7_cover.png")
