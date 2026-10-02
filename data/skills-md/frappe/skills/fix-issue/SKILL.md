---
name: fix-issue
description: Fix a bug reported in a GitHub issue or a markdown file, without letting the report's noise and guesses into the main context. Takes an issue number, an issue URL, or a file path as an argument. Use when asked to fix, investigate, or reproduce a reported bug.
disable-model-invocation: true
---

# Fix a reported issue

A bug report is not a specification. Read the reporter's guesses and you inherit them: you
look where they looked, and you stop when the symptom stops. A subagent reads the report
and returns only the observable facts. You form your own hypothesis from the code.

**Never read the issue yourself** — no `gh issue view`, no `WebFetch`, no `Read` on the
file, not even later to check a detail. If the extract is thin, `SendMessage` the
extractor agent; its context still holds the report.

## 1. Extract the facts

Spawn one `general-purpose` agent, `run_in_background: false`, passing the argument
through unchanged:

> Read the bug report at <ARGUMENT>. For a GitHub issue use `gh issue view <n> --comments`.
> For a path, read the file.
>
> Return a factual brief. Your output is the only thing the engineer will see.
>
> Include, each only if the report states it:
> - **Symptom** — what the user observed, one or two sentences.
> - **Expected** — what they expected instead.
> - **Reproduction** — exact steps, inputs, data. Verbatim, never shortened.
> - **Evidence** — errors, tracebacks, logs, response bodies. Verbatim and complete.
> - **Environment** — version, branch, database, browser, deployment type.
> - **Scope** — always or intermittent, one user or all, when it started.
>
> Exclude: any proposed fix, patch, or PR link; any guess at the cause or any file,
> function, or commit the reporter suspects; "I think" / "probably" / "it looks like"
> clauses; severity, urgency, blame, +1s, greetings, bot comments; repeated restatements
> of the symptom.
>
> A traceback is evidence — keep it, though it names files. A commenter writing "the bug
> is in x.py" is a guess — drop it.
>
> End with **Gaps**: what a reproduction needs that the report does not give. "none" if
> complete.
>
> Do not read the codebase, verify anything, or offer an opinion. Under 400 words plus
> verbatim blocks.

## 2. Reproduce before you fix

Reproduce the symptom from the brief. Three outcomes end the work here, and each is a
valid result to report: cannot reproduce and the brief lists gaps; cannot reproduce and
the brief is complete (search the log for a commit that already fixed it); or it
reproduces but the behaviour is correct.

## 3. Find the cause yourself

Work backwards from the failure through the code. The report told you where the symptom
surfaced, not where the defect is. Fix the cause; if you can only reach the symptom, say
so rather than patching it in silence.

## 4. Fix and verify

Smallest change that removes the cause — no refactors, no adjacent fixes. Add a regression
test that fails without the change and run it both ways, then the surrounding test module
and `pre-commit run --files <changed files>`.

## 5. Review in a separate agent

Spawn one `general-purpose` agent, `run_in_background: false`:

> Load the `frappe-code-review` skill and review the working diff (`git diff` plus any
> untracked files it adds). The change is meant to fix this bug:
>
> <paste the Symptom and Expected lines from step 1>
>
> Judge two things: does the change stop the bug at its cause or mask the symptom, and the
> skill's checklist. Report only findings worth acting on, most serious first — file and
> line, what breaks and for whom, the fix. No summary of the diff. If nothing is worth
> acting on, say so in one line.

Act on the findings and re-run the tests.

## 6. Report

Four to six lines: the cause, the change, the test, the review outcome, anything
unresolved. Commit only if asked; if you do, load `technical-writing` for the message and
add no co-author trailer.
