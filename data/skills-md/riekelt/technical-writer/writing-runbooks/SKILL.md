---
name: writing-runbooks
description: Use when writing operational documentation - runbooks, setup guides, release procedures, migration guides, deprecation guides, troubleshooting entries, or any ordered procedure someone will execute under time pressure. Encodes the runbook skeleton, the risk legend, the symptom-first troubleshooting format, and the migration-guide rules (mapping table, mandatory rollback, deprecation dates, built-in expiry). Use whenever someone will execute the text, even if it is called a "guide" or "setup notes".
---

# Writing runbooks

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

The reader is in a hurry, often mid-incident. Every runbook is ordered, one action per step, copy-pasteable, with danger marked where the eye already is.

Write from a real run: every step one actually taken, every failure named one that actually happened. A procedure imagined at the desk is a draft, not a runbook. A partially exercised procedure may be published with per-branch honesty: name the variant that has not run yet, mark that branch draft, and ask its first real runner to report back. A procedure with no real run behind any branch is a draft outright. When a value the commands need is genuinely unknown, keep the placeholder visibly bracketed, never invented, and fill it from a real run before publishing; truth outranks paste-readiness.

## When to invoke, and not

Invoke for anything a person will execute: runbooks, setup and release procedures, troubleshooting entries, operational checklists, and the operator-facing strings inside a system. Do NOT invoke for design rationale (`writing-design-docs`) or for reference material nobody executes. If the procedure has not been run at least once, either run it first or label the document a draft; publishing an untested procedure as a runbook is the defect, not the labeling.

## Structure

- Title carries the scope: "MVP runbook (Reddit)", "Release runbook".
- Open with what this document is relative to its siblings ("this doc is the sequence; deep detail per step lives in X") and state what it does NOT cover.
- **Legend up front** when steps differ in risk, applied to every command: safe to run anytime / operator-only (writes to production) / manual step outside the terminal. Tags combine where a step is more than one thing.
- **TL;DR happy path first**, then the same steps as numbered sections for the reader who needs only one.
- Version-pinned prerequisites before any command, each with a check command.
- Numbered ordinal steps (not bullets), one action each, present tense or imperative, with a visible actor.
- Every command copy-pasteable as-is, with concrete example values ("common paths: `/public_html/`, `/www/`"). Label variants inside the code block:

```bash
# safe mode
app sync run --channel=reddit --limit=100

# live mode (writes to the provider)
app sync run --live --approval-token=...
```

- Ordered steps state the consequence of wrong ordering inline: "deploy jar, then DB cleanup; wrong order = silent data loss."
- Every state-changing procedure names its rollback, or states plainly that none exists and what that means.
- End with a "verify it worked" section: the observable end state and the command that proves it.
- Mark the preferred path "(recommended)" when several paths exist; document UI and CLI for the same task side by side rather than twice.
- If the runbook will shrink when tooling lands, say so: "when X lands, steps 2 to 4 become one command and this document keeps only the judgment."

## Troubleshooting entries

Symptom-first:

```markdown
## <symptom as the user sees it>
**Symptom**: verbatim error strings (searchable)
**Cause**: ...
**Fix**: exact commands
```

Order diagnostic steps cheapest first. Group entries by failure class. Cross-link the deeper doc instead of inlining it.

## Migration and deprecation guides

A migration guide is a runbook whose subject is the change itself: everything above applies, plus five rules of its own. The argument for the migration is a design doc (`writing-design-docs`), the decision to deprecate is an ADR (`recording-decisions`), the announcement is a changelog entry (`writing-changelogs`); this section covers only the guide the reader executes.

1. **History is the content here, stated positively.** The before/after comparison is the job, not a violation: this is the document class the no-history hard rule explicitly carves out. Write "the tag now replaces the manual version bump" freely; that sentence is banned everywhere else and load-bearing here.
2. **The mapping table is the core artifact.** Old to new per behavior, config key, command, or API, one row each. Prose explains the rows that need it; the table carries the migration.
3. **Rollback is mandatory, per step.** Every step names its undo, or states plainly that it is irreversible and what that means for the ordering around it.
4. **The deprecation contract carries dates.** What stops working, on which date, what happens to stragglers, and where the escape hatch is until then. "Will be removed in a future release" names no date and is banned here.
5. **Born with an expiry.** When the migration completes, the owner reclassifies the guide as historical and adds the superseded banner pointing at the current-state documentation, never deleting it silently. State the completion condition in the guide itself.

## Operator-facing strings

Error messages and log lines are runbook prose with the shortest reading window: keep remediation specific and actionable, and make error states visible rather than letting workflows appear healthy.
