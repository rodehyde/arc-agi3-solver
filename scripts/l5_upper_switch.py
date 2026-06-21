"""Test whether R occupying the upper-left purple (rows 6-9 cols 14-17)
opens the left-shaft barriers — the symmetric switch hypothesis.
Also tests: can R move left independently when L is blocked at cols 26-29?
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
char = {0: '.', 5: '#', 6: 'p', 7: 'q', 10: 'L', 12: 'O', 14: 'G', 15: 'V'}
val_name = {5:'black', 6:'pink', 7:'lt-pink', 10:'lt-blue',
            12:'orange', 14:'green', 15:'purple'}


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
    for r,c in sorted(interior)[:15]:
        print(f"    [{r},{c}]: {char.get(int(gb[r,c]),'?')}({gb[r,c]})->{char.get(int(ga[r,c]),'?')}({ga[r,c]})")
    return len(interior), trans


def render(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     "+"".join(f"{c%10}" for c in range(c0,c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f"{r:3d}  {row}")


def barrier_status(g):
    lo = {int(g[r,c]) for r in range(38,42) for c in range(10,22)}
    lu = {int(g[r,c]) for r in range(22,26) for c in range(14,26)}
    ro = {int(g[r,c]) for r in range(38,42) for c in range(42,54)}
    ru = {int(g[r,c]) for r in range(22,26) for c in range(42,54)}
    return lo, lu, ro, ru


# ═══════════════════════════════════════════════════════════════════
print("="*65)
print("SECTION 1: Verify connectivity at rows 6-9 and 10-21")
print("="*65)
env0, obs0 = make_l5()
g0 = np.array(obs0.frame[-1])

print("\nCell values at rows 6-9 (checking for black bridge):")
for r in range(6, 10):
    vals = [(c, val_name.get(int(g0[r,c]),'?')) for c in range(0,64) if int(g0[r,c]) != 5]
    blacks = [(c, c+1) for c in range(64) if g0[r,c]==5]
    non_black = [(c, val_name.get(int(g0[r,c]),'?')) for c in range(64) if g0[r,c]!=5]
    print(f"  row {r}: non-black cells = {non_black}")

print("\nCell values at rows 10-21 — any non-black?")
for r in range(10, 22):
    non_black = [(c, val_name.get(int(g0[r,c]),'?')) for c in range(64) if g0[r,c]!=5]
    if non_black:
        print(f"  row {r}: non-black = {non_black}")
    else:
        print(f"  row {r}: all black (cols 2-61)")

render(g0, 0, 12, 0, 63, "\nRows 0-12 full width:")


# ═══════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("SECTION 2: Can R move LEFT independently when L is blocked?")
print("Navigate: DIVERGE x2 (switch ON) + UP x11 (R to top) + DIVERGE until L blocked")
print("Then test: does R continue moving left while L is stuck at cols 26?")
print("="*65)
env1, obs1 = make_l5()

# DIVERGE x2: L on switch
obs1 = env1.step(GameAction.ACTION3)
obs1 = env1.step(GameAction.ACTION3)
g1 = np.array(obs1.frame[-1])
lp1, rp1 = block_pos(g1)
print(f"After DIVERGE x2: L={lp1}, R={rp1}")

# UP x11: R navigates to top, L pinned
for _ in range(11):
    obs1 = env1.step(GameAction.ACTION1)
g1 = np.array(obs1.frame[-1])
lp1, rp1 = block_pos(g1)
print(f"After UP x11: L={lp1}, R={rp1}")

# DIVERGE x3 to move L off switch and toward max position
print("\nDIVERGE sequence (L leaving switch, R navigating left at rows 6-9):")
for i in range(1, 12):
    gb = np.array(obs1.frame[-1])
    obs1 = env1.step(GameAction.ACTION3)
    ga = np.array(obs1.frame[-1])
    lp1, rp1 = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"DIVERGE {i}: L={lp1}, R={rp1}")
    lo, lu, ro, ru = barrier_status(ga)
    print(f"    L-barriers: orange={lo}, green={lu}")
    print(f"    R-barriers: lower={ro}, upper={ru}")
    if n_int == 0:
        print(f"    *** FULLY BLOCKED ***")
        break
    # Check if R is approaching upper purple at cols 14-17
    if rp1 and rp1[1] <= 18:
        print(f"    *** R approaching upper purple! ***")


# ═══════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("SECTION 3: Direct test — R onto upper purple (rows 6-9 cols 14-17)")
print("="*65)
env2, obs2 = make_l5()

# DIVERGE x2 + UP x11 + DIVERGE until L blocked + continue DIVERGE for R
obs2 = env2.step(GameAction.ACTION3)
obs2 = env2.step(GameAction.ACTION3)   # L on switch at (50,14), R at (50,46)
for _ in range(11):
    obs2 = env2.step(GameAction.ACTION1)  # R to (6,46), L pinned
g2 = np.array(obs2.frame[-1])
lp2, rp2 = block_pos(g2)
print(f"After setup (DIVERGE x2 + UP x11): L={lp2}, R={rp2}")

# Now DIVERGE repeatedly to move R left to upper purple
print("\nDIVERGE until R reaches cols 14-17 or is blocked:")
for i in range(1, 20):
    gb = np.array(obs2.frame[-1])
    obs2 = env2.step(GameAction.ACTION3)
    ga = np.array(obs2.frame[-1])
    lp2, rp2 = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"DIVERGE {i}: L={lp2}, R={rp2}")
    lo, lu, ro, ru = barrier_status(ga)
    print(f"    L-barriers (orange/green): {lo}/{lu}")
    # Check if left barriers opened
    if 5 in lo or 5 in lu:
        print(f"    *** LEFT BARRIERS OPENED! orange={lo}, green={lu} ***")
        render(ga, 0, 63, 2, 31, "Full left shaft after R presses upper purple:")
        break
    if n_int == 0:
        print(f"    *** FULLY BLOCKED — both L and R stuck ***")
        break
    if rp2 and rp2[1] <= 14:
        print(f"    *** R is AT upper purple position (cols 14-17)! ***")
        render(ga, 4, 16, 2, 63, "Grid at upper purple region:")
        # Test all actions from this state
        for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
            gb3 = np.array(obs2.frame[-1])
            obs3 = env2.step(getattr(GameAction, f"ACTION{act_num}"))
            ga3 = np.array(obs3.frame[-1])
            lp3, rp3 = block_pos(ga3)
            n3, t3 = full_diff(gb3, ga3, f"  {act_name}: L={lp3}, R={rp3}")
            lo3, lu3, ro3, ru3 = barrier_status(ga3)
            print(f"    L-barriers: orange={lo3}, green={lu3}")
            print(f"    win={obs3.levels_completed > 4}")
            obs2 = obs3
        break

# ═══════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("SECTION 4: Render final state — full grid")
print("="*65)
g_final = np.array(obs2.frame[-1])
lp_f, rp_f = block_pos(g_final)
print(f"Final: L={lp_f}, R={rp_f}")
lo_f, lu_f, ro_f, ru_f = barrier_status(g_final)
print(f"L-shaft barriers: orange={lo_f}, green={lu_f}")
print(f"R-shaft barriers: lower={ro_f}, upper={ru_f}")
render(g_final, 0, 63, 2, 63, "Full grid final state:")

print("\nDone.")
