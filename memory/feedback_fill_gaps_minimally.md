---
name: feedback-fill-gaps-minimally
description: "When a step has one remaining unknown, write the smallest possible script to answer just that — don't re-probe what's already established"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

When a step is nearly complete with one specific unknown remaining, identify exactly what is missing and fill it with the minimum code needed.

**Why:** On m0r0 L4 Step 2, the only unknown was "which direction does DIVERGE/CONVERGE move the marker in frozen state?" — a single 10-line probe. Instead, a comprehensive re-probe was written covering already-confirmed mechanics, wasting time.

**How to apply:** Before writing any probe script, state the specific gap in one sentence. Write code that answers only that question. If the answer could be a 10-line script, don't write a 100-line one.
