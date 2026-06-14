"""ar25 L3: per-state action table with FULL black bbox + connected components.

Borders excluded (row 63, col 63). Tracks each black component's top-left so
moves of one cluster aren't masked by the other.
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


def grid(f):
    return np.array(f.frame[-1])


def fresh(n_state):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2:
        r = env.step(A[a], data={})
    for _ in range(n_state):
        r = env.step(A[5], data={})
    return env, r


def interior(g, v):
    m = (g == v)
    m[63, :] = False
    m[:, 63] = False
    return m


def black_full_bbox(g):
    m = interior(g, 5)
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max()), int(len(ys)))


def label(mask):
    """4-connected flood-fill labelling; returns list of lists of (y,x)."""
    seen = np.zeros_like(mask, dtype=bool)
    comps = []
    H, W = mask.shape
    for sy in range(H):
        for sx in range(W):
            if mask[sy, sx] and not seen[sy, sx]:
                stack = [(sy, sx)]
                seen[sy, sx] = True
                cells = []
                while stack:
                    y, x = stack.pop()
                    cells.append((y, x))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
                comps.append(cells)
    return comps


def black_components(g):
    """Return list of (top-left y, top-left x, size) for each black blob, sorted."""
    m = interior(g, 5)
    out = []
    for cells in label(m):
        ys = [c[0] for c in cells]
        xs = [c[1] for c in cells]
        out.append((min(ys), min(xs), len(cells)))
    return sorted(out)


def ltblue_rows(g):
    m = interior(g, 10)
    ys, _ = np.where(m)
    return (int(ys.min()), int(ys.max())) if len(ys) else None


for s in range(3):
    print("=" * 74)
    print(f"CONTROL STATE {s}")
    print("=" * 74)
    env, r = fresh(s)
    g0 = grid(r)
    print(f"  baseline: black_bbox={black_full_bbox(g0)}  ltblue_rows={ltblue_rows(g0)}")
    print(f"            black_components(tl)={black_components(g0)}")
    for a in [1, 2, 3, 4, 7]:
        env, r = fresh(s)
        g0 = grid(r)
        c0 = black_components(g0)
        r = env.step(A[a], data={})
        g1 = grid(r)
        c1 = black_components(g1)
        n = int((g0 != g1).sum())
        bb0, bb1 = black_full_bbox(g0), black_full_bbox(g1)
        lb0, lb1 = ltblue_rows(g0), ltblue_rows(g1)
        moves = []
        if bb0 != bb1:
            moves.append(f"black_bbox {bb0}->{bb1}")
        if c0 != c1:
            moves.append(f"comps {c0}->{c1}")
        if lb0 != lb1:
            moves.append(f"ltblue_rows {lb0}->{lb1}")
        info = "  ".join(moves) if moves else "(no black/ltblue change)"
        print(f"  ACTION{a}: cells={n:4d}  {info}")
    print()
