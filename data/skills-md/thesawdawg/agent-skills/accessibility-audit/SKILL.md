---
name: accessibility-audit
description: Run a WCAG 2.2 (AA and above) accessibility audit of a live web app — automated axe-core scanning cross-referenced against the current WCAG success-criteria table, plus manual verification of what automated tools structurally can't check (keyboard operability, focus order, alt-text quality, timing/motion). Produces a per-criterion conformance report. Use when the user wants an accessibility/a11y audit, a WCAG compliance check, or to know whether a site meets AA before shipping.
---

# Accessibility Audit Skill

WCAG-conformance testing of a web application: automated rule scanning against an up-to-date standards engine, manual verification of what that engine can't check by nature, and a report mapped to specific WCAG success criteria — not just a generic bug list.

This skill is [dogfood](../dogfood/SKILL.md)'s sibling — it reuses the same persistent-browser driver (`../dogfood/scripts/browser-driver.mjs`) rather than duplicating it, and adds one thing dogfood doesn't have: an `axe` command that runs [axe-core](https://github.com/dequelabs/axe-core) (the industry-standard, actively-maintained WCAG rule engine used by Deque, Google Lighthouse, and most enterprise a11y tooling) against the current page. axe-core's rules are tagged by WCAG version and level (`wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa`) and updated upstream as the spec evolves — that's the "up-to-date database of standards" this skill relies on, rather than a static hand-maintained checklist. [references/wcag-criteria.md](references/wcag-criteria.md) is the human-readable companion table (SC numbers, names, levels) used to cite findings by criterion, not a substitute rule source.

See also: [USE_CASES.md](USE_CASES.md) for trigger phrases and a worked example, and the [top-level skills index](../USE_CASES.md).

## Prerequisites

- One-time setup: `cd ../dogfood/scripts && npm install` (pulls in `playwright` and `axe-core`; the Chromium *binary* is pre-installed in this environment already).
- A target URL and testing scope from the user, or the defaults below if they don't give one.

## Inputs

The user provides:

1. **Target URL** — same discovery pattern as dogfood: check `package.json` for a dev script, probe common local ports (`3000`, `5173`, `8080`, `4200`, `5000`, `8000`), or ask for a staging/public URL if none respond.
2. **Scope** — which pages/flows to audit. Default to the site's key pages (home, nav targets, primary forms/flows) rather than every URL, and say explicitly what's in scope.
3. **Conformance target** — default to **WCAG 2.2 Level AA** (covers 2.0 AA and 2.1 AA too, since 2.2 only adds criteria at each level, never removes them — see [references/wcag-criteria.md](references/wcag-criteria.md)). Ask only if the user wants **AAA** on specific criteria, or wants to scope down to A-only.
4. **Output directory** (optional, default `./accessibility-audit-output`).

## Workflow

Work through five phases. Track each as a task.

### Phase 1: Plan

1. Create the output directory:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence for violations and manual findings
   ├── violations.json    # Running list of findings (build this as you go)
   └── report.md          # Final report (generated in Phase 5)
   ```
2. Confirm scope and conformance target with the user.
3. Launch the shared browser driver in the background, same as dogfood:
   ```bash
   node ../dogfood/scripts/browser-driver.mjs launch --state-dir {output_dir}/.browser
   ```
   Run with `run_in_background: true`. It blocks until `close` in Phase 5.

### Phase 2: Automated Scan

For each page in scope:

1. **Navigate:**
   ```bash
   node ../dogfood/scripts/browser-driver.mjs navigate --state-dir {output_dir}/.browser --url "https://example.com/page"
   ```
2. **Run the axe scan**, scoped to the conformance target's tags (default shown; drop `wcag22aa` for a 2.1-only target, or add nothing extra for AAA — axe's AAA tags are `wcag2aaa`/`wcag21aaa`, add them explicitly only where the user asked for AAA on a specific criterion):
   ```bash
   node ../dogfood/scripts/browser-driver.mjs axe --state-dir {output_dir}/.browser --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa
   ```
3. For each violation in the result's `violations[]` array, record: `id`, `impact`, `tags` (map to WCAG SC via [references/wcag-criteria.md](references/wcag-criteria.md)), `description`, `help`/`helpUrl`, and every entry in `nodes[]` (`target` selector, `html`, `failureSummary`).
4. **Screenshot flagged elements** — use `annotate` to badge and screenshot the page so violations have visual evidence, same as dogfood:
   ```bash
   node ../dogfood/scripts/browser-driver.mjs annotate --state-dir {output_dir}/.browser --path {output_dir}/screenshots/page-N.png
   ```
5. Append each violation to `{output_dir}/violations.json`.

### Phase 3: Manual Verification

Automated tools cover an estimated 30-50% of WCAG failures by nature — the rest require deliberate manual checks. Do these for every page/flow in scope, using the same driver:

1. **Keyboard-only navigation** (2.1.1, 2.1.2, 2.4.3, 2.4.7): repeatedly `press --key Tab` through the page. Verify every interactive element is reachable, focus order matches visual/logical order, focus is always visible, and nothing traps focus.
   ```bash
   node ../dogfood/scripts/browser-driver.mjs press --state-dir {output_dir}/.browser --key Tab
   node ../dogfood/scripts/browser-driver.mjs screenshot --state-dir {output_dir}/.browser --path {output_dir}/screenshots/focus-N.png
   ```
2. **Screen-reader semantics** (1.3.1, 2.4.6, 4.1.2): dump the accessibility tree and review landmark roles, heading hierarchy, and whether custom/ARIA controls expose sensible names and roles.
   ```bash
   node ../dogfood/scripts/browser-driver.mjs snapshot --state-dir {output_dir}/.browser
   ```
3. **Alt-text quality** (1.1.1): axe only flags *missing* alt text. Read the `annotate` screenshots yourself (you're multimodal) and judge whether existing alt text is meaningful, not just present — "image123.png" or "photo" is a failure axe won't catch.
4. **Reflow at 400% zoom** (1.4.10): resize the effective viewport (or use `scroll` + `screenshot` at a narrow width) and confirm no content loss or two-dimensional scrolling.
5. **Timing, motion, flashing** (2.2.1, 2.2.2, 2.3.1): observe any auto-advancing carousels, countdown timers, or animations over a few seconds; confirm pause/stop controls exist and nothing flashes more than 3×/second.
6. **Error identification and suggestion** (3.3.1, 3.3.2, 3.3.3): submit forms with invalid/empty input, same as dogfood's form-validation testing, and judge whether errors are identified in text with a usable suggestion — not just a red border.
7. **Cross-page consistency** (3.2.3, 3.2.4, 3.2.6), if scope spans multiple pages: confirm navigation, component labeling, and help mechanisms stay in the same relative order and use consistent names across pages.

Record each manual finding the same way as automated ones: WCAG SC, severity, evidence, expected vs. actual.

### Phase 4: Categorize

1. Read back `{output_dir}/violations.json` in full, plus manual findings.
2. De-duplicate — the same underlying issue (e.g. a shared header component) often triggers on every page; merge those into one finding with all affected URLs listed, don't report it N times.
3. For every WCAG SC actually touched by scope, assign a status: **Pass**, **Fail**, **Needs manual review** (axe can't be sure — e.g. it flags "check that this makes sense" rules), or **N/A** (criterion doesn't apply — e.g. no audio/video content means the media criteria are N/A).
4. Sort automated violations by axe `impact` (critical → serious → moderate → minor); sort manual findings by your own judgment of severity (Blocker/Major/Minor).

### Phase 5: Report

1. Fill [templates/accessibility-report-template.md](templates/accessibility-report-template.md): executive summary, the full success-criteria checklist for the audited scope, violation details with screenshots, manual findings, not-tested section. Save to `{output_dir}/report.md`.
2. State the **overall conformance verdict** explicitly and plainly — does this scope currently meet the target level, or not, and by how much (N violations across M criteria)? Don't bury this in the middle of the report.
3. Close the browser session:
   ```bash
   node ../dogfood/scripts/browser-driver.mjs close --state-dir {output_dir}/.browser
   ```
4. Surface the report and Critical/Serious violation screenshots to the user — the evidence is the point, same as dogfood.

## Notes on axe-core's coverage

- axe-core is versioned via npm (`dogfood/scripts/package.json`) — `npm update axe-core` in that directory pulls newer rules as the library evolves. This skill doesn't hardcode rule logic; it defers entirely to whatever axe-core version is installed.
- A **zero-violations automated scan is not a conformance guarantee** — say so in the report. It means "no automated rule fired," not "meets WCAG." The Phase 3 manual checks are not optional filler; report both together.
- If `axe` returns an empty `violations[]` array but `incomplete[]` is non-empty, treat `incomplete` entries as "needs manual review," not as passes — axe uses `incomplete` specifically for checks it can't resolve automatically (e.g. some color-contrast cases behind dynamic styles).
