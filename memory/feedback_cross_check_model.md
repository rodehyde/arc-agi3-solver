---
name: feedback-cross-check-model
description: Cross-check additive models against combined-measurement tests before declaring them confirmed
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

Cross-check any model built from individual measurements against all available combined-measurement observations before treating the model as confirmed.

**Why:** In tn36 L1, an offset table was built from individual toggle measurements. A combined-toggle test ("Remove full D group") returned a result that contradicted the table by exactly 1 row. The discrepancy was never noticed because the test result and the table were never explicitly compared. This locked in a wrong model that produced an incorrect reachability conclusion, causing wasted analysis.

**How to apply:** After building any additive model (offset table, contribution table, per-element rate), write one sentence: "Now check: does every combined test result in this session agree with this model's prediction?" If any combined result disagrees with the sum of the individual contributions, the individual measurements contain an error — not the combined test.
