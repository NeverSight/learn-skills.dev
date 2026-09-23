---
name: neckbeard
description: >-
  Use when asked to fix, build, refactor, review, verify, or release software and the work
  is non-trivial — including delivering a change request through planning, gates,
  implementation, review, verified PR, and authorized release; continuing work started
  elsewhere with no packet via evidence-based position assessment; or operating tracked
  work items in Linear, Jira, or Notion via their tooling skills. neckbeard routes the
  change through framing, discovery, design, implementation, review, verification, and
  learning — choosing the smallest *safe* intervention, proving it at the real delivery
  boundary, and leaving an inspectable evidence ledger. For issue-to-PR work, conditionally
  loads a 9-phase journey with gates and lifecycle integration. Composes specialist catalog
  skills rather than replacing them. Not a persona or LOC-minimizer. Do not use this skill
  for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Agent harness with file read/write, terminal, and skill loading. No network or runtime dependency required by the bundle itself.
metadata:
  spec-version: "1.0"
  tags: sdlc, delivery, evidence, verification, workflow
---

# neckbeard

A disciplined operating model for software delivery. It does not perform a
character. It makes an agent do six things reliably: frame the change, discover
the real system before designing, pick the smallest *safe* intervention, execute
by stage, record evidence, and stop or escalate when the evidence runs out.

The name is a joke about the "10x developer in a Markdown file" trope. The
substance is the opposite of that trope: effectiveness here is earned by
observable outcomes and scoped claims, never asserted by a persona.

## When to load this

Load neckbeard when a request is a non-trivial software change — a bug to
diagnose, a feature to build, a refactor, a review, a release to verify — and
you need a bounded, stage-aware way to carry it to a defensible "done."

## When not to use

Do **not** load it for:
- A single factual question or lookup (answer directly).
- A one-line edit whose contract is already fully specified (just do it, but
  still verify at the boundary).
- A task already owned end-to-end by a more specific skill (route there; see
  [references/routing-table.md](references/routing-table.md)).

## Core loop

Every run moves through the same spine. Each stage has entry conditions,
required evidence, exit conditions, and escalation rules detailed in
[references/stages.md](references/stages.md).

1. **Frame the change contract.** State the user-visible problem, constraints,
   system boundary, risks, and explicit non-goals. Distinguish *authority to
   explore* from *authority to modify, publish, deploy, or merge*. Stop early if
   no change is justified, and keep the evidence for that decision.
   Template: [templates/change-contract.md](templates/change-contract.md).

2. **Discover before designing.** Inspect the actual repository, contribution
   guidance, architecture, callers, tests, config, and recent changes *before*
   proposing a fix. Prefer primary evidence (code, tests, runtime output,
   project docs) over plausible architecture narratives. Make unverified
   assumptions and missing access explicit.

3. **Select the smallest safe intervention.** Reuse existing code and platform
   capabilities first; then the smallest implementation that satisfies the
   verified contract. Treat "smallest diff" as a *consequence of understanding*,
   not an optimization target. Never trade away trust-boundary validation, data
   safety, security, accessibility, observability, operational recovery, or
   explicitly requested behavior. Record any deliberate ceiling and its upgrade
   trigger.

   Classify a test-hardening request explicitly when production behavior is
   already correct and the work adds a focused guard for a coverage gap or named
   mutation. That is a lightweight-path subtype, not an ordinary production
   bugfix: use baseline-pass / mutant-fail evidence instead of requiring the new
   test to fail on clean `main`. Load
   [references/lightweight-test-hardening.md](references/lightweight-test-hardening.md)
   for the bounded contract and escalation triggers.

4. **Execute by SDLC stage.** Route the work to the stage that owns it —
   discovery/requirements, design, implementation, verification, delivery,
   learning. Load the matching specialist skill where one exists rather than
   re-deriving its method (see routing table).

5. **Keep an evidence ledger.** Each non-trivial run emits a compact record:
   intent, inspected artifacts, assumptions, rejected alternatives, files
   changed, commands/checks run, observed outputs, unverified boundaries,
   rollback/follow-up triggers. Distinguish a component check from an
   end-to-end or production-boundary check. Format and rules:
   [references/evidence-ledger.md](references/evidence-ledger.md).
   Template: [templates/evidence-ledger.md](templates/evidence-ledger.md).

6. **Stop and escalate by rule.** Stop and report when the task has no verified
   need, a risk/authority boundary needs a human, or two materially different
   approaches have failed. Never trade persistence for privilege escalation,
   destructive recovery, or unbounded workaround churn. Rules:
   [references/risk-authority-gates.md](references/risk-authority-gates.md).

For asynchronous work and stage-finality decisions, use
[references/progress-and-finality.md](references/progress-and-finality.md):
judge semantic progress and declared dependencies, not elapsed time or
repeated observations.

## Change-request work (conditional)

When the request is a change request — an issue, ticket, or tracked request that
will produce a pull request or an equivalent reviewable deliverable — the 6-step
core loop above still governs each stage, but the run also follows the canonical
9-phase change-request journey:

→ **[references/journey.md](references/journey.md)** — intake → discovery →
design → spec → test plan → implementation → review → readiness → authorized
release.

The journey adds gates, a delivery packet for cross-phase state, and platform
lifecycle mechanics (GitHub or enterprise). It does **not** replace the core loop
or create a second orchestrator.

**Do not load the journey for:** a simple fix, refactor, or review that has no
issue/ticket trajectory. That work uses the core loop and the stage references
below without the journey's phases, packet, or gates.

### Mid-flight engagement (conditional)

When the request is to **continue delivery work that started elsewhere** — a
half-implemented branch, an adopted spec, a change request another contributor
began — and no delivery packet exists, do not restart at phase 1 and do not
trust narrative summaries of what was done. Run position assessment first:
inventory observable artifacts, score them against phase exit conditions, emit
a position report (current step, satisfied gates with evidence pointers,
remaining checklist), then bootstrap a packet and continue under the normal
journey.

Procedure: [references/position-assessment.md](references/position-assessment.md).
Load it only for mid-flight engagement; fresh change requests start at phase 1,
and existing packets govern resumability through
[references/delivery-packet.md](references/delivery-packet.md).

## Path selection before ceremony

Select the delivery path immediately after current-state discovery and before
creating path-specific artifacts. Use the affected surface and risk, not line
count alone.

For a test-hardening request, choose the lightweight path only when production
behavior is already correct, production code remains unchanged, the change is
confined to tests or fixtures, and a focused deterministic check plus a bounded
controlled weakening can expose the regression. Record the invariant, the clean
baseline evidence, the named mutation, and the non-goals. Do not apply the
ordinary bugfix requirement that a new test fail on clean `main`.

For expensive or serialized CI, local design, hermeticity, focused tests,
targeted mutation, lint, compilation, and scope checks must pass before the
first push. Freeze the candidate before requesting one bounded final review or
the repository's required platform review. A timed-out review is inconclusive,
not a reason to launch repeated review rounds. Material changes invalidate the
relevant verification and bind the replacement verdicts to the new exact head.

The detailed test-hardening contract and escalation triggers are in
[references/lightweight-test-hardening.md](references/lightweight-test-hardening.md).

## The one rule that defines "done"

> "Done" is prohibited unless the declared verification target has actually been
> exercised. If it has not, report the unverified gap honestly instead of
> claiming completion.

A passing unit test is not the same as exercising the delivery boundary. A local
render is not production. State which boundary was checked and which was not.
Verification method: load the catalog skill `verification-methodology`.

## Minimalism, correctly

Minimalism in this bundle is a *conditional* design choice made **after**
real-flow understanding — not an unconditional "fewest lines wins" reflex. The
correct answer is sometimes a larger change, a new dependency, a process change,
or no code change at all. The evaluation fixtures include adversarial cases
specifically so the bundle cannot win by reflexively deleting or compressing.
See [references/stages.md](references/stages.md) §3.

## Routing: compose, don't swallow

neckbeard owns the *cross-stage contracts* — the change contract, evidence
ledger, stop rules, and evaluation protocol. It does **not** own domain method.
When a stage has a specialist skill, load it and follow it. The full table with
"use existing skill instead" conditions is
[references/routing-table.md](references/routing-table.md). Summary:

| Stage / need | Load this catalog skill instead of re-deriving |
|---|---|
| Stakeholder discovery, requirements, ACs | `product-discovery` |
| User-facing behavior, interaction, information architecture | `product-design-and-ux` |
| Formal specification, phase gates | `spec-driven-development` |
| Reverse-engineering an existing codebase | `software-architecture-analysis` |
| Designing or evolving an API / interface contract | `api-design-and-evolution` |
| Root-cause debugging | `systematic-debugging` |
| Security review, threat modeling, secure design | `secure-software-engineering` |
| Accessibility (WCAG, keyboard/focus, error recovery) | `web-accessibility` |
| Test strategy, regression testing, CI quality gates | `qa-methodology` |
| Mobile app implementation (iOS/Android/Flutter/React Native) | `mobile-development` |
| Docs / README / API reference | `technical-documentation` |
| Verification verdicts and evidence | `verification-methodology` |
| Intent contracts, work classification, autonomy gating, failure routing across a run | `bmad` |
| Release planning, versioning, pipeline promotion, readiness, rollout, or rollback design | `release-engineering` |
| Reliability, incident response, or operational recovery | `site-reliability-engineering` |

If a specialist skill is not installed, neckbeard's stage references provide a
minimal fallback method — but note in the ledger that the specialist was absent.

## Evaluation is a first-class deliverable

This bundle ships a versioned evaluation harness in [eval/](eval/). It measures
SDLC *outcomes* the bundle claims to improve — correctness, regression safety,
scope discipline, boundary verification, honest uncertainty — never LOC or
response brevity. Before claiming any improvement, run the public suite and
report holdout results through the maintainers' workflow. Methodology:
[references/evaluation.md](references/evaluation.md).

**Claims policy.** Scope every performance claim to the evaluated models,
harnesses, repositories, task classes, and dates. Do not use "10x developer,"
"always," "best," or any global performance claim without a published,
reproducible definition and evidence. LOC may appear only as diagnostic
metadata, never as a success proxy.

## File map

| Path | Loaded when |
|---|---|
| [references/stages.md](references/stages.md) | Entering any SDLC stage; defines entry/evidence/exit/escalation per stage |
| [references/evidence-ledger.md](references/evidence-ledger.md) | Building or auditing the ledger; defines required fields and boundary rules |
| [references/risk-authority-gates.md](references/risk-authority-gates.md) | Before any mutation, deploy, merge, or destructive act; and on stop/escalation |
| [references/routing-table.md](references/routing-table.md) | Deciding whether a specialist skill owns the current stage |
| [references/journey.md](references/journey.md) | **Change-request work only** — an issue/ticket/request that will produce a PR or equivalent reviewable deliverable. Defines the 9-phase intake→release sequence, gates, and paths. **Not loaded** for a simple fix, refactor, or review without an issue/ticket trajectory (that work uses the core loop above). |
| [references/lightweight-test-hardening.md](references/lightweight-test-hardening.md) | Test-only regression guards for already-correct production behavior: baseline-pass / mutant-fail evidence, hermeticity, finality-before-push, bounded review, and escalation triggers. |
| [references/lifecycle.md](references/lifecycle.md) | **Change-request work only** — platform mechanics (GitHub reference mode or enterprise mode) for intake, submission, CI/review monitoring, and authorized release. **Not loaded** for a simple fix, refactor, or review without an issue/ticket trajectory. |
| [references/delivery-packet.md](references/delivery-packet.md) | **Change-request work only** — carrying state across phases of a change-request run, or resuming after a context boundary; defines packet fields, artifact ownership, lifecycle states, and resumability. **Not loaded** for a simple fix, refactor, or review without an issue/ticket trajectory. |
| [references/position-assessment.md](references/position-assessment.md) | **Mid-flight engagement only** — continuing delivery work that started elsewhere with no delivery packet: artifact inventory, exit-condition scoring, position report, packet bootstrap. |
| [references/tracker-discovery.md](references/tracker-discovery.md) | **Change-request intake** — detecting which tracking system holds the work item and routing tracker operations to the matching catalog tooling skill; keeps the journey vocabulary tracker-neutral. |
| [references/evaluation.md](references/evaluation.md) | Designing, running, or reporting an evaluation |
| [templates/](templates/) | Change contract, decision record, evidence ledger, verification plan, eval report; plus [templates/delivery-packet.md](templates/delivery-packet.md) — the fillable packet, **for change-request work only** (not for a simple fix/refactor/review without an issue trajectory) |
| [eval/](eval/) | Task schema, rubric, baseline protocol, fixtures, runner |