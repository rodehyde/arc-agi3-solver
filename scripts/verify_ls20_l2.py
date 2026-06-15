"""Verify the 45-move Level 2 solution step by step."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2='URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD'

def ppos(r):
    g=np.array(r.frame[-1]); ys,xs=np.where(g==12)
    return (int(xs.min()),int(ys.min())) if len(ys) else None

def ref_str(r):
    g=np.array(r.frame[-1]); c={}
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            c[(ri,ci)]=9 if blk.count(9)>=2 else 5
    return '/'.join(''.join('B' if c[(ri,ci)]==9 else '.' for ci in range(3)) for ri in range(3))

def pickups(env):
    positions=set()
    for sp in env._game.current_level.get_sprites():
        if sp.tags and 'npxgalaybz' in sp.tags:
            positions.add((sp.x, sp.y))
    return positions

arcade=Arcade(operation_mode=OperationMode.OFFLINE)
env=arcade.make('ls20')
r=env.observation_space
for a in L1: r=env.step(a)
sc=env._game._step_counter_ui

print("Replaying Level 2 solution step by step:")
print(f"  Start: pos={ppos(r)}  ref={ref_str(r)}  steps={sc.current_steps}  rot={env._game.cklxociuu}  pickups={pickups(env)}")
print()

prev_pickups=pickups(env)
for i,c in enumerate(L2):
    a=AMAP[c]
    r=env.step(a)
    pos=ppos(r)
    cur_pickups=pickups(env)
    notes=[]
    if pos==ppos(r) if False else False: pass
    if cur_pickups != prev_pickups:
        notes.append(f"PICKUP collected!")
    if env._game.cklxociuu > (0 if i==0 else env._game.cklxociuu):
        pass
    notes_str = '  *** '+' | '.join(notes) if notes else ''
    print(f"  {i+1:2d} {c}: pos={pos}  steps={sc.current_steps}  rot={env._game.cklxociuu}  levels={r.levels_completed}{notes_str}")
    if cur_pickups != prev_pickups:
        print(f"      ^ pickup change: {prev_pickups} -> {cur_pickups}")
    if r.levels_completed > 1:
        print(f"\n*** LEVEL 2 COMPLETE in {i+1} moves! ***")
        break
    prev_pickups=cur_pickups

print(f"\nFinal: levels_completed={r.levels_completed}")
