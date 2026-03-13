---
name: excalidraw-workflow
description: Load when building or reviewing an Excalidraw diagram. Adds an autonomous completion loop (no mid-task stops), quick planning before drawing, element-by-element build order for live progress, and a review checklist that catches overlaps, truncated text, and unconnected arrows before finishing.
---

# Excalidraw Workflow

## 0. Autonomous Completion Loop (No Mid-Task Stops)

Use this loop whenever the request is to build, improve, or fix anything substantial.

1. Capture the target outcome in 2-5 concrete checkpoints.
2. Execute one checkpoint immediately (do not pause after planning).
3. Prove the checkpoint with evidence (for diagrams: `describe` + viewport/screenshot spot-check).
4. Fix any issue before starting the next checkpoint.
5. Continue until all checkpoints are complete, then do one final verification pass.

**Default behavior:** do the work continuously. Do not stop between checkpoints for routine permission requests.

**No confirmation pauses:**
- Do not pause after "plan" to ask routine permission.
- Do not pause after one command output when more checkpoints remain.
- Ask only when truly blocked by missing credentials/secrets or irreversible production risk.

**When working in a git repo and the user asks to ship:**
- After each verified checkpoint, stage and commit with a focused message.
- Push after the final verification pass (or at each checkpoint if the user requested incremental pushes).

**Checkpoint proof standard (each checkpoint must include all):**
1. Action performed.
2. Observable evidence (`describe`, screenshot, command output).
3. Next checkpoint started immediately.

---

## 1. Quick Grid Plan (30 seconds, saves minutes)

Before the first draw command, decide your coordinate grid. This prevents overlaps and misaligned arrows that are painful to fix mid-diagram.

**For architecture / flowcharts** — sketch this mentally:
```
Tier 1 (y=60):   Client / Entry points      (x=80, 320, 560 ...)
Tier 2 (y=200):  Gateway / Edge             (x=80, 320, 560 ...)
Tier 3 (y=340):  Services                   (x=80, 320, 560 ...)
Tier 4 (y=480):  Data stores                (x=80, 320, 560 ...)
```
Rule of thumb: 140px vertical between tiers, 240px horizontal between columns.

**For mind maps / brainstorming**: start with the center node, assign fixed radial slots (center -> branches -> children), then draw incrementally.

**Only one thing to decide before drawing**: what is the first element and where does it go? Draw it immediately.

---

## 2. Draw Element by Element — User Can Steer in Real Time

Create each element with its own `excalidraw create` call so the user sees every shape appear live and can redirect if something looks wrong.

**Order:**
1. Background zones / containers (sets the skeleton)
2. Primary nodes one by one (main shapes)
3. Arrows one by one — only after both source and target exist
4. Detail labels / annotations last

**Example — element by element:**
```bash
excalidraw create --type rectangle --id zone-backend --x 40 --y 40 --width 500 --height 400 \
  --fill "#e9ecef" --stroke-color "#868e96" --opacity 40
excalidraw viewport --fit

excalidraw create --type rectangle --id api-gw --x 80 --y 100 --width 200 --height 60 \
  --text "API Gateway" --stroke-color "#9c36b5" --fill "#eebefa"
excalidraw viewport --fit

excalidraw create --type rectangle --id db --x 80 --y 260 --width 200 --height 60 \
  --text "Database" --stroke-color "#0c8599" --fill "#99e9f2"
excalidraw viewport --fit

excalidraw create --type arrow --x 0 --y 0 --start api-gw --end db
excalidraw viewport --fit
```

> **Rule**: something must appear on canvas within your first tool call.
>
> **`excalidraw batch` is best** when you have a complete diagram ready — arrow bindings are computed across the whole set at once, giving better geometry. For live incremental drawing, use individual `create` calls.

### Mindmap-specific build rule (for clean radial maps)
If the request is "mindmap" and the branch count is known in advance, prefer:
1. Build nodes first with fixed radial coordinates (center -> branches -> branch children).
2. Add all arrows only after all node IDs exist.
3. Run `viewport --fit` and visual QA before calling done.

This prevents the scattered-node look caused by improvising positions mid-build.

---

## 3. Fix As You Go — Don't Save It For the End

**Before every `excalidraw create`:**
- Width big enough? `max(160, charCount * 11 + 40)`. Go wider when unsure.
- Multi-word labels: `max(160, longestWord * 11 + 80)`.
- Both shapes exist before drawing the arrow?
- At least 60px gap between this shape and its neighbors?

**Fix immediately:**
```bash
excalidraw update <id> --width 220         # text truncating
excalidraw update <id> --x 320 --y 180    # overlapping neighbor
excalidraw viewport --fit
```

**Arrow passes through a box?** Shapes were too close, or arrow wasn't bound. Delete it, increase gap, recreate with `--start <id> --end <id>`.

**Overlapping elements?** Use `excalidraw distribute` to space them evenly.

Run `excalidraw describe` at each checkpoint boundary (not after every element) to verify IDs and branch connectivity.

---

## 4. Review Before Finishing

Run this before calling the diagram done:

```bash
excalidraw describe
```
Check:
- [ ] Every shape has a label
- [ ] Every arrow connects two shapes (not floating)
- [ ] No element IDs are duplicated
- [ ] Text isn't truncated (shapes wide enough)

```bash
excalidraw viewport --fit
excalidraw screenshot --out /tmp/final.png
```
Visual check — look for:
- [ ] No overlapping shapes
- [ ] Arrow lines don't pass through boxes
- [ ] Consistent color/sizing within each tier

Mindmap-specific check (if applicable):
- [ ] Center node is visually central
- [ ] First-level branches radiate in distinct directions
- [ ] Each branch has continuation depth (at least one child)
- [ ] No floating labels outside node bounds
- [ ] Branch spacing is balanced (no one side collapsed)
- [ ] First-level branch center distances are within about 80px of each other unless intentional emphasis is stated

**Save before stopping:**
```bash
excalidraw export --out backup.excalidraw
```
Canvas state and snapshots are both in-memory — lost on server restart.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `503 No frontend client connected` | Open `http://localhost:3000` in a browser. `viewport`, `screenshot`, and `mermaid` require a live browser tab. |
| Arrow not connecting | Use `--start <id> --end <id>` — both shapes must exist before creating the arrow |
| Elements scattered / overlapping | Run `excalidraw distribute id1 id2 id3 --direction vertical` to space evenly |
| Elements lost after restart | Run `excalidraw export --out backup.excalidraw` before stopping the server |
| Fill looks sketchy/hatched | Add `--fill` color with `"fillStyle": "solid"` in batch JSON |
