"""L3 win test: BFS with full path tracking to find win and diagnose target states.
Hypothesis: both blocks converge simultaneously to col=30 in central passage."""
import numpy as np
from collections import deque
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

def setup_game():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    # Blue-1: RIGHT, UP, RIGHT×4, DOWN×3, LEFT×2, UP×1 → rows 19-20 cols 43-44
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3,
                GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-2: UP, RIGHT, UP → rows 11-12 cols 15-16
    g = np.array(obs.frame[-1])
    bxy2 = next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-3: RIGHT×3 → rows 31-32 cols 51-52
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    return env, obs

def get_state(obs):
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    if not len(cells): return None
    left = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:,0].min()), int(left[:,1].min()),
            int(right[:,0].min()), int(right[:,1].min()))

def replay(path):
    e, o = setup_game()
    for a in path:
        o = e.step(AMAP[a])
    return e, o

print("Setting up game (markers moved)...")
_, obs_start = setup_game()
init = get_state(obs_start)
print(f"Start: L({init[0]},{init[1]}) R({init[2]},{init[3]})")

# BFS with full path tracking (state → shortest path)
queue = deque([(init, "")])
visited = {init: ""}
win_found = False
win_path = None
n = 0

# Target states from theoretical analysis
TARGETS = {
    (14, 26, 14, 34),  # ideal: both in passage, left=26 right=34 → CONVERGE → WIN
    (14, 30, 10, 34),  # intermediate: left in passage col=30, right above at col=34
    (14, 30, 14, 34),  # both in passage, left=30 right=34
    (18, 26, 14, 34),  # left below passage, right in passage col=34
    (18, 30, 14, 30),  # left below col=30, right in passage col=30
    (14, 30, 14, 30),  # full overlap state (col=30 both)
}

while queue:
    state, path = queue.popleft()
    n += 1

    for name in ['U', 'D', 'X', 'C']:
        e2, o2 = replay(path)
        o3 = e2.step(AMAP[name])
        if o3.levels_completed > 2:
            win_path = path + name
            win_found = True
            break
        ns = get_state(o3)
        if ns and ns not in visited:
            visited[ns] = path + name
            queue.append((ns, path + name))

    if win_found:
        break
    if n % 100 == 0:
        print(f"  {n} states explored, {len(visited)} unique...")

print(f"\nBFS complete: {n} states, {len(visited)} unique")

if win_found:
    print(f"\n*** WIN! path='{win_path}' ({len(win_path)} actions) ***")
else:
    print("\nNo win found. Diagnosing target states:")
    for ts in sorted(TARGETS):
        if ts in visited:
            print(f"  REACHABLE {ts}: path='{visited[ts]}'")
        else:
            print(f"  UNREACHABLE {ts}")

    # All states where right block is at col=34 in central passage (rows 14-17)
    r34 = sorted((s, p) for s, p in visited.items() if s[2] == 14 and s[3] == 34)
    print(f"\nAll states with R(14,34) [right at col=34 rows 14-17]: {len(r34)}")
    for s, p in r34:
        print(f"  L({s[0]},{s[1]}) R(14,34)  path='{p}'")

    # States where BOTH blocks are in central passage rows 14-17
    both = sorted((s, p) for s, p in visited.items()
                  if 14 <= s[0] <= 17 and 14 <= s[2] <= 17)
    print(f"\nStates with BOTH in rows 14-17: {len(both)}")
    for s, p in both:
        print(f"  L({s[0]},{s[1]}) R({s[2]},{s[3]})  path='{p}'")

    # Right block's maximum leftward penetration into central passage
    right_in_passage = [(s[3], s, p) for s, p in visited.items() if 14 <= s[2] <= 17]
    if right_in_passage:
        best = min(right_in_passage, key=lambda x: x[0])
        print(f"\nRight block closest to col=30 in central passage: col={best[0]}")
        print(f"  State: L({best[1][0]},{best[1][1]}) R({best[1][2]},{best[1][3]})")
        print(f"  Path: '{best[2]}'")
