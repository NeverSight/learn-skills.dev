---
name: bot-dependency-automerge
description: >
  Audits a repository's dependency bot and arms GitHub auto-merge on Dependabot
  or Renovate minor and patch PRs when they open, with majors left to a human.
  Supports GitHub merge queues and hands PRs to Mergify, Kodiak, Trunk, or
  Aviator queues.
  Use when the user says "auto-merge dependabot", "automerge renovate minor and
  patch", "dependabot PRs never merge", "set up bot dependency auto-merge",
  "audit dependency bot auto-merge", or invokes /bot-dependency-automerge.
  Do NOT use to create a first dependabot.yml (/oss-hygiene), to change
  rulesets or merge settings (/gh-bootstrap), or for an org-wide rollout
  (/safe-settings).
license: MIT
---

# bot-dependency-automerge

Arm GitHub auto-merge on each minor or patch dependency-bot PR when it opens, while its required checks are still pending.

## Why arm at open

- GitHub offers auto-merge only on a PR that cannot merge yet. A later job that reaches a green PR cannot arm it.
- `gh pr merge --auto` merges at once when the merge state is `CLEAN`, `HAS_HOOKS`, or `UNSTABLE`. Without required checks, that merge comes before CI.
- Auto-merge waits only for required status checks and reviews. Other checks do not hold the merge.

## Scope

This skill covers one repository: an audit, the Dependabot workflow or the Renovate rule, and a report. Major updates stay open for a human. Settings, rulesets, and branch protection change only after explicit user approval. Route that work to /gh-bootstrap.

## Inputs

The text after the skill name is an optional `owner/repo`. Without it, use the repository of the current checkout.

## Flow

1. **Audit.** The audit is read-only. Set `REPO` to the `owner/repo` input when one is given. Set `BASE` to the base branch of the recent bot PRs. Then run these commands:

   ```bash
   R=${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}
   gh api "repos/$R" --jq '{allow_auto_merge,allow_squash_merge,allow_merge_commit,allow_rebase_merge,default_branch}'
   gh pr list -R "$R" --state all --limit 50 --json author,baseRefName \
     --jq 'map(select(.author.is_bot)) | group_by(.author.login + " -> " + .baseRefName) | map({bot: .[0].author.login, base: .[0].baseRefName, prs: length})'
   gh api "repos/$R/rules/branches/$BASE" --jq '[.[] | select(.type == "required_status_checks") | .parameters.required_status_checks[].context]'
   gh api "repos/$R/branches/$BASE" --jq '{protected, classic: (.protection.required_status_checks.checks // [] | map(.context))}'
   gh api "repos/$R/rules/branches/$BASE" --jq '[.[] | select(.type == "merge_queue") | .parameters.merge_method]'
   ```

   Also list the bot config files: `.github/dependabot.yml`, `renovate.json`, `renovate.json5`, `.github/renovate.json`, `.github/renovate.json5`, `.renovaterc`, `.renovaterc.json`, and a `renovate` key in `package.json`.
   Search `.github/workflows/` for `fetch-metadata`, `gh pr merge`, `github.actor`, and `merge_group`.
   Find a third-party merge queue with the config files and check runs in `references/merge-queues.md`.
   Recent PR authors identify the active bot (`app/dependabot`, `app/renovate`). A config file alone does not, because the app can be uninstalled.
   A required check can come from a ruleset or from classic protection, so read both.
   A `null` value or an HTTP 404 means missing permission. Report it as `unknown`, not as `false` or `none`.
   Done when each row of the output audit table holds a value or `unknown`.

2. **Stop when no bot is active.** Report the audit. Route a first `dependabot.yml` to /oss-hygiene.
   Done when the report names the missing bot.

3. **Report the missing preconditions.** Name each one with its effect:

   | Precondition | Effect when missing |
   | --- | --- |
   | `allow_auto_merge` is `true` | The Dependabot workflow cannot arm. Renovate falls back to merging on its own run after checks pass. |
   | A required status check on `BASE` | The template guard does not arm, so Dependabot PRs stay open. Renovate platform auto-merge can merge before tests finish. When the checks are `none` or `unknown` and `BASE` has no GitHub merge queue, add `"platformAutomerge": false` to the Renovate rule. Renovate then merges only after every status check passes. |
   | The merge method of the template is allowed | Change `--squash` to an allowed method. |
   | A GitHub merge queue on `BASE` has an App token and `merge_group` checks | `GITHUB_TOKEN` cannot add a PR to the queue. A required check without `merge_group` never reports, so the queue drops the PR. |

   Ask before any settings or ruleset change. Name the exact change in the question.
   Done when each missing precondition is named with its effect and its fix.

4. **Set up the arm-at-open path** for each active bot. With a merge queue, copy the files below first, then apply the changes in `references/merge-queues.md`. With a third-party queue, never arm GitHub auto-merge.
   - **Dependabot:** copy `assets/dependabot-automerge.yml` to `.github/workflows/dependabot-automerge.yml`.
     Keep the default 3-day cooldown. Do not set a lower cooldown. Make sure `.github/dependabot.yml` lists the `github-actions` ecosystem.
   - **Renovate:** append the rule in `assets/renovate-automerge.json` to `packageRules` in the existing config file.
     A later rule overrides an earlier one. When the config sets `automerge: false` anywhere, stop and ask before you add the rule.
     Keep the default `platformAutomerge` when `BASE` has a required check. Propose `helpers:pinGitHubActionDigests` in `extends` when the config does not pin action digests.

   Done when each written file parses, and the change adds only the arm-at-open path.

5. **Pin and verify.** Pin each `uses:` to a 40-character commit SHA with a `# vX.Y.Z` comment.
   Resolve the latest release with `gh api repos/OWNER/ACTION/releases/latest --jq .tag_name`.
   Resolve its commit with `gh api repos/OWNER/ACTION/git/ref/tags/TAG --jq '.object.type + " " + .object.sha'`.
   For type `tag`, run `gh api repos/OWNER/ACTION/git/tags/SHA --jq .object.sha` to get the commit.
   Run the repository's workflow linters, such as zizmor, actionlint, and yamllint, when they are present.
   Done when each pin matches its tag's commit and each present linter exits 0.

6. **Report** with the output block.
   Done when each audit row, missing precondition, change, and verification result appears in the block.

## Merge token

A merge by auto-merge that a `GITHUB_TOKEN` workflow armed is not expected to start `push` workflows on `BASE`. GitHub documents that `GITHUB_TOKEN` events start no new runs. It does not document the auto-merge actor. After the first auto-merge, check with `gh run list --event push --branch BASE --limit 3`.
When a release or deploy workflow must run on push, offer `references/github-app-token.md`.

## Supply-chain defaults

- **Release age.** Dependabot waits 3 days by default. The Renovate rule sets `minimumReleaseAge: "3 days"`. The malicious Nx and chalk releases of 2025 were live for hours.
- **Security updates.** Dependabot security updates skip the cooldown. The workflow still arms a minor or patch security update. State this in the report.
- **SHA pins.** A moved tag, as in tj-actions/changed-files, cannot change a SHA pin.

## Output

```markdown
## bot-dependency-automerge: <owner/repo>

| Check | Value | Evidence |
| --- | --- | --- |
| Active bot | dependabot / renovate / both / none | recent PR authors |
| Bot config | <path> / none | file list |
| PR base branch | <BASE> (default: <branch>) | bot PR baseRefName |
| allow_auto_merge | true / false / unknown | repo API |
| Merge methods | <allowed list> / unknown | repo API |
| Required checks on <BASE> | <contexts> / none / unknown | rules and branch API |
| Merge queue | github (<method>) / mergify / kodiak / trunk / aviator / graphite / bors-ng / none / unknown | rules API, config files, check runs |
| Existing automation | <workflow paths> / none | workflow search |

### Missing preconditions
<precondition — effect — fix — approval needed>

### Changes
<path — what changed>

### Verification
<command — result>

### Not done
<item — reason>
```

## What this skill never does

- It never merges a PR, and it never arms auto-merge on a major update.
- It never changes settings, rulesets, or branch protection without explicit approval.
- It never uses `pull_request_target` or a `github.actor` check in a bot gate. An attacker can spoof `github.actor`, so the gate checks `github.event.pull_request.user.login` and the repository.
- It never writes a tag-pinned or branch-pinned action, or a credential.

## References

- `references/merge-queues.md` — read when the audit finds a GitHub or third-party merge queue.
- `references/github-app-token.md` — read when push workflows must run after the merge, or `BASE` has a GitHub merge queue.
- `references/evidence.md` — read when the user asks why a default exists, or challenges one.
