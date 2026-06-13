"""Build the complete Action Table for a given ar25 level, both modes, unbiased (any-cell-change).

Usage: python scripts/action_table.py            # current target level = first unsolved
Reports for every action 1-7, in Mode-A (start) and Mode-B (after one ACTION5):
  cells changed, bbox of change, value transitions, available_actions change.
ACTION6 is tested against each distinct target object.
"""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 6: GameAction.ACTION6,
     7: GameAction.ACTION7}
PRIOR = {1: [2]*10 + [3]*5, 2: [3, 3, 5, 2, 2, 2, 2, 2, 2, 2, 2]}

# ACTION6 click targets for this level (x, y), one per distinct object + empty.
CLICK_TARGETS = {
    "black-piece": (13, 25), "yellow-struct": (36, 4), "divider": (30, 49),
    "divider-dot": (1, 49), "empty": (5, 18),
}


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for lvl in sorted(PRIOR):
        for a in PRIOR[lvl]:
            r = env.step(A[a], data={})
    return env, r


def change(before, after):
    d = before != after
    if not d.any():
        return 0, "", ""
    ys, xs = np.where(d)
    box = f"r{ys.min()}-{ys.max()} c{xs.min()}-{xs.max()}"
    trans = {}
    for y, x in zip(ys, xs):
        k = (int(before[y, x]), int(after[y, x]))
        trans[k] = trans.get(k, 0) + 1
    ts = " ".join(f"{a}->{b}:{n}" for (a, b), n in sorted(trans.items()))
    return int(d.sum()), box, ts


def run(pre, n, data):
    env, r = fresh()
    for p in pre:
        r = env.step(A[p], data={})
    b = grid(r); av = r.available_actions
    r2 = env.step(A[n], data=data)
    cells, box, ts = change(b, grid(r2))
    avc = "" if r2.available_actions == av else f" avail->{r2.available_actions}"
    return cells, box, ts, avc


print("ACTION TABLE — ar25 Level 3 (unbiased any-cell-change instrument)\n")
hdr = f"{'action':8} {'mode':6} {'cells':>5}  {'bbox':14} transitions"
print(hdr); print("-" * len(hdr) * 1)
for n in [1, 2, 3, 4, 5, 7]:
    for mode, pre in [("A", []), ("B", [5])]:
        cells, box, ts, avc = run(pre, n, {})
        print(f"ACTION{n:<2} {mode:6} {cells:>5}  {box:14} {ts}{avc}")

print("\nACTION6 (click) — per target, both modes:")
for name, (x, y) in CLICK_TARGETS.items():
    for mode, pre in [("A", []), ("B", [5])]:
        cells, box, ts, avc = run(pre, 6, {"x": x, "y": y})
        print(f"  click {name:13} mode-{mode}: {cells:>3} cells  {box:14} {ts}{avc}")
