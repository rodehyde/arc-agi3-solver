# CLAUDE.md — ARC-AGI-3
*Last updated: 2026-06-22*

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

ARC-AGI-3 is a set of interactive 2D game environments. An agent must play each game, infer the rules from observation, and complete it. The metric is **RHAE** (Relative Human Action Efficiency): (human_baseline_actions / agent_actions)², so a perfectly efficient agent equals the human baseline score of 1.0. Frontier LLMs score ~0.18–0.51%.

The central challenge: **the rules are unknown at the start of each game.**

The structured approach must be used throughout. Any creativity occurs within that approach. The only information allowed is the grid and the available actions — no source code, no external information.

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
- **Observation API**: `obs.frame[-1]` is the top visible layer. Key fields: `obs.available_actions`, `obs.levels_completed`, `obs.win_levels`. Do NOT use `obs.grid`.
- **Step 1 script discipline**: one comprehensive inspection script — explore obs attributes, display bounding box, print values present — in a single pass. Never suppress stderr.
- **Grid colours**: 0=white 1=lt-grey 2=md-grey 3=dk-grey 4=vdk-grey 5=black 6=pink 7=lt-pink 8=red 9=blue 10=lt-blue 11=yellow 12=orange 13=maroon 14=green 15=purple

---

You are in training mode unless told otherwise.

---

## Mandatory step markers — enforced gate

Before writing ANY code for a level, these markers MUST appear in conversation output, in order:

```
STEP 1 COMPLETE — [scene description + novel elements listed]
STEP 2 COMPLETE — ACTION TABLE: [full table]
ELEMENT AUDIT COMPLETE — FUNCTION TABLE: [table with all elements graded]
STEP 3 HYPOTHESIS: [sequence derived from audit, in plain English]
```

Not optional. Not abbreviatable. Not post-hoc. Present in both training and evaluation mode.

When something difficult is encountered — including when you've spent more than two minutes on a problem — print an interim statement and wait to be told to proceed.

---

## Core verification rules — apply everywhere, every step

**1. Check before stating.** If a claim can be verified by reading cells or running an action, verify it first. Unverified claims are marked "I think" or "appears to be."

**2. Three grades — never collapse them.**
- *Idea*: untested
- *Hypothesis*: inferred from evidence, not directly confirmed
- *Confirmed fact*: directly observed

A subsequent step must never treat a lower grade as load-bearing.

**3. Eliminating a hypothesis requires evidence.** Name the specific observation that rules it out and verify it is correct. Circumstantial evidence is not ruling-out evidence.

**4. Cross-check additive models.** After building a model from individual measurements, explicitly ask: "Does every combined-measurement test in this session agree with this model?" A discrepancy exposes an error in the individual measurements.

---

## Data-reading discipline — required before treating any probe result as evidence

For every probe result that feeds a hypothesis, write these two lines explicitly:

> **Data says:** [literal values / counts / positions / final state from the output]
> **I derive:** [the conclusion drawn from those values]

These must be genuinely separate sentences. If "Data says" contains inference, you are not reading data — re-read the raw output.

**Canonical failure (tn36 L5):** Zone 4 left legend showed 6 bars active in group 2's final state. I wrote "Zone 4 adds 4 bars" (delta, not state) and clicked only 4 for the target group. Correct reading: "Data says: rows 33,35,39,41,45,47 all active for group 2" → "I derive: click all 6 for group 6."

---

## Per-level analysis process

**Follow this sequence for every level. Do not skip ahead.**

### 1 — Describe the scene (written in conversation)

Games are of two types so far:
- A player moves around the grid and performs actions.
- No player — click on elements within the grid.

If the type is unclear, stop and state why.

Write in words:
- **What is FAMILIAR vs what is NEW** — which mechanics are confirmed from prior levels? What is different or unconfirmed?
- What objects are present? (colour, size, position)
- What does a win look like?
- Any special objects — dividers, markers, toggles?

**Required: print the rendered grid** (char-map render script).

**Required: produce a zone map** — every distinct region by row range, column range, colour, and accessibility (track vs background/void).

**Required: one-sentence purpose description** — what this grid IS, not what colours are where. Must be consistent with every zone. Flag any contradiction before proceeding.

**Required: answer the five scene-comprehension questions from observation alone:**

1. **What does winning look like?** Describe the win state as a visual. If you cannot, look harder.
2. **What are the objects and their roles?** Classify every object as: *Agent / Target / Obstacle / Mechanism*. Any object fitting none of these four means the model is incomplete. **Mechanisms are most frequently missed.** List all NEW elements explicitly — each becomes a mandatory Step 2b investigation target.
3. **What is the gap?** "To win, [agent] needs to [transformation], and currently [obstacle/mechanism] prevents or enables this."
4. **What is the simplest explanation?** One candidate mechanism in plain English.
5. **What carries over? (L2+)** State the prior level's confirmed solution. Does the current level RESET it or BUILD ON it? What is the concrete evidence? **Default: the prior solution IS a required sub-component.** Treat this as true until there is explicit evidence otherwise.

If any question cannot be answered from the grid alone, state it explicitly — it becomes a targeted Step 2 question.

> **TRAINING MODE HARD STOP — print Step 1 complete, wait for confirmation.**

---

### 2 — Work out the actions (written in conversation)

**Reason before probing.** Before writing any Step 2 script:

1. Derive the win path geometrically from Step 1.
2. Check confirmed mechanics first — don't re-probe what a prior level confirmed.
3. Connect structural mismatches to new mechanics directly — a mismatch is a pointer to the new mechanic, not an open question.
4. Before any probe, complete: "I am probing X because Y is confirmed and Z is genuinely unknown." If you cannot, don't run the probe.

**🚧 ACTION TABLE GATE — required before Step 2b.**

Probe every available action. Standards:

1. **Any-cell-change instrument** — full grid compare before/after. Report: cells changed, bounding box of change, every value transition (`0→9:20, 11→12:1`). Movement-only tracking is forbidden as the basis for "no effect."
2. **Every action 1–7** in every control mode (re-probe after each toggle).
3. **ACTION6: every distinct object** — not one arbitrary point. "No effect" requires testing every distinct target.
4. **All frames** — count frames: 1=no event, 5–6=animation, 8=panel fire, 11+=completion. Read every frame. A button appearing inert in frame[-1] may drive a full animation.
5. **"No effect" is a conclusion** — only after the any-cell-change instrument shows zero changed cells.
6. **Toggle rule** — any colour-change or apparent no-op may be a state toggle. Probe all actions again in the changed state. Build this second-pass into the script.
7. **Probe every distinct colour** — navigate to each colour type and probe from there.

Apply the data-reading discipline to every probe result before using it as evidence.

> **TRAINING MODE HARD STOP — print Action Table, wait for confirmation.**

---

### 2b — Element Function Audit (HARD GATE between Step 2 and Step 3)

The Action Table records what actions do. The Element Function Audit records what each **object** is for. These are different questions.

**Required: produce a Function Table with one row per distinct game element:**

| Element | Colour/value | Confirmed function | Grade |
|---------|-------------|-------------------|-------|
| example: lt-blue blocks | 10 | move via ACTION1–4 | CONFIRMED |

**Grade definitions:**
- **CONFIRMED**: directly observed
- **HYPOTHESISED**: inferred — flag explicitly; Step 3 reliance requires stating the assumption
- **UNKNOWN**: no confirmed function yet

**🚨 No element may remain UNKNOWN before Step 3.** For each UNKNOWN: write the smallest probe that would confirm or refute a hypothesis. Run it. Update the table.

**Self-check before concluding any element is irrelevant:** "What would be the point of this element if my current model is correct?" If the answer is "no point," the model is wrong.

**Pre-activated elements** are half-finished configurations from a prior level. Ask: "What does this complete, and what is the missing half?" Never treat them as decorative.

> **TRAINING MODE HARD STOP — print Function Table, wait for confirmation.**

---

### 3 — Hypothesis (audit-driven, written in conversation)

**Before writing, read:**
- `memory/feedback_hypothesis_reasoning.md`
- `memory/feedback_hypothesis_evaluation.md`

**The hypothesis must be derivable from the Element Function Audit.** A hypothesis requiring an UNKNOWN element is not a hypothesis — it is a wish. Direction of reasoning: audit → gap → mechanism match → sequence. Not the reverse.

Build in this order:

1. **Restate the gap** (from Step 1 Q3). List each stage separately.
2. **Match each gap component to a mechanism**: "Gap: [X]. Mechanism: [Y from audit]. Because: [confirmed function of Y]." No matching CONFIRMED element → return to Step 2b.
3. **Identify sequencing constraints** — what must happen before what?
4. **Order mechanisms** in dependency order.
5. **State the sequence in plain English** — one numbered step per action: which element, why (what gap it closes), expected state afterwards.

Apply the data-reading discipline for each mechanism: "Data says: [what the audit confirms about this element]" → "I derive: [why this closes the gap]."

**Before proceeding to Step 4 — four checks:**
1. Every step uses a CONFIRMED element (or flags a HYPOTHESISED assumption).
2. Complexity matches the level number — a complex L1 sequence almost certainly means the model is wrong.
3. For maze-type games: render and confirm the path is physically possible.
4. **Mechanism-first check**: for every click, complete "This click operates [mechanism] via [trigger] to produce [state change]." If you cannot, remove the click.

> **TRAINING MODE HARD STOP — print hypothesis, wait for confirmation.**

---

### 4 — Write code to test the hypothesis

Write a short Python script to:
1. Load the game and replay to the current level
2. Execute the proposed sequence
3. Print before/after state and whether the level completed

**Validate the first click before running the full sequence:**
1. State the expected state — which tiles should change and how.
2. Execute. Compare actual to expected using the full cell-change instrument.
3. Match → proceed. Mismatch → STOP, return to Step 2, re-probe, revise hypothesis.
4. If revised hypothesis also fails → step-by-step inspection after every click.

**Failure protocol:**
1. Identify which element's function the failure exposed.
2. Downgrade it to UNKNOWN in the Function Audit.
3. Write a targeted probe — one probe, one question.
4. Update the Function Table.
5. Return to Step 3, re-derive from the corrected audit.

**Do NOT brainstorm variations on the failed path.** A failed Step 4 means the model is wrong. Fix the model.

Training Mode: print updated audit and revised hypothesis, stop for user input.
Evaluation Mode: revise and re-test up to three times; if no solution, move on.

---

## Recurring structural patterns in ARC3

**Control-scheme toggle.** One action switches between control modes. When directional actions appear to do nothing, look for a toggle state first.

**Compound objects.** Multiple colours that always move together. Measure step size by top-left corner, not centroid.

**Structural symmetry.** Identical structures → identical mechanics via different triggers. Map both structures to their triggers before probing. A second structure is never decorative — its trigger is the key to the level.

**Derive before probing more.** When a new operative combination is found, ask: "Does the structure now let me derive the full solution?" Only probe further if the derivation is genuinely incomplete.

**Rule stability across levels.** Once a rule wins a level, treat it as correct for subsequent levels until there is strong evidence it changed.

---

## Notebook workflow (Cell 7 is the execution cell)

- Cell 1: setup (run once per session)
- Cell 2: load a game
- Cell 3: take one action at a time (exploration)
- Cell 4: reset; `RESET_TO_LEVEL=N` replays to level N
- Cell 7: execute an ACTIONS list; completed levels auto-saved to `LEVEL_SOLUTIONS`
- Cell 8: action table from game start (useful for initial exploration)

Verbal analysis (Steps 1–3) in conversation. Step 4 code in a script. Cell 7 executes the final ACTIONS sequence.

---

## Autonomous operation

**Training mode:** proceed without confirmation on all local work except the hard stops inside each step above.

**Evaluation mode:** proceed without confirmation throughout. Three failed attempts → move on and report.

**After each level completes:** check `win_levels`. If `levels_completed >= win_levels`, the game is finished — do not attempt a further level.

---

## Memory policy

Working notes live in a **per-task memory file** at `.claude/projects/…/memory/`. Survives logoff and context compaction.

**When switching to a new game: clear the per-task memory file.**

Only insights applicable across multiple games belong in CLAUDE.md. Per-game findings stay in the per-task file.

**Write structural relationships, not specific values.** Record the relationship ("panel A's pre-activated state encodes panel B's valid configurations"), not the specific values. Re-derive values from the current level's observed state at each new level.

---

## Key questions for ARC3 research

1. Is the control-scheme toggle a universal mechanic across all 25 games?
2. How many control states does each game have?
3. Can the world model be derived reliably from the verbal process alone?
