"""Level 4 inspection script for m0r0. Replays L1+L2+L3 then renders L4."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
char = {0: '.', 1: 'a', 2: 'm', 3: 'd', 4: 'v', 5: '#', 6: 'p', 7: 'q',
        8: 'R', 9: 'B', 10: 'L', 11: 'Y', 12: 'O', 13: 'M', 14: 'G', 15: 'V'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space

# Replay L1
for a in L1:
    obs = env.step(AMAP[a])
print(f"After L1: levels_completed={obs.levels_completed}")

# Replay L2
for a in L2:
    obs = env.step(AMAP[a])
print(f"After L2: levels_completed={obs.levels_completed}")

# Replay L3: marker moves + navigation
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
for act in [GameAction.ACTION4, GameAction.ACTION1,
            GameAction.ACTION4, GameAction.ACTION4,
            GameAction.ACTION4, GameAction.ACTION4,
            GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
            GameAction.ACTION3, GameAction.ACTION3,
            GameAction.ACTION1]:
    obs = env.step(act)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})

g = np.array(obs.frame[-1])
bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
    obs = env.step(act)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})

g = np.array(obs.frame[-1])
bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
for _ in range(3):
    obs = env.step(GameAction.ACTION4)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})

for a in NAV3:
    obs = env.step(AMAP[a])
print(f"After L3: levels_completed={obs.levels_completed}")

# L4 is now active
g = np.array(obs.frame[-1])
print(f"\nL4 grid shape: {g.shape}")
print(f"Available actions: {obs.available_actions}")
print(f"win_levels={obs.win_levels}, levels_completed={obs.levels_completed}")

# Unique values
vals = sorted(np.unique(g))
print(f"Values present: {vals}")
val_labels = {0:'white', 1:'lt-grey', 2:'md-grey', 3:'dk-grey', 4:'vdk-grey',
              5:'black', 6:'pink', 7:'lt-pink', 8:'red', 9:'blue',
              10:'lt-blue', 11:'yellow', 12:'orange', 13:'maroon', 14:'green', 15:'purple'}
for v in vals:
    count = int(np.sum(g == v))
    print(f"  {v} ({val_labels.get(v, '?')}): {count} cells")

# Full grid render
print("\n=== FULL GRID (L4) ===")
print("     " + "".join(f"{c % 10}" for c in range(64)))
print("     " + "".join(f"{c // 10}" for c in range(64)))
for r in range(64):
    row = "".join(char.get(int(g[r, c]), '?') for c in range(64))
    # Annotate interesting rows
    special = []
    row_vals = set(int(g[r, c]) for c in range(64))
    for v in [9, 10, 11, 14]:
        if v in row_vals:
            cols = [c for c in range(64) if g[r, c] == v]
            special.append(f"{val_labels[v]}@{cols}")
    ann = "  <- " + ", ".join(special) if special else ""
    print(f"{r:3d}  {row}{ann}")

# Block positions
lt_blue = np.argwhere(g == 10)
if len(lt_blue):
    left = lt_blue[lt_blue[:, 1] < 32]
    right = lt_blue[lt_blue[:, 1] >= 32]
    if len(left):
        print(f"\nLeft block: rows {left[:,0].min()}-{left[:,0].max()}, cols {left[:,1].min()}-{left[:,1].max()}")
    if len(right):
        print(f"Right block: rows {right[:,0].min()}-{right[:,0].max()}, cols {right[:,1].min()}-{right[:,1].max()}")

# Blue markers
blue = np.argwhere(g == 9)
if len(blue):
    print(f"\nBlue markers (value=9): {sorted((int(r), int(c)) for r, c in blue)}")
else:
    print("\nNo blue markers in L4.")

# Green cells
green = np.argwhere(g == 14)
if len(green):
    print(f"Green cells (value=14): {sorted((int(r), int(c)) for r, c in green)}")
