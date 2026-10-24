---
name: allure-agent-mode
description: Write, review, debug, and improve tests with Allure agent mode by preserving useful coverage, planning scope, creating per-run expectations, running targeted tests, inspecting existing Allure results or dumps from local or CI runs, reviewing runtime evidence, and enriching weak test evidence. Use whenever you author, modify, or review tests — including as a step inside a larger feature, bug-fix, or implementation task, not only when test work is the headline request; load it before writing assertions rather than authoring from general knowledge.
---

# Allure Agent Mode

Use this skill for feature or bug work that changes tests, for reviewing existing tests, auditing coverage, triaging failing suites, investigating weak evidence, or debugging flaky and environment-sensitive failures.

## Why Agent Mode

A test run is an instrument, not a pass/fail to scrape. Running tests through `allure agent` turns any run into a reviewable account of what actually happened — the steps, HTTP exchanges, SQL, browser sessions, and attachments — plus automated findings about the tests themselves, such as a test that ran with no assertions or an API call with no evidence it was made. The console gives you a status; the agent output gives you understanding and a critique, and a report a human can actually review. Reach for it because it makes the work better.

- **Run with intent.** `allure agent --goal "<what this run should confirm>" -- <test cmd>`. Recent `allure agent` prints a run summary to stdout — counts, findings with severity, expectation result, the report link, and pointers into the output — so the headline reaches you without opening a file (a `--silent` option is available to quiet passthrough noise; confirm its effect with `allure agent --help`). Read that summary, then open the agent output for depth: the output dir's `AGENTS.md` guide, `index.md`, the findings, and the per-test evidence. The report carries the goal next to the evidence, so you, an upstream agent, or a human can validate the run against what it was meant to prove.
- **Make evidence checkable with expectations.** When a behavior must be proven — an API call, an attachment, a step — add the matching `--expect-*` option. Missing expected evidence is a finding, not a pass: it means you cannot be sure the behavior was exercised.
- **Triage failures without the hunt.** The output names the exact failures with enough context to fix in place. Confirm flakiness by rerunning just the failed tests through agent mode — `allure agent --rerun-latest` (or `--rerun-from <prior-output>`, recovering it via `allure agent latest`) with the matching `--rerun-preset`, so you need not remember the test name or this framework's filter syntax. Confirm the exact flags with `allure agent --help`. Don't rerun blind or scrape logs.
- **Debug from CI without local repro.** Run `allure agent inspect` on downloaded `allure-results` to get the same review surface with full context — often enough to fix a failure you cannot reproduce locally (a Windows-only failure from a Mac).
- **Use tests as a debugging instrument.** A test already sets up the environment, exercises the behavior, and captures the evidence — reach for the relevant test under agent mode instead of ad-hoc bash or driving a browser MCP by hand.
- **Learn the real surface.** Run `allure agent capabilities` to see what the local CLI actually supports instead of assuming.

The run already prints a summary digest to stdout — read it, then open the full output. Reducing the run with `tail`/`grep`/`head` or `>/dev/null`, or stopping at the printed counts, throws the rest away: the findings, the evidence, sometimes whole test binaries. The agent output is the signal.

## Read First

If the project has `docs/allure-agent-mode.md`, read it before writing or reviewing tests.

If it does not, use the guidance in this skill and suggest using `$allure-configure-agent-workflow` later.

Read `references/test-design.md` before adding, changing, deleting, skipping, suppressing, or reviewing tests.

Read `references/allure-evidence.md` before adding, reviewing, or fixing Allure steps, attachments, parameters, labels, descriptions, or weak evidence findings.

Read `references/expectations.md` before creating or evaluating Allure agent expectations. Confirm the local expectation mechanism through the project guide or `allure agent --help`.

## Workflow

1. Understand the feature, issue, or review goal and decide the intended test scope.
2. Decide whether expectation controls reduce a real risk for this run. When they do, create the smallest fresh expectations supported by the local Allure agent.
3. Write or update the tests using test-design rules, or keep the current tests unchanged if the task is review-only.
4. When executing tests yourself, run only the intended scope with `allure agent` before relying on raw console output.
5. When investigating an execution that already emitted raw Allure results or dump artifacts, prefer a locally confirmed `allure agent inspect` flow to create agent-readable output from those artifacts before parsing raw logs or generated HTML reports.
6. For iterative agent-only loops, prefer `--report off` when supported. For a final validation or user-facing review run, prefer `--report auto` or force the appropriate HTML report mode, then share the generated report link when one exists.
7. Print the run or inspected output's `index.md` path so collaborators can open the overview quickly.
8. Review `index.md`, `manifest/run.json`, `manifest/test-events.jsonl`, `manifest/tests.jsonl`, `manifest/findings.jsonl`, `manifest/expected.json` when the run used expectations, and the relevant test markdown files before inspecting source code.
9. If evidence is weak, enrich the tests with real steps, attachments, or minimal metadata.
10. Confirm the run is a trustworthy signal: the selected profile fits the goal, important tests are not silently excluded, and any non-gating local or CI signal is called out.
11. Rerun with a fresh agent output directory and fresh expectations when expectation controls are still justified for the same intended scope. Use the CLI-provided temp output unless a specific path is needed.
12. Accept only when scope matches, coverage remains meaningful, evidence is good enough to review, execution limitations are explicit, and any partial runtime modeling has been called out.

## Task Variants

These are the main Workflow scoped to a task, not separate procedures — the same run-then-review-the-agent-output loop applies. (Failure debugging is already the **Triage failures** loop above; for CI failures, `allure agent inspect` downloaded results rather than reproducing locally.)

- **Small test change.** Run only the touched scope through `allure agent` — a smoke check still goes through agent mode, even after a mechanical change such as typing cleanup or a mock refactor — review the agent output, and only then make a regression-safety or correctness statement.
- **Test authoring.** Read `references/test-design.md` and `references/allure-evidence.md` first; write or change the test, run the touched scope with a `--goal`, then review the findings and evidence — not just pass/fail — and enrich weak steps, attachments, or metadata before rerunning with fresh output.
- **Coverage review.** Split a command or package audit into scoped groups, each with distinct agent output and expectations only when the group has a known scope. Run each group, review runtime artifacts before source, and mark the review incomplete until every group is validated through matched expectations, reviewed observed scope, or explicit broad package-health documentation.

Compact coverage-review pattern:

```bash
npx allure agent \
  <report mode: --report off for iterative loops, auto/awesome/config for final runs> \
  <minimal local expectation options when justified> \
  -- npm test -- <scope>
```

Before running, decide what should run, what should not, why that scope is enough, and whether an expectation option would catch a real mistake. Use the CLI-provided temp output by default; add `--output <path>` only when a specific path is needed.

## Requirements

- Full agent-mode runtime evidence requires Allure CLI `allure@3.11.0` or newer with `allure agent`.
- Before relying on agent-mode conclusions, confirm the local project wrapper supports `allure agent` and is not below the minimum version. If the wrapper reports an older version, warn the user and treat agent-mode evidence as unavailable or incomplete until the CLI is upgraded.
- Existing-result inspection requires local `allure agent inspect` support, available in `allure@3.12.0` and newer. Confirm it through the project wrapper with `allure agent capabilities --json` and `allure agent inspect --help`.
- Use `allure agent inspect [<allure-results-dir-or-glob> ...]` for local or downloaded `allure-results` directories, and repeated `--dump <archive-or-glob>` for dump archives created by `allure run --dump`.
- Use `--report auto|off|awesome|config` when controlling optional report generation. The default `auto` mode may write an HTML report at `awesome/index.html` and `manifest/human-report.json` inside the agent output when the stored result count is within the local CLI threshold.
- Use `--report off` for private iterative loops unless the user needs an HTML report for that run. For final validation or handoff runs, prefer `--report auto`; use `--report awesome` to force the single-file Awesome report, or `--report config` when the project-configured report plugins should run.
- When `allure agent inspect` is unavailable or cannot consume the artifact shape, prefer an advanced fallback that generates a temporary Allure config enabling only the `agent` plugin, then run `allure generate --config <generated-config> --output <agent-output> <results...>` with repeated `--dump <archive-or-glob>` as needed. Treat that explicit `<agent-output>` as caller-managed cleanup.
- If neither `agent inspect` nor the generated agent-only config fallback is usable, inspect raw Allure results, dump contents, or logs only as a weaker fallback. `allure log <allure-results>` is a local console fallback for result folders when supported, but it is not agent output.
- Agent-mode runs need unique output. Modern `allure agent` creates and prints a temp output directory when no output is provided; use that default unless a specific path is needed. In `allure@3.12.0` and newer, each `allure agent` run removes the previous run's CLI-provided temp output automatically, so default-output runs do not accumulate.
- Agent mode detects only the result files the current run produces, so clearing `allure-results` between runs is unnecessary — it picks up only the new results either way. Whether to clear or keep the framework results is the project's choice, not an agent-mode requirement.
- When using the default output location, get the generated directory from the agent output or a supported helper such as `allure agent latest` when available.
- When choosing a specific output directory, prefer the supported `--output` option. An explicit `--output` path is the one thing the agent must clean up itself — automatic cleanup never touches caller-provided paths — so remove or archive that `--output` directory when done. Use an output-related environment variable only if the local CLI help, wrapper, or official docs explicitly document one; the supported control on the current CLI is `--output`.
- Agent output, framework Allure results, and generated reports are separate artifacts. Do not use framework result settings such as `ALLURE_RESULTS_DIR` as agent-output controls.
- Do not add or override framework result directories in an agent command unless the project guide, runner config, installed help, official docs, or adapter README/source confirms it is required for this run. When a per-run result directory is needed, keep its final path component `allure-results` and ensure it is discoverable by the local Allure command.
- Never invent Allure environment variables from plausible names. If the exact variable or flag is not confirmed, use the documented `allure agent` option, leave the setting unknown, or ask to verify official docs.
- Runs that use expectations must use fresh expectations for the intended scope.
- Concurrent agent-mode runs must each pass their own caller-managed `--output` directory; they cannot rely on the default temp output, because each `allure agent` run clears the previous run's temp output and would clobber a parallel run's. Never share output paths or expectation state across parallel runs.
- After a final run that generates an HTML report, read `manifest/human-report.json` and resolve its recorded report path against the agent output directory before sharing it.
- In user-facing output, call the artifact simply the report and do not put the report target in inline code or a code block. Say `Here is the report: <link>` using a normal Markdown link to the absolute local report file, such as `[report](/absolute/agent-output/awesome/index.html)`, so Codex and similar clients can expose clickable or previewable affordances. Never link a relative manifest value such as `awesome/index.html` directly.
- Inspect `allure agent --help` before assuming specific expectation option names. Prefer inline options; use file-based expectations only as advanced mode for large, generated, or policy-controlled contracts.
- Do not add expectation flags defensively. If expectation controls are unavailable or not justified, review observed scope from the output and call out weaker scope checking.
- If a run, local command, or CI job is non-gating or excludes important tests by default, call that out before using it as proof.
- Metadata enrichment is part of this loop, not a separate workflow.

## Guardrails

- Runtime first, source second.
- Tests are behavior contracts; do not weaken assertions, skip tests, or delete coverage just to make the run pass.
- Keep tests boring and explicit. Prefer readable, stable, linear tests over conditional logic, loops, factories, or generated tests whose main value is saving a few repeated lines.
- Do not hard-skip tests with runtime `if` branches, early returns, conditional test registration, or helper aliases that hide coverage gaps; use runner-native skip, conditional-skip, or assumption mechanics with clear reasoning.
- Steps must represent real behavior, not filler.
- Do not wrap an entire test body in one manual step just to make Allure evidence non-empty.
- Attachments must come from the current execution.
- Keep metadata minimal and only add labels that help review or policy.
- Keep per-test intent metadata inline with the test: descriptions, labels, links, parameters, and intent-defining step names must be explicit at each test site.
- Prefer helper-boundary instrumentation over repetitive caller wrapping.
- Reusable helpers may handle mechanics, but must not centralize test intent in wrappers, lookup tables, or test-name mappings.
- If runner-visible failures are not represented as logical tests, inspect global stderr and treat the run as a partial runtime review.
- Do not present ignored, excluded, swallowed, or non-gating tests as a passing validation signal.
