"""tn36 L5 — what does each button do? Track left piece through every frame."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]

def make_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    for r, c in L1 + L2 + L3 + L4:
        obs = env.step(GameAction.ACTION6, {'x': c, 'y': r})
    assert obs.levels_completed == 4
    return env, obs

def click(env, row, col):
    return env.step(GameAction.ACTION6, {'x': col, 'y': row})

def piece_state(frame, panel='left'):
    g = np.array(frame)
    if panel == 'left':
        cells = [(int(r),int(c)) for r,c in np.argwhere(g==4) if c<=31 and 3<=r<=31]
        # also black=5 cells that are the piece (track is also black, so use vdkgrey=4)
    else:
        cells = [(int(r),int(c)) for r,c in np.argwhere(g==11) if c>=32 and 3<=r<=31]
    if not cells:
        return "none"
    rs = sorted(set(r for r,c in cells))
    cs = sorted(set(c for r,c in cells))
    return f"r{rs[0]}-{rs[-1]} c{cs[0]}-{cs[-1]} n={len(cells)}"

def test_button(label, row, col):
    env, obs = make_l5()
    before = piece_state(obs.frame[-1], 'left')
    result = click(env, row, col)
    print(f"\n{'='*55}")
    print(f"Button: {label}  ({len(result.frame)} frames)")
    print(f"  Before: {before}")
    for i, frame in enumerate(result.frame):
        state = piece_state(frame, 'left')
        marker = " <-- CHANGED" if state != before else ""
        print(f"  f{i}: {state}{marker}")
    # Also show right piece trajectory
    rp_states = [piece_state(f, 'right') for f in result.frame]
    if any(s != rp_states[0] for s in rp_states):
        print(f"  Right piece: {' | '.join(rp_states)}")

# The five buttons
test_button("blue box    (58, 5)", 58, 5)
test_button("zone 1      (58,15)", 58, 15)
test_button("zone 2      (58,25)", 58, 25)
test_button("zone 3      (58,35)", 58, 35)
test_button("zone 4      (58,45)", 58, 45)

# Change direction: single legend bar click (H33 at group 1)
print(f"\n{'='*55}")
print("Single legend bar: click H33 at RC[0] (col 34)")
env, obs = make_l5()
g0 = np.array(obs.frame[-1])
result = click(env, 33, 34)
g1 = np.array(result.frame[-1])
changed = np.argwhere(g0 != g1)
print(f"  frames={len(result.frame)}  cells changed={len(changed)}")
for r,c in changed:
    print(f"    ({r},{c}): {int(g0[r,c])} -> {int(g1[r,c])}")
