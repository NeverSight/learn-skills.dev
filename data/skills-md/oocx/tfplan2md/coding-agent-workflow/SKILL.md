---
name: coding-agent-workflow
description: Standard workflow for GitHub Copilot coding agents including report_progress usage, delegation handling, and PR communication patterns.
---

# Coding Agent Workflow Skill

## Purpose
Provides the standard operational workflow that all GitHub Copilot coding agents must follow when executing tasks in pull requests.

## When to Use
This skill is automatically loaded by all coding agents. It defines the core workflow for:
- Handling questions (direct vs delegated contexts)
- Reporting progress with the `report_progress` tool
- Creating summary comments after work completion

## Workflow

**You are running as a GitHub Copilot coding agent.** Follow this workflow:

### CRITICAL: Branch and PR Management

**GitHub Copilot automatically creates branches and PRs** - you do NOT create them:
- When an issue is assigned to `@copilot`, GitHub automatically creates a `copilot/*` branch and draft PR
- When you start working, you're already on the correct branch with an active PR
- **NEVER run `git checkout`, `git switch`, or `git branch` commands** - you're already on the right branch
- **NEVER attempt to create a new PR** - one already exists for your work
- Your job is to commit work to the existing branch using `report_progress` (which handles git push automatically)

**Why this fails:**
- Manual `git checkout -b` commands will fail (permission denied)
- Attempting to create PRs will fail or create duplicate PRs
- These operations are GitHub's responsibility, not yours

1. **For Direct Questions (When Running as Primary Agent)**: If you are the primary agent on a PR (not delegated via `task` tool), you can create PR comments to ask the Maintainer questions. Wait for a response before proceeding.

2. **For Delegated Execution (When Invoked via `task` Tool)**: If you were invoked by the Workflow Orchestrator via the `task` tool, you run in an isolated context. In this case:
   - **DO NOT attempt to create PR comments** - you cannot access the parent PR from your isolated context
   - **Include questions in your response** - return them as part of your output text
   - **The orchestrator will forward your questions** to the maintainer and resume you with answers
   - **Wait for the orchestrator to re-invoke you** with the maintainer's answer
   - **You MUST use `edit`/`create` tools to apply all file changes** - do not just describe changes; actually apply them
   - **You MUST use `git commit` to commit your changes** — `report_progress` is NOT available to subagents; use `git add <files> && git commit -m "type: message"` instead (see step 4 for details)

3. **Complete Your Work**: Implement the requested changes following your role's guidelines. **Use `edit`/`create` tools to apply all file modifications** — never just describe or list changes without applying them.

4. **Commit and Push Changes**:

   - **Primary agent** (running the top-level PR): Use the `report_progress` tool. It handles `git add`, `git commit`, and `git push` automatically with the GitHub Actions token. Manual `git push` fails (no personal credentials). Call it with:
     - `commitMessage`: Conventional commit message (e.g., "feat: add feature X")
     - `prDescription`: Markdown checklist showing completed and remaining work

     ```
     report_progress(
       commitMessage="feat: implement user authentication",
       prDescription="""
       - [x] Add authentication service
       - [ ] Add authorization middleware
       """
     )
     ```

   - **Delegated subagent** (spawned via `task` tool): **`report_progress` is NOT available** — it exists only in the primary agent's tool context. Use `git commit` instead:
     ```bash
     git add <changed files>
     git commit -m "type: description of changes"
     # Do NOT run git push — it will fail with HTTP 403
     ```
     Your commits accumulate in the local branch. When the parent agent calls `report_progress`, ALL local commits (including yours) are pushed to the remote PR branch.

5. **Create Summary Comment (After Progress Reported)**: Post a PR comment with:
   - **Summary**: Brief description of what you completed
   - **Changes**: List of key files/features modified
   - **Next Agent**: Recommend which agent should continue the workflow (see docs/agents.md for workflow sequence)
   - **Status**: Ready for next step, or Blocked (with reason)
   
   **Note**: If you're running in delegated mode (via `task` tool), include this summary in your response text instead of creating a PR comment.

**Example Summary Comment:**
```
✅ Implementation complete

**Summary:** Implemented feature X with tests and documentation

**Changes:**
- Added FeatureX.cs with core logic
- Added FeatureXTests.cs with 15 test cases
- Updated README.md

**Next Agent:** Technical Writer (to review documentation)
**Status:** Ready
```

## Key Principles

- **GitHub creates branches/PRs automatically** - never attempt to create them yourself
- **`report_progress` is only available to the primary agent** - subagents spawned via `task` tool must use `git commit` instead
- **Always use `report_progress`** for commits and pushes (primary agent) - never use manual `git push` commands
- **Subagents MUST `git commit` before completing** - uncommitted changes will be lost if only in memory; the parent's `report_progress` can pick up uncommitted files via `git add .` but this is a fallback, not the primary mechanism
- **Always use `edit`/`create` tools** to apply file changes - never just describe changes in your response without applying them
- **Respect execution context** - behave differently when delegated vs primary agent
- **Communicate clearly** - provide complete summaries with status and next steps
- **Track progress** - use markdown checklists in PR descriptions to show work completed and remaining
