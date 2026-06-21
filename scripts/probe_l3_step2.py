"""Step 2 probe for m0r0 Level 3.
Tests every action in normal state and frozen state.
Reports: cells changed, value transitions, bounding box.
ACTION6 tested on every distinct target type.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs

def diff(g1, g2):
    g1, g2 = np.array(g1), np.array(g2)
    changed = np.argwhere(g1 != g2)
    if not len(changed):
        return 0, None, {}
    r0,c0 = changed[:,0].min(), changed[:,1].min()
    r1,c1 = changed[:,0].max(), changed[:,1].max()
    transitions = {}
    for r,c in changed:
        k = (int(g1[r,c]), int(g2[r,c]))
        transitions[k] = transitions.get(k, 0) + 1
    return len(changed), (r0,c0,r1,c1), transitions

def probe_action(env_fn, action, label, x=None, y=None):
    env, obs = env_fn()
    g1 = obs.frame[-1]
    aa1 = list(obs.available_actions)
    lc1 = obs.levels_completed
    if x is not None:
        obs2 = env.step(action, {"x": x, "y": y})
    else:
        obs2 = env.step(action)
    g2 = obs2.frame[-1]
    aa2 = list(obs2.available_actions)
    n, bbox, trans = diff(g1, g2)
    print(f"  {label}:")
    if n == 0:
        print(f"    NO EFFECT (0 cells changed)")
    else:
        print(f"    {n} cells changed, bbox=rows {bbox[0]}-{bbox[2]} cols {bbox[1]}-{bbox[3]}")
        for (v1,v2),cnt in sorted(trans.items()):
            names = {0:'white',1:'lt-grey',5:'black',8:'red',9:'blue',10:'lt-blue',11:'yellow',15:'purple'}
            print(f"    {names.get(v1,v1)}->{names.get(v2,v2)}: {cnt}")
    if aa2 != aa1:
        print(f"    *** available_actions changed: {aa1} -> {aa2} ***")
    if obs2.levels_completed > lc1:
        print(f"    *** LEVEL COMPLETED ***")
    return n, trans

# ── NORMAL STATE PROBE ─────────────────────────────────────────────────────
print("="*70)
print("NORMAL STATE — Actions 1-7 from starting position")
print("="*70)
env0, obs0 = make_l3()
g0 = obs0.frame[-1]
print(f"Starting: available_actions={list(obs0.available_actions)}")
print(f"Left block: rows 46-49 cols 22-25  |  Right block: rows 46-49 cols 38-41")
print(f"Blue markers: Blue-1(r15-16,c31-32) Blue-2(r19-20,c11-12) Blue-3(r31-32,c39-40)")

for name, action in [("ACTION1 (UP)", GameAction.ACTION1),
                     ("ACTION2 (DOWN)", GameAction.ACTION2),
                     ("ACTION3 (DIVERGE)", GameAction.ACTION3),
                     ("ACTION4 (CONVERGE)", GameAction.ACTION4),
                     ("ACTION5", GameAction.ACTION5),
                     ("ACTION7", GameAction.ACTION7)]:
    probe_action(make_l3, action, name)

# ACTION6 on distinct targets
print("\nACTION6 on distinct targets:")
targets = [
    ("Blue-1 (r15,c31)", 31, 15),
    ("Blue-2 (r19,c11)", 11, 19),
    ("Blue-3 (r31,c39)", 39, 31),
    ("Empty black cell (r46,c26)", 26, 46),
    ("Empty black cell (r42,c18)", 18, 42),
    ("Red cell (r14,c38)", 38, 14),
]
for label, x, y in targets:
    probe_action(make_l3, GameAction.ACTION6, f"ACTION6 on {label}", x=x, y=y)

# ── FROZEN STATE PROBE ────────────────────────────────────────────────────
print("\n" + "="*70)
print("FROZEN STATE — After clicking Blue-1, probe all actions")
print("="*70)

def make_frozen_blue1():
    env, obs = make_l3()
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    g = np.array(obs.frame[-1])
    yellow = np.argwhere(g == 11)
    if len(yellow):
        print(f"  [Blue-1 frozen] Yellow at rows {yellow[:,0].min()}-{yellow[:,0].max()}, cols {yellow[:,1].min()}-{yellow[:,1].max()}")
    print(f"  available_actions={list(obs.available_actions)}")
    return env, obs

make_frozen_blue1()
for name, action in [("ACTION1 (UP)", GameAction.ACTION1),
                     ("ACTION2 (DOWN)", GameAction.ACTION2),
                     ("ACTION3 (LEFT)", GameAction.ACTION3),
                     ("ACTION4 (RIGHT)", GameAction.ACTION4),
                     ("ACTION5", GameAction.ACTION5),
                     ("ACTION7", GameAction.ACTION7)]:
    probe_action(make_frozen_blue1, action, name)

print("\nACTION6 on distinct targets while frozen:")
for label, x, y in [("Black wall (r46,c26)", 26, 46),
                     ("Black wall (r14,c26)", 26, 14),
                     ("Yellow marker itself (r15,c31)", 31, 15),
                     ("Red cell (r14,c38)", 38, 14)]:
    probe_action(make_frozen_blue1, GameAction.ACTION6, f"ACTION6 on {label}", x=x, y=y)

print("\n" + "="*70)
print("FROZEN STATE — After clicking Blue-2")
print("="*70)

def make_frozen_blue2():
    env, obs = make_l3()
    obs = env.step(GameAction.ACTION6, {"x": 11, "y": 19})
    g = np.array(obs.frame[-1])
    yellow = np.argwhere(g == 11)
    if len(yellow):
        print(f"  [Blue-2 frozen] Yellow at rows {yellow[:,0].min()}-{yellow[:,0].max()}, cols {yellow[:,1].min()}-{yellow[:,1].max()}")
    print(f"  available_actions={list(obs.available_actions)}")
    return env, obs

make_frozen_blue2()
for name, action in [("ACTION1 (UP)", GameAction.ACTION1),
                     ("ACTION2 (DOWN)", GameAction.ACTION2),
                     ("ACTION3 (LEFT)", GameAction.ACTION3),
                     ("ACTION4 (RIGHT)", GameAction.ACTION4)]:
    probe_action(make_frozen_blue2, action, name)

print("\n" + "="*70)
print("FROZEN STATE — After clicking Blue-3")
print("="*70)

def make_frozen_blue3():
    env, obs = make_l3()
    obs = env.step(GameAction.ACTION6, {"x": 39, "y": 31})
    g = np.array(obs.frame[-1])
    yellow = np.argwhere(g == 11)
    if len(yellow):
        print(f"  [Blue-3 frozen] Yellow at rows {yellow[:,0].min()}-{yellow[:,0].max()}, cols {yellow[:,1].min()}-{yellow[:,1].max()}")
    print(f"  available_actions={list(obs.available_actions)}")
    return env, obs

make_frozen_blue3()
for name, action in [("ACTION1 (UP)", GameAction.ACTION1),
                     ("ACTION2 (DOWN)", GameAction.ACTION2),
                     ("ACTION3 (LEFT)", GameAction.ACTION3),
                     ("ACTION4 (RIGHT)", GameAction.ACTION4)]:
    probe_action(make_frozen_blue3, action, name)
