"""Verify BFS-found 13-move solution for ls20 L1."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r

def pos(r):
    g=np.array(r.frame[-1])
    ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

# BFS found: LLLUUUURRRUUU (13 moves)
seq=[A3,A3,A3, A1,A1,A1,A1, A4,A4,A4, A1,A1,A1]
print(f"Testing {''.join(ANAMES[a] for a in seq)} ({len(seq)} moves)")
env,r=fresh()
print(f"  start: pos={pos(r)}")
for i,a in enumerate(seq):
    r=env.step(a)
    print(f"  step {i+1} {ANAMES[a]}: pos={pos(r)}  levels={r.levels_completed}  state={r.state.name}")
    if r.levels_completed>=1:
        print(f"  *** LEVEL 1 COMPLETE in {i+1} moves ***")
        break
