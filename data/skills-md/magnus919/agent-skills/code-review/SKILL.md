---
name: code-review
description: >-
  Review a code change for correctness, security, maintainability, and test adequacy,
  and reach a defensible verdict. Use when reviewing a pull request, diff, patch, or
  AI-generated change; when scoping an oversized review into reviewable units; when
  writing or triaging review comments; when assigning reviewers or setting review
  policy; or when investigating why a defect escaped review. Covers change sizing and
  attention budgets, risk-tiered checklists, severity-labeled comments, verdict and
  residual-risk records, review metrics that resist gaming, and the measured limits of
  checklists and AI reviewers. Do not use for implementing the requested change,
  root-cause debugging of a failing test or incident (use systematic-debugging),
  security assessment of a whole system (use security-audit-methodology), designing
  new code securely (use secure-software-engineering), architecture review across
  systems (use software-architecture), or reverse-engineering an unfamiliar codebase
  (use software-architecture-analysis).
license: MIT
compatibility: >-
  Platform-agnostic methodology. The bundled scripts require Python 3.10+, git, and
  the standard library only. No network access, review platform, or CI mandate.
metadata:
  spec-version: "1.0"
  tags: code-review, pull-request, diff, verdict, review-quality, defect-detection
---

# Code Review

Review is a decision about a change, supported by evidence a second person gathered
independently. Everything else — the comment count, the approval ritual, the review
template — is scaffolding around that decision.

Two facts shape the method in this skill:

- Review catches what a reviewer can hold in working memory. Effectiveness falls as
  changes grow and sessions run long, so scope and attention are the first decisions,
  not the last.
- Most review comments are about evolvability, not defects. That is a fine use of
  review, but it means "approved" is a statement about the evidence examined, never
  proof that the change is correct.

The reviewer's job is to say precisely what was examined, what was found, what was
decided, and what remains unknown.

## When to use this skill

- A pull request, patch, or diff needs a verdict.
- A change is too large to review in one pass and needs scoping or splitting.
- Review comments need triage, severity labels, or rewriting so they are actionable.
- A team needs reviewer assignment, review policy, or review-latency norms.
- A defect reached production and the question is what review missed.
- A model produced candidate review comments that a human must accept or discard.

## When not to use this skill

- The task is to fix the defect the review found — that is implementation work in the
  owning engineering skill.
- The task is to find the cause of a failure: route to `systematic-debugging`.
- The task is a whole-system security assessment: route to `security-audit-methodology`.
- The task is to design a new system or subsystem securely: route to
  `secure-software-engineering` and `software-architecture`.
- The task is architecture review across systems rather than a change: route to
  `software-architecture`.
- The task is to understand an unfamiliar codebase: route to
  `software-architecture-analysis`.

## The review contract

Before reading the diff, establish four things. If any is missing, ask for it — this
is the cheapest possible review comment.

| Element | Question | Failure if missing |
|---|---|---|
| Decision | What will this review authorise — merge, promote, release, incident closure? | The review optimizes for the wrong risk |
| Authority | Comment-only, approve, or approve-and-merge? | Reviewer implies authority they lack |
| Intent artifact | Issue, spec, ADR, or PR description stating the intended behavior | Reviewer reviews the code against their imagination |
| Evidence | Test output, runnable command, or artifact the author supplied | "Tests pass" is taken on faith |

Record the contract in the review record. See the review record template.

## The review loop

### 1. Read the intent before the diff

Read what the change claims to do, then read the diff. The gap between them is a
finding class of its own: behavior described but not implemented, implementation that
does more than described, and scope that drifted into unrelated files.

If the description is a restatement of the code ("adds `parseHeader`"), it is not
intent. Ask what problem the change solves and who is affected.

### 2. Scope the change with evidence, not impressions

Run the scope tool. It reports size, file classes, risk-bearing paths by convention,
whether source files moved with tests, and an attention budget:

```bash
python3 scripts/review_scope.py --base origin/main --head HEAD --markdown
python3 scripts/review_scope.py --base origin/main --head HEAD --json

# Reviewing an already-merged squash commit (or any single commit)
python3 scripts/review_scope.py --base <merge-sha>^ --head <merge-sha>

# Project-specific build output that the default markers do not know
python3 scripts/review_scope.py --base origin/main --head HEAD --exclude 'reports/*.json'
```

Use its output for three decisions:

- **Tier the risk.** A 40-line authorization change outranks a 900-line test refactor.
  Risk-bearing paths and change type set the tier, not line count. Use the risk-tiered
  checklist.
- **Set the budget.** Roughly 300 effective lines per hour is the conservative planning
  rate; sessions past about an hour stop paying. If the estimate exceeds one session,
  split the review or ask for a split change.
- **Order attention.** Risk-bearing and behavioral code first. Generated files,
  lockfiles, and vendored code are inspected for provenance, not read line by line.
  Exclusion is a claim about provenance: if a path is generated, say what generates it.

If the change is oversized, write a review plan and ask for it to be split or stacked.
Reviewing an oversized diff in one pass produces an approval that covers less than it
appears to.

### 3. Orient in one pass

Skim the whole diff once, without commenting, to learn its shape: entry points,
changed interfaces, new dependencies, data changes, test changes. Note file names as
you go. This pass exists so the second pass has a map.

### 4. Review in depth by attention order

Work through units in the order the scope tool suggests. For each unit, ask the
questions in the defect taxonomy rather than reading line by line:

1. **Correctness** — does it do the stated thing for valid input, and what happens at
   the boundaries?
2. **Failure paths** — errors, timeouts, partial writes, retries, cancellation.
3. **Trust boundaries** — untrusted input reaching a privileged sink; identity and
   authorization checked on the object being touched.
4. **Compatibility** — callers, stored data, wire contracts, configuration defaults.
5. **Test adequacy** — do the tests assert the behavior, including the denial and
   failure cases?
6. **Operability** — can an operator distinguish success from failure later?

Do not review formatting a linter already enforces. Do not restate the diff as
comments. If a unit is too large to hold, stop and ask for a split.

### 5. Gather independent evidence

Review is weaker than it looks when the reviewer only reads. Add at least one piece of
evidence the author did not supply when the change is T2 or above:

- Run the test that is supposed to prove the behavior, and confirm it fails without the
  change when that is cheap to do.
- Exercise the boundary the change claims to guard — empty input, wrong tenant,
  missing header.
- Read the code the change calls, not just the code it modifies.
- Check the rollback path actually exists.

State what you could not verify. "Not exercised in this environment" is an honest and
useful line in a review record; silence implies coverage you did not have.

### 6. Write findings the author can act on

Every finding carries a severity label, and blocking findings carry both evidence and
a verification method:

```
- [blocking] <claim> — evidence: <path:line or observation> — verify: <test or check>
- [should-fix] <claim> — evidence: <...>
- [question] <what the diff cannot tell you>
- [nit] <optional polish>
- [praise] <what to keep>
```

One claim per comment. Name the requirement, not a rewrite. A comment that says
"this is confusing" transfers the analysis back to the author; a comment that names
the missing case does not.

Comment discipline, tone, and disagreement handling: see the comment quality
reference. Reusable sheet: comment set template.

### 7. Decide the verdict

| Verdict | Asserts | Requires |
|---|---|---|
| `APPROVE` | Examined scope is correct and complete enough for the decision | No open blocking findings; residual risk recorded |
| `APPROVE WITH COMMENTS` | Mergeable now; the comments do not need to block | No open blocking findings; non-blocking items have owners |
| `REQUEST CHANGES` | At least one finding must be fixed before merge | Every blocking finding has evidence and a verification method |
| `NEEDS MORE EVIDENCE` | You cannot decide yet, and here is what is missing | The specific evidence gap, and who can supply it |

A verdict is a claim about the evidence you examined. It is not a claim about the
whole system, and it does not transfer to changes you did not see. Record residual
risk and explicitly unreviewed scope with the verdict; run
`python3 scripts/review_record_check.py <record.md>` to confirm the record does not
contradict itself.

### 8. Close the loop

- Re-review increments, not the whole change again. Confirm each blocking finding is
  fixed *and* verified, rather than merely edited.
- Resolve or explicitly defer every non-blocking finding with an owner.
- If the change grows materially after approval, the approval lapses. Say so.
- When a defect escapes, treat the escape as evidence about the review process, not
  about the reviewer's character: see the review metrics reference.

## Reviewing AI-generated and AI-reviewed changes

Two distinct problems, often confused:

- **AI wrote the change.** The risks are plausible-but-wrong code, tests overfitted to
  the implementation, invented APIs, and unexamined dependencies. Require the tests to
  be derived from the requirement, not from the patch, and review provenance and new
  dependencies explicitly.
- **AI reviewed the change.** Model output is a candidate finding list, not a verdict.
  Findings without a locator and evidence are dropped, not softened. Automation bias —
  accepting a machine suggestion because it is fluent — is the failure mode to guard
  against.

Do not credit a model's review of its own output as independent verification. See the
AI-assisted review reference and the AI pre-review brief template.

## Routing to the skills that own adjacent work

| When the review needs… | Route to |
|---|---|
| Judgment about design, naming, coupling, or refactoring quality | `programming-principles` |
| Independence model, test adequacy, mutation evidence, AI code quality gates | `qa-methodology` |
| A pass/fail verdict against explicit acceptance criteria | `verification-methodology` |
| Threat modeling or secure design for new code | `secure-software-engineering` |
| Whole-system security assessment or vulnerability classification | `security-audit-methodology` |
| Root cause of a failure found during review | `systematic-debugging` |
| Architecture-level tradeoffs or cross-system review | `software-architecture` |
| API or event contract compatibility and deprecation | `api-design-and-evolution` |
| Schema, migration, or pipeline correctness | `data-engineering`, `data-architect` |
| Performance evidence and regression benchmarks | `performance-optimization` |
| Release gates, rollout, rollback, and change-failure metrics | `release-engineering` |
| Documentation quality in the change | `technical-documentation` |
| Accessibility review of UI changes | `web-accessibility` |
| Privacy impact of data-handling changes | `privacy-engineering` |
| Durable decision record for a consequential choice | `adr-authoring` |
| Adversarial multi-perspective judgment on a contested change | `agent-council` |
| End-to-end delivery discipline for the change itself | `neckbeard` |

Read the routing table as ownership, not as prerequisites: review judgment stays here,
and the specialist skill supplies the depth for its own domain.

## Honest limits

- Review is not a defect filter with a known recall. It catches some classes well and
  misses others; treat a clean review as evidence of examination, not of correctness.
- Checklist coverage is not defect coverage. A ticked box records that a question was
  asked.
- Comment volume, approval rate, and review count are not quality measures. They are
  activity measures that improve when the process gets worse.
- The scope tool classifies paths by convention. It cannot see semantics, and a risky
  change in an innocuously named file will not be flagged.

## Completion criteria

The review is complete when the record states scope, evidence, labeled findings with
evidence and verification, a verdict consistent with those findings, an explicit
coverage level, residual risk, and explicitly unreviewed scope — and the record passes
`scripts/review_record_check.py`. Stop when the budget is spent rather than skimming
the remainder; reschedule or split instead of pretending coverage.

## Files in this skill

| File | Use |
|---|---|
| [references/evidence-base.md](references/evidence-base.md) | What the research actually shows about review effectiveness, size, latency, and AI review |
| [references/review-scoping-and-depth.md](references/review-scoping-and-depth.md) | Change sizing, tiers, attention allocation, incremental and stacked review |
| [references/defect-taxonomy.md](references/defect-taxonomy.md) | What to look for by defect class, with detection and false-positive traps |
| [references/comment-quality-and-communication.md](references/comment-quality-and-communication.md) | Severity taxonomy, actionable comment structure, disagreement and tone |
| [references/verdicts-and-evidence.md](references/verdicts-and-evidence.md) | Verdict semantics, approval authority, residual risk, evidence boundaries |
| [references/ai-assisted-review.md](references/ai-assisted-review.md) | Model-written and model-reviewed changes, automation bias, provenance |
| [references/review-metrics.md](references/review-metrics.md) | Review latency, size, defect escape, and which metrics are gameable |
| [references/source-index.md](references/source-index.md) | Dated sources behind the claims in this skill |
| [templates/review-record.md](templates/review-record.md) | Durable record of scope, evidence, findings, verdict, residual risk |
| [templates/review-plan.md](templates/review-plan.md) | Split and schedule an oversized review |
| [templates/comment-set.md](templates/comment-set.md) | Severity-labeled comment sheet with worked examples |
| [templates/risk-tier-checklist.md](templates/risk-tier-checklist.md) | Risk-tiered questions, each naming the evidence that answers it |
| [templates/ai-review-brief.md](templates/ai-review-brief.md) | Brief for a model doing candidate-finding pre-review |
| [scripts/review_scope.py](scripts/review_scope.py) | Deterministic diff scope, risk flags, test mapping, attention budget |
| [scripts/review_record_check.py](scripts/review_record_check.py) | Validate a review record for completeness and verdict consistency |
| [scripts/test_review_scope.py](scripts/test_review_scope.py) | Tests for the scope tool against real temporary repositories |
| [scripts/test_review_record_check.py](scripts/test_review_record_check.py) | Tests for the record checker, including the shipped template |
