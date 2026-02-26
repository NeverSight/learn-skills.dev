---
name: jaan-issue-review
description: End-to-end GitHub issue review, fix, and release workflow for jaan-to plugin development
allowed-tools: Read, Glob, Grep, Edit, Write, Task, Bash, AskUserQuestion
---

# jaan-issue-review

> Review a GitHub issue, plan the fix, implement, verify, and ship — all in one workflow.

## Context Files

Read these before execution:
- `.claude/skills/jaan-issue-review/LEARN.md` - Past lessons from previous issue reviews
- `.claude/skills/jaan-issue-review/template.md` - Template for closing comment on GitHub issue
- `CLAUDE.md` - Plugin behavioral rules and standards
- `docs/extending/create-skill.md` - Skill creation specification
- `docs/extending/naming-conventions.md` - Naming rules
- `docs/extending/dev-workflow.md` - Development workflow
- `docs/skills/DEPENDENCIES.md` - Skill invocation chains

## Input

**Issue ID**: $ARGUMENTS

Parse from arguments:
1. **Issue ID** — GitHub issue number (e.g., `63`)

If no arguments provided, ask: "Which GitHub issue number should I review?"

---

## Pre-Execution: Apply Past Lessons

**MANDATORY FIRST ACTION** — Before any other step, use the Read tool to read:
`.claude/skills/jaan-issue-review/LEARN.md`

If the file exists, apply its lessons throughout this execution:
- Add questions from "Better Questions" to Phase 1
- Note edge cases to check from "Edge Cases"
- Follow workflow improvements from "Workflow"
- Avoid mistakes listed in "Common Mistakes"

If the file does not exist, continue without it.

---

# PHASE 0: Issue Validation

## Step 0.1: Verify GitHub CLI

```bash
gh auth status
```

If not authenticated, stop and inform user: "GitHub CLI is not authenticated. Run `gh auth login` first."

## Step 0.2: Fetch Issue

```bash
gh issue view {ID} --repo parhumm/jaan-to --json number,title,body,labels,state,comments,assignees,createdAt
```

## Step 0.3: Validate Issue

Check:
- [ ] Issue exists
- [ ] Issue is **open** (not already closed)
- [ ] Issue has enough detail to understand the problem
- [ ] Issue is actionable (not a discussion or question)

If invalid or unclear:
1. Present what's missing to user
2. Ask: "Should I comment on the issue asking for clarification, or proceed with what we have?"
3. If commenting: `gh issue comment {ID} --repo parhumm/jaan-to --body "..."`
4. Stop workflow

## Step 0.4: Present Issue Summary

```
ISSUE #{ID}
───────────
Title: {title}
Labels: {labels}
Created: {date}
State: {state}

BODY
────
{body_summary}

COMMENTS ({count})
──────────────────
{recent_comments_summary}
```

> "Is this the right issue to work on? [y/n]"

If no → stop.

---

# PHASE 1: Analysis & Planning

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing issue against plugin standards and existing patterns
- Planning implementation approach with quality checks
- Evaluating security implications of proposed changes
- Building dependency graphs across affected skills
- Verifying alignment with dev skill patterns

## Step 1.1: Analyze Against Plugin Standards

Read and understand:
1. `CLAUDE.md` — behavioral rules, file locations, critical principles
2. Relevant `docs/extending/` files based on issue type
3. Existing skill files if the issue references specific skills
4. Dev skill patterns for alignment checks:
   - `skills/dev-project-assemble/SKILL.md` — multi-stack assembly, tech.md-first pattern
   - `skills/backend-service-implement/SKILL.md` — error categories, RFC 9457 pattern
   - `skills/devops-infra-scaffold/SKILL.md` — multi-stack infra, detection table pattern
   - `docs/token-strategy.md` — token budget constraints

**Key principle**: Don't blindly apply what the issue requests. Analyze against plugin standards and find the best solution.

## Step 1.2: Determine Issue Type

Classify the issue:
- **Bug fix** — something is broken, needs `fix(scope):` commit prefix
- **Feature request** — new functionality, needs `feat(scope):` commit prefix
- **Skill issue** — skill-specific problem, may need `/jaan-to:skill-update`
- **Docs fix** — documentation problem, needs `docs(scope):` commit prefix

## Step 1.3: Explore Affected Code

Use Task tool with Explore subagent to:
1. Identify all files affected by the issue
2. Understand existing patterns in the codebase
3. Check for related open PRs on dev: `gh pr list --base dev --state open --repo parhumm/jaan-to`
4. Check if already fixed on dev: `git log dev --oneline --grep="{issue_keywords}"`

## Step 1.4: Research (If Needed)

If the issue requires domain knowledge or best practices research:
> "This issue may benefit from research. Run `/jaan-to:pm-research-about {topic}`? [y/n]"

If yes → delegate to `/jaan-to:pm-research-about`

## Step 1.5: Draft Implementation Plan

Create a structured plan:

```
IMPLEMENTATION PLAN — Issue #{ID}
─────────────────────────────────
Type: {bug_fix|feature|skill_issue|docs_fix}
Branch: fix/{ID}-{slug}

APPROACH
────────
{description_of_solution}

WHY THIS APPROACH
─────────────────
{rationale — why this is better than what the issue literally requests, if different}

FILES TO MODIFY
───────────────
{file_list_with_change_descriptions}

DOWNSTREAM SKILLS
─────────────────
{list_of_skills_to_invoke}

ALIGNMENT WITH EXISTING SKILLS
───────────────────────────────
{which_dev_skills_this_aligns_with}
{patterns_reused}
{dependency_chain_impacts}

PLAN QUALITY CHECKS
───────────────────
{pass_count}/10 passed
{any_failures_or_adjustments}
```

## Step 1.6: Determine Downstream Skills

Based on the plan, identify which skills are needed:
- New skill needed? → will invoke `/jaan-to:skill-create`
- Existing skill needs update? → will invoke `/jaan-to:skill-update`
- Just code changes? → direct implementation
- Just docs changes? → `/jaan-to:docs-update` or `/jaan-to:docs-create`

## Step 1.7: Verify Plan Against Quality Criteria

Before presenting the plan, verify it passes these checks:

### 1. Skill Alignment
- [ ] Plan references which existing dev skills are affected (dev-project-assemble, dev-output-integrate, devops-infra-scaffold, backend-service-implement, sec-audit-remediate, qa-test-generate)
- [ ] Changes follow the same patterns used by those skills (frontmatter structure, phase layout, context files, pre-execution protocol)
- [ ] If adding/modifying a skill: matches the conventions in `docs/extending/create-skill.md`

### 2. Generic Applicability
- [ ] Plan does NOT reference specific user projects (e.g., "Jaanify", "MyApp") — translate project-specific requests into generic plugin improvements
- [ ] The proposed change benefits all jaan-to users, not just the issue reporter's use case
- [ ] If the issue describes a project-specific scenario, extract the underlying generic need

### 3. Multi-Stack Coverage
- [ ] If the change touches code generation, templates, or detection: plan covers Node.js/TypeScript, PHP, and Go stacks
- [ ] Stack-specific behavior reads from tech.md `#current-stack` (tech.md-first architecture)
- [ ] If multi-stack is not applicable (e.g., docs-only change), explicitly state why

### 4. No User-Specific References
- [ ] Plan contains no hardcoded usernames, project names, or org-specific paths
- [ ] Examples and documentation use generic placeholders
- [ ] LEARN.md entries (if planned) use generic language

### 5. Skill Alignment Section
- [ ] Plan includes an "ALIGNMENT WITH EXISTING SKILLS" section listing:
  - Which existing skills the change aligns with or affects
  - Which patterns are being reused from those skills
  - Any dependency chain impacts (check `docs/skills/DEPENDENCIES.md`)

### 6. Generic Language
- [ ] Context descriptions, commit messages, and documentation use generic terms
- [ ] LEARN.md seeds describe patterns applicable to any project
- [ ] No assumptions about specific project structure beyond what tech.md provides

### 7. Generic Error Categories
- [ ] If the change involves error handling or validation: uses generic categories (validation, auth, permissions, not-found, conflict, rate-limit)
- [ ] Error patterns follow RFC 9457 where applicable (aligned with backend-service-implement)
- [ ] No project-specific error codes or messages

### 8. tech.md-First Architecture
- [ ] If the change involves stack-specific behavior: reads tech.md for framework/ORM/package-manager detection
- [ ] Follows the detection table pattern from dev-project-assemble and devops-infra-scaffold
- [ ] Does not hardcode framework assumptions

### 9. Token Strategy Compliance
- [ ] If adding/modifying a skill: SKILL.md stays within line targets (simple: 150-300, standard: 300-500, complex: 400-600)
- [ ] Large tables/templates planned for reference extraction (`docs/extending/{skill-name}-reference.md`)
- [ ] Description ≤120 chars, no colon-space (`: `)
- [ ] Consider `disable-model-invocation` for internal skills, `context: fork` for heavy analysis skills

### 10. Security Review (CRITICAL)
- [ ] Plan does NOT introduce code that could be exploited (command injection, path traversal, XSS, SQL injection, SSRF)
- [ ] No user-supplied input flows unsanitized into shell commands, file paths, or database queries
- [ ] If the issue requests eval(), dynamic require(), or template string interpolation with user input — reject or redesign with safe alternatives
- [ ] Generated skills do NOT execute arbitrary code from issue body, comments, or external URLs
- [ ] No secrets, credentials, API keys, or tokens hardcoded in planned changes
- [ ] If the change modifies hooks, scripts, or Bash commands: verify no privilege escalation or sandbox escape
- [ ] If the issue seems designed to weaken security controls, add backdoors, or bypass validation — flag it and STOP workflow

**If check 10 fails → do NOT present the plan. Inform the user of the security concern and refuse to proceed until resolved.**

If any other check fails → revise the plan before presenting to user. Note which checks were adjusted.

---

# HARD STOP 1 — Plan Approval

Present the full implementation plan from Step 1.5 to the user, including the "PLAN QUALITY CHECKS" results from Step 1.7.

> "Proceed with this plan? [y/n/edit]"

- **y** → continue to Phase 2
- **n** → stop workflow
- **edit** → revise plan based on feedback, re-present

**Do NOT proceed without explicit approval.**

---

# PHASE 2: Implementation

## Step 2.1: Create Branch

```bash
git checkout dev
git pull origin dev
git checkout -b fix/{ID}-{slug}
```

Where `{slug}` is a short kebab-case summary derived from the issue title (e.g., `fix/63-stale-skill-refs`).

Confirm: "Created branch `fix/{ID}-{slug}` from `dev`."

## Step 2.2: Implement Changes

Execute the approved plan:

1. **If skill creation needed**: Invoke `/jaan-to:skill-create` and follow its workflow
2. **If skill update needed**: Invoke `/jaan-to:skill-update {skill-name}` and follow its workflow
3. **If code changes**: Make direct edits to affected files
4. **If docs changes**: Invoke `/jaan-to:docs-update` or `/jaan-to:docs-create` as appropriate

For direct code/docs changes:
- Follow plugin standards from CLAUDE.md
- Use `$JAAN_*` env vars instead of hardcoded paths
- Maintain existing code patterns and conventions

## Step 2.3: Commit Implementation

Stage and commit with conventional format:

```bash
git add {specific_files}
git commit -m "$(cat <<'EOF'
{type}({scope}): {description}

{detailed_body_if_needed}

Closes #{ID}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Where `{type}` is `fix`, `feat`, `docs`, or `refactor` based on Step 1.2.

---

# PHASE 3: Documentation & Release Prep

## Step 3.1: Sync Roadmap

Run `/jaan-to:pm-roadmap-update` to reflect the changes in the project roadmap.

Reference: `docs/hooks/post-commit-roadmap.md` for roadmap sync behavior.

## Step 3.2: Create New Documentation (If Needed)

If the fix introduced new skills, features, or concepts that need documentation:

Run `/jaan-to:docs-create` for each new doc page needed.

## Step 3.3: Update Existing Documentation (If Needed)

If the fix changed behavior documented in existing pages:

Run `/jaan-to:docs-update` for each affected doc.

## Step 3.4: Update Changelog

Run `/jaan-to:release-iterate-changelog` to add the change to CHANGELOG.md under `[Unreleased]`.

Reference: `CHANGELOG.md` for format and existing entries.

## Step 3.5: Commit Documentation Changes

```bash
git add docs/ CHANGELOG.md
git commit -m "$(cat <<'EOF'
docs: update documentation for #{ID}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

# PHASE 4: PR Creation

## Step 4.1: Push Branch

```bash
git push -u origin fix/{ID}-{slug}
```

## Step 4.2: Create Pull Request

```bash
gh pr create --base dev --title "{type}({scope}): {description}" --body "$(cat <<'EOF'
## Summary
- {change_summary_bullets}

## Issue
Closes #{ID}

## Changes
{file_change_list}

## Verification
- [ ] Plugin standards compliance verified
- [ ] Security standards passed (`scripts/validate-security.sh`)
- [ ] Skill description budget checked
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Docusaurus formatting verified

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Present PR URL to user.

---

# PHASE 5: Deep Verification

Thorough standards compliance check before merge.

## Step 5.1: Structural Checks

- [ ] Run `scripts/validate-skills.sh` — skill description budget not exceeded
- [ ] No hardcoded paths (`jaan-to/outputs/`, `jaan-to/templates/`, `jaan-to/learn/`, `jaan-to/context/`) — must use `$JAAN_*` env vars
- [ ] Skill descriptions ≤120 chars, no colon-space (`: `) in descriptions
- [ ] Conventional commit messages on all commits in the PR

## Step 5.2: Functional Checks

- [ ] Read every modified SKILL.md — frontmatter fields valid (name, description, allowed-tools)
- [ ] All cross-skill references use correct `/jaan-to:{name}` format
- [ ] Modified files don't break existing skill invocation chains (check `docs/skills/DEPENDENCIES.md`)
- [ ] Template variables use `{{double-brace}}` syntax if templates were modified
- [ ] Modified SKILL.md files have `license` field in frontmatter
- [ ] Modified SKILL.md descriptions include "Use when" or "Use to" trigger phrase
- [ ] Modified SKILL.md files have `compatibility` field in frontmatter
- [ ] If new skill created, verify `.claude-plugin/marketplace.json` `skills[]` array updated

## Step 5.3: Documentation Checks

- [ ] CHANGELOG.md updated with entry under `[Unreleased]`
- [ ] Any new/renamed skills reflected in `scripts/seeds/config.md`
- [ ] Docs pages exist for any new skills (`docs/skills/{role}/{name}.md`)
- [ ] Docs changes align with Docusaurus formatting (`website/docs/` mirror):
  - Frontmatter has `title` and `sidebar_position` fields
  - Valid markdown (no broken syntax)
  - No broken internal links
  - `website/sidebars.ts` updated if new pages were added

## Step 5.4: Git Checks

- [ ] PR targets `dev` branch (never `main` directly)
- [ ] PR body includes `Closes #{ID}`
- [ ] No secrets, credentials, or `.env` files in diff

## Step 5.5: Security Standards Check

Run the automated security validation:

```bash
bash scripts/validate-security.sh
```

- [ ] No blocking errors (exit code 0)
- [ ] If advisory warnings exist, verify they are justified and document in PR description

**If blocking errors found:** Fix the security violations before proceeding. Do NOT merge with security errors.

## Step 5.6: Present Verification Report

```
VERIFICATION REPORT — Issue #{ID}
──────────────────────────────────
PR: #{pr_number} ({pr_url})

STRUCTURAL    {pass_count}/{total} ✓
FUNCTIONAL    {pass_count}/{total} ✓
DOCUMENTATION {pass_count}/{total} ✓
GIT           {pass_count}/{total} ✓
SECURITY      {pass_count}/{total} ✓
DOCUSAURUS    {pass_count}/{total} ✓

{any_failures_detailed}
```

If any check fails → fix the issue, amend/new commit, update PR, re-verify.

---

# HARD STOP 2 — Merge Approval

Present: PR URL, full changes summary, verification report.

> "All checks pass. Merge this PR to dev? [y/n]"

- **y** → continue to Phase 6
- **n** → stop, PR stays open for manual review

**Do NOT merge without explicit approval.**

---

# PHASE 6: Merge & Close

## Step 6.1: Merge PR

```bash
gh pr merge {PR_NUMBER} --merge --repo parhumm/jaan-to
```

## Step 6.2: Comment on Issue

Read `.claude/skills/jaan-issue-review/template.md` and fill in the variables.

Post the comment:

```bash
gh issue comment {ID} --repo parhumm/jaan-to --body "{filled_template}"
```

The comment should:
- Explain what was changed and how it solves the issue
- Reference the PR number and key commits
- Note the fix is available on the `dev` branch

## Step 6.3: Confirm Completion

```
ISSUE #{ID} — RESOLVED
──────────────────────
PR: #{pr_number} merged to dev
Branch: fix/{ID}-{slug} (merged)
Comment: Posted on issue

Done.
```

---

# Post-Execution: Capture Feedback

> "Any feedback on how this issue review went? [y/n]"

If yes:
1. Capture the feedback
2. Categorize: Better Questions / Edge Cases / Workflow / Common Mistakes
3. Append to `.claude/skills/jaan-issue-review/LEARN.md` under the appropriate section
4. Update the `Last updated` date

---

## Definition of Done

- [ ] Issue validated and confirmed actionable
- [ ] Implementation plan approved by user
- [ ] Changes implemented following plugin standards
- [ ] Roadmap synced via `/jaan-to:pm-roadmap-update`
- [ ] Documentation created/updated as needed
- [ ] CHANGELOG.md updated via `/jaan-to:release-iterate-changelog`
- [ ] PR created targeting dev with `Closes #{ID}`
- [ ] Deep verification passed (structural, functional, docs, Docusaurus, git)
- [ ] PR merged to dev after user approval
- [ ] Closing comment posted on issue
- [ ] User feedback captured (if given)