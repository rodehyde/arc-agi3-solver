"""m0r0 Level 3 — Step 1: scene inspection."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space
for a in L1 + L2:
    obs = env.step(AMAP[a])

print(f"levels_completed={obs.levels_completed}  win_levels={obs.win_levels}")
print(f"available_actions={obs.available_actions}")

grid = np.array(obs.frame[-1])
colours = {0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
           6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
           12:'orange',13:'maroon',14:'green',15:'purple'}
print("\nColours present:")
vals, counts = np.unique(grid, return_counts=True)
for v, c in zip(vals, counts):
    print(f"  {v} ({colours.get(v,'?')}): {c} cells")

cells = np.argwhere(grid == 10)
if len(cells):
    rows, cols = cells[:, 0], cells[:, 1]
    print(f"\nlt-blue blocks: {len(cells)} cells, rows {rows.min()}-{rows.max()} cols {cols.min()}-{cols.max()}")

char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
        8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}
print("\nGrid:")
print("     " + "".join(f"{c%10}" for c in range(64)))
print("     " + "".join(f"{c//10}" for c in range(64)))
for r in range(64):
    row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
    print(f"{r:3d}  {row_str}")
