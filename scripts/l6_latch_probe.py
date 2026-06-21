"""Probe: can we latch a band open by parking the marker inside it?
Freeze at rows 14 (bands open) → move marker into band zone → unfreeze → check if band stays open.
Also checks what ACTION6 click on the green object (rows 42-45 cols 18-21) does.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1='UUXUUUUUCUCCCCCDDDCDDDDDXD'; L2='DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3='UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
L5='XXUUUUUUXUCCCCUUXXXXXXUUUUUUUUCCCCCCXXXUUUUUXXXX'
AMAP={'U':GameAction.ACTION1,'D':GameAction.ACTION2,'X':GameAction.ACTION3,'C':GameAction.ACTION4}

def make_l6():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE); env=arcade.make('m0r0')
    obs=env.observation_space
    for a in L1+L2: obs=env.step(AMAP[a])
    obs=env.step(GameAction.ACTION6,{'x':31,'y':15})
    for act in [GameAction.ACTION4,GameAction.ACTION1,GameAction.ACTION4,GameAction.ACTION4,
                GameAction.ACTION4,GameAction.ACTION4,GameAction.ACTION2,GameAction.ACTION2,
                GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION3,GameAction.ACTION1]:
        obs=env.step(act)
    obs=env.step(GameAction.ACTION6,{'x':14,'y':46})
    g=np.array(obs.frame[-1])
    bxy2=next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9),None)
    obs=env.step(GameAction.ACTION6,{'x':bxy2[0],'y':bxy2[1]})
    for act in [GameAction.ACTION1,GameAction.ACTION4,GameAction.ACTION1]: obs=env.step(act)
    obs=env.step(GameAction.ACTION6,{'x':14,'y':46})
    g=np.array(obs.frame[-1])
    bxy3=next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9),None)
    obs=env.step(GameAction.ACTION6,{'x':bxy3[0],'y':bxy3[1]})
    for _ in range(3): obs=env.step(GameAction.ACTION4)
    obs=env.step(GameAction.ACTION6,{'x':14,'y':46})
    for a in NAV3: obs=env.step(AMAP[a])
    for a in 'UU': obs=env.step(AMAP[a])
    obs=env.step(GameAction.ACTION6,{'x':30,'y':30})
    for _ in range(3): obs=env.step(GameAction.ACTION3)
    obs=env.step(GameAction.ACTION6,{'x':9,'y':40})
    for a in 'DDCDCC': obs=env.step(AMAP[a])
    for a in L5: obs=env.step(AMAP[a])
    assert obs.levels_completed==5
    return env,obs

def block_pos(g):
    cells=np.argwhere(g==10)
    if not len(cells): return None,None
    left=cells[cells[:,1]<32]; right=cells[cells[:,1]>=32]
    lp=(int(left[:,0].min()),int(left[:,1].min())) if len(left) else None
    rp=(int(right[:,0].min()),int(right[:,1].min())) if len(right) else None
    return lp,rp

def find_val(g,val):
    c=np.argwhere(g==val); return (int(c[0,0]),int(c[0,1])) if len(c) else None

char={0:'.',1:'f',5:'#',6:'p',7:'q',8:'R',9:'M',10:'L',11:'Y',12:'O',13:'m',14:'G',15:'V'}
def render(g,r0,r1,c0,c1,label=''):
    if label: print(f'\n{label}')
    print('      '+''.join(f'{c%10}' for c in range(c0,c1+1)))
    for r in range(r0,r1+1):
        row=''.join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f'{r:3d}   {row}')

def band_status(g):
    gb=[int(g[30,c]) for c in range(14,26)]
    ob=[int(g[30,c]) for c in range(38,50)]
    return gb,ob

# ─── SECTION 1: Latch green band open ───
print("="*60)
print("SECTION 1: Freeze at rows 14 → marker into green band → unfreeze")
print("="*60)
env,obs=make_l6()
# Navigate to rows 14
obs=env.step(GameAction.ACTION1); obs=env.step(GameAction.ACTION1)
g=np.array(obs.frame[-1]); A,B=block_pos(g)
gb,ob=band_status(g)
print(f"At rows 14: A={A}, B={B}")
print(f"  green band (row 30 cols 14-25): {gb}")
print(f"  orange band (row 30 cols 38-49): {ob}")

# Freeze at rows 14
obs=env.step(GameAction.ACTION6,{'x':31,'y':43})
g=np.array(obs.frame[-1]); Y=find_val(g,11)
print(f"\nFrozen at rows 14. Y={Y}")
gb,ob=band_status(g)
print(f"  green band during freeze: {gb}")

# Move marker into green band zone: DIV×1 (col 31→27), UP×3 (rows 43→39→35→31)
obs=env.step(GameAction.ACTION3); g=np.array(obs.frame[-1])
print(f"DIV×1: Y={find_val(g,11)}")
for i in range(3):
    obs=env.step(GameAction.ACTION1); g=np.array(obs.frame[-1])
    print(f"UP  {i+1}: Y={find_val(g,11)}")
Y=find_val(g,11)
print(f"Marker now at {Y} (should be in green band zone rows 30-33)")

# Unfreeze with marker inside green band zone
obs=env.step(GameAction.ACTION6,{'x':10,'y':10})
g=np.array(obs.frame[-1]); A,B=block_pos(g); M=find_val(g,9)
gb,ob=band_status(g)
print(f"\nAfter unfreeze: A={A}, B={B}, marker={M}")
print(f"  green band: {gb}  ← is it still open (5) or closed (14)?")
print(f"  orange band: {ob}")
render(g,12,48,6,57,"State after marker in green band zone")

# Test: press DOWN — does A go through open band?
print("\nTest DOWN presses with latched marker:")
for i in range(8):
    obs=env.step(GameAction.ACTION2)
    g=np.array(obs.frame[-1]); A,B=block_pos(g)
    gb,ob=band_status(g)
    print(f"  DOWN {i+1}: A={A}, B={B}  green={set(gb)}  lvl={obs.levels_completed}")
    if obs.levels_completed>5: print("WIN!"); break
    if A is None or B is None: print("RESET"); break

# ─── SECTION 2: ACTION6 on the green object ───
print("\n"+"="*60)
print("SECTION 2: Click ACTION6 on green object (rows 42-45 cols 18-21)")
print("="*60)
env2,obs2=make_l6()
obs2=env2.step(GameAction.ACTION1); obs2=env2.step(GameAction.ACTION1)  # UP×2 to rows 14
# Send A down to rows 42 (B pinned) — quick version using the known working sequence
# First freeze at rows 14: CON×3, UP×6, unfreeze → marker (19,43), B pinned
obs2=env2.step(GameAction.ACTION6,{'x':31,'y':43})
for _ in range(3): obs2=env2.step(GameAction.ACTION4)
for _ in range(6): obs2=env2.step(GameAction.ACTION1)
obs2=env2.step(GameAction.ACTION6,{'x':10,'y':10})
g2=np.array(obs2.frame[-1]); A,B=block_pos(g2); M=find_val(g2,9)
print(f"Setup: A={A}, B={B}, marker={M}")
# DOWN×7 to get A to rows 42
for _ in range(7): obs2=env2.step(GameAction.ACTION2)
g2=np.array(obs2.frame[-1]); A,B=block_pos(g2)
print(f"After DOWN×7: A={A}, B={B}")
gb2,ob2=band_status(g2)
print(f"  Bands: green={set(gb2)}, orange={set(ob2)}")

# Now click ACTION6 on green object at rows 42-45, cols 18-21
g0=np.array(obs2.frame[-1])
print(f"\nClicking green object at (x=18, y=42)...")
obs2=env2.step(GameAction.ACTION6,{'x':18,'y':42})
g2=np.array(obs2.frame[-1]); A,B=block_pos(g2); M=find_val(g2,9)
gb2,ob2=band_status(g2)
changed=np.sum(g0!=g2)
print(f"After click: A={A}, B={B}, marker={M}")
print(f"  cells changed: {changed}")
print(f"  green band: {set(gb2)}, orange band: {set(ob2)}")
render(g2,12,50,6,57,"After clicking green object")

# Try clicking other cells in green object region
for cy,cx in [(43,18),(44,19),(42,21)]:
    g0=np.array(obs2.frame[-1])
    obs2=env2.step(GameAction.ACTION6,{'x':cx,'y':cy})
    g2=np.array(obs2.frame[-1]); A,B=block_pos(g2)
    gb2,ob2=band_status(g2)
    print(f"Click (x={cx},y={cy}): A={A}, B={B}  green={set(gb2)} orange={set(ob2)}  changed={np.sum(g0!=g2)}")
