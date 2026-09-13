---
name: plan-ledger-tasks-yylo
description: Create a concise Product Development Requirement and one or more implementation-sized YYLO Ledger tasks when the user explicitly asks to plan or register work.
argument-hint: "[Required Features] [Constraints] [Acceptance Criteria]"
enable-shell-directives: true
---

# Plan Kanban work

1. Read the project instructions and relevant product code from the integration or feature worktree. Read existing task/spec metadata through the canonical controller; do not assume `.juno_task/plan.md` exists.
2. Produce one concise PDR covering the goal, current behavior, scope, exclusions, risks, dependencies, acceptance criteria, and focused tests. Draft it in a fresh external file; do not place it in the product tree or a task body.
3. Preflight `yy ledger --help` and `yy ledger artifact --help`. Capture the PDR as a local immutable `report` Artifact Record with task/request provenance, then verify its ID, digest, size, retention, retrieval, and history. If the artifact API is unavailable, stop with the external draft intact and request an upgrade; never fall back to product `docs/`, task bodies/responses, new `.juno_task/specs`, or direct store edits.
4. Split only when pieces can be implemented and validated independently. Concurrent tasks must have explicit path ownership and dependencies.
5. Create tasks through routed `yy ledger` commands. Put concise durable requirements and acceptance criteria in each task body, record the PDR artifact ID in supported task fields/provenance, and relate follow-ups instead of reopening archived IDs.
6. Product documentation is only documentation shipped with the product. Never create controller-private tasks, ledger, state, artifacts, objects, specs, or receipts inside a product or feature worktree.
7. Do not start implementation, create worktrees, push, deploy, or mutate production unless the user separately asks.

Use `--id`, not legacy `--ID`, for Kanban mutations. Return the task IDs and a short dependency/order summary.

$ARGUMENTS
