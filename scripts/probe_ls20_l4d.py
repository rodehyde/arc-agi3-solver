"""ls20 L4: get GoalShape, StartShape, and current shape state."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']
L3=[AMAP[c] for c in 'UUUUUUUULDDDDDDDDUUULLURRRRRRRUUULUDURD']

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make('ls20')
r=env.observation_space
for a in L1+L2+L3: r=env.step(a)

g=env._game
level=g.current_level

print(f"Level: {r.levels_completed}")
print(f"StartShape: {level.get_data('StartShape')}")
print(f"kvynsvxbpi (GoalShape list): {level.get_data('kvynsvxbpi')}")
print(f"GoalRotation: {level.get_data('GoalRotation')}")
print(f"GoalColor: {level.get_data('GoalColor')}")
print()
print(f"Current fwckfzsyc (shape_idx): {g.fwckfzsyc}")
print(f"Current hiaauhahz (color_idx): {g.hiaauhahz}  (color={g.tnkekoeuk[g.hiaauhahz]})")
print(f"Current cklxociuu (rot_idx): {g.cklxociuu}  (rot={g.dhksvilbb[g.cklxociuu]})")
print()
print(f"ldxlnycps (goal shape per target): {g.ldxlnycps}")
print(f"yjdexjsoa (goal color per target): {g.yjdexjsoa}")
print(f"ehwheiwsk (goal rot per target):   {g.ehwheiwsk}")
print()
print(f"Number of shapes: {len(g.ijessuuig)}")
print(f"Shapes: {[s.name for s in g.ijessuuig]}")
print()
print(f"Target positions (plrpelhym):")
for i,sp in enumerate(g.plrpelhym):
    print(f"  {i}: ({sp.x},{sp.y})  goalShape={g.ldxlnycps[i]}  goalCol={g.yjdexjsoa[i]}  goalRot={g.ehwheiwsk[i]}")
print()
print(f"bejndxqqzf(0) = {g.bejndxqqzf(0)}  (win check)")
print()

# Now simulate hitting the shape toggle (ttfwljgohq) at (24,30)
print("=== Simulating shape toggle hits ===")
print(f"Current shape: {g.fwckfzsyc}")
for hit in range(6):
    g.fwckfzsyc = (g.fwckfzsyc + 1) % len(g.ijessuuig)
    result = g.bejndxqqzf(0)
    print(f"  After {hit+1} hits: shape_idx={g.fwckfzsyc}  bejndxqqzf(0)={result}")
