---
name: git-worktree
description: Create a git worktree for the current repository at the same directory level as the project root. This skill automates branch creation, directory naming according to the format project-T-branch, and initial project setup (e.g., dependency installation). Use this when the user wants to work on a new feature or fix without switching their current workspace.
---

# Git Worktree

## Overview

This skill allows you to quickly create a new git worktree for the current project. The worktree is created in the same parent directory as the current project's root, following the naming convention `PROJECT-NAME-T-BRANCH-NAME`.

## Workflow

1.  **Verification**: 
    -   Verify the current directory is within a Git repository.
    -   Identify the absolute path of the project's root.
2.  **User Interaction**: Proactively suggest values for the required parameters. Ask the user for:
    -   **New branch name**: The name of the branch to be created. **Suggest a context-aware name** (e.g., `feat-improvement` or `fix-issue-123` based on context.
    -   **Base branch**: The branch to base the new branch on (**Default**: the current branch).
    
    **Crucially**, if the user does not respond to a question or provides no alternative, **proceed immediately using your suggested values** instead of repeating the question. The goal is to minimize friction while allowing for customization.
3.  **Path Calculation**: Calculate the new worktree path at the same directory level as the project root. For example, if the project is in `/Users/user/my-project`, the worktree will be created at `/Users/user/my-project-T-NEW-BRANCH`.
4.  **Creation**: Execute `scripts/create_worktree.sh` to:
    -   Create the new worktree and branch.
    -   Perform initial project setup (e.g., `flutter pub get`, `npm install`).
5.  **Confirmation**: Report the location of the new worktree and any initial setup status.
6.  **Management**: Use `scripts/manage_worktrees.sh` to:
    -   List all current project worktrees.
    -   Interactively select and remove a specific worktree.

## Usage Example

**User**: "Create a worktree for this repo."
**Gemini**: "I'll create a new worktree for you. I'll use the branch name `feat-wyatt_skills-260221` based on the current branch `main`. Is that okay, or would you like a different name?"
**User**: "That's fine."
**Gemini**: [Runs the script and confirms the path `/Users/huwentao/_proj/wyatt_skills-T-feat-wyatt_skills-260221`]

**Another Example (Proactive/No Response)**:
**User**: "Create a worktree for feature-login."
**Gemini**: "I'll create a worktree for `feature-login` based on `main`. Starting the setup now..."
**Gemini**: [Runs the script and confirms the path `/Users/huwentao/_proj/foo_proj-T-feature-login`]

**Manage Worktrees**:
**User**: "Show my worktrees and help me delete one."
**Gemini**: "Here are your current worktrees. Which one would you like to remove?"
**Gemini**: [Lists worktrees and prompts for selection via `scripts/manage_worktrees.sh`]

## Resources

### scripts/

*   `create_worktree.sh`: A bash script that calculates the paths, runs `git worktree add`, and performs initial project setup.
    *   Arguments: `project_path` `new_branch` `base_branch`
*   `manage_worktrees.sh`: A script to list and interactively remove worktrees.
    *   Arguments: `project_path`
