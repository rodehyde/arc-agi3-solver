"""Direct test of win path from known reachable state (18,26,14,34).
Path: 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUD' reaches L(18,26) R(14,34).
Hypothesis: +C (CONVERGE) moves right to col=30 in passage,
            +U (UP) moves left to col=26 or into right's position → WIN.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
char = {0: '.', 1: 'a', 5: '#', 8: 'R', 9: 'B', 10: 'L', 11: 'Y', 15: 'V'}

def setup_game():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    # Blue-1
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3,
                GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-2
    g = np.array(obs.frame[-1])
    bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    # Blue-3
    g = np.array(obs.frame[-1])
    bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3):
        obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    return env, obs

def get_state(obs):
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    if not len(cells): return None
    left = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:, 0].min()), int(left[:, 1].min()),
            int(right[:, 0].min()), int(right[:, 1].min()))

def render_central(obs):
    g = np.array(obs.frame[-1])
    print("     " + "".join(f"{c % 10}" for c in range(20, 45)))
    for r in range(12, 23):
        row = "".join(char.get(int(g[r, c]), '?') for c in range(20, 45))
        print(f"{r:3d}  {row}")

# Replay to known state (18,26,14,34)
NAV_PATH = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUD'
print(f"Replaying nav path: '{NAV_PATH}' ({len(NAV_PATH)} actions)...")
env, obs = setup_game()
for a in NAV_PATH:
    obs = env.step(AMAP[a])

s = get_state(obs)
print(f"State after nav: {s}  levels={obs.levels_completed}")
print("Grid (central):")
render_central(obs)

# Try all 4 single actions
print("\n--- Single-action probes ---")
for name, act in [('U', GameAction.ACTION1), ('D', GameAction.ACTION2),
                  ('X', GameAction.ACTION3), ('C', GameAction.ACTION4)]:
    env2, obs2 = setup_game()
    for a in NAV_PATH: obs2 = env2.step(AMAP[a])
    o = env2.step(act)
    ns = get_state(o)
    win = o.levels_completed > 2
    print(f"  +{name}: {ns}  levels={o.levels_completed}  {'*** WIN ***' if win else ''}")

# Try 2-action sequences from state
print("\n--- 2-action sequences ---")
win_found = False
for n1 in ['U', 'D', 'X', 'C']:
    for n2 in ['U', 'D', 'X', 'C']:
        env2, obs2 = setup_game()
        for a in NAV_PATH: obs2 = env2.step(AMAP[a])
        o1 = env2.step(AMAP[n1])
        if o1.levels_completed > 2:
            print(f"  +{n1}: *** WIN ***")
            win_found = True
            break
        o2 = env2.step(AMAP[n2])
        ns = get_state(o2)
        win = o2.levels_completed > 2
        if win:
            print(f"  +{n1}+{n2}: *** WIN *** via '{NAV_PATH+n1+n2}'")
            win_found = True
    if win_found: break

if not win_found:
    print("  No win in 2-action sequences. Trying 3-action sequences (C then 2 more)...")
    # Focus on CONVERGE first, then explore
    env2, obs2 = setup_game()
    for a in NAV_PATH: obs2 = env2.step(AMAP[a])
    o_c = env2.step(GameAction.ACTION4)  # CONVERGE
    s_c = get_state(o_c)
    print(f"\nAfter C: {s_c}  levels={o_c.levels_completed}")
    print("Grid after CONVERGE:")
    render_central(o_c)

    for n2 in ['U', 'D', 'X', 'C']:
        o2 = env2.step(AMAP[n2])
        s2 = get_state(o2)
        win = o2.levels_completed > 2
        print(f"  +C+{n2}: {s2}  levels={o2.levels_completed}  {'*** WIN ***' if win else ''}")
        if win:
            print(f"  FULL PATH: '{NAV_PATH}C{n2}'")
            win_found = True
            break
        for n3 in ['U', 'D', 'X', 'C']:
            env3, obs3 = setup_game()
            for a in NAV_PATH + 'C' + n2: obs3 = env3.step(AMAP[a])
            o3 = env3.step(AMAP[n3])
            if o3.levels_completed > 2:
                print(f"  +C+{n2}+{n3}: *** WIN *** via '{NAV_PATH}C{n2}{n3}'")
                win_found = True
                break
        if win_found: break
