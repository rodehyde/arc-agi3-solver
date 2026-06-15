"""ls20 L3: full scene inspection — sprites, colours, positions."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']

COLOR_NAMES={0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
             6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
             12:'orange',13:'maroon',14:'green',15:'purple'}

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make('ls20')
r=env.observation_space
for a in L1+L2: r=env.step(a)

g=np.array(r.frame[-1])
game=env._game
level=game.current_level

print(f"Level: {r.levels_completed}  state: {r.state.name}  avail: {r.available_actions}")
print(f"Step counter: max={game._step_counter_ui.osgviligwp}  current={game._step_counter_ui.current_steps}  decrement={game._step_counter_ui.efipnixsvl}")
print(f"GoalRotation: {level.get_data('GoalRotation')}  GoalColor: {level.get_data('GoalColor')}  StartRotation: {level.get_data('StartRotation')}")

# Player position
ys,xs=np.where(g==12); px,py=int(xs.min()),int(ys.min())
print(f"\nPlayer (orange) top-left: col={px}, row={py}")

# All tagged sprites
print("\nTagged sprites:")
for sp in level.get_sprites():
    if sp.tags:
        print(f"  ({sp.x},{sp.y}) {sp.width}x{sp.height}  tags={sp.tags}")

# Colour distribution
from collections import Counter, defaultdict
counts=Counter(g.flatten().tolist())
print(f"\nColour counts (non-background):")
for v,n in counts.most_common():
    if v != 4:
        print(f"  {v} ({COLOR_NAMES.get(v,'?')}): {n}")

# Non-background objects grouped by colour
by_color=defaultdict(list)
for row in range(64):
    for col in range(64):
        v=int(g[row,col])
        if v not in (4,3,5):  # exclude background, floor, walls
            by_color[v].append((row,col))

print("\nKey objects (excluding floor/walls/bg):")
for v in sorted(by_color.keys()):
    cells=by_color[v]
    rows=[r_ for r_,c_ in cells]; cols=[c_ for r_,c_ in cells]
    print(f"  {v} ({COLOR_NAMES.get(v,'?')}): {len(cells)} cells  rows {min(rows)}-{max(rows)}  cols {min(cols)}-{max(cols)}")

# Compact grid map
print("\n--- GRID MAP (bg=space, floor=., wall=#, player=O/B) ---")
def show(label,r0,r1,c0,c1):
    print(f"\n{label}:")
    for row in range(r0,r1+1):
        line=''
        for col in range(c0,c1+1):
            v=int(g[row,col])
            if v==4: line+=' '
            elif v==3: line+='.'
            elif v==5: line+='#'
            elif v==12: line+='O'
            elif v==9: line+='B'
            elif v==11: line+='Y'
            elif v==10: line+='b'
            elif v==8: line+='R'
            elif v==14: line+='G'
            elif v==0: line+='W'
            elif v==1: line+='g'
            else: line+=str(v)
        print(f" {row:2d}: {line}")

show("FULL GRID", 0, 63, 0, 63)
