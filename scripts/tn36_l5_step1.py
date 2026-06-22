"""tn36 L5 Step 1 — scene description: render grid and capture all observable state."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]

CMAP = {0:'.',1:'f',2:'m',3:'d',4:'v',5:'#',6:'K',7:'k',
        8:'r',9:'B',10:'L',11:'Y',12:'O',13:'M',14:'G',15:'P'}
CNAME = {0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
         6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
         12:'orange',13:'maroon',14:'green',15:'purple'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs = env.observation_space

for r, c in L1 + L2 + L3 + L4:
    obs = env.step(GameAction.ACTION6, {'x': c, 'y': r})

print(f"levels_completed={obs.levels_completed}  win_levels={obs.win_levels}")
print(f"available_actions={obs.available_actions}")
print(f"frames in obs: {len(obs.frame)}")

grid = np.array(obs.frame[-1])
print(f"\nGrid shape: {grid.shape}")

# Print full rendered grid
print("\n=== FULL GRID (obs.frame[-1]) ===")
print("     " + "".join(f"{c%10}" for c in range(64)))
print("     " + "".join(f"{c//10}" for c in range(64)))
for r in range(64):
    row_str = "".join(CMAP.get(int(grid[r,c]),'?') for c in range(64))
    if any(ch not in '.f' for ch in row_str):  # skip blank rows
        print(f"{r:3d}: {row_str}")

# Value inventory
print("\n=== VALUE INVENTORY ===")
vals, counts = np.unique(grid, return_counts=True)
for v, cnt in zip(vals, counts):
    print(f"  {v} ({CNAME.get(int(v),'?')}): {cnt} cells")

# Zone map — scan for non-background regions
print("\n=== ZONE SCAN (rows with interesting content) ===")
for r in range(64):
    row = grid[r, :]
    uv = set(int(x) for x in row) - {0,1,2,3,4,5}
    row_str = "".join(CMAP.get(int(grid[r,c]),'?') for c in range(64))
    if uv or '#' in row_str or 'Y' in row_str or 'K' in row_str or 'L' in row_str:
        vals_here = sorted(set(int(x) for x in row))
        print(f"  r{r:2d}: {row_str}  values={vals_here}")

# Left legend state — scan rows 33-49, cols 0-31
print("\n=== LEFT LEGEND STATE (rows 33-49, cols 0-31) ===")
for r in [33,35,39,41,45,47]:
    row_str = "".join(CMAP.get(int(grid[r,c]),'?') for c in range(0,32))
    active_cols = [c for c in range(0,32) if int(grid[r,c]) == 5]
    print(f"  r{r}: {row_str}  BLACK at cols={active_cols}")

# Right legend state — scan rows 33-49, cols 32-63
print("\n=== RIGHT LEGEND STATE (rows 33-49, cols 32-63) ===")
for r in [33,35,39,41,45,47]:
    row_str = "".join(CMAP.get(int(grid[r,c]),'?') for c in range(32,64))
    active_cols = [c for c in range(32,64) if int(grid[r,c]) == 5]
    print(f"  r{r}: {row_str}  BLACK at cols={active_cols}")

# Yellow piece (agent) location
print("\n=== YELLOW PIECE (value=11) ===")
yellow = [(int(r),int(c)) for r,c in np.argwhere(grid==11)]
if yellow:
    ry = sorted(set(r for r,c in yellow))
    cy = sorted(set(c for r,c in yellow))
    print(f"  rows={ry}  cols={cy}  count={len(yellow)}")
else:
    print("  None found")

# Pink band (value=6) location
print("\n=== PINK BAND (value=6) ===")
pink = [(int(r),int(c)) for r,c in np.argwhere(grid==6)]
if pink:
    rp = sorted(set(r for r,c in pink))
    cp = sorted(set(c for r,c in pink))
    print(f"  rows={rp}  cols={cp}")
    # Find gap (cols in pink row range that are NOT pink)
    if rp:
        r_sample = rp[0]
        all_cols = set(range(64))
        pink_cols_at_r = set(c for r,c in pink if r == r_sample)
        print(f"  At r{r_sample}: pink at cols={sorted(pink_cols_at_r)}, non-pink in c32-63: {sorted((all_cols - pink_cols_at_r) & set(range(32,64)))}")
else:
    print("  None found")

# Left piece (vdk-grey=4 in left panel) and right panel structure
print("\n=== LEFT PANEL PIECE SCAN (value=4 in cols 0-31, rows 3-31) ===")
for r in range(3, 32):
    seg = [int(grid[r,c]) for c in range(0,32)]
    vdkg = [c for c,v in enumerate(seg) if v == 4]
    blk  = [c for c,v in enumerate(seg) if v == 5]
    if blk:
        print(f"  r{r}: black(#) at cols={blk}  vdkgrey at={vdkg}")

print("\n=== RIGHT PANEL PIECE SCAN (yellow=11 OR black=5 in cols 32-63, rows 3-31) ===")
for r in range(3, 32):
    seg_str = "".join(CMAP.get(int(grid[r,c]),'?') for c in range(32,64))
    if 'Y' in seg_str or ('#' in seg_str and 'K' in seg_str):
        print(f"  r{r}: {seg_str}")
