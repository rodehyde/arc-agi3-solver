"""Level 5 inspection script for m0r0. Replays L1-L4 then renders L5."""
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

val_labels = {0:'white', 1:'lt-grey', 2:'md-grey', 3:'dk-grey', 4:'vdk-grey',
              5:'black', 6:'pink', 7:'lt-pink', 8:'red', 9:'blue',
              10:'lt-blue', 11:'yellow', 12:'orange', 13:'maroon', 14:'green', 15:'purple'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space

# L1
for a in L1:
    obs = env.step(AMAP[a])
print(f"After L1: levels_completed={obs.levels_completed}")

# L2
for a in L2:
    obs = env.step(AMAP[a])
print(f"After L2: levels_completed={obs.levels_completed}")

# L3
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
for act in [GameAction.ACTION4, GameAction.ACTION1,
            GameAction.ACTION4, GameAction.ACTION4,
            GameAction.ACTION4, GameAction.ACTION4,
            GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
            GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
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

# L4: U,U, freeze, X,X,X, restore, D,D,C,D,C,C
for a in 'UU':
    obs = env.step(AMAP[a])
obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})   # freeze
for _ in range(3):
    obs = env.step(GameAction.ACTION3)                     # DIVERGE x3
obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})    # restore
for a in 'DDCDCC':
    obs = env.step(AMAP[a])
print(f"After L4: levels_completed={obs.levels_completed}")

# L5 is now active
g = np.array(obs.frame[-1])
print(f"\nL5 grid shape: {g.shape}")
print(f"Available actions: {obs.available_actions}")
print(f"win_levels={obs.win_levels}, levels_completed={obs.levels_completed}")

vals = sorted(np.unique(g))
print(f"Values present: {vals}")
for v in vals:
    count = int(np.sum(g == v))
    print(f"  {v} ({val_labels.get(v,'?')}): {count} cells")

print("\n=== FULL GRID (L5) ===")
print("     " + "".join(f"{c%10}" for c in range(64)))
print("     " + "".join(f"{c//10}" for c in range(64)))
for r in range(64):
    row = "".join(char.get(int(g[r, c]), '?') for c in range(64))
    special = []
    for v in [9, 10, 11, 14]:
        if v in set(int(g[r, c]) for c in range(64)):
            cols = [c for c in range(64) if g[r, c] == v]
            special.append(f"{val_labels[v]}@{cols}")
    ann = "  <- " + ", ".join(special) if special else ""
    # Also annotate red rows
    red_cols = [c for c in range(64) if g[r, c] == 8]
    if red_cols:
        ann += f"  RED@{red_cols}"
    print(f"{r:3d}  {row}{ann}")

# Block positions
lt_blue = np.argwhere(g == 10)
if len(lt_blue):
    left = lt_blue[lt_blue[:, 1] < 32]
    right = lt_blue[lt_blue[:, 1] >= 32]
    if len(left):
        print(f"\nLeft block (lt-blue): rows {left[:,0].min()}-{left[:,0].max()}, cols {left[:,1].min()}-{left[:,1].max()}")
    if len(right):
        print(f"Right block (lt-blue): rows {right[:,0].min()}-{right[:,0].max()}, cols {right[:,1].min()}-{right[:,1].max()}")

blue = np.argwhere(g == 9)
if len(blue):
    print(f"\nBlue markers (value=9): rows {blue[:,0].min()}-{blue[:,0].max()}, cols {blue[:,1].min()}-{blue[:,1].max()}")
    print(f"  All cells: {sorted((int(r),int(c)) for r,c in blue)}")
