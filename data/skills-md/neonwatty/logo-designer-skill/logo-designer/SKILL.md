---
name: logo-designer
description: |
  Design and iterate on logos using SVG. Use this skill when the user asks to
  "create a logo", "design a logo", "make me a logo", "iterate on this logo",
  "logo for my project", or discusses logo design, branding icons, or wordmarks.
version: 1.0.0
license: MIT
---

# Logo Designer

Design and iterate on logos using SVG. Generates side-by-side previews and exports to PNG at standard sizes.

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
   - Use `subagent_type: "general-purpose"` and `mode: "bypassPermissions"`
3. After all agents complete, generate `logos/preview.html` and present the results

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

After all parallel agents complete:

1. Generate `logos/preview.html` using the preview template below
2. Tell the user to open `logos/preview.html` in their browser
3. Briefly describe each concept (1 sentence each) so the user can match descriptions to visuals
4. Ask: "Which direction do you want to explore? Pick a number, or describe what you like/dislike across them."

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

This is especially important for icon-only logos. If details disappear at 32px, suggest simplifying (remove fine details, thicken strokes, drop decorative elements).

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
3. After all agents complete, regenerate `logos/preview.html` and present the results

**Example batch dispatch:**

```
Task 1: "Take this base SVG [full SVG content] and create a variation with a warm color palette (reds, oranges, yellows). Write to logos/iterations/iteration-5.svg."

Task 2: "Take this base SVG [full SVG content] and create a variation with a cool color palette (blues, teals, purples). Write to logos/iterations/iteration-6.svg."

Task 3: "Take this base SVG [full SVG content] and create a variation with a monochrome palette (grays + one accent). Write to logos/iterations/iteration-7.svg."
```

Use `subagent_type: "general-purpose"` and `mode: "bypassPermissions"` for each agent. Always include the full base SVG content in each agent's prompt — agents do not share context.

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
3. Regenerate `logos/preview.html` after each iteration, showing all iterations (most recent first) so the user can compare
4. Tell the user to refresh their browser after each iteration
5. After each iteration, briefly describe what changed and ask for next feedback

### Iteration tips

- If the user says "go back to iteration N", use that as the new base
- If the user wants to compare specific iterations, mention which filenames to look at in the preview
- Keep SVG structure consistent across iterations (same group IDs) so the user can track what changed
- Use parallel agents for batch exploration (3+ variations), sequential writes for single tweaks
- **Check small-size legibility** — After generating iterations, include the favicon size check strip in the preview. If thin strokes vanish at 32px, proactively suggest thickening them. If fine details (clocks, sparkles, thin icons) become unreadable, suggest removing or simplifying them. This saves iteration cycles.
- When the user is satisfied, move to Phase 4

## Phase 4: Export

When the user says "export", "I'm happy with this", "this is the one", or similar:

1. Identify the final iteration SVG (ask the user to confirm which one if ambiguous)
2. Create the `logos/export/` directory
3. Copy the final SVG to `logos/export/logo.svg`
4. Run the bundled export script to generate PNGs:

```bash
bash <path-to-skill>/scripts/export.sh logos/export/logo.svg logos/export/
```

The script produces:
- `logo-16.png`
- `logo-32.png`
- `logo-48.png`
- `logo-192.png`
- `logo-512.png`
- `logo-1024.png`
- `logo-2048.png`

5. Report the results: list all exported files with their sizes
6. If the export script fails (no conversion tool found), tell the user:
   > "No SVG-to-PNG converter found. Install one of: `npm install -g @aspect-build/resvg`, or install Inkscape, or install librsvg. Then run export again."

### Export script location

The export script is bundled with this skill at `scripts/export.sh` relative to the SKILL.md file. Use the skill's directory path to locate it.

## Phase 5: Repo Integration (optional)

If the user asks to commit the logo to a project repo or create a PR:

1. **Identify target files** — Check the repo for existing icon/logo files: `public/favicon.svg`, `public/favicon.ico`, `public/pwa-*.png`, `public/apple-touch-icon.png`, `assets/logo.svg`, `ios/.../AppIcon.appiconset/`, `public/manifest.json`, etc.
2. **Clone and branch** — Clone the repo (or use the existing checkout), create a branch like `chore/new-logo`
3. **Replace files** — Copy the final SVG as the favicon/logo. Generate platform-specific sizes:
   - `favicon.ico` — 48px (use ImageMagick `convert` or `magick`)
   - `apple-touch-icon.png` — 180px
   - `pwa-192x192.png` — 192px
   - `pwa-512x512.png` — 512px
   - iOS `AppIcon-512@2x.png` — 1024px
   - Only replace files that already exist in the repo — don't add new ones the project doesn't use
4. **Commit and PR** — Commit with a message like `chore: replace logo with new [description]`, push, and create a PR with a summary of what was updated
