---
name: ux-accessibility-audit
description: Run a structured WCAG 2.1 AA accessibility audit on a design, screen, component, or page. Produces a prioritized issue list — each finding cites the violated WCAG criterion, a severity rating (Critical/Major/Minor), and a concrete fix. Use when auditing for a11y compliance or as a validation step after generating UI.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Accessibility Audit Skill


## How this skill behaves (read first)

This is an **evaluative** skill — it reviews existing work against a standard (WCAG), it doesn't generate UI. Flagging is safe, so it **auto-runs** and is designed to be **called as a validation step** by generative skills as well as invoked directly.

It **owns the accessibility concern** in this repo. Generative skills hand off to it (e.g. `ux-login-signup`, `ux-pricing`), and the **heuristics audit** (`ux-heuristics-audit`) deliberately defers contrast / keyboard / screen-reader specifics here rather than duplicating them. When invoked, do the full a11y pass; don't assume another skill covered it.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier B — offered (and narrowed to usage when a design system is in play)**. Explicit scope always wins.

---

## What this skill changes vs. default behavior

By default, accessibility feedback tends to be partial and vague — a few obvious call-outs ("add alt text", "check contrast") with no standard, no severity, and no systematic sweep. This skill forces four things:

1. **Every finding cites the WCAG criterion and level** it violates — not a vague suggestion.
2. **Every finding gets a severity** based on how completely it blocks access — so the list is prioritized.
3. **Every finding has a concrete fix** — the specific markup/design change.
4. **The audit is systematic** — it sweeps all six categories below, so issues outside the obvious ones (focus order, heading hierarchy, table semantics, motion) actually get caught.

---

## WCAG foundations

**POUR principles** — every audit item maps to one of these four:

- **Perceivable** — content must be detectable via at least one sense (sight, hearing, etc.)
- **Operable** — all interactions must work without a mouse (keyboard, switch, voice)
- **Understandable** — content and UI must be clear and predictable
- **Robust** — content must work across browsers, devices, and assistive technologies

**Compliance levels:**

- **Level A** — bare minimum; missing these creates complete barriers (e.g. no alt text, no keyboard access).
- **Level AA** — the legal standard most organizations must meet; the **default target for every audit**.
- **Level AAA** — aspirational; apply selectively where it adds high value.

Default audit target: **WCAG 2.1 Level AA**.

---

## Audit checklist

Work through every category — a partial sweep is the main way real issues get missed. Flag each violation with **WCAG criterion**, **severity** (see model below), and a **fix**.

### 1. Color & Contrast

| Check | Requirement | Notes |
|---|---|---|
| Normal text vs background | ≥ 4.5:1 (AA) / 7:1 (AAA) | Applies to all text in UI: buttons, labels, cards, nav |
| Large text (≥ 18pt or ≥ 14pt bold) | ≥ 3:1 | |
| Icons (informational or interactive) | ≥ 3:1 | Decorative icons exempt |
| Input borders vs surrounding background | ≥ 3:1 | Including focus indicators |
| Text over images | ≥ 4.5:1 between text and the portion of image behind it | Use semi-transparent overlay if needed |
| Selection states | Same ratios as regular text | |
| Disabled elements | Exempt from contrast rules | Must still be recognizable as inactive |
| Logo text | Exempt | But good practice to maintain contrast anyway |
| Color as sole differentiator | ❌ Never | Always pair color with icon, pattern, label, or text |
| Stark contrast (pure black on white) | Discouraged | Use #333 on #F8F8F8 — exceeds AA while reducing eye strain |

**Don't rely on color alone**: error states need an icon + text, not just red. Charts need patterns or labels, not just color.

---

### 2. Typography & Text

| Check | Requirement |
|---|---|
| Base body font size | ≥ 16px |
| Line length | 45–75 characters (including spaces) |
| Text alignment | Follows reading direction (LTR → left-align; RTL → right-align) |
| Headings visually distinct | Larger size, bold weight, or color difference from body text |
| One `<h1>` per page | Page title only |
| Heading hierarchy | No skipped levels (h1 → h2 → h3, never h1 → h3) |
| Semantic heading tags | Use `<h1>`–`<h6>`, not styled `<div>` or `<p>` |
| Language | Plain language, secondary-education reading level |
| Idioms & figures of speech | Avoid — confuse screen readers and non-native speakers |
| Typeface | Clear letterform distinctions (0 vs O, 1 vs l vs I); large x-height |

---

### 3. Forms

| Check | Requirement |
|---|---|
| Keyboard access | Every field, dropdown, checkbox, radio, button navigable via Tab / Shift+Tab / Enter / arrows |
| Focus indicators | Visible on every focused element — never remove browser default without replacing |
| Layout | Single-column preferred; multi-column increases cognitive load and screen-reader confusion |
| Input boundaries | Visible borders or backgrounds — never borderless inputs |
| Labels | Outside the field, not placeholder-only; min 16px; 4.5:1 contrast |
| Placeholder text | Supplemental only — disappears on input, so never the sole label |
| Autocomplete | Implement for name, email, phone, address, payment (HTML `autocomplete` attribute) |
| Error states | Multiple cues: icon + bold border + field-specific message. Never color alone |
| Error placement | Adjacent to the offending field + `aria-describedby` linking field to error |
| Error summary | At top of form on submit failure, with anchor links to each problem field |
| Authentication | No text-based CAPTCHA — use magic links, OTP, passkeys, or biometrics. Support paste in password fields |
| Mobile one-handed use | Center CTAs in lower-middle zone; avoid right-edge-only button placement |

---

### 4. Links & Navigation

| Check | Requirement |
|---|---|
| Link labels | Descriptive, specific — "Download pricing guide" not "Click here" or "Read more" |
| New-window links | Warn users in link text or aria-label: "opens in new tab" |
| File links | State type + size: "Annual Report (PDF, 2.5 MB)" |
| Raw URLs as link text | ❌ Never — screen readers read character by character |
| Link recognizability | Underline + color (not color alone) |
| Focus state | Visible, distinctive focus ring on every link and interactive element |
| `href` attribute | Required on all `<a>` tags — `<div>` with click handler is not a link |
| Voice/tone | Link text should match the product's voice, but always prioritize clarity |
| Help links | Consistently placed (footer, header utility nav, or persistent help icon) |

---

### 5. Images & Multimedia

| Check | Requirement |
|---|---|
| Informational images | `alt` attribute with meaningful description |
| Decorative images | `alt=""` (null) — tells screen readers to skip |
| Images containing text | Alt text = the exact text in the image |
| Autoplay | ❌ Disabled by default — user must initiate playback |
| Media controls | Play/pause/stop/rewind/volume/mute/captions — keyboard accessible, sufficient size and contrast |
| Video captions | Required for all pre-recorded video with audio |
| Audio transcripts | Required for all audio-only content |
| Flashing/strobing content | ❌ No content flashing > 3 Hz or red flashing at any rate |
| Animations (GIF, SVG, CSS) | No more than 5 light-dark stripe pairs; provide a way to pause/stop |
| Icons | Pair with text labels; informational icons need `aria-label` or title |
| Swipe gestures | Support both directions or provide an alternate tap target |

---

### 6. Tables & Lists

| Check | Requirement |
|---|---|
| Data tables | Use `<table>` element — never use tables for layout |
| Table caption | `<caption>` immediately after `<table>` opening tag |
| Header cells | `<th>` with `scope="col"` or `scope="row"` — never empty |
| Complex tables | Avoid merged cells and multi-level headers; split into simpler tables if needed |
| Cell widths | Use `%` not `px` — allows browser reflow; never set cell height manually |
| Lists | Use `<ul>`, `<ol>`, or `<dl>` appropriately — not styled `<div>` rows |
| Unordered lists | For items where order doesn't matter |
| Ordered lists | For sequential steps, rankings, instructions |
| Description lists | `<dl>` / `<dt>` / `<dd>` for glossaries, FAQs, key-value metadata |

---

## Severity rating

Rate each finding by **how completely it blocks access** and **which WCAG level it fails**:

| Severity | Meaning |
|---|---|
| **Critical** | Blocks access entirely for some users. Usually a **Level A** failure — no keyboard access, no alt text on informational images, missing captions, a keyboard trap. Fix before ship. |
| **Major** | Significant friction; users can sometimes work around it but shouldn't have to. Usually a **Level AA** failure — contrast below 4.5:1, placeholder-as-label, color-only error states, missing focus indicators. |
| **Minor** | Noticeable but low-impact, or a best-practice / **AAA** improvement — slightly short line length, stark pure-black text, a non-ideal but functional label. |

When in doubt, rate by the user impact (does it *block* a task or merely add friction?), not by how easy the fix is.

---

## Audit output format

```
## Accessibility Audit — [Component / Screen Name]
Context: [platform · WCAG target (default AA) · design or code]

### Critical (blocks access entirely)
- [Issue]: [what's wrong] → [fix] — WCAG [X.X.X]

### Major (significant friction)
- [Issue]: [what's wrong] → [fix] — WCAG [X.X.X]

### Minor (best practice / AAA)
- [Issue]: [what's wrong] → [fix] — WCAG [X.X.X]

### Passed ✓
- [what's already working]
```

Always end with a one-line summary stating the overall **WCAG AA compliance status** and the top fixes that would get it there.

---

## How to run a good audit

1. **Establish context.** Platform (web/mobile/native), target level (AA by default — only go AAA if asked), and whether you're auditing a design or live code (some checks, like keyboard order and `aria-*`, only apply to code).
2. **Sweep all six categories.** The value of this skill over a default review is completeness — don't stop at contrast and alt text.
3. **Rate by barrier, not by effort.** A one-line `alt` fix can still be Critical.
4. **Be specific in fixes.** Give the exact change (markup, attribute, ratio, or design adjustment), not "make it accessible."
5. **Note tooling limits.** Automated scanners catch only ~30–40% of issues — manual review of focus order, alt-text quality, and reading order still matters.

---

## Recommended tools

For automated scanning (catches ~30–40% of issues):

- **WAVE** (browser extension) — overlays visual indicators, references violated WCAG criteria
- **axe DevTools** (Chrome extension) — accurate, dev-friendly; powered by axe-core
- **Google Lighthouse** (Chrome DevTools → Lighthouse tab) — accessibility + SEO + performance in one pass

For contrast checking in design:

- **Able** (Figma plugin) — contrast checker + color-blindness simulator
- **Stark** (Figma / Sketch / Adobe XD) — contrast, vision simulator, focus order, alt-text annotations
- **WCAG Color Contrast Checker** (Chrome extension) — real-time ratio checking in browser

For screen-reader testing:

- **VoiceOver** (macOS/iOS, built-in) — navigate with `VO + arrow keys`
- **NV Access / NVDA** (Windows, free) — most widely used Windows screen reader

For seizure risk:

- **PEAT** (downloadable) — analyzes video/animation for photosensitive epilepsy triggers
- **Harding Test** — online paid service for broadcast/video content

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Use red text alone for errors | Red border + warning icon + descriptive message |
| `<a>Click here</a>` | `<a>Download the onboarding guide (PDF, 1.2 MB)</a>` |
| `<img src="chart.png">` (no alt) | `<img src="chart.png" alt="Bar chart showing Q3 revenue by region">` |
| Decorative image with alt text | `<img src="bg-swoosh.svg" alt="">` |
| Pure black `#000` on pure white `#FFF` | Dark grey `#333` on off-white `#F8F8F8` |
| Placeholder as the only label | Persistent label above the field + optional placeholder |
| Jump from `<h1>` to `<h3>` | Always use `<h1>` → `<h2>` → `<h3>` in order |
| Table for page layout | CSS Grid or Flexbox for layout; `<table>` for data only |
| Autoplay video | Controls visible at top; user initiates playback |
| Color-only chart legend | Add patterns, shapes, or data labels alongside color |
| Report only the obvious issues | Sweep all six categories; rate by barrier; cite the criterion |

---

## Source lessons (Uxcel)

- [Intro to Accessibility](https://uxcel.com/lessons/intro-to-accessibility-816)
- [Accessibility Tools](https://uxcel.com/lessons/accessibility-tools-156)
- [Color Accessibility](https://uxcel.com/lessons/accessible-colors-417)
- [Text Accessibility](https://uxcel.com/lessons/accessible-text-698)
- [Forms Accessibility](https://uxcel.com/lessons/accessible-forms-582)
- [Links Accessibility](https://uxcel.com/lessons/accessible-links-903)
- [Multimedia Accessibility](https://uxcel.com/lessons/accessible-multimedia-295)
- [Tables & Lists Accessibility](https://uxcel.com/lessons/accessible-tables-712)
