"""m0r0 Level 1 — Step 4: test hypothesis that ACTION4 x2 wins (blocks converge to overlap)."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

def make_env():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    return arcade.make('m0r0')

def get_grid(obs):
    return np.array(obs.frame[-1])

def block_positions(grid):
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return "no lt-blue cells"
    rows = cells[:, 0]; cols = cells[:, 1]
    return f"{len(cells)} lt-blue cells, rows {rows.min()}-{rows.max()} cols {cols.min()}-{cols.max()}"

env = make_env()
obs = env.observation_space
print(f"Start: {block_positions(get_grid(obs))}  levels={obs.levels_completed}")

obs = env.step(GameAction.ACTION4)
print(f"After ACTION4 x1: {block_positions(get_grid(obs))}  levels={obs.levels_completed}")

obs = env.step(GameAction.ACTION4)
print(f"After ACTION4 x2: {block_positions(get_grid(obs))}  levels={obs.levels_completed}")

if obs.levels_completed >= 1:
    print("LEVEL 1 COMPLETE!")
else:
    print("Not yet — checking further...")
    obs = env.step(GameAction.ACTION4)
    print(f"After ACTION4 x3: {block_positions(get_grid(obs))}  levels={obs.levels_completed}")
