---
name: ui-logo-designer
description: |
  Design and iterate on logos using SVG. Use this skill when the user asks to
  "create a logo", "design a logo", "make me a logo", "iterate on this logo",
  "logo for my project", or discusses logo design, branding icons, or wordmarks.
version: 1.0.0
license: MIT
source: https://github.com/tstapler/logo-designer-skill (forked from neonwatty/logo-designer-skill)
---

# Logo Designer

Design and iterate on logos using SVG. Generates side-by-side previews and exports to PNG at standard sizes.

> For brand strategy and visual direction that feeds logo design, apply the `pm-brand-strategy` skill.

## Phase 1: Interview

Before generating anything, gather context and ask the user what they need.

### Step 1: Gather context automatically

If the user points to a repo, URL, or existing project:
- Read the README, package.json, CSS/config files, and any existing branding
- Extract: project name, purpose, tech stack, color palette, design language, fonts
- Summarize what you found before asking questions — this avoids asking things you already know

If the user just says "design a logo" with no project context, skip to Step 2.

### Step 2: Ask structured questions

Use the `AskUserQuestion` tool to ask these questions. **Batch related questions together** (up to 4 per call) and **skip any question already answered** by the context gathered in Step 1 or by the user's initial message.

**Question 1 — Format:**
```
question: "What format do you need?"
header: "Format"
options:
  - label: "Icon only (512x512)"
    description: "Square icon, works for favicons, app icons, social avatars"
  - label: "Wordmark only"
    description: "Text logo, 1024x512"
  - label: "Combination mark"
    description: "Icon + text together, 1024x512"
```

**Question 2 — Style direction:**
```
question: "What style direction?"
header: "Style"
options:
  - label: "Minimal / geometric"
    description: "Clean lines, simple shapes, modern feel"
  - label: "Playful / hand-drawn"
    description: "Friendly, casual, organic shapes"
  - label: "Bold / corporate"
    description: "Strong, professional, high contrast"
  - label: "Match existing app style"
    description: "I'll extract the design language from your project"
```

**Question 3 — Color preferences:**
```
question: "Any color preferences?"
header: "Colors"
options:
  - label: "Use project colors"
    description: "I'll pull colors from your existing design system"
  - label: "Surprise me"
    description: "I'll pick a palette that fits the vibe"
  - label: "I have specific colors"
    description: "I'll ask you for them"
```

**Question 4 — Output size** (only if the user mentioned a specific platform):
```
question: "Any specific size requirements?"
header: "Size"
options:
  - label: "Standard sizes"
    description: "16, 32, 48, 192, 512, 1024, 2048px — covers most uses"
  - label: "Custom size needed"
    description: "I'll ask for the exact dimensions"
```

### Adapting to context

- **User points to a repo:** Gather context first, then ask only format + style (colors are likely known).
- **User says "design a logo for X":** Ask format, style, and colors together.
- **User gives detailed description:** Skip everything already covered, ask only what's missing.
- **User says "just make something":** Use sensible defaults (icon only, minimal, surprise me) and go straight to Phase 2.

Move to Phase 2 once you have enough to generate distinct concepts.

## Iconography Principles (Research-Backed)

Apply these during concept generation and Phase 2.5 review. They are verified findings, not preferences.

### 1. Discovered meaning > stated meaning (Gestalt, confidence: high)

The most memorable logos embed a secondary meaning in negative space — the viewer finds it rather than being shown it. This creates disproportionate recall (FedEx arrow: functional metaphor discovered in letterform, confirmed 3–0 adversarially).

**In practice:** Always look for a secondary form that can live in the negative space, counter, hole, or gap of the primary shape. The primary form must be readable alone at 16px — the secondary meaning is the 512px reward.

**For Sortie:** The departure vector (up-right arrow) is the natural hidden element. The tag hole, an S counter, or the gap between bars are all valid hiding places.

### 2. Angular geometry = competence, precision (confidence: medium, 2–1)

Angular shapes (45° angles, sharp joints, grid-aligned paths) reliably signal competence and precision. Rounded shapes signal warmth and approachability. Peer-reviewed across Journal of Consumer Psychology, Bouba-Kiki effect (95–98% cross-cultural), and Shape-Trait Consistency (PMC 2021).

**Caveat:** Acute spikes trigger threat associations. Use even proportions and the brand's warm palette to stay in "precision" not "aggression."

**In practice:** Prefer geometric polygon shapes over rounded rectangles for the primary mark. The palette does the warmth work — the mark should be unambiguously sharp.

### 3. 16px = 256 total pixels. Two or three filled regions, maximum (confidence: high, 3–0)

Hard constraint. Any element thinner than ~1px at render size disappears. Pixel-grid misalignment at 16–24px introduces visible noise. Modern favicon bundles include 32/48/192px too, but design against 16px first.

**In practice:** The mark must consist of solid filled geometric regions, not a line-based illustration. Every element must be at least 32px in SVG units (≈1px at 16px render) to survive. The hidden secondary element must work as part of the primary silhouette — it cannot be a hairline detail layered on top.

### 4. Literal category illustration = category membership

Using a luggage icon positions the brand alongside every other packing app (Packr, PackPoint, TripIt — all use a suitcase). The icon should encode the brand's *mechanic* (what it does) rather than its *object* (what it handles).

**In practice:** Ask what the product *does* rather than what it *contains*. A packing app's mechanic is list generation, trip-based filtering, and review loops — not bags. An abstract or letterform mark that encodes this mechanic will always outperform a literal luggage illustration.

### 5. Landscape shapes fail in square icon slots

A wide/short primary shape (duffel bag, horizontal bars) in a 512×512 viewBox leaves massive vertical dead zones and renders as a tiny horizontal stripe at 16px. The primary silhouette should occupy at least 65% of the viewBox height.

### 6. Accent color on the discovery, not the container

If using a two-color approach, apply the accent to the secondary/hidden element. The primary form in the dominant brand color. Finding the accent triggers the brand moment — it should reward attention, not announce itself.

**In practice:** Primary shape in olive (#3D5A47) or off-white (#F5F1EB). Ember (#C4743A) on the departure vector, closure element, or discovered meaning.

---

## SVG Conventions

When generating SVG logos, follow these rules:

- **viewBox sizing** — Always use `viewBox="0 0 W H"` without fixed `width`/`height` attributes. Use 512x512 for icons, 1024x512 for wordmarks/combination marks.
- **Self-contained** — No external fonts, images, or `<use>` references to other files. Everything inline.
- **Text handling** — Use widely available system fonts (Arial, Helvetica, Georgia, etc.) or convert text to `<path>` elements. When using system fonts, always include a generic fallback (e.g., `font-family="Helvetica, Arial, sans-serif"`).
- **Meaningful groups** — Wrap logical sections in `<g>` elements with descriptive IDs: `id="icon"`, `id="wordmark"`, `id="tagline"`. This makes iteration easier when the user says "make the icon bigger" or "change the wordmark color".
- **Flat fills by default** — Use solid `fill` colors. Only use gradients (`<linearGradient>`, `<radialGradient>`) when the user requests them or the style clearly calls for it.
- **Small-size legibility** — Logos must work at 16-32px (favicons). Prefer solid fills over thin strokes, avoid fine details that disappear at small sizes, and use `stroke-width` of 6+ for any outlines that need to remain visible. Test this mentally: if a detail won't survive being 32px wide, simplify it.
- **Clean markup** — No unnecessary transforms, no empty groups, no default namespace clutter. Keep the SVG readable.

## Phase 2: Explore

Generate 3-5 **distinct** SVG logo concepts. Each concept should take a meaningfully different creative direction — vary the icon metaphor, typography style, layout, or overall aesthetic. Do not generate minor variations of the same idea.

### Parallel generation

Use the `Task` tool to generate all concepts in parallel. This is significantly faster than writing them sequentially.

1. Create the `logos/concepts/` directory first
2. Dispatch one `Task` agent per concept, all in the **same message** so they run concurrently. Each agent should:
   - Receive the full design brief (format, style, colors, viewBox, SVG conventions)
   - Be assigned a specific creative direction (e.g., "geometric letterform", "abstract symbol", "mascot-based")
   - Write its SVG to a specific file path (e.g., `logos/concepts/concept-1.svg`)
   - Use `subagent_type: "general-purpose"`
3. After all agents complete, **you** (the main agent) generate `logos/preview.html` — do not delegate this step, as it must happen in the same turn as presenting results to the user

**Example dispatch pattern** (all in one message):

```
Task 1: "Write logos/concepts/concept-1.svg — geometric letterform using [colors]. viewBox 512x512. Self-contained SVG, no external fonts. [full SVG conventions]."

Task 2: "Write logos/concepts/concept-2.svg — abstract symbol using [colors]. viewBox 512x512. Self-contained SVG, no external fonts. [full SVG conventions]."

Task 3: "Write logos/concepts/concept-3.svg — mascot-based icon using [colors]. viewBox 512x512. Self-contained SVG, no external fonts. [full SVG conventions]."
```

Each agent prompt must include: the full SVG conventions from this skill, the target file path, the specific creative direction, and all relevant context (project name, colors, style preferences). Agents do not share context — give each one everything it needs.

### File output

```
logos/
├── concepts/
│   ├── concept-1.svg
│   ├── concept-2.svg
│   ├── concept-3.svg
│   └── ... (up to concept-5.svg)
└── preview.html
```

After all parallel agents complete, proceed to **Phase 2.5: Auto-Review & Improve** before showing anything to the user.

## Phase 2.5: Auto-Review & Improve

**Run automatically after every generation step (concepts and iterations) before showing the user anything.** Never skip this phase. The user should only see polished, vetted outputs.

### Step 1: Read all generated SVGs

Read each SVG file yourself. Do not delegate — you need the coordinates to do the geometry checks.

### Step 2: Adversarial geometry check (do this yourself)

For each SVG, work through the coordinates explicitly:

- **Checkmark intersection**: trace the checkmark polyline segments. At each x value where a manifest bar exists, compute the checkmark's y at that x. If that y falls within a bar's y range (bar.y to bar.y + bar.height), the checkmark intersects the bar — this causes a visual artifact. Fix by adjusting the checkmark's anchor point, angle, or scale so the upstroke clears all bars.
- **Element overlap**: do any same-color elements sit directly on top of each other? (e.g., handle same fill as body = invisible handle). Flag or fix.
- **Favicon legibility**: at 16px, the viewBox (512px) compresses by 32×. Any element thinner than 16px in SVG units (~0.5px at favicon) disappears. Any detail smaller than 32px SVG units reads as noise at 32px favicon. Mentally simulate: what shapes survive? If the icon reads as an unrecognizable blob, it needs simplification.
- **Aspect ratio trap**: for a 512×512 square viewBox, the dominant shape should be roughly square or use the full canvas. A strongly landscape shape (e.g., 352px wide × 210px tall duffel) leaves large dead zones top and bottom and reads as a flat rectangle at small sizes.
- **Handle/detail color-blending**: any element that shares fill color with its immediate visual background will be invisible at small sizes. Flag it.

### Step 3: Design review (spawn one agent)

Spawn a single agent with all SVG file contents inline. Ask it to review each candidate against the **Iconography Principles** defined earlier in this skill. Specifically:

- **Gestalt check:** Is there a secondary meaning discoverable in negative space, a counter, or a gap? Does the mark reward closer inspection, or is everything stated at first glance?
- **Angular vs. curved:** Does the geometry match the brand personality? Angular = systematic/sharp; rounded = warm/friendly.
- **Category trap:** Does the primary silhouette read as a product category (travel, productivity, todo) rather than as this specific brand? Would it be confused with a competitor's icon?
- **Combination mark potential:** Does the silhouette work at ~48px next to the brand name? Is it too wide, too tall, or too complex for a lockup?
- **Accent placement:** Is the accent color on the discovery/secondary element, or is it on the container?

Agent prompt pattern:
```
You are a logo design critic with expertise in gestalt psychology and icon design.
Review these SVG logo candidates for [brand name].
Brand brief: [paste relevant brand context — personality, aesthetic refs, what to avoid]
Iconography principles to evaluate against:
1. Does the mark embed a secondary meaning in negative space? (Gestalt — highest value)
2. Is the geometry angular/sharp (competence) or rounded (warmth)? Does it match the brand?
3. Does it avoid the category illustration trap (no literal product objects)?
4. Does it consist of 2–3 filled regions that survive at 16px?
5. Is the accent applied to the discovered element, not the container?
[paste each SVG file content with its label]
For each candidate: score 1–5 on each principle, then give a one-line verdict: kill / fix / keep.
Rank all candidates 1st to last. Return plain text.
```

### Step 4: Apply fixes

For each confirmed issue:

**Geometry fix** (checkmark intersection, invisible element, aspect ratio problem): fix it directly by editing the SVG yourself. Show your coordinate math in a `<!-- fix: ... -->` comment on the changed element. Example: `<!-- fix: upstroke tip moved from y=244 to y=215 to clear bar-2 bottom at y=248 -->`.

**Concept-level issue** (wrong shape, brand mismatch, weak gestalt, poor scalability — anything the design-review agent scored low or flagged as "fix"): do NOT just note it and move on — auto-refine it now, before the user ever sees it. The user should not have to spend a round of feedback asking you to address something the critic agent already found.

- For each concept scored **"fix"**: dispatch one `Task` agent (same mechanism as Phase 3's batch iterations) whose prompt is the base SVG plus the *exact* critique text from Step 3 as the brief to address. Run all of these in parallel, one per flagged concept, in the same message. Save each result as `logos/concepts/concept-N.svg` (overwrite in place — this is still pre-release polish, not a user-visible iteration yet).
- For each concept scored **"kill"**: do not try to salvage it with a patch — the critic found it fundamentally off-brief, not just rough. Either (a) drop it from the set entirely, or (b) if the user asked for a specific count of concepts, replace it with a fresh concept from a genuinely different creative angle (dispatch a new Task agent with a new direction, not a variation of the killed one). Never silently present a "kill"-rated concept as-is.
- For each concept scored **"keep"**: leave it untouched, or apply only the specific minor polish the critic called out (if any) — don't over-iterate something that already scored well.
- After the auto-refine agents return, re-read the changed SVGs yourself and re-run the Step 2 geometry check on anything that changed (a refinement pass can introduce its own new geometry bugs — e.g. new elements running flush to a canvas edge). Fix directly as needed.
- This auto-refine pass runs at most once per generation step. Do not loop indefinitely chasing a perfect score — one corrective pass, then present. Remaining subjective/taste-level notes (not objective scoring failures) are fine to surface to the user as discussion points, not defects to keep fixing.

### Step 5: Present to the user

After fixes and auto-refinement are applied:

1. Generate `logos/preview.html` (see template below) with the corrected/refined files
2. Tell the user to open `logos/preview.html`
3. Briefly describe each concept (1 sentence each)
4. List any geometry fixes applied (one line each: *"Fixed: checkmark upstroke cleared bar-2 on concept-3"*)
5. List any concept-level auto-refinements applied (one line each: *"Auto-refined: concept-2's gold accent moved from the outer border to the discovered interior mark, per the critic's accent-placement note"*) — this is disclosure of what already happened, not a request for the user to approve a fix first; the polished version is what's in the preview.
6. List any concept that was dropped/replaced and why (one line each: *"Dropped concept-4 (killed: generic monogram, no brand connection) — replaced with a new abstract-symbol direction"*)
7. Ask: "Which direction do you want to explore? Pick a number, or describe what you like/dislike."

The same Steps 1–5 apply at the end of Phase 3 (Refine) after generating each new iteration batch, before presenting to the user — including the auto-refine sub-step for any concept-level issues the reviewer raises on an iteration.

---

### Preview HTML Template

When generating `logos/preview.html`, use this template. Replace `{{CARDS}}` with one card per SVG file. Set `{{PHASE}}` to "Concepts" during explore or "Iterations" during refine.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Logo Preview — {{PHASE}}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 2rem;
    transition: background-color 0.3s, color 0.3s;
  }
  body.light { background: #f5f5f5; color: #333; }
  body.dark { background: #1a1a1a; color: #eee; }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  h1 { font-size: 1.5rem; font-weight: 600; }
  .toggle {
    padding: 0.5rem 1rem;
    border: 1px solid currentColor;
    border-radius: 6px;
    background: transparent;
    color: inherit;
    cursor: pointer;
    font-size: 0.875rem;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  .card {
    border: 1px solid rgba(128, 128, 128, 0.3);
    border-radius: 12px;
    overflow: hidden;
  }
  .card-img {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    min-height: 240px;
  }
  body.light .card-img { background: #fff; }
  body.dark .card-img { background: #2a2a2a; }
  .card-img img {
    max-width: 100%;
    max-height: 200px;
  }
  .card-label {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    font-weight: 500;
    border-top: 1px solid rgba(128, 128, 128, 0.3);
  }
  body.light .card-label { background: #fafafa; }
  body.dark .card-label { background: #222; }
</style>
</head>
<body class="light">
  <div class="header">
    <h1>Logo Preview — {{PHASE}}</h1>
    <button class="toggle" onclick="document.body.classList.toggle('dark'); document.body.classList.toggle('light'); this.textContent = document.body.classList.contains('dark') ? '☀️ Light' : '🌙 Dark';">🌙 Dark</button>
  </div>
  <div class="grid">
    {{CARDS}}
  </div>
</body>
</html>
```

#### Favicon size check strip

During Phase 3 (Refine), add a "Favicon Size Check" section below the iteration grid. This renders each iteration at 64px, 32px, and 16px so the user can spot legibility issues early. Use this HTML pattern:

```html
<h2>Favicon Size Check</h2>
<div style="display:flex;gap:2rem;flex-wrap:wrap;align-items:end;">
  <!-- Repeat for each iteration -->
  <div style="display:flex;flex-direction:column;align-items:center;gap:0.5rem;">
    <div style="font-size:0.8rem;font-weight:500;">{{LABEL}}</div>
    <div style="display:flex;gap:1rem;align-items:end;">
      <div><img src="{{PATH}}" width="64" height="64"><div style="font-size:0.75rem;opacity:0.6;">64px</div></div>
      <div><img src="{{PATH}}" width="32" height="32"><div style="font-size:0.75rem;opacity:0.6;">32px</div></div>
      <div><img src="{{PATH}}" width="16" height="16"><div style="font-size:0.75rem;opacity:0.6;">16px</div></div>
    </div>
  </div>
</div>
```

Each `{{CARDS}}` entry is:

```html
<div class="card">
  <div class="card-img">
    <img src="{{PATH}}" alt="{{LABEL}}">
  </div>
  <div class="card-label">{{LABEL}}</div>
</div>
```

Where `{{PATH}}` is the relative path from `logos/` (e.g., `concepts/concept-1.svg` or `iterations/iteration-3.svg`) and `{{LABEL}}` is the filename without extension (e.g., "concept-1" or "iteration-3").

During **explore**, show all concepts. During **refine**, show all iterations (most recent first).

## Phase 3: Refine

Once the user picks a concept direction, iterate on it.

### Single vs. batch iterations

**Single iteration** — When the user gives specific feedback ("make the icon bigger", "change the blue to green"), apply the change directly and write the next iteration SVG yourself.

**Batch variations** — When exploring multiple directions at once ("try different color palettes", "show me 5 variations of the eye shape", "experiment with bar count"), use the `Task` tool to generate variations in parallel, just like Phase 2:

1. Dispatch one `Task` agent per variation, all in the same message
2. Each agent receives: the base SVG content (copy the full SVG inline in the prompt), the specific variation to apply, the target file path, and the full SVG conventions
3. After all agents complete, run **Phase 2.5: Auto-Review & Improve** before presenting results

Use `subagent_type: "general-purpose"` for each agent. Always include the full base SVG content in each agent's prompt — agents do not share context.

### File output

```
logos/
├── iterations/
│   ├── iteration-1.svg    # First refinement (based on chosen concept)
│   ├── iteration-2.svg
│   └── ...
└── preview.html           # Regenerated to show iterations
```

1. Copy the chosen concept as the starting point — save the first refinement as `logos/iterations/iteration-1.svg`
2. Apply the user's feedback and save each new version with an incrementing number
3. Regenerate `logos/preview.html` after each iteration, showing all iterations (most recent first)
4. Tell the user to refresh their browser after each iteration
5. After each iteration, briefly describe what changed and ask for next feedback

### Iteration tips

- If the user says "go back to iteration N", use that as the new base
- Keep SVG structure consistent across iterations (same group IDs) so the user can track what changed
- Use parallel agents for batch exploration (3+ variations), sequential writes for single tweaks
- **Always run Phase 2.5 after each iteration batch** — geometry fixes and design review before presenting
- When the user is satisfied, move to Phase 4

## Phase 4: Export

When the user says "export", "I'm happy with this", "this is the one", or similar:

1. Identify the final iteration SVG (ask the user to confirm which one if ambiguous)
2. Create the `logos/export/` directory
3. Copy the final SVG to `logos/export/logo.svg`
4. Run the bundled export script to generate PNGs. Use the **absolute path** to the SVG — relative paths fail when working in git worktrees:

```bash
bash ~/.claude/skills/ui-logo-designer/scripts/export.sh /absolute/path/to/logos/export/logo.svg /absolute/path/to/logos/export/
```

The script produces: `logo-16.png`, `logo-32.png`, `logo-48.png`, `logo-192.png`, `logo-512.png`, `logo-1024.png`, `logo-2048.png`

5. Report the results: list all exported files with their sizes
6. If the export script fails (no conversion tool found), tell the user:
   > "No SVG-to-PNG converter found. Install one of: `brew install librsvg` (provides `rsvg-convert`), `brew install inkscape`, or `npm install -g @aspect-build/resvg`. Then run export again."

7. **Always proceed to Phase 4.5** — wire up all platforms before reporting done.

## Phase 4.5: Platform Wiring (always run after export)

After the export script completes, immediately deploy icons to every platform target found in the repo. Do not skip this step or wait for the user to ask.

### Step 1: Detect platforms

Scan the repo for platform indicators:

| Platform | Indicator |
|---|---|
| Web / PWA | `index.html` + `manifest.json` in any resources dir |
| Android | `AndroidManifest.xml` |
| iOS | `*.xcassets` / `AppIcon.appiconset` |
| Electron / desktop | `package.json` with `electron` dependency |

### Step 2: Web / PWA

Target: the directory containing `manifest.json` and `index.html` (e.g. `webApp/src/wasmJsMain/resources/` for KMP projects, `public/` for Vite/Next projects).

Generate and copy:
```bash
SVG=/path/to/logos/export/logo.svg
RES=/path/to/web/resources

rsvg-convert -w 192 -h 192 "$SVG" -o "$RES/icon-192.png"
rsvg-convert -w 512 -h 512 "$SVG" -o "$RES/icon-512.png"
rsvg-convert -w 180 -h 180 "$SVG" -o "$RES/apple-touch-icon.png"
rsvg-convert -w 16  -h 16  "$SVG" -o /tmp/fav16.png
rsvg-convert -w 32  -h 32  "$SVG" -o /tmp/fav32.png
rsvg-convert -w 48  -h 48  "$SVG" -o /tmp/fav48.png
magick /tmp/fav16.png /tmp/fav32.png /tmp/fav48.png "$RES/favicon.ico"
```

Update `manifest.json`:
- `background_color` → primary brand color (not `#f5f5f5`)
- `theme_color` → primary brand color (not `#009688` or another default)

Update `index.html` — add inside `<head>` if missing:
```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="[brand color]">
```

### Step 3: Android

Target: `androidApp/src/main/res/` (KMP) or `app/src/main/res/` (standard Android).

Generate mipmap icons at all densities:
```bash
SVG=/path/to/logos/export/logo.svg
RES=/path/to/android/res

declare -A SIZES=([mdpi]=48 [hdpi]=72 [xhdpi]=96 [xxhdpi]=144 [xxxhdpi]=192)
for density in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
  mkdir -p "$RES/mipmap-${density}"
  rsvg-convert -w ${SIZES[$density]} -h ${SIZES[$density]} "$SVG" \
    -o "$RES/mipmap-${density}/ic_launcher.png"
  rsvg-convert -w ${SIZES[$density]} -h ${SIZES[$density]} "$SVG" \
    -o "$RES/mipmap-${density}/ic_launcher_round.png"
done
```

Update `AndroidManifest.xml` — add to `<application>` if missing:
```xml
android:icon="@mipmap/ic_launcher"
android:roundIcon="@mipmap/ic_launcher_round"
```

### Step 4: iOS (if `*.xcassets` found)

Populate `AppIcon.appiconset/` with required sizes and update `Contents.json`:

| Filename | Size |
|---|---|
| `Icon-20@2x.png` | 40×40 |
| `Icon-20@3x.png` | 60×60 |
| `Icon-29@2x.png` | 58×58 |
| `Icon-29@3x.png` | 87×87 |
| `Icon-40@2x.png` | 80×80 |
| `Icon-40@3x.png` | 120×120 |
| `Icon-60@2x.png` | 120×120 |
| `Icon-60@3x.png` | 180×180 |
| `Icon-1024.png`  | 1024×1024 |

```bash
for size in 40 58 60 80 87 120 180 1024; do
  rsvg-convert -w $size -h $size "$SVG" -o "AppIcon.appiconset/Icon-${size}.png"
done
```

### Step 5: Report

List every file written, grouped by platform. Example:

```
Web:     favicon.ico, icon-192.png, icon-512.png, apple-touch-icon.png
Android: mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher{,_round}.png
iOS:     (not found — skipped)
```

## Phase 5: Repo Integration (optional)

If the user asks to commit or create a PR:

1. **Stage** — `git add logos/export/ webApp/src/ androidApp/src/ [ios path if any]`
2. **Commit** — `chore: add Sortie logo (iteration-N) across web, Android, and iOS`
3. **PR** — push branch, open PR with before/after favicon screenshots if possible

---

## Related Skills

| Skill | When to apply |
|-------|--------------|
| `pm-brand-strategy` | Define brand personality and visual direction before generating logo concepts |
| `pm-brand-guidelines` | Enforce clear space, color, and usage rules after the logo is finalized |
| `ui-frontend-design` | Implement the logo in frontend code with proper SVG/CSS integration |
| `ui-design-system` | Align logo with broader design tokens (colors, typography) |
