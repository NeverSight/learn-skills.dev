---
name: audit
description: Reviews a change, a session or a whole codebase against every skill in this collection and returns one ranked, numbered report.
disable-model-invocation: true
---

# Audit

This skill reviews work against every rule in this collection at once. It sends each concern to the skill that owns it and merges the results into one ranked report.

## The report, not the rules

This skill owns no interface rule. It owns the scope, the order of review, consolidation and the verdict. Each finding cites the rule id from the skill that owns it. A finding needs evidence from the code, the running app or the thread, never taste alone.

The report format is in [report.md](report.md).

## 1. State the scope

Name what is under review: the uncommitted diff, a branch, a pull request, this session's requests or the whole codebase. An audit with no stated scope is `audit-state-the-scope`.

## 2. Read the project's rules

Read `AGENTS.md`, `CLAUDE.md` and the editor rule folders. A written project rule outranks a default here. Flagging code that follows a written rule is `audit-project-rules-first`.

## 3. Run every skill

Check the scope against each skill and record what you inspected.

| Skill | Check |
| --- | --- |
| `verify` | Each changed surface opened in the running app |
| `scope` | Every request in the thread against the diff |
| `reuse` | New components, styles and icons against the shared package |
| `restraint` | Unrequested UI, settings, fallbacks, dead code and narrating comments |
| `copy` | Every label, description and status string |
| `defaults` | Surfaces, type, sound, focus, names, forms, loading, hotkeys and dialogs |
| `motion` | Every transition, animation, gesture and exit |
| `color` | Text and field contrast in each theme, tokens inside components and the accent |
| `gather` | Each reference board: platform, links and the part to take |
| `match` | Each named reference, when the work copies one |
| `rule` | Repeated corrections with no written rule, and edits that break one |
| `viewports` | Each changed layout at every width, when layout is in scope |
| `ship` | Stray files, secrets, commits and checks, when git is in scope |

Skipping a skill without saying why is `audit-run-every-skill`.

## 4. Merge by root cause

One cause that breaks rules in two skills is one finding with both ids. Five call sites with the same local fix is one finding with five locations. Listing each symptom on its own line is `audit-one-row-per-cause`.

## 5. Number the fixes and open the report

Rank findings by severity, then by reach. Number them so the user can answer "fix 1, 2 and 5".

Copy [report.html](report.html) to `.audit/<scope>/index.html`, an ignored folder and never the source tree. Write `report.js` beside it in the shape its header comment shows, then open it.

The report's look ships with the skill, so write data only. A page with its own markup or styles is `audit-shipped-report`.

The user marks findings with Pick and pastes them back with Copy Picks. Wait for the pick, then fix only the numbers chosen. Fixing everything before the user picks is `audit-fix-what-was-picked`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `audit-state-the-scope` | "Audited the app" | "Audited the uncommitted diff: 14 files" |
| `audit-project-rules-first` | A border flagged in a repo whose rules require it | The project rule cited, no finding |
| `audit-run-every-skill` | `copy` silently skipped | "`copy`: no strings changed" |
| `audit-one-row-per-cause` | Five rows for one missing primitive fix | One row, five locations |
| `audit-shipped-report` | A report page written from scratch | `report.html` copied, only `report.js` written |
| `audit-fix-what-was-picked` | All 18 findings fixed unasked | The numbers the user chose |

## Reporting

Use the severity ladder and format in [report.md](report.md). `Block` when any `HIGH` remains, `Approve` otherwise. Never `Approve` work you did not open or read.
