---
name: commit-push-pr
description: Commit, push, and open a reviewable PR, or execute an explicitly authorized merge. Use for delivery requests; --no-pr stops after push.
argument-hint: "[--no-pr]"
---

See [REFERENCE.md](REFERENCE.md) for gates, commits, labels, body, evidence.

Only explicit merge requests use [the merge contract](references/merge.md), not this PR flow.

## Preflight

1. Inspect `git status -sb`, `git diff HEAD`, branch, recent log, and branch PR.
2. Resolve endpoint: commit only, push (`--no-pr`), or PR. Commit-only skips remote and `gh` preflight.
3. Push/PR needs a remote; PR also needs authenticated `gh` and the default branch.
4. For PR, run `gh stack view --json`; inspect base/stack. A normal PR owns one layer, never `gh stack submit`.
5. Run applicable review axes inline; do not block merely over named skill invocation.
6. Runnable PR work requires current `/dogfood` PASS; BLOCKED needs user waiver.
7. Stage requested paths by purpose; ask if ownership is unclear.

## Commit

1. Stay on the feature branch; on default, create `type/description`.
2. Per coherent group, `git add <explicit paths>` then `type(scope): terse description`: lowercase, 5-72 chars, no period.
3. Explicit commit-only intent stops here after clean-tree check and summary.
4. Push/PR: show `origin/<branch>..HEAD`, then push with tracking.
5. Current user-owned branch rewrites use `--force-with-lease` without another permission prompt. Never plain-force; default/shared/foreign/concurrent rewrites need explicit permission.

## Pull request

`--no-pr` never creates a PR. Refresh an existing PR's evidence/body after push; otherwise end after push and clean-tree check. Prepare local visual evidence before push.

PR creation authorizes verification, commit, push, and lease-protected rebase on the current user branch; never merge or unrelated fixes.

1. Resolve base with `"${CLAUDE_PLUGIN_ROOT:-.}/scripts/resolve-pr-base.sh"`. Reuse the branch PR or create against that base with assignee, labels, and reference template. Whole-stack publication uses `/stacked-prs`.
2. Every PR runs `/quantify-impact`; include concise value or proven metrics, not benchmark theater.
3. Every visible change, however small, requires the reference's inventory, embedded before/after, reviewed snapshots, and passing visual tests. Missing evidence blocks publication absent an explicit user waiver.
4. Include current dogfood receipt. Re-read the body, verify reviewer image access, and print the URL. Updates/reopens use the same gate; edits invalidate affected evidence.

Do not run `/visual-recap` or `/make-pr-easy-to-review` unless the user explicitly requests.

## Completion

1. Take one CI status snapshot: `gh pr checks <number>`; note absent CI.
2. Report failures; further remediation/monitoring requires `/go`, ship, babysitting, or follow-up.
3. Report `git status`, remaining diff, branch, commits, PR, CI, and next action.
4. End with one status line: `done`, `awaiting decision`, or `blocked`, using the repository marker contract.

Never stage unrelated work, push unconfirmed mixed scope, or hide failures. If `gh pr create` fails, show error and recovery command.
