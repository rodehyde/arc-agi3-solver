"""Test whether R physically occupying the right-shaft side markers
(green rows 26-29 cols 34-37, orange rows 26-29 cols 58-61) opens left barriers.
Also confirms whether those markers are traversable or solid walls.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
val_name = {5:'black', 6:'pink', 7:'lt-pink', 10:'lt-blue',
            12:'orange', 14:'green', 15:'purple', 0:'?'}
char = {0: '.', 5: '#', 6: 'p', 7: 'q', 10: 'L', 12: 'O', 14: 'G', 15: 'V'}


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
    lp = (int(left[:,0].min()),  int(left[:,1].min())) if len(left)  else None
    rp = (int(right[:,0].min()), int(right[:,1].min())) if len(right) else None
    return lp, rp


def full_diff(gb, ga, label=""):
    diff = np.argwhere(gb != ga)
    interior = [(int(r),int(c)) for r,c in diff if 1<=r<=62 and 1<=c<=62]
    trans = {}
    for r,c in diff:
        k = (int(gb[r,c]), int(ga[r,c]))
        trans[k] = trans.get(k,0) + 1
    trans_str = {f"{val_name.get(a,'?')}({a})->{val_name.get(b,'?')}({b})": n
                 for (a,b),n in trans.items()}
    if label: print(f"\n  {label}")
    print(f"    total={len(diff)}  interior={len(interior)}  trans={trans_str}")
    return len(interior), trans


def barrier_status(g):
    lo = {int(g[r,c]) for r in range(38,42) for c in range(10,22)}
    lu = {int(g[r,c]) for r in range(22,26) for c in range(14,26)}
    print(f"    L-orange-barrier(rows38-41,cols10-21): {lo}")
    print(f"    L-green-barrier(rows22-25,cols14-25): {lu}")
    return lo, lu


def render_region(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     " + "".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        print(f"{r:3d}  {row}")


# ═══════════════════════════════════════════════════════════════════
print("="*65)
print("SECTION 1: Can R physically reach green side marker (cols 34-37 rows 26-29)?")
print("Route: DIVERGE x2 (L on switch), UP x6 (R to rows 26), then DIVERGE x3 to cols 34")
print("="*65)
env1, obs1 = make_l5()
obs1 = env1.step(GameAction.ACTION3)  # DIVERGE 1
obs1 = env1.step(GameAction.ACTION3)  # DIVERGE 2: L=(50,14) on switch, R=(50,46)
for _ in range(6):
    obs1 = env1.step(GameAction.ACTION1)  # UP x6: R to rows 26, L stays
g = np.array(obs1.frame[-1])
lp, rp = block_pos(g)
print(f"After DIVERGE x2 + UP x6: L={lp}, R={rp}")
print(f"Right barriers (rows 22-25 cols 42-53): {set(int(g[r,c]) for r in range(22,26) for c in range(42,54))}")

# Now DIVERGE to move R left toward green (34-37) — this also releases L from switch
print("\nDIVERGE x3 to move R toward green marker:")
for i in range(1, 5):
    gb = np.array(obs1.frame[-1])
    obs1 = env1.step(GameAction.ACTION3)
    ga = np.array(obs1.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"DIVERGE {i}: L={lp}, R={rp}")
    barrier_status(ga)
    if 'green(14)->lt-blue(10)' in {f"{val_name.get(a,'?')}({a})->{val_name.get(b,'?')}({b})": n for (a,b),n in trans.items()}:
        print(f"    *** R IS ON GREEN SIDE MARKER ***")
        render_region(ga, 22, 32, 30, 63, "Upper right shaft + green marker:")
        # Test all actions from this state
        print("\n  Testing all actions from R-on-green state:")
        for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
            gb3 = np.array(obs1.frame[-1])
            obs1_t = env1.step(getattr(GameAction, f"ACTION{act_num}"))
            ga3 = np.array(obs1_t.frame[-1])
            lp3, rp3 = block_pos(ga3)
            n3, t3 = full_diff(gb3, ga3, f"  {act_name}: L={lp3}, R={rp3}")
            barrier_status(ga3)
            print(f"    win={obs1_t.levels_completed > 4}")
        break
    if n_int == 0:
        print(f"    *** FULLY BLOCKED ***")
        break


# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("SECTION 2: Can R physically reach orange side marker (cols 58-61 rows 26-29)?")
print("Route: DIVERGE x2, UP x6, then CONVERGE x3 to cols 58")
print("="*65)
env2, obs2 = make_l5()
obs2 = env2.step(GameAction.ACTION3)  # DIVERGE 1
obs2 = env2.step(GameAction.ACTION3)  # DIVERGE 2: L=(50,14) on switch, R=(50,46)
for _ in range(6):
    obs2 = env2.step(GameAction.ACTION1)  # UP x6: R to rows 26, L stays
g = np.array(obs2.frame[-1])
lp, rp = block_pos(g)
print(f"After DIVERGE x2 + UP x6: L={lp}, R={rp}")

print("\nCONVERGE x3 to move R toward orange marker:")
for i in range(1, 5):
    gb = np.array(obs2.frame[-1])
    obs2 = env2.step(GameAction.ACTION4)  # CONVERGE: L goes left, R goes right
    ga = np.array(obs2.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"CONVERGE {i}: L={lp}, R={rp}")
    barrier_status(ga)
    if 'orange(12)->lt-blue(10)' in {f"{val_name.get(a,'?')}({a})->{val_name.get(b,'?')}({b})": n for (a,b),n in trans.items()}:
        print(f"    *** R IS ON ORANGE SIDE MARKER ***")
        render_region(ga, 22, 40, 30, 63, "Upper right shaft + orange marker:")
        # Test all actions from this state
        print("\n  Testing all actions from R-on-orange state:")
        for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
            gb3 = np.array(obs2.frame[-1])
            obs2_t = env2.step(getattr(GameAction, f"ACTION{act_num}"))
            ga3 = np.array(obs2_t.frame[-1])
            lp3, rp3 = block_pos(ga3)
            n3, t3 = full_diff(gb3, ga3, f"  {act_name}: L={lp3}, R={rp3}")
            barrier_status(ga3)
            print(f"    win={obs2_t.levels_completed > 4}")
        break
    if n_int == 0:
        print(f"    *** BLOCKED — R cannot enter orange ***")
        break


# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("SECTION 3: Check cell values at rows 26-33 cols 34-61 (the side marker zone)")
print("="*65)
env3, obs3 = make_l5()
g3 = np.array(obs3.frame[-1])
print("\nCell values in rows 26-33, cols 34-61:")
for r in range(26, 34):
    vals = [(c, val_name.get(int(g3[r,c]),'?')) for c in range(34, 62) if g3[r,c] != 5]
    print(f"  row {r}: non-black = {vals}")

render_region(g3, 22, 42, 30, 63, "\nRight shaft rows 22-42 (side markers visible):")


# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("SECTION 4: A5 while L is on switch (unexplored)")
print("="*65)
env4, obs4 = make_l5()
obs4 = env4.step(GameAction.ACTION3)
obs4 = env4.step(GameAction.ACTION3)  # L on switch (50,14), R at (50,46)
g4 = np.array(obs4.frame[-1])
lp4, rp4 = block_pos(g4)
print(f"State: L={lp4}, R={rp4}")
print(f"L-barriers: {set(int(g4[r,c]) for r in range(38,42) for c in range(10,22))}")
gb4 = np.array(obs4.frame[-1])
obs4 = env4.step(GameAction.ACTION5)
ga4 = np.array(obs4.frame[-1])
lp4, rp4 = block_pos(ga4)
n4, t4 = full_diff(gb4, ga4, f"A5 while L on switch: L={lp4}, R={rp4}")
barrier_status(ga4)

# Also test A5 while L is on switch + R is at rows 26
print("\n  A5 while L on switch + R at rows 26:")
env4b, obs4b = make_l5()
obs4b = env4b.step(GameAction.ACTION3)
obs4b = env4b.step(GameAction.ACTION3)  # L on switch
for _ in range(6): obs4b = env4b.step(GameAction.ACTION1)  # R to rows 26
g4b = np.array(obs4b.frame[-1])
lp4b, rp4b = block_pos(g4b)
print(f"  State: L={lp4b}, R={rp4b}")
gb4b = np.array(obs4b.frame[-1])
obs4b = env4b.step(GameAction.ACTION5)
ga4b = np.array(obs4b.frame[-1])
lp4b, rp4b = block_pos(ga4b)
n4b, t4b = full_diff(gb4b, ga4b, f"A5: L={lp4b}, R={rp4b}")
barrier_status(ga4b)
print(f"  win={obs4b.levels_completed > 4}")

print("\nDone.")
