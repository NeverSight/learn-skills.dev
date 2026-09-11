---
name: go
description: "Ship completed work through verification, review, PR, and CI."
disable-model-invocation: true
---

User-invoked full delivery: continue until verified or externally blocked.

## Exit contract

Resolve objective, non-inferable guardrails, repository checks plus real-entrypoint behavior, requested commit/remote/PR/CI delivery, and stop condition.

## Loop

Inspect -> verify -> repair -> repeat until verification passes.

1. Inspect the whole branch and endpoint: committed, staged, unstaged, untracked. Exclude unrelated files.
2. Run repository-native checks. Frontend normally includes focused tests, `bun run type:check`, `bun run lint:fix`; Go uses documented tests, vet, build.
3. Exercise every material runnable change through its real user or public entrypoint, including one credible break or recovery path. Tests do not replace this.
4. For a customer-facing surface, inspect the rendered or terminal result, states, accessibility, errors, and relevant viewports/platforms. Apply the [PR visual evidence gate](../commit-push-pr/REFERENCE.md#frontendcustomer-facing-detection--screenshot-table-phase-5), for all visible changes.
5. Review once for objective, guardrails, semantic density, and credible risk. Repair, invalidate, and replay affected evidence.
6. If the change claims measurable impact, repeat the same baseline/candidate scenario; do not invent useless benchmarks.

For dependency version upgrades, verify lockfile, clean install/build, and every affected call site against current primary documentation.

Do not manufacture reviews, cleanup passes, skills, or agent calls. Keep a single owner in the primary context; a different model requires explicit user authorization.

## Deliver

Follow [commit-push-pr/REFERENCE.md](../commit-push-pr/REFERENCE.md) for staging, commit, push, draft PR, reviewers, and body. On the current user-owned branch, rebase and `--force-with-lease` when needed without another permission prompt. Never [merge](../commit-push-pr/references/merge.md), plain-force, or rewrite default/shared/foreign/concurrent branches without explicit permission.

If `gh stack view --json` finds a stack, verify the layer against its parent. Only explicit `/stacked-prs` intent ships the whole stack.

- Bind evidence to current `HEAD`; edits invalidate it.
- This explicit full-delivery endpoint monitors CI. Repair failures, replay evidence, push, continue.
- Resolve every current human review thread; `pr-feedback-completeness-stop` enforces it. Human feedback has no cap. Do not poll after the current set.
- Stop self-review as soon as it is clean. Repeated noisy findings mean hand off, not arbitrary rounds.
- Extra recap/follow-up artifacts and history-cleanup require an explicit request.

## Done

- Real-entrypoint behavior observed or non-runnable reason recorded.
- Applicable checks pass without warnings on current `HEAD`.
- Current human feedback resolved; requested commit/push/PR/CI exists.
- No work is hidden; final response gives evidence and exactly one status line.

On the default branch, create an isolated worktree with `scripts/mux-worktree.sh <type>/<name>` before delivery. [ETHOS: Worktree Isolation]
