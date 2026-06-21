"""Test winning configurations for tn36 L1.
Key insight: need F5 = tile(1,4) = Pattern A home position.
From initial (D-h,D-v,E-h,E-v=black, F5=(3,4)), need delta=(-2,0).
The 4 combinations that give (-2,0):
  1. Remove D-h + D-v (toggle both D off)
  2. Remove E-h + E-v (toggle both E off)
  3. Remove D-h + E-v
  4. Remove D-v + E-h
Also test: win WITHOUT oval click, and oval click variants.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

char = {0:'.',1:'f',3:'d',4:'v',5:'#',9:'B',10:'L',11:'Y'}

PIECES = {
    "A-h": (42, 26), "A-v": (45, 26),
    "B-h": (42, 36), "B-v": (45, 36),
    "C-h": (42, 41), "C-v": (45, 41),
    "D-h": (42, 21), "D-v": (45, 21),
    "E-h": (42, 31), "E-v": (45, 31),
}

def fresh():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    return env, obs

def click(env, name_or_pos, is_oval=False):
    if is_oval:
        col, row = 36, 55
    elif isinstance(name_or_pos, str):
        row, col = PIECES[name_or_pos]
    else:
        row, col = name_or_pos
    return env.step(GameAction.ACTION6, {'x': col, 'y': row})

def read_f5_tile(obs_oval):
    frames = obs_oval.frame
    if len(frames) < 7: return None, None
    g6 = np.array(frames[6])
    yellow_rest = set(map(tuple, np.argwhere(g6 == 11).tolist()))
    gf5 = np.array(frames[5])
    yellow_f5 = set(map(tuple, np.argwhere(gf5 == 11).tolist()))
    displaced = yellow_f5 - yellow_rest
    if not displaced:
        return None, None  # Pattern A at home or off-screen
    rows = [r for r,c in displaced]
    cols = [c for r,c in displaced]
    r_min, c_min = min(rows), min(cols)
    return (r_min-9)//4, (c_min-14)//4

def test(toggles_off, desc):
    """Toggle specified pieces OFF (black→lt-grey), then click oval."""
    env, obs = fresh()
    for name in toggles_off:
        click(env, name)
    obs_oval = click(env, None, is_oval=True)
    f5 = read_f5_tile(obs_oval)
    won = obs_oval.levels_completed > 0
    n_clicks = len(toggles_off) + 1
    print(f"  {desc}: F5={f5}  WON={won}  clicks={n_clicks}")
    if won:
        print(f"    *** LEVEL COMPLETE! Actions used: {n_clicks} ***")
    return won, n_clicks

def test_no_oval(toggles_off, desc):
    """Toggle specified pieces OFF — no oval click."""
    env, obs = fresh()
    for name in toggles_off:
        obs = click(env, name)
    won = obs.levels_completed > 0
    print(f"  {desc} (no oval): WON={won}")
    return won

print("="*60)
print("COMBINATIONS GIVING F5=tile(1,4) — target=Pattern A home")
print("="*60)
test(["D-h","D-v"], "Remove full D group")
test(["E-h","E-v"], "Remove full E group")
test(["D-h","E-v"], "Remove D-h + E-v")
test(["D-v","E-h"], "Remove D-v + E-h")

print("\n" + "="*60)
print("SAME WITHOUT OVAL — does toggle alone win?")
print("="*60)
test_no_oval(["D-h","D-v"], "Remove full D group")
test_no_oval(["E-h","E-v"], "Remove full E group")
test_no_oval(["D-h","E-v"], "Remove D-h + E-v")
test_no_oval(["D-v","E-h"], "Remove D-v + E-h")

print("\n" + "="*60)
print("WHAT FRAME POSITIONS DO THESE SHOW?")
print("="*60)
for combo, desc in [
    (["D-h","D-v"], "D removed"),
    (["E-h","E-v"], "E removed"),
    (["D-h","E-v"], "D-h+E-v removed"),
]:
    env, obs = fresh()
    for name in combo:
        click(env, name)
    obs_oval = click(env, None, is_oval=True)
    frames = obs_oval.frame
    g6 = np.array(frames[6])
    yellow_rest = set(map(tuple, np.argwhere(g6 == 11).tolist()))
    print(f"\n  [{desc}]")
    for fi in range(1, 7):
        gf = np.array(frames[fi])
        yellow_f = set(map(tuple, np.argwhere(gf == 11).tolist()))
        displaced = yellow_f - yellow_rest
        if displaced:
            rows = [r for r,c in displaced]; cols = [c for r,c in displaced]
            r_min, c_min = min(rows), min(cols)
            tile = ((r_min-9)//4, (c_min-14)//4)
            print(f"    Frame {fi}: Pattern A at tile{tile} = rows {r_min}-{r_min+3} cols {c_min}-{c_min+3}")
        else:
            print(f"    Frame {fi}: (no displacement = Pattern A at home or off-screen)")

print("\n" + "="*60)
print("BRUTE FORCE — 1-click combinations that win")
print("="*60)
all_pieces = list(PIECES.keys())
# Test each single toggle + oval
for name in all_pieces:
    env, obs = fresh()
    click(env, name)
    obs_oval = click(env, None, is_oval=True)
    if obs_oval.levels_completed > 0:
        print(f"  WINNER: toggle {name} then oval!")

print("  (done checking 1-click combos)")

# Test 2-click combos
print("\n2-click combos (all pairs):")
from itertools import combinations
winners_2 = []
for p1, p2 in combinations(all_pieces, 2):
    env, obs = fresh()
    click(env, p1); click(env, p2)
    obs_oval = click(env, None, is_oval=True)
    if obs_oval.levels_completed > 0:
        winners_2.append((p1, p2, 3))  # 2 toggles + 1 oval = 3 actions
        print(f"  WINNER: toggle {p1} + {p2} then oval! (3 actions total)")

if not winners_2:
    print("  (no 2-click winners found)")
