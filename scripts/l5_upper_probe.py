"""Probe right-shaft upper section objects (green/orange at rows 26-29)
when R is physically adjacent, accessible via L pressing the pressure switch.
Also renders the full grid with barriers open for clarity.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
char = {0: '.', 5: '#', 6: 'p', 7: 'q', 8: 'R', 9: 'B',
        10: 'L', 12: 'O', 14: 'G', 15: 'V'}
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
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    left = cells[cells[:,1] < 32]
    right = cells[cells[:,1] >= 32]
    lp = (int(left[:,0].min()), int(left[:,1].min())) if len(left) else None
    rp = (int(right[:,0].min()), int(right[:,1].min())) if len(right) else None
    assert lp == (50, 6) and rp == (50, 54), f"Bad positions L={lp} R={rp}"
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
    print(f"    total={len(diff)}  interior={len(interior)}  transitions={trans_str}")
    for r,c in sorted(interior)[:20]:
        print(f"    [{r},{c}]: {char.get(int(gb[r,c]),'?')}({gb[r,c]})->{char.get(int(ga[r,c]),'?')}({ga[r,c]})")
    return len(interior), trans


def render(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     "+"".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0,c1+1))
        print(f"{r:3d}  {row}")


# ── Setup: activate pressure switch (DIVERGE x2) ─────────────────────────
print("="*65)
print("Setup: L on pressure switch, right-shaft barriers open")
print("="*65)
env, obs = make_l5()

# DIVERGE x2: L moves to cols 14-17, right barriers open
obs = env.step(GameAction.ACTION3)  # DIVERGE 1: L=(50,10), R=(50,50)
obs = env.step(GameAction.ACTION3)  # DIVERGE 2: L=(50,14), R=(50,46) — switch ON

g = np.array(obs.frame[-1])
lp, rp = block_pos(g)
print(f"After DIVERGE x2: L={lp}, R={rp}")
print(f"Available actions: {obs.available_actions}")

# Verify switch is active: check right-shaft barriers are black
barrier_lower_vals = {int(g[r,c]) for r in range(38,42) for c in range(42,54)}
barrier_upper_vals = {int(g[r,c]) for r in range(22,26) for c in range(42,54)}
print(f"Right lower barrier (rows 38-41, cols 42-53): {barrier_lower_vals}  (black=open?)")
print(f"Right upper barrier (rows 22-25, cols 42-53): {barrier_upper_vals}  (black=open?)")
left_barrier_orange = {int(g[r,c]) for r in range(38,42) for c in range(10,22)}
left_barrier_green  = {int(g[r,c]) for r in range(22,26) for c in range(14,26)}
print(f"Left lower barrier orange (rows 38-41, cols 10-21): {left_barrier_orange}")
print(f"Left upper barrier green  (rows 22-25, cols 14-25): {left_barrier_green}")

render(g, 20, 44, 34, 63, "\nRight shaft with barriers open:")
render(g, 20, 44, 2, 31,  "Left shaft with switch pressed:")


# ── Navigate R up to rows 26-29 via selective UPs ────────────────────────
print("\n"+"="*65)
print("Navigate R up to rows 26-29 (L pinned by pink gap)")
print("="*65)
print("\nUP sequence (L should stay pinned at rows 50-53 cols 14-17):")
for i in range(1, 7):
    gb = np.array(obs.frame[-1])
    obs = env.step(GameAction.ACTION1)  # UP
    ga = np.array(obs.frame[-1])
    lp2, rp2 = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"UP {i}: L={lp2}, R={rp2}")
    # Check if barriers still open
    left_open = {int(ga[r,c]) for r in range(38,42) for c in range(10,22)}
    right_open = {int(ga[r,c]) for r in range(38,42) for c in range(42,54)}
    print(f"    L-barrier: {left_open}, R-barrier: {right_open}")
    if rp2 and rp2[0] <= 26:
        print(f"    R reached rows 26-29!")
        break

g_at_26 = np.array(obs.frame[-1])
lp_26, rp_26 = block_pos(g_at_26)
print(f"\nCurrent: L={lp_26}, R={rp_26}")
render(g_at_26, 22, 32, 34, 63, "Right shaft upper section with R at rows 26-29:")
render(g_at_26, 22, 32, 2, 31, "Left shaft upper section:")

# Verify what values are at rows 26-29 in right shaft
print("\nCell values at rows 26-29 right shaft:")
for r in range(26, 30):
    row_vals = [(c, int(g_at_26[r,c])) for c in range(34,62)]
    print(f"  row {r}: {[(c,v) for c,v in row_vals if v != 5]}")  # non-black only


# ── Test all actions from R at rows 26-29 ────────────────────────────────
print("\n"+"="*65)
print("Test all actions from R at rows 26-29 (L pinned on switch)")
print("="*65)
for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
    # Fresh instance for each
    ev, ob = make_l5()
    ob = ev.step(GameAction.ACTION3)
    ob = ev.step(GameAction.ACTION3)   # L on switch, barriers open
    for _ in range(6): ob = ev.step(GameAction.ACTION1)  # R to rows 26-29
    gb = np.array(ob.frame[-1])
    lp_t, rp_t = block_pos(gb)
    ob2 = ev.step(getattr(GameAction, f"ACTION{act_num}"))
    ga = np.array(ob2.frame[-1])
    lp2, rp2 = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"{act_name} from L={lp_t}, R={rp_t}: -> L={lp2}, R={rp2}")
    # Check left barriers
    left_lower_after = {int(ga[r,c]) for r in range(38,42) for c in range(10,22)}
    left_upper_after = {int(ga[r,c]) for r in range(22,26) for c in range(14,26)}
    print(f"    Left lower barrier after: {left_lower_after}")
    print(f"    Left upper barrier after: {left_upper_after}")


# ── A6 on right-shaft green when R is adjacent ───────────────────────────
print("\n"+"="*65)
print("A6 on right-shaft green (rows 26-29, cols 34-37) with R adjacent")
print("="*65)
# After 6 UPs, R is at rows 26-29. Green is at rows 26-29 cols 34-37.
# R is at cols 46-49 — not immediately adjacent but in same rows.
# Test A6 on every cell of the green block.
ev, ob = make_l5()
ob = ev.step(GameAction.ACTION3)
ob = ev.step(GameAction.ACTION3)
for _ in range(6): ob = ev.step(GameAction.ACTION1)
g_base = np.array(ob.frame[-1])
lp_b, rp_b = block_pos(g_base)
print(f"Position: L={lp_b}, R={rp_b}")

for name, x, y in [("green(34,26)",34,26),("green(35,27)",35,27),("green(36,27)",36,27),
                    ("green(37,27)",37,27),("green(35,26)",35,26),("green(35,28)",35,28),
                    ("green(35,29)",35,29)]:
    gb = np.array(ob.frame[-1])
    avail_before = set(ob.available_actions)
    ob2 = ev.step(GameAction.ACTION6, {"x": x, "y": y})
    ga = np.array(ob2.frame[-1])
    avail_after = set(ob2.available_actions)
    n_int, trans = full_diff(gb, ga, f"A6({x},{y}) [{name}]:")
    left_lower = {int(ga[r,c]) for r in range(38,42) for c in range(10,22)}
    left_upper = {int(ga[r,c]) for r in range(22,26) for c in range(14,26)}
    print(f"    Left lower barrier: {left_lower}  Left upper barrier: {left_upper}")
    if avail_before != avail_after:
        print(f"    *** AVAILABLE_ACTIONS CHANGED: {avail_before} -> {avail_after} ***")
    if n_int > 0:
        print(f"    *** INTERIOR CHANGE ***")
        render(ga, 20, 44, 2, 63, "Full grid after A6:")
    ob = ob2


# ── A6 on right-shaft orange when R is adjacent ──────────────────────────
print("\n"+"="*65)
print("A6 on right-shaft orange (rows 26-29, cols 58-61) with R in same rows")
print("="*65)
ev2, ob2_start = make_l5()
ob2_start = ev2.step(GameAction.ACTION3)
ob2_start = ev2.step(GameAction.ACTION3)
for _ in range(6): ob2_start = ev2.step(GameAction.ACTION1)
g_b2 = np.array(ob2_start.frame[-1])
lp_o, rp_o = block_pos(g_b2)
print(f"Position: L={lp_o}, R={rp_o}")

ob_cur = ob2_start
for name, x, y in [("orange(59,27)",59,27),("orange(58,27)",58,27),("orange(61,27)",61,27),
                    ("orange(59,26)",59,26),("orange(59,29)",59,29)]:
    gb = np.array(ob_cur.frame[-1])
    avail_before = set(ob_cur.available_actions)
    ob_next = ev2.step(GameAction.ACTION6, {"x": x, "y": y})
    ga = np.array(ob_next.frame[-1])
    avail_after = set(ob_next.available_actions)
    n_int, trans = full_diff(gb, ga, f"A6({x},{y}) [{name}]:")
    left_lower = {int(ga[r,c]) for r in range(38,42) for c in range(10,22)}
    left_upper = {int(ga[r,c]) for r in range(22,26) for c in range(14,26)}
    print(f"    Left lower barrier: {left_lower}  Left upper barrier: {left_upper}")
    if avail_before != avail_after:
        print(f"    *** AVAILABLE_ACTIONS CHANGED ***")
    if n_int > 0:
        print(f"    *** INTERIOR CHANGE ***")
        render(ga, 20, 44, 2, 63, "Full grid after A6:")
    ob_cur = ob_next


# ── Navigate R all the way to rows 6-9, check for win ────────────────────
print("\n"+"="*65)
print("Navigate R to rows 6-9 (top of right shaft): check for win/change")
print("="*65)
ev3, ob3 = make_l5()
ob3 = ev3.step(GameAction.ACTION3)
ob3 = ev3.step(GameAction.ACTION3)  # L on switch
print("Pressing UP until R is blocked at top:")
for i in range(1, 16):
    gb3 = np.array(ob3.frame[-1])
    ob3 = ev3.step(GameAction.ACTION1)
    ga3 = np.array(ob3.frame[-1])
    lp3, rp3 = block_pos(ga3)
    n_int3, _ = full_diff(gb3, ga3, f"UP {i}: L={lp3}, R={rp3}")
    print(f"    levels_completed={ob3.levels_completed}  win={ob3.levels_completed > 4}")
    if n_int3 == 0:
        print(f"    BLOCKED")
        break

g3_final = np.array(ob3.frame[-1])
lp3f, rp3f = block_pos(g3_final)
print(f"\nFinal: L={lp3f}, R={rp3f}")
render(g3_final, 0, 15, 2, 63, "Top section with R at maximum UP:")

# Now probe all actions from this state
print("\nAll actions from top state (L pinned, R at top):")
for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
    gb = np.array(ob3.frame[-1])
    ob_t = ev3.step(getattr(GameAction, f"ACTION{act_num}"))
    ga = np.array(ob_t.frame[-1])
    lp_t2, rp_t2 = block_pos(ga)
    n_int4, trans4 = full_diff(gb, ga, f"{act_name}: L={lp_t2}, R={rp_t2}")
    left_lower_t = {int(ga[r,c]) for r in range(38,42) for c in range(10,22)}
    left_upper_t = {int(ga[r,c]) for r in range(22,26) for c in range(14,26)}
    print(f"    Left lower: {left_lower_t}  Left upper: {left_upper_t}")
    print(f"    win={ob_t.levels_completed > 4}")
    ob3 = ob_t


print("\nDone.")
