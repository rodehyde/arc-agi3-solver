---
name: feedback-no-source-code
description: Never read game source code — destroys the observation-based methodology
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

Never read or reference game source files (environment_files/**/*.py) during game analysis.

**Why:** The entire purpose of the ARC-AGI-3 methodology is to infer game rules from observation — what is visible on screen, and how the game responds to actions. Reading internal Python variables (goal states, tag names, function names) bypasses this completely. It doesn't just give away the answer; it destroys the collaborative process of building a robust solver methodology. A real evaluation agent has no source access, so any insight from source reading is worthless for the actual challenge.

**How to apply:**
- Everything must come from the rendered grid/frame and observed action outcomes only
- Win conditions: infer from what the target sprite displays, or by probing (attempt entry, observe if blocked)
- Toggle goals: probe toggles, count hits needed, observe what the display shows
- Step counter, current rotation/colour: read from the visible display
- The only legitimate game API calls are: `env.step()`, `r.levels_completed`, `r.observation_space` (the rendered frame)
- Never access `env._game.*` internal attributes to read goal state or mechanics
- This applies in both training and evaluation mode — no exceptions
