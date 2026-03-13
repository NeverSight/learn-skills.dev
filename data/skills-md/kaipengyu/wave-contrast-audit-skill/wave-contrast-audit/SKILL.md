---
name: wave-contrast-audit
description: Audit a live webpage for WCAG color contrast failures using axe-core injected via Playwright, then map every failing color pair to its exact CSS rule and apply compliant fixes. Use when a WAVE report shows contrast errors or when asked to fix accessibility contrast issues on a deployed page.
---

# WAVE Contrast Audit

Systematically find and fix every color contrast violation on a live page using axe-core for precise data, then trace failures back to CSS source rules.

## When to Use This Skill

- A WAVE report shows contrast errors on a deployed page
- User shares a WAVE report URL (`wave.webaim.org/report#/...`)
- Asked to "fix contrast issues" or "make the site WCAG AA compliant"
- After a design system token change that may have introduced failures

## Core Workflow

### Step 1 — Navigate to the live page (not the WAVE report)

Always run axe-core on the **actual page**, not the WAVE report wrapper.

```
Navigate to: https://example.com/page.html
```

### Step 2 — Inject and run axe-core for exact color pairs

This gives you precise foreground/background hex values, contrast ratios, CSS selectors, and font sizes — far more actionable than clicking WAVE icons one by one.

```javascript
async () => {
  const script = document.createElement('script');
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js';
  document.head.appendChild(script);
  await new Promise(r => script.onload = r);

  const results = await axe.run({ runOnly: ['color-contrast'] });

  // Deduplicate by unique fg+bg pair
  const pairs = {};
  for (const v of results.violations) {
    for (const node of v.nodes) {
      for (const rel of node.any) {
        if (rel.data?.fgColor) {
          const key = `${rel.data.fgColor}__on__${rel.data.bgColor}`;
          if (!pairs[key]) {
            pairs[key] = {
              fg: rel.data.fgColor,
              bg: rel.data.bgColor,
              ratio: rel.data.contrastRatio,
              fontSize: rel.data.fontSize,
              fontWeight: rel.data.fontWeight,
              required: rel.data.expectedContrastRatio,
              count: 0,
              selector: node.target[0]
            };
          }
          pairs[key].count++;
        }
      }
    }
  }
  return {
    total: results.violations.reduce((a, v) => a + v.nodes.length, 0),
    pairs: Object.values(pairs).sort((a, b) => a.ratio - b.ratio)
  };
}
```

### Step 3 — Interpret the results

For each unique pair, note:
- **fg + bg** — the actual rendered hex values (rgba already resolved to hex)
- **ratio** — current contrast (e.g. 3.1:1)
- **required** — 4.5 (normal text) or 3.0 (large text >= 18px / >= 14px bold)
- **selector** — CSS selector pointing to the failing element
- **count** — how many elements share this exact pair

### Step 4 — Find the CSS source rules

Use `Grep` to locate every CSS rule producing the failing color:

```bash
# Search for the failing value (rgba or hex)
grep -n "rgba(255,255,255,.45)\|#7a7878\|var(--steel)" src/styles.css

# Or search by selector
grep -n "\.sb-num\|\.btn-water" src/styles.css
```

Read the surrounding context to confirm background color and element role.

### Step 5 — Calculate compliant replacement values

**For white text on dark backgrounds (`rgba(255,255,255, A)`):**

| Required | Min alpha on `#022b45` | Min alpha on `#034f7d` | Min alpha on `#7a4f99` |
|----------|------------------------|------------------------|------------------------|
| 4.5:1    | >= 0.75 (use **0.82**) | >= 0.75 (use **0.82**) | >= 0.85 (use **0.88**) |
| 3.0:1    | >= 0.50 (use **0.60**) | >= 0.52 (use **0.60**) | >= 0.60 (use **0.68**) |

**For brand blue on light backgrounds:**
- `#1499e8` on white = 3.1:1 (fail) — use `#0d77c4` for button bg (4.72:1)
- `#1499e8` as text on white — use `#0d77c4`

**For brand blue as text on dark backgrounds:**
- `#1499e8` on `#022b45` = 2.8:1 (fail) — use `#8accf4` (~5.0:1)

**For muted gray on white/cream:**
- `#7a7878` on white = 4.4:1 (fail) — darken to `#686666` (5.7:1)
- `#7a7878` on `#ededed` = 3.7:1 (fail) — `#686666` also passes cream (4.9:1)

**Manual luminance calculation (when needed):**
```
Contrast = (L_lighter + 0.05) / (L_darker + 0.05)
L = 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin
R_lin = ((R/255 + 0.055) / 1.055)^2.4   for values > 0.04045
R_lin = (R/255) / 12.92                  for values <= 0.04045
```

### Step 6 — Apply fixes efficiently

Batch all changes in a single Python pass to avoid making 50+ Edit calls:

```python
with open('styles.css', 'r') as f:
    css = f.read()

changes = [
    ('--steel: #7a7878',         '--steel: #686666'),
    ('.btn-water { background: var(--vibrant-blue)',
     '.btn-water { background: #0d77c4'),
    # Add targeted string replacements for each failing rule...
]

results = []
for old, new in changes:
    if old in css:
        css = css.replace(old, new)
        results.append(f"  changed: {old[:50]}")
    else:
        results.append(f"  NOT FOUND: {old[:50]}")

with open('styles.css', 'w') as f:
    f.write(css)

print('\n'.join(results))
```

> **Warning:** `rgba(255,255,255,.X)` appears in backgrounds, borders, and
> box-shadows — not only text color. Always read context before replacing.
> Use targeted string matches (include surrounding lines) rather than broad
> single-value replacements.

### Step 7 — Verify fixes

Re-run the Step 2 script on the updated page. Target: **0 color-contrast violations**.

If the file is only local (not yet deployed), navigate Playwright directly:
```
Navigate to: file:///path/to/page.html
```

---

## Common Failure Patterns

| Pattern | Failing value | Fix |
|---------|--------------|-----|
| Sidebar nav links on dark bg | `rgba(255,255,255,.5-.62)` | Raise to `.82` |
| Section labels on dark bg | `rgba(255,255,255,.18-.25)` | Raise to `.75` |
| Body text on dark bg | `rgba(255,255,255,.52-.62)` | Raise to `.85` |
| Small labels/captions on dark bg | `rgba(255,255,255,.38-.45)` | Raise to `.82` |
| Any text on purple bg (#7a4f99) | alpha < .85 | Raise to `.88` |
| CTA button (white on #1499e8) | 3.1:1 | Change bg to `#0d77c4` |
| Muted gray on white | `#7a7878` | Darken to `#686666` |
| Brand blue as text on white | `#1499e8` | Change to `#0d77c4` |
| Brand blue as text on dark | `#1499e8` | Change to `#8accf4` |
| Brand palette 25% tint on color bg | e.g. `#ded3e6` on purple | Use `var(--white)` |

## WCAG 2.2 AA Thresholds (Quick Reference)

| Text size | Required ratio |
|-----------|---------------|
| Normal (< 18px regular, < 14px bold) | **4.5 : 1** |
| Large (>= 18px regular, >= 14px bold) | **3.0 : 1** |
| UI components and icons | **3.0 : 1** |

## WAVE False Alarms & How to Avoid Them

WAVE evaluates the DOM **after JavaScript runs**, at the initial scroll position (top of page). This causes predictable false positives that must be distinguished from real failures.

### 1 — GSAP scroll animations (`opacity: 0` → reported as 1:1 contrast)

`gsap.fromTo()` immediately applies the FROM state as an inline style the moment the script runs. Every element targeted by a scroll-triggered fade-in gets `opacity: 0` before any scrolling occurs. WAVE computes the rendered text color including opacity, so `color: #022b45` at `opacity: 0` becomes `rgba(2,43,69,0)` — a 1:1 contrast failure.

**Diagnosis**: Click the WAVE error icon — the element disappears. WAVE's code panel shows `color: rgba(r,g,b,0)` with alpha = 0.

**Fix**: Replace `opacity` with GSAP's `autoAlpha` in all content animation vars.

```javascript
// BEFORE — causes WAVE false alarms
gsap.set('.hero-title', { opacity: 0, y: 30 });
gsap.to('.hero-title',  { opacity: 1, y: 0, duration: 1 });

// AFTER — WAVE skips visibility:hidden elements, no false alarm
gsap.set('.hero-title', { autoAlpha: 0, y: 30 });
gsap.to('.hero-title',  { autoAlpha: 1, y: 0, duration: 1 });
```

`autoAlpha: 0` sets `opacity: 0; visibility: hidden`. WAVE's documented rule: *"Errors are only reported on elements visible to users"* — `visibility: hidden` is explicitly excluded from contrast checks.

Apply to all `gsap.set`, `gsap.fromTo`, and `gsap.to` calls that fade content in. Do **not** apply to background image wrappers or decorative elements that already use `aria-hidden`.

### 2 — Background-image elements (reported as 1:1 contrast)

Elements that use a child div for `background-image` (and a `::after` gradient overlay for the dark backdrop) have **no `background-color`** on the container. WAVE can't load images or evaluate gradients, so it falls back to white. White text on white = 1:1.

**Diagnosis**: Hero sections with photos behind text flagged at 1:1 despite visually clear contrast.

**Fix**: Add a solid `background-color` fallback matching the darkest gradient value. This is invisible to visual users (the image covers it) but gives WAVE a computable dark color.

```css
/* The gradient goes to rgba(4,14,25,.97) at the bottom */
.hero-a {
  background-color: #040e19; /* fallback for contrast tools that can't read background-image */
  /* rest of rules... */
}
.hero-b-left {
  background-color: #040e19;
}
```

Note: `hero-c` uses `background: #040f1c` directly (no child image div), so it never had this issue.

### 3 — Low-opacity decorative glyphs (chevrons, watermarks)

Elements with `opacity: 0.4` or similar applied via CSS/GSAP inherit a dimmed version of their parent's text color. WAVE computes this as the rendered color and flags it.

**Common culprit**: Dropdown chevrons (`▾`) inside nav links styled with `opacity: .4`.

**Fix**: `aria-hidden="true"` — these are purely decorative; the link text already conveys the interactive meaning.

```html
<!-- BEFORE -->
<a href="#">Our Work <span class="snav-chev">▾</span></a>

<!-- AFTER -->
<a href="#">Our Work <span class="snav-chev" aria-hidden="true">▾</span></a>
```

Similarly for oversized watermark text (giant serif letters behind content):
```html
<div class="tq-bg" aria-hidden="true">"</div>
<div class="co-type-bg" aria-hidden="true">Water</div>
```

### 4 — Form labels not programmatically linked

WAVE flags `<label>` elements that exist visually but are not connected to their input via `for`/`id`. These show as "Missing form label" errors, not contrast errors.

**Fix**: Add matching `for` and `id` attributes.

```html
<!-- BEFORE -->
<label class="f-label">Email Address</label>
<input class="f-input" type="email" placeholder="alex@example.com">

<!-- AFTER -->
<label class="f-label" for="f-email">Email Address</label>
<input id="f-email" class="f-input" type="email" placeholder="alex@example.com">
```

### False alarm vs. real failure — decision table

| WAVE symptom | Click element → it disappears? | Likely cause | Fix |
|---|---|---|---|
| 1:1 contrast on heading | Yes | GSAP `opacity: 0` inline | Switch to `autoAlpha` |
| 1:1 contrast on hero text | No | No `background-color` fallback on image container | Add solid dark `background-color` |
| Low contrast on tiny glyph | N/A | Decorative icon with low opacity | `aria-hidden="true"` |
| Low contrast on label text | No | Real failure — muted color on light bg | Darken the color token |
| Missing form label | N/A | No `for`/`id` association | Add `for`/`id` pair |

## Limitations

- axe-core **skips** elements where background is a CSS gradient, `background-image`,
  or `filter` — use WAVE's eyedropper tool for those manually
- WAVE counts each text node individually; axe deduplicates by color pair — expect
  axe to report fewer total violations than WAVE (e.g. 53 axe vs 187 WAVE)
- Hover and focus states are not evaluated by either tool — test manually
- Decorative elements (watermarks, icon chevrons, spacers) should receive
  `aria-hidden="true"` rather than contrast fixes
- WAVE evaluates all DOM elements regardless of scroll position — elements hidden by
  scroll-triggered JS animations will be flagged unless using `autoAlpha` or `visibility: hidden`

## Resources

- [WAVE Web Accessibility Evaluator](https://wave.webaim.org/)
- [axe-core CDN](https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [WCAG 2.2 — 1.4.3 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
