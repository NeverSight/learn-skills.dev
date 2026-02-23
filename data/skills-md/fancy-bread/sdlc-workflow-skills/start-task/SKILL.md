---
name: start-task
description: Start Task
disable-model-invocation: true
---

# Start Task

## Overview
Begin development on a task with proper setup and pre-flight checks.

## Definitions

- **{TASK_KEY}**: Story/Issue ID from the issue tracker (e.g., `FB-6`, `PROJ-123`, `KAN-42`)
- **Branch Name Format**: Use short format `{type}/{TASK_KEY}` (e.g., `feat/FB-6`, `fix/PROJ-123`)
  - Short format is recommended: `feat/FB-6` (not `feat/FB-6-file-watching-workspace-commands`)
  - **Important**: Be consistent within a project - use the same format for all branches

## Prerequisites

Before proceeding, verify (see Steps 1–2 for how):

1. **MCP Status Validation**: All required MCP servers connected and authorized. If any fail, STOP.
   - **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.
2. **Spec or Plan exists**: At least one of `specs/{FEATURE_DOMAIN}/spec.md` or `.plans/{TASK_KEY}-*.plan.md`. If neither, STOP and suggest `/create-plan {TASK_KEY}`.
3. **Story in In Progress** (or can be transitioned) and **assigned to current user**.

## Steps
1. **Pre-flight checks**
   - **MCP Status Validation**: Perform MCP server status checks (see `mcp-status.md` for detailed steps)
     - Test each configured MCP server connection
     - Verify all required integrations are authorized and operational
     - **If any MCP server fails validation, STOP and report the failure. Do not proceed.**
   - **Read relevant documents:**
     - **First, check for Spec**: Look for related spec in `specs/{FEATURE_DOMAIN}/spec.md`
       - If feature spec exists, read Blueprint for architectural constraints and Anti-Patterns
       - Read Contract for Definition of Done and Regression Guardrails
       - Specs provide permanent context for how the feature works
     - **Then, read Plan** (if exists): Look for task plan at `.plans/{TASK_KEY}-*.plan.md`
       - **Plan File Selection**: If multiple files match the pattern `.plans/{TASK_KEY}-*.plan.md`:
         - Use the most recently modified file (check file modification time)
         - If modification time cannot be determined, use the first file found alphabetically
         - Report which file was selected: "Using plan file: {filename}"
       - Plans provide transient task-level implementation steps
       - **If no plan and no spec exist, STOP and report error**: "No plan or spec found for {TASK_KEY}. Run `/create-plan {TASK_KEY}` first."
   - Verify story is in "In Progress"
     - Fetch story status using `mcp_atlassian_getJiraIssue`
     - **If status is NOT "In Progress":**
       1. Get available transitions using `mcp_atlassian_getTransitionsForJiraIssue`
       2. Find transition to "In Progress" status
       3. Transition using `mcp_atlassian_transitionJiraIssue`
       4. Verify transition succeeded
     - **If transition fails or "In Progress" status not available:**
       - STOP and report: "Story {TASK_KEY} cannot be moved to 'In Progress'. Current status: {status}. Available transitions: {list}"
   - Confirm story is assigned to current user

2. **Set up development environment**
   - Determine branch type prefix based on task type:
     - Story → `feat/{TASK_KEY}`
     - Bug → `fix/{TASK_KEY}`
     - Task/Chore → `chore/{TASK_KEY}`
     - Refactor → `refactor/{TASK_KEY}`
     - Default to `feat/{TASK_KEY}` if task type is unclear
   - **First, check if branch already exists:**
     - Use `mcp_github_list_branches` to list existing branches
     - Or use `run_terminal_cmd`: `git branch -a | grep {type}/{TASK_KEY}`
     - **If branch exists:**
       - Ask user: "Branch {type}/{TASK_KEY} already exists. Use existing branch or create new one?"
       - If "use existing": Checkout existing branch
       - If "create new": Use different name or delete old branch first
   - **If branch doesn't exist:**
     - Create locally: `git checkout -b {type}/{TASK_KEY}`
     - Or create on remote first: `mcp_github_create_branch` (if remote-first workflow)
   - **Add work checklist comment to issue (include the actual branch name created):**
     - **Timing**: Post immediately after branch creation, before starting implementation
     - This provides visibility that work has begun
     - Include the actual branch name created (e.g., `feat/FB-6`)

3. **Implement according to spec and plan**
   - **Read and understand documents:**
     - **Spec (if exists)**: Review Blueprint for design constraints, read Contract for acceptance criteria
     - **Plan (if exists)**: Review implementation steps, identify files to create/modify
     - Understand dependencies and order
   - **Analyze existing codebase:**
     - Use `codebase_search` to find related code
     - Review similar implementations for patterns
     - Understand existing test structure
   - **Implement changes:**
     - Create new files as specified
     - Modify existing files as needed
     - Follow existing code patterns and conventions
     - **Respect Anti-Patterns from Spec** (if spec exists)
   - **Write tests alongside code:**
     - Create test files for new code
     - Update existing tests for modified code
     - **Use Spec's Contract scenarios** for test cases (if spec exists)
     - Ensure tests follow existing test patterns
   - **Update Spec if behavior changes:**
     - If code changes API contracts, data models, or quality targets → update Spec
     - Spec updates must be committed in same commit as code changes (Same-Commit Rule)
     - See `specs/README.md` for when to update specs
   - **Leave changes uncommitted for review:**
     - Do NOT commit changes automatically
     - Changes remain in working directory for developer review and testing
     - Developer can review, test, and commit changes manually or use `/complete-task` to commit and push

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
- `mcp_atlassian_transitionJiraIssue` - Transition issue to "In Progress" (if needed)
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `transition` = {id: "transition-id"}
- `mcp_atlassian_addCommentToJiraIssue` - Add work checklist comment to issue
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown checklist

### MCP Tools (GitHub)
- A lightweight read-only GitHub MCP tool to verify connection (see Cursor Settings → Tools & MCP for exact names; e.g. a list/read tool)
- `mcp_github_list_branches` - List existing branches (check if branch already exists)
- `mcp_github_create_branch` - Create new branch on remote
  - Parameters: `owner`, `repo`, `branch` = `{type}/{TASK_KEY}`, `from_branch` = `main` (or default branch)

### Filesystem Tools
- `glob_file_search` - Find specs matching `specs/{FEATURE_DOMAIN}/spec.md` or plans matching `.plans/{TASK_KEY}-*.plan.md`
  - Pattern for plans: `**/.plans/{TASK_KEY}-*.plan.md`
  - Pattern for specs: `**/specs/*/spec.md`
- `read_file` - Read spec/plan files and existing code
  - Spec location: `specs/{FEATURE_DOMAIN}/spec.md`
  - Plan location: `.plans/{TASK_KEY}-{description}.plan.md`
- `write` - Create new files
- `search_replace` - Modify existing files (including specs when behavior changes)
- `list_dir` - Explore directory structure

### Codebase Tools
- `codebase_search` - Search for similar implementations, patterns, or related code
  - Query: "How is [similar feature] implemented?"
  - Query: "Where is [component] used?"
- `grep` - Find specific patterns, functions, or classes
  - Pattern: function names, class names, imports, etc.

### Terminal Tools
- `run_terminal_cmd` - Execute git commands
  - `git status` - Check current branch and status
  - `git checkout -b {type}/{TASK_KEY}` - Create and checkout new branch locally
  - `git branch` - List branches
  - Note: Committing changes is handled in `/complete-task`, not in this command

## Pre-flight Checklist
- [ ] MCP status validation performed (see `mcp-status.md`)
- [ ] All MCP servers connected and authorized
- [ ] Relevant docs checked (spec and/or plan)
- [ ] Spec read (if exists) - Blueprint and Contract sections
- [ ] Plan read (if exists) - implementation steps
- [ ] Story status is "In Progress"
- [ ] Story assigned to current user
- [ ] Feature branch created
- [ ] Branch checked out locally
- [ ] Work checklist posted to issue

## Implementation Checklist
- [ ] Requirements understood (from spec/plan)
- [ ] Spec Blueprint reviewed for architectural constraints (if exists)
- [ ] Spec Contract reviewed for acceptance criteria (if exists)
- [ ] Anti-Patterns from Spec identified (if exists)
- [ ] Codebase context reviewed
- [ ] Implementation in progress
- [ ] Code changes made
- [ ] Tests written (using Contract scenarios if spec exists)
- [ ] Spec updated if behavior changed (Same-Commit Rule)
- [ ] Documentation updated
- [ ] Changes ready for review and testing (uncommitted)

## Guidance

### Role
Act as a **software engineer** responsible for beginning development work on a task. You are methodical, thorough, and follow established development workflows and standards.

### Instruction
Execute the start-task workflow to begin development on a specified task. This includes:
1. Performing pre-flight validation checks
2. Setting up the development environment (branch creation, issue updates)
3. Implementing work according to the plan
4. Following all established conventions and standards

### Context
- The task is tracked in an issue management system (Jira, Azure DevOps, etc.)
- **Specs** may exist at `specs/{FEATURE_DOMAIN}/spec.md` with permanent feature contracts
- **Plans** may exist at `.plans/{TASK_KEY}-*.plan.md` with transient task-level implementation steps
- Specs define State (how feature works), Plans define Delta (what changes)
- The task should already be in "In Progress" status and assigned to the current user
- MCP integrations provide access to issue trackers and version control
- The codebase has existing patterns, conventions, and architectural decisions that should be respected
- **Same-Commit Rule**: If code changes behavior/contracts, update spec in same commit
- **ASDLC patterns**: [The Spec](asdlc://the-spec), [The PBI](asdlc://the-pbi), [Context Gates](asdlc://context-gates)
- **ASDLC pillars**: **Factory Architecture** (command station), **Quality Control** (pre-flight gates)

### Examples

**ASDLC**: [Context Gates](asdlc://context-gates) — MCP and plan checks act as input gates before implementation.

**Example Branch Names:**
- `feat/PROJ-123` (story/feature)
- `fix/PROJ-456` (bug fix)
- `chore/PROJ-789` (maintenance task)
- `refactor/PROJ-321` (refactoring)

**Note on Commits:** Changes are left uncommitted in this command. Use `/complete-task` to commit, push, and optionally create a PR when ready.

**Example Issue Comment (Work Checklist):**
```
## Work Checklist

- [ ] Plan reviewed
- [ ] Branch created: `feat/PROJ-123`
- [ ] Implementation in progress
- [ ] Code changes in progress
- [ ] Tests being written
- [ ] Documentation updated
```

Note: The branch name in the comment must match the actual branch name created (including the type prefix).

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data. Never commit changes automatically without user review.
   - **AGENTS.md Optional**: Commands work without AGENTS.md. Standards apply regardless of whether AGENTS.md exists.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Read Spec First** (if exists): Check for feature spec in `specs/` and read Blueprint + Contract before implementation
3. **Respect Anti-Patterns**: If spec exists, do NOT implement forbidden approaches listed in Anti-Patterns section
4. **Same-Commit Rule**: If code changes API contracts, data models, or quality targets → update spec in same commit
5. **Unit Tests Required**: All new code must have corresponding unit tests. Use Contract scenarios from spec (if exists) for test cases.
6. **No Automatic Commits**: Do NOT commit changes automatically. Leave changes uncommitted for developer review and testing. Committing is handled by `/complete-task`.
7. **Branch Naming**: Use short format: `{type}/{TASK_KEY}` (e.g., `feat/FB-6`, `fix/PROJ-123`)
   - Determine type prefix from task type:
     - Story → `feat/`
     - Bug → `fix/`
     - Task/Chore → `chore/`
     - Refactor → `refactor/`
     - Default to `feat/` if task type is unclear
   - Example: Story FB-6 → `feat/FB-6` (short format, not descriptive format)
   - **Important**: Be consistent - use short format for all branches
8. **Pre-flight Validation**: Do not proceed if:
   - **MCP status validation fails** (see `mcp-status.md` for validation steps - if any MCP server is not connected or authorized, STOP immediately)
   - Neither spec nor plan exists (STOP and suggest running `/create-plan {TASK_KEY}` first)
   - Story is not in "In Progress" status
   - Story is not assigned to current user
9. **Code Quality**:
   - Follow existing code patterns and conventions
   - Maintain or improve test coverage
10. **Documentation**: Update relevant documentation when adding features or changing behavior

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- Spec guidance: See `specs/README.md` for when to update specs and Same-Commit Rule
- Branch naming: Type prefix format (`{type}/{TASK_KEY}`) as shown in current workflow
- Test requirements: Tests written alongside code (per Implementation Checklist)
- Commit workflow: Changes are committed in `/complete-task`, not in this command
- Issue workflow: Tasks transition through "To Do" → "In Progress" → "Code Review" → "Done"
- ASDLC patterns: The Spec (permanent state), The PBI (transient delta)

### Output
1. **Development Work**: Implement the work specified in spec/plan:
   - Code changes implemented according to spec constraints and plan steps (left uncommitted for review)
   - Unit tests created or updated alongside code (using Contract scenarios if spec exists)
   - Spec updated if behavior/contracts changed (Same-Commit Rule)
   - Documentation updated as needed
   - Changes ready for developer review and testing
   - Use `/complete-task` when ready to commit, push, and optionally create a PR
