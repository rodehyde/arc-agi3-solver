"""ar25 L3 action table — any-cell-change instrument, with multi-state cycle detection.

For each action we report: cells changed, value transitions, bbox of change,
black-piece top-left displacement, and whether available_actions changed.
We then drive the state-changer through its full cycle, re-probing every action
in each state.
"""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 7: GameAction.ACTION7}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8

COLOR = {0: 'white', 5: 'black', 9: 'blue', 10: 'lt-blue', 11: 'yellow'}


def grid(f):
    return np.array(f.frame[-1])


def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2:
        r = env.step(A[a], data={})
    return env, r


def black_tl(g):
    ys, xs = np.where(g == 5)
    # ignore the bottom border row 63 and right border col 63
    mask = (ys < 63) & (xs < 63)
    ys, xs = ys[mask], xs[mask]
    if len(ys) == 0:
        return None
    return (ys.min(), xs.min())


def diff(g0, g1):
    changed = np.argwhere(g0 != g1)
    n = len(changed)
    trans = {}
    for (y, x) in changed:
        k = f"{g0[y,x]}->{g1[y,x]}"
        trans[k] = trans.get(k, 0) + 1
    bbox = None
    if n:
        ys, xs = changed[:, 0], changed[:, 1]
        bbox = (int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max()))
    return n, trans, bbox


def probe_simple(action_num, label):
    """Apply one simple action from a fresh L3 state; report the diff."""
    env, r = fresh()
    g0 = grid(r)
    av0 = list(r.available_actions)
    tl0 = black_tl(g0)
    r = env.step(A[action_num], data={})
    g1 = grid(r)
    av1 = list(r.available_actions)
    tl1 = black_tl(g1)
    n, trans, bbox = diff(g0, g1)
    dav = "SAME" if av0 == av1 else f"{av0} -> {av1}"
    disp = None
    if tl0 and tl1:
        disp = (tl1[0]-tl0[0], tl1[1]-tl0[1])
    print(f"  ACTION{action_num} [{label}]: cells={n:4d}  bbox={bbox}  "
          f"black_tl {tl0}->{tl1} disp={disp}")
    print(f"            transitions={trans}  avail={dav}")
    return n, disp, av1


print("=" * 70)
print("PASS 1 — probe each simple action once from L3 start (default state)")
print("=" * 70)
for a, lbl in [(1, 'up?'), (2, 'down?'), (3, 'left?'), (4, 'right?'),
               (5, 'state?'), (7, 'aux?')]:
    probe_simple(a, lbl)

print()
print("=" * 70)
print("CYCLE DETECTION — press ACTION5 repeatedly, watch state return to start")
print("=" * 70)
env, r = fresh()
g_start = grid(r)
av_start = list(r.available_actions)
print(f"start avail={av_start}")
prev = g_start
for k in range(1, 7):
    r = env.step(A[5], data={})
    g = grid(r)
    n, trans, bbox = diff(prev, g)
    back = "  <== BACK TO START" if np.array_equal(g, g_start) else ""
    print(f"  press #{k}: cells_changed_from_prev={n:4d} trans={trans} "
          f"avail={list(r.available_actions)}{back}")
    prev = g
