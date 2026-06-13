"""Step 4 test: ar25 level 1 hypothesis = 10x DOWN + 5x RIGHT aligns vdk-grey L onto yellow target."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5}


def grid(f):
    return np.array(f.frame[-1])


def bbox(g, val):
    ys, xs = np.where(g == val)
    if len(ys) == 0:
        return None
    return (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()), len(ys))


def main():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    obs = env.observation_space
    g0 = grid(obs)
    print(f"start: vdk-grey(4) bbox={bbox(g0,4)}  yellow(11) bbox={bbox(g0,11)}")
    print(f"       levels={obs.levels_completed}/{obs.win_levels}\n")

    seq = [2]*10 + [3]*5  # 10 DOWN, 5 RIGHT
    res = obs
    for i, a in enumerate(seq, 1):
        res = env.step(A[a], data={})
        if res.levels_completed > 0:
            print(f"  >>> LEVEL COMPLETED after {i} actions ({A[a].name})")
            break

    g = grid(res)
    print(f"end:   vdk-grey(4) bbox={bbox(g,4)}  yellow(11) bbox={bbox(g,11)}")
    print(f"       levels={res.levels_completed}/{res.win_levels}  state={res.state.name}")
    print(f"       available_actions={res.available_actions}")


if __name__ == "__main__":
    main()
