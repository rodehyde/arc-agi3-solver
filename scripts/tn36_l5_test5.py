"""tn36 L5 — ROTATE(1)+DOWN(3)+EXPAND(1)+TURN_PURPLE(V35+H39+H45+V47 at g6)+fire"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]
RC = [34, 39, 44, 49, 54, 59]

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

env, obs = make_l5()
click(env, 33, RC[0]); click(env, 39, RC[0])            # g1: ROTATE (H33+H39)
click(env, 33, RC[1]); click(env, 35, RC[1])            # g2: DOWN
click(env, 33, RC[2]); click(env, 35, RC[2])            # g3: DOWN
click(env, 33, RC[3]); click(env, 35, RC[3])            # g4: DOWN
click(env, 41, RC[4])                                    # g5: EXPAND (V41)
click(env, 35, RC[5]); click(env, 39, RC[5])             # g6: TURN PURPLE
click(env, 45, RC[5]); click(env, 47, RC[5])             # g6 continued (V35+H39+H45+V47)
result = click(env, 58, 58)

print(f"frames={len(result.frame)}  levels={result.levels_completed}")
for i, frame in enumerate(result.frame):
    g = np.array(frame)
    yc = [(int(r),int(c)) for r,c in np.argwhere(g==11) if c>=32 and 3<=r<=55]
    if yc:
        rs = sorted(set(r for r,c in yc)); cs = sorted(set(c for r,c in yc))
        print(f"  f{i}: r{rs[0]}-{rs[-1]} c{cs[0]}-{cs[-1]} n={len(yc)}")
    else:
        print(f"  f{i}: no yellow")
