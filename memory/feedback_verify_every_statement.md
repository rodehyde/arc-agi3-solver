---
name: feedback-verify-every-statement
description: Every statement in the analysis must be backed by verified data — descriptions are hypotheses until the data confirms them
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

Every statement made in the analysis must be backed by verified data, not inference or visual pattern-matching.

**Why:** In m0r0 L5 Step 1, concluded the right shaft had "side passages" by seeing that the purple obstacle didn't span the full shaft width — but didn't check that the remaining cells were black (value=5). They were lt-pink background, equally impassable. The claim stood unchallenged because no empirical test was run to refute it.

**How to apply:**
- If a claim can be checked by reading cell values → check before stating it as fact.
- If a claim can be checked by running an action → run it before stating it as fact.
- If a claim cannot yet be verified → say "I think" / "appears to be" and flag it as an open question.
- Specific trap: "not the obstacle colour" ≠ traversable. Only value=5 (black) cells are traversable. Background (pink=6, lt-pink=7, etc.) is also impassable.
