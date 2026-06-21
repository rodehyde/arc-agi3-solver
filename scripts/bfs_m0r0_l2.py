"""m0r0 Level 2 — BFS over real game states to find winning sequence.

State = (row, left_col, right_col). Replay from scratch per expansion.
Red cell traps naturally dead-end (teleport returns to visited start state).
"""
from collections import deque
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}

def make_l2():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1:
        obs = env.step(AMAP[a])
    return env, obs

def get_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return None
    rows, cols = cells[:, 0], cells[:, 1]
    return (int(rows.min()), int(cols.min()), int(cols.max()) - 3)

def replay_to(path):
    env, obs = make_l2()
    for a in path:
        obs = env.step(AMAP[a])
    return env, obs

env0, obs0 = make_l2()
initial_state = get_state(obs0)
print(f"Initial state: row={initial_state[0]} left_col={initial_state[1]} right_col={initial_state[2]}")
print(f"Searching (baseline=111 actions)...\n")

queue = deque([(initial_state, [])])
visited = {initial_state}
found = None
n = 0

while queue and not found:
    state, path = queue.popleft()
    n += 1

    if n % 50 == 0:
        print(f"  {n} states explored, queue={len(queue)}, depth={len(path)}")

    for name in ['U', 'D', 'X', 'C']:
        env, obs = replay_to(path)
        obs = env.step(AMAP[name])

        if obs.levels_completed > 1:
            found = path + [name]
            break

        new_state = get_state(obs)
        if new_state and new_state not in visited:
            visited.add(new_state)
            queue.append((new_state, path + [name]))

if found:
    print(f"\nSOLUTION: {''.join(found)}  ({len(found)} moves)")
    print(f"States explored: {n}  |  Total reachable states: {len(visited)}")
else:
    print(f"\nNo solution found after {n} states.")
    print(f"Reachable states ({len(visited)}):")
    for s in sorted(visited):
        print(f"  row={s[0]} left_col={s[1]} right_col={s[2]}")
