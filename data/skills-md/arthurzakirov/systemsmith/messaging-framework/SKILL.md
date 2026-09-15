---
name: messaging-framework
description: Core principles for technical communication such as commits, PR descriptions, branch names, and technical documentation. Use when writing or refining engineering-facing messaging and when other skills need a shared communication baseline.
---

# Messaging Framework

Core principles for writing commits, PR descriptions, branch names, and technical documentation.

## Two Goals

| Goal | Purpose |
| --- | --- |
| Inform | Help the reader understand and remember what the work is about |
| Advertise | Argue the value so review effort feels worthwhile |

## The Pain-Point Pattern

Structure messages around real pain points only:

- Observed problem
- Downstream implication

Do not write solution-heavy PR bodies. Reviewers will inspect the diff. Do not add test plan sections just to restate what is already visible in the changes.

Pain points should describe actual experience such as errors, duplicated workflows, expensive processes, or confusing behavior, plus the consequence.

| Bad | Good |
| --- | --- |
| "No common interface" | "Local-dev orchestration duplicated across environments, so copies drifted out of sync" |
| "Lost error context" | "Backend failures were mapped to the wrong outcome, so technical errors looked like domain results" |

## Sentence Structure

Prefer:

- "`[Verb]` benefit by mechanism"
- "`[Verb]` mechanism for benefit"

Examples:

- "speed up local dev by automating config and log formatting"
- "prevent data loss by fixing the asset sync race"

## Format By Artifact

| Artifact | Format | Length |
| --- | --- | --- |
| Branch name | `TICKET/short-description` | Short |
| Commit subject | `TICKET: type(scope): verb benefit by mechanism` | <=100 chars |
| Commit body | Pain points only | Medium |
| PR title | Same as commit subject | Short |
| PR description | Pain points plus one-line approach | Medium |

## Anti-Patterns

- "Add feature"
- "Fix bug"
- "Refactor code"
- "Update dependencies"
- Solution checklists in PR bodies
- Generic abstractions instead of observed problems
