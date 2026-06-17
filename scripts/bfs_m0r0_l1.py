"""m0r0 Level 1 — BFS over real game states to find winning sequence.

State = (row, left_col, right_col) — both blocks always share the same row.
We replay the action sequence from scratch for each expansion (small state space).
"""
from collections import deque
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

ACTIONS = {
    'U': GameAction.ACTION1,  # both up
    'D': GameAction.ACTION2,  # both down
    'X': GameAction.ACTION3,  # diverge (left←, right→)
    'C': GameAction.ACTION4,  # converge (left→, right←)
}

def make_env():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    return arcade.make('m0r0')

def get_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return None
    rows, cols = cells[:, 0], cells[:, 1]
    return (int(rows.min()), int(cols.min()), int(cols.max()) - 4)

def replay_to(path):
    env = make_env()
    obs = env.observation_space
    for a in path:
        obs = env.step(ACTIONS[a])
    return env, obs

# --- BFS ---
initial_env = make_env()
initial_obs = initial_env.observation_space
initial_state = get_state(initial_obs)
print(f"Initial state: row={initial_state[0]} left_col={initial_state[1]} right_col={initial_state[2]}")
print(f"Searching...\n")

queue = deque([(initial_state, [])])
visited = {initial_state}
found = None
n = 0

while queue and not found:
    state, path = queue.popleft()
    n += 1

    for name in ['U', 'D', 'X', 'C']:
        env, obs = replay_to(path)
        obs = env.step(ACTIONS[name])

        if obs.levels_completed > 0:
            found = path + [name]
            break

        new_state = get_state(obs)
        if new_state and new_state not in visited:
            visited.add(new_state)
            queue.append((new_state, path + [name]))

if found:
    print(f"SOLUTION: {''.join(found)}  ({len(found)} moves)")
    print(f"States explored: {n}")
else:
    print(f"No solution found after exploring {n} states.")
    print(f"All reachable states ({len(visited)}):")
    for s in sorted(visited):
        print(f"  row={s[0]} left_col={s[1]} right_col={s[2]}")
