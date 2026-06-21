"""tn36 — brute-force all 2^10 = 1024 legend states via Gray code.
Each state differs from the previous by 1 toggle (1 click).
Bar has 61 cells per game. ~17 fresh instances needed.
Encoding: bits 0-9 = A-h, A-v, B-h, B-v, C-h, C-v, D-h, D-v, E-h, E-v
          1=black, 0=lt-grey
Initial state: D-h=1, D-v=1, E-h=1, E-v=1, rest=0 → 0b1111000000 = 960
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

# Legend click positions: (row, col) for each bit
PIECES = [
    ("A-h", 42, 26), ("A-v", 45, 26),
    ("B-h", 42, 36), ("B-v", 45, 36),
    ("C-h", 42, 41), ("C-v", 45, 41),
    ("D-h", 42, 21), ("D-v", 45, 21),
    ("E-h", 42, 31), ("E-v", 45, 31),
]

INITIAL_STATE = 0b1111000000  # D-h=1, D-v=1, E-h=1, E-v=1

def fresh_env():
    arcade = Arcade(operation_mode=OperationMode.OFFLINE)
    env = arcade.make('tn36')
    obs = env.observation_space
    return env, obs

def click(env, col, row):
    obs = env.step(GameAction.ACTION6, {'x': col, 'y': row})
    return obs

def state_str(state):
    names = [p[0] for p in PIECES]
    active = [names[i] for i in range(10) if (state >> i) & 1]
    return f"[{','.join(active)}]" if active else "[none]"

# Gray code: each consecutive n differs by 1 bit
def gray_code(n):
    return n ^ (n >> 1)

# The sequence of bit flips to go from gray(i) to gray(i+1)
def gray_flips(n_states):
    result = []
    for i in range(1, n_states):
        diff = gray_code(i) ^ gray_code(i-1)
        bit = diff.bit_length() - 1
        result.append(bit)
    return result

# We need to navigate from INITIAL_STATE to gray(0)=0 first,
# then follow the Gray code sequence through all 1024 states.
# OR: start from the state that matches INITIAL_STATE in Gray code.
# Find which gray code index matches INITIAL_STATE:
# gray(i) = INITIAL_STATE ↔ i = gray_to_binary(INITIAL_STATE)
def gray_to_bin(g):
    # Convert Gray code g to binary
    mask = g
    while mask:
        mask >>= 1
        g ^= mask
    return g

initial_gray_idx = gray_to_bin(INITIAL_STATE)
print(f"Initial state = {INITIAL_STATE:010b} = gray({initial_gray_idx})")
print(f"Will search all 1024 states starting from initial state")

# Plan: enumerate all 1024 states, but route through them starting from INITIAL.
# Generate full 1024-step Gray code path starting from initial_gray_idx.
# Skip i=0 (that's the initial state itself, no flip needed).
all_states_ordered = [(gray_code((initial_gray_idx + i) % 1024), i)
                      for i in range(1, 1025)]

# Compute the sequence of toggles needed
toggle_sequence = []
prev = INITIAL_STATE
for state, step in all_states_ordered:
    diff = prev ^ state
    assert diff != 0, f"No diff at state {state}"
    bit = diff.bit_length() - 1
    toggle_sequence.append(bit)
    prev = state

print(f"Toggle sequence length: {len(toggle_sequence)}")

# Now run: batch into segments that fit within the bar budget (61 per game)
# After each toggle, check levels
winning_states = []
current_state = INITIAL_STATE
env, obs = fresh_env()
bar_remaining = 61

step = 0
state_num = 0
print(f"\nStarting brute force... (checking {1024} states)")

for bit in toggle_sequence:
    if bar_remaining <= 2:
        # Create fresh env, navigate back to current_state
        env, obs = fresh_env()
        bar_remaining = 61
        # Navigate from initial state (INITIAL_STATE) to current_state
        init_to_cur = INITIAL_STATE ^ current_state
        for b in range(10):
            if (init_to_cur >> b) & 1:
                name, row, col = PIECES[b]
                obs = click(env, col, row)
                bar_remaining -= 1

    # Toggle bit
    name, row, col = PIECES[bit]
    obs = click(env, col, row)
    bar_remaining -= 1
    current_state ^= (1 << bit)
    state_num += 1

    if obs.levels_completed > 0:
        print(f"  *** WIN *** at step {state_num}, state={current_state:010b} = {state_str(current_state)}")
        winning_states.append(current_state)

    if state_num % 100 == 0:
        print(f"  ... checked {state_num}/1024 states, bar={bar_remaining}")

if winning_states:
    print(f"\nWINNING STATES FOUND: {len(winning_states)}")
    for s in winning_states:
        print(f"  {s:010b} = {state_str(s)}")
        # Compute minimum clicks from INITIAL_STATE
        diff = INITIAL_STATE ^ s
        n_clicks = bin(diff).count('1')
        print(f"  Clicks from initial: {n_clicks}")
        bits = [PIECES[i][0] for i in range(10) if (diff >> i) & 1]
        print(f"  Pieces to toggle: {bits}")
else:
    print("\nNo winning state found among all 1024 configurations.")
    print("This means the win condition is NOT purely about legend toggle state.")
    print("Need to investigate other mechanics.")
