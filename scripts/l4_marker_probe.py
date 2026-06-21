"""Probe frozen-state marker movement direction and step size for m0r0 L4."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4}
L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'
NAV3 = 'UXXUUUCCCUUXXXXUUUUUCCDDDCCUUUDCUC'

def setup_l4():
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
    return env, obs

def marker_bbox(g):
    """Find bounding box of the blue (9) or yellow (11) marker cells,
    excluding the yellow wall (cols 0-8) and yellow field (rows 0-8)."""
    blue = np.argwhere(g == 9)
    yellow_new = np.argwhere((g == 11) & (np.arange(g.shape[1])[None,:] > 15) & (np.arange(g.shape[0])[:,None] > 15))
    cells = blue if len(blue) else yellow_new
    if not len(cells):
        return None
    return (int(cells[:,0].min()), int(cells[:,1].min()),
            int(cells[:,0].max()), int(cells[:,1].max()))

char = {0:'.', 1:'a', 5:'#', 8:'R', 9:'B', 10:'L', 11:'Y', 15:'V'}

def render_zone(g, r0, r1, c0, c1, label=""):
    if label:
        print(f"\n{label}")
    print("     " + "".join(f"{c%10}" for c in range(c0, c1+1)))
    for r in range(r0, r1+1):
        row = "".join(char.get(int(g[r,c]),'?') for c in range(c0, c1+1))
        print(f"{r:3d}  {row}")

# ── Step 1: confirm blue marker position at L4 start ──────────────────────────
env0, obs0 = setup_l4()
g0 = np.array(obs0.frame[-1])
blue_cells = np.argwhere(g0 == 9)
print("Blue marker cells at L4 start:")
print(f"  {sorted((int(r),int(c)) for r,c in blue_cells)}")
mb = marker_bbox(g0)
print(f"  Bounding box: rows {mb[0]}-{mb[2]}, cols {mb[1]}-{mb[3]}")
render_zone(g0, 27, 36, 25, 38, "Grid around marker (start):")

# ── Step 2: freeze and record marker-yellow position ──────────────────────────
obs_frozen = env0.step(GameAction.ACTION6, {"x": 30, "y": 30})
g_frozen = np.array(obs_frozen.frame[-1])
# Yellow cells that appeared (were blue or black before freeze)
new_yellow = np.argwhere((g_frozen == 11) & (g0 != 11))
print(f"\nAfter freeze: new yellow cells (were not yellow before):")
print(f"  {sorted((int(r),int(c)) for r,c in new_yellow)}")
render_zone(g_frozen, 27, 36, 25, 38, "Grid around marker (frozen):")

# ── Step 3: DIVERGE in frozen state — track marker ────────────────────────────
print("\n\n=== DIVERGE in frozen state ===")
env_d, obs_d = setup_l4()
g_pre = np.array(obs_d.frame[-1])
obs_d = env_d.step(GameAction.ACTION6, {"x": 30, "y": 30})
g_f = np.array(obs_d.frame[-1])
obs_d2 = env_d.step(GameAction.ACTION3)  # DIVERGE
g_after = np.array(obs_d2.frame[-1])

# New yellow cells (that appeared) = new marker position
appeared = np.argwhere((g_after == 11) & (g_f != 11))
disappeared = np.argwhere((g_f == 11) & (g_after != 11) & (g_pre != 11))
print(f"  Marker LEFT (yellow→other): {sorted((int(r),int(c)) for r,c in disappeared)}")
print(f"  Marker ARRIVED (other→yellow): {sorted((int(r),int(c)) for r,c in appeared)}")
if len(disappeared) and len(appeared):
    old_col = int(np.median(disappeared[:,1]))
    new_col = int(np.median(appeared[:,1]))
    old_row = int(np.median(disappeared[:,0]))
    new_row = int(np.median(appeared[:,0]))
    print(f"  Movement: col {old_col} → {new_col} (delta={new_col-old_col}), row {old_row} → {new_row} (delta={new_row-old_row})")
render_zone(g_after, 27, 36, 15, 45, "Grid after DIVERGE (frozen):")

# ── Step 4: CONVERGE in frozen state — track marker ───────────────────────────
print("\n\n=== CONVERGE in frozen state ===")
env_c, obs_c = setup_l4()
g_pre_c = np.array(obs_c.frame[-1])
obs_c = env_c.step(GameAction.ACTION6, {"x": 30, "y": 30})
g_f_c = np.array(obs_c.frame[-1])
obs_c2 = env_c.step(GameAction.ACTION4)  # CONVERGE
g_after_c = np.array(obs_c2.frame[-1])

appeared_c = np.argwhere((g_after_c == 11) & (g_f_c != 11))
disappeared_c = np.argwhere((g_f_c == 11) & (g_after_c != 11) & (g_pre_c != 11))
print(f"  Marker LEFT (yellow→other): {sorted((int(r),int(c)) for r,c in disappeared_c)}")
print(f"  Marker ARRIVED (other→yellow): {sorted((int(r),int(c)) for r,c in appeared_c)}")
if len(disappeared_c) and len(appeared_c):
    old_col_c = int(np.median(disappeared_c[:,1]))
    new_col_c = int(np.median(appeared_c[:,1]))
    old_row_c = int(np.median(disappeared_c[:,0]))
    new_row_c = int(np.median(appeared_c[:,0]))
    print(f"  Movement: col {old_col_c} → {new_col_c} (delta={new_col_c-old_col_c}), row {old_row_c} → {new_row_c} (delta={new_row_c-old_row_c})")
render_zone(g_after_c, 27, 36, 15, 45, "Grid after CONVERGE (frozen):")

# ── Step 5: Multiple DIVERGE steps — measure cumulative range ─────────────────
print("\n\n=== Cumulative DIVERGE steps (how far can marker go left?) ===")
env_multi, obs_multi = setup_l4()
obs_multi = env_multi.step(GameAction.ACTION6, {"x": 30, "y": 30})
g_ref = np.array(obs_multi.frame[-1])
ref_new_yellow = np.argwhere((g_ref == 11) & (np.array(np.array(obs_multi.frame[-1])) == 11))

# Track marker position after each DIVERGE
prev_g = g_ref
for i in range(1, 12):
    obs_multi = env_multi.step(GameAction.ACTION3)  # DIVERGE
    g_curr = np.array(obs_multi.frame[-1])
    new_y = np.argwhere((g_curr == 11) & (prev_g != 11))
    if len(new_y):
        col = int(np.median(new_y[:,1]))
        row = int(np.median(new_y[:,0]))
        print(f"  After {i} DIVERGE: marker centre ~(row={row}, col={col})")
        prev_g = g_curr
    else:
        print(f"  After {i} DIVERGE: marker did not move (at boundary)")
        break

# ── Step 6: Multiple CONVERGE steps — measure cumulative range ────────────────
print("\n\n=== Cumulative CONVERGE steps (how far can marker go right?) ===")
env_multi2, obs_multi2 = setup_l4()
obs_multi2 = env_multi2.step(GameAction.ACTION6, {"x": 30, "y": 30})
prev_g2 = np.array(obs_multi2.frame[-1])
for i in range(1, 12):
    obs_multi2 = env_multi2.step(GameAction.ACTION4)  # CONVERGE
    g_curr2 = np.array(obs_multi2.frame[-1])
    new_y2 = np.argwhere((g_curr2 == 11) & (prev_g2 != 11))
    if len(new_y2):
        col2 = int(np.median(new_y2[:,1]))
        row2 = int(np.median(new_y2[:,0]))
        print(f"  After {i} CONVERGE: marker centre ~(row={row2}, col={col2})")
        prev_g2 = g_curr2
    else:
        print(f"  After {i} CONVERGE: marker did not move (at boundary)")
        break

print("\nDone.")
