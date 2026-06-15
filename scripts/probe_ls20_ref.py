"""ls20 L1: track reference box changes as piece visits positions."""
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
PALETTE=['#FFFFFF','#D3D3D3','#A9A9A9','#696969','#404040','#000000','#FFC0CB',
         '#FFB6C1','#FF0000','#0000FF','#ADD8E6','#FFFF00','#FFA500','#800000','#008000','#800080']
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4

def fresh():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    return env,r
def grid(r): return np.array(r.frame[-1])

def ref_box(g):
    """Return bottom-left reference box as string (rows 54-61, cols 2-9)."""
    return tuple(int(g[r,c]) for r in range(54,62) for c in range(2,10))

def top_box(g):
    """Return top box interior as string (rows 9-15, cols 33-39)."""
    return tuple(int(g[r,c]) for r in range(9,16) for c in range(33,40))

def obbox(g):
    ys,xs=np.where(g==12); return (int(ys.min()),int(xs.min())) if len(ys) else None

# Baseline
env,r=fresh()
g0=grid(r)
ref0=ref_box(g0); top0=top_box(g0)
print(f"Start ref_box: {ref0}")
print(f"Start top_box: {top0}")

# Check all 36 reachable positions — record ref_box at each
POSITIONS = [
    ((15,34),[A1]*6),
    ((20,34),[A1]*5),
    ((25,14),[A1,A1,A1,A1,A3,A3,A3,A3]),
    ((25,19),[A1,A1,A1,A1,A3,A3,A3]),
    ((25,24),[A1,A1,A1,A1,A3,A3]),
    ((25,29),[A1,A1,A1,A1,A3]),
    ((25,34),[A1]*4),
    ((25,39),[A1,A1,A1,A1,A4]),
    ((25,44),[A1,A1,A1,A1,A4,A4]),
    ((25,49),[A1,A1,A1,A1,A4,A4,A4]),
    ((30,14),[A3,A3,A3,A1,A1,A1,A3]),
    ((30,19),[A3,A3,A3,A1,A1,A1]),
    ((30,24),[A1,A1,A1,A1,A3,A3,A2]),
    ((30,34),[A1]*3),
    ((30,39),[A1,A1,A1,A4]),
    ((30,44),[A1,A1,A1,A4,A4]),
    ((30,49),[A1,A1,A1,A4,A4,A4]),
    ((35,14),[A3,A3,A3,A1,A1,A3]),
    ((35,19),[A3,A3,A3,A1,A1]),
    ((35,24),[A3,A3,A3,A1,A1,A4]),
    ((35,34),[A1,A1]),
    ((35,39),[A1,A1,A4]),
    ((35,44),[A1,A1,A4,A4]),
    ((35,49),[A1,A1,A4,A4,A4]),
    ((40,19),[A3,A3,A3,A1]),
    ((40,34),[A1]),
    ((40,39),[A1,A4]),
    ((40,44),[A1,A4,A4]),
    ((40,49),[A1,A4,A4,A4]),
    ((45,19),[A3,A3,A3]),
    ((45,24),[A3,A3]),
    ((45,29),[A3]),
    ((45,34),[]),
    ((45,39),[A4]),
    ((45,44),[A4,A4]),
    ((45,49),[A4,A4,A4]),
]

print("\nRef box changes at each position:")
for pos, seq in POSITIONS:
    env2,r2=fresh()
    g_=grid(r2)  # need obs_space
    for a in seq: r2=env2.step(a)
    g2=grid(r2)
    ref2=ref_box(g2)
    top2=top_box(g2)
    ref_changed = (ref2 != ref0)
    top_changed = (top2 != top0)
    if ref_changed or top_changed:
        print(f"  {pos}: ref_changed={ref_changed} top_changed={top_changed}")
        if ref_changed:
            print(f"    ref: {ref2}")
    else:
        print(f"  {pos}: no change")
