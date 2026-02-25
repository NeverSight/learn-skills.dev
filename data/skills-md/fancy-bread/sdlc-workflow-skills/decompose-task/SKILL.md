---
name: decompose-task
description: Decompose Task
disable-model-invocation: true
---

# Decompose Task

## Overview
Decompose a large task (epic or large story) into well-defined, actionable subtasks. This is a critical Scrum planning activity that ensures large work items are properly broken down into sprint-sized tasks.

## Definitions

- **{TASK_KEY}**: Task/Issue ID from the issue tracker (e.g., `FB-6`, `PROJ-123`, `KAN-42`)
- **{FEATURE_DOMAIN}**: Kebab-case feature name inherited from parent task (e.g., `user-authentication`, `payment-processing`). Used to link child PBIs to the same Spec as parent.
- **Task Decomposition**: The process of breaking down a large task into smaller, more manageable subtasks
- **Subtask**: A child task that represents a specific piece of work within a larger task or epic
- **Subtask Criteria**: Requirements that each generated subtask must meet:
  - Follows appropriate format (user story format for user-facing tasks, action-oriented for technical tasks)
  - Has clear acceptance criteria (3-5 criteria minimum)
  - Is appropriately sized (completable in 1-2 days typically, 1-2 sprint points)
  - Is independent and can be developed standalone (or clearly defined dependencies)
  - Delivers user or technical value
  - Is testable and verifiable
- **Task Types for Decomposition**:
  - **Epic**: High-level initiative that typically breaks down into multiple stories
  - **Story**: User story or feature that may break down into technical tasks
  - **Technical Task**: Large technical work item that may break down into smaller technical tasks
- **Information Density Scoring**: A method to assess task information completeness using 5 key elements:
  - Clear, specific goals (not vague)
  - Defined scope or boundaries
  - User context (personas, use cases) OR technical context
  - Success criteria or acceptance criteria
  - Constraints or dependencies
  - Scoring: 0-2 elements = INSUFFICIENT (must ask), 3-4 = MARGINAL (proceed with caution), 5+ = SUFFICIENT (proceed confidently)

## Prerequisites

Before proceeding, verify:

1. **MCP Status Validation**: Perform MCP server status checks (see `mcp-status.md` for detailed steps)
   - Test each configured MCP server connection (Atlassian, GitHub, etc.)
   - Verify all required integrations are authorized and operational
   - **If any MCP server fails validation, STOP and report the failure. Do not proceed.**
   - **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.

2. **Task Exists**: Verify the task exists in the issue tracker
   - Use MCP tools to fetch task by `{TASK_KEY}`
   - Use `mcp_atlassian_getJiraIssue` for Jira issues
   - Use `mcp_github_issue_read` for GitHub Issues
   - **If task doesn't exist, STOP and report error: "Task {TASK_KEY} not found"**

3. **Task Has Sufficient Detail** (using intelligent analysis):
   - **Analyze task content intelligently:**
     - Parse task description for completeness
     - Detect vague language patterns:
       - Generic terms: "improve", "enhance", "fix", "add feature" without specifics
       - Missing context: No user personas, no use cases, no success metrics
       - Ambiguous scope: No boundaries, no "in scope" vs "out of scope"
       - Missing criteria: No acceptance criteria, no definition of done
     - Assess information density:
       - Very short descriptions (< 50 words) likely insufficient
       - No examples or scenarios provided
       - No technical requirements mentioned
       - No dependencies or constraints identified
   - **Intelligent gap detection:**
     - Identify specific missing information categories
     - Determine which gaps are critical vs nice-to-have
     - Generate contextually appropriate questions based on:
       - Task type (epic, story, technical task)
       - Domain/context clues in existing description
       - Common patterns for similar tasks
   - **Decision logic:**
     - **If task has < 3 of these elements: STOP and ask**
       - Clear, specific goals (not vague)
       - Defined scope or boundaries
       - User context (personas, use cases) OR technical context
       - Success criteria or acceptance criteria
       - Any constraints or dependencies
     - **If task description is < 50 words and vague: STOP and ask**
     - **If key terms are undefined: STOP and ask**
       - "User experience" - which users? what experience?
       - "Performance" - what metrics? what targets?
       - "Feature" - what exactly? for whom?
   - **If information is insufficient:**
     - Generate 3-5 specific, actionable questions
     - Questions should be:
       - Contextual to the task domain
       - Focused on critical gaps
       - Actionable (user can answer clearly)
       - Prioritized (most important first)
     - Present questions clearly with context
     - Wait for user response before proceeding
     - Do NOT make assumptions or proceed with incomplete information
   - **If information is sufficient:**
     - Proceed to decomposition analysis
     - Note any assumptions made (document in breakdown)
   - **If task lacks sufficient detail, STOP and ask user for clarification before proceeding.**

## Usage

```
/decompose-task TASK-123
```

---

## PBI 4-part anatomy (for subtasks)

Use this structure when generating subtask descriptions (Stories/Epics). **PBI template:** Use create-task's asset — [../create-task/assets/pbi-anatomy.md](../create-task/assets/pbi-anatomy.md) — load when building subtask PBI descriptions (same anatomy as create-task; child issues follow the same structure). Populate from parent task and inherited `{feature-domain}`; link to `specs/{feature-domain}/spec.md`. Same spec as parent; for subtasks, Directive scope is narrower than parent.

**Examples:**
- `/decompose-task PROJ-100` (epic)
- `/decompose-task STORY-50` (large story)

## Steps

1. **Read the task**
   - **Retrieve task from issue tracker:**
     - Use `mcp_atlassian_getJiraIssue` for Jira issues
       - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
     - Use `mcp_github_issue_read` for GitHub Issues
       - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY}
   - **Understand task goals and objectives:**
     - Parse task title and description
     - Identify the primary goal or objective
     - Extract any stated business value or user benefit
   - **Review task description and acceptance criteria:**
     - Read full description text
     - Extract acceptance criteria (numbered lists, checkboxes, "Given/When/Then" format)
     - Identify any existing scope definitions
   - **Identify scope boundaries:**
     - Look for explicit "in scope" vs "out of scope" statements
     - Identify any constraints or limitations mentioned
     - Note any dependencies on other work
   - **Review any attached documents or links:**
     - Check for attached files or documents
     - Review any linked issues or related tasks
     - Note any external documentation referenced
   - **If task cannot be retrieved, STOP and report: "Task {TASK_KEY} not found or inaccessible"**

2. **Validate task information (Intelligent Analysis)**
   - **Apply intelligent analysis patterns (see Prerequisites section for detailed logic):**
     - Parse task description for completeness
     - Detect vague language patterns (generic terms, missing context, ambiguous scope, missing criteria)
     - Assess information density using 5-element scoring
     - Perform intelligent gap detection
   - **Apply decision logic:**
     - **If task has < 3 of required elements: STOP and ask**
       - Clear, specific goals (not vague)
       - Defined scope or boundaries
       - User context (personas, use cases) OR technical context
       - Success criteria or acceptance criteria
       - Any constraints or dependencies
     - **If task description is < 50 words and vague: STOP and ask**
     - **If key terms are undefined: STOP and ask**
   - **If information is insufficient:**
     - Generate 3-5 specific, actionable questions using context-aware question generation
     - Present questions clearly with context
     - Wait for user response before proceeding
     - Do NOT make assumptions or proceed with incomplete information
   - **If information is sufficient:**
     - Proceed to scope analysis
     - Note any assumptions made (document in breakdown)

3. **Analyze task scope**
   - **Break down task into logical work areas:**
     - Identify major functional areas or components
     - Group related functionality together
     - Consider technical vs user-facing separation
   - **Identify user personas and use cases** (if applicable):
     - Extract user personas from task description
     - Identify primary use cases or user journeys
     - Note any edge cases or special scenarios
   - **Determine technical components involved:**
     - Identify technical layers or components (frontend, backend, database, API, etc.)
     - Note any integration points with external systems
     - Identify any technical constraints or requirements
   - **Identify dependencies between work areas:**
     - Map dependencies between different work areas
     - Identify blocking dependencies (must be done first)
     - Note parallel work opportunities (can be done simultaneously)
   - **Consider implementation phases or milestones:**
     - Identify logical phases for implementation
     - Consider MVP vs enhancement separation
     - Plan for incremental delivery if applicable
   - **If scope analysis reveals major gaps or ambiguities, ask user for clarification before proceeding.**

3a. **Extract feature domain from parent** (for PBI structure inheritance)
   - **Determine if parent requires PBI structure:**
     - Check parent task type: Epic or Story (PBI required)
     - Check parent task type: Bug or Task (PBI optional)
   - **Extract feature domain from parent task:**
     1. **From parent labels:**
        - Look for label pattern: `feature:{domain}`
        - Extract `{domain}` from label
        - Example: `feature:user-authentication` → `user-authentication`
     2. **From parent description:**
        - Parse parent description for Context Pointer section
        - Extract domain from spec link: `specs/{domain}/spec.md`
        - Example: `specs/user-authentication/spec.md` → `user-authentication`
     3. **From parent epic (if parent is a story):**
        - If parent has parent epic, check epic for domain
        - Use `mcp_atlassian_getJiraIssue` to fetch epic
        - Extract domain from epic labels or description
     4. **Ask user if domain not found:**
        - If parent has no domain, ask: "Which feature domain for these subtasks? (e.g., user-authentication, payment-processing)"
        - Provide examples from existing specs
   - **Validate feature domain format:**
     - Must be kebab-case (lowercase with hyphens)
     - Pattern: `[a-z]+(-[a-z]+)*`
     - **If invalid format, normalize or ask user for correction**
   - **Check if spec exists:**
     - Use `glob_file_search` with pattern: `**/specs/{feature-domain}/spec.md`
     - **If spec exists:** Note for PBI generation (valid links)
     - **If spec missing:** Warn but proceed with placeholders
   - **Store feature domain for subtask generation:**
     - Save domain to use in step 4 (subtask description generation)
     - All child tasks will inherit same domain

4. **Generate subtasks**
   - **Create tasks following appropriate format:**
     - For user stories: "As a [user], I want [goal], so that [benefit]" format
     - For technical tasks: Use clear action-oriented descriptions
   - **Generate subtask descriptions with PBI structure** (for Stories and Epics):
     - **Use the shared PBI 4-part anatomy** — load [../create-task/assets/pbi-anatomy.md](../create-task/assets/pbi-anatomy.md) (see "PBI 4-part anatomy (for subtasks)" section above).
     - **For each subtask, populate 4-part anatomy:**
       1. **Directive Section:**
          - Specific scope for this subtask (narrower than parent)
          - Clear in scope / out of scope boundaries
          - Dependencies on other subtasks (if any)
       2. **Context Pointer Section:**
          - Use {feature-domain} inherited from parent (step 3a)
          - Generate link: `../../specs/{feature-domain}/spec.md#blueprint`
          - Same spec as parent, but subtask-specific scope
       3. **Verification Pointer Section:**
          - Same {feature-domain} as parent
          - Generate link: `../../specs/{feature-domain}/spec.md#contract`
          - Reference parent's Contract for overall goals
       4. **Refinement Rule Section:**
          - Use the Refinement Rule from the shared PBI template; same as parent's refinement rule
     - **Validate PBI structure for each subtask:**
       - Verify all 4 sections present
       - Verify feature domain matches parent
       - Verify links are well-formed
     - **Fallback for non-Story subtasks:**
       - Use simpler description format for technical tasks/bugs
   - **Ensure each task meets subtask criteria:**
     - Independent and can be developed standalone (or clearly defined dependencies)
     - Well-defined with clear acceptance criteria
     - Appropriately sized (completable in 1-2 days typically, 1-2 sprint points)
     - Delivers user or technical value
   - **Write clear, descriptive titles:**
     - Use action verbs (create, implement, add, refactor, etc.)
     - Be specific about what is being done
     - Include context if needed (e.g., "Add user authentication to mobile app")
   - **Define comprehensive acceptance criteria for each task:**
     - Minimum 3-5 acceptance criteria per task
     - Criteria should be specific, testable, and verifiable
     - Include both positive and negative test cases where applicable
   - **Identify task dependencies and sequence:**
     - Mark which tasks depend on others
     - Establish logical sequence for task execution
     - Consider parallel execution opportunities
   - **If unable to generate well-defined subtasks, ask user for additional context or clarification.**

5. **Validate breakdown quality**
   - **Review generated tasks for completeness:**
     - Verify all major work areas are covered
     - Check that no critical functionality is missing
     - Ensure scope matches original task
   - **Ensure tasks are appropriately sized:**
     - Each task should be completable in 1-2 days
     - Tasks should be roughly similar in size
     - Large tasks should be further decomposed
   - **Verify tasks are appropriately sized:**
     - Use Task Quality Checklist (see Checklists section)
     - Ensure each task meets all criteria
   - **Check for missing dependencies:**
     - Verify all dependencies are identified
     - Ensure dependency chains are clear
     - Check for circular dependencies
   - **Verify PBI structure consistency:**
     - All subtasks reference same feature domain
     - All subtasks have 4-part anatomy (if Stories/Epics)
     - All links point to correct spec
   - **If breakdown seems incomplete or unclear:**
     - Ask user for additional context
     - Request clarification on ambiguous areas
     - Do NOT proceed with incomplete breakdown
   - **If breakdown quality is insufficient, STOP and revise before creating tasks in tracker.**

6. **Prioritize tasks**
   - **Determine task priority based on:**
     - User value and business impact (highest priority for high-value tasks)
     - Technical dependencies (blocking tasks first)
     - Risk and complexity (high-risk tasks may need early attention)
     - Implementation sequence (prerequisites first)
   - **Set task order/sequence:**
     - Establish logical sequence based on dependencies
     - Consider parallel work opportunities
     - Plan for incremental delivery
   - **Identify which tasks are MVP vs nice-to-have:**
     - Separate core functionality from enhancements
     - Mark MVP tasks clearly
     - Consider separating enhancement tasks for later sprints
   - **Document priority rationale if non-obvious:**
     - Note any business reasons for priority
     - Document any assumptions about priority

7. **Create tasks in tracker**
   - **For each subtask:**
     - **Create task with required fields:**
       - Clear title (from step 4)
       - Detailed description with PBI structure (from step 4, if Stories/Epics)
       - Acceptance criteria (from step 4)
       - Priority/rank (from step 6)
       - Labels: Include `feature:{domain}` label (inherited from parent)
     - **Use MCP tools to create tasks:**
       - Use `mcp_atlassian_createJiraIssue` for Jira
         - Parameters: `cloudId`, `projectKey`, `issueTypeName` (typically "Story" or "Task"), `summary`, `description`, `additional_fields` (for parent link, priority, labels including `feature:{domain}`)
       - Use `mcp_github_create_issue` for GitHub
         - Parameters: `owner`, `repo`, `title`, `body` (markdown with PBI description and acceptance criteria), `labels` (include `feature:{domain}`)
     - **Link all tasks to parent task/epic:**
       - Set parent field in Jira (`parent` in `additional_fields`)
       - Link via issue references in GitHub (include parent issue number in body)
     - **Set initial task status to "To Do"** (default behavior of most trackers)
     - **Leave tasks unassigned** (assignment happens during sprint planning)
   - **If task creation fails for any subtask, STOP and report the error. Do not proceed with remaining tasks until error is resolved.**

8. **Document breakdown**
   - **Add breakdown summary comment to parent task:**
     - Use `mcp_atlassian_addCommentToJiraIssue` for Jira
       - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown summary
     - Use `mcp_github_add_issue_comment` for GitHub
       - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY}, `body` = markdown summary
   - **Include in summary:**
     - Task count and overview (e.g., "Created 5 subtasks for this epic")
     - List of created subtasks with their keys/IDs
     - Brief description of breakdown approach
   - **Note any assumptions or decisions made:**
     - Document assumptions made during analysis
     - Note any decisions about scope or approach
     - Include rationale for priority decisions if non-obvious
   - **Document task dependencies if applicable:**
     - List any dependency relationships
     - Note recommended sequence for execution
     - Highlight any blocking dependencies

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
- `mcp_atlassian_getJiraIssue` - Fetch task details by {TASK_KEY}
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
  - Extract: title, description, acceptance criteria, labels, priority, status, parent/epic link
- `mcp_atlassian_createJiraIssue` - Create subtasks in Jira
  - Parameters: `cloudId`, `projectKey`, `issueTypeName` (e.g., "Story", "Task"), `summary`, `description`, `additional_fields` (for `parent`, `priority`, `labels`, `components`)
  - Use to create each subtask after decomposition
- `mcp_atlassian_addCommentToJiraIssue` - Add breakdown summary comment to parent task
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown summary
  - Use to document the decomposition results

### MCP Tools (GitHub)
- A lightweight read-only GitHub MCP tool to verify connection (see Cursor Settings → Tools & MCP for exact names)
- `mcp_github_issue_read` - Fetch GitHub issue details
  - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY} (if numeric)
  - Extract: title, body, labels, state, milestone
- `mcp_github_create_issue` - Create subtasks as GitHub issues
  - Parameters: `owner`, `repo`, `title`, `body` (markdown with description and acceptance criteria), `labels`
  - Use to create each subtask after decomposition
  - Note: GitHub doesn't have native parent-child relationships; use issue references in body
- `mcp_github_add_issue_comment` - Add breakdown summary comment to parent issue
  - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY}, `body` = markdown summary
  - Use to document the decomposition results

### Codebase Tools
- `codebase_search` - Search for technical context if needed
  - Query: "How is [similar feature] implemented?" or "Where is [component] used?"
  - Use when task involves technical work that requires understanding existing codebase patterns
  - Use to identify technical components or integration points
- `grep` - Find specific patterns, functions, or classes
  - Pattern: component names, function names, file patterns
  - Use to identify related code or technical dependencies

### Filesystem Tools
- `read_file` - Read plan files or external docs referenced in task
  - Read plan files if referenced in task
  - Parameters: `target_file` = path to document
  - PBI template: [../create-task/assets/pbi-anatomy.md](../create-task/assets/pbi-anatomy.md) (see "PBI 4-part anatomy (for subtasks)" section).
  - Use when task references external documentation or plan files
- `glob_file_search` - Search for specs
  - Find specs: Pattern `**/specs/{feature-domain}/spec.md`
  - Parameters: `pattern` = glob pattern to search
  - Use to check if spec exists for inherited feature domain

## Pre-flight Checklist
- [ ] MCP status validation performed (see `mcp-status.md`)
- [ ] All MCP servers connected and authorized
- [ ] Task retrieved from issue tracker
- [ ] Task information validated using intelligent analysis
- [ ] Task has sufficient detail (or clarification requested from user)
- [ ] All prerequisites met before proceeding to decomposition

## Task Quality Checklist

For each generated subtask, verify:
- [ ] Follows appropriate format (user story format for user-facing tasks, action-oriented for technical tasks)
- [ ] Has clear acceptance criteria (3-5 criteria minimum)
- [ ] Is appropriately sized (completable in 1-2 days typically, 1-2 sprint points)
- [ ] Is independent and can be developed standalone (or clearly defined dependencies)
- [ ] Delivers value (user or technical)
- [ ] Has clear definition of done
- [ ] Is testable and verifiable

## Task Breakdown Checklist

- [ ] Parent task read and understood
- [ ] Task information validated (sufficient detail)
- [ ] Missing information requested from user (if needed)
- [ ] Task scope analyzed
- [ ] Work areas identified
- [ ] Breakdown quality validated
- [ ] Subtasks generated (minimum 3-5 tasks per parent)
- [ ] Tasks are well-defined and appropriately sized
- [ ] Acceptance criteria defined for each task
- [ ] Tasks prioritized and sequenced
- [ ] All tasks created in tracker
- [ ] Tasks linked to parent task/epic
- [ ] Breakdown documented in parent task comments
- [ ] Tasks ready for team estimation

## Guidance

### Role
Act as a **Scrum Master or Product Manager** responsible for decomposing large tasks into well-defined, actionable subtasks. You are analytical, thorough, and ensure that decomposition results in tasks that are clear, appropriately sized, and ready for team estimation and implementation.

### Instruction
Execute the decompose-task workflow to break down large tasks into manageable subtasks. This includes:
1. Performing prerequisite validation checks
2. Reading and understanding the parent task
3. Validating task information using intelligent analysis
4. Analyzing task scope to identify work areas
5. Generating well-defined subtasks that meet quality criteria
6. Validating breakdown quality
7. Prioritizing and sequencing tasks
8. Creating tasks in the issue tracker
9. Documenting the decomposition results

### Context
- The task is tracked in an issue management system (Jira, GitHub Issues, Azure DevOps, etc.)
- Large tasks (epics or large stories) need to be broken down into sprint-sized tasks
- MCP integrations provide access to issue trackers for reading tasks and creating subtasks
- The decomposition process uses intelligent analysis to ensure tasks have sufficient detail before decomposition
- Generated subtasks must meet specific quality criteria to be useful for the development team
- **ASDLC patterns**: [The PBI](asdlc://the-pbi), [Context Gates](asdlc://context-gates)
- **ASDLC pillars**: **Factory Architecture** (decomposition workflow), **Quality Control** (information-density gate)

### Examples

**ASDLC**: [Context Gates](asdlc://context-gates) — Information-density check acts as an input gate before decomposition.

**Example 1: Vague Epic**

```
You: /decompose-task EPIC-100

AI:
✓ Reading EPIC-100: Improve User Experience

Analysis:
- Description: 8 words (insufficient length)
- Vague terms detected: "improve", "user experience" (undefined)
- Missing: scope, personas, success criteria, constraints
- Information density: 1/5 elements

⚠ Insufficient information detected. To create a proper breakdown, I need:

1. What specific user experience problems are we solving? (e.g., slow load times, confusing navigation, mobile usability)
2. Which user personas are affected? (e.g., new users, power users, mobile users)
3. What are the success criteria? (e.g., reduce bounce rate by 20%, increase task completion by 30%)
4. What's in scope vs out of scope? (e.g., only mobile app, or also web?)

Please provide this information so I can generate well-defined tasks.
```

**Example 2: Partially Defined Epic**

```
You: /decompose-task EPIC-200

AI:
✓ Reading EPIC-200: Add payment processing for subscription plans

Analysis:
- Description: Clear action and object
- Missing: user context, success criteria, technical constraints
- Information density: 2/5 elements

⚠ Some information is missing. To ensure a complete breakdown:

1. Which user personas need this? (e.g., new subscribers, existing customers upgrading)
2. What are the acceptance criteria? (e.g., support credit cards, handle refunds, PCI compliance)
3. Are there technical constraints? (e.g., must use Stripe, integrate with existing billing system)

Proceeding with breakdown, but will note assumptions made.
```

**Example 3: Well-Defined Epic**

```
You: /decompose-task EPIC-300

AI:
✓ Reading EPIC-300: Implement OAuth 2.0 authentication for mobile app users

Analysis:
- Description: Specific technology and scope
- Contains: technical approach (OAuth 2.0), scope (mobile app), users (mobile users)
- Information density: 4/5 elements

✓ Sufficient information. Proceeding with breakdown...

[Decomposition process continues...]

Generated 5 subtasks:
1. EPIC-300-1: Implement OAuth 2.0 client library integration
2. EPIC-300-2: Create authentication UI components for mobile app
3. EPIC-300-3: Implement token storage and refresh logic
4. EPIC-300-4: Add user session management
5. EPIC-300-5: Write integration tests for OAuth flow

Breakdown documented in EPIC-300 comments.
```

**Example 4: Large Story Decomposition**

```
You: /decompose-task STORY-50

AI:
✓ Reading STORY-50: Add user profile editing functionality

Analysis:
- Description: Clear feature, but needs more detail
- Information density: 3/5 elements (MARGINAL)
- Proceeding with caution...

[Decomposition analysis...]

Generated 4 subtasks:
1. STORY-50-1: Create profile edit UI components
2. STORY-50-2: Implement profile update API endpoint
3. STORY-50-3: Add profile image upload functionality
4. STORY-50-4: Write tests for profile editing flow

Breakdown documented in STORY-50 comments.
```

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data in task descriptions
   - **AGENTS.md Optional**: Commands work without AGENTS.md. Standards apply regardless of whether AGENTS.md exists.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Prerequisites Must Pass**: Do not proceed if MCP validation fails, task doesn't exist, or task lacks sufficient detail. STOP and report the issue.
3. **Intelligent Analysis Required**: Always apply intelligent analysis patterns before decomposition. Do not proceed with vague or incomplete tasks.
4. **Information Density Scoring**: Use 5-element scoring (0-2: INSUFFICIENT must ask, 3-4: MARGINAL proceed with caution, 5+: SUFFICIENT proceed confidently).
5. **Subtask Quality Criteria**: All generated subtasks must meet the Task Quality Checklist criteria. If subtasks don't meet criteria, revise before creating in tracker.
5. **Minimum Subtask Count**: Generate minimum 3-5 subtasks per parent task. If unable to generate sufficient subtasks, the parent task may need further clarification.
6. **Task Size**: Each subtask should be completable in 1-2 days (1-2 sprint points). Larger tasks should be further decomposed.
7. **Dependency Clarity**: Clearly identify and document task dependencies. Do not create tasks with unclear or circular dependencies.
8. **Validation Before Creation**: Validate breakdown quality before creating tasks in tracker. Do not create tasks if breakdown quality is insufficient.
9. **Error Handling**: If task creation fails for any subtask, STOP and report the error. Do not proceed with remaining tasks until error is resolved.
10. **Documentation Required**: Always document the decomposition results in a comment on the parent task, including task count, list of created tasks, and any assumptions or decisions.
11. **Feature Domain Inheritance**: Extract feature domain from parent task (from labels, description, or epic). All subtasks must inherit same domain.
12. **PBI Structure for Subtasks** (Stories/Epics): Generate subtask descriptions with ASDLC PBI 4-part anatomy (Directive, Context Pointer, Verification Pointer, Refinement Rule).
13. **Spec Reference Consistency**: All subtasks must reference the same spec as parent (`specs/{feature-domain}/spec.md`).
14. **PBI structure** (Stories/Epics): Use the shared PBI template at create-task/assets/pbi-anatomy.md; populate for each subtask.
15. **Feature Label Inheritance**: Add label `feature:{domain}` to all subtasks (inherited from parent).

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- Task creation patterns: See `create-task.md` for task creation workflows and validation patterns
- User story format: "As a [user], I want [goal], so that [benefit]"
- Subtask criteria: Defined in Definitions section above
- PBI structure: Shared template at create-task/assets/pbi-anatomy.md
- Spec Structure: See `specs/README.md` for Blueprint + Contract format
- ASDLC Patterns: The PBI (4-part anatomy), The Spec (permanent pointer target)

### Output
1. **Decomposed Subtasks**: Well-defined subtasks created in the issue tracker with:
   - Clear titles and descriptions
   - Comprehensive acceptance criteria (3-5 per task)
   - Appropriate priority and sequencing
   - Links to parent task/epic
   - Status set to "To Do", unassigned

2. **Documentation**: Breakdown summary comment added to parent task including:
   - Count of created subtasks
   - List of created subtasks with their keys/IDs
   - Brief description of breakdown approach
   - Any assumptions or decisions made
   - Task dependencies and recommended sequence

The decomposition should result in tasks that are ready for team estimation and sprint planning, with clear scope, acceptance criteria, and dependencies.

## Best Practices

- **Validate first** - Always check if task has sufficient information before proceeding
- **Ask, don't assume** - If information is missing, ask specific questions rather than guessing
- **Start with user value** - Focus on what users need, not technical implementation
- **Keep tasks small** - Aim for tasks that can be completed in 1-2 days
- **Be specific** - Vague tasks lead to confusion during development
- **Consider dependencies** - Identify and sequence dependent tasks
- **Think in slices** - Create vertical slices (full feature) not horizontal layers (just backend)
- **Review with team** - Use this as input for team refinement sessions

## Intelligent Analysis Patterns

The command uses pattern recognition to detect insufficient information:

### Vague Language Detection

**Red flags that trigger clarification:**
- Generic action verbs without objects: "improve", "enhance", "fix", "add"
- Abstract concepts without definition: "user experience", "performance", "quality"
- Missing specificity: "some users", "better", "faster", "easier"
- No concrete examples or scenarios

**Example analysis:**
```
Task: "Improve user experience"
Analysis:
- "Improve" is vague (what exactly?)
- "User experience" is undefined (which aspects?)
- No success criteria
→ INSUFFICIENT: Ask for specifics
```

### Information Density Scoring

**Minimum viable information:**
- Task description > 50 words (unless very technical/clear)
- Contains at least 3 of: goals, scope, users, criteria, constraints
- Has concrete examples or scenarios
- Defines key terms used

**Scoring logic:**
- 0-2 elements present: INSUFFICIENT (must ask)
- 3-4 elements present: MARGINAL (proceed with caution, note assumptions)
- 5+ elements present: SUFFICIENT (proceed confidently)

### Context-Aware Question Generation

**Question generation based on task type:**

**For user-facing tasks:**
- "Which user personas are affected?"
- "What user problems are we solving?"
- "What does success look like for users?"

**For technical tasks:**
- "What are the technical constraints?"
- "What are the integration points?"
- "What are the performance requirements?"

**For feature requests:**
- "What specific functionality is needed?"
- "Who will use this feature?"
- "What are the acceptance criteria?"

**For improvements:**
- "What specific problems are we solving?"
- "What are the current pain points?"
- "How will we measure improvement?"

### Example Intelligent Interactions

**Example 1: Vague Epic**

```
You: /decompose-task EPIC-100

AI:
✓ Reading EPIC-100: Improve User Experience

Analysis:
- Description: 8 words (insufficient length)
- Vague terms detected: "improve", "user experience" (undefined)
- Missing: scope, personas, success criteria, constraints
- Information density: 1/5 elements

⚠ Insufficient information detected. To create a proper breakdown, I need:

1. What specific user experience problems are we solving? (e.g., slow load times, confusing navigation, mobile usability)
2. Which user personas are affected? (e.g., new users, power users, mobile users)
3. What are the success criteria? (e.g., reduce bounce rate by 20%, increase task completion by 30%)
4. What's in scope vs out of scope? (e.g., only mobile app, or also web?)

Please provide this information so I can generate well-defined tasks.
```

**Example 2: Partially Defined Epic**

```
You: /decompose-task EPIC-200

AI:
✓ Reading EPIC-200: Add payment processing for subscription plans

Analysis:
- Description: Clear action and object
- Missing: user context, success criteria, technical constraints
- Information density: 2/5 elements

⚠ Some information is missing. To ensure a complete breakdown:

1. Which user personas need this? (e.g., new subscribers, existing customers upgrading)
2. What are the acceptance criteria? (e.g., support credit cards, handle refunds, PCI compliance)
3. Are there technical constraints? (e.g., must use Stripe, integrate with existing billing system)

Proceeding with breakdown, but will note assumptions made.
```

**Example 3: Well-Defined Epic**

```
You: /decompose-task EPIC-300

AI:
✓ Reading EPIC-300: Implement OAuth 2.0 authentication for mobile app users

Analysis:
- Description: Specific technology and scope
- Contains: technical approach (OAuth 2.0), scope (mobile app), users (mobile users)
- Information density: 4/5 elements

✓ Sufficient information. Proceeding with breakdown...
```

## Common Patterns

**Feature-based breakdown:**
- Break large task into major features
- Each feature becomes a task or task group

**User journey-based breakdown:**
- Identify user journeys within task
- Create tasks for each journey step

**Technical component breakdown:**
- Identify technical components
- Create tasks for each component (but ensure value)

**MVP vs Enhancement:**
- Identify core MVP tasks
- Separate enhancement tasks for later sprints

