"""Render m0r0 Level 3 initial state. Show all blue marker positions and maze structure."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
        8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space
for a in L1 + L2:
    obs = env.step(AMAP[a])

grid = np.array(obs.frame[-1])

# --- Blue marker positions ---
blue = np.argwhere(grid == 9)
lt_blue = np.argwhere(grid == 10)
print("=== Blue markers (value=9) ===")
if len(blue):
    print(f"  All blue cells: {sorted((int(r),int(c)) for r,c in blue)}")
    # Cluster by proximity
    rows_b = sorted(set(int(r) for r,c in blue))
    print(f"  Row range: {min(rows_b)}-{max(rows_b)}")
    cols_b = sorted(set(int(c) for r,c in blue))
    print(f"  Col range: {min(cols_b)}-{max(cols_b)}")
    # Group into clusters (gap > 4 = new cluster)
    clusters = []
    cur = [blue[0]]
    for cell in blue[1:]:
        prev = cur[-1]
        if abs(int(cell[0])-int(prev[0])) + abs(int(cell[1])-int(prev[1])) <= 8:
            cur.append(cell)
        else:
            clusters.append(cur)
            cur = [cell]
    clusters.append(cur)
    for i, cl in enumerate(clusters):
        rs = [int(r) for r,c in cl]
        cs = [int(c) for r,c in cl]
        print(f"  Cluster {i+1}: rows {min(rs)}-{max(rs)}, cols {min(cs)}-{max(cs)}")

print(f"\n=== Lt-blue blocks (value=10) ===")
if len(lt_blue):
    rs = [int(r) for r,c in lt_blue]
    cs = [int(c) for r,c in lt_blue]
    print(f"  Rows {min(rs)}-{max(rs)}, cols {min(cs)}-{max(cs)}")
    left  = lt_blue[lt_blue[:,1] < 32]
    right = lt_blue[lt_blue[:,1] >= 32]
    if len(left):
        print(f"  Left block:  rows {int(left[:,0].min())}-{int(left[:,0].max())}, cols {int(left[:,1].min())}-{int(left[:,1].max())}")
    if len(right):
        print(f"  Right block: rows {int(right[:,0].min())}-{int(right[:,0].max())}, cols {int(right[:,1].min())}-{int(right[:,1].max())}")

# --- Full grid render ---
print(f"\n=== Full grid (rows 10-55) ===")
print("     " + "".join(f"{c%10}" for c in range(64)))
print("     " + "".join(f"{c//10}" for c in range(64)))
for r in range(10, 56):
    row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
    print(f"{r:3d}  {row_str}")

# --- Central divider rows 13-20 zoomed ---
print(f"\n=== Central divider detail (rows 13-22, showing cols 20-44) ===")
print("     " + "".join(f"{c%10}" for c in range(20, 45)))
for r in range(13, 23):
    row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(20, 45))
    print(f"{r:3d}  {row_str}")
