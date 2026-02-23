---
name: "gitlab-assistant"
description: "GitLab automation hub. Routes requests to specialized skills. ALWAYS use this skill when: (1) any GitLab operation, (2) unsure which skill to use, (3) multi-step GitLab workflows. Start here for any gitlab task."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# GitLab Assistant

Central hub for GitLab automation using the `glab` CLI. Routes requests to the most appropriate specialized skill.

## Quick Reference

| I want to... | Use this skill | Risk |
|--------------|----------------|:----:|
| Work with merge requests | `gitlab-mr` | ⚠️ |
| Work with issues | `gitlab-issue` | ⚠️ |
| Check/run CI pipelines | `gitlab-ci` | ⚠️ |
| Clone/fork/create repos | `gitlab-repo` | ⚠️ |
| Manage releases | `gitlab-release` | ⚠️ |
| Manage labels | `gitlab-label` | ⚠️ |
| Manage milestones | `gitlab-milestone` | ⚠️ |
| Manage CI/CD variables | `gitlab-variable` | ⚠️ |
| Manage groups/teams | `gitlab-group` | ⚠️ |
| Search GitLab | `gitlab-search` | - |
| Protect branches | `gitlab-protected-branch` | ⚠️ |
| Manage webhooks | `gitlab-webhook` | ⚠️ |
| Repository file operations | `gitlab-file` | ⚠️ |
| Manage wiki pages | `gitlab-wiki` | ⚠️ |
| MR/Issue discussions | `gitlab-discussion` | ⚠️ |
| Project badges | `gitlab-badge` | ⚠️ |
| Container registry | `gitlab-container` | ⚠️⚠️ |
| Security vulnerabilities | `gitlab-vulnerability` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## Routing Rules

### Rule 1: Explicit Resource Type

Route based on the GitLab resource being worked with:

| Keywords | Route to |
|----------|----------|
| MR, merge request, pull request, review, approve, merge | `gitlab-mr` |
| issue, bug, ticket, task, feature request | `gitlab-issue` |
| CI, CD, pipeline, build, job, deploy, artifacts | `gitlab-ci` |
| repo, repository, project, clone, fork | `gitlab-repo` |
| release, tag, version, changelog | `gitlab-release` |
| label, tag (for issues/MRs) | `gitlab-label` |
| milestone, sprint, iteration | `gitlab-milestone` |
| variable, secret, env, CI variable | `gitlab-variable` |
| group, team, organization, members, namespace | `gitlab-group` |
| search, find, query (global/group/project) | `gitlab-search` |
| protect branch, branch protection, access rules | `gitlab-protected-branch` |
| webhook, hook, notification callback, integration | `gitlab-webhook` |
| file, blob, content, raw (repository files) | `gitlab-file` |
| wiki, documentation page | `gitlab-wiki` |
| discussion, thread, comment, note, reply | `gitlab-discussion` |
| badge, status badge, coverage badge | `gitlab-badge` |
| container, registry, docker, image, tag (container) | `gitlab-container` |
| vulnerability, security, scan, CVE, SAST, DAST | `gitlab-vulnerability` |

### Rule 2: Common Workflows

| Workflow | Skills Involved |
|----------|-----------------|
| Code review | `gitlab-mr` (checkout, review, approve, merge) |
| Bug tracking | `gitlab-issue` (create, assign, close) |
| Deployment | `gitlab-ci` (run, status, artifacts) |
| Release process | `gitlab-release` + `gitlab-ci` |
| Project setup | `gitlab-repo` (create, clone) |

### Rule 3: Multi-Step Operations

For complex workflows that span multiple skills, coordinate them:

```
Example: "Release version 1.2.0"
1. gitlab-mr: Ensure all MRs are merged
2. gitlab-ci: Verify pipeline passes
3. gitlab-release: Create release with changelog
```

## Skills Overview

### gitlab-mr (Merge Requests)

- **Purpose**: Create, review, approve, and merge MRs
- **Key commands**: `glab mr list`, `glab mr create`, `glab mr checkout`, `glab mr merge`
- **Risk**: ⚠️ (merge is destructive)
- **Triggers**: MR, merge request, review, approve, merge, checkout

### gitlab-issue (Issues)

- **Purpose**: Track bugs, features, and tasks
- **Key commands**: `glab issue list`, `glab issue create`, `glab issue close`
- **Risk**: ⚠️ (close/delete are destructive)
- **Triggers**: issue, bug, task, ticket, feature

### gitlab-ci (CI/CD Pipelines)

- **Purpose**: View, trigger, and manage CI/CD pipelines
- **Key commands**: `glab ci status`, `glab ci view`, `glab ci run`, `glab ci artifact`
- **Risk**: ⚠️ (run triggers compute resources)
- **Triggers**: CI, pipeline, build, job, deploy, artifacts, lint

### gitlab-repo (Repositories)

- **Purpose**: Clone, fork, create, and manage repositories
- **Key commands**: `glab repo clone`, `glab repo fork`, `glab repo create`
- **Risk**: ⚠️⚠️ (delete is highly destructive)
- **Triggers**: repo, repository, project, clone, fork

### gitlab-release (Releases)

- **Purpose**: Create and manage releases
- **Key commands**: `glab release create`, `glab release list`, `glab release view`
- **Risk**: ⚠️ (creates tags and releases)
- **Triggers**: release, version, changelog, tag

### gitlab-label (Labels)

- **Purpose**: Manage project labels
- **Key commands**: `glab label create`, `glab label list`
- **Risk**: ⚠️ (affects issue/MR categorization)
- **Triggers**: label, tag (for categorization)

### gitlab-milestone (Milestones)

- **Purpose**: Manage project milestones
- **Key commands**: `glab milestone create`, `glab milestone list`
- **Risk**: ⚠️ (affects planning)
- **Triggers**: milestone, sprint, iteration

### gitlab-variable (CI/CD Variables)

- **Purpose**: Manage CI/CD variables and secrets
- **Key commands**: `glab variable set`, `glab variable list`
- **Risk**: ⚠️⚠️ (contains secrets)
- **Triggers**: variable, secret, env var, CI variable

### gitlab-group (Groups - API)

- **Purpose**: Manage groups, members, subgroups via API
- **Key commands**: `glab api groups`, `glab api groups/:id/members`
- **Risk**: ⚠️ (group management)
- **Triggers**: group, team, organization, members, namespace

### gitlab-search (Search - API)

- **Purpose**: Search across GitLab (projects, issues, code, etc.)
- **Key commands**: `glab api "search?scope=...&search=..."`
- **Risk**: - (read-only)
- **Triggers**: search, find, query

### gitlab-protected-branch (Protected Branches - API)

- **Purpose**: Manage branch protection rules
- **Key commands**: `glab api projects/:id/protected_branches`
- **Risk**: ⚠️ (affects branch access)
- **Triggers**: protect branch, branch protection, access rules

### gitlab-webhook (Webhooks - API)

- **Purpose**: Manage project webhooks
- **Key commands**: `glab api projects/:id/hooks`
- **Risk**: ⚠️ (external integrations)
- **Triggers**: webhook, hook, notification, integration

### gitlab-file (Repository Files - API)

- **Purpose**: Read/write repository files via API
- **Key commands**: `glab api projects/:id/repository/files/:path`
- **Risk**: ⚠️ (modifies files)
- **Triggers**: file, blob, content, raw

### gitlab-wiki (Wiki - API)

- **Purpose**: Manage project wiki pages
- **Key commands**: `glab api projects/:id/wikis`
- **Risk**: ⚠️ (documentation changes)
- **Triggers**: wiki, documentation page

### gitlab-discussion (Discussions - API)

- **Purpose**: Manage threaded discussions on MRs/issues
- **Key commands**: `glab api projects/:id/merge_requests/:iid/discussions`
- **Risk**: ⚠️ (comments)
- **Triggers**: discussion, thread, comment, note, reply

### gitlab-badge (Badges - API)

- **Purpose**: Manage project badges
- **Key commands**: `glab api projects/:id/badges`
- **Risk**: ⚠️ (project display)
- **Triggers**: badge, status badge, coverage badge

### gitlab-container (Container Registry - API)

- **Purpose**: Manage container registry images and tags
- **Key commands**: `glab api projects/:id/registry/repositories`
- **Risk**: ⚠️⚠️ (delete images is destructive)
- **Triggers**: container, registry, docker, image

### gitlab-vulnerability (Vulnerabilities - API)

- **Purpose**: Manage security vulnerabilities (Ultimate)
- **Key commands**: `glab api projects/:id/vulnerabilities`
- **Risk**: ⚠️ (security state changes)
- **Triggers**: vulnerability, security, scan, CVE

## Connection Verification

Before any operation, verify GitLab is configured:

```bash
glab auth status
```

If not authenticated:
```bash
glab auth login
```

Check current repository context:
```bash
glab repo view
```

## Common glab Commands Quick Reference

```bash
# Authentication
glab auth login              # Interactive login
glab auth status             # Check auth status

# Merge Requests
glab mr list                 # List MRs
glab mr create               # Create MR
glab mr view <id>            # View MR details
glab mr checkout <id>        # Checkout MR branch
glab mr merge <id>           # Merge MR

# Issues
glab issue list              # List issues
glab issue create            # Create issue
glab issue view <id>         # View issue
glab issue close <id>        # Close issue

# CI/CD
glab ci status               # Current pipeline status
glab ci view                 # Interactive pipeline view
glab ci run                  # Trigger pipeline
glab ci artifact             # Download artifacts

# Repository
glab repo clone <path>       # Clone repository
glab repo fork <path>        # Fork repository
glab repo view               # View repo info
```

## Disambiguation

When request is ambiguous, ask for clarification:

| Ambiguous Request | Clarifying Question |
|-------------------|---------------------|
| "Show me the status" | "Do you want CI pipeline status (`glab ci status`) or MR status (`glab mr list`)?" |
| "Create a new one" | "What would you like to create? An issue, MR, or repository?" |
| "List everything" | "What would you like to list? MRs, issues, pipelines, or repos?" |

## Related Documentation

- [Decision Tree](./docs/DECISION_TREE.md)
- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
