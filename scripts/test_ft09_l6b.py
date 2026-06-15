"""ft09 L6: solve coupled-toggle linear system for two grey_target hypotheses."""
import logging
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)

L1=[(38,38),(38,46),(54,46),(38,54)]
L2=[(22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48)]
L3=[(22,6),(30,6),(38,6),(22,14),(14,22),(30,22),(14,30),
    (46,30),(30,38),(46,38),(22,46),(22,54),(30,54),(38,54)]
L4=[(15,17),(23,17),(23,17),(31,17),(47,17),(15,25),(31,25),
    (47,25),(15,33),(23,33),(23,33),(31,33),(39,33),(23,41),
    (39,41),(23,49),(23,49),(31,49),(31,49),(39,49),(39,49)]
L5=[(25,15),(25,31),(41,47),(33,7),(17,23),(33,23),(49,23),
    (17,39),(33,39),(49,39),(17,55),(33,55),(25,7),(17,15),
    (33,15),(17,31),(33,31),(41,39),(33,47),(49,47),(41,55)]
PRE=L1+L2+L3+L4+L5

ROW_STARTS=[6,14,22,30,38,46]
COL_STARTS=[4,12,20,28,36,44,52]

def tc(ri,ci): return (COL_STARTS[ci]+3, ROW_STARTS[ri]+3)

def to_l6():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ft09")
    r=env.observation_space
    for x,y in PRE:
        r=env.step(GameAction.ACTION6,data={"x":x,"y":y})
    return env,r

def run(clicks, label):
    env,r = to_l6()
    for ri,ci in clicks:
        r=env.step(GameAction.ACTION6,data={"x":tc(ri,ci)[0],"y":tc(ri,ci)[1]})
        if r.levels_completed >= 6:
            print(f"{label}: LEVEL 6 COMPLETE after {len(clicks)} clicks! >>>")
            return True
    print(f"{label}: levels={r.levels_completed}  no win")
    return False

# ── Hypothesis A: grey_target = yellow (opposite of centre=green)
# Target: GREEN=(1,0),(1,1),(1,4),(2,2),(2,3),(2,5),(3,1),(3,3),(3,4),(4,2),(4,5),(4,6)
#         YELLOW=(0,0),(1,2),(1,3),(1,5),(2,1),(3,5),(4,1),(4,3),(4,4),(5,6)
# Solve GF(2) column by column (each col is independent):
# Col0: x10=1 x00=0      (t10=G t00=Y → x00+x10=0,x10=1 → x10=1,x00=1? let me recheck)
#   t(0,0)=0: x00+x10=0; t(1,0)=1: x10=1 → x10=1,x00=1
# Col1: t11=1,t21=0,t31=1,t41=0
#   x41=0; x31+0=1→x31=1; x21+1=0→x21=1; x11+1=1→x11=0
# Col2: t12=0,t22=1; (2,2)=key-blocks below
#   x22=1; x12+1=0→x12=1
#   (4,2): x42=1
# Col3: t13=0,t23=1,t33=1,t43=0
#   x43=0; x33+0=1→x33=1; x23+1=1→x23=0; x13+0=0→x13=0
# Col4: t14=1; (2,4)=KEY; t34=1,t44=0
#   x14=1
#   x44=0; x34+0=1→x34=1
# Col5: t15=0,t25=1,t35=0,t45=1; (5,5)=KEY
#   x45=1; x35+1=0→x35=1; x25+1=1→x25=0; x15+0=0→x15=0
# Col6: t46=1,t56=0
#   x56=0; x46+0=1→x46=1
SOL_A = [(0,0),(1,0),(1,2),(1,4),(2,1),(2,2),(3,1),(3,3),(3,4),(3,5),(4,2),(4,5),(4,6)]
print(f"Hypothesis A (grey=yellow): {len(SOL_A)} clicks = {SOL_A}")
run(SOL_A, "A")

# ── Hypothesis B: grey_target = green (all tiles → green)
# All targets = 1 (green)
# Col0: x10=1,x00+x10=1→x00=0
# Col1: x41=1,x31=0,x21=1,x11=0
# Col2: x22=1,x12=0,x42=1
# Col3: x43=1,x33=0,x23=1,x13=0
# Col4: x14=1; x44=1,x34=0
# Col5: x45=1,x35=0,x25=1,x15=0
# Col6: x56=1,x46=0
SOL_B = [(1,0),(1,4),(2,1),(2,2),(2,3),(2,5),(4,1),(4,2),(4,3),(4,4),(4,5),(5,6)]
print(f"Hypothesis B (grey=green):  {len(SOL_B)} clicks = {SOL_B}")
run(SOL_B, "B")
