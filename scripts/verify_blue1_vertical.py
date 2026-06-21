"""Verify Blue-1 vertical movement in frozen state."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs

def yellow_pos(obs):
    g = np.array(obs.frame[-1])
    y = np.argwhere(g == 11)
    if not len(y): return None
    return (int(y[:,0].min()), int(y[:,1].min()))

# --- Test UP ---
print("=== Blue-1 frozen, then UP ===")
env, obs = make_l3()
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
print(f"After freeze: yellow at {yellow_pos(obs)}")
obs = env.step(GameAction.ACTION1)
pos = yellow_pos(obs)
print(f"After UP:     yellow at {pos}")
# Show grid around that area
g = np.array(obs.frame[-1])
char = {0:'.', 1:'a', 5:'#', 8:'R', 9:'B', 10:'L', 11:'Y', 15:'V'}
if pos:
    r0, c0 = max(0, pos[0]-2), max(0, pos[1]-4)
    r1, c1 = min(63, pos[0]+4), min(63, pos[1]+8)
    print(f"Grid around yellow (rows {r0}-{r1}, cols {c0}-{c1}):")
    for r in range(r0, r1+1):
        print(f"  {r:2d}: " + "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1)))

# --- Test DOWN ---
print("\n=== Blue-1 frozen, then DOWN ===")
env, obs = make_l3()
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
print(f"After freeze: yellow at {yellow_pos(obs)}")
obs = env.step(GameAction.ACTION2)
pos = yellow_pos(obs)
print(f"After DOWN:   yellow at {pos}")
if pos:
    g = np.array(obs.frame[-1])
    r0, c0 = max(0, pos[0]-2), max(0, pos[1]-4)
    r1, c1 = min(63, pos[0]+4), min(63, pos[1]+8)
    print(f"Grid around yellow (rows {r0}-{r1}, cols {c0}-{c1}):")
    for r in range(r0, r1+1):
        print(f"  {r:2d}: " + "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1)))

# --- Check what's at rows 11-12 and 19-20 cols 31-32 ---
print("\n=== Grid values at candidate positions ===")
env, obs = make_l3()
g = np.array(obs.frame[-1])
vals = {0:'white', 1:'lt-grey', 5:'black', 8:'red', 9:'blue', 10:'lt-blue', 11:'yellow', 15:'purple'}
for r in range(10, 22):
    row_vals = [int(g[r, c]) for c in range(29, 36)]
    print(f"  row {r:2d} cols 29-35: {[vals.get(v,v) for v in row_vals]}")
