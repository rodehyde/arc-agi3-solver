"""ft09 auto-solver. Parse the four 3x3 tile-grids, find the framed (active) one and the
worked examples, induce the key->tile rule, verify on examples, apply to the framed grid.
Chain through levels; STOP (don't grind) if the rule doesn't verify or a level isn't solved."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)


def grid(f):
    return np.array(f.frame[-1])


def find_tile_origins(g):
    """6x6 uniform blocks of red(8)/blue(9): return list of (r,c,color) top-left corners."""
    out = []
    for r in range(0, 58):
        for c in range(0, 58):
            v = g[r, c]
            if v not in (8, 9):
                continue
            block = g[r:r+6, c:c+6]
            if np.all(block == v):
                # top-left corner: cell above and left not same-color tile
                if (r == 0 or g[r-1, c] != v) and (c == 0 or g[r, c-1] != v):
                    out.append((r, c, int(v)))
    return out


def group_grids(origins):
    """Cluster tile origins into grids (3x3). Returns list of dicts with tile map."""
    pts = [(r, c) for (r, c, v) in origins]
    used = [False]*len(origins)
    grids = []
    for i in range(len(origins)):
        if used[i]:
            continue
        # collect all origins within 24 rows/cols of this one
        cluster = [j for j in range(len(origins))
                   if abs(origins[j][0]-origins[i][0]) <= 24 and abs(origins[j][1]-origins[i][1]) <= 24]
        for j in cluster:
            used[j] = True
        rs = sorted({origins[j][0] for j in cluster})
        cs = sorted({origins[j][1] for j in cluster})
        grids.append({'rows': rs, 'cols': cs, 'tiles': {(origins[j][0], origins[j][1]): origins[j][2] for j in cluster}})
    return grids


def grid_geometry(gd):
    """Infer the 3x3 cell origins (rows r0,r1,r2 ; cols c0,c1,c2) from observed tiles."""
    rs = sorted(set(gd['rows'])); cs = sorted(set(gd['cols']))
    # pitch 8; reconstruct full 3 rows/cols from min
    r0 = min(rs); c0 = min(cs)
    rows = [r0, r0+8, r0+16]
    cols = [c0, c0+8, c0+16]
    return rows, cols


def read_key(g, rr, cc):
    """Center key tile at (rr,cc): 6x6, decode 3x3 of 2x2 blocks. white(0)=red-target, grey(2)=blue."""
    key = []
    for br in range(3):
        row = []
        for bc in range(3):
            blk = g[rr+br*2:rr+br*2+2, cc+bc*2:cc+bc*2+2]
            vals, cnts = np.unique(blk, return_counts=True)
            dom = vals[np.argmax(cnts)]
            row.append(int(dom))
        key.append(row)
    return key  # 3x3 of dominant colors (0 white,2 grey,8 red center)


def analyse(g):
    origins = find_tile_origins(g)
    grids = group_grids(origins)
    parsed = []
    for gd in grids:
        rows, cols = grid_geometry(gd)
        tiles = {}
        for i in range(3):
            for j in range(3):
                tiles[(i, j)] = gd['tiles'].get((rows[i], cols[j]), None)  # None = center key
        # framed if vdk-grey(4) borders the grid bbox
        r0, c0 = rows[0], cols[0]
        bb = g[max(0, r0-3):rows[2]+9, max(0, c0-3):cols[2]+9]
        framed = (bb == 4).sum() > 20
        # center key tile origin
        kr, kc = rows[1], cols[1]
        key = read_key(g, kr, kc)
        parsed.append({'rows': rows, 'cols': cols, 'tiles': tiles, 'framed': framed, 'key': key})
    return parsed


def tile_center(rows, cols, i, j):
    return (cols[j]+3, rows[i]+3)  # (x,y)


def solve_level(env, r, verbose=True):
    g = grid(r)
    parsed = analyse(g)
    framed = [p for p in parsed if p['framed']]
    examples = [p for p in parsed if not p['framed']]
    if len(framed) != 1:
        return None, f"expected 1 framed grid, found {len(framed)} (parsed {len(parsed)} grids)"
    F = framed[0]
    # verify rule white->red(8), grey->blue(9) on examples
    for ex in examples:
        for i in range(3):
            for j in range(3):
                if (i, j) == (1, 1):
                    continue
                want = 8 if ex['key'][i][j] == 0 else 9
                have = ex['tiles'][(i, j)]
                if have != want:
                    return None, f"rule mismatch in example at {(i,j)}: key={ex['key'][i][j]} want{want} have{have}"
    # apply to framed: click tiles whose current color != target
    clicks = []
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                continue
            want = 8 if F['key'][i][j] == 0 else 9
            have = F['tiles'][(i, j)]
            if have != want:
                clicks.append(tile_center(F['rows'], F['cols'], i, j))
    if verbose:
        print(f"  framed grid rows={F['rows']} cols={F['cols']} key={F['key']}")
        print(f"  examples verified={len(examples)}  clicks needed={len(clicks)}: {clicks}")
    lvl0 = r.levels_completed
    for (x, y) in clicks:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return r, clicks


# ---- chain through levels ----
arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make("ft09")
r = env.observation_space
print(f"win_levels={r.win_levels}")
solutions = {}
while r.levels_completed < r.win_levels and r.state.name != 'FINISHED':
    lvl = r.levels_completed + 1
    print(f"\n=== LEVEL {lvl} ===")
    before = r.levels_completed
    r, info = solve_level(env, r)
    if r is None:
        print(f"  BLOCKED: {info}")
        break
    if r.levels_completed > before:
        solutions[lvl] = info
        print(f"  >>> LEVEL {lvl} COMPLETE in {len(info)} clicks  (now {r.levels_completed}/{r.win_levels})")
    else:
        print(f"  NOT SOLVED (levels still {r.levels_completed}); stopping to avoid grinding.")
        break
print(f"\nFinal: {r.levels_completed}/{r.win_levels}  state={r.state.name}")
print("solutions:", {k: len(v) for k, v in solutions.items()})
