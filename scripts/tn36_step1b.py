"""tn36 Step 1b — detailed zone mapping."""
import numpy as np
from arc_agi import Arcade, OperationMode

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs = env.observation_space
g = np.array(obs.frame[-1])

colour = {0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
          6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
          12:'orange',13:'maroon',14:'green',15:'purple'}
char = {0:'.',1:'f',2:'m',3:'d',4:'v',5:'#',6:'p',7:'q',8:'R',9:'B',
        10:'L',11:'Y',12:'O',13:'M',14:'G',15:'V'}

# Print each distinct zone with exact cell values
print("=== YELLOW CELLS (value=11) exact positions ===")
yc = np.argwhere(g==11)
for r,c in yc:
    print(f"  row {r}, col {c}")

print("\n=== LT-GREY CELLS (value=1) exact positions ===")
fc = np.argwhere(g==1)
for r,c in fc:
    print(f"  row {r}, col {c}")

print("\n=== BLUE CELLS (value=9) exact positions ===")
bc = np.argwhere(g==9)
# Group by row
rows = sorted(set(int(r) for r,c in bc))
for r in rows:
    cols_in_row = sorted(int(c) for rc,c in bc if rc==r)
    print(f"  row {r}: cols {cols_in_row[0]}–{cols_in_row[-1]} ({len(cols_in_row)} cells)")

# Detailed look at legend zone (rows 41-47)
print("\n=== LEGEND ZONE (rows 41-47) detailed ===")
for r in range(41, 48):
    vals = [(c, int(g[r,c])) for c in range(13,51) if g[r,c] != 5]
    non_black = [(c, colour.get(int(g[r,c]),'?')) for c in range(13,51) if g[r,c] not in (0,5)]
    print(f"  row {r}: non-background = {non_black}")

# Detailed look at yellow zone 1 (rows 13-16)
print("\n=== YELLOW ZONE 1 (rows 12-17) ===")
for r in range(12, 18):
    row_vals = {c: int(g[r,c]) for c in range(26, 40)}
    print(f"  row {r} cols 26-39: {[row_vals[c] for c in range(26,40)]}")

# Detailed look at yellow zone 2 (rows 33-37)
print("\n=== YELLOW ZONE 2 (rows 32-38) ===")
for r in range(32, 39):
    row_vals = {c: int(g[r,c]) for c in range(25, 39)}
    print(f"  row {r} cols 25-38: {[row_vals[c] for c in range(25,39)]}")

# Check if checkerboard pattern is regular
print("\n=== CHECKERBOARD STRUCTURE (sample rows 9-20, cols 14-30) ===")
for r in range(9, 21):
    row = ''.join(char.get(int(g[r,c]),'?') for c in range(14,31))
    print(f"  row {r}: {row}")

# Check what's at the path between checkered grid and blue oval
print("\n=== PATH AREA (rows 47-52) ===")
for r in range(47, 53):
    row = ''.join(char.get(int(g[r,c]),'?') for c in range(30,50))
    print(f"  row {r} cols 30-49: {row}")
