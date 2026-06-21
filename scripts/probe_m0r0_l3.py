"""m0r0 Level 3 — Step 2: comprehensive action probe with automatic second-pass.

For any action that produces a non-movement state change, replays to that
state and probes all actions again automatically.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

AMAP = {'U': GameAction.ACTION1, 'D': GameAction.ACTION2,
        'X': GameAction.ACTION3, 'C': GameAction.ACTION4,
        '5': GameAction.ACTION5}

L1 = 'UUXUUUUUCUCCCCCDDDCDDDDDXD'
L2 = 'DXXXDDDCCUCCDDDDDDXXXXXCCCCCCU'

colours = {0:'white', 1:'lt-grey', 2:'md-grey', 3:'dk-grey', 4:'vdk-grey',
           5:'black', 6:'pink', 7:'lt-pink', 8:'red', 9:'blue',
           10:'lt-blue', 11:'yellow', 12:'orange', 13:'maroon', 14:'green', 15:'purple'}

MOVEMENT_COLOURS = {5, 10}  # black <-> lt-blue is pure movement


def make_l3():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('m0r0')
    obs = env.observation_space
    for a in L1 + L2:
        obs = env.step(AMAP[a])
    return env, obs


def diff_grids(before, after):
    before, after = np.array(before), np.array(after)
    changed = np.argwhere(before != after)
    if len(changed) == 0:
        return 0, {}, None
    rows, cols = changed[:, 0], changed[:, 1]
    bbox = (rows.min(), cols.min(), rows.max(), cols.max())
    trans = {}
    for r, c in changed:
        key = (int(before[r, c]), int(after[r, c]))
        trans[key] = trans.get(key, 0) + 1
    return len(changed), trans, bbox


def is_non_movement_change(trans):
    """True if any transition involves colours outside the movement set."""
    return any(a not in MOVEMENT_COLOURS or b not in MOVEMENT_COLOURS
               for (a, b) in trans)


def get_block_state(obs):
    grid = np.array(obs.frame[-1])
    cells = np.argwhere(grid == 10)
    if len(cells) == 0:
        return "NO BLOCKS"
    rows, cols = cells[:, 0], cells[:, 1]
    return f"row={rows.min()} left_col={cols.min()} right_col={cols.max()-3}"


def probe_from(env_factory, label_prefix=""):
    """Probe all simple actions + ACTION6 targets. Returns list of (label, n, trans, obs_after)."""
    results = []

    simple_actions = [
        ("ACTION1(UP)",      GameAction.ACTION1, None),
        ("ACTION2(DOWN)",    GameAction.ACTION2, None),
        ("ACTION3(DIVERGE)", GameAction.ACTION3, None),
        ("ACTION4(CONVERGE)",GameAction.ACTION4, None),
        ("ACTION5",          GameAction.ACTION5, None),
    ]
    a6_targets = [
        ("ACTION6@left-block(23,47)",   {"x": 23, "y": 47}),
        ("ACTION6@right-block(39,47)",  {"x": 39, "y": 47}),
        ("ACTION6@blue-1(31,15)",       {"x": 31, "y": 15}),
        ("ACTION6@blue-2(11,19)",       {"x": 11, "y": 19}),
        ("ACTION6@blue-3(39,31)",       {"x": 39, "y": 31}),
        ("ACTION6@black-wall(15,15)",   {"x": 15, "y": 15}),
        ("ACTION6@black-wall(40,15)",   {"x": 40, "y": 15}),
        ("ACTION6@purple-bg(5,5)",      {"x": 5,  "y": 5}),
        ("ACTION6@red-bg(50,5)",        {"x": 50, "y": 5}),
    ]
    try:
        a7_result = [("ACTION7", GameAction.ACTION7, None)]
    except Exception:
        a7_result = []

    for name, action, _ in simple_actions + a7_result:
        env, obs = env_factory()
        before = obs.frame[-1]
        bs_before = get_block_state(obs)
        actions_before = obs.available_actions
        obs2 = env.step(action)
        after = obs2.frame[-1]
        bs_after = get_block_state(obs2)
        n, trans, bbox = diff_grids(before, after)
        actions_after = obs2.available_actions
        lbl = label_prefix + name
        results.append((lbl, n, trans, bbox, bs_before, bs_after,
                        actions_before, actions_after, obs2))

    for name, coords in a6_targets:
        env, obs = env_factory()
        before = obs.frame[-1]
        bs_before = get_block_state(obs)
        actions_before = obs.available_actions
        obs2 = env.step(GameAction.ACTION6, coords)
        after = obs2.frame[-1]
        bs_after = get_block_state(obs2)
        n, trans, bbox = diff_grids(before, after)
        actions_after = obs2.available_actions
        lbl = label_prefix + name
        results.append((lbl, n, trans, bbox, bs_before, bs_after,
                        actions_before, actions_after, obs2))

    return results


def print_result(lbl, n, trans, bbox, bs_before, bs_after, acts_before, acts_after, obs2):
    print(f"\n  {lbl}")
    print(f"    blocks: {bs_before} -> {bs_after}  |  changed={n}  |  levels={obs2.levels_completed}")
    if n > 0 and bbox:
        print(f"    bbox: rows {bbox[0]}-{bbox[2]}, cols {bbox[1]}-{bbox[3]}")
        trans_str = ", ".join(f"{colours.get(a,'?')}->{colours.get(b,'?')}:{c}"
                              for (a, b), c in sorted(trans.items()))
        print(f"    transitions: {trans_str}")
    if acts_before != acts_after:
        print(f"    ** available_actions: {acts_before} -> {acts_after}")


# ── PASS 1: from initial Level 3 state ──────────────────────────────────────
print("=" * 70)
print("PASS 1 — from initial Level 3 state")
print("=" * 70)

env0, obs0 = make_l3()
print(f"Initial: {get_block_state(obs0)}  available={obs0.available_actions}")

pass1 = probe_from(make_l3, "")
non_movement = []

for row in pass1:
    lbl, n, trans, bbox, bs_before, bs_after, acts_before, acts_after, obs2 = row
    print_result(*row)
    if n > 0 and is_non_movement_change(trans):
        non_movement.append(row)

# ── PASS 2: automatic second-pass for each non-movement state change ─────────
if non_movement:
    print("\n" + "=" * 70)
    print("PASS 2 — probing from each non-movement changed state")
    print("=" * 70)

    for trigger_row in non_movement:
        lbl_trigger, n_t, trans_t, bbox_t, bs_b, bs_a, acts_b, acts_a, obs_trigger = trigger_row
        print(f"\n>>> Changed state after: {lbl_trigger}")
        print(f"    (transitions: {', '.join(f'{colours.get(a,a)}->{colours.get(b,b)}:{c}' for (a,b),c in sorted(trans_t.items()))})")

        # Build a factory that replays to this changed state
        action_key = lbl_trigger  # for identification only

        # Determine which action/click produced this state
        # We'll replay L3 then apply the trigger action
        def make_triggered(trigger=trigger_row):
            lbl_t2 = trigger[0]
            env, obs = make_l3()
            # Identify the action from the label
            if "ACTION1" in lbl_t2:
                obs = env.step(GameAction.ACTION1)
            elif "ACTION2" in lbl_t2:
                obs = env.step(GameAction.ACTION2)
            elif "ACTION3" in lbl_t2:
                obs = env.step(GameAction.ACTION3)
            elif "ACTION4" in lbl_t2:
                obs = env.step(GameAction.ACTION4)
            elif "ACTION5" in lbl_t2:
                obs = env.step(GameAction.ACTION5)
            elif "ACTION7" in lbl_t2:
                obs = env.step(GameAction.ACTION7)
            elif "blue-1" in lbl_t2:
                obs = env.step(GameAction.ACTION6, {"x": 31, "y": 15})
            elif "blue-2" in lbl_t2:
                obs = env.step(GameAction.ACTION6, {"x": 11, "y": 19})
            elif "blue-3" in lbl_t2:
                obs = env.step(GameAction.ACTION6, {"x": 39, "y": 31})
            elif "left-block" in lbl_t2:
                obs = env.step(GameAction.ACTION6, {"x": 23, "y": 47})
            elif "right-block" in lbl_t2:
                obs = env.step(GameAction.ACTION6, {"x": 39, "y": 47})
            return env, obs

        env_t, obs_t = make_triggered()
        print(f"    State after trigger: {get_block_state(obs_t)}  available={obs_t.available_actions}")

        # Render a section of the grid to see what's there now
        grid_t = np.array(obs_t.frame[-1])
        char = {0:'.', 1:'a', 2:'b', 3:'c', 4:'d', 5:'#', 6:'P', 7:'p',
                8:'R', 9:'B', 10:'L', 11:'Y', 12:'O', 13:'M', 14:'G', 15:'V'}
        # Find lt-grey cells
        grey_cells = np.argwhere(grid_t == 1)
        yellow_cells = np.argwhere(grid_t == 11)
        if len(grey_cells):
            gr = grey_cells[:, 0]; gc = grey_cells[:, 1]
            print(f"    lt-grey cells: {len(grey_cells)} at rows {gr.min()}-{gr.max()}, cols {gc.min()}-{gc.max()}")
        if len(yellow_cells):
            yr = yellow_cells[:, 0]; yc = yellow_cells[:, 1]
            print(f"    yellow cells: {len(yellow_cells)} at rows {yr.min()}-{yr.max()}, cols {yc.min()}-{yc.max()}")

        pass2 = probe_from(make_triggered, f"  [after {lbl_trigger}] ")
        for row2 in pass2:
            print_result(*row2)

        # Check if clicking remaining blue markers does anything different
        print(f"\n  --- Additional blue marker clicks from this state ---")
        remaining_blues = [
            ("ACTION6@blue-1(31,15)", {"x": 31, "y": 15}),
            ("ACTION6@blue-2(11,19)", {"x": 11, "y": 19}),
            ("ACTION6@blue-3(39,31)", {"x": 39, "y": 31}),
        ]
        for bname, coords in remaining_blues:
            env_t2, obs_t2 = make_triggered()
            before2 = obs_t2.frame[-1]
            obs3 = env_t2.step(GameAction.ACTION6, coords)
            after2 = obs3.frame[-1]
            n2, trans2, bbox2 = diff_grids(before2, after2)
            lbl2 = f"  [after {lbl_trigger}] {bname}"
            print_result(lbl2, n2, trans2, bbox2,
                        get_block_state(obs_t2), get_block_state(obs3),
                        obs_t2.available_actions, obs3.available_actions, obs3)

print("\n=== Probe complete ===")
