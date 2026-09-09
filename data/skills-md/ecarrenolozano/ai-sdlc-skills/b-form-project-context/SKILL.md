---
name: b-form-project-context
description: Transform an approved Clarified Project Request into an evidence-grounded, human-approved Project Context. Use after a-clarify-project-request when sdlc_docs/00_inception/clarified_project_request.md is Closed, Ready, fully approved, and has no blocking issues. Create or update sdlc_docs/00_inception/project_context.md, maintain the Project context row and update only the authorized handoff fields of the Initial requirements row after valid approval in sdlc_docs/trace_workflow.md, ask project-level questions in small rounds when needed, and define the problem, purpose, goal, users, high-level scope, MVP boundary, constraints, assumptions, dependencies, risks, success criteria, and confirmed responsibilities without creating detailed requirements, user stories, architecture, implementation plans, or test plans.
---

# Project Context Formation

## Purpose

Convert an approved `Clarified Project Request` into the official high-level definition of a software project.

Produce a concise `project_context.md` that explains:

- What problem the project addresses.
- What result the project should create.
- Who will use, decide on, build, or review the result when confirmed.
- What the first useful software version includes and excludes.
- Which confirmed limits, dependencies, risks, assumptions, and uncertainties affect the work.
- How a human reviewer decides that the context is ready for Product Requirements Management.

Do not generate detailed requirements, user stories, acceptance criteria, architecture, implementation plans, repository issues, or test plans.

## Required Inputs

Use these project-owned files:

```text
sdlc_docs/00_inception/clarified_project_request.md
sdlc_docs/trace_workflow.md
```

Proceed only when the Clarified Project Request satisfies all conditions:

- `Document state` is `Closed`.
- `Ready` is selected.
- The approver name, role, and date are present.
- `Blocking Issues` is `None`.

If any approval condition fails, stop and report the exact failure.

`trace_workflow.md` is owned by the project template. Verify and update it, but never create, reconstruct, or replace it. If it is missing, stop and report the structural inconsistency.

Use original informal sources only as supporting evidence when a statement in the approved request needs verification. Do not restart Project Request Clarification.

## Output

Create or update:

```text
sdlc_docs/00_inception/project_context.md
```

Use `references/project-context-template.md`.

## Grounding Policy

Treat only the approved Clarified Project Request and explicit recorded stakeholder answers as confirmed project facts.

Classify substantive information as one of:

- `Confirmed fact`: directly supported by approved evidence.
- `Derived interpretation`: a project-level conclusion logically derived from confirmed facts; state its basis.
- `Assumption`: unconfirmed information temporarily used to continue; state why it is needed and how it will be confirmed.
- `Open question`: important information that is unknown or contradictory.
- `Approved decision`: an explicit human decision recorded in approved evidence.

Never present a derived interpretation, common practice, or plausible technical choice as a confirmed fact. When evidence is insufficient, preserve the gap and request clarification. An incomplete but grounded document is preferable to a complete-looking document containing unsupported claims.

## Mixed-Statement Rule

Do not classify an entire statement as a confirmed fact when only part of it is directly supported.

Split mixed statements into separate entries:

- the source-supported fact; and
- the consequence, interpretation, risk, or recommendation derived from it.

Example:

- `Confirmed fact`: The first release has a one-day delivery constraint.
- `Derived interpretation`: The deadline requires keeping the first-release scope tightly focused.

## Classification Promotion

When new stakeholder evidence explicitly confirms a previous derived interpretation:

1. reclassify the statement as an `Approved decision` or `Confirmed fact`, according to its meaning;
2. record the new evidence and its source;
3. update every occurrence of the statement across the Project Context;
4. do not preserve conflicting classifications in other sections;
5. rerun classification consistency validation before requesting approval.

## Classification Consistency

Use the same classification for the same substantive statement everywhere it appears.

Before validation, compare the statement across:

- Project Summary
- Evidence and Classification Register
- Desired Future Situation
- High-Level Scope
- MVP Boundary
- Constraints
- Risks and Uncertainties
- Confirmed Decisions and Responsibilities

Treat conflicting classifications as a blocking validation failure.

## Operating Modes

### Draft

Use when `project_context.md` does not exist.

- Create it from the bundled template.
- Set `Document state` to `Draft`.
- Populate only supported information.
- Mark unsupported non-blocking content as `Not identified in the approved source`.

### Update

Use when the document already exists, answers arrive, new approved evidence appears, or a reviewer selects `Not Ready`.

- Preserve supported content and valid document history.
- Integrate new evidence and reviewer feedback.
- Remove stale or contradictory statements.
- When substantive content changes in a `Closed` document, preserve the prior approved version in version control, increment the version, set `Document state` to `Under Clarification`, clear the active approval fields, and require a new approval cycle.

### Review

Use before human approval.

- Run every validation invariant.
- Remove temporary Working Questions after answers are integrated.
- Remove unsupported, duplicated, stale, or overly technical content.
- Do not make the human approval decision.

## Workflow

1. Receive `sdlc_docs/00_inception/clarified_project_request.md`.
2. Verify that the Clarified Project Request is `Closed`, `Ready`, fully approved, and has `Blocking Issues: None`.
3. If the approval gate is invalid, stop and report each failed condition.
4. Verify that `sdlc_docs/trace_workflow.md` exists.
5. If `trace_workflow.md` is missing, stop and report that the project template must provide it; do not create or reconstruct it.
6. Update only the authorized fields of the `Project context` row to `In Progress`, set `Current activity` to `Project Context Formation`, record the approved Clarified Project Request as evidence, record the current gap, and set `Next action` to `Continue b-form-project-context`; apply the Traceability Mutation Guard before saving.
7. Preserve all unrelated traceability rows.
8. Check whether `sdlc_docs/00_inception/project_context.md` exists.
9. If it does not exist, create it from `references/project-context-template.md` and set `Document state` to `Draft`.
10. If it exists, load it and preserve supported information and valid document history.
11. Check whether an existing Project Context is `Closed` and new stakeholder evidence, a new project-level decision, or reviewer feedback changes substantive content.
12. If a closed Project Context is affected, preserve the previously approved version through version control.
13. When Step 12 applies, increment the document version.
14. When Step 12 applies, set `Document state` to `Under Clarification`.
15. When Step 12 applies, clear the active approval selection, reviewer name, reviewer role or responsibility, approval date, and blocking issues or feedback.
16. When Step 12 applies, record the new evidence and its source before changing affected project statements.
17. Extract confirmed project-level information from the approved request and any newly recorded evidence.
18. Classify each substantive statement as a confirmed fact, derived interpretation, assumption, open question, or approved decision.
19. Record the evidence basis for every confirmed fact, derived interpretation, and approved decision.
20. Draft or update every affected substantive section; do not assume that a classification change affects only the Evidence and Classification Register.
21. For unsupported non-blocking content, write `Not identified in the approved source` rather than inventing an answer.
22. Do not convert missing information into a negative fact.
23. Check whether essential project-level information is missing, contradictory, or insufficiently precise.
24. If no essential uncertainty exists, continue to Step 42.
25. Identify all material uncertainties, but do not ask all possible questions at once.
26. Create or update temporary Working Questions, with a maximum of 20 distinct project-level questions across the entire lifecycle of this document.
27. Do not repeat questions already answered in approved evidence or earlier recorded answers.
28. Select only the next small round of highest-value questions, normally one to four.
29. Set `Document state` to `Under Clarification`.
30. Update only the authorized fields of the `Project context` row to show `Under Clarification`, the Project Context draft as evidence, the unresolved questions or contradictions, and `Next action: Continue b-form-project-context`; apply the Traceability Mutation Guard before saving.
31. Ask the selected small round and stop the current execution until stakeholder answers are available.
32. When answers or new stakeholder evidence are available, record each statement, who provided it, its evidence source, and its impact.
33. Determine whether the new evidence confirms, changes, or contradicts an existing confirmed fact, derived interpretation, assumption, open question, or approved decision.
34. When explicit stakeholder evidence confirms a previous derived interpretation, promote it to `Approved decision` or `Confirmed fact`, according to its meaning.
35. Check whether any affected statement combines a source-supported fact with a derived consequence, risk, interpretation, or recommendation.
36. If a mixed statement exists, split it into separate statements and classify each one independently.
37. Update every occurrence of the affected information across the Project Context, including the Evidence and Classification Register, summary, scope, constraints, risks, decisions, and other affected sections.
38. Preserve new source evidence without rewriting or replacing original evidence.
39. Check whether the same substantive statement now has conflicting classifications in different sections.
40. If classifications conflict, keep `Document state` as `Under Clarification`, record a blocking validation failure, and correct all affected occurrences before continuing.
41. Return to Step 23.
42. Run the validation invariants in `Validation Invariants`.
43. If any invariant fails, set or keep `Document state` as `Under Clarification`.
44. Convert each failure into a revision item or, only when human information is required, a Working Question.
45. Update only the authorized fields of the `Project context` row with the blocking validation failures and `Next action: Continue b-form-project-context`; apply the Traceability Mutation Guard before saving.
46. Resolve the failures and return to Step 23.
47. When every invariant passes, remove the temporary Working Questions section.
48. Set `Document state` to `Pending Approval`.
49. Update only the authorized fields of the `Project context` row to `In Progress`, record the Project Context as evidence, record `Human approval pending`, and set `Next action` to `Obtain human approval`; apply the Traceability Mutation Guard before saving.
50. Submit the document to an authorized human reviewer and stop until a decision is available.
51. Require the reviewer to select exactly one of `Ready for Product Requirements` or `Not Ready` and record name, role or responsibility, date, and blocking issues or feedback.
52. If the review record is incomplete or both/neither decisions are selected, keep `Pending Approval`, request completion, and stop.
53. If `Ready for Product Requirements` is selected while blocking issues or feedback are not `None`, treat the review as contradictory, request correction, and stop.
54. If `Not Ready` is selected, keep the document open and set `Document state` to `Under Clarification`.
55. Treat reviewer feedback as required revision evidence.
56. Clear the current approval selection and approval fields before resubmission while preserving the prior decision in version control.
57. Update only the authorized fields of the `Project context` row to `In Progress`, record the feedback as the current blocker, and set `Next action` to `Continue b-form-project-context`; apply the Traceability Mutation Guard before saving.
58. Return to Step 20.
59. If a complete and internally consistent `Ready for Product Requirements` decision is recorded with `Blocking Issues or Feedback: None`, set `Document state` to `Closed`.
60. Update only the authorized fields of the `Project context` row to `Complete`, set `Current activity` to `Project Context Formation`, record the approved Project Context as evidence, set `Missing or blocked` to `None`, and set `Next action` to `Run c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
61. Update only the authorized handoff fields of the `Initial requirements` row: leave `Status`, `Item`, and `Type` unchanged; set `Current activity` to `Product Requirements Management`, record the approved Project Context as available evidence, state that Product Requirements have not been created, and set `Next action` to `Run c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
62. Preserve all unrelated rows and existing evidence not superseded by the completed stage.
63. Deliver the approved Project Context as the input to `c-manage-product-requirements`.
64. Report the files read, files modified, assumptions introduced, open questions remaining, validation failures, approval state, authorized traceability fields changed, and any unauthorized traceability changes detected or rejected.

## Traceability Ownership

`b-form-project-context` owns these updates:

- The `Project context` row throughout Project Context Formation.
- The handoff fields in the `Initial requirements` row only after valid approval.

It must not change the status or evidence of unrelated rows. It must not mark `Initial requirements` as started or complete.

## Traceability Mutation Guard

Before the first `trace_workflow.md` mutation in each execution, copy the current file to a temporary location outside the project repository. Do not create a persistent backup file in `sdlc_docs/`.

Authorized fields:

- `Project context`: `Status`, `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.
- `Initial requirements`, only after valid Project Context approval: `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.

Forbidden mutations:

- `Item` or `Type` in any row.
- `Status` in the `Initial requirements` row.
- Any field in `Project request`, `Repository preparation`, or any other unrelated row.
- Adding, removing, renaming, or reordering rows.
- Global terminology cleanup outside authorized fields.

For every proposed traceability update:

1. compare the temporary before-copy with the proposed after-file;
2. run `.agents/skills/b-form-project-context/scripts/validate_trace_mutation.py` with the exact authorized fields for that execution;
3. reject the update and restore the before-copy when the script reports an unauthorized change;
4. do not report success until the guard passes;
5. report the exact authorized fields changed and the count of unauthorized changes.

Example after valid approval:

```bash
python3 .agents/skills/b-form-project-context/scripts/validate_trace_mutation.py /tmp/trace-before.md sdlc_docs/trace_workflow.md \
  --allow-field "Project context:Status" \
  --allow-field "Project context:Current activity" \
  --allow-field "Project context:Evidence" \
  --allow-field "Project context:Missing or blocked" \
  --allow-field "Project context:Next action" \
  --allow-field "Initial requirements:Current activity" \
  --allow-field "Initial requirements:Evidence" \
  --allow-field "Initial requirements:Missing or blocked" \
  --allow-field "Initial requirements:Next action"
```

### Runtime Script Resolution and Failure Rule

Resolve the mutation guard from the repository root using this exact path:

```text
.agents/skills/b-form-project-context/scripts/validate_trace_mutation.py
```

Do not resolve the script relative to the current working directory, the active document, or a generic `scripts/` directory.

The guard is mandatory. If the script is missing, inaccessible, cannot execute, or returns an unexpected error:

1. do not replace it with a manual, inferred, or model-based comparison;
2. do not save the proposed `trace_workflow.md` mutation;
3. preserve or restore the original `trace_workflow.md` from the temporary before-copy;
4. stop the workflow at the current step;
5. report the exact script path, command attempted, exit code when available, and failure output.

Only an executed guard result with exit code `0` authorizes saving the proposed traceability mutation. A guard result with exit code `1` means the proposed mutation is unauthorized and must be rejected. Any other exit code is a validator failure and must stop the workflow.

### Workflow Identifier Normalization

Within the `Project context` row and the authorized handoff fields of the `Initial requirements` row, use exact technical identifiers:

- `b-form-project-context`
- `c-manage-product-requirements`

Replace obsolete single-letter skill labels only in rows and fields that `b-form-project-context` owns.

Do not modify unrelated rows solely to normalize terminology.

## Document State Rules

- `Draft`: created but not yet fully analyzed.
- `Under Clarification`: evidence, answers, revisions, or review feedback still require resolution.
- `Pending Approval`: all validation invariants pass and a human decision is pending.
- `Closed`: a human selected `Ready for Product Requirements`, reviewer information is complete, and `Blocking Issues or Feedback` is `None`.

`Not Ready` is a review decision, not a document state and not a terminal state.

## Working Question Rules

- Ask no more than 20 distinct questions across the document lifecycle.
- Ask fewer whenever sufficient.
- Ask only the next small round, normally one to four questions.
- Stop and wait after presenting a round.
- Ask only questions needed for a coherent or approvable Project Context.
- Do not repeat questions already answered.
- Record who answered, the evidence source, the answer, and its impact.
- Remove Working Questions before approval.

Do not ask for detailed requirements, frameworks, libraries, components, schemas, API contracts, algorithms, repository structure, deployment configuration, or test cases unless one is already a confirmed project constraint.

## Validation Invariants

Before setting `Pending Approval`, verify all conditions:

- The approved Clarified Project Request was not modified.
- The Traceability Mutation Guard passed for every `trace_workflow.md` write in the current execution.
- The guard was executed from `.agents/skills/b-form-project-context/scripts/validate_trace_mutation.py`; no manual fallback was used.
- The before-and-after traceability comparison contains no unauthorized row or field changes.
- Every confirmed fact and approved decision has evidence.
- Every derived interpretation is labeled and states its basis.
- No substantive statement has conflicting classifications across sections.
- No statement classified as a confirmed fact combines confirmed evidence with an inferred consequence.
- Every mixed confirmed-and-derived statement has been split and classified independently.
- Every stakeholder-confirmed derived interpretation has been promoted to an `Approved decision` or `Confirmed fact`, according to its meaning.
- Every classification change has been applied consistently to all affected occurrences.
- Every assumption is labeled and includes a confirmation path.
- No open question is presented as resolved.
- Problem, goal, outcomes, scope, MVP boundary, constraints, and success criteria are mutually consistent.
- Explicit exclusions do not contradict included scope.
- Responsibilities are recorded only when confirmed.
- No detailed requirements, user stories, architecture, implementation, issue, or test content was introduced.
- Temporary Working Questions have been removed.
- No known blocking issue remains.

A validation failure prevents `Pending Approval`.

## MVP Boundary Rules

Define only the intended user, minimum useful outcome, high-level capabilities, explicit exclusions, confirmed delivery limits, and an observable completion condition. Do not decompose the MVP into stories, detailed behavior, tasks, or technical components.

## Plain-Language Rules

Write for readers with little prior knowledge of product or software-development terminology. Prefer concrete descriptions. Do not invent titles or responsibilities. Explain unavoidable terminology briefly.

## Human Approval Boundary

The skill may draft, update, validate, and submit the Project Context. It must never select a review decision, invent reviewer data, invent stakeholder answers, or treat AI review as formal approval.

The Golden Example contains fictional approval data only to demonstrate a valid final state.

## References

- Use `references/project-context-template.md` when creating the document.
- Use `references/process-flowchart.md` as the visual representation of the numbered workflow.
- Use `references/golden-example/in-approved-clarified-project-request.md` as the Golden Input.
- Use `references/golden-example/out-approved-project-context.md` as the Golden Output.
- Use `.agents/skills/b-form-project-context/scripts/validate_trace_mutation.py` before saving any traceability change.
- Use `.agents/skills/b-form-project-context/scripts/validate_workflow_alignment.py` when maintaining this skill to verify that the numbered workflow and Mermaid flowchart remain aligned.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
