"""ar25 L7: render yellow, its 4-fold closure about candidate axis, and the gap."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
Y = (g == 11); Y[:, 63] = False
B = (g == 5); B[63, :] = False
Yc = set(zip(*np.where(Y)))

# try several axes; for each compute closure size and gap
for (ra, ca) in [(22, 37), (22, 38), (21.5, 37), (22.5, 37.5)]:
    F = set()
    for (rr, cc) in Yc:
        for (mr, mc) in [(rr, cc), (rr, int(2*ca-cc)), (int(2*ra-rr), cc), (int(2*ra-rr), int(2*ca-cc))]:
            if 0 <= mr < 64 and 0 <= mc < 64:
                F.add((mr, mc))
    gap = F - Yc
    print(f"axis(row={ra},col={ca}): closure={len(F)} yellow={len(Yc)} gap={len(gap)}")

# render: yellow vs closure(22,37) vs gap, plus current black
ra, ca = 22, 37
F = set()
for (rr, cc) in Yc:
    for (mr, mc) in [(rr, cc), (rr, 2*ca-cc), (2*ra-rr, cc), (2*ra-rr, 2*ca-cc)]:
        if 0 <= mr < 64 and 0 <= mc < 64:
            F.add((mr, mc))
gap = F - Yc

img_F = np.zeros((64, 64));
for (rr, cc) in F: img_F[rr, cc] = 1
for (rr, cc) in gap: img_F[rr, cc] = 2   # gap highlighted
img_B = np.zeros((64, 64))
for (rr, cc) in zip(*np.where(B)): img_B[rr, cc] = 1

fig, axs = plt.subplots(1, 2, figsize=(20, 10))
axs[0].imshow(img_F, cmap='viridis', vmin=0, vmax=2)
axs[0].set_title("closure about (22,37): yellow=teal, GAP=yellow")
axs[1].imshow(img_B, cmap='gray')
axs[1].set_title("black pieces (current)")
for ax in axs:
    ax.set_xticks(range(0, 64, 3)); ax.set_yticks(range(0, 64, 3))
    ax.grid(True, color='#888', linewidth=0.3)
plt.savefig("scripts/l7_closure.png", dpi=70, bbox_inches='tight')
print("saved scripts/l7_closure.png")
