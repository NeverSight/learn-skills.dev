---
name: typo3-wcag22-aa-agentic
description: Use this skill to audit, fix, and document accessibility for TYPO3 websites and Fluid sitepackages. It orchestrates Playwright, axe-core, optional Deque axe MCP, TYPO3 template mapping, manual/HITL checks, CI baselines, and DACH/EAA-aware accessibility statement drafts for WCAG 2.2 AA targets.
license: MIT
compatibility: >-
  Requires Node.js 20+, npm, Playwright browsers. Optional: Docker or npm axe
  MCP Server plus AXE_API_KEY or AXE_ACCESS_TOKEN. Designed for TYPO3 local
  DDEV/staging URLs and CI.
metadata:
  author: webconsulting accessibility workflow
  version: "1.0.0"
---

# TYPO3 WCAG 2.2 AA Agentic Accessibility Skill

## Purpose

Use this skill when the user wants to check, fix, monitor, or document accessibility for a TYPO3 website, TYPO3 sitepackage, Fluid templates, CSS/SCSS, JavaScript UI components, editor-created content, or an Erklärung zur Barrierefreiheit / accessibility statement for Austria, Germany, Switzerland, or a voluntary WCAG target.

Primary goal: move a TYPO3 site toward WCAG 2.2 AA and EN 301 549 readiness with minimal but mandatory human review.

Legal examples now cover Austria, Germany, and Switzerland. The skill can generate statement drafts and audit notes for different legal profiles, but it must not give final legal advice.

Important boundary: never claim complete WCAG conformance from automated scans alone. Automated scans are evidence. Final conformance wording and legal publication require a small human review, especially for alt text, keyboard logic, screen-reader clarity, PDFs, videos, maps, and legal exceptions.

## Tool model

Prefer this order:

1. Local filesystem/search tools for repository understanding.
2. Playwright plus axe-core for reproducible browser-based scans.
3. Template/static checks for TYPO3 Fluid, SCSS, JavaScript, RTE and TCA patterns.
4. Optional Deque axe MCP tools, if available:
   - `analyze`: scan the rendered page state.
   - `remediate`: request code-level fix guidance.
   - `igt`: use only when the user has a Deque subscription/credits and interactive guided testing is explicitly useful.
5. Code edits in the TYPO3 sitepackage.
6. Re-test the exact URL/state that failed.
7. Generate `report.md`, `report.json`, `open-issues.yml`, and a draft `accessibility-statement-draft.de.md`.

When the local Codex app is used, start with `prompts/local-codex-app-prompt.md` and fill in project URL, profile, and sitepackage path.

## Manual review Chrome helper

This skill includes a no-build Chrome extension for manual WCAG review:

```text
project-template/manual-review/chrome-extension/
```

Use it when a criterion cannot be safely decided by automation alone. The helper loads the full active WCAG 2.2 Level A + Level AA checkpoint list from:

```text
project-template/.a11y/checkpoints/wcag22-aa-checkpoints.yml
project-template/manual-review/chrome-extension/data/wcag22-aa-checkpoints.json
```

WCAG 2.2 AA means all active Level A and Level AA success criteria. In this list that is 55 active checkpoints: 31 Level A and 24 Level AA. WCAG 2.2 removed 4.1.1 Parsing; keep it only as a legacy check when a contract or policy still references WCAG 2.0 or 2.1.

Manual helper capabilities:

- side-panel checklist for every active WCAG 2.2 A/AA criterion;
- page helper scan for headings, landmarks, images, forms, links, focusable elements, small targets, duplicate IDs, iframes and videos;
- visual highlights for headings, landmarks, images, forms, links, focusable elements and small targets;
- keyboard focus recorder for focus order, visible focus and focus-obscured checks;
- structured export as manual review JSON;
- structured export as an `open-issues.yml` fragment;
- local Codex prompt for remediation from the exported evidence.

Load it in Chrome via `chrome://extensions` → Developer mode → Load unpacked → select `manual-review/chrome-extension`.

After export, merge manual findings into the project source of truth:

```bash
npm run a11y:manual:merge
# or for one file:
npm run a11y:manual:merge:file -- .a11y/manual-review/2026-07-05-page-open-issues.yml
```

Important: the Erklärung zur Barrierefreiheit must be generated from `.a11y/open-issues.yml` and documented exceptions. Do not free-write it from memory or from a chat summary.

When Deque axe MCP is available, use it as acceleration, not as the single source of truth. The local Playwright/axe suite remains the repeatable project baseline.

## Project bootstrap

If the project has no accessibility setup, scaffold from the bundled `project-template` folder:

```bash
./Skills.sh scaffold --project /path/to/typo3-project
cd /path/to/typo3-project
cp .a11y/a11y.config.example.yml .a11y/a11y.config.yml
npm install
npx playwright install --with-deps chromium
npm run a11y:all
```

For DDEV, use the local HTTPS/HTTP URL from `ddev describe`, for example:

```yaml
site:
  baseUrl: "https://my-project.ddev.site"
  sitemapUrl: "https://my-project.ddev.site/sitemap.xml"
```


## Legal framework profiles

Use `legal.profile` in `.a11y/a11y.config.yml` to choose the statement context. Keep the technical test target as WCAG 2.2 AA unless the client explicitly asks for a lower legal baseline; a stricter internal target is acceptable, but the statement must accurately name the applicable legal reference.

Supported example profiles:

```yaml
legal:
  # Austria
  # profile: "at-public-wzg"        # public-sector WZG / EN 301 549 context
  # profile: "at-private-bafg"      # Austrian BaFG / EAA context, if the service is in scope

  # Germany
  # profile: "de-public-bgg-bitv"   # German public-sector BGG + BITV 2.0 context
  # profile: "de-private-bfsg"      # German BFSG / EAA context, if the product/service is in scope

  # Switzerland
  # profile: "ch-public-behig-ech0059" # Swiss federal/public-sector BehiG/BehiV + eCH-0059 context

  # Voluntary / contractual
  # profile: "voluntary-wcag22aa"   # internal or contractual WCAG 2.2 AA target
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
```

Important jurisdiction rules:

- Austria public sector: use WZG or relevant state/municipal rules and the österreichische Erklärung-zur-Barrierefreiheit structure.
- Austria private sector: use BaFG/EAA only when the offered product/service is in scope; otherwise keep it as voluntary WCAG evidence.
- Germany public sector: use BGG + BITV 2.0 on federal projects; for state/municipal projects verify the applicable Landesrecht and monitoring/enforcement body.
- Germany private sector: use BFSG/EAA only for covered products/services; do not automatically classify every brochure website as BFSG-relevant.
- Switzerland: eCH-0059 v3 is currently WCAG 2.1 AA based; the skill may still test WCAG 2.2 AA as an internal higher target, but the statement should not misrepresent the legal baseline.

Load the matching reference file when legal wording matters:

```text
project-template/references/legal-at-notes.md
project-template/references/legal-de-notes.md
project-template/references/legal-ch-notes.md
project-template/references/legal-framework-examples.md
```

## Standard workflow

### 1. Understand scope

Collect:

- base URL, preferably local DDEV or staging;
- TYPO3 version if known;
- sitepackage path(s);
- language variants;
- login/cookie-banner steps;
- optional required legal framework/profile:
  - Austrian public-sector WZG;
  - Austrian BaFG / European Accessibility Act;
  - German public-sector BGG + BITV 2.0;
  - German BFSG / European Accessibility Act;
  - Swiss public-sector BehiG/BehiV + eCH-0059;
  - internal WCAG 2.2 AA target;
- representative page types:
  - homepage;
  - standard content page;
  - list page/news list;
  - detail page/news detail;
  - search page;
  - contact/form page;
  - login/account page;
  - pages with accordions, tabs, modals, sliders, maps, videos, PDFs/downloads;
  - mobile navigation.

If the user gives only a URL, create a best-effort inventory from sitemap and common TYPO3 paths.

### 2. Prepare TYPO3 mapping

In dev/staging only, prefer component markers around sitepackage output so findings map back to Fluid templates:

```html
<nav
  aria-label="Hauptnavigation"
  data-a11y-component="navigation.main"
  data-a11y-template="EXT:sitepackage/Resources/Private/Partials/Navigation/Main.html"
>
```

Never leak internal template paths on production unless the project intentionally allows it.

### 3. Run automated checks

Run:

```bash
npm run a11y:discover
npm run a11y:test:report-only
npm run a11y:report
npm run a11y:statement
```

Use `a11y:test` instead of `a11y:test:report-only` when the team wants CI to fail on new critical/serious findings.

Axe tags should normally include:

```text
wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa
```

Optionally include `best-practice` as advisory, not as a WCAG gate.

### 4. Fix loop

For every finding:

1. Identify URL and state.
2. Identify selector and HTML snippet.
3. Map to closest `data-a11y-component` / `data-a11y-template` marker.
4. Search relevant Fluid/SCSS/JS/TCA/RTE files.
5. Prefer native HTML over ARIA.
6. Patch the source, not only the rendered HTML.
7. Re-run the failing URL/state.
8. Update open issue status.

Do not suppress a rule unless there is a documented reason, owner, expiry date, and link to a ticket.

### 5. Manual/HITL gate

Use the Chrome helper and the base checkpoint list for page samples and human-only criteria. Export findings and merge them into `.a11y/open-issues.yml` before generating the statement.

Keep human review small, but mandatory for:

- meaningful image alternative text;
- keyboard interaction and logical tab/focus order;
- Screenreader smoke test with VoiceOver/NVDA;
- PDF, video, map, social embed and third-party content exceptions;
- legal status wording: fully/partially/not compliant;
- publication of the Erklärung zur Barrierefreiheit.

Required manual evidence files:

```text
.a11y/checkpoints/wcag22-aa-checkpoints.yml
.a11y/manual-review/*.json
.a11y/manual-review/*-open-issues.yml
.a11y/open-issues.yml
```

Structured statuses:

```text
not_tested, pass, fail, not_applicable, cannot_determine, needs_expert_review
```

Statement categories:

```text
non_conformance, disproportionate_burden, outside_scope, third_party_content,
archived_content, accessible_alternative_available, legacy_non_conformance
```

## TYPO3 fix rules

### Global layout

- Exactly one visible H1 per page unless an intentional page pattern is documented.
- Correct `<html lang="de-AT">` or language variant.
- Skip link to `#main-content`.
- Real landmarks: `header`, `nav`, `main`, `footer`.
- No positive `tabindex`.
- No removed focus outline unless replaced by a clearly visible focus indicator.
- No horizontal scroll at 320 CSS pixels unless content truly requires two-dimensional scrolling.

### Navigation

- Use real links for navigation and real buttons for toggles.
- Main navigation has `aria-label="Hauptnavigation"`.
- Current page uses `aria-current="page"`.
- Mobile menu button has `aria-expanded`, `aria-controls`, and visible accessible name.
- Escape closes overlays; focus returns to the opener.

### Accordions, tabs, modals

- Accordion headers are `<button>` elements.
- Toggle state is exposed with `aria-expanded` and `aria-controls`.
- Tabs follow the ARIA tabs pattern only when it is really a tab interface.
- Modals use focus management, Escape close, focus return, and no background tab trap.

### Forms

- Every field has a programmatic label.
- Error text is linked via `aria-describedby`.
- Invalid fields use `aria-invalid="true"` when invalid.
- Error summary links to fields.
- Use `autocomplete` for personal data when applicable.
- Do not rely on placeholder-only labels.

### Images and media

- Decorative images: `alt=""`.
- Informative images: meaningful `alt`, not filename or generic words.
- Linked images: alt describes link purpose.
- Videos need captions/transcripts where in scope.
- PDFs must be tracked separately as accessible, remediated, or exception/alternative.

### Links and buttons

- Avoid “hier klicken” / “mehr” without context.
- Icon-only controls need accessible names.
- External/download links should make purpose clear.
- Buttons perform actions; links navigate.

### CSS/SCSS

- Focus styles are tokenized and visible.
- Color contrast is checked in rendered states, not only tokens.
- Respect `prefers-reduced-motion`.
- Avoid content conveyed by color alone.
- Ensure target size for interactive controls, especially mobile.

### JavaScript

- No mouse-only interactions.
- Use `aria-live` for dynamic status messages when relevant.
- Do not rewrite native form/link/button behavior without reimplementing keyboard and accessibility semantics.

## Output contract

Expected generated files:

```text
.a11y/url-inventory.json
.a11y/raw/*.json
.a11y/report.json
.a11y/report.md
.a11y/open-issues.yml
.a11y/template-lint.json
.a11y/template-lint.md
.a11y/accessibility-statement-draft.de.md
```

Reports must distinguish:

- automated axe violations;
- custom warnings;
- TYPO3 template/static findings;
- known accepted issues;
- manual review items;
- legal statement content and jurisdiction/profile assumptions.

## CI rollout

Recommended phases:

1. Report only.
2. Fail only on new critical/serious findings in core templates.
3. Fail on critical/serious findings on representative pages.
4. Expand to all sitemap pages.
5. Review statement at least annually or after major redesign/content/system changes.

## Safety and privacy

- Do not put API keys in repository files.
- Use environment variables for `AXE_API_KEY` or `AXE_ACCESS_TOKEN`.
- Prefer staging/local URLs for login-protected content.
- Redact personal data in screenshots/reports where necessary.
- Review AI-generated code patches before commit.
- Do not commit `.a11y/raw` artifacts containing sensitive HTML unless the team intentionally accepts that risk.

## Credits & Attribution

This skill is original webconsulting work.

Original repository: https://github.com/dirnbauer/webconsulting-skills
