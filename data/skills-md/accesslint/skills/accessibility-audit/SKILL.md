---
name: accessibility-audit
description: "Whole site or product — a full web accessibility (a11y) audit against WCAG 2.2, following the WCAG-EM methodology. Defines scope, samples representative pages and flows, runs the automated tier (`accessibility-scan`) and the hands-on manual tier (`accessibility-inspect`), and produces one conformance report. Grades each finding by severity and evidence basis, and states per-criterion conformance as pass, fail, or undetermined (needs a human). Use it for 'audit my site for accessibility', 'is this product accessible', 'a11y audit', 'WCAG or Section 508 conformance report', or any multi-page assessment. Assesses; does not fix (use `accessibility-fix`) or diff (use `accessibility-diff`). For a single page use `accessibility-scan`; for hands-on keyboard and screen-reader checks use `accessibility-inspect`."
argument-hint: "[target|url] [--level AA|AAA] [--selector <css>]"
allowed-tools: Read, Glob, Grep, Bash, Skill, Task, mcp__plugin_accesslint_accesslint__list_rules, mcp__plugin_accesslint_accesslint__explain_rule
---

This is a full WCAG 2.2 accessibility audit using WCAG-EM. It defines scope, samples representative pages and flows, runs both evaluation tiers, and produces one conformance report:

- Automated tier: `accesslint:accessibility-scan` (the rule engine).
- Semi-automated manual tier: `accesslint:accessibility-inspect` (keyboard, focus, state, reflow, and the rest the engine can't decide).

Assess; don't fix (`accesslint:accessibility-fix`) or diff (`accesslint:accessibility-diff`). One page with no sampling is a `accessibility-scan`, not an audit. This skill delegates each sampled page to its own subagent (step 4), so it stays light on large samples.

The full doctrine — WCAG-EM in detail, the severity rubric with examples, the no-proxy boundary, grounding — is in [`../shared/methodology.md`](../shared/methodology.md). The rules needed to run this skill are below.

## Grading

Each finding carries a severity and an evidence basis. Keep them separate.

- Evidence basis: ● verified (deterministic, with cited proof) · ◐ flagged (evidence captured, a person decides) · ○ human-required (needs assistive technology or lived experience; handed off, not emulated).
- Severity: critical (blocks a core task) · serious (major barrier) · moderate (friction, still completable) · minor (polish).

## WCAG-EM steps

Run in order and state what you did at each.

1. Scope. State the target and its boundary, the goal (default WCAG 2.2 AA; `--level AAA` adds AAA), the technologies in use, and the assistive-technology baseline the human handoff should cover. You scope that baseline; you don't test it.
2. Explore. Use Glob/Grep to find routes, templates, and shared components. Note key flows, content types, and stateful UI (modals, wizards, empty and error states). `accesslint.config.json` targets are a starting point.
3. Sample. Choose a structured set (entry page, each key flow end to end, every page with a new template or complex widget, and the important states) and a small random set. Say what's in each and why.
4. Evaluate. Delegate each sampled page or state to its own `Task` so it runs in its own context and returns its findings; independent pages can run in parallel. Each Task:
   - runs `accesslint:accessibility-scan` (`--format json`) first, then `accesslint:accessibility-inspect` against the same rendered state — same URL, `--selector`, `--wait-for` — passing scan's results (or at least the list of SCs the engine covered) into the inspect run;
   - dedups by SC ownership **before driving, not after**: `accessibility-scan` owns rule-detectable criteria, `accessibility-inspect` owns interaction and judgment criteria; inspect never re-checks an engine-owned SC, and where both still cover the same SC at the same element, `accessibility-scan`'s result wins;
   - returns a structured block: per finding, the SC, severity, evidence basis (●/◐/○), location, tier, evidence, and fix or handoff, plus this page's per-SC ledger (verified / flagged / engine-owned / N/A / not exercised).

   Aggregate the returned blocks in step 5. For a one- or two-page scope, run the tiers inline instead of spawning a `Task`.

   A shared browser is optional and improves selector matching across tiers, but it's a pre-wired precondition, not something this skill sets up at runtime: the browser MCP binds to its Chrome at server start (`--autoConnect` or `--browser-url`), with the engine pointed at the same port. Without it (the default), each Task runs both tiers against the same URL and `--wait-for` gate and dedups by SC ownership.
5. Report. Aggregate into the format below. Conformance has three states: pass or fail only for ● findings; everything ◐ or ○ — and every SC no page exercised — is undetermined and goes to a human. One sampled page failing an SC fails it for the whole scope at that level. Don't report conformance you can't support, and don't let a not-exercised SC read as a pass. Keep the ledger to counts and bare SC lists — group undetermined SCs by shared reason, one clause per group — and spend the report's words on failures, flags, and handoffs: a pass is its SC number in the list, with at most one sentence of narration for the whole passing set.

## Report format

```
# Accessibility audit — <product / scope>
WCAG 2.2 Level AA · WCAG-EM · <N> pages/states sampled

## Scope
- Target & boundary: <…>     Goal: WCAG 2.2 AA
- Technologies in use: <…>
- AT baseline (for the human handoff, not tested here): <SR+browser pairs, keyboard-only, …>

## Sample
- Structured: <page/state> — <why>   (×N)
- Random: <page/state>

## Conformance (per success criterion)
- Pass ●: <n>  ·  Fail ●: <n>  ·  Undetermined (◐/○/not exercised): <n>  ·  N/A: <n>
- Fail ●: <SCs>   Pass ●: <SCs>   N/A: <SCs>
- Undetermined: <SCs (shared reason)> · <SCs (shared reason)>
- Pass/fail is asserted only for ● criteria; ◐/○ and not-exercised are undetermined.

## Findings — by severity, tagged by evidence basis
### Critical
- [●] <barrier> — SC x.x.x — where: <selector / file:line> — tier: scan|inspect — → `accessibility-fix`
- [◐] <barrier> — SC x.x.x — evidence: <screenshot / measurement> — confirm: <what a person checks>
### Serious / Moderate / Minor
[same shape]

## Human-required (○) — the testing handoff
- <what only AT or lived experience reveals> — SC x.x.x
    needs: <functional ability + AT, per Section 508 FPC>   flow: <sampled flow>

## Recommendations
- Root-cause / pattern fixes (one change that clears many instances) → hand to `accessibility-fix`.
- What to send to human and AT testing, and on which flows.
- Wire `accesslint:accessibility-diff` into CI for the sampled targets.
```

## Notes

- Assess, don't fix (use `accessibility-fix`) or diff (use `accessibility-diff`). Don't emulate human experience: usability is ◐, lived experience is ○ and handed off.
- Conformance is per SC across the whole sample. Don't average failures away.
- Two browsers can drift selectors; prefer a shared browser for ●-precision, otherwise note that dedup is best-effort.
- State what wasn't covered (pages outside the sample, ○ criteria). Omitting it reads as "all clear".
- Use `list_rules` and `explain_rule` for engine-rule metadata.
