---
name: teach
description: "Teach design-level mental models of existing source code and explain behavioral changes in diffs, commits, patches, or file comparisons. Use when a learner asks how a focused subsystem, feature, whole project, or change works."
---

# Teach

Teach for maintainable understanding, not implementation mechanics. Build the smallest coherent mental model that explains purpose, boundaries, ownership, contracts, control and data flow, invariants, edge cases, and consequential tradeoffs.

This skill is explanatory. Explain syntax, line-by-line execution, or how to write the code only when the user asks. Include external library, protocol, runtime, or product context only when it changes how the code should be understood.

## Workflow

1. Identify the teaching target.
   - When the target is a diff, commit, range, patch, or comparison between file
     or document versions, read [guides/changes.md](guides/changes.md) and use
     its cold-reader change workflow. With no named target in a Git repository,
     default to current staged, unstaged, and relevant untracked changes. List
     changed paths before reading content and exclude secret-bearing environment
     or credential files and private documents from that default selection.
     Ask for a target when no eligible changes remain. For any selected target,
     redact secrets and private personal data before quoting or summarizing it.
   - Within this skill, treat an exact teaching target of `project` as shorthand for the whole-application workflow. Also select that workflow when the learner clearly asks to start with the entire codebase or application and choose areas afterward. Read [guides/whole-application.md](guides/whole-application.md) and use its orientation workflow.
   - When the learner selects a topic from an earlier whole-application learning map, read [guides/whole-application.md](guides/whole-application.md) and use its follow-up workflow.
   - Otherwise, infer whether the learner needs a module, feature flow, subsystem, architecture area, API boundary, runtime path, data model, state flow, or directly relevant external concept. Choose the smallest coherent model that answers the request.

2. Read top-down.
   - Start from entry points, exported symbols, route handlers, public interfaces, or the requested flow.
   - Read supporting helpers, data structures, tests, and nearby `AGENTS.md`, `ARCHITECTURE.md`, or notes only as needed.
   - Continue until you can trace the main flow end to end and name every contract or boundary it crosses without guessing.

3. Build the lesson in learning order.
   - Start with purpose, role, and boundaries; then explain flow, ownership, and contracts.
   - Explain who calls and owns what, where decisions happen, and how data changes shape across boundaries.
   - Drill into mechanisms, invariants, edge cases, and tradeoffs only as needed to make the design intelligible.
   - Reorder the explanation for understanding rather than mirroring file order.

4. Use selective evidence.
   - Explain each important point in prose first and connect evidence back to the larger model.
   - If exact code is load-bearing for a contract, condition, data shape, boundary, state transition, or API, read [guides/snippets.md](guides/snippets.md) before including a snippet.
   - If a relationship is materially clearer as a flow, map, transition, or pipeline, read [guides/diagrams.md](guides/diagrams.md) before drawing a diagram.

5. Surface important confusion points.
   - Call out misleading names, blurred responsibilities, hidden invariants, or awkward control flow only when they affect understanding.
   - Frame them as teaching notes rather than a full review; say plainly when the structure is sound.

6. Close the loop.
   - Summarize the model the learner should retain and the one or two design facts that matter most for future work.

## Output shape

For a whole-application orientation, use the output shape in [guides/whole-application.md](guides/whole-application.md).
For changes, use [guides/changes.md](guides/changes.md). For other focused targets,
use the elements below only when they help; combine or omit sections for small
targets and honor the user's requested format.

### Big Picture

Give one short paragraph on what this part of the system is for and where it fits.

### How It Works

Explain the main flow in logical learning order. Focus on roles, boundaries, contracts, ownership, and movement of control or data.

### Key Decisions

Call out the few abstractions, invariants, contracts, or design decisions that make the system make sense.

### Reviewer / Maintenance Focus

List only consequences that materially affect usage, behavior, compatibility, testing, maintenance, or future review. Include important tradeoffs, risks, confusing boundaries, or maintainer questions.

### What to Remember

State the mental model in one short paragraph or a few tight bullets. Favor the one or two points that will help the reader understand future work in this area.

### Important Confusion Points

Include this section only when something materially affects understanding. Describe design issues, awkward boundaries, or misleading structure briefly and concretely.

## Communication rules

- Optimize for reviewer understanding, not exhaustiveness.
- Match depth to the request: stay brief for tiny targets or overview asks; go deeper when the learner asks about mechanisms, decisions, or tradeoffs.
- Do not use path or line references as the primary navigation aid.
- Label inferences when the code does not prove intent directly.

## Routing

- Use a review-oriented skill when the user wants critique rather than understanding.
