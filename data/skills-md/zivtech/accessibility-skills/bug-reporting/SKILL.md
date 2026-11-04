---
name: bug-reporting
description: >
  Load this skill whenever you are filing, reviewing, or generating accessibility
  bug reports — whether from automated tool output, manual testing, or AI agent
  scans. The purpose of this skill is to make accessibility errors easier to
  report accurately, so that developers can reproduce, understand, and fix them
  without additional back-and-forth. Absolutely always include the required
  fields (URL, XPath, HTML snippet, WCAG SC, rule ID, severity, frequency) in
  every report. Under no circumstances file a vague report that omits the
  failing element, the WCAG criterion, or the steps to reproduce.
license: MIT
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: mgifford
  version: "1.0.0"
---

# Accessibility Bug Reporting Skill

> **Canonical source**: `examples/ACCESSIBILITY_BUG_REPORTING_BEST_PRACTICES.md` in `mgifford/ACCESSIBILITY.md`
> This skill is derived from that file. If the upstream guide changes, sync intentionally rather than drifting silently.

Apply these rules when filing, reviewing, or generating accessibility bug reports
from any source — automated tool output, manual testing, or AI agent scans.

---

## Core Mandate

**Reproducibility is the single most important quality of a bug report.**
If a developer cannot reproduce the problem, they cannot fix it.

Every report must give enough information for a developer who was not present
during testing to reproduce, understand, and fix the problem without additional
back-and-forth.

Serialize each report from the finding entry's captured fields (from the scan/trace input or evidence-contract block) plus targeted per-finding lookups — never by re-reading the full scan or trace corpus wholesale.

---

## Severity Scale (this skill)

| Level | Meaning | Action |
| --- | --- | --- |
| **Critical** | Users cannot complete a core task at all | Must fix before release |
| **High** | Significant barrier that degrades or blocks a key workflow | Fix urgently |
| **Medium** | Noticeable barrier with a workaround available | Fix in near-term backlog |
| **Low** | Minor issue with minimal real-world impact | Fix when convenient |

---

## Critical: Required Fields

Every accessibility bug report **must** include all eight of the following fields.
**Omitting any required field is Critical** — the report cannot be acted on.

### 1. Page URL

Provide the exact URL where the issue was found, including query string and
fragment identifier if relevant.

```
URL: https://example.com/checkout?step=2#payment-form
```

If the issue appears on multiple pages, list all affected URLs or describe the
URL pattern (e.g. "all `/product/*` pages").

### 2. XPath — Simplified

Provide the shortest XPath that uniquely identifies the failing element.
Prefer attribute-based selectors over absolute paths.

```
//button[@id="submit-payment"]
//input[@name="card-number"]
//div[@role="dialog"][@aria-labelledby="modal-title"]
```

### 3. XPath — Full DOM Path

Provide the complete ancestor chain for disambiguation or when the simplified
XPath could match multiple elements.

```
/html/body/main/section[@id="checkout"]/form[@id="payment-form"]/fieldset[2]/input[@name="card-number"]
```

Automated tools must emit **both** XPath forms. The full path supports debugging
in environments where IDs change dynamically (e.g. React, Angular).

### 4. HTML Snippet

Include the minimal HTML fragment that demonstrates the problem. Trim surrounding
markup to the smallest context that still shows the issue.

```html
<!-- Bad: no accessible name -->
<button>
  <img src="close.svg">
</button>

<!-- Good: accessible name provided -->
<button>
  <img src="close.svg" alt="Close dialog">
</button>
```

Include parent elements only when the violation depends on the parent–child
relationship (e.g. missing `<label>` for `<input>`).

### 5. WCAG Success Criterion

Cite the specific WCAG 2.1 or 2.2 Success Criterion violated, including its level.

```
WCAG SC: 1.1.1 Non-text Content (Level A)
WCAG SC: 4.1.2 Name, Role, Value (Level A)
WCAG SC: 1.4.3 Contrast (Minimum) (Level AA)
```

### 6. ACT Rule or Checker Rule

Reference the rule from the testing tool or from the W3C ACT framework.

```
Rule ID:  image-alt
Rule:     Images must have alternate text
Tool:     axe-core 4.x

ACT Rule: 23a2a8 — Image has non-empty accessible name
URL:      https://act-rules.github.io/rules/23a2a8
```

When multiple tools flag the same issue, list all rule IDs.

### 7. Severity

Assign a severity level using the taxonomy above. Use it consistently across
all reports in a project. When multiple tools report the same violation at
different severities, use the higher severity.

A `corroborated` cross-detector finding (the same violation flagged by more than one engine) is not confirmed — it is only a triage-confidence signal, so severity must never be bumped because engines agree, and any `detected_by` engine id cited must come from the fixed vocabulary (`axe-core`, `html_codesniffer`, `alfa`, `wave`) rather than an invented tool name.

### 8. Frequency / Occurrence

Report how often the element appears on the page and across the site.

```
Frequency: 1 instance on this page
Frequency: Appears on every page in the main navigation
Frequency: Found on 23 of 47 pages crawled (49%)
```

For automated scans, include aggregate counts:

```json
{
  "rule": "image-alt",
  "occurrences": 14,
  "pages_affected": 6,
  "total_pages_scanned": 50
}
```

Frequency informs prioritisation. A single critical failure may warrant immediate action; a low-severity issue across hundreds of pages may need a systematic fix.

**Frequency amplifies effective severity.** A "Low" rated issue on every page or a top user task (sign-in, checkout, search) should be treated with higher urgency than its base severity suggests.

| Situation | Suggested priority adjustment |
|-----------|-------------------------------|
| Low severity, appears on every page | Treat as Medium |
| Medium severity, appears on every page | Treat as High |
| Low/Medium severity, on a top-task page | Escalate by one severity level |
| Low/Medium severity, on a high-traffic landing page | Escalate by one severity level |

---

## High: Recommended Additional Fields

These fields are not always required but significantly improve report quality.
**Omitting them is a High severity gap** when the issue is complex or the audience is unfamiliar
with the codebase.

### Issue Summary (Title)

Write a concise title: `[Component] — [Failure mode] ([WCAG SC])`.

**Good:**

* `Close button missing accessible name (WCAG 1.1.1)`
* `Error message not associated with form field (WCAG 1.3.1)`

**Avoid:**

* `Accessibility issue found`
* `Screen reader problem on checkout`

### Description

Explain what is wrong and why it is a barrier for users with disabilities.

```
The "Close" button in the cookie-consent dialog contains only a decorative SVG
icon with no alt text, aria-label, or visible text. Screen reader users hear
"button" with no indication of its purpose, making it impossible to dismiss the
dialog by voice or from a screen reader virtual cursor.
```

### Steps to Reproduce

Number the steps a developer can follow to see the failure.

```
1. Go to https://example.com/shop
2. Wait for the cookie consent banner to appear
3. Open NVDA (or VoiceOver on macOS)
4. Press Tab to move focus to the "X" button in the banner
5. Listen to what the screen reader announces
```

For automated test output, include the command used:

```bash
npx axe https://example.com/shop --tags wcag2a,wcag2aa --reporter json
```

### Expected Behaviour

State what the correct experience should be.

```
Expected: Screen reader announces "Close cookie consent dialog, button"
          or equivalent meaningful label.
```

### Actual Behaviour

State what currently happens.

```
Actual: Screen reader announces "button" only. No accessible name is provided.
```

### Testing Environment

Specify the full stack. AT bugs are often environment-specific.

```
Browser:       Chrome 124 / Firefox 126 / Safari 17.4
OS:            Windows 11 / macOS 14 / iOS 17
Screen reader: NVDA 2024.1 / JAWS 2024 / VoiceOver
Zoom level:    100% / 200%
Tool:          axe-core 4.9.1 / Accessibility Insights 2.47 / Pa11y 6.2
```

### Impact Statement

Describe which disability groups are affected and how.

```
Impact: Blind and low-vision users relying on screen readers cannot identify
        or operate the close button. Users who rely on voice control software
        (e.g. Dragon NaturallySpeaking) cannot activate an unnamed button by
        speaking its label.
```

### Suggested Fix

Provide a concrete remediation when possible.

```html
<!-- Current (broken) -->
<button class="close-btn">
  <svg aria-hidden="true" ...></svg>
</button>

<!-- Fixed: Option A — aria-label -->
<button class="close-btn" aria-label="Close cookie consent dialog">
  <svg aria-hidden="true" ...></svg>
</button>

<!-- Fixed: Option B — visually hidden text -->
<button class="close-btn">
  <svg aria-hidden="true" ...></svg>
  <span class="visually-hidden">Close cookie consent dialog</span>
</button>
```

### Personalisation and Context

Accessibility failures are not always reproducible on every page load. Many issues only surface under specific user settings, device types, or navigation paths. Always record the personalisation state and context at the time of discovery.

**Colour scheme and display preferences**

```
Colour scheme:    Light mode / Dark mode / System default
Forced Colors:    Active (Windows High Contrast) / Inactive
Contrast mode:    Standard / Increased contrast (macOS)
```

**CSS media features**

```
prefers-color-scheme:   light / dark
prefers-reduced-motion: reduce / no-preference
prefers-contrast:       more / less / forced / no-preference
forced-colors:          active / none
```

**Viewport and device type**

```
Viewport:    375 × 812 px (iPhone 14, Safari iOS 17)
Viewport:    1440 × 900 px (MacBook Pro, Chrome 124)
Device:      Mobile — iOS 17 / Android 14
Device:      Desktop — Windows 11 / macOS 14
Orientation: Portrait / Landscape
```

**Navigation path and UI state**

```
Arrived via:   Direct URL / Search results link / Internal navigation from [page]
Preceded by:   Clicked "Add to cart" on product page, then navigated to checkout
UI state:      Modal open / Accordion expanded / Dropdown active
Login state:   Authenticated (standard user role) / Guest / Admin
```

### Baseline Test ID (declared Section 508 audits only)

When — and only when — the report belongs to an audit engagement whose audit-scope plan carries a Revised Section 508 conformance floor declaration (the a11y-planner federal profile), add the ICT Testing Baseline **web** test the issue files under:

```
Baseline test:  5.C-ControlState
```

Rules (they mirror the A11y Evidence Finding Contract's `baseline_test` field):

* The ID must exist in the web list of `docs/ict-baseline-test-id-manifest.yaml` — baseline IDs are valid per-baseline (`11.A-PageTitled` is web-only, `11.A-DocumentTitled` documents-only) and are the exact-ID class automated generators fabricate. Verify against the manifest; never trust a generated ID.
* For the three media-player-control tests (`17.A`–`17.C`) the failing requirement is a 508 provision, not a WCAG SC — cite the provision (e.g. `508 503.4.1`) in the WCAG field position, matching the evidence contract's rule.
* `24.A-Parsing` never appears on a report — it always passes upstream (WCAG 2.0 Errata 13); file markup consequences under the criteria they actually break.
* Severity stays impact-based (this skill's scale) and is orthogonal to the baseline outcome.
* Outside a declared-508 audit, omit the field entirely — a baseline citation on a component-scope report is itself a defect in the report.

### Verification Evidence (when reporting a verified fix)

When a report documents a fix rather than a fresh finding, name the evidence mode that confirmed it and confirm its type matches the defect class per a11y-test's Verification evidence contract — a screenshot alone never verifies a keyboard, focus, or announcement fix.

---

## Structured Report Templates

### Markdown Template (for GitHub Issues)

````markdown
## Accessibility Issue: [Brief Description]

**Bug ID:** `[PREFIX-xxxxxxxx]` (instance) / `[PREFIX-xxxxxxxx]` (pattern)
**URL:** [Full URL where issue was found]
**XPath:** `[Shortest unique XPath]`
**Full DOM path:** `[Full ancestor chain XPath]`
**WCAG SC:** [SC number] — [SC name] (Level [A/AA/AAA])
**Rule:** [Tool name] — [Rule ID]
**Severity:** [Critical / High / Medium / Low]
**Frequency:** [Number of instances; pages affected]
**Screen type:** [desktop / mobile] | **Colour mode:** [light / dark]

### HTML Snippet

```html
[Minimal failing HTML fragment]
```

### Description

[Explain what is wrong and why it creates a barrier]

### Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Behaviour

[What should happen]

### Actual Behaviour

[What currently happens]

### Testing Environment

| Item | Value |
|---|---|
| Browser | [name and version] |
| OS | [name and version] |
| Screen reader | [name and version, or N/A] |
| Testing tool | [name and version] |

### Impact

[Who is affected and how]

### Suggested Fix (optional)

[Code or prose describing the fix]
````

### JSON Schema for Automated Tool Output

Use this schema when scripts or CI pipelines emit machine-readable accessibility reports.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AccessibilityIssue",
  "type": "object",
  "required": ["url", "wcag_sc", "severity", "rule_id", "xpath", "html_snippet"],
  "properties": {
    "instance_id": {
      "type": "string",
      "pattern": "^[A-Z0-9]+-[0-9a-f]{8}$",
      "examples": ["DRU-a3f1b2c4"],
      "description": "Stable identifier for this specific violation on this page. Hash of page path + CSS selector + rule ID + screen type."
    },
    "pattern_id": {
      "type": "string",
      "pattern": "^[A-Z0-9]+-[0-9a-f]{8}$",
      "examples": ["DRU-f7e3a1b2"],
      "description": "Stable identifier for the underlying template-level pattern across pages. Hash of CSS selector + rule ID + screen type (no page path)."
    },
    "screen_type": { "type": "string", "enum": ["desktop", "mobile"] },
    "color_mode": { "type": "string", "enum": ["light", "dark"], "default": "light" },
    "url": { "type": "string", "format": "uri" },
    "xpath": { "type": "string" },
    "xpath_full": { "type": "string" },
    "html_snippet": { "type": "string" },
    "wcag_sc": { "type": "string", "pattern": "^\\d\\.\\d+\\.\\d+$" },
    "wcag_level": { "type": "string", "enum": ["A", "AA", "AAA"] },
    "rule_id": { "type": "string" },
    "act_rule_id": { "type": "string" },
    "baseline_test": {
      "type": "string",
      "pattern": "^\\d{1,2}\\.[A-Z]-[A-Za-z]+$",
      "examples": ["5.C-ControlState"],
      "description": "Declared Section 508 audits only: ICT Testing Baseline web test ID. Pattern match is not validity — the ID must exist in the web list of docs/ict-baseline-test-id-manifest.yaml. Omit outside declared-508 scope."
    },
    "tool": { "type": "string" },
    "severity": { "type": "string", "enum": ["critical", "high", "medium", "low"] },
    "frequency": {
      "type": "object",
      "properties": {
        "instances_on_page": { "type": "integer" },
        "pages_affected": { "type": "integer" },
        "total_pages_scanned": { "type": "integer" }
      }
    },
    "summary": { "type": "string" },
    "description": { "type": "string" },
    "impact": { "type": "array", "items": { "type": "string" } },
    "environment": {
      "type": "object",
      "properties": {
        "browser": { "type": "string" },
        "os": { "type": "string" },
        "screen_reader": { "type": "string" },
        "zoom_level": { "type": "string" }
      }
    },
    "suggested_fix": { "type": "string" },
    "steps_to_reproduce": { "type": "array", "items": { "type": "string" } }
  }
}
```

### Example JSON Report (axe-core output mapped to schema)

```json
{
  "instance_id": "DRU-a3f1b2c4",
  "pattern_id": "DRU-f7e3a1b2",
  "screen_type": "desktop",
  "color_mode": "light",
  "url": "https://example.com/checkout?step=2",
  "xpath": "//button[contains(@class,'close-btn')]",
  "xpath_full": "/html/body/div[@id='cookie-banner']/button[contains(@class,'close-btn')]",
  "html_snippet": "<button class=\"close-btn\"><svg aria-hidden=\"true\"></svg></button>",
  "wcag_sc": "4.1.2",
  "wcag_level": "A",
  "rule_id": "button-name",
  "act_rule_id": "97a4e1",
  "tool": "axe-core 4.9.1",
  "severity": "critical",
  "frequency": { "instances_on_page": 1, "pages_affected": 12, "total_pages_scanned": 50 },
  "summary": "Close button missing accessible name (WCAG 4.1.2)",
  "description": "The cookie consent close button contains only an SVG icon with no accessible name.",
  "impact": ["blind", "low-vision", "voice-control"],
  "environment": { "browser": "Chrome 124", "os": "Windows 11", "screen_reader": "NVDA 2024.1", "zoom_level": "100%" },
  "suggested_fix": "<button class=\"close-btn\" aria-label=\"Close cookie consent dialog\"><svg aria-hidden=\"true\"></svg></button>",
  "steps_to_reproduce": [
    "Go to https://example.com/checkout?step=2",
    "Wait for the cookie consent banner to appear",
    "Open NVDA and press Tab to reach the close button",
    "Observe that NVDA announces 'button' with no label"
  ]
}
```

### XLSX workbook for client triage (reference script)

When the receiving team tracks fixes in a spreadsheet rather than an issue tracker, serialize the JSON reports above into a workbook with [`references/build-error-workbook.mjs`](references/build-error-workbook.mjs) — a routed reference script, not a vendored tool: it needs `exceljs@4.4.0` (MIT) installed in *your* project, exact-pinned, never in this repository. Do not add it beside a team that already runs an issue tracker: a workbook next to a tracker is two sources of truth, and the finding that gets fixed is the one in the tracker — file issues there (Markdown template above) and treat any workbook as a read-only export.

```bash
node build-error-workbook.mjs --in findings.json --out findings.xlsx --product "Name the client uses"
node build-error-workbook.mjs --verify findings.xlsx --in findings.json   # exit 1 on any drift
```

The input is the JSON schema above (an array, or an object with `issues`). The build refuses (exit 2) rather than silently degrading: a row missing a required field, a severity outside the four-value scale, a `wcag_sc` that is neither `x.y.z` nor `N/A`, a duplicate `instance_id`, or a cell over Excel's 32,767-character limit all stop it and are listed by row. Keys outside the schema are not serialized; they are counted on the `Read Me` sheet so a dropped field is visible, never silent. `finding_id` is the one column beyond the schema. Two values are normalized and nothing else is altered — `severity` is lower-cased and an `n/a` SC is written `N/A` — and the `Read Me` says so.

Three sheets: `Read Me` (provenance — source file, SHA-256, size, row count, generator — and the claim boundary as text), `Findings` (one row per report in a fixed column order, a defined table with a header row, text-formatted ID and SC columns, no merged cells, and three owner-fillable triage columns: Owner, Remediation status with a dropdown, Notes), and `Summary` (live COUNTIF formulas by severity, by SC, and by remediation status, each with a cached result, under a one-line boundary saying these are counts of findings, not outcomes). `--verify` reads a workbook back and checks the finding cells against the input cell by cell, the defined table's span, every Summary cell by position (label, formula, and — for finding counts — cached result), Excel error strings on every sheet, and every Read Me field derivable from the input, SHA-256 included — triage columns are excluded by design, so it still proves the finding data after the client has filled them in.

What the workbook is **not**: not a conformance report (criterion-level outcomes belong to the evaluation report, `docs/a11y-evaluation-report-contract.md`, which `acr-reporting` then serializes; severity here is impact on people, never a PASS/FAIL), and not a retest ledger — `Resolved` in the status column is the receiving team's workflow state, closed only by the auditor from class-matched retest evidence (a11y-test's verification evidence contract). Boundary and validation receipts: `docs/error-workbook-adoption-assessment.md`.

### EARL: Evaluation and Report Language

**Report-level companion — `acr-reporting`.** This skill is finding-level: findings in, filable issues out. Aggregating a *finished audit-scope evaluation* into an Accessibility Conformance Report is the `acr-reporting` skill's job (OpenACR format, draft-only, human sign-off) — route ACR/VPAT-shaped requests there, and keep reports here citing their `finding_id`s so ACR remarks can trace back to the same findings.

[EARL (Evaluation and Report Language)](https://www.w3.org/WAI/standards-guidelines/earl/) is a W3C standard for expressing test results in a machine-readable format. Use EARL when you need interoperable, tool-agnostic reports that can be processed by different systems — for example, aggregating results from multiple tools, feeding a compliance dashboard, or archiving audit evidence.

```turtle
@prefix earl: <http://www.w3.org/ns/earl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] a earl:Assertion ;
   earl:assertedBy <https://example.com/tools/axe-runner> ;
   earl:subject <https://example.com/checkout?step=2> ;
   earl:test <http://www.w3.org/TR/WCAG21/#non-text-content> ;
   earl:result [
     a earl:TestResult ;
     earl:outcome earl:failed ;
     dcterms:description "Close button contains only an SVG icon with no accessible name." ;
     dcterms:date "2025-06-01T10:30:00Z"^^xsd:dateTime
   ] ;
   earl:mode earl:automatic .
```

| Term | Meaning |
|------|---------|
| `earl:Assertion` | A single test result (subject + test + outcome) |
| `earl:subject` | The URL or resource that was tested |
| `earl:test` | The criterion or rule being tested (WCAG SC, ACT rule, etc.) |
| `earl:outcome` | `earl:passed`, `earl:failed`, `earl:cantTell`, `earl:inapplicable`, or `earl:untested` |
| `earl:mode` | How the test was performed: `earl:automatic`, `earl:manual`, or `earl:semiAuto` |
| `earl:assertedBy` | The tool or person that produced the assertion |

EARL output can be produced by [Alfa](https://github.com/Siteimprove/alfa), [Axe Reporter EARL](https://github.com/dequelabs/axe-reporter-earl), and [ACT-Rules implementations](https://act-rules.github.io/). The W3C [WCAG-EM Report Tool](https://www.w3.org/WAI/eval/report-tool/) also exports EARL. [WCAG-EM 2.0](https://www.w3.org/TR/wcag-em-2/) (Group Note, 2026) keeps EARL as its recommended machine-readable report format while generalizing the methodology from websites to digital products; the Report Tool is still WCAG-EM 1-based, with a WCAG-EM 2 version announced for later in 2026.

---

## Guidance for Automated Tools and AI Agents

Apply these additional rules when scripts or AI agents generate reports.

### 5.1 Always Emit Both XPath Forms

Emit both the simplified XPath (shortest unique selector) and the full DOM path XPath in every violation. The simplified form aids human readability; the full form aids deterministic replay.

### 5.2 Deduplicate Before Reporting

Group violations by rule and normalised XPath before filing. Report one issue with `frequency.instances_on_page` set to the count rather than filing hundreds of identical issues.

```python
# Pseudocode: aggregate duplicates
issues = defaultdict(list)
for violation in raw_results:
    key = (violation["rule_id"], violation["wcag_sc"], normalize_xpath(violation["xpath"]))
    issues[key].append(violation)

for key, group in issues.items():
    report_issue(group[0], frequency=len(group))
```

### 5.3 Map Tool Output to WCAG Criteria

Every automated rule should map to at least one WCAG SC. Maintain a rule-to-WCAG mapping table in your project so that reports consistently include the criterion.

### 5.4 Preserve the HTML Snippet

Extract the failing element's outer HTML at scan time. DOM content may change after the scan. The preserved snippet allows verification of whether a deployed fix addresses the original issue.

### 5.5 Assign Severity Consistently

Use a single severity taxonomy across all reports and all tools. If multiple tools report the same violation at different severities, use the higher severity.

### 5.6 Include Confidence Score for Automated Detections

Include a `confidence` field when the tool provides it, especially for violations that require manual confirmation (e.g. colour contrast over a gradient):

```json
{
  "rule_id": "color-contrast",
  "confidence": "needs-review",
  "note": "Background colour is a CSS gradient; automated contrast check may be inaccurate. Manual verification required."
}
```

### 5.7 AI Agent Prompt for Filing a GitHub Issue

When an AI agent files a GitHub Issue from scan output, use this prompt structure:

```
You are an accessibility engineer filing a GitHub Issue.
Given the following JSON violation report, create a well-structured
GitHub Issue using the Markdown template above.

Rules:
- Use the issue summary as the title.
- Populate all fields; write "N/A" only if the data is genuinely absent.
- Do not paraphrase WCAG criterion names; use the exact W3C wording.
- Include the HTML snippet in a fenced code block.
- Add the label "accessibility" to the issue.

Violation data:
[INSERT JSON HERE]

Template:
[INSERT MARKDOWN TEMPLATE HERE]
```

### 5.8 Generate Stable Unique Identifiers for Violations

Assigning a stable identifier to each violation enables automated pipelines to track fixes, detect regressions, and deduplicate across scan runs.

**Two levels of identification**

| Level | Inputs to hash | Purpose |
|-------|---------------|---------|
| `instance_id` | page path + CSS selector + rule ID + screen type | Identifies one occurrence on one specific page |
| `pattern_id` | CSS selector + rule ID + screen type | Identifies the recurring pattern across pages |

**Identifier format:** `[PREFIX]-[8-char-hex]` (e.g. `DRU-a3f1b2c4`)

The prefix is project-specific (e.g. `DRU` for Drupal, `A11Y` as a generic default). Infer screen type from viewport width: `< 768 px = mobile`, `>= 768 px = desktop`. Default `color_mode` to `light`.

**JavaScript implementation (Node.js)**

```javascript
const crypto = require('crypto');

const MOBILE_BREAKPOINT = 768;

function detectScreenType(viewport) {
  return viewport && viewport.width < MOBILE_BREAKPOINT ? 'mobile' : 'desktop';
}

function normalizeSelector(target) {
  return Array.isArray(target) ? target.join(' > ') : String(target);
}

function generateInstanceId(pagePath, selector, ruleId, screenType, prefix = 'A11Y') {
  const input = `${pagePath}|${selector}|${ruleId}|${screenType}`;
  const hash = crypto.createHash('sha256').update(input).digest('hex').slice(0, 8);
  return `${prefix}-${hash}`;
}

function generatePatternId(selector, ruleId, screenType, prefix = 'A11Y') {
  const input = `${selector}|${ruleId}|${screenType}`;
  const hash = crypto.createHash('sha256').update(input).digest('hex').slice(0, 8);
  return `${prefix}-${hash}`;
}

function annotateViolations(axeResults, prefix = 'A11Y', colorMode = 'light') {
  const pagePath = new URL(axeResults.url).pathname;
  const viewport = { width: axeResults.testEnvironment.windowWidth };
  const screenType = detectScreenType(viewport);

  return axeResults.violations.flatMap(violation =>
    violation.nodes.map(node => {
      const selector = normalizeSelector(node.target);
      return {
        ...node,
        rule_id:     violation.id,
        instance_id: generateInstanceId(pagePath, selector, violation.id, screenType, prefix),
        pattern_id:  generatePatternId(selector, violation.id, screenType, prefix),
        screen_type: screenType,
        color_mode:  colorMode,
      };
    })
  );
}
```

The CSS selector (from `node.target`) is used in the hash rather than the XPath because axe-core reports it natively and it is stable across XPath conversion logic changes. Include both in the report; use only the CSS selector as the hash input.

---

## Reporting to External Organisations

When reporting accessibility barriers to a third-party (vendor, government,
public website), adapt the report to the audience:

1. **Check for an existing channel** — look for an accessibility statement,
   `accessibility@` email, or feedback form.
2. **Be specific** — provide the exact page, element, and barrier.
3. **Focus on impact** — explain who is affected and what they cannot complete.
4. **Reference WCAG and applicable law** — cite the specific criterion and relevant
   legislation (Section 508, EN 301 549, AODA, etc.).
5. **Offer to help** — suggest the fix; organisations act faster when a solution
   accompanies the problem.
6. **Set a timeline** — request acknowledgement within a defined period (e.g.
   10 business days) and a remediation timeline for critical issues.
7. **Escalate if necessary** — contact the relevant enforcement body or ombudsman
   if no response is received.

### External Report Email Template

```
Subject: Accessibility barrier on [Page Title] — [WCAG SC]

Dear [Organisation Name] Accessibility Team,

I am writing to report an accessibility barrier I encountered on your website.

Page:    [Full URL]
Issue:   [One-sentence description of the barrier]
Impact:  [Who is affected and what they cannot do]
WCAG SC: [SC number and name, Level]

Steps to reproduce:
1. [Step 1]
2. [Step 2]

Expected: [What should happen]
Actual:   [What happens instead]

Suggested fix: [Brief description or code snippet if appropriate]

I am available to provide further information or test a proposed fix.
I would appreciate acknowledgement within 10 business days and a
remediation timeline for this critical barrier.

Thank you for your attention to this matter.

[Your name / organisation]
```

---

## Pre-Filing Quality Checklist

Before filing or submitting an accessibility bug report, verify each item:

* [ ] URL is exact and publicly accessible (or a test account is provided)
* [ ] Unique bug identifiers (`instance_id` and `pattern_id`) are generated and included
* [ ] Screen type (`desktop` / `mobile`) and colour mode (`light` / `dark`) are recorded
* [ ] XPath (simplified) uniquely identifies the element
* [ ] Full DOM path XPath is included
* [ ] HTML snippet is minimal and self-contained
* [ ] WCAG SC is cited with the correct level (A/AA/AAA)
* [ ] Automated rule ID is included (axe-core, ACT, or tool-specific)
* [ ] Severity is assigned using the project's standard taxonomy
* [ ] Frequency / occurrence count is provided
* [ ] Summary title follows `[Component] — [Failure] ([WCAG SC])` pattern
* [ ] Steps to reproduce are numbered and complete
* [ ] Expected and actual behaviours are stated separately
* [ ] Testing environment (browser, OS, AT, tool) is documented
* [ ] Personalisation context is recorded (colour scheme, CSS media features, viewport, navigation path)
* [ ] Impact on specific disability groups is described
* [ ] Duplicate violations are aggregated, not filed individually
* [ ] For automated output: confidence level is included where relevant

---

## Commonly Violated WCAG Criteria

| SC | Name | Level | Common Violations |
| --- | --- | --- | --- |
| 1.1.1 | Non-text Content | A | Missing `alt` on images, unlabelled icon buttons |
| 1.3.1 | Info and Relationships | A | Unsemantic heading structure, missing form labels |
| 1.3.3 | Sensory Characteristics | A | Instructions that rely on shape, colour, or position only |
| 1.4.1 | Use of Color | A | Status conveyed by colour alone |
| 1.4.3 | Contrast (Minimum) | AA | Text below 4.5:1 contrast ratio |
| 1.4.4 | Resize Text | AA | Page breaks at 200% zoom |
| 1.4.11 | Non-text Contrast | AA | UI component borders below 3:1 contrast |
| 2.1.1 | Keyboard | A | Elements not reachable or operable by keyboard |
| 2.4.3 | Focus Order | A | Illogical tab order, focus moves unexpectedly |
| 2.4.7 | Focus Visible | AA | No visible focus indicator |
| 3.3.1 | Error Identification | A | Form errors not described in text |
| 3.3.2 | Labels or Instructions | A | Form fields without visible labels |
| 4.1.2 | Name, Role, Value | A | Custom widgets missing ARIA name, role, or state |
| 4.1.3 | Status Messages | AA | Notifications not exposed to screen readers |

For the complete list, see the [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/).

---

## References

* [Full best practices guide](https://github.com/mgifford/ACCESSIBILITY.md/blob/main/examples/ACCESSIBILITY_BUG_REPORTING_BEST_PRACTICES.md)
* [Writing Impactful Accessibility Reports](https://medium.com/openconcept-stories/writing-impactful-accessibility-reports-d6cdd84356fd) — Mike Gifford, OpenConcept
* [How to Fix Accessibility Bugs](https://github.com/readme/guides/fix-accessibility-bugs) — Mike Gifford, GitHub README Guides
* [Contacting Organizations about Inaccessible Websites](https://www.w3.org/WAI/teach-advocate/contact-inaccessible-websites/) — W3C WAI
* [How to Report Accessibility Bugs](https://www.digitala11y.com/how-where-to-report-accessibility-bugs/) — DigitalA11y
* [Template: Reporting Accessibility Issues](https://accessibility.huit.harvard.edu/template-reporting-accessibility-issues) — Harvard University
* [ACT Rules Community Group](https://act-rules.github.io/) — W3C
* [Accessibility Insights for Web](https://github.com/microsoft/accessibility-insights-web) — Microsoft
* [EARL: Evaluation and Report Language](https://www.w3.org/WAI/standards-guidelines/earl/) — W3C WAI
* [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
