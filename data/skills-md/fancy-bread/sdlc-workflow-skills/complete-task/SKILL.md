---
name: complete-task
description: Complete Task
disable-model-invocation: true
---

# Complete Task

## Overview
Commit changes, push to remote, create pull request, and transition issue to "Code Review" status.

## Definitions

- **{TASK_KEY}**: Story/Issue ID from the issue tracker (e.g., `FB-6`, `PROJ-123`, `KAN-42`)
- **Branch Name Format**: Use short format `{type}/{TASK_KEY}` (e.g., `feat/FB-6`, `fix/PROJ-123`)
  - Short format is recommended: `feat/FB-6` (not `feat/FB-6-file-watching-workspace-commands`)
  - **Important**: Be consistent within a project - use the same format for all branches
- **Spec Summary**: Content from spec file located at `specs/{FEATURE_DOMAIN}/spec.md`
  - Contains Blueprint (Context, Architecture, Anti-Patterns) and Contract (DoD, Guardrails, Scenarios)
  - Used in PR body to document feature contracts
- **Plan Summary**: Content from plan file located at `.plans/{TASK_KEY}-*.plan.md`
  - **Plan File Selection**: If multiple files match the pattern `.plans/{TASK_KEY}-*.plan.md`:
    - Use the most recently modified file (check file modification time)
    - If modification time cannot be determined, use the first file found alphabetically
    - Report which file was selected: "Using plan file: {filename}"
  - Contains implementation details, requirements, and acceptance criteria
- **Completed Checklist**: Markdown checklist posted as a comment to the issue showing what work was completed
- **Current Branch**: Should match the expected format `{type}/{TASK_KEY}` (e.g., `feat/FB-6`, `fix/PROJ-123`)

## Prerequisites

Before proceeding, verify:

1. **MCP Status Validation**: Perform MCP server status checks (see `mcp-status.md` for detailed steps)
   - Test each configured MCP server connection (Atlassian, GitHub, etc.)
   - Verify all required integrations are authorized and operational
   - **If any MCP server fails validation, STOP and report the failure. Do not proceed.**
   - **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.

2. **Branch Verification**:
   - Verify current branch matches expected format: `{type}/{TASK_KEY}`
   - Confirm branch exists on remote (if not, this will be created on push)
   - **If branch doesn't match expected format, STOP and report the mismatch.**

3. **Test Verification**:
   - Run all tests locally and verify they pass
   - **If any tests fail, STOP and fix them before proceeding. Do not commit failing tests.**

4. **Documentation Files**:
   - Check if spec exists at `specs/{FEATURE_DOMAIN}/spec.md`
   - Check if plan exists at `.plans/{TASK_KEY}-*.plan.md`
   - **Plan File Selection**: If multiple files match the pattern `.plans/{TASK_KEY}-*.plan.md`:
     - Use the most recently modified file (check file modification time)
     - If modification time cannot be determined, use the first file found alphabetically
     - Report which file was selected: "Using plan file: {filename}"
   - **If neither spec nor plan exists, WARN but proceed**: PR will not include detailed context
   
5. **Verify Spec Updated (if applicable)**:
   - If code changes affected API contracts, data models, or quality targets:
     - **Check if spec was updated** in the staged changes
     - If spec exists but wasn't updated: WARN user about Same-Commit Rule violation
     - **Strongly recommend** including spec update in this commit

## Steps

1. **Prepare commit**
   - Check for linting errors and fix them
     - **If linting errors cannot be fixed automatically, STOP and report the issue. Ask user for guidance.**
   - Run all tests locally to ensure they pass
     - **If tests fail, STOP and fix them before committing.**
   - Stage all changes
   - Create conventional commit message
     - Format: `{type}: {description} ({TASK_KEY})`
     - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
     - Description should be clear and concise
     - Example: `feat: add user authentication (PROJ-123)`

2. **Run Constitutional Review Gate**
   - **Check if AGENTS.md exists:**
     - Use `glob_file_search` or `read_file` to check for `AGENTS.md` in repo root
     - If AGENTS.md exists:
       - Read `AGENTS.md` Operational Boundaries (Tier 1: ALWAYS, Tier 2: ASK, Tier 3: NEVER)
       - Proceed with full Constitutional Review
     - If AGENTS.md does NOT exist:
       - Log: "⚠️ AGENTS.md not found - Constitutional Review skipped"
       - Store status: "Constitutional Review: SKIPPED (AGENTS.md not found)"
       - Proceed to next step (commit and push) without Constitutional Review
   - **If AGENTS.md exists, continue with review:**
     - If spec exists, read `specs/{FEATURE_DOMAIN}/spec.md` for functional context
   - **Get code diff:**
     - Use `run_terminal_cmd`: `git diff main...HEAD` to get all changes in PR
     - Include file paths, additions, deletions
   - **Invoke Critic Agent using Cursor's built-in review:**
     - **Use Cursor's native review capabilities** (no external API keys required)
     - The agent executing `/complete-task` acts as the Critic Agent, using Cursor's built-in review features
     - **No external dependencies:** All review happens within Cursor IDE using native capabilities
     - Prompt structure for the review:
       ```
       You are a Critic Agent performing Constitutional Review.

       **Constitution** (from AGENTS.md Operational Boundaries, if AGENTS.md exists):
       [If AGENTS.md exists: Paste full text of Tier 1 (ALWAYS), Tier 2 (ASK), Tier 3 (NEVER) sections]
       [If AGENTS.md does not exist: Note "AGENTS.md not found - Constitutional Review skipped. Proceeding with commit/PR without Constitutional Review."]

       **Spec** (functional context):
       [If spec exists: Paste Blueprint and Contract sections]
       [If no spec: Note "No spec found - validate against Constitution only"]

       **Code Changes** (git diff main...HEAD):
       [Paste full diff output]

       **Task**: Validate code against Constitution. For each violation found:
       1. **Category**: CRITICAL (Tier 3 NEVER) | WARNING (Tier 2 ASK) | INFO (Tier 1 ALWAYS)
       2. **Description**: What constitutional principle was violated?
       3. **Impact**: Why this matters (performance, security, maintainability, scalability)
       4. **Remediation**: Ordered steps to fix the violation
       5. **Location**: File:Line reference where violation occurs

       Output structured markdown report using this format:

       ## Constitutional Review

       **Status**: PASSED | FAILED | WARNING

       ### Tier 3 Violations (CRITICAL - NEVER)
       [List each violation OR state "None"]

       ### Tier 2 Violations (WARNING - ASK)
       [List each violation OR state "None"]

       ### Tier 1 Violations (INFO - ALWAYS)
       [List each violation OR state "None"]

       ### Summary
       - Total violations: X
       - Critical: Y (Tier 3)
       - Warnings: Z (Tier 2)
       - Info: W (Tier 1)
       ```
   - **Parse Critic output:**
     - Extract violations by severity (CRITICAL, WARNING, INFO)
     - Count violations in each tier
     - Store full report for PR body
   - **Gate Decision (only if AGENTS.md exists and review was performed):**
     - **If CRITICAL violations found (Tier 3: NEVER):**
       - STOP immediately
       - Display full violation report with remediation steps
       - Report: "❌ Constitutional Review FAILED. PR creation blocked due to Tier 3 violations."
       - Instruct user: "Fix violations listed above and retry `/complete-task`"
       - Do NOT proceed to commit/push/PR steps
     - **If only WARNING/INFO violations (Tier 2, Tier 1):**
       - Log: "⚠️ Constitutional Review passed with warnings/suggestions."
       - Store report for inclusion in PR body
       - Proceed to next step (commit and push)
     - **If no violations:**
       - Log: "✅ Constitutional Review: PASSED"
       - Store "PASSED" status for PR body
       - Proceed to next step
   - **If AGENTS.md does not exist:**
     - Skip Constitutional Review
     - Log: "⚠️ AGENTS.md not found - Constitutional Review skipped"
     - Store "SKIPPED" status for PR body
     - Proceed directly to commit and push (no review gate)

3. **Commit and push changes**
   - Commit staged changes with the conventional commit message
   - Push to remote branch
     - **If push fails (e.g., authentication, network, conflicts), STOP and report the error.**
     - **If branch doesn't exist on remote, it will be created on first push.**

4. **Create pull request (optional)**
   - **Note**: PR creation is optional. You may skip this step if you prefer to create the PR manually or if it's not needed.
   - **If creating PR:** CI/CD is a PR gate. Local tests passing is the prerequisite to PR creation. CI/CD will run automatically after PR is created.
   - **If skipping PR:** Proceed directly to Step 6 (Update issue) after pushing.

5. **Create pull request (if proceeding with PR creation)**
   - **After pushing, get the latest commit SHA:**
     - Use `run_terminal_cmd`: `git rev-parse HEAD` to get current commit SHA
     - Or use `mcp_github_list_commits` with `sha` = branch name to get latest commit
   - **Read documentation for PR body:**
     - **First, check for Spec** at `specs/{FEATURE_DOMAIN}/spec.md`:
       - If exists, extract: Context (from Blueprint), Definition of Done (from Contract), key scenarios
       - Include in PR body as "Feature Spec" section
     - **Then, check for Plan** at `.plans/{TASK_KEY}-*.plan.md`:
       - If exists, extract: Story, Context, Scope, Acceptance Criteria, Implementation Steps summary
       - Include in PR body as "Implementation Plan" section
     - **If neither exists**: Note in PR body that no detailed documentation was found
   - **Check if PR already exists:**
     - Use `mcp_github_get_pull_request` with `method="get"` to check for existing PRs
     - If PR exists, update it instead of creating new one
   - Create completed checklist comment for the issue (include PR link if PR was created):
     ```
     ## Completed Checklist

     - [x] Plan reviewed and implemented
     - [x] Code changes completed
     - [x] Unit tests written and passing
     - [x] Constitutional Review passed
     - [x] Spec updated (if behavior changed)
     - [x] Documentation updated
     - [x] Linting errors fixed
     - [x] All tests passing locally
     - [x] Changes committed and pushed
     - [x] PR created (if applicable)

     Pull Request: {PR_URL} (only if PR was created)
     ```
   - Create PR with:
     - Title: `{type}: {description} ({TASK_KEY})` (matching commit message)
     - Body should include:
       - **Constitutional Review report** (from Step 2):
         - If PASSED: Include "✅ Constitutional Review: PASSED"
         - If WARNING/INFO: Include full Constitutional Review report with violations
         - If SKIPPED: Include "⚠️ Constitutional Review: SKIPPED (AGENTS.md not found)"
         - Constitutional Review report should appear first in PR body
       - Feature Spec summary (if spec exists) with Blueprint context and Contract DoD
       - Implementation Plan summary (if plan exists) with extracted sections
       - Note: "CI/CD checks will run automatically on this PR"
       - Link to the issue
     - PR body template:
       ```markdown
       ## Summary
       [Brief description of changes]

       ## Constitutional Review
       [Insert Constitutional Review report from Step 2]
       - If PASSED: "✅ Constitutional Review: PASSED - No violations found"
       - If WARNING/INFO: Full report with Tier 2 and Tier 1 violations
       - If SKIPPED: "⚠️ Constitutional Review: SKIPPED (AGENTS.md not found) - Proceeded without Constitutional Review"

       ## Feature Spec
       [If spec exists, include Context and Definition of Done]

       ## Implementation Plan
       [If plan exists, include key implementation steps]

       ## Verification
       - ✅ Tests: All passing locally
       - ✅ Linting: No errors
       - ✅ Constitutional Review: [PASSED | WARNING]

       ## Related Issue
       Closes {TASK_KEY}
       ```
     - Set base branch (typically `main` or `develop`)
     - **Common failure scenarios:**
       - Branch doesn't exist on remote: Ensure branch was pushed successfully
       - PR already exists: Check using `mcp_github_get_pull_request` before creating
       - Permission errors: Verify GitHub MCP authentication
       - Invalid base branch: Verify base branch exists
     - **If PR creation fails, STOP and report the specific error with context.**
   - Link PR to the issue (using issue tracker's linking mechanism)
   - **After PR creation, monitor CI/CD status:**
     - Use `mcp_github_get_pull_request` with `method="get_status"` to check CI/CD status
     - CI/CD will run automatically as a gate on the PR
     - Note status in PR body or comments as needed

6. **Update issue**
   - **If PR was created:**
     - Add PR link as a comment to the issue
       - Format: `Pull Request: {PR_URL}`
   - **If PR was not created:**
     - Add comment indicating changes are committed and pushed, ready for review
       - Format: `Changes committed and pushed to branch {type}/{TASK_KEY}. Ready for review.`
   - **Transition issue to "Code Review" status:**
     - First, get available transitions using `mcp_atlassian_getTransitionsForJiraIssue`
     - Find transition to "Code Review" status
     - Transition using `mcp_atlassian_transitionJiraIssue`
     - Verify issue status is now "Code Review"
     - **If transition fails (permissions, workflow rules), STOP and report the error.**

## Tools

### MCP Tools (Atlassian)
- `mcp_atlassian_atlassianUserInfo` - Verify Atlassian MCP connection
- **Obtaining CloudId for Atlassian Tools:**
  - **Method 1 (Recommended)**: Use `mcp_atlassian_getAccessibleAtlassianResources`
    - Returns list of accessible resources with `cloudId` values
    - Use the first result or match by site name
    - Only call if cloudId is not already known or has expired
  - **Method 2**: Extract from Atlassian URLs
    - Jira URL format: `https://{site}.atlassian.net/...`
    - CloudId can be extracted from the URL or obtained via API
  - **Error Handling**: If cloudId cannot be determined, STOP and report: "Unable to determine Atlassian cloudId. Please verify MCP configuration."
- `mcp_atlassian_getJiraIssue` - Fetch story details by {TASK_KEY}
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
- `mcp_atlassian_getTransitionsForJiraIssue` - Get available status transitions
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
- `mcp_atlassian_transitionJiraIssue` - Transition issue to "Code Review" status
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `transition` = {id: "transition-id"}
- `mcp_atlassian_addCommentToJiraIssue` - Add completed checklist and PR link comments
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown content

### MCP Tools (GitHub)
- A lightweight read-only GitHub MCP tool to verify connection (see Cursor Settings → Tools & MCP for exact names)
- `mcp_github_list_branches` - List branches (verify current branch exists)
  - Parameters: `owner`, `repo`
- `mcp_github_list_commits` - Get latest commit SHA from branch
  - Parameters: `owner`, `repo`, `sha` = branch name
- `mcp_github_get_commit` - Get commit details
  - Parameters: `owner`, `repo`, `sha` = commit SHA, `include_diff` = false
- `mcp_github_get_pull_request` - Get PR details (check if PR already exists)
  - Parameters: `owner`, `repo`, `pullNumber`, `method` = "get"
- `mcp_github_create_pull_request` - Create new pull request
  - Parameters: `owner`, `repo`, `title`, `head` = `{type}/{TASK_KEY}`, `base` = `main` (or default), `body` = PR description
- `mcp_github_get_pull_request` - Get PR status and CI/CD checks
  - Parameters: `owner`, `repo`, `pullNumber`, `method` = "get_status"

### Filesystem Tools
- `glob_file_search` - Find specs matching `specs/{FEATURE_DOMAIN}/spec.md` or plans matching `.plans/{TASK_KEY}-*.plan.md`
  - Pattern for plans: `**/.plans/{TASK_KEY}-*.plan.md`
  - Pattern for specs: `**/specs/*/spec.md`
- `read_file` - Read spec/plan file content for PR body
  - Spec location: `specs/{FEATURE_DOMAIN}/spec.md`
  - Plan location: `.plans/{TASK_KEY}-{description}.plan.md`
- `read_lints` - Check for linting errors
  - Parameters: `paths` = array of file paths or directories

### Terminal Tools
- `run_terminal_cmd` - Execute git and test commands
  - `git status` - Check current branch and uncommitted changes
  - `git branch --show-current` - Get current branch name
  - `git rev-parse HEAD` - Get current commit SHA
  - `git diff main...HEAD` - Get code changes for Constitutional Review
  - `git add .` or `git add <files>` - Stage changes
  - `git commit -m "{type}: {description} ({TASK_KEY})"` - Commit with conventional format
  - `git push origin {type}/{TASK_KEY}` - Push branch to remote
  - `npm test` or `pytest` or project-specific test command - Run tests locally
  - `npm run lint` or project-specific lint command - Check linting

## Completion Checklist
- [ ] MCP status validation performed
- [ ] Current branch verified (matches `{type}/{TASK_KEY}` format)
- [ ] All tests passing locally
- [ ] Documentation files checked (spec and/or plan)
- [ ] Spec updated if behavior changed (Same-Commit Rule)
- [ ] Linting errors fixed
- [ ] Changes staged
- [ ] Commit message follows convention
- [ ] Changes committed
- [ ] Constitutional Review Gate executed
- [ ] Constitutional Review passed (or warnings only)
- [ ] Pushed to remote
- [ ] PR created (optional - may be skipped)
- [ ] If PR created: CI/CD checks running (as PR gate)
- [ ] Completed checklist added to issue
- [ ] If PR created: PR created with spec/plan/review summary
- [ ] If PR created: PR linked to issue
- [ ] If PR created: PR link added to issue comment
- [ ] Issue updated with status (PR link or commit/push confirmation)
- [ ] Issue transitioned to "Code Review"

## Guidance

### Role
Act as a **software engineer** responsible for completing development work on a task and preparing it for code review. You are methodical, thorough, and follow established development workflows and standards.

### Instruction
Execute the complete-task workflow to finalize development work on a specified task. This includes:
1. Performing prerequisite validation checks
2. Preparing and committing changes following conventions
3. Pushing changes to remote
4. Optionally creating a pull request with proper documentation (may be skipped)
5. Updating the issue tracker with completion status

### Context
- The task is tracked in an issue management system (Jira, Azure DevOps, etc.)
- **Specs** may exist at `specs/{FEATURE_DOMAIN}/spec.md` with permanent feature contracts
- **Plans** may exist at `.plans/{TASK_KEY}-*.plan.md` with transient implementation details
- **AGENTS.md** defines 3-tier Operational Boundaries (Constitution)
- **Constitutional Review** validates code against Constitution before PR creation using Cursor's built-in review capabilities (no external API keys required)
- Implements ASDLC Review Gate between Quality Gates and Acceptance Gates
- Development work has been completed on a branch following the `{type}/{TASK_KEY}` format
- MCP integrations provide access to issue trackers and version control
- Automated CI/CD pipelines run checks on pushed branches
- The codebase follows conventional commit standards and branch naming conventions
- **Same-Commit Rule**: Spec updates must be committed with code changes that affect behavior/contracts
- **ASDLC patterns**: [Constitutional Review](asdlc://constitutional-review), [The Spec](asdlc://the-spec), [The PBI](asdlc://the-pbi), [Context Gates](asdlc://context-gates)
- **ASDLC pillars**: **Quality Control** (Review Gate), **Standardized Parts** (Constitution)

### Examples

**ASDLC**: [Constitutional Review](asdlc://constitutional-review) — Validates changes against AGENTS.md before PR creation.

**Example Branch Names:**
- `feat/PROJ-123` (story/feature)
- `fix/FB-6` (bug fix)
- `chore/KAN-42` (maintenance task)
- `refactor/PROJ-321` (refactoring)

**Example Commit Messages:**
- `feat: add user authentication (PROJ-123)`
- `fix: resolve login timeout error (FB-6)`
- `refactor: simplify auth service (PROJ-321)`
- `test: add unit tests for auth module (PROJ-123)`
- `docs: update API documentation (PROJ-123)`

**Example PR Title:**
- `feat: add user authentication (PROJ-123)`

**Example PR Body:**
```markdown
## Summary
Implements user authentication feature as specified in PROJ-123.

## Constitutional Review
✅ **Constitutional Review: PASSED** - No violations found

All code changes comply with AGENTS.md Operational Boundaries:
- Tier 1 (ALWAYS): Command structure standards followed
- Tier 2 (ASK): No high-risk operations without approval
- Tier 3 (NEVER): No security violations or anti-patterns detected

## Feature Spec
[If spec exists at specs/user-authentication/spec.md]

### Context
User authentication is required to secure access to the application. OAuth2 provides a standard, secure authentication method.

### Definition of Done
- [ ] User can log in using OAuth2
- [ ] Session persists for 24 hours
- [ ] Failed attempts are logged
- [ ] Tests pass and coverage maintained

### Key Scenarios
- **Given** user has valid OAuth2 credentials
- **When** user attempts login
- **Then** session is created and user is authenticated

## Implementation Plan
[If plan exists at .plans/PROJ-123-*.plan.md]

### Implementation Steps
1. Set up OAuth2 library and configuration
2. Implement AuthService for OAuth2 flow
3. Create SessionManager for session handling
4. Add AuthMiddleware for request validation
5. Create login/logout API endpoints

## Verification Status
- ✅ Build: Passing
- ✅ Tests: All passing (95% coverage)
- ✅ Linting: No errors
- ✅ Constitutional Review: PASSED
- ⏳ Security scan: Pending

## Related Issue
Closes PROJ-123
```

**Example Completed Checklist Comment (with PR):**
```
## Completed Checklist

- [x] Plan reviewed and implemented
- [x] Code changes completed
- [x] Unit tests written and passing
- [x] Constitutional Review passed
- [x] Spec updated (if behavior changed)
- [x] Documentation updated
- [x] Linting errors fixed
- [x] All tests passing locally
- [x] Changes committed and pushed
- [x] PR created
- [x] Automated checks passing

Pull Request: https://github.com/owner/repo/pull/42
```

**Example Completed Checklist Comment (without PR):**
```
## Completed Checklist

- [x] Plan reviewed and implemented
- [x] Code changes completed
- [x] Unit tests written and passing
- [x] Documentation updated
- [x] Linting errors fixed
- [x] All tests passing locally
- [x] Changes committed and pushed to branch feat/FB-6

Ready for review.
```

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data. Never commit changes automatically without user review.
   - **AGENTS.md Optional**: If AGENTS.md exists, Constitutional Review is performed. If missing, review is skipped and command proceeds.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Same-Commit Rule**: If code changes API contracts, data models, or quality targets → update spec in same commit:
   - Verify spec was updated in staged changes
   - If spec exists but wasn't updated: WARN user and recommend including spec update
   - Spec and code changes must be committed together
3. **Constitutional Review Gate**: Before PR creation, validate code against AGENTS.md:
   - Use Cursor's built-in review capabilities (no external API keys required)
   - Run Critic Agent validation against 3-tier Operational Boundaries (Tier 1: ALWAYS, Tier 2: ASK, Tier 3: NEVER)
   - BLOCK PR creation on Tier 3 (NEVER) violations - display violations and STOP
   - WARN on Tier 2 (ASK) and Tier 1 (ALWAYS) violations but allow PR creation
   - Include Constitutional Review report in PR body
   - If CRITICAL violations found, instruct user on remediation before retrying
4. **Prerequisites Must Pass**: Do not proceed if MCP validation, branch verification, or test verification fails. STOP and report the issue.
5. **Conventional Commits**: All commits must follow the format: `{type}: {description} ({TASK_KEY})`
   - Valid types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
   - Description should be clear and concise
   - Task key must be included in parentheses
6. **Branch Naming**: Current branch must match short format `{type}/{TASK_KEY}` (e.g., `feat/FB-6`, `fix/PROJ-123`)
   - Use short format: `feat/FB-6` (not descriptive format)
   - **Important**: Be consistent - use short format for all branches
7. **Test Requirements**: All tests must pass locally before committing. Do not commit failing tests.
8. **Linting**: All linting errors must be fixed before committing. If errors cannot be fixed automatically, STOP and ask for guidance.
9. **PR Creation is Optional**: PR creation is optional. You may skip PR creation if you prefer to create it manually or if it's not needed. If creating PR:
   - CI/CD runs automatically after PR creation as a gate. Local tests passing is the prerequisite to PR creation. Monitor CI/CD status after PR is created.
   - PR body should include:
     - Constitutional Review report (from Step 2)
     - Feature Spec summary (if spec exists at `specs/{FEATURE_DOMAIN}/spec.md`)
     - Implementation Plan summary (if plan exists at `.plans/{TASK_KEY}-*.plan.md`)
     - If neither spec nor plan exists, note this in PR body
10. **Documentation File Handling**:
   - Check for both spec and plan files
   - If neither exists, WARN but proceed (PR will lack detailed context)
   - Prefer spec content over plan content when both exist
11. **Error Handling**: If any step fails (push, PR creation, issue transition), STOP and report the specific error. Do not proceed with remaining steps.

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- Spec guidance: See `specs/README.md` for Same-Commit Rule and when to update specs
- Constitutional Review: See AGENTS.md Operational Boundaries for 3-tier system
- Branch naming: Type prefix format (`{type}/{TASK_KEY}`) as established in `start-task.md`
- Commit message format: `{type}: {description} ({TASK_KEY})` (consistent across commands)
- Documentation locations: Specs at `specs/{FEATURE_DOMAIN}/spec.md`, Plans at `.plans/{TASK_KEY}-*.plan.md`
- Issue workflow: Tasks transition through "To Do" → "In Progress" → "Code Review" → "Done"
- ASDLC patterns: The Spec (permanent state), The PBI (transient delta), Living Specs (Same-Commit Rule), Constitutional Review (Review Gate), Context Gates (gate system)

### Output
1. **Committed Changes**: All changes committed with conventional commit format (including spec updates if behavior changed)
2. **Constitutional Review Report**: Validation report showing PASSED, WARNING, or FAILED status with violations
3. **Pushed Branch**: Branch pushed to remote repository (if Constitutional Review passed or warnings only)
4. **Pull Request (optional)**: If PR creation was chosen and Constitutional Review passed, PR created with Constitutional Review report, spec summary (if exists), plan summary (if exists), verification status, and issue link. CI/CD checks will run automatically.
5. **Updated Issue**: Issue updated with completed checklist, status information (PR link if created, or commit/push confirmation if PR skipped), and transitioned to "Code Review" status

All outputs should be verified and any failures should be reported immediately with specific error details. CRITICAL Constitutional Review violations block PR creation.
