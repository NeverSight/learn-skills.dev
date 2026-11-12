---
name: generate-avatar
description: Design a geometry-only vector avatar (one SVG silhouette path plus eye placement, as compact JSON) for the Open Bot Avatar engine from a free-form description naming a hobby, role or object. Not for raster images, icons in other formats, or styling/animation work.
metadata:
  short-description: Silhouette + eyes JSON for the avatar engine
---

# Generate avatar

Turn one free-form description ("a coach for my gym sessions", "gamedev buddy", "something for gardening") into one avatar definition JSON. Any capable model can do this.

The instructions live in one canonical, self-contained prompt shared with the editor's *Generate* copy flow: [references/system-prompt.md](references/system-prompt.md). Read it and follow it exactly; it holds the task, output schema, geometry rules, face-first proportions and reference examples. This file only adds the local validation loop.

## Workflow

1. Follow [references/system-prompt.md](references/system-prompt.md) with the user's description.
2. Write the candidate to a temp file and validate it strictly:
   `skills/generate-avatar/scripts/validate.sh --strict /tmp/avatar.json` (from the repo root; the script also works through a symlinked install). Add `--svg /tmp/avatar.svg` for a preview file if you can inspect images. `--strict` also fails when the face has too little room as the renderer draws it, or when parts meet in a small accidental ledge or notch instead of a clear step or a smooth join.
3. Fix every reported error and re-validate. Fix face-room errors by enlarging the face-bearing part, never by shrinking the eyes. Stop after three failed repair rounds and report the last errors instead of looping.
4. Reply with only the validated compact JSON on one line. The validator's stdout is the normalized form; returning either the candidate or the normalized line is fine.

Without a repo checkout the validator is unavailable; then check the definition by hand against the prompt's rules and say it is unvalidated.

## Install for other sessions

Link rather than copy so the skill stays in sync with the repo:

```bash
ln -s "$PWD/skills/generate-avatar" ~/.claude/skills/generate-avatar
ln -s "$PWD/skills/generate-avatar" ~/.codex/skills/generate-avatar
```
