---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Read `docs/agents/issue-tracker.md` before starting or resuming tracked work. Follow its assignment, Project mapping, pause/release procedure, and final PR policy. The orchestrator owns tracker updates; implementation subagents return evidence. If tracker configuration is absent, tell the user to run `/setup-matt-pocock-skills`.

The main agent is the **orchestrator**. It owns the preflight, branch and
worktree state, integration, validation, independent review, and delivery. An
**implementer subagent** owns the code for one ticket in one isolated context.

## Process

### 1. Pin the work

Read the complete ticket or spec, identify its acceptance criteria and
pre-agreed test seams, and choose the delivery mode below. Record the fixed
point for review: the immediate parent branch for a stack, the integration
branch for a child ticket, or the trunk/explicit parent for standalone work.
If the seams are not settled, ask the user before dispatching implementation.

Read current ownership, parent reservations, linked PRs, and configured Project state. Claim unassigned work for the driving developer according to the tracker policy; preserve existing assignees unless reassignment was requested. Another developer's reserved PRD is not an independently available pool of tickets. Reconstruct resumed progress before changing Status.

This step is complete when the scope, seams, blockers, fixed point, target
branch, and target worktree are all explicit.

### 2. Delegate implementation

Set selected work to `in-progress` when implementation starts, using the tracker policy and configured Project Status field. Queued tickets retain their current state.

For any ticket that crosses more than one layer, changes more than one file, or
would benefit from a fresh context, dispatch one implementer subagent using the
brief in [IMPLEMENTER-BRIEF.md](IMPLEMENTER-BRIEF.md). A tiny, isolated edit can
stay in the orchestrator context.

Give each subagent its own context and worktree. Dispatch independent frontier
tickets in parallel, one worktree per ticket; wait for a blocker before
dispatching a dependent ticket. The orchestrator never lets two agents edit the
same worktree or branch concurrently.

The implementer subagent calls the Skill tool with "tdd" at the pre-agreed
seams, typechecks regularly, runs focused tests during the loop, runs the full
suite once, and commits only to its implementation branch. It returns the
commit, changed files, checks, and any blocker. It does not choose delivery
topology or review its own work.

If the harness has no isolated subagent or worktree capability, execute the same
brief in the orchestrator context and record that fallback in the final report.

This step is complete when every dispatched ticket has either returned a
verifiable commit and report or has been completed through the documented local
fallback.

### 3. Review independently

Inspect the implementation diff and run the relevant checks before reading the
implementer's narrative. Check out the returned implementation branch at its
commit in the reviewer context or worktree, then call the Skill tool with
"code-review" against the fixed point. Verify that
`git diff <fixed-point>...<implementation-commit>` is non-empty before review.
The review must run after the implementation commit and in a clean reviewer
context or worktree where the harness supports it.

The orchestrator classifies every finding as resolved, deferred with a reason,
or blocking. Fix blocking findings in the orchestrator or a distinct repair
subagent, rerun the affected checks, and repeat the review after material fixes.
The implementer report is evidence about what was attempted, not acceptance
of the result.

This step is complete when the diff satisfies the ticket's acceptance criteria,
the relevant checks pass, and no blocking review finding remains.

### 4. Deliver

Continue with the selected delivery mode below. The orchestrator owns the final
Git history, branch/PR operations, merges, and the final report; the implementer
subagent only supplies the committed implementation.

When a standalone or stacked ticket PR is open and ready for review, set the delivered ticket to `waiting-validation` and verify its assignees, Project membership, and Status when configured. In integration delivery, child-branch integration remains non-terminal progress; move the PRD and delivered tickets to `waiting-validation` only when the final integration PR is ready. Review repairs return the affected scope to `in-progress`.

Keep issues open and Project states non-terminal until their final delivery PR is verified merged into its intended base. Use closing references only in final PR bodies when the actual base supports them, and ordinary references elsewhere. Merging requires a separate user instruction. Report tracking failures separately from the implementation/PR result, retaining URLs for an idempotent retry.

## Delivery mode

Choose the delivery mode from the user's instruction, the repository's `AGENTS.md`, or the current branch state. Do not infer stacked or integration delivery merely because a feature has multiple tickets.

### Standalone delivery

Use standalone delivery by default when no stack has been requested:

1. Prepare a new branch named `feat/implement-<short-description-of-work>` and
   assign its worktree to the implementer subagent.
2. After independent review, push the branch and create a pull request against
   the configured final PR base, declaring the fully delivered ticket or spec for closure on merge where supported.

### Stacked delivery

Use stacked delivery when the user requests it or the repository explicitly enables it for the current flow. Use the `gh-stack` skill's commands as the operational reference.

Before writing code:

1. Read the full ticket and verify that its real blockers are complete or that the requested parent branch already contains them.
2. Confirm the worktree is clean.
3. Run `gh stack view --json` to inspect the current stack. If it reports that the branch is not in a stack, initialize or continue with standalone delivery as appropriate. If the existing implementation branch already has a PR, adopt it with `gh stack init <existing-branch>` rather than recreating the branch or PR.
4. Plan the layer against the immediate parent. A ticket dependency graph can contain forks and joins; `gh-stack` is strictly linear. Do not append a sibling or join ticket to a stack unless serializing that work is an intentional decision.

Create and navigate branches with `gh stack`:

- For the first layer, use `gh stack init feat/implement-<short-description-of-work>`.
- For each subsequent layer, use `gh stack add feat/implement-<short-description-of-work>` while checked out on the stack top.
- Use standard `git add` and `git commit` for deliberate staging; do not use `git switch -c` for a stacked layer.

The implementation, TDD loop, typechecking, full test suite, and independent review requirements are the same in both modes. In stacked mode, review the diff against the immediate parent branch, not against the trunk, so the review matches the PR's incremental change.

At the end of a stacked layer:

1. Use `Refs #<ticket-number>` in commits. After submission, include `Closes #<ticket-number>` in the final ticket PR body only when its actual base supports closure on merge; otherwise retain references and report the required post-merge reconciliation. `gh stack submit --auto` derives initial PR metadata from commits.
2. Run `gh stack submit --auto --open` to push the stack and create or synchronize ready-for-review PRs.
3. Run `gh stack view --json` and report the resulting stack and PR URLs.

Use `gh stack sync --prune` after merges and `gh stack merge --yes` when the entire approved stack should be merged. Do not use `gh pr merge` for a stacked PR.

### Integration delivery

Use integration delivery for a multi-ticket spec or PRD whose approved dependency graph has forks or joins and whose merge policy requires one final pull request into the trunk. This is different from a `gh-stack`: the integration branch is a shared feature branch, not a linear stack.

The shape is:

```text
trunk
 └── integration/<spec-slug> → final PR to trunk (Closes #<spec>)
      ├── ticket-a → PR to integration/<spec-slug>
      ├── ticket-b → PR to integration/<spec-slug>
      └── ticket-c → PR to integration/<spec-slug>
```

Before writing code:

1. Read the full ticket and verify that its real blockers are already merged into the integration branch. A blocker PR being open is not enough.
2. Confirm the worktree is clean and use a separate worktree for each ticket that will be developed in parallel.
3. Create or check out the durable `integration/<spec-slug>` branch from the updated trunk. Open one draft integration PR from that branch to the trunk before or alongside the child PRs.
4. Create each ticket branch from the latest integration branch and target the child PR at the integration branch, never at the trunk.

At the end of an integration-delivery ticket:

1. Include `Refs #<ticket-number>` in the child PR body. The final integration PR is responsible for `Closes #<spec-number>` and may close any child tickets that are still open.
2. Push the ticket branch and create or update a normal PR whose base is `integration/<spec-slug>`.
3. After the child PR is merged into the integration branch, rebase or recreate dependent ticket branches from the updated integration branch before continuing.
4. Do not merge a child PR directly into the trunk.

Only the final integration PR is merged into the trunk. Use the repository's normal PR merge policy for child PRs and the final PR; `gh-stack` is optional for any strictly linear sub-chain inside the larger integration effort.

Each implementation still starts in a fresh context when the ticket flow calls for it. The stack is durable repository/GitHub state, so the new context must perform the stack preflight above instead of relying on conversation memory.
