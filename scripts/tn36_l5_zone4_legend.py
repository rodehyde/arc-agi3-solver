"""What left legend config does Zone 4 set?"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = [(42,26),(45,26),(42,36),(45,36),(42,41),(45,41),(55,36)]
L2 = [(47,8),(47,13),(47,18),(47,23),(58,21),
      (33,39),(47,39),(33,44),(47,44),(33,49),(47,49),(33,54),(47,54),(55,47)]
L3 = [(58,5),(33,34),(47,33),(35,38),(35,43),(35,48),(35,53),(33,59),(47,58),(58,58)]
L4 = [(33,34),(41,34),(35,39),(47,39),(33,44),(35,44),
      (33,49),(35,49),(33,54),(35,54),(33,59),(35,59),(58,58)]

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs = env.observation_space
for r,c in L1+L2+L3+L4:
    obs = env.step(GameAction.ACTION6, {'x':c,'y':r})

g0 = np.array(obs.frame[-1])
result = env.step(GameAction.ACTION6, {'x':45,'y':58})
g1 = np.array(result.frame[-1])

print("Zone 4 legend changes (rows 33-49):")
for row_r in [33,35,39,41,45,47]:
    before = [c for c in range(64) if int(g0[row_r,c])==5]
    after  = [c for c in range(64) if int(g1[row_r,c])==5]
    activated   = [c for c in after if c not in before]
    deactivated = [c for c in before if c not in after]
    if activated or deactivated:
        print(f"  r{row_r}: +{activated}  -{deactivated}")
    else:
        print(f"  r{row_r}: unchanged  active={after}")
