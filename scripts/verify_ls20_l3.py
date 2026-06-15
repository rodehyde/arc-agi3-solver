"""ls20 L3: step-by-step verification of 39-move BFS solution."""
import logging, numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
AMAP={'U':A1,'D':A2,'L':A3,'R':A4}
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

L1=[A3,A3,A3,A1,A1,A1,A1,A4,A4,A4,A1,A1,A1]
L2=[AMAP[c] for c in 'URUUUUURRDRDDDDDDUDDLLRURUUUUUUULLLLLLDLDDDDD']
L3_SEQ='UUUUUUUULDDDDDDDDUUULLURRRRRRRUUULUDURD'

def make_env():
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make('ls20')
    r=env.observation_space
    for a in L1+L2: r=env.step(a)
    return env, r

def pp(env): sp=env._game.gudziatsk; return (sp.x, sp.y)

def pickup_positions(env):
    return frozenset(
        (sp.x,sp.y) for sp in env._game.current_level.get_sprites()
        if sp.tags and 'npxgalaybz' in sp.tags
    )

env,r=make_env()
print(f"L3 START: pos={pp(env)}  rot={env._game.cklxociuu}  col={env._game.hiaauhahz}  steps={env._game._step_counter_ui.current_steps}")
print(f"  pickups remaining: {pickup_positions(env)}")
print(f"  target: col=54 row=50  goalRot=180  goalCol=blue(9)")
print()

actions=[AMAP[c] for c in L3_SEQ]
prev_pickups=pickup_positions(env)

for i,a in enumerate(actions):
    prev_pos=pp(env)
    prev_rot=env._game.cklxociuu
    prev_col=env._game.hiaauhahz
    prev_steps=env._game._step_counter_ui.current_steps

    r=env.step(a)

    pos=pp(env)
    rot=env._game.cklxociuu
    col=env._game.hiaauhahz
    steps=env._game._step_counter_ui.current_steps
    cur_pickups=pickup_positions(env)

    notes=[]
    if rot!=prev_rot: notes.append(f'ROT {prev_rot}->{rot}')
    if col!=prev_col: notes.append(f'COL {prev_col}->{col}')
    if cur_pickups!=prev_pickups:
        collected=prev_pickups-cur_pickups
        notes.append(f'PICKUP COLLECTED {collected}  steps reset->{steps}')
    if pos==prev_pos: notes.append('BLOCKED')
    if r.levels_completed>2: notes.append('*** LEVEL COMPLETE ***')

    note_str=('  '+' | '.join(notes)) if notes else ''
    print(f"  {i+1:2d} {ANAMES[a]}: {prev_pos}->{pos}  rot={rot}  col={col}  steps={steps}{note_str}")

    prev_pickups=cur_pickups

    if r.levels_completed>2:
        print(f"\n=== LEVEL 3 COMPLETE in {len(L3_SEQ)} moves! ===")
        print(f"  levels_completed={r.levels_completed}")
        break
else:
    print(f"\n  Final: pos={pp(env)}  rot={env._game.cklxociuu}  col={env._game.hiaauhahz}  levels={r.levels_completed}")
    print("  *** DID NOT COMPLETE ***")
