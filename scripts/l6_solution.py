"""m0r0 Level 6 solution attempt.

Full sequence (all actions at L6 start):
  Phase 0: UP×2, freeze@14, DIV×2+UP×1+DIV×1+UP×5, unfreeze → marker(19,19), pins A from DOWN
  Phase 1: DOWN×7 → B through orange band to (42,42). A pinned at (14,18).
  Phase 2: freeze@(19,19), CON×1+UP×1, unfreeze → marker(15,23), pins A from CONVERGE
  Phase 3: CONVERGE×6 → B moves left (42,42)→(42,18). A stays at (14,18).
  Phase 4: freeze@(15,23), DOWN×8+DIV×1, unfreeze → marker(47,19), pins B from DOWN
  Phase 5: DOWN×7 → A descends (14,18)→(42,18) = overlap with B → WIN
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1='UUXUUUUUCUCCCCCDDDCDDDDDXD'; L2='DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3='UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
L5='XXUUUUUUXUCCCCUUXXXXXXUUUUUUUUCCCCCCXXXUUUUUXXXX'
AMAP={'U':GameAction.ACTION1,'D':GameAction.ACTION2,'X':GameAction.ACTION3,'C':GameAction.ACTION4}
char={0:'.',1:'f',5:'#',6:'p',7:'q',8:'R',9:'M',10:'L',11:'Y',12:'O',13:'m',14:'G',15:'V'}

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

def band_status(g):
    gb=set(int(g[r,c]) for r in range(30,34) for c in range(14,26))
    ob=set(int(g[r,c]) for r in range(30,34) for c in range(38,50))
    return gb,ob

def render(g,r0,r1,c0,c1,label=''):
    if label: print(f'\n{label}')
    print('      '+''.join(f'{c%10}' for c in range(c0,c1+1)))
    for r in range(r0,r1+1):
        row=''.join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f'{r:3d}   {row}')

def step(env,act,obs,label=None):
    obs2=env.step(act)
    g=np.array(obs2.frame[-1])
    if label:
        A,B=block_pos(g); M=find_val(g,9); Y=find_val(g,11)
        marker=f"Y={Y}" if Y else f"M={M}"
        gb,ob=band_status(g)
        print(f"  {label}: A={A} B={B} {marker} green={'open' if gb=={5} else 'CLOSED'} orange={'open' if ob=={5} else 'CLOSED'} lvl={obs2.levels_completed}")
    return obs2

# ───────────────────────────────────────────
env,obs=make_l6()
g=np.array(obs.frame[-1])
print(f"L6 start: A={block_pos(g)[0]}, B={block_pos(g)[1]}, marker={find_val(g,9)}")
render(g,12,50,6,57,"L6 initial")

# ── Phase 0: navigate to rows 14, freeze, reposition marker to (19,19) ──
print("\n=== PHASE 0: UP×2, freeze@14, marker→(19,19) ===")
obs=step(env,GameAction.ACTION1,obs,"UP 1")
obs=step(env,GameAction.ACTION1,obs,"UP 2")  # blocks at rows 14, bands open

obs=env.step(GameAction.ACTION6,{'x':31,'y':43})  # FREEZE
g=np.array(obs.frame[-1]); print(f"  Frozen: Y={find_val(g,11)}")

obs=step(env,GameAction.ACTION3,obs,"  DIV 1")   # col 31→27
obs=step(env,GameAction.ACTION3,obs,"  DIV 2")   # col 27→23 (green object blocks col 19 at rows 43)
obs=step(env,GameAction.ACTION1,obs,"  UP  1")   # rows 43→39 (above green object)
obs=step(env,GameAction.ACTION3,obs,"  DIV 3")   # col 23→19 (clear at rows 39)
obs=step(env,GameAction.ACTION1,obs,"  UP  2")   # rows 39→35
obs=step(env,GameAction.ACTION1,obs,"  UP  3")   # rows 35→31 (through open green band)
obs=step(env,GameAction.ACTION1,obs,"  UP  4")   # rows 31→27
obs=step(env,GameAction.ACTION1,obs,"  UP  5")   # rows 27→23
obs=step(env,GameAction.ACTION1,obs,"  UP  6")   # rows 23→19

obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); A,B=block_pos(g); M=find_val(g,9)
print(f"  Unfrozen: A={A} B={B} marker={M}")
render(g,12,48,6,57,"After Phase 0")

# ── Phase 1: DOWN×7 → B through orange band to rows 42 ──
print("\n=== PHASE 1: DOWN×7 (A pinned, B through orange band) ===")
for i in range(7):
    obs=step(env,GameAction.ACTION2,obs,f"DOWN {i+1}")
    if obs.levels_completed>5: print("WIN!"); break
    if block_pos(np.array(obs.frame[-1]))[0] is None: print("RESET"); break

g=np.array(obs.frame[-1]); A,B=block_pos(g)
print(f"\nAfter Phase 1: A={A}, B={B}")
gb,ob=band_status(g)
print(f"Green band: {gb}  Orange band: {ob}")
render(g,12,50,6,57,"After Phase 1")

# ── Phase 2: freeze@(19,19), move to (15,23), unfreeze → pins A from CONVERGE ──
print("\n=== PHASE 2: freeze@(19,19), marker→(15,23) ===")
obs=env.step(GameAction.ACTION6,{'x':19,'y':19})  # FREEZE
g=np.array(obs.frame[-1]); print(f"  Frozen: Y={find_val(g,11)}")

obs=step(env,GameAction.ACTION4,obs,"  CON 1")   # col 19→23
obs=step(env,GameAction.ACTION1,obs,"  UP  1")   # rows 19→15

obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); A,B=block_pos(g); M=find_val(g,9)
print(f"  Unfrozen: A={A} B={B} marker={M}")

# ── Phase 3: CONVERGE×6 → B from col 42 to col 18 ──
print("\n=== PHASE 3: CONVERGE×6 (A blocked, B moves left to green object) ===")
for i in range(6):
    obs=step(env,GameAction.ACTION4,obs,f"CON {i+1}")
    if obs.levels_completed>5: print("WIN!"); break

g=np.array(obs.frame[-1]); A,B=block_pos(g)
gb,ob=band_status(g)
print(f"\nAfter Phase 3: A={A}, B={B}")
print(f"Green band: {gb} ({'OPEN' if gb=={5} else 'CLOSED'})  Orange band: {ob}")
render(g,12,50,6,57,"After Phase 3")

# ── Phase 4: freeze@(15,23), marker→(47,19), pins B from DOWN ──
print("\n=== PHASE 4: freeze@(15,23), marker→(47,19) ===")
obs=env.step(GameAction.ACTION6,{'x':23,'y':15})  # FREEZE
g=np.array(obs.frame[-1]); print(f"  Frozen: Y={find_val(g,11)}")
gb2,ob2=band_status(g); print(f"  Bands during freeze: green={gb2} orange={ob2}")

for i in range(8):
    obs=step(env,GameAction.ACTION2,obs,f"  DOWN {i+1}")  # rows 15→19→...→47
obs=step(env,GameAction.ACTION3,obs,"  DIV  1")           # col 23→19

obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); A,B=block_pos(g); M=find_val(g,9)
print(f"  Unfrozen: A={A} B={B} marker={M}")
render(g,12,52,6,57,"After Phase 4")

# ── Phase 5: DOWN×7 → A descends to overlap B → WIN ──
print("\n=== PHASE 5: DOWN×7 (B pinned, A descends through green band) ===")
for i in range(7):
    obs=step(env,GameAction.ACTION2,obs,f"DOWN {i+1}")
    g=np.array(obs.frame[-1])
    if obs.levels_completed>5:
        print(f"\n*** LEVEL {obs.levels_completed} COMPLETE! WIN! ***")
        break
    A,B=block_pos(g)
    if A is None or B is None: print("RESET"); break

print(f"\nFinal: levels={obs.levels_completed}/{obs.win_levels}")
render(g,38,52,6,57,"Final state")
