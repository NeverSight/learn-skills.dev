---
name: accessibility-fix
description: "Remediation only — repair web accessibility (a11y) violations against WCAG 2.2 with a baseline, edit, and verify loop. Takes a target (URL, files, directory) or a findings worklist from `accessibility-scan`/`accessibility-inspect`/`accessibility-audit`, applies mechanical fixes as given, leaves TODOs for visual or contextual judgment, and verifies by re-running the baseline check. It only fixes. To find issues use `accessibility-scan` (one page, automated), `accessibility-inspect` (one page, manual), or `accessibility-audit` (whole site, WCAG-EM); to check for regressions use `accessibility-diff`. Use it for 'fix the a11y issues in X', 'make this accessible', 'add missing alt text and labels', 'apply these accessibility fixes', 'remediate these violations'."
argument-hint: "[target|url|report]"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Skill, Task, mcp__plugin_accesslint_accesslint__audit_html, mcp__plugin_accesslint_accesslint__audit_live, mcp__plugin_accesslint_accesslint__explain_rule, mcp__plugin_accesslint_accesslint__list_rules
---

This skill remediates accessibility violations: baseline, edit, verify. It only fixes. To find what's wrong, use `accesslint:accessibility-scan` (one page, automated), `accesslint:accessibility-inspect` (one page, manual), or `accesslint:accessibility-audit` (whole site, WCAG-EM); to check for regressions, use `accesslint:accessibility-diff`. The engine runs here are internal to the loop — a baseline before and a check after — not a report.

Shared conventions (grounding, never invent content): [`../shared/methodology.md`](../shared/methodology.md).

For large remediations, run via `Task` for context isolation; the steps are the same.

## Input

- A findings worklist (from `accessibility-scan`, `accessibility-inspect`, or `accessibility-audit`, or pasted): apply it directly; the baseline is already done.
- A target (URL, config target name, files, or a directory): audit it first for the baseline, then fix.

Given neither, ask what to fix. Don't sweep a whole codebase unprompted.

## Picking a flow (for baseline and verify)

1. `audit_live` for any URL. It ensures a debuggable Chrome (auto-launches a headless one if none is reachable) and audits the live DOM. Use `selector` to scope and `wait_for` for async content. The live DOM catches what source can't.
2. `audit_html` for raw HTML strings, files (`Read` first), or JSX rendered to a string.

For an authenticated session, have the user start a headed debuggable Chrome (`npx @accesslint/chrome ensure --headed`), sign in, then call `audit_live({ url, port })` to attach to it.

## Steps

1. Baseline. Audit with `format: "compact"` and record the violation set (rule ID and selector for each). Skip this if you were handed a worklist.
2. Apply. For each violation:
   - If a `Source:` line is present, open that file at that line. If several are listed (separated by `←`), the first is the JSX literal and the rest are enclosing components; use `Symbol` to disambiguate.
   - If not, grep stable hooks (`data-testid`, `id`, `aria-label`), then visible text, then tree position.
   - Use the `Fixability:` and `Fix:` fields: apply `mechanical` fixes as given; leave a `TODO` with the rule ID for `contextual` or `visual`. Don't invent content (alt text, labels, link text).
   - Group edits to the same file into one operation.
   - Confirm scope before editing files outside the obvious target, or before more than about 10 mechanical fixes.
3. Verify. Re-run the same audit and compare to the baseline: every targeted violation gone, no new ones. For a precise new/fixed/pre-existing comparison on a URL, use `accesslint:accessibility-diff` rather than checking by eye.

`Source:` lines come from React DevTools fibers and appear only in live-DOM audits against React dev builds. Static audits won't have them; fall back to selectors. When unsure about a rule, use `explain_rule({ id })`.

## When to stop

- A violation with no `Fix:` directive: leave a `TODO`, don't guess.
- Verification fails (a new violation appeared, or a targeted one remains): report it and stop. Don't iterate silently.

## Output

Per cycle: the flow used, violations by impact, what was applied (file and rule), what was deferred (TODOs and why), and the before and after counts.
