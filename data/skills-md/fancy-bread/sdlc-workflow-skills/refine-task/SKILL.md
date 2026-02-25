---
name: refine-task
description: Refine Task
disable-model-invocation: true
---

# Refine Task

## Overview
Refine a task to meet Definition of Ready (DoR) by ensuring clarity, completeness, and readiness for work. Focuses on producing clean, well-organized PBIs (Product Backlog Items) with clear acceptance criteria and minimal fluff. Used during backlog refinement sessions to prepare tasks for human refinement meetings.

## Definitions

- **{TASK_KEY}**: Task/Story ID from issue tracker (e.g., `FB-15`, `PROJ-123`)
- **Definition of Ready (DoR)**: Criteria that a task must meet before it's ready for work:
  - Clear, unambiguous description
  - Complete acceptance criteria
  - Dependencies identified (if any)
  - Well-organized, scannable structure
- **Definition of Done (DoD)**: Criteria that must be met for a task to be considered complete (reference for refinement context)
- **PBI (Product Backlog Item)**: Task formatted with 4-part anatomy (Directive, Context Pointer, Verification Pointer, Refinement Rule) per ASDLC patterns
- **PBI 4-Part Anatomy**:
  - **Directive**: What to do, with explicit scope boundaries
  - **Context Pointer**: Reference to Spec Blueprint section
  - **Verification Pointer**: Reference to Spec Contract section
  - **Refinement Rule**: Protocol for when implementation diverges from Spec
- **Feature Domain**: Kebab-case feature name identifying the functional area (e.g., `user-authentication`, `payment-processing`) used to locate Specs at `specs/{feature-domain}/spec.md`
- **Completed Status**: "Done" or "Completed" status in Jira

## Prerequisites

Before proceeding, verify:

1. **MCP Status Validation**: Perform MCP server status checks (see `mcp-status.md` for detailed steps)
   - Test each configured MCP server connection (Atlassian, GitHub, etc.)
   - Verify all required integrations are authorized and operational
   - **If any MCP server fails validation, STOP and report the failure. Do not proceed.**
   - **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.

2. **Task Exists**: Verify the task exists in Jira
   - Use MCP tools to fetch task by `{TASK_KEY}`
   - **If task doesn't exist, STOP and report error: "Task {TASK_KEY} not found"**

3. **Task Has Sufficient Detail**: Verify task has:
   - Readable title and description
   - At least basic context
   - **If task is completely empty or unreadable, STOP and ask user to provide basic information.**

4. **Task is Refinable**: Verify task is not already in "Done" or "Completed" status
   - **If task is already completed, STOP and report: "Task {TASK_KEY} is already completed and cannot be refined."**

## PBI 4-part anatomy (validation reference)

Use to validate and refine tasks. **Shared template:** [../create-task/assets/pbi-anatomy.md](../create-task/assets/pbi-anatomy.md) — load when validating PBI structure. **Summary:** Directive (what to do, scope, constraints) → Context Pointer (`specs/{feature-domain}/spec.md#blueprint`) → Verification Pointer (`specs/{feature-domain}/spec.md#contract`) → Refinement Rule (STOP / update spec same commit / flag review if boundaries affected).

## Steps

1. **Validate and Read Task**
   - **Perform MCP status validation:**
     - Test Atlassian MCP connection using `mcp_atlassian_atlassianUserInfo`
     - Verify connection is authorized and operational
     - **If MCP connection fails, STOP and report the failure.**
   - **Obtain CloudId for Atlassian Tools:**
     - Use `mcp_atlassian_getAccessibleAtlassianResources` to get cloudId
     - Use the first result or match by site name
          - **Error Handling**: If cloudId cannot be determined, STOP and report: "Unable to determine Atlassian cloudId. Please verify MCP configuration."
       - **Fetch task from Jira:**
         - Use `mcp_atlassian_getJiraIssue` with `cloudId` and `issueIdOrKey` = {TASK_KEY}
         - Extract: title, description, acceptance criteria, labels, components, status, project key
       - **Verify task is in refinable state:**
         - Check status is not "Done" or "Completed"
         - **If task is completed, STOP and report: "Task {TASK_KEY} is already completed and cannot be refined."**
       - **Extract task details:**
         - Title, description, acceptance criteria (if present)
         - Labels, components
         - Project key

2. **Validate PBI Structure**
   - **Check for 4-part anatomy:**
     - **Directive**: Look for "## Directive" section with scope boundaries
     - **Context Pointer**: Look for "## Context Pointer" section with reference to Spec Blueprint
     - **Verification Pointer**: Look for "## Verification Pointer" section with reference to Spec Contract
     - **Refinement Rule**: Look for "## Refinement Rule" section with protocol for spec divergence
   - **Validate structure is present and well-formed:**
     - Check that all 4 parts are present (if task follows PBI structure)
     - Verify Context Pointer and Verification Pointer link to valid spec paths
     - Note any missing parts or malformed sections
   - **Provide guidance if structure is missing (graceful degradation):**
     - If PBI structure is not present: Note "Task does not follow PBI 4-part anatomy. Consider restructuring for better organization."
     - If structure is partial: Note which parts are missing and suggest adding them
     - **Important**: Tasks without PBI structure should still be refinable - focus on clarity and organization

3. **Detect Feature Domain and Validate Spec Existence**
   - **Extract feature domain from task:**
     - Parse labels for feature domain hints (e.g., "feature:authentication" → "user-authentication")
     - Extract from title or description if domain is mentioned
     - Check Context Pointer section if present (extract from spec path)
     - Use kebab-case format (e.g., `user-authentication`, `payment-processing`)
   - **Check if spec exists:**
     - Use `glob_file_search` to check for `specs/{feature-domain}/spec.md`
     - If spec exists: Validate that Context Pointer and Verification Pointer link to correct spec
     - If spec doesn't exist but is referenced: Warn "Spec referenced but not found at `specs/{feature-domain}/spec.md`. Consider creating spec using `/create-plan {TASK_KEY}`."
   - **Validate spec links:**
     - If Context Pointer exists: Verify it points to correct Blueprint section
     - If Verification Pointer exists: Verify it points to correct Contract section
     - If links are broken or incorrect: Note the issue and suggest correction

4. **Refine Task Content to Meet Definition of Ready** (Focus on clarity and organization)
   - **Focus on Definition of Ready criteria:**
     - **Clear, unambiguous description**: Ensure what, why, and context are clear
     - **Complete acceptance criteria**: Must be testable, specific, and concise
     - **Dependencies identified**: Note any blocking dependencies (if applicable)
     - **Well-organized structure**: Content is easy to scan and read
     - **Ready to start work**: All information needed to begin work is present
   - **Analyze description completeness:**
     - Check if description clearly states what needs to be done and why
     - Identify if description is significantly shorter or less detailed
     - Look for gaps in description (what, why, how)
     - Note: Only enhance if clearly missing critical information
   - **Check acceptance criteria quality:**
     - Verify acceptance criteria are testable and specific
     - Ensure acceptance criteria are concise (not verbose or redundant)
     - Identify if key acceptance criteria are missing
     - Note: Only add if clearly missing critical criteria
   - **Remove fluff and unnecessary content:**
     - Identify verbose or redundant sections
     - Remove unnecessary explanations that don't add value
     - Consolidate repetitive information
     - Focus on essential information only
   - **Organize content for easy scanning:**
     - Ensure clear headings and structure
     - Use bullet points for lists
     - Group related information together
     - Make content scannable (easy to read quickly)
   - **Enhancements (if needed):**
     - **Clarify ambiguous language:**
       - Replace vague terms with specific terms (if clear from context)
       - Do NOT rewrite entire sentences unnecessarily
       - Preserve existing structure when possible
     - **Add missing critical acceptance criteria only:**
       - Only if 0-1 acceptance criteria exist
       - Add 1-2 critical criteria based on task context
       - Keep criteria concise and testable
     - **Fill gaps in description:**
       - Add 1-2 sentences if description is extremely short (< 50 words)
       - Only add what's clearly missing (what or why)
       - Do NOT restructure unnecessarily
   - **Preserve existing good content:**
     - Keep all existing valuable information
     - Only enhance, never replace unnecessarily
     - Maintain original structure and style when appropriate

5. **Update Task in Jira**
   - **Prepare update fields:**
     - Description: Only if refined (clarity improvements, fluff removal, organization)
     - Acceptance criteria: Only if refined (added missing criteria, improved clarity)
   - **Update task:**
     - Use `mcp_atlassian_editJiraIssue` with:
       - `cloudId`
       - `issueIdOrKey` = {TASK_KEY}
       - `fields`: Object with fields to update
         - Description (if refined): `{ "description": { "type": "doc", "version": 1, "content": [...] } }`
         - Acceptance criteria (if refined): Update within description or use appropriate field
   - **Preserve all other fields:**
     - Do not modify labels, components, links, assignee, story points, etc.
   - **Verify update succeeded:**
     - Re-fetch task to confirm changes were applied

6. **Generate and Post Report**
   - **Create markdown report:**
     - **Header**: "## Refinement Report for {TASK_KEY}"
     - **Definition of Ready Status:**
       - List DoR criteria checked:
         - "✅ Clear description"
         - "✅ Acceptance criteria present, testable, and concise"
         - "✅ Dependencies identified (if any)"
         - "✅ Content organized for easy scanning"
     - **PBI Structure Validation:**
       - If PBI structure complete: "✅ Task follows PBI 4-part anatomy (Directive, Context Pointer, Verification Pointer, Refinement Rule)"
       - If PBI structure partial: "⚠️ Task has partial PBI structure. Missing: {list missing parts}. Consider adding missing sections for better organization."
       - If PBI structure missing: "ℹ️ Task does not follow PBI 4-part anatomy. Consider restructuring for better organization (see create-task/assets/pbi-anatomy.md)."
     - **Feature Domain and Spec Existence:**
       - If feature domain detected: "Feature domain: `{feature-domain}`"
       - If spec exists: "✅ Spec found at `specs/{feature-domain}/spec.md`"
       - If spec missing but referenced: "⚠️ Spec referenced but not found at `specs/{feature-domain}/spec.md`. Consider creating spec using `/create-plan {TASK_KEY}`."
       - If spec links validated: "✅ Context Pointer and Verification Pointer link to correct spec sections"
       - If spec links broken: "⚠️ Spec links are broken or incorrect. Please verify and update."
     - **Clarity Improvements:**
       - If description refined: "- Enhanced description clarity (added {count} sentences/clarifications, removed fluff)"
       - If acceptance criteria improved: "- Improved acceptance criteria (added {count} missing criteria, enhanced clarity, removed redundancy)"
       - If content organized: "- Reorganized content for better scanning and readability"
       - If fluff removed: "- Removed verbose or redundant content ({count} sections/sentences)"
       - If no refinements: "- No refinements needed (task already meets Definition of Ready)"
     - **Next Steps:**
       - If PBI structure incomplete: "Consider adding missing PBI sections for better organization."
       - If spec missing: "Consider creating spec at `specs/{feature-domain}/spec.md` using `/create-plan {TASK_KEY}`."
       - Otherwise: "Task refined and ready for human refinement meeting."
   - **Post report as comment:**
     - Use `mcp_atlassian_addCommentToJiraIssue` with:
       - `cloudId`
       - `issueIdOrKey` = {TASK_KEY}
       - `commentBody` = markdown report content
   - **Verify comment was posted:**
     - Confirm comment appears in issue

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
- `mcp_atlassian_getJiraIssue` - Fetch task to refine
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
  - Extract: title, description, acceptance criteria, labels, components, status, project key
- `mcp_atlassian_editJiraIssue` - Update task (description, acceptance criteria)
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `fields` = object with fields to update
- `mcp_atlassian_addCommentToJiraIssue` - Post refinement report
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown report

### Filesystem Tools
- `glob_file_search` - Check for spec existence at `specs/{feature-domain}/spec.md`
  - Pattern: `**/specs/*/spec.md`
- PBI template: [../create-task/assets/pbi-anatomy.md](../create-task/assets/pbi-anatomy.md) (see "PBI 4-part anatomy (validation reference)" section).

## Pre-flight Checklist
- [ ] MCP status validation performed (see `mcp-status.md`)
- [ ] All MCP servers connected and authorized
- [ ] Task exists in Jira
- [ ] Task has readable title and description
- [ ] Task is in refinable state (not "Done" or "Completed")
- [ ] CloudId obtained for Atlassian tools

## Refinement Checklist
- [ ] Task read and details extracted
- [ ] PBI structure validated (4-part anatomy checked)
- [ ] Feature domain detected and spec existence checked
- [ ] Task content analyzed for Definition of Ready refinements
- [ ] Clarity improvements made (description, AC, fluff removal)
- [ ] Content organized for easy scanning
- [ ] Task updated in Jira (if applicable)
- [ ] Refinement report generated and posted

## Guidance

### Role
Act as a **Scrum Master, Product Manager, or Team Lead** responsible for backlog refinement. You are analytical, detail-oriented, and focused on improving task clarity, organization, and readiness for human refinement meetings.

### Instruction
Execute the refine-task workflow to improve a task by validating PBI structure, checking spec existence, and enhancing clarity and organization. Focus on producing clean, scannable task descriptions that are ready for human refinement meetings. Remove fluff and ensure content is well-organized and easy to read.

### Context
- Tasks need refinement to meet Definition of Ready (DoR) before work begins
- DoR criteria: Clear description, complete acceptance criteria, dependencies identified, well-organized structure
- PBIs should follow 4-part anatomy (Directive, Context Pointer, Verification Pointer, Refinement Rule) per ASDLC patterns
- Feature domains link to Specs at `specs/{feature-domain}/spec.md` for permanent context
- Focus on clarity and organization, not adding unnecessary content
- Remove verbose or redundant content (fluff removal)
- Organize content for easy scanning and reading
- Tasks without PBI structure should still be refinable (graceful degradation)
- Conservative refinement approach preserves existing content while improving clarity
- **ASDLC patterns**: [The PBI](asdlc://the-pbi), [The Spec](asdlc://the-spec), [Context Gates](asdlc://context-gates)
- **ASDLC pillars**: **Factory Architecture** (refinement step), **Quality Control** (DoR as gate), **Standardized Parts** (PBI structure)

### Examples

**ASDLC**: [Context Gates](asdlc://context-gates) — Definition of Ready acts as an input gate before work can start.

**Example 1: Task with Complete PBI Structure**

```
Input: /refine-task FB-123

Task: "Add user authentication"
PBI Structure: ✅ Complete (all 4 parts present)
Feature Domain: user-authentication
Spec Existence: ✅ Found at specs/user-authentication/spec.md

Output:
- ✅ PBI structure validated (all 4 parts present)
- ✅ Spec found and links validated
- Enhanced description clarity (removed 2 redundant sentences)
- Improved acceptance criteria (added 1 missing criterion, enhanced clarity)
- Task refined and ready for human refinement meeting
```

**Example 2: Task with Partial PBI Structure**

```
Input: /refine-task FB-124

Task: "Update README.md with new command documentation"
PBI Structure: ⚠️ Partial (missing Context Pointer and Verification Pointer)
Feature Domain: commands
Spec Existence: ✅ Found at specs/user-authentication/spec.md

Output:
- ⚠️ PBI structure partial. Missing: Context Pointer, Verification Pointer
- ✅ Spec found
- Added missing PBI sections (Context Pointer, Verification Pointer)
- Enhanced description clarity
- Task refined and ready for human refinement meeting
```

**Example 3: Task with No PBI Structure**

```
Input: /refine-task FB-125

Task: "Create new reporting dashboard"
PBI Structure: ℹ️ Not present
Feature Domain: reporting
Spec Existence: ⚠️ Not found (referenced but missing)

Output:
- ℹ️ Task does not follow PBI 4-part anatomy
- ⚠️ Spec referenced but not found at specs/reporting/spec.md
- Enhanced description clarity (added what/why context)
- Improved acceptance criteria (added 2 missing criteria, removed fluff)
- Reorganized content for better scanning
- Task refined and ready for human refinement meeting
```

**Example 4: Task with Fluff and Poor Organization**

```
Input: /refine-task FB-126

Task: "Refactor payment service"
PBI Structure: ✅ Complete
Feature Domain: payment-processing
Spec Existence: ✅ Found

Output:
- ✅ PBI structure validated
- ✅ Spec found and links validated
- Removed verbose content (3 redundant sections)
- Enhanced description clarity (consolidated repetitive information)
- Improved acceptance criteria (removed redundancy, enhanced clarity)
- Reorganized content for better scanning
- Task refined and ready for human refinement meeting
```

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data in task descriptions
   - **AGENTS.md Optional**: Commands work without AGENTS.md. Standards apply regardless of whether AGENTS.md exists.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **MCP Validation**: Do not proceed if MCP status validation fails. STOP and report the failure.
3. **Task Validation**: Task must exist and be refinable (not "Done"). If not, STOP and report error.
4. **Definition of Ready Focus**: Refinement must ensure task meets DoR criteria (clear description, acceptance criteria, dependencies identified, well-organized structure).
5. **PBI Structure Validation**: Check for 4-part anatomy (Directive, Context Pointer, Verification Pointer, Refinement Rule). Provide guidance if missing, but allow graceful degradation (tasks without PBI structure should still be refinable).
6. **Feature Domain Detection**: Extract feature domain from task (labels, title, description) and check spec existence. Warn if spec is referenced but missing.
7. **Clarity Focus**: Enhance description completeness, improve acceptance criteria quality, remove fluff, and organize content for easy scanning.
8. **Conservative Refinement**: Only add missing critical details. Do NOT rewrite or restructure existing content unnecessarily.
9. **Fluff Removal**: Identify and remove verbose or redundant content. Focus on essential information only.
10. **Content Organization**: Ensure content is well-organized with clear headings, bullet points, and scannable structure.

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- PBI structure: Shared template at create-task/assets/pbi-anatomy.md; ASDLC patterns
- Task refinement: Conservative approach (preserve existing, enhance minimally)
- Spec location: `specs/{feature-domain}/spec.md` for permanent context

### Output
1. **Refined Task**: Task updated in Jira with:
   - Enhanced description (if clarity improvements made, fluff removed, content organized)
   - Enhanced acceptance criteria (if added missing criteria, improved clarity, removed redundancy)

2. **Refinement Report**: Comment posted to task with:
   - Definition of Ready status (DoR criteria checked)
   - PBI structure validation (complete, partial, or missing with guidance)
   - Feature domain and spec existence (domain detected, spec found/missing, links validated)
   - Clarity improvements (description enhancements, AC improvements, fluff removal, content organization)
   - Next steps (if PBI structure incomplete or spec missing)

The refinement should ensure tasks meet Definition of Ready criteria with clean, well-organized, scannable content that is ready for human refinement meetings. Tasks should follow PBI 4-part anatomy when possible, but graceful degradation allows refinement of tasks without PBI structure.

