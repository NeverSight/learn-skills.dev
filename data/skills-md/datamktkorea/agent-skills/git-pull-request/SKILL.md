---
name: git-pull-request
description: This skill is used by the AI agent to automatically generate Pull Request (PR) content by analyzing Git commit logs and branch strategies. It activates when the user requests to "Create a PR," "Summarize changes," or specifies a commit range for documentation.
---

# Git Pull Request Message Convention

This skill automates the analysis of commit logs to save time and ensure consistent PR documentation according to team conventions.

## When to Use This Skill

Activate this skill when the user:

- Requests PR creation ("Write a PR for me," "Generate PR content").
- Needs a summary of work between branches or specific commits ("[Hash] to latest").
- Has completed work in `features/*`, `hotfix/*`, or `develop` branches and is ready to merge.

## How to Generate Pull Request Content

### Step 1: Environment & Branch Analysis

The agent identifies the current environment and determines the target parent branch.

1. **Check Current Branch**: `git branch --show-current`
2. **Determine Parent Branch**:

   | Current Branch | Parent Branch         | Description                          |
   | :------------- | :-------------------- | :----------------------------------- |
   | `features/*`   | `main` (or `develop`) | Feature branches PR to main/develop. |
   | `hotfix/*`     | `main`                | Hotfixes PR directly to main.        |
   | Others         | `main`                | Default target is main.              |

### Step 2: Extract Changes

Analyze the differences between the parent branch and the current branch.

- **Commit Log Analysis**:
  - `git log --oneline <parent-branch>..<current-branch>`
  - `git log --format="%h|%s|%b" <parent-branch>..<current-branch>`
- **File Diff Analysis**:
  - `git diff --name-status <parent-branch>..<current-branch>`
  - `git diff --stat <parent-branch>..<current-branch>`

### Step 3: Parse and Categorize Commits

Map commits to PR categories based on Gitmojis and Types.

**Gitmoji Mapping:**

| Gitmoji | PR Category   | Description               |
| :-----: | :------------ | :------------------------ |
|   ✨    | Features      | New features              |
|   🐛    | Fixes         | Bug fixes                 |
|   📝    | Documentation | Documentation changes     |
|   ♻️    | Refactoring   | Code refactoring          |
|   🔧    | Chores        | Configurations and others |
|   🚀    | Performance   | Performance improvements  |
|   ✅    | Test          | Adding/correcting tests   |

> Always check this: [gitmoji | An emoji guide for your commit messages](https://gitmoji.dev/)

**Type Analysis:**

- `feat` → Features
- `fix` → Fixes
- `refactor` → Refactoring
- `chore` → Chores
- `perf` → Performance
- `docs` → Documentation
- `test` → Test.

### Step 4: Generate PR Content

Apply the template from `.github/PULL_REQUEST_TEMPLATE.md` or the internal guide. Generate **Review Points** by identifying complex logic or potential side effects in the code changes.

### Step 5: Finalize and Save PR Content

Since Git itself does not support PR creation, the agent should save the finalized content to a file for easy access.

1. **Review**: Present the generated content to the user.
2. **Save**: Write the content to a file (e.g., `PULL_REQUEST.md`) in the project root or a temporary directory.
3. **Instruction**: Provide the user with instructions on how to use this file (e.g., "Copy this to GitHub" or "Use `gh pr create -F PULL_REQUEST.md`").

## Guidelines

- **Accuracy**: Ensure commit hashes and messages strictly match the actual git log.
- **Selective Sections**: Only include sections that are relevant. **Omit** sections like "Related Issues," "Breaking Changes," or "Screenshots" entirely if they do not apply. Do not leave empty headers or "N/A".
- **Insightful Review Points**: Go beyond simple summaries; explain the "Why" behind decisions (e.g., trade-offs, library choices) and highlight critical logic.
- **User Preference**: If a user manually specifies a parent branch or commit range, override the automatic detection logic.

## PR Template Structure (Output Standard)

The agent must output the PR using the following Markdown structure. **Sections marked with (Optional) should be omitted if not applicable.**

```markdown
# Pull Request

## 🔗 Related Issues (Optional: Omit if none)

- Closes #123
- Fixes [JIRA-456]

## 📋 PR Title Rule

<gitmoji> <type>(<scope>): <subject>

## 🎯 Summary

<!-- Explain the purpose of the change and "Why" it was done -->

## ⚠️ Breaking Changes (Optional: Omit if none)

<!-- List compatibility issues only if they exist -->

## 📸 Screenshots (Optional: Omit if no UI changes)

<!-- Include only for UI/UX changes -->

## 💡 Review Points

<!-- Focus on critical logic, trade-offs, and decision background -->

## ✨ Changes

### 🚀 Features / 🐛 Fixes / ⚡ Performance / ♻️ Refactoring & Chores

- [x] Change description (commit_hash)

## 🛠️ Test & Verification

- [ ] Test Case 1: ...
- [ ] Test Case 2: ...

## ✅ Checklist

- [ ] PR title follows conventions
- [ ] Self-review performed
- [ ] Tests added/updated
- [ ] Documentation updated
```

## Constraints & Warnings

1. **Git Repository Required**: This skill only functions within a valid Git environment.
2. **Branch Naming**: Incorrect branch naming (not following `features/*` etc.) may lead to incorrect parent branch detection.
3. **Manual Review**: Always advise the user to review the generated content before final submission.
