---
name: project-ar25-working
description: "ar25 game notes — L1-L2 solved, L3 action probing done; mirror-symmetry mechanics for L5-L7"
metadata: 
  node_type: memory
  type: project
  originSessionId: b8ee3f4f-73f4-47a6-9722-3029aaac5fc3
---

# ar25 Working Notes

**Why:** Per-task memory for the ar25 ARC-AGI-3 game. Clear when switching games.

## Status
L1 and L2 solved. L3 characterised. See commit history for solutions.

---

## Mirror-symmetry levels (ar25 L5–L7)

These levels are won by making a figure symmetric across one or more movable **mirror bands** (a lt-blue strip that reflects everything on one side as vdk-grey). The recipe: place the black piece(s) to fill part of the yellow target, then move each band onto the figure's symmetry axis so the reflection completes the rest.

- One band = a single mirror; two perpendicular bands = **4-fold symmetry**
- The control that moves a band is one state of the multi-state ACTION5 cycle

### THREE HARD-WON LESSONS (each unblocked a level only after real effort was wasted)

**1 — Find the axes with the CENTROID, never the bounding-box centre.**
The two symmetry axes cross at the figure's centroid: the **mean row and mean column of all target (yellow) cells**. Compute it directly. (Assuming the bbox centre cost real effort on L6, which was symmetric about col 19, not col 22. On L7 the centroid was exactly (row 22, col 37).)

**2 — Identify the ACTUAL symmetry; test rotations (90°, 180°, 270°), not just mirrors.**
Two perpendicular mirror bands compose into a **180° rotation**, and many figures are symmetric under rotation but NOT under any mirror alone. At the centroid, measure mirror-about-col, mirror-about-row, AND 180°-rotation match fractions. L7 scored 0.71 on each mirror but **1.00 on rotation**. Believe the data.

**3 — Win by COVERING every target cell, not by matching piece shapes.**
The pieces are reflected by the bands; you only need the union of reflected copies to **cover every target square** — overflow beyond the target shape is allowed. On L7 the winning placement spilled 40 cells outside the yellow. Every search demanding subset/exact-match found nothing; "cover, overflow allowed" solved it immediately.

### Process note
In Training Mode, a failed hypothesis is a STOP — report it and ask, don't grind variations. On L7 each decisive insight (centroid, it's-a-rotation, cover-don't-match) came from the user; grinding between them wasted time and trust.
