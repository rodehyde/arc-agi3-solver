"""BFS on game state after all three markers are moved.
Check if both blocks can reach overlap in central passage."""
import numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

def setup_game():
    """Replay to L3 then move all three markers."""
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    g = np.array(obs.frame[-1])

    def find_blue(row_range, col_range):
        for r in range(row_range[0], row_range[1]+1):
            for c in range(col_range[0], col_range[1]+1):
                if g[r, c] == 9:
                    return c, r
        return None

    def freeze_move_restore(clicks, restore_xy=(14, 46)):
        nonlocal obs, g
        bx, by = clicks[0]
        obs = env.step(GameAction.ACTION6, {"x": bx, "y": by})
        for action in clicks[1:]:
            obs = env.step(action)
        obs = env.step(GameAction.ACTION6, {"x": restore_xy[0], "y": restore_xy[1]})
        g = np.array(obs.frame[-1])

    # Blue-1: RIGHT, UP, RIGHT×4, DOWN×3, UP×3 (to cul-de-sac rows 11-12 cols 51-52)
    bxy1 = find_blue((14, 17), (30, 33))
    obs = env.step(GameAction.ACTION6, {"x": bxy1[0], "y": bxy1[1]})
    for act in [GameAction.ACTION4,                    # RIGHT
                GameAction.ACTION1,                    # UP
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4, # RIGHT×4
                GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION2,                    # DOWN×3
                GameAction.ACTION1, GameAction.ACTION1,
                GameAction.ACTION1]:                   # UP×3 to cul-de-sac
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    b1 = np.argwhere(g == 9)
    b1_pos = (int(b1[b1[:,0]<20][:,0].min()), int(b1[b1[:,0]<20][:,1].min())) if any(b1[:,0]<20) else None
    print(f"Blue-1 final: {b1_pos}")

    # Blue-2: UP, RIGHT, UP
    bxy2 = None
    for r in range(18, 23):
        for c in range(10, 15):
            if g[r, c] == 9:
                bxy2 = (c, r)
                break
        if bxy2: break
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    print(f"Blue-2 final: rows 11-12 cols 15-16 (cul-de-sac)")

    # Blue-3: RIGHT×3
    bxy3 = None
    g = np.array(obs.frame[-1])
    for r in range(30, 34):
        for c in range(38, 43):
            if g[r, c] == 9:
                bxy3 = (c, r)
                break
        if bxy3: break
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3):
        obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    print(f"Blue-3 final: rows 31-32 cols 51-52")

    return env, obs

def get_state(obs):
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    if not len(cells): return None
    left  = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:,0].min()), int(left[:,1].min()),
            int(right[:,0].min()), int(right[:,1].min()))

def replay(path):
    env2, obs2 = setup_game()
    for a in path:
        obs2 = env2.step(AMAP[a])
    return env2, obs2

print("Setting up game with all markers moved...")
env0, obs0 = setup_game()
init = get_state(obs0)
print(f"\nStart state: L({init[0]},{init[1]}) R({init[2]},{init[3]})")

queue = deque([(init, "")])
visited = {init}
win_found = False
max_states = 3000

central_states = []  # both blocks in central passage area (rows 10-17)
n = 0

while queue and n < max_states:
    state, path = queue.popleft()
    n += 1
    lr, lc, rr, rc = state

    # Track states where right block reaches rows 10-17
    if rr <= 17:
        central_states.append((state, path))

    for name in ['U', 'D', 'X', 'C']:
        e2, o2 = replay(path)
        o3 = e2.step(AMAP[name])
        if o3.levels_completed > 2:
            print(f"\n*** WIN FOUND! path={path+name} ({len(path+name)} actions) ***")
            win_found = True
            break
        ns = get_state(o3)
        if ns and ns not in visited:
            visited.add(ns)
            queue.append((ns, path + name))
    if win_found:
        break

print(f"\nBFS: explored {n} states, {len(visited)} unique, queue={len(queue)}")

if central_states:
    right_rows = sorted(set(s[0][2] for s in central_states))
    right_cols = sorted(set(s[0][3] for s in central_states))
    print(f"Right block rows reached (≤17): {right_rows}")
    print(f"Right block cols when in rows ≤17: {right_cols}")

    # Can right block reach row=14 (top of central passage)?
    at14 = [(s, p) for s, p in central_states if s[2] == 14]
    if at14:
        print(f"\nRight block reached row=14 in {len(at14)} states:")
        for s, p in sorted(at14)[:5]:
            print(f"  L({s[0]},{s[1]}) R({s[2]},{s[3]}) path_len={len(p)}")
    else:
        print(f"\nRight block CANNOT reach row=14 — path may be blocked by Blue-1 at rows 11-12")
else:
    print("Right block never reached rows ≤17 — path completely blocked")

if not win_found:
    print("\nNo win found within BFS limit.")
    # Show reachable left-block positions in central passage
    left_central = [(lr,lc) for lr,lc,rr,rc in visited if 14<=lr<=17]
    right_central = [(rr,rc) for lr,lc,rr,rc in visited if 14<=rr<=17]
    print(f"Left block central-passage positions reached: {sorted(set(left_central))}")
    print(f"Right block central-passage positions reached: {sorted(set(right_central))}")
