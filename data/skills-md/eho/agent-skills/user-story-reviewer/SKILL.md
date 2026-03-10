---
name: user-story-reviewer
description: Review an implemented user story or task (via GitHub Pull Request) for completeness, test coverage, and code quality. Use this when asked to QA, review a PR, verify implementation, or as a follow-up to the user-story-implementer skill.
metadata:
  author: eho
  version: '2.0.0'
---

# User Story Reviewer

You are acting as an autonomous QA and code review sub-agent. Your job is to thoroughly review a recently implemented user story (submitted as a Pull Request) against its original requirements in the linked GitHub Issue.

**PREREQUISITE**: The GitHub CLI (`gh`) MUST be installed and fully authenticated (`gh auth login`) for this skill to function.

## The Objective

Too often, implementations miss subtle acceptance criteria, lack meaningful test coverage, or fail to update documentation. Your objective is to proactively identify such gaps. You will not approve a Pull Request until it fully passes all checks.

## Workflow

1. **Identify the Target PR**:
   - If the user specified a PR number or URL in their input, use that PR.
   - Otherwise, run `gh pr list --state open --limit 1 --search "sort:created-asc"` to find the oldest open pull request that needs review (matching PRD story order).
2. **Read the Requirements (The Issue)**:
   - Identify the linked issue. Usually, the PR body will contain `Closes #<issue-number>`.
   - Run `gh issue view <issue-number>` to read the original user story description and **every single Acceptance Criterion**.
3. **Analyze the Implementation**: Review the code changes made in the Pull Request.
   - Run `gh pr diff <pr-number>` to view the changes.
   - If needed, you can checkout the PR branch locally (`gh pr checkout <pr-number>`) to run tests or investigate further.
4. **Conduct the Review**: Evaluate the implementation across the key dimensions (see Review Dimensions below). Document any gaps or issues found.
5. **Report & Fix**:
   - If there are NO gaps, proceed to step 6.
   - If there ARE gaps:
     - **Fix yourself if the gap is small and clear** (e.g., missing a single test, typo in comment, adding 1-2 lines of code). Checkout the PR branch with `gh pr checkout <pr-number>`, make the fix, commit with `git add <specific-files>` (not `git add .`), and push.
     - **Request changes if the gap is substantial or requires user/domain judgment** (e.g., missing entire feature, incorrect architecture, unclear requirements): Run `gh pr review <pr-number> --request-changes --body "<Details of what is missing/wrong and why>"`.
   - Only proceed to step 6 once all gaps are resolved.
6. **Sign off (Approve or Merge PR)**: Determine if you are the author of the PR. GitHub prevents users from approving their own PRs. If you are the author, leave a comment and merge it. If you are not, formally approve the PR.
   ```bash
   PR_AUTHOR=$(gh pr view <pr-number> --json author -q .author.login)
   CURRENT_USER=$(gh api user -q .login)
   
   REVIEW_BODY=$(cat <<'EOF'
   Reviewed and verified:
   - All acceptance criteria met
   - Tests passing
   - Code quality acceptable
   - Documentation updated (if applicable)
   EOF
   )

   if [ "$PR_AUTHOR" = "$CURRENT_USER" ]; then
     gh pr review <pr-number> --comment --body "$REVIEW_BODY"
     gh pr merge <pr-number> --squash --delete-branch
   else
     gh pr review <pr-number> --approve --body "$REVIEW_BODY"
   fi
   ```

## Review Dimensions

### 1. Requirements & Implementation Alignment
- Does the implementation fully solve the problem outlined in the user story description?
- Walk through **each individual Acceptance Criterion**. Does the codebase strictly satisfy every single one?
- Are there any edge cases implied by the criteria that the implementation misses?

### 2. Test Coverage & Quality
- Are there newly added unit, integration, or browser tests?
- Do the tests *actually* exercise the core logic of the new feature, or are they superficial?
- Do the tests cover both the "happy path" and relevant error/edge cases?
- Run the tests locally to ensure they actually pass.

### 3. Documentation & Code Quality
- **Documentation**: Check if the project has a README, API docs, or user guide. If this feature adds user-facing functionality (new command, option, UI element, etc.), those docs MUST be updated. If it's an internal refactor or non-user-facing change, documentation updates are optional.
- Is the code clean, readable, and following the project's established style guidelines?
- Did the implementation introduce any obvious security or performance issues?

## Examples

**Example 1:**
*Input:* "Review the latest open PR."
*Action:*
1. Run `gh pr list --state open --limit 1 --search "sort:created-asc"`. Returns PR #13: "feat: Add priority selector".
2. Read the PR body and find `Closes #12`.
3. Run `gh issue view 12` and note the acceptance criteria: Dropdown in modal, shows current priority, saves immediately, type-checks pass.
4. Run `gh pr diff 13` to review the code changes in `TaskEdit.tsx` and `TaskEdit.test.tsx`.
5. Notice that changes were made to save immediately, but no tests verify the immediate save functionality.
6. Check out the PR: `gh pr checkout 13`. This is a small, clear gap (missing test), so fix it yourself.
7. Write the missing test in `TaskEdit.test.tsx` and update the README if needed.
8. Commit and push: `git add TaskEdit.test.tsx README.md && git commit -m "test: add immediate save test"` and `git push`.
9. Approve or Merge the PR:
   ```bash
   PR_AUTHOR=$(gh pr view 13 --json author -q .author.login)
   CURRENT_USER=$(gh api user -q .login)

   REVIEW_BODY=$(cat <<'EOF'
   Reviewed and verified:
   - All acceptance criteria met
   - Added missing immediate-save test
   - Documentation updated
   - Tests passing
   EOF
   )

   if [ "$PR_AUTHOR" = "$CURRENT_USER" ]; then
     gh pr review 13 --comment --body "$REVIEW_BODY"
     gh pr merge 13 --squash --delete-branch
   else
     gh pr review 13 --approve --body "$REVIEW_BODY"
   fi
   ```
