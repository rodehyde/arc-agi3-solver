# CLAUDE.md — ARC-AGI-3
*Last updated: 2026-06-20*

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

ARC-AGI-3 is a set of interactive 2D game environments. An agent must play each game, infer the rules from observation, and complete it. The metric is **RHAE** (Relative Human Action Efficiency): (human_baseline_actions / agent_actions)², so a perfectly efficient agent equals the human baseline score of 1.0. Frontier LLMs score ~0.18–0.51%.

The central challenge: **the rules are unknown at the start of each game.** The agent must explore, form hypotheses, test them, and converge on the optimal action sequence — all within a budget.

These tasks are very difficult and the difficulty increases with each level. They're designed to test you to and beyond your limit. We're working on producing a structured approach based on our learnings by completing tasks. 

This is equivalent to the way human beings are taught general principles and processes and then learned by example.

For this project to be valuable it is vital that:
The structured approach is used throughout and any creativity occurs within that approach.
The only information that you're allowed to use about the task is the grid and the actions available. You must not cheat by finding information about the task online Or in the code you have available 




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
- **Observation API**: `obs.frame` is the list of grid layers; `obs.frame[-1]` is the top visible layer. Key fields: `obs.available_actions`, `obs.levels_completed`, `obs.win_levels`. Do NOT use `obs.grid` — it does not exist.
- **Step 1 script discipline**: Write one comprehensive inspection script — explore obs attributes, display bounding box, print values present — in a single pass. Never suppress stderr (`2>/dev/null`) during exploration; silent failures waste round-trips.
- **Grid colours**: 0=white 1=lt-grey 2=md-grey 3=dk-grey 4=vdk-grey 5=black 6=pink 7=lt-pink 8=red 9=blue 10=lt-blue 11=yellow 12=orange 13=maroon 14=green 15=purple

---
You are in training mode unless told otherwise. 


## Mandatory step markers — enforced gate

Before writing ANY code or script for a level, the following markers MUST appear in the conversation output, in order. Their absence before a code block is a verifiable process violation.

```
STEP 1 COMPLETE — [scene description + novel elements listed]
STEP 2 COMPLETE — ACTION TABLE: [full table]
ELEMENT AUDIT COMPLETE — FUNCTION TABLE: [table with all elements graded]
STEP 3 HYPOTHESIS: [sequence derived from audit, in plain English]
```

These markers are not optional, not abbreviatable, and not post-hoc. They must be printed before the first tool call that writes or runs code. In evaluation mode they still apply — the markers appear in output even when no human is reading.

When something difficult is encountered — and that can be when you've worked on a problem for more than two minutes — print out an interim statement and wait to be told to proceed.

---

## Per-level analysis process

**MUST follow this sequence for every level. Do not jump to testing a sequence before completing all four steps.**

> ## ⚠️ VERIFICATION RULE — applies to every statement in every step
>
> **Every statement made in the analysis must be backed by verified data, not inference or visual pattern-matching.**
>
> - If a claim can be checked by reading cell values → check the values before stating it as fact.
> - If a claim can be checked by running an action → run it before stating it as fact.
> - If a claim cannot yet be verified → state it as "I think" or "appears to be" and flag it explicitly as an open question for the next step.
>
> **Descriptions are hypotheses until the data confirms them.** The specific failure mode to avoid: concluding a cell is traversable because it is not the obstacle colour — background cells (pink, lt-pink, etc.) are also impassable. Only value=5 (black) cells are traversable. Check actual cell values, not just "not the obstacle."
>
> **A model built from individual measurements must be cross-checked against any observations that combine those measurements before it is treated as confirmed.**
>
> When you derive a model by summing individual probe results (e.g. an offset table, a contribution table, a per-piece rate), and you also have any test result that exercises multiple elements together, you MUST explicitly ask: *"Does this combined result match what my model predicts?"* A discrepancy between a combined observation and the model's prediction exposes an error in the individual measurements — not in the combined test. Perform this cross-check before declaring the model CONFIRMED.
>
> **The specific failure mode to avoid:** holding both a model and a contradicting combined test result in context simultaneously without noticing the contradiction. Example: an offset table predicted removing two pieces would move Pattern A by −2 rows; a two-piece removal test showed −1 row; the contradiction was never noticed because the results were never explicitly compared. The fix is a single sentence after building any additive model: *"Now check: does every combined test result in this session agree with this model's predictions?"*
>
> **Eliminating a hypothesis is a positive claim and requires the same verification standard.** Before ruling out a line of inquiry, name the specific observation that rules it out and verify it is correct. If the ruling-out evidence is itself derived from a model or inference rather than a direct measurement, the hypothesis is not eliminated — it is merely deprioritised pending verification.
>
> **The specific failure mode:** stating "approach X is ruled out because of Y" where Y is an unverified inference, then moving on. When the approach later turns out to be correct, far more time is wasted than a quick double-check at dismissal time would have cost. The simpler and more obvious an approach looks, the higher the bar for ruling it out — because the simpler the approach, the more likely the ruling-out evidence contains an error. Circumstantial evidence (e.g. "the baseline action count is high, so a simple solution is unlikely") is not ruling-out evidence.
Please show me your complete action table. 
### 1 — Describe the scene (written in conversation)

There are a number of different types of game. We've identified two so far:
A player moves around the grid and performs actions. 
There is no player. It's necessary to click on various elements within the grid. 

We will develop special instructions for the different types of games as we progress. 
 
Load the level and write — in words — what is visible:
- try and identify the type of game, and if it's unclear, stop and review
- **State what is FAMILIAR vs what is NEW.** Which mechanics have already been confirmed in prior levels of this game? What looks different or unconfirmed at this level? This prevents re-deriving known rules and flags genuine novelty early.

- What objects are present? (colour, size, position)
- What does a win look like? Is there an obvious symmetry or alignment to achieve?
- Any special objects — dividers, markers, toggles?

**Required: print the rendered grid** (use the char-map render script) so both you and the user can see the full layout before proceeding.

**Required: produce a zone map.** Annotate every distinct region by row range, column range, colour, and whether it is accessible to the moving pieces (track) or not (background/void). Example format:
- Rows 0: black border
- Rows 1–5, cols 0–31: pink background (not accessible)
- Rows 6–17, cols 6–29: black outer ring (track)
- etc.

**Required: produce a novel description of the grid's purpose.** In one or two sentences, describe what this grid IS as if explaining it to someone who has never seen it — not just what colours are where, but what the overall structure suggests about how the game works and what the goal might be. This must be consistent with every zone in the map. If you cannot produce a consistent description, flag the contradiction before proceeding.

**Required: answer the four scene-comprehension questions.** These must be answered from observation alone, before any action is taken. They are the output of understanding the scene, not a description of it.

1. **What does winning look like?** Describe the win state as a visual: "the grid will look like X." If you cannot describe it, you have not understood the scene — look harder before proceeding.
2. **What are the objects and their roles?** Classify every distinct object into one of four categories:
   - *Agent*: what you control or move
   - *Target*: what defines the win state
   - *Obstacle*: what currently prevents the win
   - *Mechanism*: what controls, gates, or enables state transitions (e.g. a marker that freezes blocks, a band that opens or closes, a toggle that switches modes)

   Any object that fits none of these four categories means your model is incomplete — look again. **Mechanisms are the most frequently missed objects and the most likely to be the key to a level.** When a level is harder than expected, an unclassified object is almost always the reason.

   **After classifying, explicitly list all elements that are NEW at this level** (not seen in prior levels of this game, or seen but not yet confirmed to function the same way). Each new element whose role is not yet confirmed becomes a **mandatory Step 2b investigation target**. Write this list now.

3. **What is the gap?** One sentence: "To win, [agent] needs to [transformation], and currently [obstacle/mechanism] prevents or enables this."
4. **What is the simplest explanation?** State a candidate mechanism in plain English — not a path or a sequence, just "I think the game works by X." Prefer the simplest explanation consistent with what is visible. If you cannot state one, say so explicitly.

If any of the four questions cannot be answered from the grid alone, state that explicitly — it becomes a specific, targeted question for Step 2 to resolve, rather than leaving Step 2 as open-ended probing.

Print out your observations here. Do not proceed until you've done so. 

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
> **Required: probe interactions with every distinct colour in the grid.** If the grid contains colours beyond the background and the moving piece (e.g. red cells, markers, toggles), you MUST navigate the moving piece(s) onto or adjacent to those cells and probe all actions from that position. Probing only from the starting position is not sufficient — special cells may only react when the piece physically reaches them.
>
> **Required output before proceeding:** a printed table with one row per action (ACTION1–ACTION7), columns for each mode, stating for each: cells changed, value transitions, what moved / what toggled, and whether `available_actions` changed. Print it to the user. Only then continue to Step 3.

Probe each available action one at a time. For each, describe:
- What moved? In which direction? By how much (measured at the top-left corner, not centroid)?
- What value transitions occurred (counters, indicator cells, marker/dot patterns)?
- Did `available_actions` change? If yes, this action is a **control-scheme toggle**.

**Toggle rule — MUST NOT be skipped:** Any action that only produces a colour change somewhere or seems to do nothing is a candidate for a state change. It could be a toggle, or it could actually be two, three, four, or more state changes before getting back to the original state.  After finding it, probe all actions again in the changed state to find what becomes available. A toggle may switch the control *axis* (horizontal-only ↔ vertical-enabled) OR switch *which object* you control (e.g. divider ↔ pieces). At least two levels of ar25 use such a toggle. Do not assume a direction or object is unavailable until every toggled state has been probed.

**The Step 2 probe script must include automatic second-pass probing.** For any action that produces a non-movement state change (any transition beyond the moving piece appearing/disappearing in its new position), the script must replay to that changed state and probe all actions again from it, printing the results. The toggle follow-up must be built into the script itself — not left to be recognised from the output afterwards.

Action 6 is a **click** that requires an (x, y) coordinate on the 64×64 grid. It is **context-sensitive**: it often only acts when the click lands on the currently-active object, and does nothing on the wrong target — so it must be tested against every distinct object, not one arbitrary point.

**Step 2 close-out checklist — required before proceeding to Step 2b:**
1. Every distinct colour in the grid has been physically tested: a block was navigated to that cell type and a movement probe run from there. "Looks inaccessible" is not sufficient — verify by attempting entry. This includes red cells, marker cells, unusual wall colours, and any cell that is not the plain background or the moving block.
2. Write out all confirmed Step 2 findings as a numbered list. This list feeds directly into the Step 2b Element Function Audit.

Print out your observations here. Do not proceed until you've done so.

---

### 2b — Element Function Audit (HARD GATE between Step 2 and Step 3)

The Action Table records what actions do. The Element Function Audit records what each game **object** is for. These are different questions. You can completely characterise every action and still miss the function of the object that is the key to the level.

**Required: produce a Function Table with one row per distinct game element** — not per action, but per physical object or zone in the grid. Include every element classified in Step 1 (all four categories) plus any element whose behaviour was observed during Step 2 probing.

| Element | Colour/value | Confirmed function | Grade |
|---------|-------------|-------------------|-------|
| lt-blue blocks | 10 | move via ACTION1–4 | CONFIRMED |
| blue marker | 9 | example: freezes blocks when clicked; moves in frozen state | CONFIRMED |
| orange band | 12 | example: blocks passage unless opened by X | CONFIRMED |
| ... | ... | ... | ... |

**Grade definitions:**
- **CONFIRMED**: function has been directly observed and verified by probing
- **HYPOTHESISED**: function is inferred from indirect evidence — must be explicitly flagged; relying on a HYPOTHESISED function in Step 3 is permitted only if the hypothesis is stated and the risk acknowledged
- **UNKNOWN**: no confirmed or hypothesised function yet

> ## 🚨 HARD GATE — no element may remain UNKNOWN before Step 3.
>
> For each UNKNOWN element: write the smallest possible probe that would confirm or refute a hypothesis about its function. Run it. Update the table. Only proceed to Step 3 when every element is CONFIRMED or HYPOTHESISED.
>
> **This gate exists because the most common cause of a stuck investigation is an element whose function was never confirmed.** The blue marker in m0r0 L6 is the canonical example: it was probed, it produced an observable effect, and its function was not written down — so when the solution required using it as a blocker, that capability was invisible.
>
> The fix is not more brainstorming. The fix is: if you are stuck, find the element in your audit table whose function is UNKNOWN or HYPOTHESISED and probe it specifically in context.

Print the completed Function Table before proceeding. This is the mandatory training mode hard stop before Step 3.

### 3 — Hypothesis (audit-driven, written in conversation)

**Before writing anything, read these memory files:**
- `memory/feedback_hypothesis_reasoning.md`
- `memory/feedback_hypothesis_evaluation.md`

> ## ⚠️ CRITICAL RULE — the hypothesis must be derivable from the Element Function Audit.
>
> A hypothesis that requires an element whose function is UNKNOWN is not a hypothesis — it is a wish. A hypothesis that requires an element whose function is HYPOTHESISED must flag that reliance explicitly. If you cannot derive the full sequence from CONFIRMED elements, the correct response is to return to Step 2b and confirm the missing element — not to proceed and hope.
>
> **The specific failure mode to avoid:** forming a candidate solution first and then checking whether it is consistent with the audit. That is backwards and produces commitment bias — you become invested in a path that may not survive contact with the evidence. The correct direction is: audit → gap → mechanism match → sequence.

**Build the hypothesis in this order — do not skip steps:**

**1. Restate the gap.** Copy it from Step 1 Q3. If the level has multiple stages, list each stage's gap separately. This is the problem to solve — every subsequent step is about solving it.

**2. For each gap component, find the matching mechanism.** Ask: *"Which CONFIRMED element in the Function Audit closes this gap?"* Do not brainstorm — survey the table. For each gap component, write: "Gap: [X]. Mechanism: [Y from audit]. Because: [confirmed function of Y]."

   If a gap component has no matching CONFIRMED element: it is unresolved. Return to Step 2b, investigate the most likely candidate specifically, and confirm its function before continuing.

**3. Identify sequencing constraints.** Do any mechanisms need to be activated before others become usable? (e.g. "the band must be open before the block can pass through it.") List the dependencies explicitly.

**4. Order the mechanisms into a sequence** in dependency order: prerequisites first, gap-closers last.

**5. State the sequence in plain English.** One numbered step per action or state change. For each step: which element is being used, why (what gap component it closes), and what the expected state is afterwards.

Never conclude that an obstacle is insurmountable without running an experiment — mathematical reasoning about impossibility has been wrong before (m0r0 L5: the column invariant "proof").

**Before proceeding to Step 4 — three checks:**
1. Every step in the sequence uses an element whose function is CONFIRMED. Any HYPOTHESISED element is explicitly flagged with the assumption being made.
2. Does the complexity match the level number? A Level 1 sequence should be simple. A complex sequence at Level 1 almost certainly means the model is wrong — look for the simpler explanation.
3. For maze-type games: render the grid and confirm the proposed path is physically possible before writing any code.

Only proceed to Step 4 with the hypothesis you would genuinely bet on.

**If no sequence can be derived from the audit:** the audit is incomplete. Do not return to Step 1 or brainstorm — return to Step 2b. Ask "which element in the table is still UNKNOWN or HYPOTHESISED?" and investigate that element. Maximum two return cycles before escalating to the user.

Print out your reasoning here. Do not proceed until you've done so.

### 4 — Write code to test the hypothesis

Write a short Python script (not a notebook cell) to:
1. Load the game and replay to the current level
2. Execute the proposed sequence
3. Print before/after positions and whether the level completed

**After-action grid inspection (Step 4 guard)**

Before running the full sequence, validate the first click:
1. Record the expected state: which tiles should change and how.
2. Execute the click. Compare the actual grid to expected using the full cell-change instrument (not just bounding box).
3. If actual matches expected → proceed with the full sequence.
4. If **any** click in the sequence produces an unexpected result → STOP. Return to Step 2, re-probe the failing action, and revise the hypothesis.
5. If the revised hypothesis still fails at any point → switch to **step-by-step inspection**: after every click, compare actual to expected and correct the sequence in-place before continuing.

Report the result. If it works, give the ACTIONS list for Cell 7. If not, describe what position was reached vs what was needed.

**Step 4 failure protocol — when the test fails at action N:**
1. Identify exactly which element's function the failure exposed as wrong or incomplete.
2. Return to the Element Function Audit — downgrade that element to UNKNOWN.
3. Write a targeted probe for that element specifically and run it (use the "fill gaps minimally" principle — one probe, one question).
4. Update the Function Table with the confirmed function.
5. Return to Step 3 and re-derive the hypothesis from the corrected audit.

**Do NOT brainstorm variations on the failed path.** A failed Step 4 means the model was wrong — the fix is to correct the model, not to try paths around the wrong model. Brainstorming variations on a wrong model deepens commitment to the wrong direction and wastes investigation budget.

In Training Mode: after a failure, print the updated audit table and the revised hypothesis, then stop for user input. In Evaluation Mode: revise and re-test up to three times; if no solution, move on and print where you reached.


---

## Recurring structural patterns in ARC3

**Control-scheme change state.** One action (often a colour-flip or marker change) switches the game between different modes. In ar25 levels 2+: ACTION5 flips a colour AND switches from horizontal-only to vertical-enabled. When directional actions appear to do nothing, look for the change state first.

**Compound objects.** Multiple colours that always move together (e.g. an L-shape + embedded markers). Measure step size by top-left corner movement, not centroid.

**Mirror-symmetry puzzles (the "place + reflect" family).** Several ar25 levels are won by making a figure symmetric across one or more movable **mirror bands** (a lt-blue strip that reflects everything on one side onto the other as vdk-grey). The recipe: place the black piece(s) to fill part of the yellow target, then move each band onto the figure's symmetry axis so the reflection completes the rest. One band = a single mirror; two perpendicular bands = **4-fold symmetry** (each placed piece is reflected into 4 copies). The control that moves a band is one state of the multi-state ACTION5 cycle.

> ## ⚠️ THREE BIG LEARNINGS for mirror-symmetry levels (ar25 L5–L7). Internalise these — they each unblocked a level only after real effort was wasted.
>
> **1 — Find the axes with the CENTROID, never the bounding-box centre.** The two symmetry axes cross at the figure's centroid: the **mean row and mean column of all target (yellow) cells**. Compute it directly — no brute-forcing, no eyeballing. (Assuming the bbox centre cost real effort on L6, which was symmetric about col 19, not col 22. On L7 the centroid was exactly (row 22, col 37) — that is where the two bands must cross.)
>
> **2 — Identify the ACTUAL symmetry; test rotations (e.g. 90°, 180°, 270°), not just mirrors.** Two perpendicular mirror bands compose into a **180° rotation**, and many figures are symmetric under a *rotation* but NOT under any mirror alone. At the centroid, measure all three match fractions — mirror-about-col, mirror-about-row, AND 180°-rotation — and believe the data. L7 scored only 0.71 on each mirror but **1.00 on rotation**; testing only mirror symmetry invented a phantom "gap" and sent the analysis down a blind alley for a long time. Place the pieces for the symmetry the figure *actually* has.
>
> **3 — The win could be to COVER every target cell, NOT to match piece shapes to the target.** Do not waste time forcing exact tilings or requiring each piece's orbit to be a *subset* of the target. The pieces are reflected by the bands (one band → 2 copies; two bands → 4-fold), and you only need the union of those reflected copies to **cover every target square** — the black is allowed to overflow far beyond the target shape. On L7 the winning placement spilled 40 boxes outside the yellow; every search that demanded subset/exact-match found nothing, while "cover, overflow allowed" solved it immediately.
>
> **Process:** in Training Mode, a failed hypothesis is a STOP — report it and ask, don't grind through more variations. On L7 each decisive insight (centroid, it's-a-rotation, cover-don't-match) came from the user; grinding between them wasted time and trust.

**Rule stability across levels.** Once a rule has been confirmed to win a level, treat it as correct for subsequent levels of the same game until there is strong evidence it has changed. Don't reopen confirmed rules without cause — focus on what's *new* at the current level. If a previously confirmed rule appears to fail, look for a *new* mechanic layered on top before concluding the rule has changed.

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
When In training mode Proceed without asking for confirmation on all local work except for the hard stops listed below.

**Training mode hard stops — wait for user confirmation before continuing:**
1. After Step 1 is printed — before starting Step 2 probing
2. After Step 2 action table is printed — before starting Step 2b Element Audit
3. After Step 2b Element Function Audit is printed — before stating Step 3 hypothesis
4. After Step 3 hypothesis is printed — before writing any Step 4 code
5. After a level completes (success or failure)

When not in training mode Proceed without asking for confirmation on all local work 

In Training Mode, At the end of a level If successful, print out the result and wait for confirmation to proceed. If not successful revise the hypothesis step 3 and print out the new hypothesis and stop for user input. 

If in Evaluation Mode, Print out the result and continue. if not successful revise the hypothesis and re-test up to three times, and if there's no solution, move on. Print out where you're up to.

**After each level completes, check `win_levels` before starting the next level.** If `levels_completed >= win_levels`, the game is finished — do not attempt a further level. The victory screen may render as a grid that looks like a puzzle; ignore it.


## Memory policy

Working notes about the current game (confirmed mechanics, per-level findings, open questions) live in a **per-task memory file** at `.claude/projects/…/memory/`. This file survives logoff and context compaction — prior level findings are available when returning to the same game in a new session.

**When switching to a new game: clear the per-task memory file** so it doesn't contaminate the fresh task.

Only insights general enough to apply across *multiple* games belong in CLAUDE.md. Per-game findings stay in the per-task memory file and are cleared with it.

---

## Key questions for ARC3 research

1. Is the control-scheme change state operation a universal mechanic across all 25 games?
2. How many control states does each game have?
3. Can the world model be derived reliably from the verbal process alone?
