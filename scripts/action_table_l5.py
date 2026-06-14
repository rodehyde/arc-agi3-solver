"""ar25 L5 action table: detect ACTION5 cycle length, probe all actions per state.
Tracks black components, horizontal band (rows of lt-blue spanning width) and
vertical band (cols of lt-blue spanning height)."""
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
L4 = [5] + [4]*7 + [5] + [1]*7 + [4]*7 + [5] + [2]*6


def grid(f):
    return np.array(f.frame[-1])


def fresh(s=0):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ar25")
    r = env.observation_space
    for a in L1 + L2 + L3 + L4:
        r = env.step(A[a], data={})
    for _ in range(s):
        r = env.step(A[5], data={})
    return env, r


def interior(g, v):
    m = (g == v); m[63, :] = False; m[:, 63] = False
    return m


def comps(g, v=5):
    m = interior(g, v); seen = np.zeros_like(m, dtype=bool); out = []
    H, W = m.shape
    for sy in range(H):
        for sx in range(W):
            if m[sy, sx] and not seen[sy, sx]:
                st = [(sy, sx)]; seen[sy, sx] = True; cs = []
                while st:
                    y, x = st.pop(); cs.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx]=True; st.append((ny,nx))
                ys=[c[0] for c in cs]; xs=[c[1] for c in cs]
                out.append((min(ys),min(xs),len(cs)))
    return sorted(out)


def hband(g):
    """rows where lt-blue spans most of the width."""
    m = interior(g, 10)
    rows = [y for y in range(64) if m[y, :].sum() > 30]
    return (min(rows), max(rows)) if rows else None


def vband(g):
    m = interior(g, 10)
    cols = [x for x in range(64) if m[:, x].sum() > 30]
    return (min(cols), max(cols)) if cols else None


print("CYCLE DETECTION:")
env, r = fresh(); g_start = grid(r); prev = g_start
for k in range(1, 9):
    r = env.step(A[5], data={}); g = grid(r)
    n = int((prev != g).sum())
    print(f"  press#{k}: changed_from_prev={n}{'  <==START' if np.array_equal(g,g_start) else ''}")
    prev = g
print()


def cic(g0, g1):
    d = (g0 != g1); d[:, 63] = False
    return int(d.sum())


for s in range(4):
    print("=" * 70)
    print(f"STATE {s}")
    env, r = fresh(s); g0 = grid(r)
    print(f"  baseline black={comps(g0)} hband={hband(g0)} vband={vband(g0)}")
    for a in [1, 2, 3, 4, 7]:
        env, r = fresh(s); g0 = grid(r)
        c0, h0, v0 = comps(g0), hband(g0), vband(g0)
        r = env.step(A[a], data={}); g1 = grid(r)
        c1, h1, v1 = comps(g1), hband(g1), vband(g1)
        msg = []
        if c0 != c1: msg.append(f"black {c0}->{c1}")
        if h0 != h1: msg.append(f"hband {h0}->{h1}")
        if v0 != v1: msg.append(f"vband {v0}->{v1}")
        print(f"  ACTION{a}: cells={cic(g0,g1):4d}  {'  '.join(msg) if msg else '(no tracked change)'}")
    print()
