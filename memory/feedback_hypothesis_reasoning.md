---
name: feedback-hypothesis-reasoning
description: Prompts that unblock over-complicated hypotheses and restore Level-1 simplicity; road-map method for multi-stage problems
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

When forming a Step 3 hypothesis, there is a tendency to jump to complex explanations (maze navigation, fitting blocks into openings) before considering the simplest possibility.

Two questions reliably cut through this:

1. **"Why do you think X?"** — forces examination of assumptions. On m0r0 L1, "why do you think the blocks are the same colour?" triggered the insight that *same colour = designed to merge*, leading directly to the correct hypothesis (converge twice).

2. **"This is Level 1 — what's more obvious?"** — redirects from complex mechanics to the simplest visual interpretation.

**Why:** The methodology builds up a world model from observation. The risk is treating every game as maximally complex. Level 1 is designed to be solved by a straightforward observation, not maze-solving logic.

**How to apply:** Before stating a Step 3 hypothesis, explicitly ask: "What is the simplest possible win condition consistent with what I've observed?" State that first, then note more complex alternatives. If the simple version fits Level 1, go with it.

---

## Road-map method for multi-stage problems (added after m0r0 L5)

**Why:** On L5 I kept treating Step 3 as open-ended brainstorming, which led to reasoning about why things were impossible rather than finding the path. The fix is to build the road map *inward from the goal*, not outward from the start.

**The method (for maze-type games):**

1. **Identify the final state** — what does winning look like, precisely?
2. **Identify potential routes** — what paths could physically connect start to finish?
3. **Identify obstacles on each route** — what walls, barriers, or invariants block each stage?
4. **Identify how to overcome each obstacle** — ask: "Which already-confirmed Step 2 mechanism produces a positive contribution toward the needed state change?" Not: "is there any way?" but: "which specific thing I already know about does this?"
5. **First step** — once the road map is drawn, the first step is the one confirmed mechanism that starts the first stage.

**Key discipline:** Do not jump to step 5 until steps 1–4 are complete. And do not brainstorm step 4 open-endedly — survey only the confirmed Step 2 findings.

**Pattern that worked on m0r0 L1:**
- Two identical lt-blue blocks, one per half
- Same colour → two halves of one thing → need to merge
- ACTION4 converges by 10 cols per press; gap starts at 15, so 2 presses = overlap
- No maze navigation needed

**Pattern that worked on m0r0 L5 (once correctly applied):**
- Goal: both blocks overlap at top (rows 6–9)
- Route: A through left gates (orange then green), B through right shaft, converge at top
- Obstacle 1: orange gate geometry — A at col 2 when B on orange marker
  - Mechanism: pink gap pins A at col 18 → sum breaks to 76 → A in orange gap
- Obstacle 2: green gate geometry — A drifts to col 26 when B moved to green marker
  - Mechanism: *same class* — orange wall right edge pins A at col 18 while B walks to green marker
- First step: DIVERGE×2 (puts A on switch, opens right shaft for B)

**The specific failure to avoid:** Proving something is impossible without testing it. If mathematical reasoning says X can't work, *run the experiment first*. The column invariant "proof" on L5 was wrong — the experiment showed sum=76 was achievable. Never conclude impossibility without experimental verification.
