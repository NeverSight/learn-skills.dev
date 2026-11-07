---
name: test-manim
description: >
  Create teaching-quality STEM animations using ManimGL. Generates narrative-driven
  animations as 15-second chunks merged into a final video. Configurable topic,
  duration, and model name. Works with Claude Code and opencode across any model.
  Invoke: /test-manim "topic" [--duration 30|60|90|120] [--model name]
  Default duration: 30s. Primary goal: great storytelling + visual clarity.
user-invocable: true
---

# ManimGL STEM Animation Skill

Produce pedagogically-effective STEM teaching animations: narrative-first, chunk-based
(15s segments), rendered in ManimGL (manimgl v1.7+), merged into one final video.

---

## Invocation

```
/test-manim "Newton's Laws of Motion"
/test-manim "Fourier Series" --duration 60
/test-manim "Neural Networks" --duration 90 --model minimax
```

| Arg | Default | Values |
|-----|---------|--------|
| topic | required | any STEM subject string |
| --duration | 30 | 30, 60, 90, 120 (seconds) |
| --model | session model | identifier used in folder name |

---

## Phase 0 — Parse & Scaffold

Extract from invocation:
- `TOPIC` — subject string (required)
- `DURATION` — total seconds (default: 30)
- `MODEL_NAME` — folder identifier (default: derive from session context or use "claude")
- `CHUNK_COUNT` = ceil(DURATION / 15)
- `TOPIC_SLUG` = TOPIC lowercased, spaces→underscores, strip special chars

**Create project at current working directory:**

```
manim-{MODEL_NAME}/
  {TOPIC_SLUG}/
    scenes/
      chunk_01_{name}.py
      chunk_02_{name}.py
      ...
    output/
      chunks/
      final/
    assets/
    SCENE_PLAN.md
    render.sh
    merge.sh
```

Create all directories with `mkdir -p` before writing any files.
Make render.sh and merge.sh executable with `chmod +x`.

---

## Phase 1 — Narrative Planning (ALWAYS before code)

Write `SCENE_PLAN.md` completely before writing any `.py` files.

### Story Arc Requirements

Every animation must have:
1. **Hook** (first chunk): One striking visual that poses the core question
2. **Build** (middle chunks): One concept per chunk, each building on prior
3. **Resolution** (last chunk): Visual synthesis connecting all prior chunks; key insight held on screen

### SCENE_PLAN.md Template

```markdown
# {TOPIC} — Animation Plan

**Duration**: {DURATION}s | **Chunks**: {CHUNK_COUNT} × 15s | **Model**: {MODEL_NAME}

## Story Arc
- Hook: [striking opening visual — what question does it pose?]
- Build: [ordered list of concepts, one per chunk]
- Resolution: [final synthesis — what understanding has the viewer gained?]

## Visual Language
- Background: BLACK
- Primary concept color: BLUE
- Secondary concept color: YELLOW
- Accent / highlight: RED or GREEN
- Text / labels: WHITE
- Rule: one color = one concept, consistent across ALL chunks

## Chunks

### Chunk 1 — {name} (0s–15s)
- Role: Hook
- Concept: [what is demonstrated]
- Opening: [first visual the viewer sees]
- Key moment: [the reveal or insight at ~10s]
- Closing: [held frame at 15s — clean fade out]
- ManimGL objects: [list specific classes]
- Equations: [LaTeX strings if any]

### Chunk 2 — {name} (15s–30s)
- Role: Build
- Concept: ...
[repeat for each chunk]

### Chunk {CHUNK_COUNT} — {name} ({DURATION-15}s–{DURATION}s)
- Role: Resolution
- Concept: ...
- Callback: [reference to visuals from chunk 1]

## Issues Log
[fill during render phase]
```

---

## Phase 2 — Scene File Generation

Load `references/manim-gl-api.md` before writing any scene code.
Load `references/storytelling.md` during planning to shape narrative.

Write ALL chunk files before rendering any of them.

### File Naming
`chunk_{N:02d}_{slug}.py` — slug is 1–3 words from chunk name, underscored, lowercase.

### Required Scene Template

```python
from manimlib import *


class Chunk{N}{PascalName}(Scene):
    def construct(self):
        # Target: ~15 seconds total
        # Color contract from SCENE_PLAN.md — do not deviate
        pass
```

### Scene Code Rules

**Timing — target exactly 15s per chunk**
```
total = sum(all run_time values) + sum(all self.wait() values) ≈ 15
```
- Animation transitions: `run_time=0.8`–`1.5`
- Key reveals: `run_time=1.5`–`2.5`
- After every major step: `self.wait(1.5)` minimum
- Insight moment: `self.wait(3)`
- Chunk closing hold: `self.wait(2)`

**Layout — stay within camera bounds**
- Objects: x∈[-6,6], y∈[-3.5,3.5]
- Title / top label: `obj.to_edge(UP)` (y≈3.0)
- Main visual: `obj.move_to(ORIGIN)`
- Bottom caption: `obj.to_edge(DOWN)` (y≈-3.0)

**Typography**
- Math: `Tex(r"F = ma")`
- Regular text: `TexText("Newton's First Law")`
- Font sizes: title 48, body 36, caption 28
- Example: `TexText("An object at rest...", font_size=36)`

**Chunk cleanup — end of every construct()**
```python
# Safe fadeout — handles empty scene
to_fade = list(self.mobjects)
if to_fade:
    self.play(*[FadeOut(m) for m in to_fade], run_time=0.5)
```

**Quality checks — verify before moving to render**
- [ ] At least one `self.play()` call (prevents black frame)
- [ ] All objects positioned before first `self.play()`
- [ ] `self.add(obj)` if object needs to appear instantly without animation
- [ ] Cleanup block at end of construct()
- [ ] Timing estimate ≈ 15s
- [ ] No cross-file imports between chunks
- [ ] No f-strings containing LaTeX — use raw strings `r"..."`

---

## Phase 3 — Render

Write `render.sh` into the project root, then run it:

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$SCRIPT_DIR/output/chunks"

for scene_file in $(ls "$SCRIPT_DIR/scenes"/chunk_*.py | sort); do
    base="${scene_file##*/}"
    out_name="${base%.py}"

    class_name=$(python3 -c "
import ast
with open('$scene_file') as f:
    tree = ast.parse(f.read())
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        print(node.name)
        break
")

    echo "Rendering: $class_name → output/chunks/$out_name.mp4"
    manimgl "$scene_file" "$class_name" \
        -w -q --hd \
        --video_dir "$SCRIPT_DIR/output/chunks" \
        --file_name "$out_name"
done

echo "All chunks rendered."
```

### Render Error Protocol

If a chunk fails:
1. Read full error — identify exact line + error type
2. Check `references/manim-gl-api.md` error table for known fixes
3. Fix minimum code — do not rewrite whole chunk
4. Re-render only failed chunk: `manimgl scenes/chunk_NN_name.py ClassName -w -q --hd --video_dir output/chunks --file_name chunk_NN_name`
5. Log in `SCENE_PLAN.md` under `## Issues Log`

Do NOT merge until ALL chunks render without error.

---

## Phase 4 — Merge

Write `merge.sh` into the project root, then run it:

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHUNKS_DIR="$SCRIPT_DIR/output/chunks"
FINAL_DIR="$SCRIPT_DIR/output/final"
mkdir -p "$FINAL_DIR"

CONCAT_FILE=$(mktemp /tmp/manim_concat_XXXXXX.txt)

for f in $(ls "$CHUNKS_DIR"/chunk_*.mp4 | sort); do
    echo "file '$f'" >> "$CONCAT_FILE"
done

OUTPUT_FILE="$FINAL_DIR/TOPIC_SLUG_final.mp4"

ffmpeg -f concat -safe 0 -i "$CONCAT_FILE" \
    -c:v libx264 -crf 18 -preset slow \
    -pix_fmt yuv420p \
    "$OUTPUT_FILE"

rm "$CONCAT_FILE"
echo "Final video: $OUTPUT_FILE"
```

Replace `TOPIC_SLUG_final.mp4` with the actual topic slug when generating this file.

Verify output:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "output/final/TOPIC_SLUG_final.mp4"
```

---

## Phase 5 — Report

```markdown
## Animation Report: {TOPIC}

| Field | Value |
|-------|-------|
| Model | {MODEL_NAME} |
| Duration | {actual}s ({CHUNK_COUNT} chunks × ~15s) |
| Output | manim-{MODEL_NAME}/{TOPIC_SLUG}/output/final/{TOPIC_SLUG}_final.mp4 |

### What Was Created
[2–3 sentences: topic, visual approach, key animations used]

### Chunk Summary
| Chunk | Concept | Render | Notes |
|-------|---------|--------|-------|
| 1 | ... | ✓ | |
| 2 | ... | ✓ | |

### Code Quality
- ManimGL API: [correct / N workarounds needed]
- Timing: [within 2s of target per chunk / drifted by Xs]
- Color contract: [maintained / broken at chunk N]
- Cleanup: [all chunks fade cleanly / issues at chunk N]

### Issues Encountered
[list render errors and fixes — or "None"]

### Rating: X/10
[1-line justification]

### Recommendations
- [concrete improvement 1]
- [concrete improvement 2]
```

---

## Token Efficiency Rules

- Write ALL `.py` chunk files in one batch before running any render
- Load references once — `manim-gl-api.md` at Phase 2 start, `storytelling.md` at Phase 1 start
- Run `render.sh` once for all chunks — only re-render individual chunks when fixing errors
- Plan fully (Phase 1 complete) before writing any code (Phase 2)
- If topic is ambiguous, pick most common STEM interpretation, note in SCENE_PLAN.md
- Do not ask clarifying questions mid-task — decide and proceed

---

## Open-Weight Model Rules

Applied always; critical for non-Claude models:

- `from manimlib import *` at top of every file — no partial imports
- Every file self-contained — no cross-file imports between chunks
- All LaTeX as raw strings: `r"\frac{d}{dx}"` not `"\\frac{d}{dx}"`
- No f-strings containing LaTeX — backslash chars break in f-strings
- Class names: strict PascalCase, no spaces, must not start with number
- Keep each `construct()` under 80 lines — extract `_helper()` methods if needed
- Colors by name constant only: `BLUE`, `YELLOW`, `RED`, `GREEN`, `WHITE`
- Camera moves: `self.play(self.camera.frame.animate.shift(RIGHT * 2))`

---

## ManimGL vs ManimCE — Critical Differences

| Feature | ManimGL (correct) | ManimCE (wrong — will error) |
|---------|-------------------|------------------------------|
| Import | `from manimlib import *` | `from manim import *` |
| Regular text | `TexText("hello")` | `Text("hello")` |
| Math | `Tex(r"x^2")` | `MathTex(r"x^2")` |
| Create anim | `ShowCreation(obj)` | `Create(obj)` |
| Write anim | `Write(obj)` | same ✓ |
| Camera | `self.camera.frame` | `self.camera` |
| Axes / NumberPlane | same ✓ | same ✓ |
