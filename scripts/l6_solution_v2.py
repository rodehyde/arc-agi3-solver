"""m0r0 Level 6 — fixed version.
Phase 5 fix: B stays at col 18 (left half) so block_pos returns B=None.
Fixed by tracking only A and checking levels_completed for WIN.
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

def find_val(g,val):
    c=np.argwhere(g==val); return (int(c[0,0]),int(c[0,1])) if len(c) else None

def block_pos_all(g):
    """Find all lt-blue blocks as distinct row-groups."""
    cells=np.argwhere(g==10)
    if not len(cells): return []
    rows=sorted(set(int(r) for r,c in cells))
    groups=[]; cur=[rows[0]]
    for r in rows[1:]:
        if r-cur[-1]<=4: cur.append(r)
        else: groups.append(cur); cur=[r]
    groups.append(cur)
    result=[]
    for grp in groups:
        gcells=cells[[r in grp for r,c in cells]]
        result.append((int(min(gcells[:,0])),int(min(gcells[:,1]))))
    return result

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
        blocks=block_pos_all(g); M=find_val(g,9); Y=find_val(g,11)
        marker=f"Y={Y}" if Y else f"M={M}"
        gb,ob=band_status(g)
        print(f"  {label}: blocks={blocks} {marker} green={'open' if gb=={5} else 'CLOSED'} orange={'open' if ob=={5} else 'CLOSED'} lvl={obs2.levels_completed}")
    return obs2

# ─────────────────────────
env,obs=make_l6()
print("L6 start. Running full sequence...")

# Phase 0: UP×2, freeze, DIV×2+UP×1+DIV×1+UP×5, unfreeze → marker(19,19)
obs=step(env,GameAction.ACTION1,obs)
obs=step(env,GameAction.ACTION1,obs)
obs=env.step(GameAction.ACTION6,{'x':31,'y':43})  # FREEZE
for _ in range(2): obs=env.step(GameAction.ACTION3)  # DIV×2
obs=env.step(GameAction.ACTION1)                      # UP×1
obs=env.step(GameAction.ACTION3)                      # DIV×1
for _ in range(5): obs=env.step(GameAction.ACTION1)   # UP×5 → marker (19,19)
obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); print(f"Phase 0 done: blocks={block_pos_all(g)} marker={find_val(g,9)}")

# Phase 1: DOWN×7 — B descends through orange band to rows 42
print("\nPhase 1: DOWN×7 (A pinned, B through orange band)")
for i in range(7):
    obs=step(env,GameAction.ACTION2,obs,f"DOWN {i+1}")
    if obs.levels_completed>5: print("WIN!"); import sys; sys.exit(0)
g=np.array(obs.frame[-1]); print(f"After P1: blocks={block_pos_all(g)} marker={find_val(g,9)}")

# Phase 2: freeze@(19,19), CON×1+UP×1 → marker(15,23), pins A from CONVERGE
obs=env.step(GameAction.ACTION6,{'x':19,'y':19})  # FREEZE
obs=env.step(GameAction.ACTION4)  # CON×1
obs=env.step(GameAction.ACTION1)  # UP×1
obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); print(f"Phase 2 done: blocks={block_pos_all(g)} marker={find_val(g,9)}")

# Phase 3: CONVERGE×6 — B moves left from col 42 to col 18 (A pinned)
print("\nPhase 3: CONVERGE×6 (B moves left to green object)")
for i in range(6):
    obs=step(env,GameAction.ACTION4,obs,f"CON {i+1}")
    if obs.levels_completed>5: print("WIN!"); import sys; sys.exit(0)
g=np.array(obs.frame[-1])
gb,ob=band_status(g)
print(f"After P3: blocks={block_pos_all(g)} marker={find_val(g,9)}")
print(f"  Green band: {gb} ({'OPEN' if gb=={5} else 'CLOSED'})  Orange: {ob}")
render(g,12,50,6,57,"After Phase 3")

# Phase 4: freeze@(15,23), DOWN×8+DIV×1 → marker(47,19), pins B from DOWN
obs=env.step(GameAction.ACTION6,{'x':23,'y':15})  # FREEZE
g=np.array(obs.frame[-1]); print(f"\nPhase 4 frozen: Y={find_val(g,11)}")
for _ in range(8): obs=env.step(GameAction.ACTION2)  # DOWN×8
obs=env.step(GameAction.ACTION3)                      # DIV×1
obs=env.step(GameAction.ACTION6,{'x':10,'y':10})  # UNFREEZE
g=np.array(obs.frame[-1]); print(f"Phase 4 done: blocks={block_pos_all(g)} marker={find_val(g,9)}")
gb,ob=band_status(g); print(f"  Green band: {gb} ({'OPEN' if gb=={5} else 'CLOSED'})")
render(g,12,52,6,57,"After Phase 4")

# Phase 5: DOWN×7 — A descends through green band to overlap B → WIN
print("\nPhase 5: DOWN×7 (B pinned, A descends)")
for i in range(7):
    obs=env.step(GameAction.ACTION2)  # DOWN — no label to avoid false-RESET on B=None
    g=np.array(obs.frame[-1])
    blocks=block_pos_all(g); M=find_val(g,9)
    gb,ob=band_status(g)
    print(f"  DOWN {i+1}: blocks={blocks} M={M} green={'open' if gb=={5} else 'CLOSED'} lvl={obs.levels_completed}")
    if obs.levels_completed>5:
        print(f"\n*** LEVEL {obs.levels_completed} COMPLETE — WIN! ***")
        break
    if not len(blocks):
        print("  All blocks gone — unexpected state"); break

print(f"\nFinal: levels={obs.levels_completed}/{obs.win_levels}")
render(g,38,52,6,57,"Final state")
