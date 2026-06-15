"""ls20: BFS solver for all 7 levels using game simulation.

State = (player_x, player_y, ref_bits) where ref_bits encodes shape/color/rotation.
Each BFS node stores the full action path; game is re-simulated from level start for each node.
"""
import logging, time
from collections import deque
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

logging.basicConfig(level=logging.ERROR)
A1,A2,A3,A4=GameAction.ACTION1,GameAction.ACTION2,GameAction.ACTION3,GameAction.ACTION4
ACTIONS=[A1,A2,A3,A4]
ANAMES={A1:'U',A2:'D',A3:'L',A4:'R'}

def make_env(preamble):
    arcade=Arcade(operation_mode=OperationMode.OFFLINE)
    env=arcade.make("ls20")
    r=env.observation_space
    for a in preamble:
        r=env.step(a)
    return env, r

def read_state(r):
    """(x, y, ref_bits): ref_bits = 9-bit encoding of 3x3 ref box."""
    g=np.array(r.frame[-1])
    ys,xs=np.where(g==12)
    if len(ys)==0: return None
    px,py=int(xs.min()),int(ys.min())
    ref_bits=0
    for ri,rr in enumerate([55,57,59]):
        for ci,cc in enumerate([3,5,7]):
            blk=[int(g[rr+dr,cc+dc]) for dr in range(2) for dc in range(2)]
            if blk.count(9)>=2: ref_bits|=(1<<(ri*3+ci))
    return (px, py, ref_bits)

def bfs(preamble, start_level, max_depth=40):
    """BFS from the state after executing preamble. Returns winning extra moves."""
    t0=time.time()
    env0,r0=make_env(preamble)
    init_state=read_state(r0)
    if init_state is None:
        return None
    start_levels=r0.levels_completed

    # Queue: (extra_moves, state)
    queue=deque([([], init_state)])
    seen={init_state}
    nodes=0

    while queue:
        path, state=queue.popleft()
        nodes+=1
        if nodes % 500 == 0:
            print(f"    nodes={nodes} depth={len(path)} queue={len(queue)} seen={len(seen)}")
        if len(path) >= max_depth:
            continue

        for a in ACTIONS:
            env2,r2=make_env(preamble)
            for m in path: r2=env2.step(m)
            r2=env2.step(a)

            if r2.levels_completed > start_levels:
                win=path+[a]
                print(f"  Win in {len(win)} moves ({nodes} nodes, {time.time()-t0:.1f}s)")
                return win

            ns=read_state(r2)
            if ns is None: continue
            if ns in seen: continue
            seen.add(ns)
            queue.append((path+[a], ns))

    print(f"  No win in {max_depth} moves ({nodes} nodes, {time.time()-t0:.1f}s)")
    return None

LEVEL_SOLUTIONS={}

def solve_all():
    full_seq=[]
    for level_num in range(1,8):
        print(f"\n=== Level {level_num} ===")
        sol=bfs(full_seq, level_num)
        if sol is None:
            print(f"  FAILED on level {level_num}")
            return None
        LEVEL_SOLUTIONS[level_num]=sol
        seq_str=''.join(ANAMES[a] for a in sol)
        print(f"  L{level_num}: {len(sol)} moves: {seq_str}")
        full_seq.extend(sol)
        env,r=make_env(full_seq)
        print(f"  After L{level_num}: levels_completed={r.levels_completed} state={r.state.name}")
        if r.state.name=='WIN':
            print(f"\nGAME COMPLETE! Total moves: {len(full_seq)}")
            print(f"Full: {''.join(ANAMES[a] for a in full_seq)}")
            return full_seq
    return full_seq

if __name__=='__main__':
    result=solve_all()
    if result:
        print(f"\nACTIONS={result}")
