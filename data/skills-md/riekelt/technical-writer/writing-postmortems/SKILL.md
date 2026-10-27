---
name: writing-postmortems
description: Use when writing a postmortem, incident report, or root-cause analysis after an outage, a defect that reached users, a data issue, or a near miss - or when turning an incident channel, alert log, or war-room thread into a durable document. Encodes the blameless framing, the evidence-only timeline, contributing factors, and owned action items. Use whenever something broke and the write-up must outlive the incident.
---

# Writing postmortems

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

Audience: the engineer who hits something similar in a year, not the people in the room. Core principle: **facts from evidence, causes from mechanisms, lessons from both, and no names.** Classification: historical; once reviewed it is immutable, and corrections are dated addenda.

## When to invoke, and not

Invoke after an incident is resolved, or at a stable milestone of a long one. A defect that reached users and a near miss (a guard caught what review missed) earn the same write-up. Do NOT invoke during the live incident: the runbook governs that. Not for assigning accountability: a postmortem that needs a person's name to make sense is describing a process hole. Not for a status update to stakeholders, which is a report.

## Skeleton

```markdown
# [System]: [the failure, as its symptom, one line]

| | |
|---|---|
| **Incident date** | YYYY-MM-DD |
| **Duration** | detection to resolution |
| **Severity** | [per the org taxonomy, defined where used] |
| **Status** | Draft / Reviewed |

## Summary
[User-visible impact with numbers, the root cause in one sentence, current state.
The reader who stops here still knows what happened.]

## Impact
[Who and what, quantified: requests failed, records affected, money or time lost.
Estimates labeled as estimates; "no evidence of data loss" only if actually checked,
and say what was checked.]

## Timeline
[Timestamped entries, facts only, each traceable to evidence: an alert, a log line,
a commit, a message. Interpretation lives in the sections below, never here.]

## Root cause and contributing factors
[The mechanism, grounded in code and commits. Contributing factors as a list;
"every component was correct and the defect lived between them" is a valid root
cause. Name which layer of checking missed it and which caught it.]

## Wrong turns during the response
[The wrong first fix, the misleading signal followed, the theory that cost an hour.]

## Action items
[Each with an owner and an acceptance check, filed as tracker issues and linked.
"Investigate X" without an owner is banned here as everywhere.]

## Sign-off
[- YYYY-MM-DD <reviewer>: approved <scope>, one line per review event.]
```

## Rules

- **Blameless means structural.** Name the role, the gate, the dependency, the missing guard; never the person. Blaming a person stops at "be more careful"; blaming a structure produces an action item. This governs the narrative (timeline, causes, response); action-item ownership is assignment, not blame: a role in this document, an individual in the linked tracker issue.
- **The timeline is evidence, not narrative.** Every entry traces to something checkable, timestamps from the systems rather than memory. Where memory is the only source, say so.
- **Wrong fixes are content.** The fix that made sense and did not work belongs in the document with the reasoning that made it plausible; embarrassment is not a retention policy.
- **Severity comes from the org taxonomy**, defined where used, not assumed. When no taxonomy exists, leave the field explicitly unassigned rather than inventing one.
- **Action items follow `writing-issues`**: outcome, owner, acceptance check, filed and linked, never left as prose intentions in the postmortem. When filing is not possible from where you sit, mark each item `[to file: <who files it>]`; the postmortem stays Draft until the links exist.
- **Immutable once reviewed.** New findings are dated addenda; a rewritten postmortem is a falsified record. The review itself goes in a sign-off line (see `references/truth.md` in the core skill).
- **Near misses use the same skeleton**, with Impact describing what would have happened, labeled as the counterfactual it is.

The decision that often follows a postmortem (a new invariant, a policy change) is recorded via `recording-decisions` and linked, not embedded. Runbook updates the incident exposed go through `writing-runbooks` in the same change as the fix; documentation is part of done, not a follow-up ticket.
