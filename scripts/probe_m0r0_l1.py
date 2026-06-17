"""m0r0 Level 1 — Step 2: probe all actions, produce full action table."""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

colours = {0:'.',1:'a',2:'b',3:'c',4:'d',5:'#',6:'P',7:'p',8:'R',9:'B',10:'L',11:'Y',12:'O',13:'M',14:'G',15:'V'}

def make_env():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    return env

def get_grid(obs):
    return np.array(obs.frame[-1])

def diff_grids(before, after):
    changed = np.argwhere(before != after)
    if len(changed) == 0:
        return "NO CHANGE"
    r0, c0 = changed.min(axis=0)
    r1, c1 = changed.max(axis=0)
    transitions = {}
    for r, c in changed:
        key = (int(before[r, c]), int(after[r, c]))
        transitions[key] = transitions.get(key, 0) + 1
    t_str = ", ".join(
        f"{colours.get(a,'?')}{a}->{colours.get(b,'?')}{b}:{n}"
        for (a, b), n in sorted(transitions.items())
    )
    return f"{len(changed)} cells changed, bbox rows {r0}-{r1} cols {c0}-{c1}, transitions: {t_str}"

print("=== m0r0 Level 1 — Action Table ===\n")
print(f"Initial state summary:")
env0 = make_env()
obs0 = env0.observation_space
g0 = get_grid(obs0)
vals, counts = np.unique(g0, return_counts=True)
for v, c in zip(vals, counts):
    print(f"  colour {v} ({colours.get(v,'?')}): {c} cells")
print(f"  available_actions: {obs0.available_actions}")
print(f"  levels_completed={obs0.levels_completed} win_levels={obs0.win_levels}")
print()

# Test ACTION1–ACTION5
for action_num, action in [
    (1, GameAction.ACTION1),
    (2, GameAction.ACTION2),
    (3, GameAction.ACTION3),
    (4, GameAction.ACTION4),
    (5, GameAction.ACTION5),
]:
    env = make_env()
    obs_before = env.observation_space
    g_before = get_grid(obs_before)
    aa_before = obs_before.available_actions

    obs_after = env.step(action)
    g_after = get_grid(obs_after)
    aa_after = obs_after.available_actions

    result = diff_grids(g_before, g_after)
    aa_note = f" | aa: {aa_before}->{aa_after}" if aa_before != aa_after else ""
    lvl_note = f" | LEVEL COMPLETE" if obs_after.levels_completed > 0 else ""
    print(f"ACTION{action_num}: {result}{aa_note}{lvl_note}")

# ACTION6 — click on distinct objects
print()
print("ACTION6 (click) — distinct targets:")
test_points = [
    (19, 49, "left L-block (lt-blue)"),
    (39, 49, "right L-block (lt-blue)"),
    (15, 15, "left black structure"),
    (47, 15, "right black structure"),
    (10, 10, "yellow background (left half)"),
    (52, 10, "orange background (right half)"),
    (0,  32, "top-centre border"),
    (32, 32, "vertical midpoint"),
    (63, 32, "bottom-centre"),
    (0,   0, "top-left corner"),
    (19, 53, "just below left L-block"),
    (39, 53, "just below right L-block"),
]
for x, y, label in test_points:
    env = make_env()
    obs_before = env.observation_space
    g_before = get_grid(obs_before)

    obs_after = env.step(GameAction.ACTION6, {"x": x, "y": y})
    g_after = get_grid(obs_after)

    result = diff_grids(g_before, g_after)
    lvl_note = f" | LEVEL COMPLETE" if obs_after.levels_completed > 0 else ""
    print(f"  ({x:2d},{y:2d}) {label}: {result}{lvl_note}")
