---
name: infrahub-reporting-skill-gaps
description: >-
  Turns friction from an Infrahub skill session into a reviewed GitHub issue about an Infrahub skill's guidance.
  Infrahub skills fail quietly: a missing or unclear rule does not crash, it produces extra round trips and
  repeated user nudges. This skill gathers evidence of that friction, checks the tracker for an existing
  report, works out whether the skill or the underlying product is at fault, and drafts a proposed rule
  change. It never files anything itself: it hands the redacted draft to infrahub-reporting-issues, which
  shows it to the user and gets explicit approval before any submission.
  TRIGGER when: accepting a friction offer, the user says "report skill friction", asks why an Infrahub skill
  kept failing or needed so many retries, or wants a gap in an Infrahub skill's guidance reported.
  DO NOT TRIGGER when: reporting a bug in Infrahub itself or any other opsmill/infrahub-* product (use
  infrahub-reporting-issues instead), or for ordinary Infrahub work where nothing went wrong.
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Skill Gap Reporter

## Overview

Infrahub skills fail quietly. A missing rule does not
crash; it produces eleven round trips and four user
nudges before the model finds the right answer on its
own. This skill works out which rule was missing,
wrong, or unclear, and drafts the improvement as an issue
report. It does **not** file anything itself, and it does
not decide where the report goes: it prepares a complete,
redacted draft and hands it to
[infrahub-reporting-issues](../infrahub-reporting-issues/SKILL.md),
which owns the 11-repo registry and the routing, the
consent gate, submission-method choice, and confirmation.
This skill's job ends at the handoff.

## When to Use

Trigger this skill when the user says things like:

- "That took way too many tries, can you report the
  friction?"
- "Report skill friction."
- "Why did the schema skill keep getting this wrong?"
- "This skill's guidance is missing something, can we
  fix it?"

Do not trigger for a bug in Infrahub, the SDK, or any
other `opsmill/infrahub-*` product; that belongs to
[infrahub-reporting-issues](../infrahub-reporting-issues/SKILL.md).
Do not trigger for ordinary Infrahub work that
completed without friction.

## Workflow

Follow these steps in order. Stop at every gate step;
never proceed past one without explicit
confirmation.

### 1. Detect and confirm the gap

Start with the current conversation. Only look at a
past session's transcript when the user points at one.
Read [reference.md](reference.md) for how transcript
discovery works and where the signals live.

Then work the detection ladder in order, and stop as
soon as the friction is described:

1. **Verifier verdict.** Find a red-to-green transition
   on the same target (`infrahubctl schema load`,
   `object load`, `check run`, `transform run`, a
   `pytest` run). It is the strongest evidence there is,
   because no self-assessment produced it. It only
   counts when the skill was loaded before the first
   attempt.
2. **Coverage read.** `ls skills/<skill>/rules/` and
   grep the topic. This names the file, or its absence.
3. **Correction delta.** Diff the first authored version
   against the accepted one. That delta is the proposed
   rule change, not a paraphrase of it.
4. **Session-shape counters.** Retries, edit churn,
   repeated asks, a docs escape. These open an
   investigation and never close one.

A draft supported only by counters is not ready: say
which probe came up empty and stop. See
[rules/evidence-detection-ladder.md](rules/evidence-detection-ladder.md).

### 2. Check the tracker

Search `opsmill/infrahub-skills` before drafting
anything. The search decides the shape of the report,
never whether there is one: a match means a comment on
that issue, no match means a new issue with an explicit
confidence label. See
[rules/workflow-tracker-first.md](rules/workflow-tracker-first.md).

### 3. Triage: level 1, routing

Decide whether the friction is a skill defect, a
product defect, or neither. Only skill defects continue
to level 2 and drafting. See
[rules/workflow-triage-classification.md](rules/workflow-triage-classification.md).

### 3b. Triage: level 2, bug, feature, or docs gap

For a skill defect, decide the kind from three outcomes:
a bug (a rule or reference covers the topic and the
model still got it wrong), a feature (no rule covers the
topic, and a docs escape either found the answer or
never happened), or a docs gap (no rule covers the
topic, a docs escape happened but still failed to answer
it, and the underlying behavior is settled). That last
condition is a gate, not a detail: if the workflow is
still being defined or is deliberately undocumented,
there is nothing to document yet, so do not draft at
all, tell the user why, and stop. This decides the
title prefix used for drafting in step 6, and it is what
the receiver routes on. See
[rules/workflow-bug-vs-feature.md](rules/workflow-bug-vs-feature.md).

### 4. Hand off if product

If triage points at the underlying product rather than
the skill's guidance, stop here and hand off to
[infrahub-reporting-issues](../infrahub-reporting-issues/SKILL.md)
instead of drafting a skill-friction issue. See
[rules/workflow-handoff-product-bugs.md](rules/workflow-handoff-product-bugs.md).

### 5. Locate the artifact

Name the specific rule file, or lack of one, that should
have prevented the friction. Probe B in step 1 already
ran this read; this step is where its result becomes a
citation. A draft that cannot name the implicated file,
or the gap in coverage, is not ready. See
[rules/evidence-cite-the-artifact.md](rules/evidence-cite-the-artifact.md).

### 6. Draft and redact

Fill [templates/skill-friction.md](templates/skill-friction.md),
using the `bug:`/`feat:`/`bug(docs):` title prefix
decided in step 3b and the confidence label decided in
step 2. Redact anything that identifies the user's
infrastructure or organization per
[rules/evidence-no-customer-data.md](rules/evidence-no-customer-data.md).
This is security-critical and applies before the draft
ever leaves this skill.

The header carries three versions, and a report is not
ready without all three:

1. **Skills**, from `metadata.version` in the implicated
   skill's own SKILL.md frontmatter. Says which revision
   of the rule failed.
2. **Infrahub SDK**, from the `SDK Version` line of
   `infrahubctl info`. Says what a rule naming a CLI
   flag or client method was aimed at.
3. **Infrahub**, from the `Infrahub Version` line of
   the same output. Says what a rule about schema
   loading, branch behavior, or a check pipeline was
   aimed at.

Run `infrahubctl info` as
[../infrahub-common/rules/connectivity-server-check.md](../infrahub-common/rules/connectivity-server-check.md)
prescribes; the runner prefix matters.

Without them a maintainer cannot tell whether the
guidance is wrong or merely older than what ran, which
is the difference between rewriting a rule and adding a
version note to it. Copy only the version values:
`infrahubctl info` also prints the server address and
deployment ID, which
[rules/evidence-no-customer-data.md](rules/evidence-no-customer-data.md)
forbids. Write `unknown` for any of the three that
cannot be read; never guess.

This produces the three handoff fields `type`, `title`,
and `body`. It does **not** produce a target repository:
naming one is not this skill's call, and the draft must
not contain one.

When step 2 found a match, draft a comment instead: no
title, no repeated problem statement, only the new
evidence this session adds.

### 7. Hand off

Invoke [infrahub-reporting-issues](../infrahub-reporting-issues/SKILL.md)
with the payload `{type, title, body, searched, issue?}`,
where `searched` names the repo step 2 searched and
`issue` is set only when it matched. There is no `repo`
field: that skill resolves the destination from `type`
against its own registry, and owns the review gate,
submission-method choice, and confirmation from here.
Never file or comment directly. See
[rules/workflow-handoff-to-reporting.md](rules/workflow-handoff-to-reporting.md).

### 8. Relay the outcome

One line on what the hand-off returned, with the issue
URL if it produced one. The receiver already confirmed
with the user; this is a relay, not a second
confirmation. The tracker is the durable record; this
skill keeps no local state of its own.

## Rule Categories

| Prefix | Category | Description |
| --------- | -------- | ----------- |
| `workflow-` | Workflow | Ordering and gating: the tracker check, triage, and handoff (to `infrahub-reporting-issues`, either for a product defect or to file a skill defect). Skipping one produces noise in the maintainers' tracker or a second, drifting filing pipeline |
| `evidence-` | Evidence | What may and may not appear in a filed issue. Security-critical: issue bodies are public and cannot be retracted |

See [rules/_sections.md](rules/_sections.md) for the
index.

## Supporting References

- [reference.md](reference.md): evidence source
  priority, transcript discovery, and friction signals.
  **Read this in step 1.**
- [rules/evidence-detection-ladder.md](rules/evidence-detection-ladder.md):
  the four probes that establish a gap exists, and why
  counters alone never do. Read this in step 1.
- [templates/skill-friction.md](templates/skill-friction.md):
  the draft template filled in step 6.
- [rules/workflow-tracker-first.md](rules/workflow-tracker-first.md):
  search the tracker before drafting, and label the
  confidence of what you draft. Read this in step 2.
- [rules/evidence-no-customer-data.md](rules/evidence-no-customer-data.md):
  what to redact before drafting. Security-critical;
  read this before every draft.
- [rules/workflow-handoff-to-reporting.md](rules/workflow-handoff-to-reporting.md):
  hand the payload to `infrahub-reporting-issues`; never
  file directly. Read this before step 7.
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap

## Anti-patterns

- **Filing without a proposed rule change.** A friction
  report that does not name a file to create or edit,
  and what it should say, is not actionable. The
  maintainers should not have to reverse-engineer the
  fix from a symptom description.
- **Filing when the implicated skill is unknown.** If
  step 5 cannot name a skill and a rule file (or the
  absence of one), the report is not ready to draft.
- **Filing a retry count.** Round trips, nudges, and
  edit churn measure a session, not a ruleset. They rise
  for reasons that have nothing to do with the skill: an
  unclear request, a slow instance, a user changing
  their mind. They open an investigation; a verifier
  verdict or a coverage read closes it.
- **Drafting without checking the tracker.** Step 2 is
  not optional. A report drafted blind either duplicates
  an open issue or throws away the one place a second
  observer would have found it.
- **Filing a duplicate instead of commenting.** When an
  issue already covers the friction, a second issue
  splits the evidence across two threads. The comment is
  the more valuable artifact: it is the corroboration
  the maintainer needs.
- **Suppressing a first sighting.** A single observation
  is weak evidence, not zero evidence. Label it
  `unconfirmed` and let the maintainer judge; silence
  guarantees the second observer never finds it.
- **Pasting raw error text without redaction.** Error
  messages carry file paths, hostnames, and node kinds
  that identify a customer's infrastructure. Paraphrase,
  don't paste.
- **Filing directly instead of handing off.** This
  skill has no consent gate, no duplicate search, and no
  submission method of its own. Running `gh issue create`
  here, or claiming an issue was filed, bypasses the one
  review gate `infrahub-reporting-issues` provides and
  risks a second, unreviewed submission.
