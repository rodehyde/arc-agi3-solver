"""ar25 L3: replay to level 3 and describe the scene in text."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}
# Solutions as action numbers
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8

COLOR = {0: 'white', 1: 'lt-grey', 2: 'md-grey', 3: 'dk-grey', 4: 'vdk-grey',
         5: 'black', 6: 'pink', 7: 'lt-pink', 8: 'red', 9: 'blue', 10: 'lt-blue',
         11: 'yellow', 12: 'orange', 13: 'maroon', 14: 'green', 15: 'purple'}


def grid(f):
    return np.array(f.frame[-1])


def describe(g):
    vals, counts = np.unique(g, return_counts=True)
    print(f"grid shape: {g.shape}")
    print("colour histogram:")
    for v, c in sorted(zip(vals, counts), key=lambda x: -x[1]):
        print(f"   {v:2d} {COLOR.get(v,'?'):8s}: {c} cells")
    print("\nbounding box per non-background colour:")
    bg = vals[np.argmax(counts)]
    for v in vals:
        if v == bg:
            continue
        ys, xs = np.where(g == v)
        print(f"   {v:2d} {COLOR.get(v,'?'):8s}: rows {ys.min()}-{ys.max()}, "
              f"cols {xs.min()}-{xs.max()}  ({len(ys)} cells)")
    return bg


arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ar25")
r = env.observation_space
print(f"win_levels={r.win_levels} baseline={env.info.baseline_actions}")
for a in L1:
    r = env.step(A[a], data={})
for a in L2:
    r = env.step(A[a], data={})
print(f"\nAfter replay: levels_completed={r.levels_completed} state={r.state.name}")
print(f"available_actions={r.available_actions}")
g = grid(r)
print("\n===== LEVEL 3 STARTING SCENE =====")
describe(g)

# print a downsampled ascii of the grid (every cell, compact)
print("\nASCII grid (hex per cell, '.' = background):")
bg = np.bincount(g.flatten()).argmax()
for y in range(g.shape[0]):
    row = g[y]
    if np.all(row == bg):
        continue
    line = ''.join('.' if v == bg else format(int(v), 'x') for v in row)
    print(f"{y:2d} {line}")
