---
name: ship
description: Ship PRs or scoped local work to the configured Git remote’s default
  branch following the project’s versioning policy and updating an existing changelog.
  Handle "release this" using the project’s existing release process, without assuming
  tags or GitHub releases. Clean up safely merged PR branches; deployment is separate.
metadata:
  version: 0.1.0
license: MIT
---

# Ship

Ship the work identified by the user or current conversation using `git` and the selected host’s available review tools. Use `gh` only for GitHub repositories. In this skill, “PR” also includes a host’s equivalent merge request. “Ship this”, `$ship`, or a specified PR authorizes committing the scoped work, preparing its version when the applicable policy calls for it, updating its existing changelog, pushing, merging into the default branch, and safely cleaning up merged PR branches. “Main” means the repository's actual default branch. Do not ask for a second approval of these actions.

“Release this” uses the same version-and-delivery workflow and follows the project’s existing release process. Neither phrase by itself introduces tags or GitHub releases. Create or publish those only when explicitly requested or required by the established project release workflow; a historical tag alone does not establish that requirement. A project that tracks releases solely in its manifest and changelog continues doing so. Neither mode authorizes deployment commands, package-registry publishing, or notification messages. Existing repository automation may run after a push or merge; honor active constraints on its consequences.

Editing this skill alone does not authorize shipping or releasing the current repository. Apply explicit user overrides, such as shipping without a version bump. Follow the project's versioning policy and configured release tooling. Read the optional bundled setup configuration as described below; a configured preference never bypasses a concrete repository approval gate.

## Portable configuration

Read [the runtime contract](../hap-mode/references/runtime.md) for host features, action authority, and T3 PR registration/watching.

Read [configuration](../setup-hapstack/references/configuration.md) when that bundled file is available. Resolve the project configuration before global configuration. When no configuration exists, use the project’s existing version/release policy, merge convention, and tools; do not apply another user’s preferences. If this skill was installed alone, these defaults are sufficient.

Version preparation follows the selected policy: `project` uses the repository convention; `bump-on-ship` prepares a version for each authorized shipment where a version source exists; `release-only` changes the version only for an explicit release request. A release request always follows the established release process. Explain a skipped version bump rather than inventing a version source.

## Discover and prepare

- Read applicable repository instructions. Inspect `git status --short`, the current branch, `git worktree list --porcelain`, remotes, and tracking branches. Record the starting state. Identify which local changes belong to the requested shipment. Commit only that work and its version/changelog updates; preserve unrelated edits. Never automatically stash, reset, or discard work.
- Resolve the delivery remote before choosing a provider tool. Honor an explicit user target; otherwise inspect branch upstream/push configuration and remote fetch/push URLs. Use `origin` when it is the unambiguous delivery target, regardless of provider. If fork/upstream or conflicting push destinations make the target ambiguous, ask before mutation. Never substitute a GitHub remote merely because `gh` is available.
- Resolve the selected remote’s actual default branch from its advertised HEAD (`git ls-remote --symref REMOTE HEAD`) or verified provider metadata; a cached `refs/remotes/REMOTE/HEAD` can be stale. If neither establishes the default, ask rather than guessing `main`. Do not change remote URLs or tracking configuration to make the workflow fit.
- Select the provider path below. Check `gh` authentication and repository identity only for GitHub (including a verified Enterprise host). For other providers, use available host-specific tools for PRs and policy; plain Git delivery does not require GitHub authentication.
- Fetch that remote with pruning. This refreshes remote-tracking references; it does not authorize deleting local branches.
- If the user names a PR number, URL, or branch, resolve that exact PR and verify the repository. A URL pointing elsewhere is not permission to operate on a different checkout. If already merged, verify its merged head and inspect any remaining cleanup instead of attempting another merge.
- When no exact PR was specified and the selected host has an available PR interface, discover open PRs, including drafts, retrieving every page or checking for truncated results. Prefer the current branch's PR as the candidate. Use the current conversation or current branch to select an unambiguous candidate; if a discovered PR is not identified by that context, ask for selection. If several unrelated PRs are plausible, present a short numbered list and ask which to ship; do not select the newest, all PRs, or only PRs authored by the user without justification. With no relevant open PR, ship clearly scoped local changes or commits directly using the local workflow below. If neither scoped work nor a release request exists, report that there is nothing to ship; do not manufacture a version-only shipment. Do not create an unrelated PR.
- Build the dependency graph before merging. Read [stacked-prs.md](references/stacked-prs.md) whenever a PR has a non-default base, stack metadata, dependent open PRs, or overlapping commit ancestry. Include required ancestors; do not automatically include descendants or unrelated PRs.
- Inspect each candidate's head SHA, base, draft status, mergeability, required checks, reviews, changed files, and diff. Follow required repository checks. Use a clean temporary worktree if local checkout changes would interfere. Do not turn shipping into unsolicited feature development or an exhaustive review.
- Resolve ambiguity and identify blockers before merging. Unrelated dirty work, another worktree using main, or unrelated local main commits can prevent the requested checkout/sync/cleanup. Explain the concrete issue and obtain a handling choice rather than silently stashing or destroying work. Read-only PR inspection can continue while waiting.

### Provider routing

- **GitHub:** Use `gh` for PR discovery, checks, merges, and release metadata, explicitly targeting the verified repository and host. The commands below are GitHub examples.
- **Cursor Origin:** For `origin.cursor.com` remotes or `cursor.com/codebase` PR URLs, read [cursor-origin.md](references/cursor-origin.md). Distinguish native Origin repositories from GitHub mirrors before choosing PR tools or verifying delivery.
- **Other Git hosts:** Use their available CLI/API for the equivalent PR operations and required checks. Preserve the same scope, readiness, inspected-head, stack, and cleanup guarantees. Inspect supported commands before use; do not translate `gh` flags by guesswork. If the interface cannot enforce an inspected head or establish required readiness, report that limitation before merging.
- **Plain Git or unavailable review tooling:** For clearly scoped local work, use the direct Git workflow when repository policy permits it. A non-GitHub remote does not itself require `gh` or a GitHub PR. Infer capabilities from the actual remote and available tools, not its name. If a specific PR was requested, review requirements cannot be established, or policy requires a PR, prepare the scoped work and report the missing host capability; do not treat inaccessible PRs as nonexistent or bypass review by pushing directly. An authentication or API failure is not evidence that a host has no PRs.

GitHub discovery examples; adjust to installed `gh` capabilities and target the verified host/repository:

```sh
gh repo view --json nameWithOwner,defaultBranchRef,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed,deleteBranchOnMerge
gh api --paginate 'repos/OWNER/REPO/pulls?state=open&per_page=100'
gh pr view NUMBER --repo OWNER/REPO --json number,url,title,state,isDraft,baseRefName,headRefName,headRefOid,headRepository,headRepositoryOwner,isCrossRepository,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
gh pr diff NUMBER --repo OWNER/REPO
gh pr checks NUMBER --repo OWNER/REPO --required
```

Distinguish “no required checks configured” from failed checks, pending checks, or inability to read them. Re-read unknown mergeability after the selected host computes it. Do not bypass protection, dismiss reviews, or mark drafts ready without explicit authorization. Use the repository-required merge queue for a ready, requested PR; do not enable indefinite auto-merge for failing or pending checks unless requested. Never use `--admin` as a workaround.

## Authorization and progress

A specified PR, unambiguous branch, or “ship this” referring to the work just completed authorizes the corresponding shipment. Ask only when the target or ownership of local changes is ambiguous; a PR is not required for local shipping.

Give a concise progress update with the repository, selected PRs and inspected heads, merge method/order, checks, and intended branch cleanup. This is informational, not an approval gate.

Include necessary stack ancestors and ordinary retargeting within the requested shipment; exclude unrelated PRs and unrequested descendants. Ask only for a missing scope decision or a concrete action beyond ordinary shipping, such as resolving ambiguous stack history, rewriting published branches, bypassing protection, or handling local work that prevents safe checkout. Preserve unrelated uncommitted work and branches with additional unmerged commits.

## Prepare the version and changelog

- Before delivery, determine whether the selected versioning policy calls for a bump. If it does not, preserve the version and follow existing changelog conventions. Otherwise inspect the project's authoritative version source, release conventions, and existing automation. Choose the appropriate SemVer increment from the delivered changes: patch for fixes, maintenance, or documentation; minor for backward-compatible features; major for breaking changes, subject to documented pre-1.0 conventions. Respect a requested version. Do not upgrade dependencies.
- Bump once per shipment, including a stack shipped together, not once per commit or retry. Reuse an appropriate version bump already included in the shipment. Update required matching lockfile or workspace version fields with the project's established tools; avoid unrelated lockfile churn or tools that implicitly tag/publish. If existing automation owns versioning, use its established input and verify the resulting bump instead of creating a competing bump.
- If a changelog exists, follow its format: collect the shipped entries in the new version's section dated YYYY-MM-DD, preserve history, and leave unrelated pending entries under Unreleased. Mark breaking changes and include migration guidance. If no changelog exists, skip this step without creating one; continue versioning and delivery.
- If the project has no version source or convention, do not invent a manifest. Report the skipped version bump; if a release requires a version and no existing version source (including versioned changelog headings) establishes one, ask for the initial version and where the project should track it.
- Include version/changelog changes in the selected PR before its final checks and head inspection, or in the scoped local commit before pushing. For a stack, place shared version changes in the final selected dependent. If branch ownership or protection prevents updating the selected PR, report the concrete blocker rather than silently merging without the bump.
- Follow mandatory repository checks and run only checks needed for the changed release metadata. Do not add routine full-suite validation. Explain the selected version in the progress update.

## Ship local work directly

Use this path when the conversation identifies local work and no relevant PR is being shipped.

1. Inspect the exact diff and outgoing commits. Stage explicit paths or hunks belonging to the shipment, including version/changelog edits, and commit them. Do not include unrelated staged changes or local commits.
2. Fetch the verified remote. If already on the default branch, ensure the outgoing commits are all in scope. Otherwise switch safely to the default branch, fast-forward from the remote, and merge the scoped feature branch. Do not rewrite published history or disturb another worktree. Resolve only routine conflicts within the authorized work; stop for ambiguous conflicts or unrelated changes.
3. Push normally to the verified default branch; never force-push. If remote advancement rejects the push, fetch and inspect before one safe retry. If branch protection requires a PR, create a focused PR through the selected host’s supported interface and use the PR workflow. If that interface is unavailable, report the blocker; do not bypass protection or push to a different provider.
4. Fetch and verify the delivered commit is on the remote default branch. Keep local-only feature branches unless their deletion is explicitly requested; PR branch cleanup follows the proven-merged rules below.

## Merge and verify

1. Re-read each PR immediately before acting. Confirm the inspected head SHA and base, required checks/reviews, and readiness. If the head changes, inspect the new commits and recheck readiness before pinning the new head. Ask only if the change materially exceeds the requested PR scope or changes the destination.
2. Merge ancestors before dependents using the chosen, repository-supported method. Use the host’s inspected-head precondition. For GitHub, for example:

   ```sh
   gh pr merge NUMBER --repo OWNER/REPO --squash --match-head-commit FULL_SHA
   ```

   Replace `--squash` with the chosen method. Do not pass `--delete-branch`: cleanup is a separate verified phase, especially for stacks.
3. If a merge queue is required, use the repository-required queue flow. Enqueued or auto-merge-enabled is not merged. Watch status in bounded intervals; if it remains pending, report pending and preserve branches. Never clean up a queued PR or merge its dependents prematurely.
4. Confirm the selected host reports the PR merged, record the merge commit and original head, and fetch the updated destination. Follow the stack reference for dependent bases and head changes. Inspect the next PR again after its parent merges.
5. If a PR fails, stop its dependent chain. Re-fetch and inspect a transient failure before one retry; do not loop through overrides. Report completed and unmerged PRs separately. Continue cleanup only where it is independently proven safe and consistent with the requested scope.

## Return to main and clean up

Only clean up branches belonging to the requested, confirmed-merged PRs. Recheck the working tree and worktree inventory first.

- Switch the current checkout to the actual default branch when safe. If it does not exist locally, create a tracking branch from the verified remote/default. Fast-forward explicitly from that remote: `git merge --ff-only <remote>/<default>`. Do not use plain `pull` if it could create a merge commit or rebase local work.
- During PR cleanup, if main is ahead of or diverged from remote, leave its commits intact and report that it is not an exact match. Scoped local shipments use the local workflow above. Do not reset or push it to make the task look complete. If main is checked out in another worktree, do not use `--ignore-other-worktrees` or remove that worktree; report the specific checkout constraint.
- Before deleting a PR head, confirm no open PR still uses it as its base and no unmerged descendant needs it. Preserve shared stack branches until their dependents are safely retargeted or merged.
- Remote deletion: verify head repository ownership and the branch's current remote SHA. Delete only a branch belonging to the requested shipment on the matching remote whose tip is the confirmed-merged PR head. Prefer an exact lease to prevent deleting commits pushed since inspection:

  ```sh
  git push REMOTE --force-with-lease=refs/heads/BRANCH:CONFIRMED_HEAD_SHA :refs/heads/BRANCH
  ```

  Substitute and shell-quote actual values. This is a guarded deletion, not permission for a general force push. If the branch changed, preserve it and report why. Treat already-deleted remote branches as success. Do not delete branches in contributors' forks unless the user specifically approved that repository and branch.
- Local deletion: ensure the branch is not checked out in any worktree. Use `git branch -d BRANCH` when ancestry permits. Squash/rebase merges may require `-D`; allow that only after the selected host confirms the PR merged at the recorded head and the local tip equals or is an ancestor of that original PR head. This proves the local branch has no additional commits outside the delivered work. Otherwise preserve it. Never force-delete based on a matching branch name, a closed PR, or the presence of a squash commit alone.
- Never delete the default branch, release/protected branches, unrelated branches, or pre-existing worktrees. Remove only temporary worktrees created by this invocation, and only while clean; leave preserved work accessible.
- Fetch/prune again and verify the final branch, status, and `HEAD` versus the fetched default ref. Confirm each intended remote and local deletion. Do not create tags, releases, deployments, or notification messages as an incidental part of shipping.

## Finish the project’s release process

For “release this”, confirm the version update, existing changelog’s dated release section, and delivery to the remote default branch. A project using only these mechanisms needs no further publishing. If the requested version is already delivered and its established release steps are complete, report it complete without another bump.

Only when explicitly requested or required by the established project release workflow:

- Follow the repository's tag naming convention and tag the exact delivered version commit. Confirm that an existing tag points to that commit; never move or overwrite a conflicting tag. Create and push a tag only when that step applies.
- Publish a release on the selected host only when that step applies and its release interface is available, using the appropriate version tag and notes from the delivered changelog section or, if absent, the inspected changes. Do not include unrelated pending work in release notes. If the request requires a new tag, creating and pushing that tag is included.
- If automation owns the applicable tag/release step, verify its result instead of duplicating it. Confirm remote tags and published release URLs only for steps actually performed. On partial failure, report completed steps and resume without another version bump or duplicate release.

## Completion

Report the shipped version, merged PRs or directly pushed commit, deleted branches, and current branch/sync result. Note skipped changelog/version steps and include the release URL when published. Explicitly list any preserved branch and its reason, pending queue item, or incomplete action. For a fully successful run, a concise result is enough: “Merged #123 and #124. Removed both remote/local feature branches. On `main`, up to date with `origin/main`.”
