---
name: validating-completed-tasks
description: "Use when validating a completed task or a colleague's deliverable for task acceptance, initially or after prior review and revisions: whether the work is correct, complete, and trustworthy, including review plus real acceptance/edge-case testing, re-reviewing fixes against earlier findings and current task requirements, or checking a research/security report and its evidence. Not for defect-only or merge-readiness review without task-completion validation even if a ticket is cited; test-only execution; reporting settled findings; explanation-only walkthroughs; implementing the task; or fixing findings."
---

# Validating Completed Tasks

Determine whether the delivered work actually satisfies the task, whether its conclusions or behavior
can be trusted, and what remains before acceptance. Review, real verification, and an author-facing
report are one workflow; passing unit tests or a plausible document alone does not answer the question.

## Scope and Authority

Use for implementations, research/security reports, or mixed deliverables. This is a coordinator, not
another review method or report template. **Load the owner skill for each applicable stage** below;
reuse it if already loaded. Refer to its resources from that skill's actual loaded directory, not guessed
installation paths or sibling folders. Do not rely on an agent profile to load the method.

| Stage | Owner and when to use it |
| --- | --- |
| Code inspection and findings | `reviewing-code-changes` before inspecting a change. It owns scope, whole-change coverage, conformance, design/defect review, finding validation, severity, and readiness. Use its `references/requirements.md` when task requirements exist, `references/scope-and-evidence.md` for the comparison cases it covers, and `references/test-design.md` when designing checks. |
| Research claim validation | `research-with-evidence` before substantive investigation of a delivered report. It owns source fitness, claim provenance, counterevidence, quantitative claims, and research coverage. This skill adds the task-completeness check. |
| Code-review report | `writing-code-review-reports` once results exist, before drafting the requested/default report. It owns report structure, classifications, extras/minor/baseline sections, language, evidence, and safe delivery; use its Persian or consolidation reference when applicable. |

These are dependencies for the applicable stage, not optional alternatives with a duplicate local
fallback. If a required skill cannot be loaded, report the missing dependency and its effect, request
access to the skill or its content, and pause that stage. Continue unaffected authorized stages and
provide a bounded status if needed; do not invent a replacement workflow or install anything unasked.
Pure research reports do not require a code-review/reporting skill: use the research owner's delivery
guidance plus the task-specific conclusions in step 5. Mixed tasks use both branches.

The distinguishing goal is validating delivery of the task, not merely finding defects in a diff or
deciding merge readiness. A ticket reference alone does not select this workflow or its default report
file. Task-linked code inspection can use both skills: this one owns acceptance coordination and
`reviewing-code-changes` owns the inspection method. The user need not literally say “acceptance” when
asking whether the colleague's work is correctly and fully done, with real tests and edge cases.

Preserve the colleague's implementation and original report. Validation does not authorize fixes,
commits, publication, deployment, destructive resets, paid calls, or access outside permitted targets.
Follow the owner skills' safety/evidence rules and project/tool permissions in each stage.

By default, deliver **a Markdown report file for the author plus a short chat summary**. An explicit
chat-only request overrides this default; do not require another request for the file.

## 1. Establish What Is Being Accepted

If the task was already reviewed, open [follow-up validation](references/follow-up-validation.md)
before selecting scope or tests. Recover the prior target/evidence and current decisions, track each
previous finding's disposition, review the new delivery, and revalidate affected acceptance paths.
Use the same stage owners; a follow-up is neither a full restart nor merely ticking off old fixes.

Read the task text, approved clarifications, project guidance, and delivered artifacts. Establish:

- The task identity and intended user outcome; branch names and linked earlier experiments are not
  necessarily the current task ID. Retrieve a referenced acceptance experiment when its details matter.
- Each checkable requirement, important stated edge case, explicit non-goal, and approved constraint.
  Distinguish mandatory behavior from examples, preferences, and the author's design choices.
- The exact deliverable: base/head or local-change scope for each repository, document revision/sections,
  and components needed for the actual flow, including build, installation, workers, UI, or integrations.
- Available environments, tools, supplied test evidence, permitted writes, and any cost/credential limits.

Define expected behavior from the agreed task or independent contract before letting the implementation
frame the tests. Ask focused questions only where unresolved intent changes acceptance or safe execution.
Explain conflicting wording in ordinary language; do not silently choose the broader destructive reading.
Proceed with unaffected review/tests while a material question is open. If requirements are unavailable,
give a bounded correctness assessment, not invented criteria or an unqualified task-acceptance verdict.

Keep a compact requirement-to-evidence map, in working notes or the eventual report, not a mandatory
new planning document. Reuse the code-review owner's conformance map and status definitions rather
than producing another checklist. For research, map the brief's questions and required experiments to
the claim/coverage evidence collected with the research owner.
Track verification level separately: supplied result, source trace, executed unit/integration check, or
real end-to-end flow; this is independent of whether a criterion is met or still unresolved.

## 2. Inspect the Delivery in Its Real Context

### Implementation

Execute `reviewing-code-changes` for every agreed implementation component, using the same requirement
map and evidence throughout. Do not repeat its inspection or conformance pass here. Pass through the
user's material design/quality constraints without turning a preference into a new acceptance contract.

Before runtime claims, reconcile reviewed code with the running artifact: revisions, build inputs,
applied patches, image identity, mounts, effective configuration, and worker/frontend versions where
relevant. An old image or populated volume can both hide and invent a defect. Open
[acceptance verification](references/acceptance-verification.md) when planning tests or resolving
environment/build uncertainty; it covers real flows, boundaries, isolated setup, and evidence.

### Research or Security Report

Open [validating research deliverables](references/research-deliverables.md) for this branch. Check two
questions independently: **Are the claims sound?** and **Was the requested investigation completed?**
Use `research-with-evidence` for the first question and this skill's brief/experiment coverage for the
second. Do not run an unrelated repository-wide audit or adopt the author's claims as requirements.

## 3. Execute Acceptance Verification

Choose tests from the requirements and meaningful risks, not only tests already written by the author.
Open [acceptance verification](references/acceptance-verification.md) before designing or running this
pass. Use project norms, trustworthy current supplied evidence, and the smallest additional checks that
resolve material uncertainty. For check design and execution safety, use the code-review owner's
`references/test-design.md`; the local guide adds acceptance-flow coverage and runtime alignment,
not another test-design method.

When real testing is requested, execute the relevant shipped flow where safe and available. Unit tests,
manual helper calls, mocked services, and transport tests with a synthetic server prove narrower things;
label them accordingly. Cover the important edge/failure paths and integration seams. Select layers
according to the task: browser E2E is not necessary for a backend-only task, but invoking a job manually
does not prove its UI trigger or asynchronous handoff. If real execution is blocked, name the precise
missing permission/resource and its acceptance impact rather than replacing it silently with a mock.

Do not stop all verification at the first blocker. Complete other material, safe, authorized checks that
could expose independent failures or establish coverage. Skip a dependent flow when its prerequisite
is already broken, with the reason; don't spend resources repeating the same failure. “Full testing”
means accounted-for relevant requirements, paths, and risks, not every imaginable input or an automatic
whole-suite/staging run. Never claim all cases were tested.

Keep the applicable owners' evidence records with one shared acceptance/coverage map for handoff,
with acceptance cases/layers marked executed, supported
by supplied evidence, not applicable, blocked, or skipped with reason. Preserve manual-inspection data
under project rules and portable evidence needed for handoff; a lost temporary log is an inspectability
limit, not current reproducible evidence.

## 4. Challenge Findings and Close Material Gaps

Challenge candidate findings with their owner method. In the conformance pass, explicitly distinguish
acceptance-only fixtures from test scaffolding accidentally shipped as product functionality. Use the
code-review and reporting owners' classifications/severity; do not maintain a competing rubric here.

Use independent validation proportionately when delegation is authorized and available: for acceptance-
determining findings, high-risk security/data behavior, disputed evidence, or a required project gate.
For a code reviewer, use the review owner's `references/reviewer-brief.md`, adding the acceptance map
and disputed points. For a research reviewer, supply the brief, claim/completeness map, evidence, allowed
verification targets/writes, and an explicit request for the research method. Ask for confirmation,
refutation, and material coverage gaps, not fixes. If delegation is unavailable or prohibited, disclose
the independent-review limit; don't present self-checks as independent review or finalize with a reviewer
still in flight. Load `dispatching-parallel-agents` when coordinating substantial parallel work, not for
a lone reviewer you simply await.

New decisions, revisions, or environment changes reopen only dependent conclusions/checks. Replace
superseded claims explicitly in working evidence. Produce a coherent current report without retelling
every review round, while retaining unresolved conflicts and limitations that affect acceptance.

## 5. Deliver an Author-Facing Report

Use the requested path or an existing review-document convention. Otherwise choose a non-colliding
`<task-id>-review.md` (or `task-review.md`) within the authorized project directory. Read before updating
an existing target; don't overwrite unrelated work or write to a desktop/outside path without permission.
If no authorized writable path exists, provide the report in chat, state the file-delivery limitation,
and ask for a permitted destination only if needed; do not bypass a read-only boundary.
For a mixed task, deliver one integrated report with clear implementation/research evidence boundaries.
For follow-ups, pass prior-finding dispositions, new findings, current acceptance map, and retained
versus newly executed evidence to the applicable delivery owner. For code/mixed reports, use the code-
report owner's `references/consolidation-and-evidence.md` for earlier reports, drift, or conflicts;
for pure research, use the research owner and local trust/completeness guidance. Keep closed historical
items out of active findings while retaining a concise closure summary where useful.

For code or mixed deliveries, hand the completed findings, conformance map, acceptance-test results,
reviewer outcome, and limits to `writing-code-review-reports`. Use its report structure, Persian labels,
extras/minor/baseline rules, verdict rules, and delivery checks without recreating them here. Drafting the
report is not a second inspection/test pass. Add the research trust/completeness conclusions for mixed
tasks, with document/claim locators rather than fabricated code lines.

The coordinator retains the **whole-task acceptance conclusion** across all required deliverables.
Pass it to the report owner along with the separate branch assessments: a confirmed required gap in
either branch prevents overall acceptance; otherwise material unresolved evidence in either branch
leaves overall acceptance undetermined. Code readiness alone cannot make a mixed task Ready. Apply
the owners' existing finding/verdict rules, not a second severity rubric.

For pure research, use `research-with-evidence` delivery guidance to write the file in the reader's
language. State the task's acceptance conclusion, claim trustworthiness, coverage of the brief and
required experiments, confirmed omissions/extras, and material uncertainty with supporting locators.
Do not force a code-merge verdict/template onto a research task. Distinguish a confirmed required
deliverable gap from missing evidence: the former prevents acceptance; the latter leaves acceptance
undetermined until resolved. Reviewer-created evidence can strengthen claims without proving that the
colleague delivered a required artifact. Do not require author-committed tests/logs unless the task or
project requires them; reviewer evidence can otherwise verify acceptance.

For the pure-research handoff, redact credentials, secrets, unnecessary personal data, and private
environment identifiers; state material redactions. Use document/claim or revision-pinned locators and
portable reproduction evidence instead of machine-local paths as the sole evidence. This safety step
fills the research delivery boundary without borrowing a code-only report template.

Keep personal Q&A, unrelated working-tree trivia, and internal review-round history out of the author
handoff. Retain provenance and limitations that affect the engineering conclusion.

Before finishing, account for every agreed criterion, changed/delivered component, material finding, and
relevant untested path; reconcile the report with the latest valid evidence and reviewer outcome. Return
the report path, short verdict/reasons, checks and important limits, and any next required decision.

## Maintainer Checks

When changing this skill, use [evaluation scenarios](references/evaluation-scenarios.md) to check
selection separately from application. They are test inputs, not completed verification or extra steps
for every task validation.
