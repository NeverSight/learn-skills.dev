---
name: chief-of-staff-methodology
description: >-
  Prepare accountable executive decisions, information triage, briefing, calendar choices,
  organizational sensing, and institutional memory without assuming authority or
  monitoring people. Use when a chief of staff or CoS, executive office, gatekeeping,
  decision memo, executive briefing, board materials, organizational sensing, team health,
  institutional memory, calendar triage, meeting audit, strategic time, or attention
  allocation is requested. Do not use this skill for unrelated requests; route to the
  nearest named specialist.
license: MIT
compatibility: No runtime dependency.
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: "867a555"
  source_path: skills/chief-of-staff-methodology
  source_treatment: Adapted from supplied issue source material and substantially rewritten for host-neutral, privacy-aware use.
---

# Chief of Staff Methodology

The Chief of Staff supports an accountable leader's capacity to operate across
domains. This skill helps prepare, triage, coordinate, surface trade-offs, and
preserve decision context; it does not transfer the leader's authority.

## When to Load

Load this skill for executive-office work involving:

- Information triage, gatekeeping, escalation paths, or decision rights.
- Decision memos, executive briefing, board materials, or preparation for an accountable decision-maker.
- Calendar triage, meeting audits, strategic time, or attention allocation.
- Cross-functional coordination where ownership, dependencies, or escalation need clarification.
- Transparent organizational sensing or team-health concerns.
- Institutional memory, leadership transitions, documented decisions, or commitments.
- Chief of staff, CoS, or leader-effectiveness work that needs a bounded operating method.

## When Not to Use

Do not use this skill as a meeting-transcript action-item generator or a general
backlog-capture mechanism. A recommendation, a discussion topic, or an inferred
next step belongs in a briefing or decision record unless an accountable owner
has confirmed a discrete commitment and a realistic due date. Use the authorized
task-system skill only after those conditions are satisfied.

## What This Skill Provides

This skill provides six methodology domains as progressive disclosure through
`references/`. Load the reference matching the task using your agent's normal
means; no specific profile, memory, calendar, or orchestration system is assumed.

## Reference Files

| Reference | Load when | File |
|---|---|---|
| Gatekeeping and triage | Mapping information to authority, access, and escalation | `references/gatekeeping-and-triage.md` |
| Executive briefing | Preparing decision-ready material or an executive update | `references/executive-briefing.md` |
| Leverage mechanisms | Improving the leader's operating system without false measurement | `references/force-multiplication.md` |
| Organizational sensing | Addressing team-health or organizational signals responsibly | `references/organizational-sensing.md` |
| Institutional memory | Recording decisions, commitments, and authorized handoffs | `references/institutional-memory.md` |
| Meeting and calendar triage | Reviewing meetings and calendar choices with the leader | `references/meeting-and-calendar-triage.md` |
| Source index | Checking provenance and the limits of source treatment | `references/source-index.md` |

## Operating Method

1. Identify the accountable human decision-maker, the decision rights already delegated, and the decision or outcome at stake.
2. Gather authorized evidence and label it as verified fact, assumption, reported concern, or unknown. Do not invent costs, timelines, authority, or stakeholder views.
3. Route ordinary work to its authorized owner. Keep direct, protected routes open for safety, ethics, legal, HR, fraud, retaliation, and whistleblowing concerns.
4. Prepare options and trade-offs, then give a clearly labeled recommendation when the request calls for one. The accountable human reviews and decides.
5. Record only decision-relevant material under the access, retention, correction, and handoff rules in the applicable reference.

## Task Creation Discipline

**Applicability:** Only when creating or updating tasks in an authorized task system.

A task is a record of a concrete, documented commitment, not a place to store
advice, aspirations, meeting summaries, inferred next steps, or recurring
leadership habits. Create a task only when the source establishes all of the
following:

1. A discrete outcome or next action that can be completed or explicitly reviewed.
2. An accountable owner who has made, confirmed, or accepted the commitment.
3. A realistic due date grounded in an explicit deadline, an agreed review date,
   or context that supports a specific date. Never invent a date merely to fill
   a required field.
4. Enough provenance in the task or linked record for the owner to understand
   the commitment and correct it.

Before creating the task, check all four conditions. If the source offers a
recommendation, a general principle, or an inferred action without an owner or
defensible due date, preserve it as a briefing observation or ask the accountable
human to confirm the commitment and date. Do not create the task.

When a task is created, include the owner and due date in the creation request,
then read it back and verify both fields persisted. If either is absent or wrong,
repair it before reporting success. A past deadline is a triage signal: surface
it as overdue for an explicit reschedule, completion, or closure decision rather
than silently assigning a new date.

## Accountable Human Authority

This skill supports an accountable human leader. It may prepare, advise, triage,
synthesize, and surface trade-offs. It does not make employment, compensation,
disciplinary, legal, fiduciary, or other reserved decisions, and it does not
present an automated recommendation as a decision.

Name the decision-maker and applicable approval or review path in consequential
artifacts. A CoS function can coordinate delegated work, but it must route work
outside that delegation to the authorized owner. Human review is required before
material is issued as the leader's position.

## Privacy, Confidentiality, and Ethics

Use only authorized, purpose-limited information. Prefer aggregate information
and the minimum data needed for the stated purpose. Be transparent about what is
collected, who can access it, how it is retained, and how people can correct it.

Do not use covert monitoring, individual trust scores, dossiers, gossip maps,
quiet-quitting labels, hidden relationship profiling, or speculative judgments
about people. Confidentiality has limits: safety, harassment, fraud, legal, and
policy obligations may require escalation through authorized channels. Preserve
anti-retaliation protections and involve qualified HR, legal, safety, or ethics
professionals for matters in their remit.

## Boundaries

| Domain | Boundary | Use instead |
|---|---|---|
| Product definition and prioritization | This skill prepares or coordinates a decision; it does not define product strategy | `product-methodology` |
| Corporate or business strategy | This skill structures a leader's operating work; it does not set strategy | `strategy-frameworks` |
| Financial models and budgets | This skill may surface a resource question but does not build or validate a model | `financial-modeling` |
| Verification claims | This skill prepares artifacts but does not turn missing evidence into a pass | `verification-methodology` |
| Evidence presentation | This skill does not prescribe a research-artifact hierarchy | `artifact-pyramids` |
| Operational tooling | It does not automate mail, calendars, personal data stores, or task systems | Use the organization's authorized tools and policies |

## Pitfalls

- Treating triage as a private veto instead of a transparent route to the authorized owner.
- Hiding uncertainty, weak evidence, or an unresolved conflict to make a brief look decisive.
- Speaking as the leader without review, approval, and clear authorship.
- Treating people signals as proof of individual performance, intent, or protected-status issues.
- Storing personal impressions instead of durable, documented decision context.

## Related Skills

- `artifact-pyramids` for layered, inspectable decision artifacts.
- `financial-modeling` for assumptions-led financial analysis.
- `product-methodology` for product decisions and prioritization.
- `strategy-frameworks` for strategy choices and trade-offs.
- `verification-methodology` for evidence-backed completion claims.
- `slack` — channel triage and message search through the Slack Web API; confirmed posting only. The everyday read layer for "what was said, find it later."
- `notion` — knowledge search, page and database reads through the Notion API; confirmed edits only.
- `email` — transactional email sends and delivery verification (bounces, spam reports, event-webhook signature check) through SendGrid. Read-only discovery before any send.

## Portability

This skill is intentionally host-neutral. Use your agent's normal mechanisms to
load the references listed here. Do not assume a particular profile system, task
orchestrator, memory service, calendar provider, or response-handoff format.
