---
name: c-manage-product-requirements
description: Transform an approved Project Context or triaged imported repository issues into evidence-grounded, human-approved product requirements, atomic user stories, and acceptance criteria in sdlc_docs/01_requirements/product_requirements.md. Use for the initial release after b-form-project-context, or for a later increment after e-sync-repository-requirements imports accepted issues. Build explicit source-scope coverage, prevent silent capability omissions and unsupported story grouping, preserve approved requirements, ask blocking questions in small rounds, prevent duplicate repository stories, maintain only authorized traceability fields, and prepare the handoff to d-design-product-architecture or e-sync-repository-requirements without editing remote issues.
---

# Product Requirements Management

## Purpose

Maintain one canonical product requirements document:

```text
sdlc_docs/01_requirements/product_requirements.md
```

Use a two-level hierarchy:

```text
REQ
└── one or more US
```

Keep acceptance criteria inside each user story. Do not create acceptance-criterion issues.

Do not design architecture, choose frameworks, create implementation tasks, edit remote repository issues, or approve requirements on behalf of a human.

## Required Inputs

Always require:

```text
sdlc_docs/trace_workflow.md
```

The traceability file is owned by the project template. Verify and update authorized fields, but never create, reconstruct, replace, rename, or globally normalize it. If it is missing, stop and report the structural inconsistency.

Choose exactly one operating mode from the available evidence. Do not guess.

### Initial Release

Require an approved:

```text
sdlc_docs/00_inception/project_context.md
```

Proceed only when:

- `Document state` is `Closed`.
- `Ready for Product Requirements` is selected.
- Reviewer name, role or responsibility, and date are present.
- `Blocking Issues or Feedback` is `None`.

### Product Increment

Require:

- the current `sdlc_docs/01_requirements/product_requirements.md`;
- one or more repository issues already imported by `e-sync-repository-requirements` as unapproved requirements;
- an explicit imported classification of `broad-request` or `user-story`;
- the source repository issue reference;
- the corresponding active increment row in `sdlc_docs/trace_workflow.md`.

Do not read or modify the remote repository directly. `e-sync-repository-requirements` owns repository reads and writes.

## Output

Create or update:

```text
sdlc_docs/01_requirements/product_requirements.md
```

Use `references/product-requirements-template.md`.

Keep these top-level sections:

1. Document Control
2. Requirements Overview
3. Requirements
4. Approval Record

## Grounding Policy

Treat only these sources as evidence:

- the approved Project Context for the initial release;
- imported triaged issue content for a product increment;
- explicit stakeholder answers recorded during Product Requirements Management;
- existing approved requirements only as immutable historical context.

For every requirement, story, and acceptance criterion:

- record its source or evidence basis;
- do not silently add fields, behavior, limits, roles, error handling, formats, or workflow details;
- ask when missing detail is necessary for an observable or testable outcome;
- omit non-blocking detail that is not supported;
- prefer an incomplete but grounded requirement over a complete-looking invented requirement.

A high-level capability in Project Context is not automatically a detailed requirement. Refine it only as far as approved evidence and recorded answers support.

## Approved-Content Immutability

An approved requirement is immutable.

- Do not rewrite its description, stories, acceptance criteria, source, or approval record.
- Create a new requirement for a later approved product change.
- Preserve retired requirements and IDs as history.
- Never reuse an existing REQ or US identifier.

## Repository Representation Rules

### Imported `broad-request`

- Keep the original issue as the requirement source.
- Generate one or more stories only after clarification.
- Preserve the original issue as a possible future repository container.
- Mark generated story repository references as `Not created`.
- If refinement produces one story, do not require a separate parent issue; `e-sync-repository-requirements` may reuse the original issue as that story.

### Imported `user-story`

- Keep a documentation-only requirement grouping.
- Reuse the original issue as the story repository reference.
- Do not create or request a requirement issue.
- Do not duplicate the user-story issue.

## Status Rules

Requirement statuses:

- `Unapproved`
- `Under Clarification`
- `Pending Approval`
- `Approved`
- `Retired`

User story statuses:

- `Draft`
- `Pending Approval`
- `Approved`
- `Retired`

Repository states recorded in the document:

- `Not created`
- `Open`
- `Closed`

## Scope Coverage, Source Decomposition, and Story Atomicity

Maintain both of these structures under Requirements Overview:

1. `Source Statement Coverage Register`, with stable `SRC-NNN` identifiers for every controlling source statement.
2. `Source Scope Coverage Matrix`, with stable `CAP-NNN` identifiers for atomic user-observable capabilities.

For the initial release:

- inspect all confirmed included product outcomes in Project Summary, Expected Outcomes, High-Level Scope `Included`, MVP `Included High-Level Capabilities`, and Success Criteria;
- use `Included High-Level Capabilities` as the controlling deterministic list when it exists;
- copy every controlling statement exactly into the Source Statement Coverage Register;
- classify each source statement as `Atomic`, `Compound`, or `Umbrella`;
- map every source statement to the CAP IDs that satisfy it.

Use these source-statement roles:

- `Atomic`: one independently observable outcome; map to exactly one CAP ID.
- `Compound`: two or more independently observable outcomes joined in one statement; decompose into at least two CAP IDs.
- `Umbrella`: a broad category such as manage, handle, support, maintain, administer, or operate; decompose into at least two concrete CAP IDs and begin the rationale with `Umbrella decomposition —`.

Never create an atomic capability or user story whose primary outcome is an umbrella verb. When more specific approved statements already define the behavior, use them to satisfy the umbrella statement without asking what the umbrella verb means. Ask a clarification only when the approved evidence contains no sufficiently specific outcomes.

For a product increment, apply the same rules to the exact imported issue content and recorded refinement answers.

Every atomic capability must have exactly one explicit disposition:

- `Covered`;
- `Grouped`;
- `Pending clarification`;
- `Deferred by approved decision`;
- `Excluded by approved decision`.

Do not silently omit a confirmed source statement or atomic capability. `Deferred` and `Excluded` require an explicit approved decision and evidence. `Grouped` requires explicit human approval; begin its rationale with `Approved grouping —`.

Every story must record:

- `Covered scope IDs`;
- `Atomicity: Single observable outcome`, or `Approved grouping — <rationale and approval evidence>`.

Editing and deleting, creating and moving, or other independently observable outcomes must be separate stories unless a human explicitly approves the grouping. Similar implementation, shared screens, convenience, or an umbrella verb are not valid grouping reasons.

### Validator Report Synchronization

The scope validator has two passes:

1. Run without `--require-report-sync` and capture the exact command, exit code, errors, and `requirement_reports[].expected` values.
2. Write the exact result into each active Requirement Validation block, then rerun with `--require-report-sync`.

Use these report values exactly:

- `Preflight passed` for a structurally valid requirement that remains Draft, Unapproved, or Under Clarification.
- `Passed` for a structurally valid requirement in Pending Approval or Approved state.
- `Failed` when structural validation fails.

Also record the exact validator command and `Scope validator report synchronized: Yes`. Never report a validator result in the assistant summary that differs from the saved Product Requirements document.

## Workflow

1. Receive `sdlc_docs/trace_workflow.md`.
2. Verify that `trace_workflow.md` exists.
3. If it is missing, stop and report that the project template must provide it; do not create or reconstruct it.
4. Determine from available evidence whether the mode is `initial release` or `product increment`; do not guess when both or neither are valid.
5. Before the first traceability mutation in the current execution, copy `trace_workflow.md` to a temporary location outside the repository.
6. If the mode is `initial release`, continue to Step 7; if it is `product increment`, continue to Step 13.
7. Verify that `project_context.md` is `Closed`, has `Ready for Product Requirements` selected, contains complete reviewer data, and has `Blocking Issues or Feedback: None`.
8. If the Project Context approval gate is invalid, stop and report every failed condition.
9. Verify that the `Initial requirements` row exists in `trace_workflow.md`.
10. If the row is missing, stop and report the structural inconsistency.
11. Update only authorized fields of `Initial requirements` to `In Progress`, activity `Product Requirements Management`, evidence pointing to the approved Project Context, the current requirements gap, and `Next action: Continue c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
12. Load the existing Product Requirements document or create it from the template, preserve approved content, set the mode to `Initial release`, and continue to Step 20.
13. Load the current Product Requirements document.
14. Identify only imported requirements with status `Unapproved` or `Under Clarification`, an explicit `broad-request` or `user-story` classification, and a source issue reference.
15. Verify that the corresponding active increment row exists in `trace_workflow.md`.
16. If imported evidence or the active increment row is missing, stop and report the exact missing input.
17. Update only authorized fields of the active increment row to `In Progress`, activity `Requirements Refinement`, evidence pointing to the imported requirement and source issue, the current clarification or approval gap, and `Next action: Continue c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
18. Preserve all approved requirements, stories, criteria, identifiers, source rows, capability rows, and approval records unchanged.
19. Set the mode to `Product increment` and continue to Step 20.
20. Select the next unapproved requirement in the active scope; review one requirement at a time unless the user explicitly requests a batch.
21. Extract every controlling confirmed included source statement for the active scope; for an initial release use `Included High-Level Capabilities` when present and use the other approved sections as consistency evidence.
22. Create or update the Source Statement Coverage Register with stable `SRC-NNN` identifiers, exact statements, locations, roles, CAP decompositions, and rationale.
23. Create or update the Source Scope Coverage Matrix with stable `CAP-NNN` identifiers, atomic capabilities, source IDs, dispositions, and story mappings.
24. Decompose every `Compound` or `Umbrella` source statement into concrete CAP IDs; never create a CAP or story whose primary outcome is an umbrella verb.
25. Record the source or evidence basis for the requirement, every source row, every atomic capability, and each story.
26. Create or update provisional Draft story skeletons for every active CAP so omissions are visible; do not invent acceptance details that require clarification.
27. Map every story to `Covered scope IDs`, every CAP back to its stories, and every source row bidirectionally to its CAP IDs.
28. Run the Scope Coverage Validator without `--require-report-sync` as a structural preflight.
29. If the validator is missing, inaccessible, cannot execute, or returns an unexpected exit code, do not use manual validation; keep content unapproved, stop, and report the command and failure.
30. Write the exact validator command and expected report status into every active Requirement Validation block and set `Scope validator report synchronized: Yes`.
31. Rerun the same validator with `--require-report-sync`.
32. If the synchronized preflight returns exit code `1`, keep the scope `Under Clarification`, record every structural revision item, update the authorized traceability row using the Mutation Guard, correct the document, and return to Step 21; any other nonzero exit code stops the workflow.
33. Determine whether blocking information is missing for a meaningful user outcome, testable acceptance criterion, capability disposition, or atomic story boundary.
34. If no blocking information is missing, continue to Step 44.
35. Create or update temporary Working Questions, with a maximum of 20 distinct questions for the active requirement lifecycle.
36. Do not repeat questions answered by approved evidence, the imported issue, earlier answers, or preserved approved content; do not ask what an umbrella verb means when concrete approved outcomes already decompose it.
37. Select only the next small round of highest-value questions, normally one to four.
38. Set the affected requirement to `Under Clarification`, keep affected stories as `Draft`, and mark unresolved capability rows `Pending clarification`.
39. Update only the authorized traceability row with unresolved questions and `Next action: Continue c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
40. Ask the selected round and stop the current execution until stakeholder answers are available.
41. When answers are available, record who answered, the evidence source, the answer, and its impact.
42. Update only the affected unapproved requirement, source row, capability row, story, or criterion.
43. Return to Step 21 so source decomposition, coverage, and report synchronization are recalculated.
44. Finalize one or more stories under the requirement, or refine the existing story when the imported issue is classified as `user-story`.
45. Map each story to its `Covered scope IDs` and map every covered matrix row back to the owning requirement and stories.
46. Split stories by independently observable user outcomes and reject umbrella-action stories; a story covering multiple CAP IDs requires explicit `Approved grouping —` evidence.
47. If independently observable outcomes are combined or an umbrella story remains without approved grouping, return to Step 35 and ask for a split or a human grouping decision.
48. Preserve the original repository issue reference according to the Repository Representation Rules and do not create duplicate story references.
49. Add testable acceptance criteria supported by evidence, using Given/When/Then when suitable.
50. If a testable criterion requires an unstated behavior, return to Step 35 instead of inventing it.
51. Remove temporary Working Questions for the affected requirement.
52. Set the affected requirement and reviewed stories to `Pending Approval` and set the active scope state to `Pending Approval`.
53. Run the Scope Coverage Validator without `--require-report-sync` and capture its exact expected report status.
54. If the validator cannot execute or returns an unexpected exit code, restore `Under Clarification`, stop, and report the exact command and failure without manual fallback.
55. Update each active Requirement Validation block with the exact command, status, errors, and `Scope validator report synchronized: Yes`.
56. Rerun the validator with `--require-report-sync`.
57. If synchronized scope validation fails, restore `Under Clarification`, record concrete revision items, update the authorized traceability row with blockers using the Mutation Guard, and return to Step 33.
58. Run all remaining checks in `Validation Invariants` for the affected requirement, stories, source register, capability matrix, and active scope.
59. If any remaining invariant fails, restore `Under Clarification`, record concrete revision items, update the authorized traceability row with blockers using the Mutation Guard, and return to Step 33.
60. Present the requirement title, description, source evidence, source register rows, capability rows, stories, acceptance criteria, source issue, validator command and synchronized result, and intended repository representation to an authorized human reviewer, then stop.
61. Require exactly one review outcome: `Approved` or concrete corrections, plus reviewer name, role or responsibility, date, and blocking issues or feedback.
62. If the review record is incomplete, keep `Pending Approval`, request the missing review data, and stop.
63. If `Approved` is recorded while `Blocking Issues or Feedback` is not exactly `None`, treat the review as contradictory, request correction, and stop.
64. If corrections are requested, set the affected requirement and stories to `Under Clarification`, clear the active approval fields, preserve the prior review in version control, and record the feedback as evidence.
65. Update only the authorized traceability row with the review blocker and `Next action: Continue c-manage-product-requirements`; apply the Traceability Mutation Guard before saving.
66. Return to Step 33.
67. When a complete and internally consistent `Approved` decision is recorded, mark the requirement and its stories `Approved` and preserve reviewer data.
68. Update the Requirements Overview, Source Statement Coverage Register, Source Scope Coverage Matrix, and Approval Record without changing previously approved items.
69. If another unapproved requirement remains in the active scope, return to Step 20.
70. Save `sdlc_docs/01_requirements/product_requirements.md`.
71. If the mode is `initial release`, update only authorized fields of `Initial requirements` to `Complete`, activity `Product Requirements Management`, evidence pointing to the approved Product Requirements, `Missing or blocked: None`, and `Next action: Run d-design-product-architecture`; apply the Traceability Mutation Guard before saving.
72. If the mode is `initial release`, update only the authorized handoff fields of `Repository preparation`: leave `Item`, `Type`, and `Status` unchanged; set activity `Product Architecture Design`, evidence pointing to the approved Product Requirements, the missing architecture work, and `Next action: Run d-design-product-architecture`; also refresh the existing `Architecture` row only when its status is `Not Started`: set activity `Product Architecture Design`, evidence pointing to the approved Product Requirements, `Missing or blocked: Architecture baseline not created`, and `Next action: Run d-design-product-architecture`. Preserve its `Item`, `Type`, and `Status`. If the row is absent, report the structural gap to the orchestrator instead of adding it; if architecture has already started, preserve its fields and evidence. Apply the Traceability Mutation Guard before saving.
73. If the mode is `product increment`, update only authorized fields of the active increment row: keep `Status` as `In Progress`, set activity `Repository Synchronization` when there is no material architectural impact, or `Product Architecture Design` when there is material architectural impact. Record the approved requirement and stories as evidence, record the pending handoff, and set `Next action` to `Run e-sync-repository-requirements` when no architecture change is needed or `Run d-design-product-architecture` when material architecture work is needed; apply the Traceability Mutation Guard before saving.
74. Preserve every unrelated row and every field outside the authorized mutation set.
75. Deliver the approved Product Requirements as input to `d-design-product-architecture` for the initial workflow. For an approved increment with no material architectural impact, deliver the approved requirement to `e-sync-repository-requirements`; when material architectural impact exists, route through `d-design-product-architecture` before synchronization.
76. Report the mode, files read, files modified, questions asked, approval state, approved REQ/US IDs, SRC/CAP IDs and dispositions, both validator commands and synchronized results, authorized traceability fields changed, and any unauthorized changes detected or rejected.

## Working Question Rules

- Ask no more than 20 distinct questions for an active requirement lifecycle.
- Ask fewer whenever sufficient.
- Ask only the next small round, normally one to four.
- Stop after presenting a round.
- Ask only questions needed for a user-observable outcome or testable acceptance criterion.
- Do not ask for frameworks, libraries, components, schemas, API contracts, algorithms, repository structure, deployment configuration, or implementation tasks unless one is already a confirmed product constraint.

## Human Approval Boundary

The skill may draft, refine, validate, and submit requirements. It must not select `Approved`, invent reviewer data, infer approval from silence, or treat AI review as human approval.

A valid approval requires:

- an explicit `Approved` decision;
- reviewer name;
- reviewer role or responsibility;
- approval date;
- `Blocking Issues or Feedback: None`.

## Traceability Ownership

`c-manage-product-requirements` owns:

### Initial Release

- `Initial requirements`: `Status`, `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.
- `Repository preparation`, only after all active initial-release requirements are validly approved: `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.

- `Architecture`, only after all active initial-release requirements are validly approved and only while the existing row is `Not Started`: `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.

It must not change `Architecture` or `Repository preparation` status.

### Product Increment

- The active increment row during `Requirements Refinement` and the handoff to `Repository Synchronization`: `Status`, `Current activity`, `Evidence`, `Missing or blocked`, and `Next action`.

It must not add, remove, rename, or reorder foundation rows. It must not modify `Project request`, `Project context`, or unrelated increment rows.

## Traceability Mutation Guard

Before each traceability write:

1. compare the temporary before-copy with the proposed after-file;
2. run `.agents/skills/c-manage-product-requirements/scripts/validate_trace_mutation.py` using the exact authorized row and fields for the current mode;
3. reject the update and restore the before-copy when any unauthorized change appears;
4. do not perform global terminology cleanup outside owned fields;
5. report actual changed fields and unauthorized-change count.

For an initial-release handoff, authorize only:

```text
Initial requirements: Status, Current activity, Evidence, Missing or blocked, Next action
Repository preparation: Current activity, Evidence, Missing or blocked, Next action
Architecture: Current activity, Evidence, Missing or blocked, Next action
```

Include the Architecture allowances only for an existing `Not Started` row. Pass each allowed pair separately as `--allow-field "Architecture:Current activity"`, `--allow-field "Architecture:Evidence"`, `--allow-field "Architecture:Missing or blocked"`, and `--allow-field "Architecture:Next action"`; never authorize `Architecture:Status`.

For an increment, authorize only the active increment row fields:

```text
Status, Current activity, Evidence, Missing or blocked, Next action
```

### Runtime Script Resolution and Failure Rule

Resolve the mutation guard from the repository root using this exact path:

```text
.agents/skills/c-manage-product-requirements/scripts/validate_trace_mutation.py
```

Do not resolve the script relative to the current working directory, the active document, or a generic `scripts/` directory.

The guard is mandatory. If the script is missing, inaccessible, cannot execute, or returns an unexpected error:

1. do not replace it with a manual, inferred, or model-based comparison;
2. do not save the proposed `trace_workflow.md` mutation;
3. preserve or restore the original `trace_workflow.md` from the temporary before-copy;
4. stop the workflow at the current step;
5. report the exact script path, command attempted, exit code when available, and failure output.

Only an executed guard result with exit code `0` authorizes saving the proposed traceability mutation. A guard result with exit code `1` means the proposed mutation is unauthorized and must be rejected. Any other exit code is a validator failure and must stop the workflow.

## Scope Coverage Validator

Run the validator from the repository root with the exact bundled path.

Initial-release preflight:

```text
python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release
```

Initial-release synchronized verification:

```text
python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync
```

For a product increment, use the exact imported source artifact and `--mode product-increment`, first without and then with `--require-report-sync`.

The validator must confirm:

- every canonical source statement appears exactly once in the Source Statement Coverage Register;
- source statements are classified as Atomic, Compound, or Umbrella and map bidirectionally to CAP IDs;
- umbrella statements decompose into concrete capabilities and do not create umbrella CAPs or stories;
- every matrix row has a valid disposition and source-ID mapping;
- covered rows reference existing stories;
- story-to-matrix mappings are bidirectional;
- every story records Covered scope IDs and Atomicity;
- compound or umbrella stories require explicit approved-grouping evidence;
- Pending Approval or Approved scope contains no `Pending clarification` disposition;
- the saved validator command and status match the actual result when `--require-report-sync` is used.

Exit-code rules:

- `0`: validation passed;
- `1`: validation failed; keep or restore the scope as `Under Clarification`;
- any other exit code: validator execution failure; stop without manual fallback.

Do not claim a result until the synchronized verification pass has executed. The assistant summary and the saved Requirement Validation block must report the same command and result.

## Workflow Identifier Rules

Use exact technical identifiers in owned fields:

- `c-manage-product-requirements`
- `d-design-product-architecture`
- `e-sync-repository-requirements`

Do not use single-letter skill aliases or descriptive substitutes as executable next actions.

## Validation Invariants

Before requesting approval or completing the active scope, verify:

- the input approval or import gate is valid;
- every controlling source statement appears exactly once in the Source Statement Coverage Register;
- each source statement is correctly classified as Atomic, Compound, or Umbrella;
- every Compound or Umbrella statement is decomposed into concrete CAP IDs with bidirectional mappings;
- no atomic capability or ungrouped story uses an umbrella action such as manage, handle, support, maintain, administer, or operate;
- every atomic capability has one allowed disposition, source location, and source-ID mapping;
- no source statement or capability is silently omitted, deferred, or excluded;
- every `Deferred` or `Excluded` disposition has an explicit approved decision and evidence;
- every active requirement and story has a source or evidence basis;
- approved requirements and identifiers remain unchanged;
- every US belongs to exactly one primary REQ;
- REQ, US, SRC, and CAP identifiers are unique and never reused;
- every story expresses one independently observable user outcome unless explicit approved-grouping evidence exists;
- every story records Covered scope IDs and Atomicity;
- every covered matrix row references existing stories and every story maps back to the same CAP IDs;
- every acceptance criterion is testable and supported by evidence;
- no unstated product behavior was introduced;
- no technical layer or implementation task was presented as a story;
- imported `user-story` issues are reused, not duplicated;
- broad single-story requests do not require an unnecessary parent issue;
- the Requirements Overview, source register, coverage matrix, and detailed sections agree;
- no unresolved blocking question is presented as resolved;
- no `Pending clarification` disposition remains before Pending Approval;
- the approval record is complete and internally consistent;
- the Scope Coverage Validator completed both passes from the required path with no manual fallback;
- every active Requirement Validation block records the exact command, the actual expected status, and `Scope validator report synchronized: Yes`;
- the assistant summary reports the same validator status as the saved document;
- the Traceability Mutation Guard passed from the required path with no manual fallback;
- no unauthorized traceability row or field changed.

A failed invariant prevents approval or handoff.

## References

- Use `references/product-requirements-template.md` when creating the document.
- Use `references/process-flowchart.md` as the exact visual mirror of the numbered workflow.
- Use the matching folder under `references/golden-example/` for atomic initial release, umbrella-source initial release, broad-request increment, or existing-user-story increment behavior.
- Use `.agents/skills/c-manage-product-requirements/scripts/validate_trace_mutation.py` before saving any traceability change.
- Use `.agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py` for preflight and synchronized verification before questions, approval, or completion.
- Use `.agents/skills/c-manage-product-requirements/scripts/validate_workflow_alignment.py` when maintaining this skill.
- Run `.agents/skills/c-manage-product-requirements/scripts/run_regression_tests.py` before packaging or distributing an update.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
