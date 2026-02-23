---
name: github-cli
description: 'GitHub CLI workflows for repositories, issues, pull requests, actions, releases, projects, and API calls. Use when creating PRs, reviewing code, triaging issues, triggering workflows, publishing releases, managing projects, verifying attestations, or querying the GitHub API. Use for gh cli, github automation, code review, release management.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# GitHub CLI Skill

Provides patterns for the `gh` CLI to interact with GitHub repositories, services, and APIs directly from the terminal. Covers authentication, repository management, issues, pull requests, actions, releases, projects, search, and the REST/GraphQL API. Git workflow patterns (branching, commits, CI/CD) are handled by a separate skill.

## Quick Reference

| Area          | Key Commands                                                          |
| ------------- | --------------------------------------------------------------------- |
| Auth          | `gh auth status`, `gh auth login`, `gh auth token`                    |
| Repos         | `gh repo clone`, `gh repo create`, `gh repo fork`, `gh repo sync`     |
| Browse        | `gh browse`, `gh browse --settings`, `gh browse file.ts:42`           |
| Issues        | `gh issue list`, `gh issue create`, `gh issue edit`, `gh issue close` |
| Pull Requests | `gh pr create`, `gh pr review`, `gh pr merge`, `gh pr checkout`       |
| Actions       | `gh run list`, `gh run view`, `gh workflow run`, `gh cache list`      |
| Releases      | `gh release create`, `gh release list`, `gh release verify`           |
| Projects      | `gh project list`, `gh project create`, `gh project item-add`         |
| Search        | `gh search repos`, `gh search issues`, `gh search code`               |
| API           | `gh api repos/{owner}/{repo}`, `gh api graphql`                       |
| Security      | `gh attestation verify`, `gh ruleset list`, `gh secret set`           |
| Status        | `gh status`, `gh pr checks`, `gh pr status`                           |
| Codespaces    | `gh codespace create`, `gh codespace ssh`, `gh codespace code`        |

## Common Workflows

| Workflow             | Commands                                                                                      |
| -------------------- | --------------------------------------------------------------------------------------------- |
| Quick PR             | `git push -u origin feat` then `gh pr create --fill`                                          |
| Draft PR             | `gh pr create --draft --fill` then `gh pr ready` when done                                    |
| Review and merge     | `gh pr checkout 45` then `gh pr review --approve` then `gh pr merge --squash --delete-branch` |
| Auto-merge PR        | `gh pr merge --auto --squash` (waits for required checks to pass)                             |
| Check CI             | `gh pr checks` then `gh run watch`                                                            |
| Rerun failed CI      | `gh run rerun <run-id> --failed`                                                              |
| Create release       | `gh release create v1.0.0 --generate-notes`                                                   |
| Search code          | `gh search code "handleAuth" --repo owner/repo`                                               |
| Add issue to project | `gh project item-add 1 --owner @me --url <issue-url>`                                         |
| Verify artifact      | `gh attestation verify artifact.tar.gz --owner owner`                                         |
| Trigger workflow     | `gh workflow run deploy.yml -f environment=production`                                        |
| Revert merged PR     | `gh pr revert 45`                                                                             |
| Sync fork            | `gh repo sync` to update fork from upstream                                                   |

## Output Formatting

Most `gh` list and view commands support structured output for scripting and automation.

| Flag         | Purpose                           |
| ------------ | --------------------------------- |
| `--json`     | Output specified fields as JSON   |
| `--jq`       | Filter JSON with jq expressions   |
| `-t`         | Format JSON with Go templates     |
| `--web`      | Open the resource in a browser    |
| `--comments` | Include comments (issues and PRs) |

## Scoping: Repo, Env, Org

Secrets and variables can be scoped to different levels.

| Scope        | Flag Example                                |
| ------------ | ------------------------------------------- |
| Repository   | `gh secret set KEY` (default)               |
| Environment  | `gh secret set KEY --env production`        |
| Organization | `gh secret set KEY --org name --visibility` |

Project commands always require `--owner @me` or `--owner org-name`.

## Authentication Prerequisites

The `gh` CLI requires authentication before most commands work. Run `gh auth status` to verify the current session. Missing scopes cause silent failures -- use `gh auth refresh -s scope` to add scopes without re-authenticating. For CI environments, set the `GITHUB_TOKEN` or `GH_TOKEN` environment variable instead of interactive login.

## Common Mistakes

| Mistake                                                         | Correct Pattern                                                          |
| --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Running `gh pr create` without pushing the branch first         | Push with `git push -u origin branch` before creating a PR               |
| Using `gh pr merge` without checking CI status                  | Run `gh pr checks` first or use `gh pr merge --auto` to wait for checks  |
| Forgetting `--fill` when creating PRs from well-written commits | Use `gh pr create --fill` to auto-populate title and body from commits   |
| Using REST API when GraphQL is more efficient for nested data   | Use `gh api graphql` for queries needing related objects in one call     |
| Not authenticating with correct scopes                          | Run `gh auth status` to verify scopes, `gh auth refresh -s scope` to add |
| Using `gh project` commands without specifying `--owner`        | Always pass `--owner @me` or `--owner org-name` for project commands     |
| Manually downloading CI artifacts                               | Use `gh run download <run-id>` to download artifacts programmatically    |
| Not using `--json` for scripting                                | Add `--json field1,field2` and `--jq` for machine-readable output        |
| Merging without `--delete-branch`                               | Use `gh pr merge --squash --delete-branch` to clean up after merge       |
| Running `gh api` POST without `-f` fields                       | Use `-f key=value` for string fields, `-F` for typed fields              |

## Delegation

- **Search across repositories for code patterns or issues**: Use `Explore` agent with `gh search code` and `gh search issues`
- **Automate multi-step release workflows**: Use `Task` agent to coordinate branch creation, PR merge, and release publishing
- **Plan repository structure and access controls**: Use `Plan` agent to design team permissions, branch protection, and workflow architecture

## References

- [Repos & Auth](references/repos-auth.md) -- Authentication, repository management, configuration, extensions, aliases
- [Issues](references/issues.md) -- Issue CRUD, labels, assignments, pinning, transferring, development branches
- [Pull Requests](references/pull-requests.md) -- PR creation, review, merge, checkout, checks, diff, auto-merge
- [Actions](references/actions.md) -- Workflow runs, manual triggers, secrets, variables, caches, artifact downloads
- [Releases & Search](references/releases-search.md) -- Releases, attestation verification, search, gists, SSH/GPG keys
- [Projects & API](references/projects-api.md) -- Projects v2 management, REST API, GraphQL API, rulesets, status
