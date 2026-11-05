---
name: visual-testing
description: Use when rendered UI needs visual regression checking — "did the UI change", "visual test", "screenshot diff", "compare against the baseline", "catch layout regressions", or a visual assertion in a test run. Works on any HTML you can render — a generated static page (design mock, report, flow-map poster) opened from disk, or a running app driven by your existing browser/device automation. Screenshots each screen, diffs it against a committed baseline with reg-cli (MIT, no cloud), and reports what changed as an HTML report plus a pass/fail summary. Capture rides on whatever browser or device tool you already have — no separate headless engine is installed. NOT a functional or correctness check (a diff proves pixels moved, not that anything is right), and a red diff is a prompt to look, not an automatic verdict.

---

# Visual testing

Catch **unintended** visual change. Rendered UI is deterministic enough that a pixel
which moved without an intended cause is worth seeing — a card that lost its shadow,
a table that overflows on tablet, a button that drifted but still works. This skill
screenshots each screen and diffs it against a baseline captured when the UI was
last correct.

Two halves, kept separate on purpose:

- **Capture is agent-driven.** You open the thing under test in whatever browser or
  device tool you already have and save a PNG. No headless browser is bundled or
  installed — capture rides on the tooling that already exists (a connected browser,
  a Playwright/Appium session, a running app's automation).
- **Diff is browser-free.** `scripts/visual-diff.mjs` shells out to `reg-cli`
  (resolved local-first, else `npx --yes reg-cli@latest`, so nothing is added to
  `package.json`) to compare, manage baselines, and write a report.

## Workflow

1. **Render the thing under test.**
   - A generated static page → build it, then open the HTML from disk (`file://`);
     the pages are self-contained, no server needed.
   - A running app → drive it to the screen/state with the automation you already
     use (Playwright for web, the device tooling for mobile). This is the same
     navigation a functional check performs — the visual diff is an extra assertion,
     not a separate run.
2. **Capture** each screen into a `current/` directory, one PNG per variant, named
   by the scheme below. See `references/capturing.md` for driving each source and
   controlling the noise that makes diffs flaky.
3. **Diff** against the baseline:
   ```bash
   node scripts/visual-diff.mjs --current <current/> --baseline <baselines/> --diff <out/>
   ```
   Exit `0` = no change; exit `1` = something changed (report at `<out/>/report.html`).
4. **Review the report.** An **intended** change (a redesign, a shipped restyle) →
   promote it:
   `node scripts/visual-diff.mjs --current <current/> --baseline <baselines/> --diff <out/> --update`
   then commit the updated baselines. An **unintended** change → a finding: fix the
   cause (or file the defect with the diff image); do not update the baseline.

**A green diff is not a passing test.** It proves the screen is unchanged since the
baseline — nothing about whether that baseline was ever correct or whether the
feature works. Use it to hold a *reviewed* UI steady, alongside the checks that judge
correctness, never instead of them.

## Naming (this is what pairs a shot with its baseline)

`reg-cli` matches `current/<name>.png` to `baselines/<name>.png` by filename, so
names must be stable and describe exactly one variant. Pick a scheme that fits what
you're testing and keep it lowercase and stable; examples:

| Context | Filename |
|---|---|
| design mock (mobile) | `screen-<flow>-<screenId>-<state>-<device>.png` |
| design mock (web) | `screen-<flow>-<screenId>-<state>-web-<style>-<bp>.png` |
| running web app | `web-<screen>-<state>-<viewport>.png` |
| running mobile app | `mobile-<screen>-<state>-<device>.png` |
| flow-map / poster | `flow-<flowId>.png` |

Renaming a file breaks its baseline pairing — reg-cli then reports one *deleted* +
one *new*, which is the signal to re-approve, not a bug.

## Keep the baseline set honest

Screens × states × sizes/styles is a combinatorial trap. Default coverage: the
screens actually touched, in their default state, at the size/device set you target,
in one representative variant. Add more only where a real regression risk lives.
Every variant is a baseline someone re-approves on every intended change — a giant
set nobody re-approves is worse than a focused one people actually look at.

## Files

| Path | What it is |
|---|---|
| `scripts/visual-diff.mjs` | The reg-cli wrapper: build args, local-or-npx, read the JSON report, summary + exit code. `--update` promotes current → baseline. |
| `references/capturing.md` | Driving each source (static page / running app), the naming scheme, and taming the noise that makes diffs flaky. |
| `references/baselines.md` | Where baselines live, the promote/approve flow, what to commit, reading the report. |
