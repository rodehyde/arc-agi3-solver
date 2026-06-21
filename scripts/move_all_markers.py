"""Execute Blue-1 complex path, then Blue-2 and Blue-3.
Report yellow position after each step, then render final grid."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
char = {0:'.', 1:'a', 5:'#', 8:'R', 9:'B', 10:'L', 11:'Y', 15:'V'}

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

def move_until_stuck(env, obs, action, label, max_steps=20):
    """Repeat action until yellow stops moving. Return final obs."""
    prev = yellow_pos(obs)
    for i in range(max_steps):
        obs2 = env.step(action)
        pos = yellow_pos(obs2)
        if pos is None or pos == prev:
            print(f"  {label} step {i+1}: stuck at {prev}")
            return obs
        print(f"  {label} step {i+1}: yellow {prev} -> {pos}")
        prev = pos
        obs = obs2
    return obs

def find_and_click_blue(obs_grid, row_range, col_range):
    """Return (x,y) of first blue cell in range."""
    for r in range(row_range[0], row_range[1]+1):
        for c in range(col_range[0], col_range[1]+1):
            if obs_grid[r, c] == 9:
                return c, r
    return None

def restore(env, obs, black_cell_xy):
    """Restore frozen state by clicking a black wall cell."""
    x, y = black_cell_xy
    obs2 = env.step(GameAction.ACTION6, {"x": x, "y": y})
    g = np.array(obs2.frame[-1])
    yellow = np.argwhere(g == 11)
    if len(yellow):
        print(f"  RESTORE FAILED — yellow still present at {int(yellow[:,0].min()),int(yellow[:,1].min())}")
    else:
        print(f"  Restored (clicked black at {black_cell_xy})")
    return obs2

env, obs = make_l3()
g0 = np.array(obs.frame[-1])

# ── BLUE-1: complex path ────────────────────────────────────────────────────
print("="*60)
print("BLUE-1 MOVE SEQUENCE")
print("="*60)
bxy = find_and_click_blue(g0, (14,17), (30,33))
print(f"Blue-1 found at click coords: {bxy}")
obs = env.step(GameAction.ACTION6, {"x": bxy[0], "y": bxy[1]})
print(f"Frozen. Yellow at: {yellow_pos(obs)}")

print("\n1. RIGHT as far as possible:")
obs = move_until_stuck(env, obs, GameAction.ACTION4, "RIGHT")
print(f"   => {yellow_pos(obs)}")

print("\n2. UP as far as possible:")
obs = move_until_stuck(env, obs, GameAction.ACTION1, "UP")
print(f"   => {yellow_pos(obs)}")

print("\n3. RIGHT as far as possible:")
obs = move_until_stuck(env, obs, GameAction.ACTION4, "RIGHT")
print(f"   => {yellow_pos(obs)}")

print("\n4. DOWN as far as possible:")
obs = move_until_stuck(env, obs, GameAction.ACTION2, "DOWN")
print(f"   => {yellow_pos(obs)}")

print("\n5. LEFT until UP is possible, then UP to cul-de-sac:")
for i in range(20):
    pos_before = yellow_pos(obs)
    # Try UP — if it moves, we found the upward path
    test_obs = env.step(GameAction.ACTION1)
    pos_after = yellow_pos(test_obs)
    if pos_after and pos_after != pos_before:
        print(f"  UP works from {pos_before} -> {pos_after}! Going UP to cul-de-sac...")
        obs = test_obs
        obs = move_until_stuck(env, obs, GameAction.ACTION1, "UP (cul-de-sac)")
        break
    else:
        # UP didn't work, go LEFT
        obs = env.step(GameAction.ACTION3)
        pos_left = yellow_pos(obs)
        if pos_left == pos_before:
            print(f"  LEFT stuck at {pos_before} — no more moves")
            break
        print(f"  LEFT: {pos_before} -> {pos_left}")

print(f"\nBlue-1 final position: {yellow_pos(obs)}")
obs = restore(env, obs, (14, 46))  # black wall cell at row=46, col=14

# ── BLUE-2: UP → RIGHT → UP → restore ──────────────────────────────────────
print("\n" + "="*60)
print("BLUE-2 MOVE SEQUENCE")
print("="*60)
g_cur = np.array(obs.frame[-1])
bxy2 = find_and_click_blue(g_cur, (18,22), (10,14))
print(f"Blue-2 found at click coords: {bxy2}")
obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
print(f"Frozen. Yellow at: {yellow_pos(obs)}")

obs2 = env.step(GameAction.ACTION1)
print(f"UP: {yellow_pos(obs2)}")
obs2 = env.step(GameAction.ACTION4)
print(f"RIGHT: {yellow_pos(obs2)}")
obs2 = env.step(GameAction.ACTION1)
print(f"UP: {yellow_pos(obs2)}")
obs = obs2
print(f"Blue-2 final position: {yellow_pos(obs)}")
obs = restore(env, obs, (14, 46))

# ── BLUE-3: RIGHT ×3 → restore ──────────────────────────────────────────────
print("\n" + "="*60)
print("BLUE-3 MOVE SEQUENCE")
print("="*60)
g_cur = np.array(obs.frame[-1])
bxy3 = find_and_click_blue(g_cur, (30,34), (38,42))
print(f"Blue-3 found at click coords: {bxy3}")
obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
print(f"Frozen. Yellow at: {yellow_pos(obs)}")

for i in range(3):
    obs2 = env.step(GameAction.ACTION4)
    print(f"RIGHT {i+1}: {yellow_pos(obs2)}")
    obs = obs2

print(f"Blue-3 final position: {yellow_pos(obs)}")
obs = restore(env, obs, (14, 46))

# ── RENDER FINAL GRID (central section) ─────────────────────────────────────
print("\n" + "="*60)
print("FINAL GRID STATE (rows 10-55)")
print("="*60)
g_final = np.array(obs.frame[-1])
print("     " + "".join(f"{c%10}" for c in range(64)))
for r in range(10, 56):
    row_str = "".join(char.get(int(g_final[r, c]), '?') for c in range(64))
    markers = ""
    if 9 in [g_final[r,c] for c in range(64)]:
        bcols = [c for c in range(64) if g_final[r,c]==9]
        markers = f"  <- Blue marker at cols {bcols}"
    if 10 in [g_final[r,c] for c in range(64)]:
        lcols = [c for c in range(64) if g_final[r,c]==10]
        markers += f"  <- LtBlue block at cols {lcols}"
    print(f"{r:3d}  {row_str}{markers}")

# ── CENTRAL PASSAGE STATUS ───────────────────────────────────────────────────
print("\n" + "="*60)
print("CENTRAL PASSAGE STATUS (rows 14-17, cols 26-37)")
print("="*60)
print("     " + "".join(f"{c%10}" for c in range(20, 45)))
for r in range(13, 22):
    row_str = "".join(char.get(int(g_final[r, c]), '?') for c in range(20, 45))
    print(f"{r:3d}  {row_str}")

blue_in_passage = [(r,c) for r in range(14,18) for c in range(26,38)
                   if g_final[r,c] == 9]
print(f"\nBlue markers in central passage: {blue_in_passage}")
print(f"Central passage clear: {len(blue_in_passage) == 0}")
