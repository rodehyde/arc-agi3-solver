"""Try: left x3, up x1 from L5 start. Report positions after each step."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
char = {0:'.', 5:'#', 6:'p', 7:'q', 10:'L', 12:'O', 14:'G', 15:'V'}

def make_l5():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2: obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c,r) for r in range(18,23) for c in range(10,15) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    for a in NAV3: obs = env.step(AMAP[a])
    for a in 'UU': obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})
    for a in 'DDCDCC': obs = env.step(AMAP[a])
    assert obs.levels_completed == 4
    return env, obs

def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left  = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    lp = (int(left[:,0].min()),  int(left[:,1].min())) if len(left) else None
    rp = (int(right[:,0].min()), int(right[:,1].min())) if len(right) else None
    return lp, rp

def render(g, r0, r1, c0, c1):
    print("     "+"".join(f"{c%10}" for c in range(c0,c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f"{r:3d}  {row}")

env, obs = make_l5()
g = np.array(obs.frame[-1])
lp, rp = block_pos(g)
print(f"L5 start: A={lp}, B={rp}, sum={lp[1]+rp[1]}")
render(g, 44, 60, 0, 63)

print("\n--- LEFT x3 (ACTION3) then UP x1 ---")
for name, act in [
    ("LEFT1 A3", GameAction.ACTION3),
    ("LEFT2 A3", GameAction.ACTION3),
    ("LEFT3 A3", GameAction.ACTION3),
    ("UP    A1", GameAction.ACTION1),
]:
    obs = env.step(act)
    g = np.array(obs.frame[-1])
    lp, rp = block_pos(g)
    s = (lp[1]+rp[1]) if lp and rp else '?'
    print(f"{name}: A={lp}, B={rp}, sum={s}")

print("\nGrid rows 44-60 after sequence:")
render(g, 44, 60, 0, 63)

print("\n--- Now RIGHT ARROW (ACTION4: A tries left, B goes right) repeatedly ---")
for i in range(20):
    obs = env.step(GameAction.ACTION4)
    g = np.array(obs.frame[-1])
    lp, rp = block_pos(g)
    s = (lp[1]+rp[1]) if lp and rp else '?'
    note = " *** SUM > 60 ***" if s > 60 else ""
    print(f"RIGHT {i+1:2d}: A={lp}, B={rp}, sum={s}{note}")
