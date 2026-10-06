---
name: design-critique
description: >
  Critique an existing design (web page, HTML/React UI, screenshot, generated image,
  or Figma frame) with a repeatable procedure: capture it (Playwright screenshots or
  Read for images), run automated checks (axe, style inventory), score against a
  weighted rubric, and output severity-ranked fixes with code, then re-verify.
  Use after any design is produced or when asked to review one. Trigger phrases: "design critique", "review design",
  "improve design", "design audit", "design feedback", "evaluate UI",
  "design score", "accessibility audit", "visual review", "design assessment"
license: MIT
---

# Design Critique

Systematically evaluate existing designs and provide specific, actionable improvements with code.

## Prerequisites

- Read `.agents/design-context.md` (see `design-context`) for brand colors, fonts, style archetype, audience, and tone. "On-brand" is judged against this file, not taste. If it doesn't exist, say the Consistency/Aesthetics scores are judged without brand context.
- Understand the project's purpose, audience, and the one action the design should drive.
- Never critique from source code alone. Look at the rendered result first (Step 0).

---

## Step 0: Capture the Artifact (Always First)

| Artifact | How to look at it |
|----------|-------------------|
| HTML file / local dev server / URL | Run the capture script below, then Read every PNG it writes |
| PNG/JPG/WebP (screenshot, generated image, poster) | Read the file. For small details, crop/zoom with Pillow (`Image.open(p).crop(box).resize(...)`) and Read the crop |
| Figma frame | Figma MCP `get_screenshot` (plus `get_variable_defs` for tokens) if connected; otherwise ask for an export |
| React/Vue component | Render it in the project's dev server or Storybook, then treat as a URL |

**Capture script** -- bundled at `<design-critique>/scripts/audit.mjs` (`<design-critique>` is this skill's directory). Needs Playwright with Chromium; `npm i -D axe-core` enables offline accessibility checks (otherwise it loads axe from a CDN):

```bash
node <design-critique>/scripts/audit.mjs <url-or-html-file> audit/            # 375, 768, 1440 px
node <design-critique>/scripts/audit.mjs http://localhost:3000 audit/ --widths 390,1280
```

It writes `{mobile,tablet,desktop}-fold.png` (first impression), `*-full.png`, `desktop-dark-fold.png`, and `report.json` (also printed), containing:

| Section | What it measures |
|---------|------------------|
| `widths.<name>` | Horizontal overflow, font sizes / families / text colors in use (consistency), off-4px-grid spacing, tap targets under 24px, text failing WCAG contrast against its nearest solid background, text sitting on images (check those by eye) |
| `darkMode` | Contrast failures with `prefers-color-scheme: dark` |
| `structure` | `lang`, viewport meta, h1 count, skipped heading levels, images without `alt`, unlabeled form controls, lazy-loaded images in the first viewport (LCP risk), animation with no `prefers-reduced-motion` rule |
| `axe` | axe-core violations: rule id, impact, count, first selector |

Treat the numbers as evidence, not verdicts: a contrast "failure" on a disabled control or decorative text may be fine; say so explicitly.

**Procedure** (same order every time, so critiques are comparable):
1. Look at `desktop-fold.png` for 5 seconds' worth: write down what you noticed first, second, third, and what the page is asking you to do. That is your hierarchy evidence.
2. Walk Steps 1-7 using the screenshots plus the JSON. Every finding must cite evidence: a screenshot region, a measured value, or an axe rule id.
3. Assign severity (Step 8), score (Step 10), and write the report.
4. After fixes are applied, re-run the capture and compare before/after screenshots (Step 9).

For static images (posters, ads, social graphics, generated images) there is no DOM: skip keyboard/performance checks, estimate contrast by sampling pixel colors with Pillow (`im.getpixel((x, y))`) and the WCAG formula, and also judge the image at its real display size (e.g. downscale a thumbnail to 320px wide and Read it). To fix a generated image, give concrete edit instructions for the `image-generation` skill rather than CSS.

---

## Step 1: Visual Hierarchy Assessment

Evaluate how effectively the design guides the user's eye.

### Checklist

- [ ] **Primary focal point**: Is there one clear element that draws attention first?
- [ ] **Secondary elements**: Can you identify a clear 2nd and 3rd level of importance?
- [ ] **Size contrast**: Is the most important element the largest? Is there enough size difference between levels?
- [ ] **Color contrast**: Does the primary CTA use the strongest color? Are secondary elements visually receded?
- [ ] **Weight contrast**: Do headings feel heavier than body text?
- [ ] **Whitespace**: Does the most important element have the most breathing room?
- [ ] **Reading flow**: Does the layout follow an F-pattern (content) or Z-pattern (landing page)?

### Common Fixes

```css
/* Problem: All elements same visual weight */
/* Fix: Create clear hierarchy with size and color */

/* Before: flat hierarchy */
.heading { font-size: 1.5rem; color: #333; }
.subheading { font-size: 1.25rem; color: #333; }
.body { font-size: 1rem; color: #333; }

/* After: clear hierarchy */
.heading { font-size: 2.5rem; font-weight: 800; color: var(--gray-900); letter-spacing: -0.02em; }
.subheading { font-size: 1.25rem; font-weight: 500; color: var(--gray-500); }
.body { font-size: 1rem; font-weight: 400; color: var(--gray-700); line-height: 1.65; }
```

---

## Step 2: Color Usage Evaluation

### Checklist

- [ ] **Palette cohesion**: Are all colors from the same family/system or do some feel random?
- [ ] **Meaningful color**: Does each color serve a purpose (brand, semantic, decorative)?
- [ ] **Color count**: Are there too many colors? (Aim for 1-2 brand + 4 semantic + neutrals.)
- [ ] **Contrast ratios**: Does all text meet WCAG AA (4.5:1 normal; 3:1 for ≥24px or ≥18.66px bold)? Use axe's `color-contrast` results; for text over images/gradients, measure the worst spot in the screenshot.
- [ ] **Consistent semantic colors**: Is red always error? Green always success?
- [ ] **Dark mode**: If present, are colors adapted (not just inverted)?
- [ ] **Color-only information**: Is any information conveyed by color alone? (It should not be.)

### Common Fixes

```css
/* Problem: Text fails contrast check */
/* Before: light gray on white */
.muted-text { color: #aaa; } /* ~2.3:1 on white -- FAILS AA */

/* Fix: darken until AA passes */
.muted-text { color: #737373; } /* 4.74:1 on white -- passes AA (design-context Neutral 500) */

/* Problem: Link indistinguishable from text */
/* Fix: underline + color */
a { color: var(--brand-500); text-decoration: underline; text-underline-offset: 2px; }
```

---

## Step 3: Typography Consistency Check

### Checklist

- [ ] **Font count**: Max 2 typefaces (3 with monospace). More feels chaotic.
- [ ] **Size scale**: Do sizes follow a consistent scale ratio or are they arbitrary?
- [ ] **Weight usage**: Are only 2-3 weights used? (400, 600, 700 is a good set.)
- [ ] **Line height**: Is body text 1.5-1.75? Are headings 1.1-1.3?
- [ ] **Line length**: Is body text constrained to 45-75 characters per line?
- [ ] **Consistency**: Same element types use same styles throughout?
- [ ] **Text wrap**: Are headings using `text-wrap: balance` (no single-word last lines)?
- [ ] **Scale evidence**: The capture JSON `fontSizes` should show roughly 5-8 distinct sizes; 12+ means no scale.
- [ ] **Responsive**: Does text scale appropriately on mobile?

### Common Fixes

```css
/* Problem: Line length too long */
/* Before: text spans full 1400px container */
.content { max-width: 1400px; }

/* Fix: constrain prose */
.content { max-width: 1400px; }
.content .prose { max-width: 65ch; }

/* Problem: Arbitrary font sizes -- Fix: adopt the typography skill's modular scale */
:root {
  --type-ratio: 1.25; /* design-context Scale Ratio */
  --text-base: 1rem;
  --text-lg: calc(var(--text-base) * var(--type-ratio));
  --text-xl: calc(var(--text-lg) * var(--type-ratio)); /* ...see typography Step 1 */
}
```

---

## Step 4: Spacing and Alignment Audit

### Checklist

- [ ] **Consistent spacing**: Are gaps between similar elements the same?
- [ ] **Spacing scale**: Do spacings use a base unit (4px or 8px multiples)?
- [ ] **Alignment**: Are elements aligned to a grid? Left edges lining up?
- [ ] **Proximity**: Are related items closer together than unrelated items?
- [ ] **Padding balance**: Is internal padding consistent within components?
- [ ] **Vertical rhythm**: Is there a consistent rhythm to the vertical spacing?
- [ ] **Edge consistency**: Are page margins consistent across sections?

### Common Fixes

```css
/* Problem: Inconsistent spacing */
/* Before: random pixel values */
.card { padding: 17px; margin-bottom: 23px; }
.section { padding: 45px 30px; }

/* Fix: use a 4px/8px scale */
.card { padding: var(--space-5); margin-bottom: var(--space-6); }
.section { padding: var(--space-12) var(--space-8); }

/* Problem: Misaligned elements */
/* Fix: use consistent padding and max-width */
.container {
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: var(--space-6);
}
```

---

## Step 5: Accessibility Review

### Contrast

- [ ] Normal text: 4.5:1 minimum contrast ratio.
- [ ] Large text (≥24px, or ≥18.66px bold): 3:1 minimum.
- [ ] UI components (borders, icons): 3:1 against adjacent colors.
- [ ] Focus indicators: 3:1 against adjacent background.

### Keyboard Navigation

- [ ] All interactive elements are focusable.
- [ ] Focus order follows visual order.
- [ ] Focus indicator is visible and has sufficient contrast.
- [ ] No keyboard traps (user can always tab away).
- [ ] Skip-to-content link exists.

### Screen Reader

- [ ] Images have meaningful alt text (or `alt=""` if decorative).
- [ ] Form inputs have associated labels.
- [ ] Icon-only buttons have `aria-label`.
- [ ] Headings form a logical outline (no skipped levels).
- [ ] Dynamic content changes are announced (aria-live regions).

### Common Fixes

```css
/* Problem: Custom focus style removed */
/* Before */
*:focus { outline: none; } /* NEVER DO THIS */

/* Fix: custom but visible focus */
*:focus-visible {
  outline: 2px solid var(--brand-500);
  outline-offset: 2px;
}

/* Problem: No skip link */
/* Fix: */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 0.5rem 1rem;
  background: var(--brand-500);
  color: white;
  z-index: 9999;
}

.skip-link:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

---

## Step 6: Responsive Behavior Check

### Checklist

- [ ] **Mobile layout**: Does the layout stack sensibly on small screens?
- [ ] **Touch targets**: At least 24x24px (WCAG 2.2 AA, SC 2.5.8; see `smallTargets` in the JSON); 44x44px recommended on mobile.
- [ ] **Text readability**: Is body text at least 16px on mobile (no zoom needed)?
- [ ] **Horizontal scroll**: Is there any horizontal overflow?
- [ ] **Images**: Do images resize appropriately (max-width: 100%)?
- [ ] **Navigation**: Is mobile navigation accessible and usable?
- [ ] **Breakpoints**: Do layouts transition smoothly between breakpoints?

### Common Fixes

```css
/* Problem: Fixed widths cause overflow */
/* Before */
.card { width: 400px; }

/* Fix: flexible with max */
.card { width: 100%; max-width: 400px; }

/* Problem: Small touch targets */
/* Before */
.icon-button { width: 24px; height: 24px; }

/* Fix: larger hit area, same visual icon (works with box-sizing: border-box) */
.icon-button {
  min-width: 44px;
  min-height: 44px;
  display: inline-grid;
  place-items: center;
}

/* Problem: Images overflow container */
img {
  max-width: 100%;
  height: auto;
}
```

---

## Step 7: Performance Impact Assessment

### Checklist

- [ ] **Font loading**: Using `font-display: swap`? Preloading critical fonts?
- [ ] **Image formats**: Using AVIF/WebP with fallbacks, and `srcset` + `sizes` so phones don't download desktop images?
- [ ] **Image sizing**: Are images sized appropriately (not 4000px for a 400px display)?
- [ ] **Animation performance**: Animations using only `transform` and `opacity`?
- [ ] **CSS efficiency**: Any redundant or overriding styles?
- [ ] **Layout shifts**: Are dimensions reserved for images/embeds (aspect-ratio, width/height)?
- [ ] **Excessive shadows/blurs**: Are there complex box-shadows on frequently painted elements?

### Common Fixes

```css
/* Problem: Animation causes layout recalculation */
/* Before */
.card:hover { margin-top: -5px; }  /* triggers layout */

/* Fix: use transform */
.card:hover { transform: translateY(-5px); }  /* GPU composited */

/* Problem: Layout shift from images */
/* Fix: put the intrinsic size in HTML (<img width="1600" height="900">), then: */
img { max-width: 100%; height: auto; }
```

---

## Step 8: Severity and Recommendation Format

### Severity Levels (assign exactly one per issue)

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Blocks a user from completing the core task, or fails WCAG A/AA on core content | Body text 2.3:1, CTA invisible on mobile, keyboard trap, horizontal scroll on mobile, missing labels on form fields |
| **High** | Core task works but is noticeably harder, or the design undermines its main goal | No clear primary CTA, competing focal points, off-brand colors/fonts, tap targets < 24px |
| **Medium** | Visible polish/consistency problem most users feel but can work around | 10+ font sizes, off-grid spacing, inconsistent radii, weak secondary hierarchy |
| **Low** | Refinement a designer would notice | Heading widows, slightly loose letter-spacing, minor alignment drift |

Order the fix list by severity, then by impact ÷ effort within a severity.

### Recommendation Format

```
### [Severity] Issue: [What's wrong]
**Category**: Hierarchy | Color | Typography | Spacing | Accessibility | Responsive | Performance
**Evidence**: [screenshot + region, measured value, or axe rule id]
**Problem**: [1-2 sentences: what's wrong and why it matters]
**Fix**: [Specific CSS/HTML using the project's tokens]
**Impact**: [What improves]
```

### Example

```
### [High] Issue: Hero headline, subtitle, and CTA compete for attention
**Category**: Hierarchy
**Evidence**: desktop-fold.png -- headline 28px/600, subtitle 24px/600, CTA is a gray outline button
**Problem**: Nothing reads first, and the only action looks secondary.
**Fix**: .hero-headline { font-size: clamp(2.5rem, 5vw + 1rem, 5rem); font-weight: 800; }
         .hero-subtitle { font-size: var(--text-xl); color: var(--text-secondary); max-width: 50ch; }
         .hero-cta { background: var(--interactive-primary); color: white; }
**Impact**: Headline -> value prop -> CTA reads in order within 3 seconds.
```

---

## Step 9: Before/After Verification

A critique is not done until the fixes are checked on the rendered page.

1. For each fix, show the current CSS (before) and the improved CSS (after), and say what changed and why. Use existing tokens (`--space-*`, `--text-*`, `--bg-*`, `--text-primary`, `--interactive-primary`, `--radius-*`, `--shadow-*`); never introduce new hard-coded values.
2. If you applied the fixes, re-run the capture script into a new folder and Read the before and after screenshots of the same viewport side by side.
3. Confirm every Critical/High issue is resolved (axe violations gone, overflow false, targets ≥ 24px) and nothing regressed at the other widths or in dark mode. Re-score only after this check.

---

## Step 10: Scoring Framework

Rate the design across these dimensions (1-10 scale):

### Categories

| Category       | Weight | What to evaluate (checklist steps)                 |
|----------------|--------|---------------------------------------------------|
| **Hierarchy**  | 25%    | Clear focal points, scannable, directed flow (Step 1, 5-second test) |
| **Consistency**| 25%    | Spacing scale, color system, type system, brand match (Steps 2-4, capture JSON) |
| **Aesthetics** | 25%    | Color harmony, whitespace, polish, fit to style archetype |
| **Usability**  | 25%    | Accessibility, responsiveness, clarity, performance (Steps 5-7, axe) |

Overall = weighted average, rounded to one decimal. **Caps** keep scores honest: any open Critical issue caps its category at 4 and the overall at 6; any open High issue caps its category at 7. Aesthetics must cite at least one concrete observation, not just "looks modern."

### Scoring Rubric

| Score | Meaning                                               |
|-------|-------------------------------------------------------|
| 1-2   | Fundamentally broken. Major rework needed.            |
| 3-4   | Significant issues. Multiple areas need attention.    |
| 5-6   | Functional but unpolished. Clear improvement areas.   |
| 7-8   | Good. Minor refinements would elevate it.             |
| 9-10  | Excellent. Professional quality, well-executed.       |

### Report Template

```
## Design Critique Report

### Overall Score: X/10

| Category    | Score | Notes                                |
|-------------|-------|--------------------------------------|
| Hierarchy   | X/10  | [brief note]                         |
| Consistency | X/10  | [brief note]                         |
| Aesthetics  | X/10  | [brief note]                         |
| Usability   | X/10  | [brief note]                         |

### Top 3 Strengths
1. [What's working well]
2. [What's working well]
3. [What's working well]

### Issues by Severity
| # | Severity | Category | Issue | Evidence |
|---|----------|----------|-------|----------|
| 1 | Critical | ...      | ...   | ...      |

### Fixes (in priority order, with code -- Step 8 format)

### Quick Wins (< 5 min each)
- [Small change, big impact]
- [Small change, big impact]
```

---

## Critique Process Summary

0. **Capture** the artifact (Step 0) and look at the screenshots before reading code.
1. **Read design context** and understand goals.
2. **Assess visual hierarchy**: Is there a clear 1-2-3 priority?
3. **Evaluate colors**: Cohesive? Accessible? Purposeful?
4. **Check typography**: Consistent scale? Good line length? Readable?
5. **Audit spacing**: Using a system? Aligned? Consistent?
6. **Review accessibility**: Contrast, focus, labels, keyboard?
7. **Test responsive**: Mobile stacking, touch targets, overflow?
8. **Check performance**: Animations efficient? Images sized? Fonts loaded?
9. **Provide specific fixes**: Always include code, never just describe.
10. **Score and prioritize**: Assign severity, apply caps, rank fixes.
11. **Re-verify**: Re-capture after fixes and confirm Critical/High issues are gone (Step 9).
