---
name: manimate
description: Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 (default) or GIF on request.
---

# /manimate — Manim Animation Video Maker

Generate diagram and animation videos from natural language descriptions using Manim. Outputs MP4 video by default; GIF available on request.

## Usage

```
/manimate "explain how binary search works"
/manimate "show the Pythagorean theorem proof"
/manimate "visualize bubble sort step by step"
```

## Pipeline

When the user invokes `/manimate`, execute these 12 steps in order:

---

### Step 1: Parameter Inference

Parse the user's prompt and infer rendering parameters:

| Parameter | Range | Default | How to infer |
|-----------|-------|---------|--------------|
| `scenes` | 1-6 | 2 | Count distinct concepts/steps/phases in the prompt |
| `quality` | l/m/h | h | Default high; use medium for quick drafts |
| `format` | gif/mp4/both | mp4 | Default mp4; use gif or both only if user explicitly requests GIF |
| `style` | educational/minimal/cinematic | educational | Infer from the tone/subject |
| `duration_per_scene` | 5-15s | 8 | Longer for complex concepts, shorter for simple transitions |

Write to `$WORK_DIR/params.json`:

```json
{
  "prompt": "explain how binary search works",
  "scenes": 3,
  "quality": "h",
  "format": "mp4",
  "style": "educational",
  "duration_per_scene": 8
}
```

Write `$WORK_DIR/manim.cfg`:

```ini
[CLI]
quality = high_quality
format = mp4
renderer = cairo
disable_caching = True

[output]
media_dir = media
video_dir = {media_dir}/videos
images_dir = {media_dir}/images
```

> **Why `renderer = cairo`**: Cairo is the safe default for headless/CI environments. It requires no GPU, no display server, and no OpenGL context.

---

### Step 2: Preflight Checks

Verify dependencies and set pipeline-wide capability flags:

```bash
# Required: Python 3.8+
python3 --version 2>/dev/null || { echo "python3 not found"; exit 1; }

# Required: ManimCE
python3 -c "import manim; print(f'manim {manim.__version__}')" 2>/dev/null || {
  echo "manim not found. Install: pip install manim"
  exit 1
}

# Required: ffmpeg
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found"; exit 1; }

# Optional: LaTeX + dvisvgm
LATEX_AVAILABLE=false
if command -v latex >/dev/null 2>&1 && command -v dvisvgm >/dev/null 2>&1; then
  LATEX_AVAILABLE=true
  echo "LaTeX + dvisvgm available — MathTex/Tex enabled"
else
  echo "LaTeX or dvisvgm not found. Falling back to Text-only mode."
  echo "  Install: brew install --cask mactex-no-gui (macOS) or apt install texlive-full (Linux)"
fi

# Detect timeout command (used for render timeouts in Step 10)
TIMEOUT_CMD=""
if command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD="gtimeout"
elif command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout"
else
  echo "Neither timeout nor gtimeout found. Render hangs won't be caught."
fi
```

Create a **run-scoped** working directory to allow concurrent pipeline executions:

```bash
WORK_DIR=".manimate-$(date +%s)-$$"
mkdir -p "$WORK_DIR"/scenes "$WORK_DIR"/assets "$WORK_DIR"/lastframes "$WORK_DIR"/output
echo "Working directory: $WORK_DIR"
```

> **`WORK_DIR` is the pipeline root for this run.** All subsequent steps reference `$WORK_DIR` instead of a hardcoded `.manimate` path. This prevents data loss when multiple `/manimate` invocations run concurrently.

> **Pipeline-wide LATEX_AVAILABLE flag**: When `false`, scene code must NOT use MathTex or Tex — use Text() for all text, including math expressions. Render equations as Unicode or ASCII.

---

### Step 3: Story Decomposition

Break the prompt into scenes. Each scene specifies visual elements, animations, and narrative arc.

**Default to SVG icons for every real-world concept.** For each scene, identify concepts that can be icons and add them to `asset_manifest`. Every video should have at least 2 SVG assets — if the manifest is empty, revisit the decomposition.

Use basic Manim shapes **only** for: array cells, flowchart boxes, graphs/axes, code blocks, containers, math expressions. **Everything else gets an SVG.**

Write `$WORK_DIR/story.json` with a top-level `asset_manifest` and per-scene `svg_assets` referencing manifest keys:

```json
{
  "title": "How Binary Search Works",
  "asset_manifest": {
    "magnifier_icon": {
      "description": "Magnifying glass with circular lens and angled handle",
      "viewbox": "0 0 64 64",
      "primary_color_token": "ACCENT",
      "used_in": [1]
    },
    "checkmark_icon": {
      "description": "Bold checkmark inside a rounded square",
      "viewbox": "0 0 64 64",
      "primary_color_token": "SUCCESS",
      "used_in": [3]
    }
  },
  "scenes": [
    {
      "id": 1,
      "title": "The Problem",
      "description": "Show a sorted array of numbers. Highlight that we need to find a target value.",
      "visual_elements": ["sorted array of boxes with numbers", "target value highlighted"],
      "animations": ["Create array", "Highlight target", "Write question text"],
      "svg_assets": ["magnifier_icon"],
      "scene_class": "TheProblem",
      "duration": 8,
      "template": "basic",
      "text_elements": ["title: 3 words", "description: 12 words"],
      "estimated_reading_pauses": 6.0,
      "continuity_in": null,
      "continuity_out": "Array remains visible, target highlighted"
    }
  ],
  "shared_style": {
    "NOTE": "LOCKED — copy these values verbatim into shared.py. Do NOT change any hex code.",
    "bg_color": "#2a2a3a",
    "surface_color": "#3a3a4a",
    "border_color": "#4a4a5a",
    "primary_color": "#ff3366",
    "accent_color": "#33ccff",
    "highlight_color": "#ffcc00",
    "success_color": "#66ff66",
    "negative_color": "#ff4444",
    "text_color": "#ffffff",
    "muted_color": "#8a8aaa",
    "font_heading": "Helvetica Neue",
    "font_body": "Helvetica Neue",
    "font_code": "Monaco",
    "font_size_title": 44,
    "font_size_body": 26
  },
  "latex_available": true
}
```

**`asset_manifest` schema**: Each key is an asset ID (snake_case). Fields:
- `description` — what the icon depicts, enough detail for accurate SVG generation
- `viewbox` — SVG viewBox (tall: `"0 0 80 100"`, square: `"0 0 64 64"`, wide: `"0 0 100 60"`)
- `primary_color_token` — which palette token to use as the main fill (`PRIMARY`, `ACCENT`, `HIGHLIGHT`, `SUCCESS`, `NEGATIVE`)
- `used_in` — list of scene IDs that use this asset

**Per-scene `svg_assets`** is a list of asset IDs from the manifest (not freeform hints). If a scene needs no SVG assets, use an empty list `[]`.

**Asset density target**: Aim for 1-2 SVG assets per scene, 3-6 per video. Scenes with SVG icons are dramatically more engaging than scenes with only basic shapes.

**If no scenes need SVG assets** (e.g., a pure math derivation), set `asset_manifest` to `{}` and all `svg_assets` to `[]`. Steps 6-7 will no-op.

**Continuity rules:**
- `continuity_out` of scene N must match `continuity_in` of scene N+1
- Shared visual elements should use identical styling constants
- Color palette must be consistent across all scenes (defined in `shared_style`)

**Pacing rules:**
- `text_elements` lists each text block with its approximate word count — used to calculate reading pauses
- `estimated_reading_pauses` is the total seconds of `self.wait()` needed for reading time (sum of `max(2, words / 3)` for each text block)
- `duration` must be >= animation time + `estimated_reading_pauses` — increase duration if needed to fit reading time
- Use the formula: **`self.wait(max(2, word_count / 3))`** after every text appearance

---

### Step 4: Outline Confirmation

Before generating any code, present the story outline to the user for review and approval.

**Build a readable summary from `$WORK_DIR/story.json`:**

```
Scene Outline for: "{title}"

  Scene 1: {scene_title}
    {description}
    Key visuals: {visual_elements joined as comma-separated list}
    Duration: {duration}s

  Scene 2: {scene_title}
    {description}
    Key visuals: {visual_elements joined as comma-separated list}
    Duration: {duration}s

  ...

SVG Assets to generate:
  - magnifier_icon
    Icon: Magnifying glass with circular lens and angled handle
    Color: ACCENT (#33ccff)
    Used in: Scene 1
  - checkmark_icon
    Icon: Bold checkmark inside a rounded square
    Color: SUCCESS (#66ff66)
    Used in: Scene 3

Total duration: {sum of all durations}s
Output format: MP4 (default). Would you like GIF, or both?
```

**Present this outline to the user and ask:**

```
Does this outline look good? You can:
  1. Approve and continue
  2. Request changes (add/remove/reorder scenes, adjust descriptions, change durations)
  3. Change output format (mp4 / gif / both)
```

**⛔ HARD STOP — Do NOT proceed past this point until the user explicitly approves.**

After presenting the outline, STOP. Do not generate any code, write any files, or start any subsequent steps. Wait for the user to respond. This is a mandatory approval gate.

**Revision loop:**

- If the user requests changes, update `$WORK_DIR/story.json` accordingly (add/remove scenes, edit descriptions, adjust durations, etc.) and re-present the outline.
- If the user changes the output format, update `$WORK_DIR/params.json` (`format` field) and `$WORK_DIR/manim.cfg` to match.
- Repeat until the user explicitly approves (e.g., "looks good", "approved", "go ahead", "yes").

Once — and ONLY once — the user explicitly approves, proceed to Step 5.

---

### Step 5: Shared Preamble Generation

Generate `$WORK_DIR/shared.py` — a single module containing palette constants, helpers, and asset loading that all scenes import. This eliminates ~50 lines of duplicated boilerplate from each scene file.

**Write `$WORK_DIR/shared.py`** by copying the code block below VERBATIM. Do NOT change ANY hex value — not even the background tones (BG, SURFACE, BORDER). The exact hex codes below are the Creative Chaos brand palette and must appear character-for-character in the generated file:

```python
from manim import *
import tempfile, os

# ── Creative Chaos Dark — LOCKED palette, do not modify ──
BG        = "#2a2a3a"
SURFACE   = "#3a3a4a"
BORDER    = "#4a4a5a"
PRIMARY   = "#ff3366"
ACCENT    = "#33ccff"
HIGHLIGHT = "#ffcc00"
SUCCESS   = "#66ff66"
NEGATIVE  = "#ff4444"
TEXT_CLR  = "#ffffff"
TEXT_DIM  = "#8a8aaa"

# ── Asset directory ──
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def svg_icon(svg_string, scale=1.0):
    """Write inline SVG to temp file and load as SVGMobject.
    Use for rare one-off SVGs (under 5 lines). Prefer load_asset() for validated assets."""
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "icon.svg")
    with open(path, "w") as f:
        f.write(svg_string)
    return SVGMobject(path).scale(scale)


def load_asset(asset_id, scale=1.0):
    """Load a validated SVG asset from the assets directory."""
    path = os.path.join(ASSET_DIR, f"{asset_id}.svg")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Asset not found: {path}")
    return SVGMobject(path).scale(scale)


def tw(text_str):
    """Calculate reading time wait duration: max(2, word_count / 3)."""
    return max(2, len(text_str.split()) / 3)


def dot_grid():
    """Create the signature Creative Chaos dot grid background."""
    return VGroup(*[
        Dot([x, y, 0], radius=0.02, fill_opacity=0.08, color=TEXT_CLR)
        for x in range(-7, 8) for y in range(-4, 5)
    ])


def setup_scene(scene):
    """Set background color and add dot grid. Call at the start of construct()."""
    scene.camera.background_color = BG
    scene.add(dot_grid())


def title_card(scene, text, wait=2.0):
    """Show title with signature underline, then move to corner.

    Args:
        scene: the Scene instance (pass `self` from construct)
        text: the title string
        wait: seconds to display before moving to corner (default 2.0)
    Returns:
        title Mobject (now in the UL corner at scale 0.55)
    """
    title = Text(text, font="Helvetica Neue", font_size=44, color=TEXT_CLR, weight=BOLD)
    underline = Line(
        title.get_left() + DOWN * 0.35,
        title.get_right() + DOWN * 0.35,
        color=PRIMARY, stroke_width=2.5,
    )
    scene.play(
        FadeIn(title, shift=UP * 0.4),
        GrowFromCenter(underline),
        run_time=0.7,
    )
    scene.wait(wait)
    scene.play(
        title.animate.scale(0.55).to_corner(UL, buff=0.5),
        FadeOut(underline, run_time=0.3),
        run_time=0.5,
    )
    return title


def make_node(label, color=None, w=2.5, h=0.8):
    """Create a labeled rounded rectangle node. Box auto-sizes to fit text."""
    if color is None:
        color = PRIMARY
    text = Text(label, font="Helvetica Neue", font_size=22, color=TEXT_CLR)
    box_w = max(w, text.width + 0.6)
    box_h = max(h, text.height + 0.4)
    box = RoundedRectangle(
        corner_radius=0.15, width=box_w, height=box_h,
        fill_color=SURFACE, fill_opacity=1,
        stroke_color=color, stroke_width=1.5,
    )
    text.move_to(box)
    return VGroup(box, text)


def progress_bar(width=8, height=0.4, fill_color=None):
    """Create a progress bar. Returns VGroup(track, fill) with fill at 0%.
    Animate with: self.play(set_progress(bar, 0.75), run_time=1.0)"""
    if fill_color is None:
        fill_color = PRIMARY
    pad = height * 0.12
    track = RoundedRectangle(
        corner_radius=height / 2, width=width, height=height,
        fill_color=SURFACE, fill_opacity=1,
        stroke_color=BORDER, stroke_width=1.5,
    )
    fill = RoundedRectangle(
        corner_radius=max(0.05, (height - 2 * pad) / 2),
        width=pad, height=height - 2 * pad,
        fill_color=fill_color, fill_opacity=1, stroke_width=0,
    )
    fill.align_to(track, LEFT).shift(RIGHT * pad)
    return VGroup(track, fill)


def set_progress(bar, pct):
    """Return animation for bar fill to reach pct (0.0-1.0).
    Rebuilds the fill shape each frame to avoid .animate vertex interpolation artifacts."""
    track, fill = bar[0], bar[1]
    pad = track.height * 0.12
    start_w = fill.width
    target_w = max(pad, (track.width - 2 * pad) * max(0.0, min(1.0, pct)))
    cr = max(0.05, (track.height - 2 * pad) / 2)
    fc = fill.get_fill_color()

    def _update(mob, alpha):
        w = interpolate(start_w, target_w, alpha)
        mob.become(RoundedRectangle(
            corner_radius=cr, width=w, height=track.height - 2 * pad,
            fill_color=fc, fill_opacity=1, stroke_width=0,
        ))
        mob.move_to([track.get_left()[0] + pad + w / 2, track.get_center()[1], 0])

    return UpdateFromAlphaFunc(fill, _update)


def make_cell(value, color=None, w=0.7, h=0.7):
    """Create a data cell — sharp-cornered square with a number inside.
    Use for array elements, grid data, table cells."""
    if color is None:
        color = PRIMARY
    box = Square(
        side_length=max(w, h),
        fill_color=SURFACE, fill_opacity=0.6,
        stroke_color=color, stroke_width=1.5,
    )
    text = Text(str(value), font="Monaco", font_size=22, color=TEXT_CLR)
    text.move_to(box)
    return VGroup(box, text)


def make_array(values, color=None, cell_w=0.7, cell_h=0.7, buff=0.05):
    """Create a horizontal array of data cells."""
    if color is None:
        color = PRIMARY
    cells = VGroup(*[make_cell(v, color, cell_w, cell_h) for v in values])
    cells.arrange(RIGHT, buff=buff)
    return cells
```

**IMPORTANT — PALETTE IS LOCKED**: Every hex value above is final. BG must be `#2a2a3a`, SURFACE must be `#3a3a4a`, BORDER must be `#4a4a5a`. Do NOT substitute theme-specific or topic-specific colors. The only exception is the light theme palette from the style guide. If the generated shared.py contains any hex value not listed above, it is wrong — fix it before proceeding.

**Semantic aliases are allowed**: After the palette block, you may add project-specific aliases that map to palette tokens (e.g., `US_COLOR = ACCENT`, `SENDER_COLOR = PRIMARY`). These improve scene code readability without introducing custom hex values. Never assign a raw hex code to an alias.

**Scene files import via:**

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *
```

This works because render runs from `$WORK_DIR` as CWD (`cd "$WORK_DIR" && manim render scenes/scene_NN.py`).

---

### Step 6: Asset Generation

For each entry in `asset_manifest` from story.json, generate a validated SVG file.

**If `asset_manifest` is empty `{}`**, pause — are there real-world concepts that could use icons? Only skip for purely mathematical/abstract videos. Otherwise revisit Step 3.

**For each asset in the manifest:**

1. Read the `description`, `viewbox`, and `primary_color_token` from the manifest entry
2. Read the SVG Icon Style Rules from `library/style-guide.md`
3. Generate the SVG file following these constraints:
   - Flat fills only — NO gradients, NO filters, NO `<text>` elements, NO `stroke-dasharray`
   - Use palette hex colors from `shared_style` (e.g., `#ff3366` for PRIMARY, not Manim color names)
   - Outer strokes: `stroke="#ffffff" stroke-width="2"`
   - Detail strokes: `stroke-width="1.5"`
   - Line endings: `stroke-linecap="round" stroke-linejoin="round"`
   - Center content within the viewBox
   - Keep simple — Manim's SVG parser handles basic shapes well but struggles with complex paths
4. Write the SVG file to `$WORK_DIR/assets/{asset_id}.svg`

```bash
# Verify each asset file was written
for ASSET_ID in $(python3 -c "
import json
m = json.load(open('$WORK_DIR/story.json'))['asset_manifest']
print(' '.join(m.keys()))
"); do
  [ -f "$WORK_DIR/assets/${ASSET_ID}.svg" ] || echo "Missing asset: ${ASSET_ID}"
done
```

---

### Step 7: Asset Validation Gate

Verify all generated SVG assets render correctly in Manim before using them in scenes.

**If `asset_manifest` is empty**, skip this step.

**Procedure:**

1. Write a temporary validation scene `$WORK_DIR/scenes/_asset_validation.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shared import *

class AssetValidation(Scene):
    def construct(self):
        setup_scene(self)
        title = Text("Asset Validation", font="Helvetica Neue", font_size=32,
                      color=TEXT_CLR, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        assets = []
        # One VGroup(icon, label) per asset — filled dynamically
        # ASSET_ENTRIES_PLACEHOLDER

        if assets:
            grid = VGroup(*assets).arrange_in_grid(
                rows=max(1, (len(assets) + 2) // 3),
                cols=min(3, len(assets)),
                buff=1.0,
            )
            grid.move_to(DOWN * 0.3)
            self.add(grid)
        self.wait(1)
```

2. Fill in the asset loading code for each manifest entry (load via `load_asset()`, add a label below each icon)

3. Render the validation scene as a still frame:

```bash
cd "$WORK_DIR" && manim render -ql -s --renderer=cairo --disable_caching \
  scenes/_asset_validation.py AssetValidation 2>/dev/null
```

4. Find and read the output PNG:

```bash
VALIDATION_PNG=$(find "$WORK_DIR"/media/images -name "AssetValidation*.png" 2>/dev/null | head -1)
```

5. Inspect the grid image. For each asset, verify:
   - The icon is **recognizable** (matches the description)
   - Colors are **correct** (matches the `primary_color_token`)
   - Rendering is **clean** (no artifacts, broken paths, or missing elements)

6. If any asset fails: regenerate its SVG file, re-render the grid (max 2 retries per asset)

7. Clean up: `rm "$WORK_DIR/scenes/_asset_validation.py"`

---

### Step 8: Scene Generation

Generate each scene file. Scenes import from `shared.py` and load assets via `load_asset()` — no inlined palette constants or helper functions.

**For each scene N (sequentially):**

1. **Read the scene spec** from `$WORK_DIR/story.json` — extract the scene entry, `shared_style`, and `latex_available` flag.

2. **Read the relevant library files** based on scene template type:

| Scene template | Always read | Conditionally read |
|---------------|------------|-------------------|
| All types | `library/cheatsheet.md`, `library/style-guide.md`, `library/common-errors.md` | — |
| `basic` | — | `library/animations.md` |
| `math` | — | `library/animations.md`, `library/text-and-math.md` |
| `graph` | — | `library/animations.md` |
| `code` | — | `library/text-and-math.md` |

3. **Read the template** from `templates/{template}.py` (e.g., `templates/basic.py`).

4. **Write the scene file** to `$WORK_DIR/scenes/scene_NN.py` following these rules:

   1. Start with the shared import: `import sys, os` / `sys.path.insert(...)` / `from shared import *`
   2. Define exactly ONE Scene subclass named `{scene_class}` (from story.json)
   3. All animation logic goes in the `construct(self)` method
   4. Call `setup_scene(self)` at the start of `construct()` (sets BG + dot grid)
   5. Use `title_card(self, "...")` for the title entrance
   6. Use `load_asset(asset_id, scale)` for SVG icons from the manifest
   7. Use `svg_icon()` only for rare one-off inline SVGs (under 5 SVG lines)
   8. Use `tw(text_string)` for reading time: `self.wait(tw("your text here"))`
   9. Use `make_node(label, color)` for diagram nodes
   10. Keep the scene self-contained (no file I/O beyond asset loading, no network)
   11. Target duration: ~{duration}s (use self.wait() to pad if needed)
   12. Use .animate syntax for simple property changes
   13. Use Transform/ReplacementTransform for morphing between objects
   14. If `latex_available` is false: do NOT use MathTex or Tex — use Text() for all text including math. Render equations as Unicode. If true: use MathTex (not Tex) for math expressions.

   **Layout Rules (CRITICAL — prevents overlapping elements):**

   15. Use `next_to()`, `arrange()`, `arrange_in_grid()` for spatially-related elements — NOT absolute coordinates
   16. Group with `VGroup()` before positioning — position the group, not individual items
   17. Absolute coords only for placing independent groups at anchor positions (e.g., `left_panel.move_to(LEFT * 3)`)
   18. Never place content within 0.8 units of the frame edge

   **Text Pacing Rules (CRITICAL — text must be readable):**

   19. After EVERY Write(text) or FadeIn(text), add a reading pause: `self.wait(tw("your text content"))` — this gives ~180 WPM reading speed with a 2-second minimum.
   20. Title cards: display for at least 2 seconds before animating to corner/top
   21. Key insight or annotation text: minimum 3 seconds on screen
   22. NEVER use bare `self.wait()` after text — always calculate from word count
   23. NEVER use `self.wait(0.5)` or `self.wait(1)` after text that has more than 3 words
   24. Between conceptual sections, use `self.wait(1.5)` as a transition pause

   **Visual Polish Rules (CRITICAL — prevents rendering issues):**

   25. **Text color**: body text (font_size >= 20) always uses `TEXT_CLR`. Use `TEXT_DIM` ONLY for captions (font_size 16) and axis labels.
   26. **Contained text**: when placing text inside a container, ALWAYS measure text width first and size the container to fit: `max(desired_w, text.width + 0.6)`. Or use `make_node()` which auto-sizes. NEVER hard-code a container width without checking the text.
   27. **Progress bars**: use `progress_bar()` and `set_progress()` from shared.py. NEVER animate a raw Rectangle's width for progress — it will overflow the track.

**Expected scene size**: 80-130 lines (vs 180-230 with inlined constants).

5. **Validate the generated file:**

```bash
FILE="$WORK_DIR/scenes/scene_$(printf "%02d" $N).py"
SCENE_CLASS="<scene_class from story.json>"

python3 -c "compile(open('$FILE').read(), '$FILE', 'exec')" 2>/dev/null || {
  echo "Syntax error in $FILE — fix before rendering"
}

python3 -c "
import ast, sys
tree = ast.parse(open('$FILE').read())
classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
if '$SCENE_CLASS' not in classes:
    print(f'$FILE does not define class $SCENE_CLASS (found: {classes})')
    sys.exit(1)
print('$FILE defines $SCENE_CLASS')
"
```

If validation fails (syntax error or wrong class name), fix the file immediately and re-validate before moving on.

---

### Step 9: Layout Validation Gate

After writing each scene, validate the layout visually. Scenes end with `FadeOut(*self.mobjects)` which makes the last frame blank — so we extract a mid-animation frame instead.

**For each scene N:**

1. **Render a low-quality video** (fast: ~5-10s at 480p 15fps):

```bash
cd "$WORK_DIR" && manim render -ql --renderer=cairo --disable_caching \
  scenes/scene_$(printf "%02d" $N).py $SCENE_CLASS 2>/dev/null
```

2. **Extract a frame at ~2 seconds** (frame 30 at 15fps) — content should be visible before exit animations:

```bash
SCENE_FILE="scene_$(printf "%02d" $N)"
VIDEO_PATH=$(find "$WORK_DIR"/media/videos/${SCENE_FILE} -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
ffmpeg -i "$VIDEO_PATH" \
  -vf "select=eq(n\,30)" -vframes 1 -y \
  "$WORK_DIR"/lastframes/${SCENE_FILE}_layout.png 2>/dev/null
```

3. **Read the extracted PNG** and evaluate against this rubric:

| Check | Pass condition |
|-------|---------------|
| Text readability | No text cut off or extending beyond frame |
| No overlaps | All elements visible, no unintended overlap |
| Asset rendering | SVG icons recognizable and properly colored |
| Safe margins | Nothing within 0.8 units of frame edge |

4. **If any check fails**: fix the scene positioning code, re-render at `-ql`, re-inspect (max 2 retries per scene)

> **Cost**: ~5-10s per scene for a `-ql` render vs 60-180s for a wasted full render. This catches layout issues early.

---

### Step 10: Full Render & Recovery

For each scene, render at the target quality. If rendering fails, read the error output, fix the scene file directly, and retry. Max 3 attempts per scene.

**Output path resolution**: Manim writes to structured subdirs. After each render, resolve the actual output path.

**For each scene N**, run the render command:

```bash
SCENE_FILE="scene_$(printf "%02d" $N)"
SCENE_CLASS="<scene_class from story.json>"

RENDER_LOG=$(mktemp)
RENDER_CMD="manim render scenes/${SCENE_FILE}.py $SCENE_CLASS \
    --renderer=cairo -qh --format=mp4 --disable_caching"

if [ -n "$TIMEOUT_CMD" ]; then
  RENDER_CMD="$TIMEOUT_CMD 180 $RENDER_CMD"
fi

cd "$WORK_DIR" && eval $RENDER_CMD 2>"$RENDER_LOG"
RENDER_EXIT=$?
cd ..
```

**On success**: locate the output MP4:

```bash
QUALITY_SUBDIR="1080p60"  # matches -qh
EXPECTED_PATH="$WORK_DIR/media/videos/${SCENE_FILE}/${QUALITY_SUBDIR}/${SCENE_CLASS}.mp4"
if [ ! -f "$EXPECTED_PATH" ]; then
  FOUND_PATH=$(find "$WORK_DIR"/media/videos -name "${SCENE_CLASS}.mp4" 2>/dev/null | head -1)
fi
```

**On failure (up to 3 retries):**

1. Read the render error output from the log file
2. Read the current scene file and `library/common-errors.md`
3. Fix the scene file directly — preserve the animation intent, fix the error, ensure the Scene class name stays `{scene_class}`
4. If LaTeX is failing, switch to Text() as fallback
5. Re-run the render command

---

### Step 11: Stitch & Convert

Run the render script to concatenate scene videos and convert to GIF:

```bash
bash "scripts/render.sh" \
  --scenes-dir "$WORK_DIR"/scenes \
  --media-dir "$WORK_DIR"/media \
  --output-dir "$WORK_DIR"/output \
  --format "$FORMAT" \
  --story-file "$WORK_DIR"/story.json
```

> `scripts/render.sh` is relative to the skill directory. `$FORMAT` comes from `$WORK_DIR/params.json`.

---

### Step 12: Report

```
Animation complete!

Prompt: "explain how binary search works"
Scenes: 3 (all rendered successfully)
Duration: 28s (8s + 12s + 8s)
Quality: 1080p @ 60fps
Renderer: cairo

Assets: 2 SVGs generated and validated (magnifier_icon, checkmark_icon)
Layout validation: 3/3 scenes passed

Output:
  MP4: $WORK_DIR/output/animation.mp4 (1.2MB)
  GIF: $WORK_DIR/output/animation.gif (3.4MB)
  Layout previews: $WORK_DIR/lastframes/
```

---

## Component Library Reference

Read these library files before writing each scene (see Step 8 for which files apply per scene type):

| File | Purpose | Used by |
|------|---------|---------|
| `library/cheatsheet.md` | Manim API quick reference | All scene types |
| `library/style-guide.md` | Color palette, font sizes, timing, SVG style rules, layout best practices | All scene types |
| `library/animations.md` | Animation patterns with code | basic, math, graph |
| `library/text-and-math.md` | Text, MathTex, Code patterns | math, code |
| `library/common-errors.md` | Known pitfalls and fixes | All scene types |

## Key Conventions

1. **ManimCE only** — `from manim import *` (never `manimlib`). Cairo renderer for headless safety.
2. **One Scene class per file** — each scene is a separate `.py` file for isolated error recovery.
3. **Inline generation** — the orchestrating agent writes scene files directly (no sub-processes), ensuring the user's chosen model is used throughout.
4. **Shared preamble** — `shared.py` contains palette constants, helpers (`setup_scene`, `title_card`, `dot_grid`, `tw`, `make_node`, `progress_bar`, `set_progress`), and asset loading (`load_asset`). Scenes import, not copy.
5. **Asset-first** — SVG icons are generated and validated in Steps 6-7 before scene code is written. Scenes load validated assets via `load_asset()`, not inline SVG strings.
6. **Two validation gates** — asset grid (Step 7) and layout frame (Step 9) catch visual issues before the expensive full render in Step 10.
7. **Import from shared.py** — scenes use `from shared import *` for palette, helpers, and asset loading. No inlined constants.
8. **LaTeX fallback** — if LaTeX is unavailable, use `Text()` instead of `MathTex()`.
9. **Render timeout** — 180s timeout on render commands to catch hangs.
10. **Error recovery** — on render failure, read the error, fix the scene file, and retry. Max 3 attempts per scene.
11. **Selective library reads** — only read library docs relevant to the scene type to stay focused.
12. **SVG-first visuals** — every video defaults to custom SVG icons for real-world concepts. Aim for 3-6 assets per video. A video with zero SVG assets should be the exception (pure math only), not the norm.
