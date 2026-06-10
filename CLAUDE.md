# CLAUDE.md — ARC-AGI-3
*Last updated: 2026-06-10*

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

ARC-AGI-3 is a set of interactive 2D game environments. An agent must play each game, infer the rules from observation, and complete it. The metric is **RHAE** (Relative Human Action Efficiency): (human_baseline_actions / agent_actions)², so a perfectly efficient agent equals the human baseline score of 1.0. Frontier LLMs score ~0.18–0.51%.

The central challenge: **the rules are unknown at the start of each game.** The agent must explore, form hypotheses, test them, and converge on the optimal action sequence — all within a budget.

## Data

- `environment_files/` — 25 game environments, each with a Python game file and `metadata.json`
- Each `metadata.json` includes `baseline_actions` (the human solution action count)
- Games run locally via the `arc-agi` Python package; no API key required in OFFLINE mode

## Environment Setup

```bash
conda activate arc-agi3

# Run the exploration script (local, no API key needed)
python scripts/explore_game.py sp80
python scripts/explore_game.py sp80 reset 1 2 3
```

Available games (25 total): ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30

## Game mechanics

- **Grid**: up to 64×64, values 0–15
- **Actions**: RESET, ACTION1–ACTION7 (subset available per game; check `available_actions` in frame)
- **Win condition**: `levels_completed == win_levels`
- **Frame**: multi-layer; `frame[-1]` is the top (visible) layer
- **Grid colours**: 0=white 1=lt-grey 2=md-grey 3=dk-grey 4=vdk-grey 5=black 6=pink 7=lt-pink 8=red 9=blue 10=lt-blue 11=yellow 12=orange 13=maroon 14=green 15=purple

## Game exploration process

For each game:

**THE CODE GATE applies here too.** Load and print the initial state. Then write the analysis before any hypothesis-testing action sequences.

### Step 1 — Read the initial state
Print the grid and note:
- What objects are present (by colour/value)?
- Where is the player? (look for the moving object — usually a distinctive colour)
- What looks like a goal/target? A door? Walls?
- What do the available actions suggest? (ACTION1–4 usually = directional movement)

### Step 2 — Probe one action at a time
Take one action and compare the before/after grids:
- What moved? What stayed?
- Did the player position change? In which direction?
- Did any state variable change (levels_completed, available_actions)?

Write your observation **as text** before taking the next action. Do not chain actions silently.

### Step 3 — Build a world model
After probing each action type, write a world model:
- Player position and movement rules
- Obstacle/wall behaviour
- Goal/win condition
- Any special objects (doors, keys, switches)

### Step 4 — Plan and execute
Once the world model is confirmed, plan the minimum action sequence to win, execute it, and record the result.

### Observation format
After every action, always write:
1. **What changed**: diff of the grid (what positions changed and to what value)
2. **Player position**: where the player is now
3. **Hypothesis update**: does this confirm or refute the current world model?
4. **Next action and why**: what you will probe next

## Code loading pattern

```python
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('sp80')
obs = env.observation_space  # initial state after RESET

# Take an action
frame = env.step(GameAction.ACTION1, data={})
```

## Autonomous operation

Proceed without asking for confirmation on all local work:
- Running game exploration scripts
- Writing or editing scripts and notebooks
- Updating CLAUDE.md or memory files
- Any local file read, write, or edit

**Always ask before:**
- `git push` (to any remote branch)
- Deleting files or branches
- Any operation affecting shared or remote state

Do not run long autonomous action sequences (>10 actions) without reporting observations to the user first.

## Key questions for ARC3 research

1. Can the verbal hypothesis-building process (from ARC2) transfer to interactive games?
2. What world-model representation is most efficient for ARC3 games?
3. Can the optimal action sequence be derived analytically from the world model, or does it require search?
4. How does the game structure compare to ARC2? Are there "recurring structural patterns" equivalent to ARC2's pattern library?
