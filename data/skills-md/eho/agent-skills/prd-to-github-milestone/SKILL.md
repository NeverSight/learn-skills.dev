---
name: prd-to-github-milestone
description: Parses a Product Requirements Document (PRD) to extract User Stories and creates corresponding GitHub Issues. It can optionally link them to a GitHub Milestone. This skill acts as a setup phase for GitHub-native issue tracking. Make sure to use this skill whenever the user asks to "send the PRD to GitHub", "create issues from the PRD", "setup the milestone", or mentions turning requirements into actionable GitHub issues.
metadata:
  author: eho
  version: '1.0.0'
---

# Instructions

You are acting as an autonomous sub-agent to parse a Product Requirements Document (PRD) and scaffold a GitHub milestone by creating GitHub Issues for each user story.

**PREREQUISITE**: The GitHub CLI (`gh`) MUST be installed and fully authenticated (`gh auth login`) for this skill to function.

## Workflow

1. **Setup Labels**: Before creating any issues, verify the `user-story` label exists and that a label for the specific feature prefix (e.g., `PRI`) exists. Run `gh label list --limit 1000 | grep "user-story"`. If not found, create it: `gh label create "user-story" --color "0e8a16" --description "User story task"`. Repeat this check and creation process for the PRD's specific prefix if applicable: `gh label create "<prefix>" --color "1d76db"`.
2. **Parse PRD**: Read the specified PRD file (e.g., `docs/PRD.md` or `tasks/prd-[feature].md`). Extract all User Stories and their complete details, including Titles, Descriptions, Acceptance Criteria, Technical Notes, Data Models, dependencies, the feature prefix representing this PRD, and any other relevant context.
3. **Identify Dependencies**: If the PRD outlines dependencies between user stories, note them. You will add these as comments or task lists in the issues.
4. **Idempotency Check**: Before creating an issue, check if an issue already exists for a given user story using `gh issue list --search "in:title <User Story Title>"`. This prevents creating duplicate issues if the skill is run multiple times.
5. **Create Issues**: Loop through the extracted stories. For each uncreated story, construct a GitHub blob URL to the PRD file. Get the repo info with `gh repo view --json nameWithOwner -q` (format: `owner/repo`), then format the issue body:
   ```
   ## Description
   <User Story Description>

   ## Acceptance Criteria
   - [ ] <Criterion 1>
   - [ ] <Criterion 2>
   ...

   ## Technical Notes
   <Any technical details>

   ## Original PRD
   [View in PRD](https://github.com/<owner>/<repo>/blob/main/<prd-file-path>)
   ```
   Example: `https://github.com/eho/test-example/blob/main/tasks/prd-example.md`

   Run `gh issue create --title "<Story ID>: <Title>" --body "<Formatted Body>" --label "user-story,<prefix>"` and capture the issue number. Since the command outputs a URL (e.g., `https://github.com/owner/repo/issues/42`), extract the issue number:
   ```bash
   ISSUE_URL=$(gh issue create --title "..." --body "..." --label "user-story,<prefix>")
   ISSUE_NUMBER=$(echo $ISSUE_URL | grep -oE '[0-9]+$')
   # Now $ISSUE_NUMBER contains "42" for use in dependency linking
   ```
   If there are dependencies noted from Step 3, add them to the issue body as a "Dependencies" section, or add a comment later once all issues are created.
6. **Link Dependencies**: After creating all issues, if there are dependencies between user stories, add comments to dependent issues listing their blockers. Use the captured issue numbers from Step 5:
   ```bash
   gh issue comment <dependent-issue-number> --body "Depends on: #<blocker-issue-number>"
   ```
   For example: `gh issue comment 43 --body "Depends on: #42"`
7. **Create & Link to Milestone**:
   - Determine the milestone name: Check if the PRD explicitly organizes stories by milestone. If yes, use that name. Otherwise, use the PRD feature name.
   - Create the milestone first (ensures it exists): `gh api repos/$(gh repo view --json nameWithOwner -q) milestones -f title="<Milestone Title>"`.
   - Link all created issues to the milestone: `gh issue edit <issue-number> --milestone "<Milestone Title>"`.
8. **Output Mapping**: Generate a markdown table and present to user:
   ```
   | Story ID | Title | Issue # | URL |
   |----------|-------|---------|-----|
   | PRI-001 | User Login | #12 | https://github.com/.../issues/12 |
   | PRI-002 | User Logout | #13 | https://github.com/.../issues/13 |
   ```

## Examples

**Example 1:**
*Input:* "Create issues from tasks/prd-login.md and add them to the 'v1.0' milestone"
*Action:*
1. Setup labels: `gh label list --limit 1000 | grep "user-story"`. If not found, run `gh label create "user-story" --color "0e8a16"`. Extract the prefix (`PRI` from `tasks/prd-login.md`), then check and create it: `gh label create "PRI" --color "1d76db"`.
2. Read `tasks/prd-login.md`.
3. Extract PRI-001 (Login), PRI-002 (Logout) with dependencies: PRI-002 depends on PRI-001.
4. Get repo info: `gh repo view --json nameWithOwner -q` → returns `myorg/myapp`.
5. Create issue for PRI-001:
   ```bash
   ISSUE_URL=$(gh issue create --title "PRI-001: User Login" \
     --body "## Description
   User should be able to log in...

   ## Acceptance Criteria
   - [ ] Form validates email
   - [ ] Form validates password

   ## Original PRD
   [View in PRD](https://github.com/myorg/myapp/blob/main/tasks/prd-login.md)" \
     --label "user-story,PRI")
   # Output: https://github.com/myorg/myapp/issues/42
   ISSUE_NUMBER=$(echo $ISSUE_URL | grep -oE '[0-9]+$')  # Extract "42"
   ```
6. Create issue for PRI-002 (with dependency noted):
   ```bash
   ISSUE_URL=$(gh issue create --title "PRI-002: User Logout" \
     --body "## Description
   User should be able to log out...

   ## Dependencies
   - Depends on #42 (User Login)

   ## Original PRD
   [View in PRD](https://github.com/myorg/myapp/blob/main/tasks/prd-login.md)" \
     --label "user-story,PRI")
   ```
7. Create milestone `v1.0` and link both issues.
8. Output summary:
   ```
   | Story ID | Title | Issue # | URL |
   |----------|-------|---------|-----|
   | PRI-001 | User Login | #42 | https://github.com/myorg/myapp/issues/42 |
   | PRI-002 | User Logout | #43 | https://github.com/myorg/myapp/issues/43 |
   ```