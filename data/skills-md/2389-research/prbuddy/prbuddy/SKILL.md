---
name: prbuddy
description: Monitors PR health by checking CI status and triaging review comments, then fixes issues and implements systematic prevention. Use when CI checks are failing, review comments are unresolved, or the user says "check my PR", "make PR green", "fix PR", "ready to merge", or "handle PR feedback".
---

<!-- ABOUTME: Main orchestrator skill for PR health management -->
<!-- ABOUTME: Routes to prbuddy:ci and prbuddy:reviews sub-skills -->

# prbuddy

## Overview

prbuddy helps agents monitor PR health by checking CI status and triaging review comments. It fixes immediate issues and implements systematic prevention measures.

**Philosophy:** "Fix the acute issue AND prevent the class of error from recurring."

**Sub-skills:**
- `prbuddy:ci` - CI/workflow monitoring, failure diagnosis, fix + prevent
- `prbuddy:reviews` - Review comment triage, fix critical, create issues for nitpicks

## Prerequisites

### Required: gh CLI

Verify `gh` is installed and authenticated:

```bash
gh auth status
```

If not authenticated, run `gh auth login`.

**Required token scopes:**
- `repo` - Full control of private repositories (for PR operations)
- `read:org` - Read org membership (for issue creation in org repos)
- `workflow` - Update GitHub Action workflows (for CI operations)

To check scopes: `gh auth status` shows granted scopes.

### Required: gh-pr-review Extension

This extension is required for review comment handling:

```bash
gh extension install agynio/gh-pr-review
```

Verify installation:

```bash
gh pr-review --help
```

### Optional: PAL MCP Server

The `prbuddy:ci` and `prbuddy:reviews` sub-skills can consult the team's PAL MCP server (`mcp__pal__chat`) for expert opinion on complex CI failures and review comment analysis. If PAL is unavailable, both sub-skills fall back to direct log analysis and code inspection without it.

## When This Skill Applies

- "check my PR" / "PR status"
- "make this PR green"
- "fix my PR"
- "ready to merge"
- "handle PR feedback"
- "what's blocking my PR"

## Workflow

### Step 1: Detect PR

```bash
gh pr view --json number,title,body,url,headRefName,closingIssuesReferences
```

If no PR found for current branch, ask user:
- Create a PR: `gh pr create`
- Specify PR number: `/prbuddy 123`
- Specify PR URL

### Step 2: Check CI Status

```bash
gh pr checks --json name,state,bucket,link
```

**If any checks failed:** Route to `prbuddy:ci`

**If checks pending:** Report status and suggest checkpoint timing:
- "CI is still running. Check again before requesting review or declaring done."

**If all checks passed:** Continue to reviews

### Step 3: Check Review Comments

Route to `prbuddy:reviews`

### Step 4: Report Summary

```
PR #42 Health Check Complete

CI: ✓ All checks passing
Reviews:
  - 2 critical comments fixed (with prevention)
  - 3 issues created from nitpicks

Ready for: [next action - request review / merge / etc.]
```

## Routing Logic

### Keywords → Sub-Skill

**prbuddy:ci:**
- "CI failing", "workflow failed", "checks red"
- "build broken", "tests failing"
- "check CI status", "rerun workflows"

**prbuddy:reviews:**
- "review comments", "address feedback"
- "reviewer asked", "changes requested"
- "handle comments", "triage reviews"

**prbuddy (full orchestrator):**
- "check my PR", "PR health", "make PR green"
- "fix PR", "ready to merge"
- Ambiguous requests

### Routing Process

1. Analyze request for keywords
2. If clearly CI-related → `prbuddy:ci`
3. If clearly reviews-related → `prbuddy:reviews`
4. Otherwise → Run full orchestrator (CI then reviews)

## Error Handling

### No PR Found

```
No PR found for current branch 'feature-xyz'.

Options:
1. Create a PR: gh pr create
2. Specify PR number: /prbuddy 123
3. Specify PR URL: /prbuddy https://github.com/owner/repo/pull/123
```

### gh-pr-review Extension Missing

```
The gh-pr-review extension is required for review comment handling.

Install it:
  gh extension install agynio/gh-pr-review

Then retry: /prbuddy:reviews
```

### gh Not Authenticated

```
GitHub CLI is not authenticated.

Run: gh auth login

Then retry: /prbuddy
```

### Fork-Based PRs

This skill assumes write access to the PR branch. For fork-based PRs:
- You may not have push access to the source branch
- Protected branch rules may prevent direct pushes
- Consider creating a fix branch and opening a separate PR

**Workaround:** Ask the user to push changes manually or grant write access.

### Dry-Run Mode

To preview changes without committing, tell the agent:
- "Show me what you would fix, but don't commit"
- "Dry-run mode" or "preview only"

The agent will analyze and report proposed fixes without making changes.
