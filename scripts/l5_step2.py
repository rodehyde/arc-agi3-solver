"""Step 2 probe for m0r0 L5.
Tests every distinct colour when block is physically adjacent.
All claims backed by cell values. Fresh verified instance per section.
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
    """Fresh verified L5 instance. Asserts levels=4 and block positions."""
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
    for act in [GameAction.ACTION4, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
        obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3):
        obs = env.step(GameAction.ACTION4)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    for a in NAV3:
        obs = env.step(AMAP[a])
    for a in 'UU':
        obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})
    for _ in range(3):
        obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})
    for a in 'DDCDCC':
        obs = env.step(AMAP[a])
    # Verify
    assert obs.levels_completed == 4, f"Bad setup: levels={obs.levels_completed}"
    g = np.array(obs.frame[-1])
    lp, rp = block_pos(g)
    assert lp == (50, 6),  f"Bad L pos: {lp}"
    assert rp == (50, 54), f"Bad R pos: {rp}"
    return env, obs


def block_pos(g):
    cells = np.argwhere(g == 10)
    if not len(cells): return None, None
    left  = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    lp = (int(left[:, 0].min()),  int(left[:, 1].min()))  if len(left)  else None
    rp = (int(right[:, 0].min()), int(right[:, 1].min())) if len(right) else None
    return lp, rp


def full_diff(gb, ga, label=""):
    diff = np.argwhere(gb != ga)
    interior = [(int(r), int(c)) for r, c in diff if 1 <= r <= 62 and 1 <= c <= 62]
    trans = {}
    for r, c in diff:
        k = (int(gb[r, c]), int(ga[r, c]))
        trans[k] = trans.get(k, 0) + 1
    trans_str = {f"{val_name.get(a,'?')}({a})->{val_name.get(b,'?')}({b})": n
                 for (a, b), n in trans.items()}
    print(f"\n  {label}")
    print(f"    total={len(diff)}  interior={len(interior)}  transitions={trans_str}")
    for r, c in sorted(interior)[:30]:
        print(f"    [{r},{c}]: {char.get(int(gb[r,c]),'?')}({gb[r,c]})->{char.get(int(ga[r,c]),'?')}({ga[r,c]})")
    return len(interior), trans


def render(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     " + "".join(f"{c % 10}" for c in range(c0, c1 + 1)))
    for r in range(r0, r1 + 1):
        row = "".join(char.get(int(g[r, c]), '?') for c in range(c0, c1 + 1))
        print(f"{r:3d}  {row}")


def probe_a6_with_followup(env, obs, x, y, label):
    """A6 click, then if interior changes, probe all movement actions."""
    gb = np.array(obs.frame[-1])
    avail_before = set(obs.available_actions)
    obs2 = env.step(GameAction.ACTION6, {"x": x, "y": y})
    ga = np.array(obs2.frame[-1])
    avail_after = set(obs2.available_actions)
    n_int, _ = full_diff(gb, ga, f"A6({x},{y}) [{label}]")
    if avail_before != avail_after:
        print(f"    *** AVAILABLE_ACTIONS CHANGED: {avail_before} -> {avail_after} ***")
    if n_int > 0:
        lp_a, rp_a = block_pos(ga)
        print(f"    *** INTERIOR CHANGE DETECTED! L={lp_a}, R={rp_a} ***")
        render(ga, max(0,lp_a[0]-4) if lp_a else 0, 57, 2, 61, "Grid after A6:")
        print("    Follow-up: all movement actions from changed state:")
        for fn, fa in [("U",GameAction.ACTION1),("D",GameAction.ACTION2),
                       ("X",GameAction.ACTION3),("C",GameAction.ACTION4),
                       ("A5",GameAction.ACTION5)]:
            gb2 = np.array(obs2.frame[-1])
            obs3 = env.step(fa)
            ga2 = np.array(obs3.frame[-1])
            lp2, rp2 = block_pos(ga2)
            full_diff(gb2, ga2, f"  -> {fn}: L={lp2}, R={rp2}")
            obs2 = obs3
    return obs2


# ═══════════════════════════════════════════════════════════════════
print("=" * 65)
print("SECTION 1: Verify obstacle cell values (no inference)")
print("=" * 65)
env0, obs0 = make_l5()
g0 = np.array(obs0.frame[-1])

obstacles = [
    ("L purple-upper",  (6,  9), (14, 17)),
    ("L green-barrier", (22, 25), (14, 25)),
    ("L orange-barrier",(38, 41), (10, 21)),
    ("L pink-gap",      (46, 49), (14, 17)),
    ("L purple-lower",  (50, 53), (14, 17)),
    ("R purple-lower",  (38, 41), (42, 53)),
    ("R green",         (26, 29), (34, 37)),
    ("R orange",        (26, 29), (58, 61)),
    ("R purple-upper",  (22, 25), (42, 53)),
]
print("\nObstacle cell value verification:")
for name, (r0, r1), (c0, c1) in obstacles:
    vals = {int(g0[r, c]) for r in range(r0, r1+1) for c in range(c0, c1+1)}
    named = {val_name.get(v, f'?{v}'): v for v in vals}
    print(f"  {name}: rows {r0}-{r1}, cols {c0}-{c1} -> {named}")

print("\nSide-passage check (must be non-black to confirm full blockage):")
checks = [
    ("L orange barrier, left side",  40, range(2, 10)),
    ("L orange barrier, right side", 40, range(22, 30)),
    ("R purple barrier, left side",  40, range(34, 42)),
    ("R purple barrier, right side", 40, range(54, 62)),
    ("L green barrier, left side",   23, range(2, 14)),
    ("L green barrier, right side",  23, range(26, 30)),
    ("R purple upper, left side",    23, range(34, 42)),
    ("R purple upper, right side",   23, range(54, 62)),
]
for name, row, cols in checks:
    vals = {int(g0[row, c]) for c in cols}
    has_black = 5 in vals
    named = {val_name.get(v, f'?{v}'): v for v in vals}
    flag = " *** HAS BLACK — passage exists ***" if has_black else " (confirmed non-black)"
    print(f"  {name} (row {row}): {named}{flag}")

render(g0, 44, 57, 2, 29,  "\nLeft shaft lower (rows 44-57):")
render(g0, 44, 57, 34, 61, "Right shaft lower (rows 44-57):")


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 2: Movement characterization from start")
print("=" * 65)
env_m, obs_m = make_l5()
g_m = np.array(obs_m.frame[-1])
lp0, rp0 = block_pos(g_m)
print(f"Start: L={lp0}, R={rp0}")

print("\nUP sequence (both blocks, track until blocked):")
for i in range(1, 14):
    gb = np.array(obs_m.frame[-1])
    obs_m = env_m.step(GameAction.ACTION1)
    ga = np.array(obs_m.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"UP {i}: L={lp}, R={rp}")
    if not any(5 in k for k in trans):  # only border changes
        print(f"  BLOCKED after UP {i}")
        break

env_x, obs_x = make_l5()
print("\nDIVERGE (ACTION3) sequence from start:")
for i in range(1, 12):
    gb = np.array(obs_x.frame[-1])
    obs_x = env_x.step(GameAction.ACTION3)
    ga = np.array(obs_x.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"DIVERGE {i}: L={lp}, R={rp}")
    blk_moved = any(5 in k for k in trans)
    if not blk_moved:
        print(f"  BLOCKED after DIVERGE {i}")
        break

env_c, obs_c = make_l5()
print("\nCONVERGE (ACTION4) sequence from start:")
for i in range(1, 12):
    gb = np.array(obs_c.frame[-1])
    obs_c = env_c.step(GameAction.ACTION4)
    ga = np.array(obs_c.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"CONVERGE {i}: L={lp}, R={rp}")
    blk_moved = any(5 in k for k in trans)
    if not blk_moved:
        print(f"  BLOCKED after CONVERGE {i}")
        break


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 3: A6 on every distinct object from start")
print("=" * 65)
a6_from_start = [
    ("L-block",          7, 51),
    ("R-block",         55, 51),
    ("L-purple-lower",  15, 51),
    ("L-purple-lower2", 14, 51),
    ("L-pink-gap",      15, 47),
    ("L-purple-upper",  15,  7),
    ("L-green",         19, 23),
    ("L-orange-mid",    15, 39),
    ("L-orange-left",   10, 39),
    ("L-orange-right",  21, 39),
    ("R-purple-lower",  47, 39),
    ("R-purple-upper",  47, 23),
    ("R-green",         35, 27),
    ("R-orange",        59, 27),
    ("black-corridor",  10, 30),
    ("pink-bg",          1, 30),
]
for name, x, y in a6_from_start:
    ev, ob = make_l5()
    probe_a6_with_followup(ev, ob, x, y, name)


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 4: L block adjacent to lower-purple (cols 14-17, rows 50-53)")
print("NAVIGATE: DIVERGE once -> L at cols 10-13")
print("=" * 65)
env4, obs4 = make_l5()
obs4 = env4.step(GameAction.ACTION3)  # DIVERGE: L → cols 10-13
g4 = np.array(obs4.frame[-1])
lp4, rp4 = block_pos(g4)
print(f"After DIVERGE: L={lp4}, R={rp4}")
# Verify purple is still at cols 14-17
vals_purple = {int(g4[r, c]) for r in range(50, 54) for c in range(14, 18)}
print(f"Purple at rows 50-53 cols 14-17: {vals_purple}  (expected {{15}})")
render(g4, 48, 55, 2, 22, "Left lower shaft after 1 DIVERGE:")

print("\nA6 on purple cells (cols 14-17, rows 50-53) with L at cols 10-13:")
for name, x, y in [("purple(14,50)", 14, 50), ("purple(15,50)", 15, 50),
                    ("purple(14,51)", 14, 51), ("purple(15,51)", 15, 51),
                    ("purple(17,51)", 17, 51), ("purple(15,53)", 15, 53)]:
    obs4 = probe_a6_with_followup(env4, obs4, x, y, name)

print("\nAll movement actions with L at cols 10-13 (adjacent to purple):")
for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
    ev, ob = make_l5()
    ob = ev.step(GameAction.ACTION3)  # position L at cols 10-13
    gb = np.array(ob.frame[-1])
    ob2 = ev.step(getattr(GameAction, f"ACTION{act_num}"))
    ga = np.array(ob2.frame[-1])
    lp, rp = block_pos(ga)
    full_diff(gb, ga, f"{act_name}: L->{lp}, R->{rp}")


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 5: L block adjacent to orange barrier (rows 38-41)")
print("NAVIGATE: UP x2 -> L at rows 42-45, cols 6-9")
print("=" * 65)
env5, obs5 = make_l5()
for _ in range(2): obs5 = env5.step(GameAction.ACTION1)
g5 = np.array(obs5.frame[-1])
lp5, rp5 = block_pos(g5)
print(f"After 2 UPs: L={lp5}, R={rp5}")
vals_orange = {int(g5[r, c]) for r in range(38, 42) for c in range(10, 22)}
print(f"Orange at rows 38-41 cols 10-21: {vals_orange}  (expected {{12}})")
render(g5, 36, 47, 2, 29, "Left shaft (L adjacent below orange):")

print("\nA6 on orange cells (rows 38-41, cols 10-21) with L at rows 42-45:")
for name, x, y in [("orange(15,39)",15,39),("orange(10,39)",10,39),("orange(21,39)",21,39),
                    ("orange(15,38)",15,38),("orange(15,41)",15,41),
                    ("orange(10,38)",10,38),("orange(21,41)",21,41)]:
    obs5 = probe_a6_with_followup(env5, obs5, x, y, name)

print("\nAll movement actions from L adjacent to orange (fresh instances):")
for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
    ev, ob = make_l5()
    for _ in range(2): ob = ev.step(GameAction.ACTION1)
    gb = np.array(ob.frame[-1])
    ob2 = ev.step(getattr(GameAction, f"ACTION{act_num}"))
    ga = np.array(ob2.frame[-1])
    lp, rp = block_pos(ga)
    full_diff(gb, ga, f"{act_name} (L at rows 42-45): L->{lp}, R->{rp}")


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 6: R block adjacent to purple barrier (rows 38-41)")
print("NAVIGATE: UP x2 -> R at rows 42-45, cols 54-57")
print("=" * 65)
env6, obs6 = make_l5()
for _ in range(2): obs6 = env6.step(GameAction.ACTION1)
g6 = np.array(obs6.frame[-1])
lp6, rp6 = block_pos(g6)
print(f"After 2 UPs: L={lp6}, R={rp6}")
vals_purp = {int(g6[r, c]) for r in range(38, 42) for c in range(42, 54)}
print(f"Purple at rows 38-41 cols 42-53: {vals_purp}  (expected {{15}})")
render(g6, 36, 47, 34, 61, "Right shaft (R adjacent below purple):")

print("\nA6 on purple cells (rows 38-41, cols 42-53) with R at rows 42-45:")
for name, x, y in [("purple(47,39)",47,39),("purple(42,39)",42,39),("purple(53,39)",53,39),
                    ("purple(47,38)",47,38),("purple(47,41)",47,41),
                    ("purple(42,38)",42,38),("purple(53,41)",53,41)]:
    obs6 = probe_a6_with_followup(env6, obs6, x, y, name)

print("\nAll movement actions from R adjacent to purple (fresh instances):")
for act_name, act_num in [("UP",1),("DOWN",2),("DIVERGE",3),("CONVERGE",4),("A5",5)]:
    ev, ob = make_l5()
    for _ in range(2): ob = ev.step(GameAction.ACTION1)
    gb = np.array(ob.frame[-1])
    ob2 = ev.step(getattr(GameAction, f"ACTION{act_num}"))
    ga = np.array(ob2.frame[-1])
    lp, rp = block_pos(ga)
    full_diff(gb, ga, f"{act_name} (R at rows 42-45): L->{lp}, R->{rp}")


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 7: Navigate L into lower shaft interior at rows 42-45")
print("Test A6 on orange from various horizontal positions (cols 6-26)")
print("=" * 65)
env7, obs7 = make_l5()
for _ in range(2): obs7 = env7.step(GameAction.ACTION1)  # L at (42,6)
# Navigate L rightward via DIVERGE
print("\nNavigating L right while at rows 42-45:")
for i in range(1, 7):
    gb = np.array(obs7.frame[-1])
    obs7 = env7.step(GameAction.ACTION3)  # DIVERGE: L moves right
    ga = np.array(obs7.frame[-1])
    lp, rp = block_pos(ga)
    n_int, trans = full_diff(gb, ga, f"DIVERGE {i}: L={lp}")
    if not any(5 in k for k in trans):
        print(f"  L blocked at {lp}")
        break
    # At each position, test A6 on the orange above
    if lp:
        # Orange is above at rows 38-41 in cols 10-21
        # Test A6 on the orange cell directly above current L col
        orange_x = max(10, min(21, lp[1] + 2))  # orange center col near L
        gb_a6 = np.array(obs7.frame[-1])
        obs_a6 = env7.step(GameAction.ACTION6, {"x": orange_x, "y": 39})
        ga_a6 = np.array(obs_a6.frame[-1])
        n_a6, _ = full_diff(gb_a6, ga_a6, f"  A6({orange_x},39) from L={lp}:")
        if n_a6 > 0: print(f"  *** INTERIOR CHANGE at this position! ***")
        obs7 = obs_a6  # chain state


# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SECTION 8: ACTION5 from various adjacent positions")
print("=" * 65)
positions = [
    ("start",              []),
    ("DIVERGE-1 (L adj purple)", ["X"]),
    ("2-UP (L adj orange)",      ["U","U"]),
    ("2-UP + DIVERGE",           ["U","U","X"]),
    ("2-UP + 3-DIVERGE",         ["U","U","X","X","X"]),
]
for pos_name, nav in positions:
    ev, ob = make_l5()
    for a in nav: ob = ev.step(AMAP[a])
    gb = np.array(ob.frame[-1])
    lp, rp = block_pos(gb)
    ob2 = ev.step(GameAction.ACTION5)
    ga = np.array(ob2.frame[-1])
    n_int, trans = full_diff(gb, ga, f"ACTION5 from {pos_name}: L={lp}")
    if ob.available_actions != ob2.available_actions:
        print(f"  *** AVAILABLE_ACTIONS CHANGED ***")


print("\nDone.")
