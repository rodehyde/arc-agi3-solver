"""Diagnose Level 3: navigate to row=22 ceiling and render the maze above it."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
        8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs

def render(grid, r0, r1, label=""):
    print(f"\n{label}")
    print("     " + "".join(f"{c%10}" for c in range(64)))
    for r in range(r0, r1+1):
        row_str = "".join(char.get(int(grid[r, c]), '?') for c in range(64))
        print(f"{r:3d}  {row_str}")

def get_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if not len(cells): return None
    rows, cols = cells[:, 0], cells[:, 1]
    return (int(rows.min()), int(cols.min()), int(cols.max()) - 3)

# Navigate to ceiling: UUUUUUXXXXXXXX (to get left block to col=10, then up)
# Path found by BFS: from (46,22,38) to (22,10,34)
# Let's trace a path: X gets left=18, right=42; X again: left=14, right=46
# But the ceiling states are left=10 — need more X's.
# Let's use: XXXXUUUUUUUU to diverge then go up

# Actually, let's just replay one of the known ceiling states by trying sequences
# Path to (22, 10, 34):  from BFS we know it's reachable but not the path.
# Let's navigate manually step by step.

env, obs = make_l3()
print(f"Start: {get_state(obs)}")
grid = np.array(obs.frame[-1])
render(grid, 10, 55, "=== Initial grid rows 10-55 ===")

# Try to reach row=22 by going up from row=46
# Need: left_col=10, right_col=34
# Start: left=22, right=38. Need to diverge to left=10: 3 X's (22→18→14→10)
# And right needs to converge to 34: from 42 after 3X → right=42+12=54? No.
# DIVERGE: left-=4, right+=4. CONVERGE: left+=4, right-=4.
# Start: left=22, right=38
# 3 X: left=10, right=50
# 4 C: right=50-16=34, left=10+16=26... no
# 3 X then 3 C: left=10+12=22, right=50-12=38 — back to start!
#
# Let's just use XXXXCCUUUUUU:
# XXXX: left=22-16=6, right=38+16=54
# CC: left=6+8=14, right=54-8=46
# Hmm.
#
# Better: use BFS path. From reachable states we know (22,10,34) exists.
# Let's try XXXXXUUUUUUU:
# XXXXX: left=22-20=2, right=38+20=58 — probably out of bounds
#
# Let's try: XXX then navigate up
path = 'XXXUUUUUUU'
env, obs = make_l3()
for a in path:
    obs = env.step(AMAP[a])
    s = get_state(obs)
    print(f"  {a}: {s}")

print(f"\nAfter {path}:")
grid = np.array(obs.frame[-1])
render(grid, 10, 55, f"=== Grid after {path} ===")

# Now try to go further up
print("\n--- Trying to go UP from here ---")
env2, obs2 = make_l3()
for a in path:
    obs2 = env2.step(AMAP[a])

for move in ['U', 'D', 'X', 'C']:
    env3, obs3 = make_l3()
    for a in path:
        obs3 = env3.step(AMAP[a])
    obs_after = env3.step(AMAP[move])
    s_before = get_state(obs2)
    s_after = get_state(obs_after)
    print(f"  {move}: {s_before} -> {s_after}")
