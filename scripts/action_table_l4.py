"""ar25 L4 action table: detect ACTION5 cycle length, then probe all actions per state."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3,
     4: GameAction.ACTION4, 5: GameAction.ACTION5, 7: GameAction.ACTION7}
L1 = [2]*10 + [3]*5
L2 = [3, 3, 5] + [2]*8
L3 = [5] + [4]*7 + [2]*7 + [5] + [3]*12 + [2]*5 + [5] + [1]*7


def grid(f):
    return np.array(f.frame[-1])


def fresh(n_state=0):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2 + L3:
        r = env.step(A[a], data={})
    for _ in range(n_state):
        r = env.step(A[5], data={})
    return env, r


def interior(g, v):
    m = (g == v)
    m[63, :] = False; m[:, 63] = False
    return m


def comps(g, v):
    m = interior(g, v)
    seen = np.zeros_like(m, dtype=bool); out = []
    H, W = m.shape
    for sy in range(H):
        for sx in range(W):
            if m[sy, sx] and not seen[sy, sx]:
                stack = [(sy, sx)]; seen[sy, sx] = True; cells = []
                while stack:
                    y, x = stack.pop(); cells.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx] = True; stack.append((ny,nx))
                ys=[c[0] for c in cells]; xs=[c[1] for c in cells]
                out.append((min(ys), min(xs), len(cells)))
    return sorted(out)


def band_rows(g):
    ys, _ = np.where(interior(g, 10))
    return (int(ys.min()), int(ys.max())) if len(ys) else None


# --- cycle detection ---
print("CYCLE DETECTION (press ACTION5 repeatedly):")
env, r = fresh()
g_start = grid(r)
prev = g_start
for k in range(1, 8):
    r = env.step(A[5], data={})
    g = grid(r)
    n = int((prev != g).sum())
    back = "  <== identical to START" if np.array_equal(g, g_start) else ""
    print(f"  press#{k}: changed_from_prev={n}{back}")
    prev = g
print()

# Strip the right-border counter when diffing
def changed_ignoring_counter(g0, g1):
    d = (g0 != g1)
    d[:, 63] = False
    return int(d.sum())


N_STATES = 3  # adjust after seeing cycle; probe a few
for s in range(N_STATES):
    print("=" * 70)
    print(f"STATE {s}")
    env, r = fresh(s)
    g0 = grid(r)
    print(f"  baseline black comps={comps(g0,5)}  band={band_rows(g0)}")
    for a in [1, 2, 3, 4, 7]:
        env, r = fresh(s)
        g0 = grid(r)
        bc0 = comps(g0, 5); br0 = band_rows(g0)
        r = env.step(A[a], data={})
        g1 = grid(r)
        bc1 = comps(g1, 5); br1 = band_rows(g1)
        n = changed_ignoring_counter(g0, g1)
        msg = []
        if bc0 != bc1:
            msg.append(f"black {bc0}->{bc1}")
        if br0 != br1:
            msg.append(f"band {br0}->{br1}")
        print(f"  ACTION{a}: cells={n:4d}  {'  '.join(msg) if msg else '(no black/band change)'}")
    print()
