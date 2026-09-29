---
name: lcs-debug-ext
description: 'use this skill when the user asks for report-only debugging, evidence-based diagnosis, or a patch proposal without applying code changes for a bug, failure, error, broken behavior, flaky behavior, or performance regression. trigger especially for prompts like "make a debug report", "diagnose this but do not edit files", "propose a patch only", "investigate this bug without applying changes", or "why is this failing? create a report". do not trigger for general code review, security audit, feature implementation, broad architecture documentation, normal debugging that should update .lcs/work-items/{timestamp}-{slug-work-item}/debug.md, or direct patch application unless the user explicitly asks for report-only diagnosis.'
---

# LCS Debug Ext

Use this skill to investigate bugs with evidence first, then produce a report and patch proposal. The agent must not apply code changes.

## Core Contract

- Create generated artifacts only under `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/`.
- Before finishing, ensure `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/debug.md` exists.
- Do not write generated output to `.lcs/debug/`, `.aix/`, `docs/`, project root, source files, test files, instruction files, or skill files unless the user explicitly asks in a separate follow-up task.
- Do not modify source code, tests, config, docs, or instructions.
- Produce only a debug report, evidence summary, reproduction notes, ranked hypotheses, instrumentation suggestions, optional regression-test proposal, and patch proposal.
- Clearly state `Changes applied: None` in the report.
- Separate confirmed facts from hypotheses.
- Separate patch proposal from applied changes.
- Use `[TODO]` where evidence is missing.
- Use `[ASK USER]` where clarification or a user decision is required.

## Shared Contract

- Follow shared folder naming rules from `../lcs-shared/contract.md` and `../AGENTS.md`.
- For this skill, use a work-item folder ending in `-debug-ext`, for example `.lcs/work-items/20260529-143000-payment-timeout-debug-ext/`.
- End every generated report with the canonical Handoff footer.

## Inputs To Inspect

Use only available evidence from the user, repository, or commands the user permits. Inputs may include:

- Current user description.
- Error messages, stack traces, logs, traces, HAR files, screenshots, or test output.
- Failing command, reproduction steps, fixture input, request payload, or environment details.
- Relevant source files, folders, recent diffs, issue descriptions, or pull request diffs.
- Project references such as `.lcs/work-items/`, `.lcs/codebase/`, `.lcs/rules/`, `AGENTS.md`, `README.md`, or user-provided references.

If references are provided, inspect them before forming hypotheses. If evidence is insufficient, create a limited report with `[TODO]` and `[ASK USER]` rather than guessing.

## Workflow Checklist

- [ ] Phase 1: Collect context and create `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/`
- [ ] Phase 2: Build or identify a lightweight feedback loop
- [ ] Phase 3: Reproduce or characterize the failure
- [ ] Phase 4: Generate ranked falsifiable hypotheses
- [ ] Phase 5: Propose targeted instrumentation
- [ ] Phase 6: Produce patch proposal and regression-test options
- [ ] Phase 7: Generate `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/debug.md`
- [ ] Phase 8: Cleanup guidance and post-mortem

## Phase 1: Collect Context

1. Create the output directory: `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/`.
2. Choose a concise slug from the reported symptom, using lowercase `a-z0-9-`.
3. Identify available evidence before proposing causes.
4. Preserve the distinction between user claims, observed output, and code evidence.
5. If there is not enough evidence to diagnose, still produce the report with missing evidence clearly marked.

## Phase 2: Feedback Loop First

Try to identify the fastest repeatable pass/fail signal before speculation. Prefer:

1. Existing failing test.
2. Small targeted test command.
3. CLI invocation with fixture input.
4. HTTP request against a local or dev server.
5. Minimal script or harness that exercises the failing path.
6. Manual reproduction checklist.
7. Human-in-the-loop notes using `scripts/hitl-loop.template.sh`.

The loop should be fast, specific, repeatable, and focused on the reported symptom. Do not require heavy flaky-loop stress testing by default. For non-deterministic bugs, prefer 3-5 lightweight runs, record reproduction confidence, and present heavier stress strategies only as optional follow-up.

If no useful feedback loop exists, stop claiming progress. Record what is missing and ask for the smallest useful artifact, such as logs, stack trace, failing command, input sample, HAR file, screen recording, or environment access.

## Phase 3: Reproduce Or Characterize

Confirm and document:

- Exact observed symptom.
- Whether the symptom matches the user-described bug.
- Reproduction status: Reproduced, Partially reproduced, Not reproduced, or Evidence-only.
- Command, test, request, input, or manual scenario used.
- Expected behavior and actual behavior.
- Evidence captured.
- Confidence level: High, Medium, or Low.

If reproduction is unavailable, characterize from evidence and mark confidence as Low or Medium.

## Phase 4: Ranked Falsifiable Hypotheses

Before proposing a fix, generate 3-5 ranked hypotheses when enough evidence exists. Each hypothesis must include:

- Hypothesis name.
- Why it is plausible.
- Supporting evidence.
- Evidence that would disprove it.
- Predicted observation.
- Confidence level.

Use this form:

```text
If <X> is the cause, then <Y observation> should be true, and <Z check> should confirm or disprove it.
```

Avoid anchoring on the first plausible cause. If fewer than 3 useful hypotheses exist, explain why.

## Phase 5: Targeted Instrumentation

For each major hypothesis, propose one targeted check. Change one variable at a time. Prefer:

1. Debugger or REPL inspection, if available.
2. Focused logs at boundaries that distinguish hypotheses.
3. Targeted assertions.
4. Minimal test or harness.
5. Diff against known-good behavior.
6. Config or environment comparison.

Every temporary debug log proposal must use a unique prefix, for example `[DEBUG-lcs-7f3a]`. Include the prefix and cleanup command in the report:

```bash
grep -R "\[DEBUG-lcs-7f3a\]" .
```

Avoid broad "log everything" strategies.

## Phase 6: Patch Proposal And Regression Options

Do not apply patches. Produce a patch proposal containing:

- Suspected root cause.
- Files likely affected.
- Code-level change summary.
- Before/after snippet if available.
- Unified diff if enough context is available.
- Risk rating.
- Validation command.
- Rollback note.

Regression tests are options, not unconditional requirements. Present one recommended option:

1. Recommended regression test, when a correct test seam exists.
2. Lightweight smoke test, when full regression coverage is too heavy.
3. No good test seam found, when architecture makes testing unsafe or misleading.

Explain why the option was selected.

## Phase 7: Generate Report

Use `references/report-template.md` when writing `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/debug.md`.

The report must include:

- Bug summary.
- Available evidence.
- Reproduction status.
- Feedback loop status.
- Exact observed symptom.
- Ranked falsifiable hypotheses.
- Investigation notes.
- Proposed patch.
- If the bug implies a product/behavior requirement, include a `## Source Requirement Ledger` with stable `SRC-###` IDs (P0/P1/P2) so downstream `lcs-toprd` can carry it into the PRD without loss.
- Optional regression-test options.
- Cleanup checklist.
- Post-mortem.
- Open questions.
- Limitations.
- Handoff.

## Phase 8: Cleanup And Post-Mortem

Before finalizing, verify:

- `.lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/debug.md` exists.
- No code changes were applied.
- No source files were modified.
- Any proposed debug prefix is documented.
- Cleanup guidance exists.
- Patch proposal is clearly marked as not applied.
- Regression-test options are included.
- Post-mortem is included.
- Handoff footer is present.

## Handoff Behavior

If the bug appears caused by broader design or architecture issues, recommend a follow-up rather than trying to solve architecture inside this skill.

Possible follow-ups:

- Use `lcs-codebase-doc` if codebase structure or architecture is not sufficiently understood.
- Use an architecture-improvement workflow if available.
- Use `lcs-self-improvement` if the debugging workflow revealed repeated agent/user friction.
- Ask the user which follow-up path to take if no obvious target exists.

Handoff footer format:

```markdown
## Chain of Truth Report
### Level
Very Strict

### Sources Checked
- All inputs, files read, commands run with paths and line numbers
- <exact line references for all quoted content>

### Assumptions
- <label each [verified] or [unverified]>

### Plan
<Enumerated steps>

### Actions Taken
- <Exact commands run with stdout/stderr captured>

### Verification
- <All test and lint commands run; results quoted verbatim>

### Report
<Blocked items listed explicitly; confidence stated as high/medium/low with justification>

## Handoff
Next recommended skill: <skill-name>
Next file to read: .lcs/work-items/{timestamp}-{slug-work-item}-debug-ext/debug.md
Current phase: debug
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <short>
Source of Truth Bundle: .lcs/state.md, debug.md
Must Preserve IDs: SRC-001, SRC-002, ... (from Source Requirement Ledger)
Unresolved IDs: <list or None>
Suggested next command: <command>
```

## Chain of Truth Level

Level: Very Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
