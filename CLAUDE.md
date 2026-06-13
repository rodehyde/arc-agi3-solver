# CLAUDE.md — ARC-AGI-3
*Last updated: 2026-06-13*

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
```

Available games (25 total): ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30

## Game mechanics

- **Grid**: up to 64×64, values 0–15
- **Actions**: RESET, ACTION1–ACTION7 (subset available per game; check `available_actions` in frame)
- **Win condition**: `levels_completed == win_levels`
- **Frame**: multi-layer; `frame[-1]` is the top (visible) layer
- **Grid colours**: 0=white 1=lt-grey 2=md-grey 3=dk-grey 4=vdk-grey 5=black 6=pink 7=lt-pink 8=red 9=blue 10=lt-blue 11=yellow 12=orange 13=maroon 14=green 15=purple

---

## Per-level analysis process

**MUST follow this sequence for every level. Do not jump to testing a sequence before completing all four steps.**

### 1 — Describe the scene (written in conversation)

There are a number of different types of game. We've identified two so far:
A player moves around the grid and performs actions. 
There is no player. It's necessary to click on various elements within the grid. 

We will develop special instructions for the different types of games as we progress. 
 
Load the level and write — in words — what is visible:
- try and identify the type of game, and if it's unclear, stop and review

- What objects are present? (colour, size, position)
- What does a win look like? Is there an obvious symmetry or alignment to achieve?
- Any special objects — dividers, markers, toggles?

### 2 — Work out the actions (written in conversation)

Here are the available actions. 
Available Actions
Agents interact with environments using up to 7 actions:

Action	Description
RESET	Start or restart the game
ACTION1 – ACTION5	Simple actions (e.g., move up/down/left/right, interact)
ACTION6	Complex action requiring (x, y) coordinates
ACTION7	Additional simple action

> ## 🚧 HARD GATE — the Action Table. DO NOT PASS THIS POINT until it is complete and printed.
>
> **This step has repeatedly been cut short, and that has repeatedly broken the investigation.** It is now a blocking gate. You **MUST NOT** state a hypothesis (Step 3), run a solver, propose a sequence, or ask the user about the win condition until a **complete action table for the current level has been written out and printed to the user in this conversation.** No exceptions, no "I'll characterise the rest later."
>
> **The instrument must detect ANY cell change — never movement-only.** Compare the full grid before/after and report: total cells changed, the bounding box of the change, AND every value transition (e.g. `0->9:20, 11->12:1`). A probe that only tracks a piece's bounding-box displacement is forbidden as the basis for "no effect" — it is blind to state changes (toggles, counters, indicator cells, dot patterns) and has produced wrong conclusions before.
>
> **Every action 1–7 must appear in the table**, characterised in **every control mode** (probe all actions again after each toggle). For ACTION6 (click), you MUST test clicks on **each distinct object/target** (every coloured shape, the divider, its markers, AND empty space) — a single arbitrary click is not sufficient and must never be the basis for "ACTION6 does nothing."
>
> **"No effect" is a conclusion, not a default.** You may only write "no effect" for an action after the unbiased any-cell-change instrument has been run against it (and, for ACTION6, against every distinct target) and shown zero changed cells.
>
> **Required output before proceeding:** a printed table with one row per action (ACTION1–ACTION7), columns for each mode, stating for each: cells changed, value transitions, what moved / what toggled, and whether `available_actions` changed. Print it to the user. Only then continue to Step 3.

Probe each available action one at a time. For each, describe:
- What moved? In which direction? By how much (measured at the top-left corner, not centroid)?
- What value transitions occurred (counters, indicator cells, marker/dot patterns)?
- Did `available_actions` change? If yes, this action is a **control-scheme toggle**.

**Toggle rule — MUST NOT be skipped:** Any action that changes the grid without producing a useful movement is a candidate toggle. After finding it, probe all actions again in the toggled state to find what becomes available. A toggle may switch the control *axis* (horizontal-only ↔ vertical-enabled) OR switch *which object* you control (e.g. divider ↔ pieces). At least two levels of ar25 use such a toggle. Do not assume a direction or object is unavailable until every toggled state has been probed.

Action 6 is a **click** that requires an (x, y) coordinate on the 64×64 grid. It is **context-sensitive**: it often only acts when the click lands on the currently-active object, and does nothing on the wrong target — so it must be tested against every distinct object, not one arbitrary point.

### 3 — Hypothesis (written in conversation)

State in words:
- If there is a player the player's starting position and the target's position?
- If there is no player, then any symmetry that could be the winning situation. 
- How many steps of each type are needed?
- Which actions satisfy each step, including any toggle before/after?
- What is the proposed action sequence in plain English?

### 4 — Write code to test the hypothesis

Write a short Python script (not a notebook cell) to:
1. Load the game and replay to the current level
2. Execute the proposed sequence
3. Print before/after positions and whether the level completed

Report the result. If it works, give the ACTIONS list for Cell 7. If not, describe what position was reached vs what was needed, revise the hypothesis (step 3), and re-test.

---

## Recurring structural patterns in ARC3

**Control-scheme toggle.** One action (often a colour-flip or marker change) switches the game between movement modes. In ar25 levels 2+: ACTION5 flips a colour AND switches from horizontal-only to vertical-enabled. When directional actions appear to do nothing, look for the toggle first.

**Compound objects.** Multiple colours that always move together (e.g. an L-shape + embedded markers). Measure step size by top-left corner movement, not centroid.

**Level-specific mechanics.** Mechanics change between levels. Re-run steps 1–2 at the start of each new level.

---

## Notebook workflow (Cell 7 is the execution cell)

- Cell 1: setup (run once per session)
- Cell 2: load a game
- Cell 3: take one action at a time (exploration)
- Cell 4: reset; `RESET_TO_LEVEL=N` replays to level N
- Cell 7: execute an ACTIONS list; completed levels auto-saved to `LEVEL_SOLUTIONS`
- Cell 8: action table from game start (useful for initial exploration)

The verbal analysis (steps 1–3) happens in conversation. Code for step 4 runs in a script or notebook scratch cell. Cell 7 executes the final ACTIONS sequence.

---

## Autonomous operation

Proceed without asking for confirmation on all local work, and **keep going without pausing for permission between steps or levels.** Do not end a turn with "shall I run this?", "want me to continue?", or "shall I move to the next level?" — just do it and report the result. Work straight through the per-level process (steps 1→4) and straight on to the next level until the game is solved, the budget is exhausted, or you hit something genuinely ambiguous.

The only reasons to stop and ask:
- A hypothesis has **failed twice** and you need the user's read on the scene before trying again.
- The scene is genuinely ambiguous and the analysis process says to stop and review (e.g. unclear game type).
- `git push`, deleting files, or any operation affecting shared or remote state.

Otherwise: report findings as you go, but never wait for a "yes" to keep working.

## Key questions for ARC3 research

1. Is the control-scheme toggle a universal mechanic across all 25 games?
2. How many control states does each game have?
3. Can the world model be derived reliably from the verbal process alone?
