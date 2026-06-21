"""Find the exact 2 cells that change on every even-numbered action in L5."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'
char = {0:'.', 1:'a', 5:'#', 6:'p', 7:'q', 8:'R', 9:'B',
        10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}

def setup_l5():
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
    for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]: obs = env.step(act)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    g = np.array(obs.frame[-1])
    bxy3 = next(((c,r) for r in range(30,35) for c in range(38,43) if g[r,c]==9), None)
    obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})
    for a in NAV3: obs = env.step(AMAP[a])
    for a in 'UU': obs = env.step(AMAP[a])
    obs = env.step(GameAction.ACTION6, {"x": 30, "y": 30})
    for _ in range(3): obs = env.step(GameAction.ACTION3)
    obs = env.step(GameAction.ACTION6, {"x": 9, "y": 40})
    for a in 'DDCDCC': obs = env.step(AMAP[a])
    return env, obs

def render_zone(g, r0, r1, c0, c1, label=""):
    if label: print(f"\n{label}")
    print("     " + "".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        print(f"{r:3d}  {row}")

# ── 1. Find exact cells that change on the 2nd action ───────────────────────
print("=== Finding exact cells changed on 2nd action ===")
env1, obs1 = setup_l5()
g0 = np.array(obs1.frame[-1])
obs1 = env1.step(GameAction.ACTION1)  # action 1 (odd) — normal UP
g1 = np.array(obs1.frame[-1])
obs1 = env1.step(GameAction.ACTION5)  # action 2 (even) — should trigger 2-cell change
g2 = np.array(obs1.frame[-1])

diff = np.argwhere(g1 != g2)
print(f"Cells changed on action 2 (A5 after 1 UP):")
for r, c in diff:
    print(f"  [{r},{c}]: {char.get(int(g1[r,c]),'?')}({g1[r,c]}) -> {char.get(int(g2[r,c]),'?')}({g2[r,c]})")

# ── 2. Track the 2-cell changes over many even actions ──────────────────────
print("\n=== Track 2-cell changes across 20 even actions ===")
env2, obs2 = setup_l5()
g_base = np.array(obs2.frame[-1])
changes_seen = {}  # (r,c) -> list of values seen

for i in range(1, 21):
    g_before = np.array(obs2.frame[-1])
    # Alternate: odd=UP/BLOCKED, even=ACTION5
    if i % 2 == 1:
        obs2 = env2.step(GameAction.ACTION5)  # odd action
    else:
        obs2 = env2.step(GameAction.ACTION5)  # even action
    g_after = np.array(obs2.frame[-1])
    diff = np.argwhere(g_before != g_after)
    if len(diff):
        print(f"  Action {i}: {len(diff)} cells changed: " +
              ", ".join(f"[{r},{c}] {g_before[r,c]}->{g_after[r,c]}" for r,c in diff))
        for r, c in diff:
            k = (int(r), int(c))
            changes_seen[k] = changes_seen.get(k, [])
            changes_seen[k].append(int(g_after[r,c]))

print(f"\nAll cell positions that ever changed (over 20 actions):")
for pos, vals in sorted(changes_seen.items()):
    print(f"  {pos}: values seen {vals}")

# ── 3. Render the whole grid after 20 even-action toggles ───────────────────
print("\n=== Grid state after 20 ACTION5s ===")
g_final = np.array(obs2.frame[-1])
diff_from_start = np.argwhere(g_base != g_final)
print(f"Total cells different from L5 start: {len(diff_from_start)}")
for r, c in diff_from_start:
    print(f"  [{r},{c}]: start={g_base[r,c]} now={g_final[r,c]}")

# ── 4. Specifically probe: does ACTION5 ever change non-border cells? ────────
print("\n=== Do changes only happen in border rows/cols? ===")
env3, obs3 = setup_l5()
for _ in range(100):
    g_before = np.array(obs3.frame[-1])
    obs3 = env3.step(GameAction.ACTION5)
    g_after = np.array(obs3.frame[-1])
    diff = np.argwhere(g_before != g_after)
    for r, c in diff:
        r, c = int(r), int(c)
        if 1 <= r <= 62 and 1 <= c <= 62:
            print(f"  *** INTERIOR CELL CHANGED: [{r},{c}] {g_before[r,c]}->{g_after[r,c]} ***")

# ── 5. Test A6 on colored objects AFTER navigating block adjacent ────────────
print("\n\n=== A6 on purple (left-lower) after navigating block adjacent ===")
# Left block at (50,6). After DIVERGE, L=(50,10). Purple at cols 14-17.
# Navigate: DIVERGE to col 10, then A6 on purple at (15,51)
env4, obs4 = setup_l5()
obs4 = env4.step(GameAction.ACTION3)  # DIVERGE: L→(50,10)
g_before = np.array(obs4.frame[-1])
obs4 = env4.step(GameAction.ACTION6, {"x": 15, "y": 51})
g_after = np.array(obs4.frame[-1])
diff = np.argwhere(g_before != g_after)
print(f"A6 purple (15,51) with L at col 10: {len(diff)} cells changed")
for r, c in diff:
    print(f"  [{r},{c}]: {char.get(int(g_before[r,c]),'?')}->{char.get(int(g_after[r,c]),'?')}")

# ── 6. Render the left shaft showing what value 0 cells look like ────────────
print("\n=== Left shaft after 10 A5 presses starting from action 1 ===")
env5, obs5 = setup_l5()
for i in range(10):
    obs5 = env5.step(GameAction.ACTION5)
g5 = np.array(obs5.frame[-1])
white_cells = np.argwhere(g5 == 0)
print(f"White (value=0) cells: {sorted((int(r),int(c)) for r,c in white_cells)}")
render_zone(g5, 0, 5, 0, 63, "Border rows 0-5:")
render_zone(g5, 58, 63, 0, 63, "Border rows 58-63:")

print("\nDone.")
