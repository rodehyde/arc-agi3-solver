---
name: feedback-hypothesis-evaluation
description: "Evaluate a hypothesis before testing it — likelihood, alternatives, level-appropriate simplicity"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

Before writing any Step 4 code, explicitly evaluate the hypothesis rather than jumping straight to testing it.

**Why:** On m0r0 L1, a "converge to merge" hypothesis was tested immediately without assessing whether it was likely or consistent with prior observations. It failed because the center was a wall — something already noted in Step 1. A one-minute evaluation would have caught this.

**How to apply — four checks before Step 4:**
1. **Consistency:** Does the hypothesis contradict anything already observed in Steps 1 or 2? If yes, revise before testing.
2. **Alternatives:** Name one or two other possible win conditions. Explain why your hypothesis is more likely than those.
3. **Level-appropriate simplicity:** Level 1 should have a simple, obvious win. Don't propose a complex path when a simple one is consistent with the evidence. Complexity should increase with level number.
4. **Physical plausibility (maze games):** If movement is constrained by structure, render the grid and confirm the proposed path is navigable before writing code.

Only proceed to Step 4 with the hypothesis you would genuinely bet on — not the first one that comes to mind.

See also [[feedback-hypothesis-reasoning]] for the complementary prompts that help form a good hypothesis in the first place.
