"""Verify m0r0 Level 1 solution."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

ACTIONS = {
    'U': GameAction.ACTION1,
    'D': GameAction.ACTION2,
    'X': GameAction.ACTION3,
    'C': GameAction.ACTION4,
}

def get_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return "no blocks"
    rows, cols = cells[:, 0], cells[:, 1]
    return f"row={rows.min()} left_col={cols.min()} right_col={cols.max()-4}"

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space

SEQ = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
print(f"Start: {get_state(obs)}  levels={obs.levels_completed}")
for i, a in enumerate(SEQ):
    obs = env.step(ACTIONS[a])
    print(f"  {i+1:2d} {a}: {get_state(obs)}  levels={obs.levels_completed}")
    if obs.levels_completed > 0:
        print(f"\nLEVEL 1 COMPLETE at move {i+1}!")
        break
