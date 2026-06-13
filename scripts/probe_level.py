"""Replay known ar25 level solutions, then describe + probe the current level.

Usage: python scripts/probe_level.py            # advance through all known solutions, probe next level
"""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6,
     7: GameAction.ACTION7}

# Known per-level solutions (action-number lists)
LEVEL_SOLUTIONS = {
    1: [2]*10 + [3]*5,                          # 10 DOWN, 5 RIGHT
    2: [3, 3, 5, 2, 2, 2, 2, 2, 2, 2, 2],       # 2xLEFT(H), toggle, 8xDOWN(V)
}

_SYM = "·₁₂₃₄■PpRBbYOmGV"
COLOURS = {0:"white",1:"lt-grey",2:"md-grey",3:"dk-grey",4:"vdk-grey",5:"black",
           6:"pink",7:"lt-pink",8:"red",9:"blue",10:"lt-blue",11:"yellow",
           12:"orange",13:"maroon",14:"green",15:"purple"}


def grid(f):
    return np.array(f.frame[-1])


def bbox(g, val):
    ys, xs = np.where(g == val)
    if len(ys) == 0:
        return None
    return (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()), int(len(ys)))


def print_grid(g, label=""):
    print(f"\n--- {label} [{g.shape[0]}x{g.shape[1]}] ---")
    for r in range(g.shape[0]):
        print(f"{r:3d} " + "".join(_SYM[v] if 0 <= v < 16 else "?" for v in g[r]))
    vals = sorted(set(int(v) for v in g.flatten()))
    print("values: " + ", ".join(f"{v}={COLOURS[v]} bbox={bbox(g,v)}" for v in vals))


def changes(before, after):
    d = before != after
    if not d.any():
        return "no change"
    ys, xs = np.where(d)
    moved = []
    for val in sorted(set(int(v) for v in before.flatten()) | set(int(v) for v in after.flatten())):
        b, a = bbox(before, val), bbox(after, val)
        if b and a and (b[0] != a[0] or b[1] != a[1]):
            moved.append(f"{COLOURS[val]}({val}) dy={a[0]-b[0]:+d} dx={a[1]-b[1]:+d}")
    return f"rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} ({d.sum()} cells); " + ("; ".join(moved) if moved else "no bbox shift")


def main():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    res = env.observation_space

    # replay known solutions
    for lvl in sorted(LEVEL_SOLUTIONS):
        for a in LEVEL_SOLUTIONS[lvl]:
            res = env.step(A[a], data={})
    cur = res.levels_completed + 1
    print(f"=== Now at LEVEL {cur} (levels_completed={res.levels_completed}/{res.win_levels}) ===")
    print(f"available_actions={res.available_actions}")
    g0 = grid(res)
    print_grid(g0, f"Level {cur} initial scene")

    # probe each action (one at a time, restoring by re-replaying)
    print("\n=== Probing actions at level start ===")
    for n in [1, 2, 3, 4, 5, 7]:
        env2 = arcade.make("ar25")
        r = env2.observation_space
        for lvl in sorted(LEVEL_SOLUTIONS):
            for a in LEVEL_SOLUTIONS[lvl]:
                r = env2.step(A[a], data={})
        before = grid(r)
        avail_before = r.available_actions
        r2 = env2.step(A[n], data={})
        after = grid(r2)
        tog = "  <-- AVAILABLE_ACTIONS CHANGED" if r2.available_actions != avail_before else ""
        print(f"ACTION{n}: {changes(before, after)}{tog}")


if __name__ == "__main__":
    main()
