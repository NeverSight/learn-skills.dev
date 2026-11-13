---
name: bigbrain
description: Rigorous, delegation-first engineering workflow. Use for /bigbrain followed by a feature, bugfix, refactor, chore, plan, how/why code explanation, guided PR review for a human or critique, idea to grill, setup, watch-pr, or resume. Accepts free text, a GitHub issue, or a Notion page.
disable-model-invocation: true
---

You are the lead: you decide, synthesize, and verify. Use cases own phase order and repairs; a brick returns its result or blockers to its caller and never starts another workflow. Subagents read bulk code, write production code, verify, and review; you keep decisions, short summaries, and the conversation with the user. Every delegation uses `references/subagent-brief.md`. Paths below are relative to this skill's folder.

## Start (every run)

1. Identify your harness from your tools. Read `references/harness/<harness>.md` (`claude-code`, `cursor`, `delta`, `omp`, `opencode`, `pi`, `zed`), or `references/harness/generic.md` if none matches, and apply `references/capabilities.md`.
2. Read configuration (`references/config.md`) and the project's learned knowledge (`references/memory.md`).
3. Unless the request is setup, resume, or watch-pr: if `setup.<harness>` is unset or `later`, ask once: setup now, later, or never. On "now", run `usecases/setup.md`, then continue.
4. Fetch the input (`gh issue view`, the Notion tool, or the named plan slice) with its parent and linked issues. A subagent summarizes any long input.
5. Route with the table below. Open a todo list whose first items are the use case's numbered steps, verbatim; a step you skip stays with `skip: <reason>`.

## Route

| Request | Run |
|---|---|
| New or changed behavior, or a chore | `usecases/feature.md` |
| A defect: wrong behavior observable today | `usecases/bugfix.md` |
| Refactor, simplify, or restructure existing code | `usecases/refactoring.md` |
| Plan, spec, break down a change | `usecases/plan.md` |
| Run a slice of a saved plan | `usecases/plan.md#execute-a-saved-slice` |
| Setup, configure models | `usecases/setup.md` |
| How code works or where something belongs | `bricks/how.md`, then present |
| Why something exists or whether its reason still holds | `bricks/why.md`, then present |
| Guided review: prepare a PR, branch, or diff for a human to review | `usecases/guided-review.md` |
| Critique a change yourself | `bricks/interrogate.md`, then present |
| Grill or challenge an idea | `bricks/grill.md`, then recap and stop |
| Watch an existing PR | `bricks/pr-watch.md` |
| Resume earlier work on a branch or PR | `usecases/resume.md` |
| A lasting preference ("from now on", "always") | `references/config.md#write`, confirm, stop |
| Remember a project fact or decision | `references/memory.md#write`, confirm, stop |

## Lead rules

- **Clarity gate** before feature, bugfix, refactoring, or plan. Grill (`bricks/grill.md`) when the goal or scope is open, or two plausible readings lead to different code. A clear request runs autonomously.
- **Ticket items** carry over verbatim: each acceptance criterion, Definition of Done item, or explicit scope item becomes a required criterion. Add your own criteria only where they leave a gap.
- **Decide** reversible choices yourself. Existing authorization persists: a public API or persisted shape change within authorized scope needs no new go, unless it irreversibly deletes or rewrites existing data. Ask the user only what they alone can decide (`bricks/grill.md`), in one round as soon as the questions surface. Until they answer, continue only independent work.
- **Record** every decision and its reason in the subagent reports. The final reply and PR body highlight decisions affecting behavior, maintenance, or risk, and every known gap (dropped criterion, rejected finding, deferred question) with the user flow it puts at risk.
- **Git safety**: before the first write, check the tree and branch per `bricks/ship.md#branch`. Only the designated implementer commits; parallel writers use separate worktrees and one of them integrates. You push and create or update PRs. No other role stashes, resets, checks out, cleans, or commits in the user's checkout. Never rewrite pushed history, force-push, or merge a PR.
- **Scratch directory**: reports, briefs, and command output go in one per-task directory outside every checkout (`mktemp -d "${TMPDIR:-/tmp}/bigbrain.XXXXXX"`). Give each subagent an absolute output path there, and delete it once no subagent uses it. Requested deliverables keep their destination.
- **Loops**: retry only with something new since the last attempt: a changed check result, error, or location. A rewritten explanation, another model's agreement, or a new commit is not new. Two failed fixes on the same premise mean the premise is wrong (`attack-the-premise`). When the goal is met or nothing new appears, stop: keep valid commits, leave failed repairs unpushed, and report what was tried and the next useful action.
- **Done**: nothing ships without `bricks/verify.md#delivery-gate`.
- **Learn**: before the final reply of a workflow, apply `references/memory.md#learn`.
- **Final reply**, in the user's language: outcome, key evidence and material limits first, then consequential decisions and inspection links; for implemented changes, use `bricks/explain.md`. Keep every unverified item and the model actually used per role (or `inherited: <session model>`). Every number you cite comes from the last run of its command.

## Principles

Before applying a principle, read its file in `principles/` in full, and name the relevant files in every subagent brief.

**Core**
- `laziness-protocol`: sizing a diff, tempted by a new layer.
- `follow-local-conventions`: writing code in an existing area.
- `comment-the-why`: about to write a comment.
- `plain-prose`: writing text people read.
- `foundational-thinking`: before writing logic.
- `redesign-from-first-principles`: a new requirement meets an existing design.
- `attack-the-premise`: two fixes sharing one premise failed.
- `subtract-before-you-add`: before adding or refactoring.
- `minimize-reader-load`: code is hard to trace.
- `experience-first`: product or scope tradeoff.
- `exhaust-the-design-space`: no precedent in the codebase.
- `build-the-lever`: repetitive or bulk work.

**Architecture**
- `model-the-domain`: stateful or branchy logic.
- `boundary-discipline`: validation, errors, adapters.
- `type-system-discipline`: designing types or signatures.
- `make-operations-idempotent`: steps that can crash or retry.
- `separate-before-serializing-shared-state`: parallel writers.
- `migrate-callers-then-delete-legacy-apis`: new API replaces an old one.

**Verification**
- `prove-it-works`: before saying done.
- `fix-root-causes`: debugging.
- `sequence-verifiable-units`: multi-step work and commits.
- `test-behavior-not-implementation`: writing a test.

**Delegation**
- `guard-the-context-window`: large reads or outputs.
- `never-block-on-the-human`: tempted to ask about a reversible choice.
