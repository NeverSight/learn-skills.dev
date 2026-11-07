---
name: clean-layers
description: Audits selected frame(s) for three structural cleanup patterns — deletable hidden layers, collapsible single-child auto layout chains, and fixed-width children that could be fill-width — then lists every finding for confirmation before applying any fix. Use when the user wants to tidy up, clean up, or streamline a frame's layer structure, or asks about redundant wrappers, hidden layers, or fill vs fixed width. Do NOT use for visual or content edits — this skill only changes layer structure.
disable-model-invocation: true
---

## Step 1 — Gate

If `figma.currentPage.selection` is empty or contains no frames, stop and ask the user to select one or more frames. Do not proceed.

If multiple frames are selected, scan each and report findings grouped by frame.

## Step 2 — Scan

**Run all three checks in a single `evaluate_script` call** that walks the tree once and returns structured JSON for all three categories. Do not make separate calls per check.

Read-only — nothing is written in this step. If data isn't available for a check (e.g. prototype reaction data), note it once in the report rather than treating "couldn't check" as "clean."

**Check 1 — Deletable hidden layers:** `visible = false`. Skip if the ancestor chain includes a component instance. Skip if the layer is a known prototype interaction target — if not detectable, say so rather than treating it as safe.

**Check 2 — Redundant single-child auto layout chain:** A chain of 2+ auto layout frames where each frame's only child is another auto layout frame. Flag for collapsing **only if lossless**: merged frame takes layout properties (direction, gap, padding, alignment, sizing) from the **innermost** frame; carries forward any non-default visual property (fills, strokes, effects, corner radius, opacity, rotation, clipping) from any wrapper. If two wrappers set different values for the same property, flag as "needs manual review: conflicting `<property>`" — do not auto-resolve.

**Check 3 — Fixed-width child matching parent's content width:** A direct child of an auto layout frame with `layoutSizingHorizontal = FIXED` and a width equal to the parent's content width (parent width minus horizontal padding). Flag as "could be Fill" — robustness suggestion, not a visual fix.

**Constraints:** Never flag or touch any layer inside a component instance. Only flag lossless fixes — if uncertain, surface as "needs manual review."

## Step 3 — Report and Confirm

Do not change anything yet. Omit a section entirely if it has zero findings. If a frame has no findings at all, write "No cleanup opportunities found in [frame name]."

```
# Layer Cleanup — [Frame name(s)]

## [Frame name]

### 🗑️ Deletable Hidden Layers ([count])
1. `[Layer path]`

### 🧱 Redundant Auto Layout Chains ([count])
1. `[Outer wrapper path]` → collapses using [innermost frame]'s layout[, carries: property=value]
2. `[Chain path]` — needs manual review: conflicting `[property]`

### 📏 Fixed-Width → Fill-Width Candidates ([count])
1. `[Layer path]` — Fixed at [width]px, matches parent content width

---
**What would you like me to fix?** (all / by category / specific numbered items)
```

## Step 4 — Apply

Apply only confirmed findings in this order: hidden layers → auto layout collapses → fill-width changes. For Check 2 conflicts mid-batch, stop on that item, ask which value to keep, then continue with the rest.

## Step 5 — Summary

Report counts changed per category. Note anything that needed a manual decision mid-way and why, and anything still outstanding because it wasn't confirmed.
