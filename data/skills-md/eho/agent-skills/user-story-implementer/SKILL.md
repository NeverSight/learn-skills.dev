---
name: user-story-implementer
description: Implement a single user story or task from a GitHub Issue backlog. Executes a single Ralph Loop iteration by fetching the next open issue, assigning it, implementing the code, creating a branch and PR, and moving on. You MUST use this skill when asked to "implement a user story", "run one iteration", "do the next task", "execute a ralph loop iteration", or "complete a task from the backlog".
metadata:
  author: eho
  version: '2.0.0'
---

# Instructions

You are acting as an autonomous sub-agent to implement a user story or task managed via GitHub Issues, often as part of a single iteration of a task execution loop.

Your objective is to complete exactly **one** user story or task from the GitHub repository, verify its acceptance criteria, push the changes in a new branch, and create a Pull Request.

**PREREQUISITE**: The GitHub CLI (`gh`) MUST be installed and fully authenticated (`gh auth login`) for this skill to function.

## Workflow

1. **Identify the Next Task**: Instead of reading a progress markdown file, run `gh issue list --label "user-story" --limit 1 --search "sort:created-asc"` to grab the next available issue in creation order (lowest issue number first, matching PRD story order). Note the issue number, title, and body (which contains the Acceptance Criteria).
2. **State Management**: Before starting work, assign the issue to yourself (or the current user) using `gh issue edit <issue-number> --add-assignee "@me"`. This provides visibility and prevents conflicts.
3. **Branching**: Follow standard Git flow. Create and checkout a new branch based on the issue number: `git checkout -b feature/us-<issue-number>`.
4. **Execute**: Implement the code, configuration, or changes required to complete that single user story.
   - Ensure you fulfill all of the listed Acceptance Criteria in the GitHub issue body.
   - Write unit tests or perform browser verification if required.
   - Update any relevant documentation.
   - **Important**: If you cannot complete the entire story within ~2 hours of effort, or if you identify missing requirements or technical blockers during implementation, do NOT continue. Move to step 5 (Handling Blockers) instead.
5. **Handling Blockers**: If you encounter missing requirements, ambiguity, or blockers that prevent completion, add a comment to the issue detailing the blocker using `gh issue comment <issue-number> --body "<Details>"`, add a `blocked` label using `gh issue edit <issue-number> --add-label "blocked"`, and stop work on this issue.
6. **Self-Review**: Before considering the task complete, perform this specific checklist:
   - [ ] For each Acceptance Criterion listed in the issue, is there code implementing it? (Check each one individually.)
   - [ ] Are there new tests? Run them locally to verify they pass.
   - [ ] Do the tests exercise the core feature (not just superficial checks)?
   - [ ] Do the tests cover the happy path AND relevant error cases?
   - If all checkboxes pass, proceed to step 7. If any fail, return to step 4 to address gaps.
7. **Commit Code**: Once your user story or chunk is complete, you must commit your changes to your feature branch.
   - Do not use `git commit -a`. Select files manually.
8. **Pull Request & Linking**: 
   - Push the branch: `git push -u origin HEAD`.
   - Create a Pull Request using a heredoc to ensure newlines render correctly:
     ```bash
     gh pr create --title "feat: <issue-title>" --body "$(cat <<'EOF'
     Closes #<issue-number>

     ### Summary
     <Summary of work done>
     EOF
     )"
     ```
     Include `Closes #<issue-number>` so merging the PR automatically closes the issue.

## Loop Completion Mechanism

When you run `gh issue list --label "user-story" --limit 1 --search "sort:created-asc"` and find **no open issues**, you must signal the end of the loop.

If no specific marker string was provided to you by the user for this loop, print out:
`[RALPH_LOOP_DONE_MARKER]`

**CRITICAL WARNING**:
- Complete exactly **one** user story or task per invocation. Do not attempt to complete multiple user stories.
- If all user stories are done, you MUST output the completion marker so the loop knows to stop.

## Examples

**Example 1:**
*Input:* "Implement the next task"
*Action:*
1. Run `gh issue list --label "user-story" --limit 1 --search "sort:created-asc"`. Returns Issue #12: "Add priority selector".
2. Assign: `gh issue edit 12 --add-assignee "@me"`.
3. Branch: `git checkout -b feature/us-12`.
4. Implement the feature and write tests.
5. Review the code to ensure it meets Acceptance Criteria in Issue #12.
6. Commit: `git add src/components/TaskEdit.tsx` and `git commit -m "feat: add priority selector (US-002)"`.
7. Push: `git push -u origin HEAD`.
8. Create PR:
   ```bash
   gh pr create --title "feat: Add priority selector" --body "$(cat <<'EOF'
   Closes #12

   ### Summary
   Added priority selector to task edit.
   EOF
   )"
   ```