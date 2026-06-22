---
name: feedback-data-reading
description: Separate raw observation from derived conclusion before using probe results as evidence
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

For every probe result that feeds a hypothesis, write two explicitly separate lines before using it:

> **Data says:** [literal values / counts / positions / final state from the output]
> **I derive:** [the conclusion drawn from those values]

**Why:** The canonical failure (tn36 L5): Zone 4 left legend showed 6 bars active in group 2's final state. I read it as "4 bars newly activated" (computing a delta instead of reading the final state), then clicked only 4 bars for the target group. The raw data was correct; the reading was wrong. One explicit "Data says" line would have caught it.

**How to apply:** Any time a probe result is being used to justify a click in the sequence, write both lines first. If "Data says" contains an inference or interpretation rather than literal output values, stop and re-read the raw output. The failure is almost always: confusing a delta (what changed) with a state (what is now true).
