"""Probe each action of ar25 independently from a fresh RESET and report changes."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

ACTIONS = {
    1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
    4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6,
    7: GameAction.ACTION7,
}


def grid(frame):
    return np.array(frame.frame[-1])


def bbox(g, val):
    ys, xs = np.where(g == val)
    if len(ys) == 0:
        return None
    return (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()), len(ys))


def shift_report(before, after):
    out = []
    for val, name in [(4, "vdk-grey(4)"), (5, "black(5)"), (0, "white-dots(0)")]:
        b, a = bbox(before, val), bbox(after, val)
        if b and a:
            dy, dx = a[0] - b[0], a[1] - b[1]
            out.append(f"    {name}: top-left {b[0],b[1]} -> {a[0],a[1]}  (dy={dy:+d}, dx={dx:+d}), n {b[4]}->{a[4]}")
    return "\n".join(out)


def describe_changes(before, after):
    diff = before != after
    if not diff.any():
        return "  no change"
    ys, xs = np.where(diff)
    box = f"rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()} ({diff.sum()} cells)"
    # value transitions
    trans = {}
    for y, x in zip(ys, xs):
        k = (int(before[y, x]), int(after[y, x]))
        trans[k] = trans.get(k, 0) + 1
    tstr = ", ".join(f"{a}->{b}:{n}" for (a, b), n in sorted(trans.items()))
    return f"  changed {box}\n    transitions: {tstr}"


def main():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    init = grid(env.observation_space)
    init_actions = env.observation_space.available_actions

    for n, act in ACTIONS.items():
        env.step(GameAction.RESET, data={})
        before = grid(env.observation_space)
        if act == GameAction.ACTION6:
            # coordinate action — probe a center click as a sample
            res = env.step(act, data={"x": 32, "y": 32})
            label = "ACTION6 (click x=32,y=32)"
        else:
            res = env.step(act, data={})
            label = act.name
        after = grid(res)
        avail_changed = res.available_actions != init_actions
        print(f"\n=== {label} ===")
        print(f"  available_actions: {res.available_actions}"
              f"{'  <-- CHANGED' if avail_changed else ''}")
        print(f"  levels_completed: {res.levels_completed}/{res.win_levels}")
        print(describe_changes(before, after))
        print(shift_report(before, after))


if __name__ == "__main__":
    main()
