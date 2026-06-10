"""
explore_game.py — inspect an ARC3 game environment locally.

Usage:
    python scripts/explore_game.py sp80          # print initial state
    python scripts/explore_game.py sp80 reset    # take RESET action
    python scripts/explore_game.py sp80 1 2 1    # RESET then ACTION1, ACTION2, ACTION1

Actions:
    reset  — RESET
    1–7    — ACTION1 through ACTION7

Grid values (ARC3 colour scheme, 0–15):
    0=white  1=lt-grey  2=md-grey  3=dk-grey  4=vdk-grey  5=black
    6=pink   7=lt-pink  8=red      9=blue     10=lt-blue  11=yellow
    12=orange 13=maroon 14=green  15=purple
"""

import sys
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

# Single-char display symbols for values 0–15
_SYMBOLS = "·₁₂₃₄■PpRBbYOmGV"  # 16 chars, index = value

ARC3_COLOURS = {
    0: "white", 1: "lt-grey", 2: "md-grey", 3: "dk-grey",
    4: "vdk-grey", 5: "black", 6: "pink", 7: "lt-pink",
    8: "red", 9: "blue", 10: "lt-blue", 11: "yellow",
    12: "orange", 13: "maroon", 14: "green", 15: "purple",
}

ACTION_MAP = {
    "reset": GameAction.RESET,
    "0": GameAction.RESET,
    "1": GameAction.ACTION1,
    "2": GameAction.ACTION2,
    "3": GameAction.ACTION3,
    "4": GameAction.ACTION4,
    "5": GameAction.ACTION5,
    "6": GameAction.ACTION6,
    "7": GameAction.ACTION7,
}


def print_grid(grid, label=""):
    rows = [row.tolist() if hasattr(row, "tolist") else row for row in grid]
    H, W = len(rows), len(rows[0]) if rows else 0
    print(f"\n{'─'*40}")
    if label:
        print(f"  {label}  [{H}×{W}]")
    print(f"{'─'*40}")
    for r, row in enumerate(rows):
        line = "".join(
            _SYMBOLS[v] if 0 <= v < len(_SYMBOLS) else "?" for v in row
        )
        print(f"{r:3d} {line}")
    # Count unique values and their meanings
    vals = sorted(set(v for row in rows for v in row))
    meanings = ", ".join(f"{v}={ARC3_COLOURS.get(v, '?')}" for v in vals)
    print(f"\n  Values present: {meanings}")
    print(f"{'─'*40}")


def print_frame_info(frame, action_name=""):
    print(f"\n{'='*50}")
    if action_name:
        print(f"  After: {action_name}")
    print(f"  State:            {frame.state.name}")
    print(f"  Levels completed: {frame.levels_completed} / {frame.win_levels}")
    print(f"  Available actions: {frame.available_actions}")
    print(f"  Full reset:       {frame.full_reset}")
    layers = frame.frame if hasattr(frame.frame, "__len__") else []
    print(f"  Frame layers:     {len(layers)}")
    print(f"{'='*50}")
    if layers:
        print_grid(layers[-1], label="Game grid (top layer)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    game_id = sys.argv[1]
    action_args = sys.argv[2:] if len(sys.argv) > 2 else []

    import logging
    logging.basicConfig(level=logging.WARNING)

    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    available = [e.game_id.split("-")[0] for e in arcade.available_environments]
    if game_id not in available:
        print(f"Game '{game_id}' not found. Available: {sorted(set(available))}")
        sys.exit(1)

    env = arcade.make(game_id)
    if env is None:
        print(f"Failed to load game '{game_id}'")
        sys.exit(1)

    obs = env.observation_space
    print(f"\nLoaded game: {game_id}")
    print(f"Win condition: complete {obs.win_levels} levels")
    baseline = env.info.baseline_actions
    if baseline:
        print(f"Baseline human solution: {len(baseline)} actions")
    print_frame_info(obs, action_name="Initial state")

    for arg in action_args:
        arg_lower = arg.lower()
        if arg_lower not in ACTION_MAP:
            print(f"Unknown action '{arg}'. Use: reset or 1–7")
            continue
        action = ACTION_MAP[arg_lower]
        result = env.step(action, data={})
        if result is None:
            print(f"Action {arg} returned None")
            break
        print_frame_info(result, action_name=f"{action.name} ({arg})")


if __name__ == "__main__":
    main()
