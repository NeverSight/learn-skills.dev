---
name: github
description: Quickly audit, document, validate, commit, and safely publish or update a project on GitHub. Use for /github, publishing, repository setup or updates, README or repository-health work, pre-publish checks, and launch reviews. Supports private, public, update, docs-only, no-push, and launch.
---

# Fast GitHub Publisher

Finish as quickly as possible without weakening safety or making unverified claims. Start work immediately, batch independent reads and checks, make the fewest justified edits, and avoid optional ceremony. Keep updates and the final report terse.

## Options

- **Default:** Prepare and publish; preserve existing visibility, or make a new repository private.
- **`private` / `public`:** Set new-repository visibility. Confirm before changing an existing private repository to public.
- **`update`:** Include intended current changes, validate, commit, and push.
- **`docs-only`:** Edit documentation only; never push.
- **`no-push`:** Prepare and commit locally; never mutate the remote.
- **`launch`:** Run a comprehensive public-launch review.

Combine compatible options. `docs-only` and `no-push` disable pushing.

## Fast workflow

1. Snapshot Git status, branch, remotes, and recent commits. Run `python <skill-dir>/scripts/project_audit.py --path . --format text`.
2. Inspect only the audit-identified manifests, commands, entry points, configuration, tests, and docs needed to understand and describe the project. Run independent reads and checks in parallel.
3. Resolve safety blockers. Preserve unrelated user changes. Never expose secret values.
4. Make minimal evidence-based edits. Read [references/readme.md](references/readme.md) only when changing `README.md`; read [references/templates.md](references/templates.md) only when adding repository files; read [references/research.md](references/research.md) only for `launch`.
5. Run configured lint, test, type-check, format-check, and build commands in parallel when safe. Do not invent checks or reinstall dependencies unnecessarily. Re-run affected failures, then run the audit with `--strict`.
6. Review the diff and stage explicit paths. Commit logically without rewriting history.
7. For remote work, read [references/github-operations.md](references/github-operations.md), check active `gh` authentication, run `remote_guard.py` in dry-run mode, execute it with `--push`, then verify the remote SHA and metadata.
8. Report URL, changed files, checks or failures, commits, remote actions, and blockers—nothing extra.

## Non-negotiable safety

- Never push secrets, private data, accidental generated or dependency files, or files over GitHub's limit. If a credential may be committed, stop and recommend rotation plus history remediation.
- Never use `git add .`, force-push, delete repositories or branches, rewrite history, bypass protection, or change an existing visibility/default branch without explicit authorization.
- Never fabricate project claims, badges, compatibility, metrics, demos, licenses, or policies.
- Default new repositories to private and preserve existing visibility.
- A failed check that makes documentation false blocks publishing. Report unrelated failures without expanding scope.

Read [references/safety.md](references/safety.md) only when the audit finds a risk. Read [references/workflow.md](references/workflow.md) for ambiguous or complex repositories, [references/usage-and-troubleshooting.md](references/usage-and-troubleshooting.md) for failures, and [references/github-operations.md](references/github-operations.md) for remote actions. Use the bundled scripts as the preferred fast path.
