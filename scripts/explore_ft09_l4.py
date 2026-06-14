"""ft09 L4: extract the 3 keys precisely, then test candidate grey-cell rules in-game."""
import logging
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
L1 = [(38, 38), (38, 46), (54, 46), (38, 54)]
L2 = [(22, 16), (22, 24), (38, 24), (22, 32), (38, 32), (22, 48), (30, 48)]
L3 = [(22, 6), (30, 6), (38, 6), (22, 14), (14, 22), (30, 22), (14, 30),
      (46, 30), (30, 38), (46, 38), (22, 46), (22, 54), (30, 54), (38, 54)]
PRE = L1 + L2 + L3
ROWS = [14, 22, 30, 38, 46]
COLS = [12, 20, 28, 36, 44]
CLICKS_FOR = {9: 0, 8: 1, 12: 2}  # blue,red,orange in cycle blue->red->orange


def grid(f):
    return np.array(f.frame[-1])


def to_l4(env=None):
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make("ft09")
    r = env.observation_space
    for (x, y) in PRE:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    return env, r


def dom(block):
    v, c = np.unique(block, return_counts=True)
    return int(v[np.argmax(c)])


env, r = to_l4()
g = grid(r)

# detect present slots and keys
present = {}
keys = {}
for ri, rr in enumerate(ROWS):
    for ci, cc in enumerate(COLS):
        blk = g[rr:rr+6, cc:cc+6]
        if np.all(blk == 4):
            continue
        present[(ri, ci)] = True
        if (blk == 0).any():  # contains white -> key
            mini = [[dom(g[rr+2*i:rr+2*i+2, cc+2*j:cc+2*j+2]) for j in range(3)] for i in range(3)]
            keys[(ri, ci)] = {'center': mini[1][1], 'mini': mini}

print("present slots:", sorted(present))
for k, v in keys.items():
    print(f"key at {k}: center={v['center']} mini={v['mini']}")


def tile_center(ri, ci):
    return (COLS[ci]+3, ROWS[ri]+3)


def build_target(grey_target):
    """white->key center; grey->grey_target (None=skip). white-wins on overlap."""
    white_votes = {}
    grey_votes = {}
    for (kr, kc), kd in keys.items():
        for i in range(3):
            for j in range(3):
                if (i, j) == (1, 1):
                    continue
                sr, sc = kr-1+i, kc-1+j
                if (sr, sc) not in present:
                    continue
                if kd['mini'][i][j] == 0:        # white
                    white_votes.setdefault((sr, sc), set()).add(kd['center'])
                elif grey_target is not None:    # grey
                    grey_votes.setdefault((sr, sc), set()).add(grey_target)
    target = {}
    conflict = []
    for s in present:
        if s in keys:
            continue
        if s in white_votes:
            if len(white_votes[s]) > 1:
                conflict.append((s, 'white', white_votes[s]))
            target[s] = sorted(white_votes[s])[0]
        elif s in grey_votes:
            target[s] = sorted(grey_votes[s])[0]
        else:
            target[s] = 9  # base blue
    return target, conflict


for grey_target in (9, 8, None):
    target, conflict = build_target(grey_target)
    clicks = []
    for s, col in target.items():
        for _ in range(CLICKS_FOR[col]):
            clicks.append(tile_center(*s))
    env, r = to_l4()
    for (x, y) in clicks:
        r = env.step(GameAction.ACTION6, data={"x": x, "y": y})
    print(f"grey->{grey_target}: conflicts={len(conflict)} clicks={len(clicks)} "
          f"=> levels={r.levels_completed} {'<<< WIN' if r.levels_completed>=4 else ''}")
