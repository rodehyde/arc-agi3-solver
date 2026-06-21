"""Inspect all animation frames returned after clicking the blue oval.
The API returns 7 frames; I've been using only frame[-1] (final/resting state).
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

char = {0:'.',1:'f',3:'d',4:'v',5:'#',9:'B',10:'L',11:'Y',12:'O'}

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs0 = env.observation_space
g0 = np.array(obs0.frame[0])  # initial state (1 layer)

print(f"Initial: {len(obs0.frame)} layers")

# Click the oval
obs1 = env.step(GameAction.ACTION6, {'x': 36, 'y': 55})
print(f"After oval click: {len(obs1.frame)} layers")
print()

def render_frame(g, label=''):
    """Print the full interesting region of a frame."""
    if label: print(f"\n  [{label}]")
    # Full grid
    for r in range(0, 64):
        row = ''.join(char.get(int(g[r,c]),'?') for c in range(0,64))
        if any(c != '.' for c in row):
            print(f"  {r:2d}: {row}")

def diff_frames(g_base, g_new, label=''):
    """Show what changed between two frames."""
    changed = np.argwhere(g_base != g_new)
    if not len(changed):
        print(f"  {label}: NO CHANGE from base")
        return
    trans = {}
    for r,c in changed:
        k = (int(g_base[r,c]), int(g_new[r,c]))
        trans[k] = trans.get(k,0) + 1
    cells = sorted([(int(r),int(c)) for r,c in changed])
    print(f"  {label}: {len(changed)} cells — {trans}")
    # Show by region
    bar = [(r,c) for r,c in cells if r==1]
    oval = [(r,c) for r,c in cells if 50<=r<=62 and 28<=c<=44]
    legend = [(r,c) for r,c in cells if 41<=r<=47]
    grid = [(r,c) for r,c in cells if 9<=r<=40 and 14<=c<=50]
    if bar: print(f"    BAR: {len(bar)} cells at cols {[c for r,c in bar]}")
    if oval: print(f"    OVAL: {len(oval)} cells ({trans})")
    if legend:
        print(f"    LEGEND: {len(legend)} cells at {legend}")
    if grid:
        print(f"    GRID (main): {len(grid)} cells at {grid}")

print("="*60)
print("EACH ANIMATION FRAME vs INITIAL STATE")
print("="*60)
for i, layer in enumerate(obs1.frame):
    g = np.array(layer)
    diff_frames(g0, g, f"Frame {i}")

print()
print("="*60)
print("EACH ANIMATION FRAME vs PREVIOUS FRAME")
print("="*60)
for i in range(1, len(obs1.frame)):
    g_prev = np.array(obs1.frame[i-1])
    g_cur  = np.array(obs1.frame[i])
    diff_frames(g_prev, g_cur, f"Frame {i-1}→{i}")

# Show each frame's full legend zone
print()
print("="*60)
print("LEGEND ZONE (rows 41-47) IN EACH FRAME")
print("="*60)
for i, layer in enumerate(obs1.frame):
    g = np.array(layer)
    row42 = ''.join(char.get(int(g[42,c]),'?') for c in range(13,51))
    row45 = ''.join(char.get(int(g[45,c]),'?') for c in range(13,51))
    print(f"  Frame {i} row42: {row42}")
    print(f"  Frame {i} row45: {row45}")

# Show yellow/grid zone in each frame
print()
print("="*60)
print("CHECKERED GRID (rows 9-40 cols 14-50) IN EACH FRAME — only rows with yellow")
print("="*60)
for i, layer in enumerate(obs1.frame):
    g = np.array(layer)
    yellow_rows = [r for r in range(9,41) if any(g[r,c]==11 for c in range(14,51))]
    changed_rows = [r for r in range(9,41) if any(g[r,c] != g0[r,c] for c in range(14,51))]
    all_interesting = sorted(set(yellow_rows+changed_rows))
    if all_interesting:
        print(f"\n  Frame {i}:")
        for r in all_interesting:
            row = ''.join(char.get(int(g[r,c]),'?') for c in range(14,51))
            row0 = ''.join(char.get(int(g0[r,c]),'?') for c in range(14,51))
            marker = " <-- CHANGED" if r in changed_rows else ""
            print(f"    row{r:2d}: {row}{marker}")

# Now try clicking a legend piece and then the oval — see animation
print()
print("="*60)
print("CLICK LEGEND A-HORIZ, THEN OVAL — animation frames")
print("="*60)
arcade2 = Arcade(operation_mode=OperationMode.OFFLINE)
env2 = arcade2.make('tn36')
obs2 = env2.observation_space
g_init2 = np.array(obs2.frame[0])

# Toggle A-horiz
obs2 = env2.step(GameAction.ACTION6, {'x': 26, 'y': 42})
g_after_toggle = np.array(obs2.frame[-1])
print(f"After toggling A-horiz: {len(obs2.frame)} layers")

# Now click the oval
obs3 = env2.step(GameAction.ACTION6, {'x': 36, 'y': 55})
print(f"After oval click (A-horiz toggled): {len(obs3.frame)} layers")
print("\nEach frame vs initial:")
for i, layer in enumerate(obs3.frame):
    g = np.array(layer)
    diff_frames(g_init2, g, f"Frame {i}")

print("\nLegend zone in each frame:")
for i, layer in enumerate(obs3.frame):
    g = np.array(layer)
    row42 = ''.join(char.get(int(g[42,c]),'?') for c in range(13,51))
    row45 = ''.join(char.get(int(g[45,c]),'?') for c in range(13,51))
    print(f"  Frame {i} row42: {row42}")
    print(f"  Frame {i} row45: {row45}")
