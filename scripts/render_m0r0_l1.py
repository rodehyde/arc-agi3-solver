"""Render m0r0 Level 1 grid visually."""
import numpy as np
from arc_agi import Arcade, OperationMode

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space
grid = np.array(obs.frame[-1])

# Compact char map: . = white, # = black wall, Y = yellow, O = orange, L = lt-blue
char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
        8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

print(f"Grid 64x64  (# = black wall, Y = yellow, O = orange, L = lt-blue block)")
print(f"     " + "".join(f"{c%10}" for c in range(64)))
print(f"     " + "".join(f"{c//10}" for c in range(64)))
print()
for r in range(64):
    row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
    print(f"{r:3d}  {row_str}")
