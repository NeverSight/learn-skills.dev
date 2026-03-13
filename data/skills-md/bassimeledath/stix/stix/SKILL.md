---
name: stix
description: Generate stick figure animations from natural language descriptions. Outputs GIF and MP4.
---

# /stix — Stick Figure Animation

Generate stick figure animations from natural language descriptions. Outputs GIF and MP4 files.

## Usage

```
/stix "a cat chasing a mouse across a park"
```

## Pipeline

When the user invokes `/stix`, execute these steps in order:

---

### Step 1: Parameter Inference

Parse the user's prompt and infer these parameters. The user never sees or sets these directly — infer them from the natural language description:

| Parameter | Range | Default | How to infer |
|-----------|-------|---------|--------------|
| `scenes` | 1–6 | 2 | Count distinct moments/locations/emotional beats in the prompt |
| `fps` | 8–24 | 8 | Default for most; use 12 for fast action |
| `format` | gif/mp4/both | both | Default both unless user specifies |
| `mood` | playful/melancholy/energetic/calm | playful | Infer from the emotion in the prompt |

Each scene is always **8 seconds** (the animation system is built around this fixed duration).

Write these to `.stix/params.json`:

```json
{
  "prompt": "a cat chasing a mouse across a park",
  "scenes": 3,
  "fps": 8,
  "format": "both",
  "mood": "playful"
}
```

---

### Step 2: Preflight Checks

Verify dependencies are installed:

```bash
command -v agent-browser >/dev/null 2>&1 || { echo "agent-browser not found"; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found"; exit 1; }

# Detect agent CLI (configurable via STIX_AGENT_CLI env var)
STIX_AGENT_CLI="${STIX_AGENT_CLI:-}"
if [ -z "$STIX_AGENT_CLI" ]; then
  if command -v claude >/dev/null 2>&1; then
    STIX_AGENT_CLI="claude -p --dangerously-skip-permissions"
    STIX_AGENT_ENV_UNSET="CLAUDE_CODE_ENTRYPOINT,CLAUDECODE"
  elif command -v codex >/dev/null 2>&1; then
    STIX_AGENT_CLI="codex --quiet --full-auto"
    STIX_AGENT_ENV_UNSET=""
  else
    echo "No supported agent CLI found. Set STIX_AGENT_CLI env var."
    echo "   Supported: claude, codex. Or set STIX_AGENT_CLI to your agent's pipe command."
    exit 1
  fi
fi
AGENT_BIN=$(echo "$STIX_AGENT_CLI" | awk '{print $1}')
command -v "$AGENT_BIN" >/dev/null 2>&1 || { echo "Agent CLI '$AGENT_BIN' not found"; exit 1; }
```

Create the working directory:

```bash
rm -rf .stix
mkdir -p .stix/scenes .stix/assets/characters .stix/assets/props .stix/qc .stix/frames .stix/output
```

---

### Step 3: Story Decomposition

Break the prompt into scenes. The story includes an **asset manifest** that lists every character, background element, and prop needed across all scenes, plus per-scene **position contracts** with exact coordinates.

Write `.stix/story.json`:

```json
{
  "title": "Cat Chases Mouse",
  "assets": {
    "characters": [
      { "id": "cat", "description": "Orange tabby cat (#e8a040), pointy ears, whiskers, curved tail", "expressions_needed": ["determined", "happy"] },
      { "id": "mouse", "description": "Small grey mouse (#999), round ears, thin tail", "expressions_needed": ["neutral", "surprised"] }
    ],
    "background": {
      "description": "Park setting: green grass, 2 trees, bench on the right, blue sky gradient, sun"
    },
    "props": ["tree", "bench"]
  },
  "scenes": [
    {
      "id": 1,
      "description": "A mouse scurries across a park path, unaware.",
      "characters": {
        "mouse": { "start": [50, 330], "end": [500, 330], "start_expr": "neutral", "end_expr": "neutral" }
      },
      "animation_notes": "Mouse runs left to center, scurry animation cycle",
      "props_used": ["tree", "bench"],
      "timing": { "run": "0-100%" },
      "mood": "playful"
    },
    {
      "id": 2,
      "description": "A cat spots the mouse and launches into a chase.",
      "characters": {
        "cat": { "start": [30, 310], "end": [600, 310], "start_expr": "determined", "end_expr": "determined" },
        "mouse": { "start": [500, 330], "end": [850, 330], "start_expr": "neutral", "end_expr": "surprised" }
      },
      "animation_notes": "Cat enters from left chasing mouse, both running right. Cat gains on mouse.",
      "props_used": ["tree"],
      "timing": { "chase": "0-100%" },
      "mood": "energetic",
      "continuity": "Mouse position matches end of scene 1"
    }
  ]
}
```

**Asset manifest rules:**
- Every character that appears in ANY scene must be listed in `assets.characters`
- One shared background for ALL scenes
- All unique props listed in `assets.props`
- Character descriptions include specific colors for consistency

**Per-scene position contracts:**
- `start` / `end` are `[x, y]` pixel coordinates within the 900x400 viewBox
- `start_expr` / `end_expr` specify which expression variant to show
- `timing` maps animation phases to percentages of the 8s duration
- `continuity` notes link scenes together

---

### Step 4: Asset Generation (Parallel Workers)

Generate reusable SVG assets that will be shared across all scenes. Each asset is a self-contained SVG file.

**Output structure:**
```
.stix/assets/
├── characters/
│   ├── cat.svg
│   └── mouse.svg
├── background.svg
└── props/
    ├── tree.svg
    └── bench.svg
```

**The dispatcher must read and inject library file contents into each worker prompt.** Workers run as independent agent subprocesses and cannot access the skill directory.

```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")" 2>/dev/null || cd "$(dirname "$0")" && pwd)"
# If SKILL_DIR detection fails, try common install locations:
# ~/.claude/skills/stix, ~/.codex/skills/stix, or ~/.agents/skills/stix

# Read library files
STYLE_GUIDE="$(cat "$SKILL_DIR/library/style-guide.md")"
POSES="$(cat "$SKILL_DIR/library/poses.md")"
EXPRESSIONS="$(cat "$SKILL_DIR/library/expressions.md")"
PROPS_LIB="$(cat "$SKILL_DIR/library/props.md")"
ANIMALS="$(cat "$SKILL_DIR/library/animals.md")"

# Read reference templates
CHAR_REF="$(cat "$SKILL_DIR/references/asset-character.md")"
BG_REF="$(cat "$SKILL_DIR/references/asset-background.md")"
PROPS_REF="$(cat "$SKILL_DIR/references/asset-props.md")"

# Read asset manifest from story.json
ASSET_MANIFEST=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
print(json.dumps(story['assets'], indent=2))
")
```

**Spawn parallel workers:**

#### 4a. Character workers (1 per character)

For each character in the asset manifest:

```bash
CHARACTER_DESC=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
chars = story['assets']['characters']
char = [c for c in chars if c['id'] == '$CHAR_ID'][0]
print(json.dumps(char, indent=2))
")

cat > /tmp/stix-asset-char-${CHAR_ID}-prompt.txt << PROMPT_EOF
You are generating a reusable SVG character asset for a stick figure animation system.

## Character Specification
$CHARACTER_DESC

## Asset Template & Instructions
$CHAR_REF

## Component Library

### Style Guide
$STYLE_GUIDE

### Poses
$POSES

### Expressions
$EXPRESSIONS

### Animals (if this is an animal character)
$ANIMALS

## Output
Write ONLY the SVG content to: .stix/assets/characters/${CHAR_ID}.svg
No explanation, no markdown — just the SVG file.
PROMPT_EOF

# Build env unset command
ENV_CMD="env"
if [ -n "$STIX_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$STIX_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-asset-char-${CHAR_ID}-prompt.txt)" &
```

#### 4b. Background worker (1 total)

```bash
BG_DESC=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
print(json.dumps(story['assets']['background'], indent=2))
")

cat > /tmp/stix-asset-bg-prompt.txt << PROMPT_EOF
You are generating a reusable SVG background for a stick figure animation system.

## Background Specification
$BG_DESC

## Asset Template & Instructions
$BG_REF

## Component Library

### Style Guide
$STYLE_GUIDE

### Props (for background elements like trees, benches)
$PROPS_LIB

## Output
Write ONLY the SVG content to: .stix/assets/background.svg
No explanation, no markdown — just the SVG file.
PROMPT_EOF

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-asset-bg-prompt.txt)" &
```

#### 4c. Props worker (1 total for all props)

```bash
PROPS_LIST=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
print(json.dumps(story['assets']['props'], indent=2))
")

cat > /tmp/stix-asset-props-prompt.txt << PROMPT_EOF
You are generating reusable SVG props for a stick figure animation system.

## Props Needed
$PROPS_LIST

## Asset Template & Instructions
$PROPS_REF

## Component Library

### Style Guide
$STYLE_GUIDE

### Props Reference
$PROPS_LIB

## Output
Write each prop as a separate SVG file to: .stix/assets/props/<prop_id>.svg
No explanation, no markdown — just the SVG files.
PROMPT_EOF

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-asset-props-prompt.txt)" &
```

Wait for all asset workers:

```bash
wait
```

Verify all assets exist:

```bash
# Check characters
for CHAR_ID in $(python3 -c "
import json
story = json.load(open('.stix/story.json'))
for c in story['assets']['characters']:
    print(c['id'])
"); do
  FILE=".stix/assets/characters/${CHAR_ID}.svg"
  if [ ! -f "$FILE" ]; then
    echo "Missing character asset: $FILE"
    exit 1
  fi
  echo "character: $FILE"
done

# Check background
if [ ! -f ".stix/assets/background.svg" ]; then
  echo "Missing background asset"
  exit 1
fi
echo "background: .stix/assets/background.svg"

# Check props
for PROP_ID in $(python3 -c "
import json
story = json.load(open('.stix/story.json'))
for p in story['assets']['props']:
    print(p)
"); do
  FILE=".stix/assets/props/${PROP_ID}.svg"
  if [ ! -f "$FILE" ]; then
    echo "Missing prop asset: $FILE"
    exit 1
  fi
  echo "prop: $FILE"
done
```

---

### Step 5: Asset Validation

Render each asset in a minimal HTML wrapper and screenshot it. The orchestrating agent visually inspects the screenshots and regenerates bad assets (max 2 retries).

```bash
# For each asset file, create a wrapper HTML
for ASSET in .stix/assets/characters/*.svg .stix/assets/props/*.svg .stix/assets/background.svg; do
  [ -e "$ASSET" ] || continue
  ASSET_NAME=$(basename "$ASSET" .svg)
  ASSET_CONTENT=$(cat "$ASSET")

  cat > "/tmp/stix-validate-${ASSET_NAME}.html" << WRAP_EOF
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
  body { background: #faf9f6; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
  svg { width: 400px; height: 400px; border: 1px solid #eee; }
</style>
</head><body>
<svg viewBox="-100 -100 300 300" xmlns="http://www.w3.org/2000/svg">
$ASSET_CONTENT
</svg>
</body></html>
WRAP_EOF

  ABS_WRAPPER="$(realpath /tmp/stix-validate-${ASSET_NAME}.html)"
  agent-browser open "file://$ABS_WRAPPER"
  sleep 0.5
  agent-browser screenshot "$(realpath .stix/qc)/asset-${ASSET_NAME}.png"
  agent-browser close
done
```

Visually inspect each screenshot. If an asset is malformed (missing body parts, wrong proportions, empty SVG), regenerate it by re-running the relevant worker from Step 4 with additional fix instructions. Max 2 retries per asset.

---

### Step 6: Scene Composition (Parallel Workers)

Scene composers read the pre-built assets and compose them into animated HTML scenes. Their job is ONLY positioning + keyframes + timing — not character/prop design.

**Read the scene count:**

```bash
TOTAL_SCENES=$(python3 -c "import json; print(len(json.load(open('.stix/story.json'))['scenes']))")
```

**Read reference template:**

```bash
COMPOSE_REF="$(cat "$SKILL_DIR/references/scene-compose.md")"
BASE_TEMPLATE="$(cat "$SKILL_DIR/references/scene-base.html")"
TRANSITIONS="$(cat "$SKILL_DIR/library/transitions.md")"
```

**For each scene N, build the composer prompt:**

```bash
SCENE_DESC=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
scene = story['scenes'][$((N-1))]
print(json.dumps(scene, indent=2))
")

# List asset files this scene needs
ASSET_FILES=""
for CHAR_ID in $(python3 -c "
import json
story = json.load(open('.stix/story.json'))
scene = story['scenes'][$((N-1))]
for cid in scene['characters']:
    print(cid)
"); do
  ASSET_FILES="$ASSET_FILES
- .stix/assets/characters/${CHAR_ID}.svg"
done

ASSET_FILES="$ASSET_FILES
- .stix/assets/background.svg"

for PROP_ID in $(python3 -c "
import json
story = json.load(open('.stix/story.json'))
scene = story['scenes'][$((N-1))]
for p in scene.get('props_used', []):
    print(p)
"); do
  ASSET_FILES="$ASSET_FILES
- .stix/assets/props/${PROP_ID}.svg"
done

cat > /tmp/stix-compose-$(printf "%02d" $N)-prompt.txt << PROMPT_EOF
You are composing an animation scene by positioning pre-built SVG assets and adding CSS keyframes.

## Scene Specification
$SCENE_DESC

## Composition Instructions
$COMPOSE_REF

## Base HTML Template
$BASE_TEMPLATE

## Transition Library
$TRANSITIONS

## Asset Files to Read
Read these SVG files and embed them in the scene:
$ASSET_FILES

## Rules
1. COPY asset SVG groups exactly as-is — do NOT modify SVG paths or shapes
2. Position each asset via \`<g transform="translate(x, y)">\` wrappers
3. Add CSS @keyframes for movement, limb animation, expression toggling
4. All scene animations: 8s duration, CSS-only, infinite loop
5. Sub-loops (walk cycle 0.5s, run cycle 0.4s) nest inside the 8s scene loop
6. Background is placed once, identical across scenes
7. Use start/end coordinates from the scene spec for translate animations
8. Toggle expressions via display:none/block at keyframe percentages

## Output
Write ONLY the complete HTML file to: .stix/scenes/scene-$(printf "%02d" $N).html
No explanation, no markdown — just the HTML file.
PROMPT_EOF

# Build env unset command
ENV_CMD="env"
if [ -n "$STIX_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$STIX_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-compose-$(printf "%02d" $N)-prompt.txt)" &
```

After spawning all workers, wait for completion:

```bash
wait
```

Verify all scene files exist:

```bash
for N in $(seq 1 $TOTAL_SCENES); do
  FILE=".stix/scenes/scene-$(printf "%02d" $N).html"
  if [ ! -f "$FILE" ]; then
    echo "Missing: $FILE"
    exit 1
  fi
  echo "scene: $FILE"
done
```

---

### Step 7: Visual QC

For each scene, capture keyframes using `agent-browser eval` for frame-accurate positioning and run a review worker.

**Per scene:**

1. **Capture 4 keyframes using eval-based seeking:**

```bash
SCENE_FILE=".stix/scenes/scene-$(printf "%02d" $N).html"
ABS_PATH="$(realpath "$SCENE_FILE")"

agent-browser open "file://$ABS_PATH"
sleep 0.5

# Pause all CSS animations
agent-browser eval "document.getAnimations().forEach(a => a.pause())"

# Seek to 0%
agent-browser eval "document.getAnimations().forEach(a => { a.currentTime = 0 })"
agent-browser screenshot "$(realpath .stix/qc)/scene-${N}-kf0.png"

# Seek to 33% (2640ms of 8000ms)
agent-browser eval "document.getAnimations().forEach(a => { a.currentTime = 2640 })"
agent-browser screenshot "$(realpath .stix/qc)/scene-${N}-kf33.png"

# Seek to 66% (5280ms)
agent-browser eval "document.getAnimations().forEach(a => { a.currentTime = 5280 })"
agent-browser screenshot "$(realpath .stix/qc)/scene-${N}-kf66.png"

# Seek to 100% (8000ms)
agent-browser eval "document.getAnimations().forEach(a => { a.currentTime = 8000 })"
agent-browser screenshot "$(realpath .stix/qc)/scene-${N}-kf100.png"

agent-browser close
```

2. **Spawn a QC reviewer** (use a fast model — review-tier is sufficient):

```bash
QC_RUBRIC="$(cat "$SKILL_DIR/references/qc-rubric.md")"

SCENE_DESC=$(python3 -c "
import json
story = json.load(open('.stix/story.json'))
scene = story['scenes'][$((N-1))]
print(json.dumps(scene, indent=2))
")

cat > /tmp/stix-qc-$(printf "%02d" $N)-prompt.txt << QC_EOF
Review these 4 keyframe screenshots of a stick figure animation scene against the QC rubric.

Screenshots:
- .stix/qc/scene-${N}-kf0.png (0% - start)
- .stix/qc/scene-${N}-kf33.png (33%)
- .stix/qc/scene-${N}-kf66.png (66%)
- .stix/qc/scene-${N}-kf100.png (100% - end)

QC Rubric:
$QC_RUBRIC

Scene description:
$SCENE_DESC

Evaluate each category: Animation Correctness, Scene Composition, Visual Quality.

Note: Character and prop integrity was already validated at the asset step. Focus on
whether the COMPOSITION and ANIMATION are correct — positioning, movement, timing,
expression changes, and visual quality.

Output a JSON object:
{
  "scene": $N,
  "overall": "PASS" or "FAIL",
  "categories": {
    "animation_correctness": { "result": "PASS/FAIL", "notes": "..." },
    "scene_composition": { "result": "PASS/FAIL", "notes": "..." },
    "visual_quality": { "result": "PASS/FAIL", "notes": "..." }
  },
  "fix_instructions": ["list of specific fixes needed"]
}

Write the result to: .stix/qc/scene-${N}-result.json
QC_EOF

ENV_CMD="env"
if [ -n "$STIX_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$STIX_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-qc-$(printf "%02d" $N)-prompt.txt)"
```

3. **If FAIL, fix and re-review (max 3 iterations):**

```bash
ITERATION=0
MAX_ITERATIONS=3

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
  QC_RESULT=$(cat ".stix/qc/scene-${N}-result.json" 2>/dev/null)

  if echo "$QC_RESULT" | grep -q '"overall": "PASS"'; then
    echo "Scene $N passed QC"
    break
  fi

  ITERATION=$((ITERATION + 1))
  echo "Scene $N failed QC (attempt $ITERATION/$MAX_ITERATIONS). Fixing..."

  CURRENT_HTML="$(cat ".stix/scenes/scene-$(printf "%02d" $N).html")"

  cat > /tmp/stix-fix-$(printf "%02d" $N)-prompt.txt << FIX_EOF
Fix this stick figure animation scene based on QC feedback.

IMPORTANT: Do NOT modify the SVG asset shapes — only fix positioning, keyframes, and timing.

Current HTML:
$CURRENT_HTML

QC Result:
$QC_RESULT

## Transition Library
$TRANSITIONS

Fix the issues listed in fix_instructions. Write the corrected HTML to:
.stix/scenes/scene-$(printf "%02d" $N).html
FIX_EOF

  ENV_CMD="env"
  if [ -n "$STIX_AGENT_ENV_UNSET" ]; then
    IFS=',' read -ra UNSET_VARS <<< "$STIX_AGENT_ENV_UNSET"
    for var in "${UNSET_VARS[@]}"; do
      [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
    done
  fi

  $ENV_CMD $STIX_AGENT_CLI \
    "$(cat /tmp/stix-fix-$(printf "%02d" $N)-prompt.txt)"

  # Re-capture keyframes and re-review (repeat eval-based capture + QC from above)
done
```

4. **Continuity check (multi-scene only):**

For scenes 2+, compare the last frame of the previous scene with the first frame of the current scene:

```bash
PREV=$((N - 1))
cat > /tmp/stix-continuity-prompt.txt << CONT_EOF
Compare these two screenshots for continuity:
1. .stix/qc/scene-${PREV}-kf100.png (end of scene $PREV)
2. .stix/qc/scene-${N}-kf0.png (start of scene $N)

Check:
- Character position consistency
- Pose continuity
- Prop consistency
- Emotional progression

Output: PASS or FAIL with specific fix notes.
Write to: .stix/qc/continuity-${PREV}-${N}.json
CONT_EOF

ENV_CMD="env"
if [ -n "$STIX_AGENT_ENV_UNSET" ]; then
  IFS=',' read -ra UNSET_VARS <<< "$STIX_AGENT_ENV_UNSET"
  for var in "${UNSET_VARS[@]}"; do
    [ -n "$var" ] && ENV_CMD="$ENV_CMD -u $var"
  done
fi

$ENV_CMD $STIX_AGENT_CLI \
  "$(cat /tmp/stix-continuity-prompt.txt)"
```

---

### Step 8: Frame Capture & Stitch

Run the capture script with inferred parameters. The capture script uses `agent-browser eval` to pause CSS animations and seek to exact millisecond positions — no timing drift.

```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")" 2>/dev/null || cd "$(dirname "$0")" && pwd)"

bash "$SKILL_DIR/scripts/capture.sh" \
  --scenes-dir .stix/scenes \
  --frames-dir .stix/frames \
  --output-dir .stix/output \
  --fps $FPS \
  --format $FORMAT
```

---

### Step 9: Report

After the pipeline completes, report to the user:

```
Animation complete!

Prompt: "a cat chasing a mouse across a park"
Scenes: 3
Duration: 24s (3 x 8s)
FPS: 8
Assets: 2 characters, 1 background, 2 props
QC: All scenes passed (1 required fix)

Output:
  GIF: .stix/output/animation.gif (270KB)
  MP4: .stix/output/animation.mp4 (90KB)
```

---

## Component Library Reference

When generating assets, the dispatcher must read these files and inject their full contents into worker prompts:

| File | Used by |
|------|---------|
| `library/style-guide.md` | All asset workers + scene composers |
| `library/poses.md` | Character asset workers |
| `library/transitions.md` | Scene composition workers |
| `library/expressions.md` | Character asset workers |
| `library/props.md` | Background + prop asset workers |
| `library/animals.md` | Character asset workers (for animal characters) |

## Asset Reference Templates

| File | Purpose |
|------|---------|
| `references/asset-character.md` | Template + instructions for character asset workers |
| `references/asset-background.md` | Template + instructions for background asset workers |
| `references/asset-props.md` | Template + instructions for prop asset workers |
| `references/scene-compose.md` | Instructions for scene composition workers |
| `references/scene-base.html` | Base HTML template for composed scenes |
| `references/qc-rubric.md` | QC evaluation rubric |

## Key Conventions

1. **Asset-first pipeline** — characters, background, and props are generated as reusable SVG assets before scene composition. This guarantees visual consistency across scenes.
2. **CSS-only animation** — no JavaScript in scene HTML. Deterministic timing, no race conditions.
3. **8s scene duration** — all `animation-duration: 8s` with `infinite` loop.
4. **Relative coordinates** — characters defined at origin, positioned via `translate()`.
5. **Phase-based scenes** — for multi-moment scenes, use opacity toggling (see `transitions.md` → phase_transition).
6. **Sub-loops** — walk cycle (0.5s), run cycle (0.4s) nest inside the 8s scene loop.
7. **Eval-based capture** — `agent-browser eval` pauses animations and seeks to exact millisecond positions. No sleep-based timing drift.
8. **Generation tier for creation, review tier for QC** — use your agent's most capable model for asset/scene generation, the fastest capable model for QC review.
9. **Max 3 QC fix iterations** — if still failing after 3, report the remaining issues to the user.
