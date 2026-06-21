"""Complete L3 solution for m0r0.
Moves all 3 blue markers, then navigates blocks to win.
Win path (after markers): UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'

char = {0: '.', 1: 'a', 5: '#', 8: 'R', 9: 'B', 10: 'L', 11: 'Y', 15: 'V'}

def get_state(obs):
    g = np.array(obs.frame[-1])
    cells = np.argwhere(g == 10)
    if not len(cells): return None
    left = cells[cells[:, 1] < 32]
    right = cells[cells[:, 1] >= 32]
    if not len(left) or not len(right): return None
    return (int(left[:, 0].min()), int(left[:, 1].min()),
            int(right[:, 0].min()), int(right[:, 1].min()))

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('m0r0')
obs = env.observation_space

# ── L1 replay ─────────────────────────────────────────────────────────────────
print("Replaying L1...")
for a in L1:
    obs = env.step(AMAP[a])
print(f"  levels_completed={obs.levels_completed}")

# ── L2 replay ─────────────────────────────────────────────────────────────────
print("Replaying L2...")
for a in L2:
    obs = env.step(AMAP[a])
print(f"  levels_completed={obs.levels_completed}")

# ── L3: move Blue-1 ───────────────────────────────────────────────────────────
print("\nMoving Blue-1 (RIGHT, UP, RIGHT×4, DOWN×3, LEFT×2, UP×1)...")
g = np.array(obs.frame[-1])
obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})  # freeze Blue-1
for act in [GameAction.ACTION4,                              # RIGHT
            GameAction.ACTION1,                              # UP
            GameAction.ACTION4, GameAction.ACTION4,
            GameAction.ACTION4, GameAction.ACTION4,          # RIGHT×4
            GameAction.ACTION2, GameAction.ACTION2,
            GameAction.ACTION2,                              # DOWN×3
            GameAction.ACTION3, GameAction.ACTION3,          # LEFT×2
            GameAction.ACTION1]:                             # UP×1
    obs = env.step(act)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})  # restore
g = np.array(obs.frame[-1])
b1_cells = np.argwhere(g == 9)
b1_cul = b1_cells[(b1_cells[:, 0] >= 18) & (b1_cells[:, 0] <= 22) &
                   (b1_cells[:, 1] >= 40) & (b1_cells[:, 1] <= 50)]
print(f"  Blue-1 at cul-de-sac: {sorted((int(r), int(c)) for r, c in b1_cul)}")

# ── L3: move Blue-2 ───────────────────────────────────────────────────────────
print("\nMoving Blue-2 (UP, RIGHT, UP)...")
bxy2 = next(((c, r) for r in range(18, 23) for c in range(10, 15) if g[r, c] == 9), None)
print(f"  Blue-2 found at {bxy2}")
obs = env.step(GameAction.ACTION6, {"x": bxy2[0], "y": bxy2[1]})  # freeze
for act in [GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION1]:
    obs = env.step(act)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})  # restore
g = np.array(obs.frame[-1])
b2_cul = np.argwhere(g == 9)
b2_top = b2_cul[b2_cul[:, 0] <= 14]
print(f"  Blue-2 at rows 10-14: {sorted((int(r), int(c)) for r, c in b2_top)}")

# ── L3: move Blue-3 ───────────────────────────────────────────────────────────
print("\nMoving Blue-3 (RIGHT×3)...")
bxy3 = next(((c, r) for r in range(30, 35) for c in range(38, 43) if g[r, c] == 9), None)
print(f"  Blue-3 found at {bxy3}")
obs = env.step(GameAction.ACTION6, {"x": bxy3[0], "y": bxy3[1]})  # freeze
for _ in range(3):
    obs = env.step(GameAction.ACTION4)
obs = env.step(GameAction.ACTION6, {"x": 14, "y": 46})  # restore
g = np.array(obs.frame[-1])
b3_area = np.argwhere(g == 9)
b3_placed = b3_area[(b3_area[:, 0] >= 29) & (b3_area[:, 0] <= 34)]
print(f"  Blue-3 placed: {sorted((int(r), int(c)) for r, c in b3_placed)}")

# ── Central passage check ──────────────────────────────────────────────────────
blue_in_passage = [(r, c) for r in range(14, 18) for c in range(26, 38) if g[r, c] == 9]
print(f"\nCentral passage clear: {len(blue_in_passage) == 0}  (markers={blue_in_passage})")

# ── L3: navigate blocks to win ────────────────────────────────────────────────
print(f"\nNavigating blocks with path: '{NAV}' ({len(NAV)} actions)...")
s0 = get_state(obs)
print(f"  Start: L({s0[0]},{s0[1]}) R({s0[2]},{s0[3]})")

for i, a in enumerate(NAV):
    obs = env.step(AMAP[a])
    if obs.levels_completed > 2:
        print(f"\n*** LEVEL 3 COMPLETE at action {i+1} ('{a}')! ***")
        print(f"    levels_completed={obs.levels_completed}")
        break
else:
    sf = get_state(obs)
    print(f"  End state: L({sf[0]},{sf[1]}) R({sf[2]},{sf[3]})")
    print(f"  levels_completed={obs.levels_completed}")
    if obs.levels_completed > 2:
        print("\n*** LEVEL 3 COMPLETE! ***")
    else:
        print("\nWin not detected in NAV path — check sequence.")

print(f"\nFinal: win_levels={obs.win_levels}, levels_completed={obs.levels_completed}")
if obs.levels_completed >= obs.win_levels:
    print("GAME COMPLETE!")
