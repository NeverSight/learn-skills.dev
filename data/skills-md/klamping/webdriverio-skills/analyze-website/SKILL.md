---
name: analyze-website
description: Use when investigating and documenting website structure, components, functionality importance, and version-to-version differences for human understanding and test planning.
---

# Analyze Website

Investigate and document site structure and functionality for humans and agents.

This skill produces reusable analysis artifacts that support test planning, coverage decisions, and change impact reviews.

## Performance Goals

- Minimize repeated deep scans when analysis already exists.
- Use the lightest evidence path first (HTML/routes/labels), then deepen only as needed.
- Reuse cached analysis for unchanged targets.

## When to Use

- You need a structured map of a website before writing or triaging tests.
- You need component inventory and functionality importance levels.
- You need to compare two site versions (or two snapshots) for differences.

## When Not to Use

- You only need to implement a specific test immediately.
- You only need to run a known test file.
- You have no page evidence (URL, HTML, screenshot, or metadata).

## Inputs

Preferred inputs (use what is available):

- URL(s) to analyze
- screenshot(s)
- HTML source and metadata
- optional baseline + current versions for comparison
- optional product context (critical flows, business priorities)

For authenticated areas, accept one of these:

- test credentials (username/password)
- HTML snapshots for authenticated pages
- permission to run temporary WDIO login navigation using existing page objects

Never persist credentials in output artifacts.

## Fast-Path Workflow

Use this sequence to improve speed and reduce token usage:

1. Check for existing analysis in `references/website-analysis/<target>/`.
2. If recent and target unchanged, reuse and update only affected sections.
3. Fetch lightweight evidence first (route shell, key labels, structural markers).
4. Only run deeper extraction (bundle/string/component scan) when lightweight evidence is insufficient.
5. Skip version diff steps unless baseline/current inputs are explicitly provided.

For JS-heavy sites, treat static HTML as shell-only and extract structure from available bundled assets or provided screenshots.

## Auth-Gated Discovery

When key functionality is behind authentication:

1. Prefer provided authenticated HTML/snapshots for target pages.
2. If unavailable and credentials are provided, use temporary WDIO navigation with existing login page objects.
3. Capture only resulting page structure and feature evidence (not secret values).
4. Mark inaccessible areas explicitly as `unknown` instead of guessing.

Temporary WDIO scripts should be minimal and disposable, used only to unlock page evidence for analysis.

## Just-Enough Information Policy

Do not recreate the full site in exhaustive prose.

Capture only what is required to plan tests and triage/fix failures:

- critical routes/pages
- high-impact components and actions
- core state transitions
- important dependencies and risk points
- known unknowns/gaps

Keep low-value cosmetic detail brief unless it affects behavior or selectors.

## Analysis Model (Two-Level Structure)

Use a two-level hierarchy inspired by page-structure decomposition:

1. **Section boundaries**: top-level page regions and thematic breaks
2. **Content sequences within each section**: ordered subflows/components in each section

This avoids mixing page-level and component-level findings.

## Investigation Workflow

1. Validate evidence availability (URL/screenshot/HTML/version refs).
2. Identify top-level sections (header, hero, content groups, footer, etc.).
3. For each section, identify ordered content sequences.
4. Build component inventory (tabs, menus, forms, tables, actions, modals, filters, pagination).
5. Capture key functionality and interaction states.
6. Assign importance levels to functionality.
7. If baseline/current versions are provided, run structured diff comparison.
8. Save outputs for downstream human/agent use.

## Component Inventory Requirements

For each component/functionality, capture:

- location (section + sequence)
- user purpose
- key actions/events
- critical states (default/loading/empty/error/success)
- dependencies (auth, API, feature flags, permissions)

## Importance Scoring

Assign each functionality an importance level:

- `high`: business-critical flows (auth, checkout, account access, data submission)
- `medium`: primary usability and navigation flows
- `low`: non-critical enhancements and cosmetic interactions

Use this weighted lens when helpful:

`importance = business impact x usage frequency x change risk x failure severity`

## Version Comparison (When Available)

Compare baseline vs current for:

- structural changes (sections, sequences, routes)
- component changes (added/removed/modified)
- interaction/state changes
- selector/DOM changes likely to impact tests
- visible UX and accessibility shifts

Classify diffs by impact:

- `breaking`: likely to break existing tests or critical behavior
- `significant`: meaningful behavior or structure change
- `minor`: low-risk cosmetic or copy changes

## Output Files

Write/update:

- `references/website-analysis/<target>/website-analysis.md`
- `references/website-analysis/<target>/website-analysis.json`
- `references/website-analysis/<target>/website-diff.md` (only when comparison input exists)

## Target Resolution Rule

Resolve `<target>` consistently:

- Use the lowercase site host (e.g. `https://demo.learnwebdriverio.com/...` -> `demo.learnwebdriverio.com`).
- If host is unavailable but route/page path is known, use `unknown-target` and record the assumed source in analysis notes.
- For multi-site projects, keep one folder per host.
- Do not include protocol, query params, or trailing slash in `<target>`.

Optional mirror for cross-skill runtime consumption:

- `.webdriverio-skills/website-analysis.md`
- `.webdriverio-skills/website-analysis.json`

## Output Size Guidance

Use compact outputs by default:

- `website-analysis.md`: concise, high-signal sections only
- `website-analysis.json`: structured fields needed for downstream automation
- include an explicit `unknowns` list when evidence is incomplete

## Output Format (Markdown)

`website-analysis.md` should include:

1. Overview and input evidence
2. Section map (Level 1)
3. Content sequences per section (Level 2)
4. Component inventory
5. Functionality importance matrix
6. Testing implications (high-priority coverage targets)

`website-diff.md` should include:

1. Baseline vs current summary
2. Structured diff list by impact (`breaking`/`significant`/`minor`)
3. Recommended test updates

## Minimal JSON Shape

```json
{
  "updatedAt": "ISO-8601",
  "sections": [],
  "sequences": [],
  "components": [],
  "functionalities": [],
  "importance": [],
  "diff": []
}
```

## Common Mistakes

- Skipping section-level analysis and jumping straight to components.
- Capturing components without interaction states.
- Assigning importance without business context.
- Comparing versions without classifying impact.
- Producing narrative notes without reusable structure.
- Re-running full deep analysis when cached references are still valid.
