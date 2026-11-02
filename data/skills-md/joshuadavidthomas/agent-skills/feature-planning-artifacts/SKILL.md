---
name: feature-planning-artifacts
description: "Use when creating or iterating staged planning artifacts for a complex feature: design discussion, structure outline, final executor plan, or supporting research/research questions. Also use when designing before coding, breaking work into vertical slices, or deepening a high-value roadmap item, NNN improve plan, architecture candidate, or HumanLayer-style task."
---

# Feature Planning Artifacts

Create or update staged HumanLayer-style planning artifacts for work that needs research, design judgment, vertical slicing, or an executor-safe plan before implementation.

This skill is **not** a one-shot plan generator. It should normally take an input, delegate or perform reconnaissance, write or revise the current-stage artifact, then stop at the review gate. Do not continue to the next artifact until the current one is accepted or the user explicitly asks to proceed.

Treat detailed planning as meta-work: each artifact should make future implementation safer by defining success, surfacing decisions, turning recurring choices into policy when appropriate, and specifying evals/regression checks.

Open and resolved questions live in the design discussion. Plan iteration updates the plan itself.

## Source Frame

Before writing or updating planning artifacts, load what applies:

- The selected strategic-roadmap item, opportunity card, architecture candidate, or `NNN-*.md` plan.
- Existing artifacts for this effort, especially the latest design discussion, outline, or plan.
- The `coding-standards` skill as the canonical source for design claims. Load the matching references; do not copy the standards into this skill or artifact.
- Project docs: `AGENTS.md`, `README.md`, `CONTEXT.md`, architecture docs, ADRs, verification config, current VCS state, and relevant existing plans.

The artifact rules in this skill are canonical. For source patterns and examples, read the vendored HumanLayer v2 planning skills at `reference/humanlayer-riptide-v2-skills/` and the `improve-codebase-architecture` skill when architecture/deepening vocabulary matters.

## Stage Contract

Default to the smallest stage that creates durable progress.

| Stage | Use when | Inputs | Output | Stop gate |
|---|---|---|---|---|
| Research questions | The current-state unknowns are broad or ambiguous | Roadmap item, plan, user request | Questions about how the system works today | Stop after questions; ask whether to research |
| Research | Questions exist and current behavior must be established before design | Research questions or explicit scope | Descriptive current-state research | Stop after research; recommend design discussion |
| Design discussion | A feature or architecture direction needs judgment | Source item plus research or enough repo context | Options, recommendation, decisions, open questions | Stop for review; do not outline yet |
| Structure outline | The design is accepted or has one clearly recommended direction | Accepted/current design discussion | Vertical implementation slices | Stop for review; do not write final plan yet |
| Final plan | The outline is accepted or equivalent structure is provided | Accepted/current outline | Executor-safe implementation plan | Stop for execution handoff |

If the user only says “plan this,” start with a **design discussion** unless the unknowns are large enough that research questions or research must be written first. Do not generate research questions, research, design, outline, and plan in one pass unless the user explicitly asks for a full sequence.

## Reconnaissance Before Design

For design discussion work, do not make the main artifact carry all discovery labor inline.

1. Extract the current design questions from the input.
2. Split reconnaissance into independent threads when useful:
   - current implementation and data flow;
   - relevant tests/fixtures and validation commands;
   - existing patterns to follow or avoid;
   - architecture docs, ADRs, and prior plans;
   - external dependency or ecosystem behavior, only when the design depends on it;
   - applicable `coding-standards` concerns.
3. Use read-only subagents/scouts when available for independent reconnaissance. Give each one a narrow evidence request and require file paths, line ranges, citations, or commands inspected.
4. Verify load-bearing claims before they enter the design discussion.
5. Put detailed discovery in a research artifact only when it is durable enough to be reused. Otherwise summarize the evidence inside the design discussion.

Research is descriptive. Recommendations start in the design discussion.

## Artifact Bundle and Location

Use the canonical structures in [references/artifact-templates.md](references/artifact-templates.md). Prefer a feature bundle for each coherent feature or design effort: `.agents/plans/features/<feature-slug>/`.

Each bundle has a concise `README.md` index plus chronological `NNN-` artifacts. The number tracks artifact order rather than a fixed stage ID, so a design-first flow starts at `001-design-discussion.md`:

```txt
.agents/plans/features/<feature-slug>/README.md
.agents/plans/features/<feature-slug>/001-design-discussion.md
.agents/plans/features/<feature-slug>/002-structure-outline.md
.agents/plans/features/<feature-slug>/003-plan.md
```

When durable current-state discovery needs its own artifacts, place it before the design discussion and continue numbering:

```txt
.agents/plans/features/<feature-slug>/001-research-questions.md
.agents/plans/features/<feature-slug>/002-research.md
.agents/plans/features/<feature-slug>/003-design-discussion.md
```

When working inside an existing HumanLayer task, use `.humanlayer/tasks/<task>/` instead.

Create or update exactly one **primary** artifact per invocation unless the user explicitly asks for a full sequence. Updating the bundle `README.md` to reflect artifact status, decisions, or implementation routing is allowed alongside the primary artifact. A reconnaissance note or research artifact may be created first only when the design would otherwise rest on unverified current-state claims; if you create it, stop there.

When working inside `.humanlayer/tasks/<task>/`, use `ls -La` to inspect the directory because it may be a symlink. Do not use glob tools or plain `ls` there. Read task artifacts fully, not partial slices, before updating them.

## Workflow

1. **Choose the current stage**
   - Identify the exact roadmap item, plan, or candidate being deepened.
   - Inspect existing artifacts and choose the current stage by the stage contract.
   - If a design discussion exists but is not accepted, iterate that document rather than writing an outline.
   - If an outline exists but is not accepted, iterate that outline rather than writing a final plan.
   - Define what “better” means for this artifact before writing: user outcome, architecture leverage, verification strength, executor readiness, reliability, or another concrete standard.
   - Choose the artifact destination, defaulting to `.agents/plans/features/<feature-slug>/` when no project convention exists.
   - Inspect existing artifact files and continue `NNN-` numbering; do not overwrite existing artifacts unless iterating them deliberately.
   - Create or refresh `README.md` when opening a feature bundle, adding an artifact, accepting a stage, or recording whether implementation should proceed directly or be split into an improvement plan batch.

2. **Research questions stage**
   - Write questions only about how the current codebase, dependencies, and prior artifacts work today.
   - Do not ask “how should we implement…” or leak a preferred solution into the questions.
   - Stop after writing or updating the research-questions artifact.

3. **Research stage**
   - Require research questions, a user query, or an explicit research scope.
   - Document current behavior, architecture, data flow, tests, constraints, and relevant prior plans.
   - Research is descriptive only. No recommendations, implementation section, or “should” language.
   - Stop after writing or updating the research artifact.

4. **Design discussion stage**
   - Require completed research or enough verified current-state context from reconnaissance.
   - Present current state, desired end state, explicit non-goals, proposed architecture, design questions, options, recommendations, and resolved decisions.
   - Cite the selected `coding-standards` skill concern/reference for the actual design pressure.
   - Use architecture/deepening vocabulary for module/interface/depth/seam/adapter/leverage/locality.
   - Include patterns to follow with file references and concise snippets when they materially guide implementation.
   - Identify recurring decisions that should become a standing policy, ADR, repo instruction, template, or eval.
   - Keep unresolved questions in `Design Questions`; move answered ones to `Resolved Design Questions`.
   - Mark the document `status: in-review` unless the user explicitly accepts it in the same request.
   - Stop after writing or updating the design discussion. Ask for review of the recommendation and open questions. Do not write a structure outline yet.

5. **Design iteration stage**
   - When the user gives feedback on the design discussion, update the same document.
   - Verify factual corrections when possible before changing the design.
   - Preserve rejected options and rationale; do not erase useful decision history.
   - When the design is accepted, mark it `status: accepted` and stop with the next recommended artifact: structure outline.

6. **Structure outline stage**
   - Require an accepted design discussion, unless the user explicitly overrides that gate.
   - Convert the chosen design into vertical phases.
   - Name files likely touched, key signatures or sketches, and validation per phase.
   - The outline should be specific enough to plan from but not a giant implementation dump.
   - Mark the outline `status: in-review` unless explicitly accepted.
   - Stop after writing or updating the structure outline. Do not write the final plan yet.

7. **Outline iteration stage**
   - When the user gives feedback on the outline, update the same document.
   - If feedback reopens architecture choices, return to the design discussion instead of forcing the outline forward.
   - When the outline is accepted, mark it `status: accepted` and stop with the next recommended artifact: final plan.

8. **Final plan stage**
   - Require an accepted structure outline, unless the user explicitly provides an equivalent outline.
   - Write an executor-safe plan from the outline.
   - Include current-state evidence, definition of “better,” desired end state, scope/out-of-scope, phase sequence, implementation routing, automated verification, evals/regression checks, manual checks only when meaningful, autonomy boundary, drift checks, STOP conditions, and rejected approaches.
   - Do not reopen resolved design questions in the final plan.
   - Stop after writing or updating the final plan artifact.

## Review Gates

Use explicit gates so the workflow does not drift into a full one-pass plan.

- **After research questions:** “These are the questions I would research next.”
- **After research:** “This is the current-state evidence; recommendations belong in the design discussion.”
- **After design discussion:** “Review the recommendation, unresolved questions, and non-goals before I outline implementation.”
- **After structure outline:** “Review the vertical slices and validation before I write the executor plan.”
- **After final plan:** “This is ready for execution unless a STOP condition or drift check fails.”

If the user asks to proceed, continue from the accepted current artifact. If the user gives critique, iterate the current artifact instead.

## Update Rules

- Document precedence is: accepted plan > accepted structure outline > accepted design discussion > research > source roadmap/NNN plan.
- Draft or in-review artifacts do not supersede accepted earlier artifacts until the user accepts them or explicitly says to proceed.
- When iterating, update the existing artifact at its original path.
- Do not blindly accept user corrections. Verify cited files or claims when possible, then update the artifact.
- If a design fork appears during outline or plan writing, return to the design discussion rather than burying the fork downstream.
- If a decision will recur across future work, record it as a standing policy recommendation in the design discussion rather than leaving it as one-off advice.

## Done Criteria

The artifacts are ready when each stage has stopped at its review gate: the bundle README shows current status and next gate, research is descriptive, the design discussion records options and decisions, recurring decisions have policy recommendations when useful, the structure outline slices the work vertically, and the final plan either supports direct execution or can be split into an improvement plan batch without relying on hidden conversation context.
