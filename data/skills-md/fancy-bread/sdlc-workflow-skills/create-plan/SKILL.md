---
name: create-plan
description: Create a living specification (Spec) or plan for a feature by analyzing requirements and codebase
disable-model-invocation: true
---

# Create Spec

## Overview
Create a living specification (Spec) for a feature by analyzing requirements, reviewing the codebase, and generating a Blueprint + Contract document that evolves with the code.

## Definitions

- **{TASK_KEY}**: Story/Issue ID from the issue tracker (e.g., `FB-6`, `PROJ-123`, `KAN-42`)
- **{FEATURE_DOMAIN}**: Kebab-case feature name (e.g., `user-authentication`, `payment-processing`, `notifications`)
- **Spec Document**: Living specification saved at `specs/{FEATURE_DOMAIN}/spec.md`
  - **Blueprint**: Context, Architecture, Anti-Patterns (the "why" and "how")
  - **Contract**: Definition of Done, Regression Guardrails, Scenarios (the "what")
  - Lives permanently with code, updated in same commit as behavior changes
- **Plan Document** (still exists for transient task planning): Task-level implementation plan at `.plans/{TASK_KEY}-{description}.plan.md`
  - Defines Delta (what changes) vs Spec which defines State (how it works)
  - Created per-task, discarded after merge
- **Story Details**: Information from issue tracker (Jira, GitHub Issues, Azure DevOps, etc.)
  - Includes title, description, acceptance criteria, and related context
- **User Story Format**: Typically follows "As a [user type], I want [goal], so that [benefit]"
- **Acceptance Criteria**: Specific, testable conditions that must be met for the story to be considered complete

## Prerequisites

Before proceeding, verify:

1. **MCP Status Validation**: Perform MCP server status checks (see `mcp-status.md` for detailed steps)
   - Test each configured MCP server connection (Atlassian, GitHub, etc.)
   - Verify all required integrations are authorized and operational
   - **If any MCP server fails validation, STOP and report the failure. Do not proceed.**
   - **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.

2. **Story Exists**: Verify the story exists in the issue tracker
   - Use MCP tools to fetch story by `{TASK_KEY}`
   - **If story doesn't exist, STOP and report error: "Story {TASK_KEY} not found"**

3. **Story Has Sufficient Detail**: Verify story has:
   - Clear description or user story format
   - At least 3-5 acceptance criteria
   - Context about the problem being solved
   - **If story lacks sufficient detail, STOP and ask user for clarification before proceeding.**

4. **Determine Document Type**: Decide whether to create a Spec or Plan
   - **Create Spec** when: New feature domain, architectural patterns, API contracts, data models, cross-team dependencies
   - **Create Plan** when: Bug fix, task-level implementation details, transient work
   - **Both** when: Feature needs permanent spec AND task needs implementation plan
   - **If unclear, ask user: "Should I create a Spec (permanent) or Plan (transient)?"**

## Steps

1. **Analyze story**
   - **Fetch story from issue tracker using MCP:**
     - Use `mcp_atlassian_getJiraIssue` for Jira issues
     - Use `mcp_github_issue_read` for GitHub Issues
     - Extract: title, description, acceptance criteria, labels, priority, related issues
   - **Parse user story format:**
     - Identify user persona ("As a...")
     - Extract goal ("I want...")
     - Understand benefit ("so that...")
     - If not in user story format, extract requirements from description
   - **Extract acceptance criteria:**
     - Look for numbered lists, checkboxes, or "Given/When/Then" format
     - Convert each criterion into a testable requirement
     - **If no acceptance criteria found, STOP and ask user to provide them.**
   - **Identify technical requirements:**
     - Parse technical constraints from description
     - Note any dependencies mentioned
     - Identify performance or security requirements
   - **Check for missing information:**
     - Is the problem clearly defined?
     - Are acceptance criteria specific and testable? (Minimum 3-5 criteria)
     - Is the scope clear?
     - Does it follow user story format or have clear requirements?
     - **If critical information is missing, STOP and ask specific questions to fill gaps.**
     - **Reference**: See `create-task.md` for detailed validation criteria
   - **Extract keywords for ASDLC pattern queries:**
     - Parse story title and description for domain terms (nouns, technical terms)
     - Identify keywords: authentication, security, testing, review, spec, plan, etc.
     - Map keywords to ASDLC pattern search terms:
       - "authentication", "security" → search for "security", "specs", "contracts"
       - "spec", "plan" → search for "the-spec", "the-pbi", "living-specs"
       - "review", "code review" → search for "adversarial-code-review", "constitutional-review"
       - "test", "testing" → search for "behavior-driven-development", "gherkin"
     - Use story labels if available (e.g., "asdlc-alignment" → search for ASDLC patterns)
     - Store keywords for use in Step 2.5

2. **Analyze codebase**
   - **Use codebase_search to find similar implementations:**
     - Search for similar features or patterns
     - Example: "How is file watching implemented?" or "Where is user authentication handled?"
     - Review 3-5 similar implementations to understand patterns
   - **Identify affected components:**
     - Use `codebase_search` to find related modules/components
     - Use `grep` to find specific patterns, functions, or classes
     - Review directory structure to understand organization
   - **Review existing patterns:**
     - How are similar features structured?
     - What testing patterns are used?
     - What naming conventions are followed?
     - How are errors handled?
   - **Identify files to examine:**
     - Main implementation files
     - Test files (look for `*.test.ts`, `*_test.py`, `*Test.java`, etc.)
     - Configuration files
     - Documentation files
   - **Review related test files:**
     - Understand test structure and patterns
     - Note test utilities and helpers
     - Identify test coverage expectations
   - **If codebase analysis reveals blockers or unclear patterns, note them in the plan for discussion.**

2.5. **Query ASDLC knowledge base for relevant patterns**
   - **Extract keywords from story:**
     - Use keywords extracted in Step 1 (domain terms mapped to ASDLC pattern categories)
     - Combine keywords into search query (space-separated or single term)
   - **Query ASDLC MCP:**
     - Use `mcp_asdlc_search_knowledge_base` with extracted keywords
     - Example: For story about "authentication", query: `mcp_asdlc_search_knowledge_base("authentication security specs")`
     - **If search fails, log warning and continue** (ASDLC queries are optional; don't block plan creation)
   - **Filter and rank results:**
     - Select 3-5 most relevant patterns based on keyword matches in title/description
     - Prefer patterns that match multiple keywords
     - Include both "Concepts" and "Patterns" from ASDLC knowledge base
     - Store pattern results: slugs, titles, descriptions
   - **Optional: Fetch detailed content:**
     - Use `mcp_asdlc_get_article` for top 1-2 patterns if detailed summaries needed
     - Only if full article content is required for plan generation

3. **Design implementation**
   - **For Specs**: Design Blueprint + Contract structure
     - **Blueprint**:
       - Context: Why does this feature exist? What problem does it solve?
       - Architecture: API contracts, data models, dependencies, dependency directions
       - Anti-Patterns: What agents must NOT do (with rationale)
     - **Contract**:
       - Definition of Done: Observable success criteria (checkboxes)
       - Regression Guardrails: Critical invariants that must never break
       - Scenarios: Gherkin-style (Given/When/Then) behavioral specifications
   - **For Plans**: Design task-level implementation steps
     - Break down into subtasks (3-7 logical units)
     - Identify files to create/modify
     - Plan test strategy
     - Document dependencies
   - **Identify files to create/modify:**
     - List new files to create (with paths)
     - List existing files to modify (with specific changes)
     - Group by component/module
   - **Plan database changes (if applicable):**
     - Schema changes
     - Migration scripts
     - Data model updates
   - **Design API changes (if applicable):**
     - New endpoints
     - Modified endpoints
     - Request/response formats
     - Error handling
   - **Plan test strategy:**
     - Unit tests for each component
     - Integration tests for workflows
     - Test data requirements
     - Mock/stub requirements
   - **Document dependencies:**
     - External libraries needed
     - Internal dependencies
     - Order of implementation
   - **Plan error handling:**
     - Error scenarios to handle
     - Error messages and codes
     - Logging requirements

4. **Generate document (Spec or Plan)**

   ### Option A: Generate Spec Document

   - **Check if spec already exists:**
     - Ask user for `{FEATURE_DOMAIN}` (kebab-case feature name)
     - Check if `specs/{FEATURE_DOMAIN}/spec.md` exists
     - If exists, ask: "Spec exists. Update existing or create new?"
   
   - **Create spec directory and file:**
     - Create directory: `specs/{FEATURE_DOMAIN}/`
     - Create file: `specs/{FEATURE_DOMAIN}/spec.md`
   
   - **Write spec using Blueprint + Contract structure:**
     ```markdown
     # Feature: {Feature Name}

     > **ASDLC Pattern**: [The Spec](https://asdlc.io/patterns/the-spec/)
     > **Status**: Active | Deprecated | Superseded
     > **Last Updated**: YYYY-MM-DD

     ---

     ## Blueprint

     ### Context
     [Why does this feature exist? What business problem does it solve?]

     ### Architecture
     - **API Contracts**: Endpoints, request/response formats
     - **Data Models**: Schemas, validation rules, data structures
     - **Dependencies**: What this depends on, what depends on this
     - **Dependency Directions**: Inbound/outbound relationships

     ### Anti-Patterns
     - [What agents must NOT do, with rationale]
     - [Forbidden approaches that were considered and rejected]

     ---

     ## Contract

     ### Definition of Done
     - [ ] [Observable success criterion 1]
     - [ ] [Observable success criterion 2]
     - [ ] [Observable success criterion 3]
     - [ ] [Automated verification: tests pass, lint passes, builds successfully]

     ### Regression Guardrails
     - [Critical invariant that must never break]
     - [Performance targets that must be maintained]
     - [Security requirements that must hold]

     ### Scenarios
     **Scenario: {Scenario Name}**
     - **Given**: [Precondition]
     - **When**: [Action]
     - **Then**: [Expected outcome]

     [Additional scenarios as needed]
     ```
   
   - **Post spec summary to issue tracker:**
     - Comment should include:
       - Link to spec file: `specs/{FEATURE_DOMAIN}/spec.md`
       - Brief summary of Blueprint (Context, Architecture)
       - Brief summary of Contract (Definition of Done, key scenarios)
     - **If posting fails, note it but don't stop - spec file creation is the primary goal.**

   ### Option B: Generate Plan Document (for transient task-level work)

   - **Create plan file at `.plans/{TASK_KEY}-{kebab-case-description}.plan.md`:**
     - **First, check if file already exists (optional - for information only):**
       - Use `glob_file_search` with pattern: `**/.plans/{TASK_KEY}-*.plan.md`
       - If files found, note them but proceed with creation (overwriting is acceptable for plan updates)
     - Use kebab-case for description (e.g., `PROJ-123-user-authentication.plan.md`)
   - **Write plan using the following structure:**
     ```markdown
     # {Story Title} ({TASK_KEY})

     ## Story
     [User story format or description]

     ## Context
     [Background information, why this is needed, related issues]

     ## Scope
     ### In Scope
     - [What is included]

     ### Out of Scope
     - [What is explicitly excluded]

     ## Acceptance Criteria
     1. [Criterion 1]
     2. [Criterion 2]
     3. [Criterion 3]
     ...

     ## Technical Design
     ### Architecture
     [High-level design approach]

     ### Components
     - Component 1: [Description]
     - Component 2: [Description]

     ### Data Model
     [If applicable: database schema, data structures]

     ### API Design
     [If applicable: endpoints, request/response formats]

     ## Implementation Steps
     1. **Subtask 1**: [Description]
        - Files to create: `path/to/file1.ts`
        - Files to modify: `path/to/file2.ts`
        - Tests: `path/to/file1.test.ts`

     2. **Subtask 2**: [Description]
        ...

     ## Testing
     ### Unit Tests
     - [Test cases for component 1]
     - [Test cases for component 2]

     ### Integration Tests
     - [Integration test scenarios]

     ### Test Data
     - [Test data requirements]

     ## Dependencies
     - [External libraries]
     - [Internal dependencies]

     ## Referenced ASDLC Patterns

     [If ASDLC patterns were discovered during analysis (Step 2.5), include them here]

     The following ASDLC patterns are relevant to this implementation:

     - **[{Pattern Title}](https://asdlc.io/patterns/{slug}/)** - {Brief description from search results}
     - **[{Pattern Title}](https://asdlc.io/practices/{slug}/)** - {Brief description}

     [If no patterns found or ASDLC MCP unavailable, omit this section or note: "No ASDLC patterns identified for this task."]

     ## Status
     - [ ] Story analyzed
     - [ ] Codebase reviewed
     - [ ] Technical design complete
     - [ ] Implementation steps defined
     - [ ] Testing strategy defined
     - [ ] Ready for implementation
     ```
   - **Verify plan file was created successfully**
   - **Post plan summary to issue tracker:**
     - **Sequence:**
       1. Fetch issue to verify it exists: `mcp_atlassian_getJiraIssue` or `mcp_github_issue_read`
       2. Create comment with plan summary: `mcp_atlassian_addCommentToJiraIssue` or `mcp_github_add_issue_comment`
       3. Verify comment was posted (optional - check issue comments)
     - Comment should include:
       - Link to plan file: `.plans/{TASK_KEY}-*.plan.md`
       - Brief summary of approach
       - Key implementation steps (3-5 bullets)
     - **If posting fails, note it but don't stop - plan file creation is the primary goal.**

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
  - Extract: title, description, acceptance criteria, labels, priority, status
- `mcp_atlassian_getJiraIssueRemoteIssueLinks` - Get related issues/links
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}
- `mcp_atlassian_addCommentToJiraIssue` - Post plan summary comment to issue
  - Parameters: `cloudId`, `issueIdOrKey` = {TASK_KEY}, `commentBody` = markdown summary

### MCP Tools (GitHub)
- A lightweight read-only GitHub MCP tool to verify connection (see Cursor Settings → Tools & MCP for exact names)
- `mcp_github_issue_read` - Fetch GitHub issue details
  - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY} (if numeric)
  - Extract: title, body, labels, state
- `mcp_github_add_issue_comment` - Post plan summary comment to GitHub issue
  - Parameters: `owner`, `repo`, `issue_number` = {TASK_KEY}, `body` = markdown summary

### MCP Tools (ASDLC)
- `mcp_asdlc_search_knowledge_base` - Search ASDLC knowledge base for patterns
  - Parameters: `query` = keywords extracted from story (string, space-separated or single term)
  - Returns: Array of matching articles with slug, title, description
  - Error handling: If search fails, log warning and continue without patterns (optional feature; don't block plan creation)
  - Usage: Called in Step 2.5 to discover relevant ASDLC patterns based on task domain
- `mcp_asdlc_get_article` - Get full article content for a pattern
  - Parameters: `slug` = pattern identifier from search results (string)
  - Returns: Full markdown content of pattern article
  - Usage: Optional, only for top 1-2 patterns if detailed content needed for plan generation

### Filesystem Tools
- `glob_file_search` - Check if plan file already exists
  - Pattern: `**/.plans/{TASK_KEY}-*.plan.md`
- `write` - Create new plan document file
  - Parameters: `file_path` = `.plans/{TASK_KEY}-{description}.plan.md`, `contents` = markdown plan
- `read_file` - Read existing code files for analysis
- `list_dir` - Explore directory structure to understand codebase organization

### Codebase Tools
- `codebase_search` - Search for similar implementations and patterns
  - Query: "How is [similar feature] implemented?"
  - Query: "Where is [component/pattern] used?"
  - Query: "How does [existing functionality] work?"
  - Use to find: similar features, existing patterns, architectural decisions
- `grep` - Find specific patterns, functions, classes, or imports
  - Pattern: function names, class names, imports, file extensions
  - Use to find: related files, test patterns, configuration files
- `glob_file_search` - Find files by pattern
  - Pattern: `**/*.test.ts`, `**/*_test.py`, `**/*Test.java` (test files)
  - Pattern: `**/config.*`, `**/*.config.*` (config files)

### Terminal Tools
- `run_terminal_cmd` - Execute commands for codebase analysis
  - `find . -name "*.test.*" -type f` - Find test files
  - `git log --oneline --grep="{keyword}"` - Search commit history for related work
  - `git ls-files | grep {pattern}` - List files matching pattern

## Planning Checklist
- [ ] MCP status validation performed
- [ ] Story fetched from issue tracker
- [ ] Story has sufficient detail (description, acceptance criteria)
- [ ] Document type determined (Spec vs Plan)
- [ ] User story format parsed (or requirements extracted)
- [ ] Acceptance criteria extracted and validated
- [ ] Codebase searched for similar implementations
- [ ] Existing patterns reviewed
- [ ] Affected components identified
- [ ] Related test files reviewed
- [ ] **If creating Spec:**
  - [ ] Feature domain identified
  - [ ] Blueprint designed (Context, Architecture, Anti-Patterns)
  - [ ] Contract designed (Definition of Done, Guardrails, Scenarios)
  - [ ] Spec document created at `specs/{FEATURE_DOMAIN}/spec.md`
  - [ ] Spec summary posted to issue
- [ ] **If creating Plan:**
  - [ ] Implementation broken down into subtasks
  - [ ] Files to create/modify identified
  - [ ] Database/API changes planned (if applicable)
  - [ ] Test strategy defined
  - [ ] Dependencies documented
  - [ ] Error handling planned
  - [ ] Plan document created at `.plans/{TASK_KEY}-*.plan.md`
  - [ ] Plan summary posted to issue

## Document Structures

### Spec Document Structure (Permanent)

The spec document must include the following sections:

1. **Feature Header**: Feature name, ASDLC pattern link, status, last updated date
2. **Blueprint Section**:
   - **Context**: Business problem and solution rationale
   - **Architecture**: API contracts, data models, dependencies, dependency directions
   - **Anti-Patterns**: Forbidden approaches with rationale
3. **Contract Section**:
   - **Definition of Done**: Observable, testable success criteria (checkboxes)
   - **Regression Guardrails**: Critical invariants that must never break
   - **Scenarios**: Gherkin-style (Given/When/Then) behavioral specifications

### Plan Document Structure (Transient)

The plan document must include the following sections:

1. **Story**: User story format or clear description
2. **Context**: Background, motivation, related issues
3. **Scope**: What's included and explicitly excluded
4. **Acceptance Criteria**: Numbered, testable criteria
5. **Technical Design**: Architecture, components, data model, API design
6. **Implementation Steps**: Ordered subtasks with file changes
7. **Testing**: Unit tests, integration tests, test data
8. **Dependencies**: External and internal dependencies
9. **Status**: Checklist for tracking progress

## Guidance

### Role
Act as a **software engineer** responsible for creating either a permanent living specification (Spec) or a transient implementation plan (Plan). You are analytical, thorough, and understand the difference between State (Spec) and Delta (Plan).

### Instruction
Execute the create-spec/create-plan workflow to generate either:
- **Spec** (Blueprint + Contract): Permanent living specification for a feature domain
- **Plan** (Implementation Steps): Transient task-level implementation guide

This includes:
1. Performing prerequisite validation checks
2. Analyzing the story and extracting requirements
3. Determining whether to create Spec or Plan (or both)
4. Reviewing the codebase to understand patterns
5. Designing the appropriate document structure
6. Generating the structured document with all required sections

### Context
- The story is tracked in an issue management system (Jira, Azure DevOps, GitHub Issues, etc.)
- The codebase has existing patterns, conventions, and architectural decisions that should be respected
- MCP integrations provide access to issue trackers for fetching story details
- **Specs** are stored in `specs/{FEATURE_DOMAIN}/spec.md` and live permanently with code
- **Plans** are stored in `.plans/{TASK_KEY}-{description}.plan.md` and are discarded after merge
- Specs define State (how the feature works), Plans define Delta (what changes for this task)
- Specs follow Blueprint + Contract structure per ASDLC patterns
- The document will be used by developers and agents to implement/maintain the feature
- **ASDLC patterns**: [The Spec](asdlc://the-spec), [The PBI](asdlc://the-pbi)
- **ASDLC pillars**: **Standardized Parts** (spec/plan as State vs Delta)

### Examples

**ASDLC**: [The Spec](asdlc://the-spec) and [The PBI](asdlc://the-pbi) — Specs define State; plans define Delta for a task.

**Example Story Input (from Jira):**
```
Title: Add user authentication
Description: As a user, I want to log in with OAuth2, so that I can access my account securely.

Acceptance Criteria:
1. User can log in using Google OAuth2
2. User session is maintained for 24 hours
3. Failed login attempts are logged
4. User can log out
5. Session expires after inactivity
```

**Example Plan Document Output:**
```markdown
# Add user authentication (PROJ-123)

## Story
As a user, I want to log in with OAuth2, so that I can access my account securely.

## Context
Currently, users cannot access their accounts. We need to implement OAuth2 authentication to provide secure access. This is part of the user management epic.

## Scope
### In Scope
- OAuth2 login with Google
- Session management
- Logout functionality
- Session expiration

### Out of Scope
- Password-based authentication
- Multi-factor authentication
- Social login providers other than Google

## Acceptance Criteria
1. User can log in using Google OAuth2
2. User session is maintained for 24 hours
3. Failed login attempts are logged
4. User can log out
5. Session expires after inactivity

## Technical Design
### Architecture
- Use OAuth2 library for authentication flow
- Store sessions in Redis
- Middleware for session validation

### Components
- AuthService: Handles OAuth2 flow
- SessionManager: Manages user sessions
- AuthMiddleware: Validates sessions on requests

### Data Model
- User table: id, email, oauth_id, created_at
- Session table: session_id, user_id, expires_at

## Implementation Steps
1. **Set up OAuth2 library**: Install and configure OAuth2 client
   - Files to create: `src/auth/config.ts`
   - Tests: `src/auth/config.test.ts`

2. **Implement AuthService**: Create service for OAuth2 flow
   - Files to create: `src/auth/service.ts`
   - Tests: `src/auth/service.test.ts`

3. **Implement SessionManager**: Create session management
   - Files to create: `src/auth/session.ts`
   - Tests: `src/auth/session.test.ts`

4. **Create AuthMiddleware**: Add middleware for session validation
   - Files to create: `src/auth/middleware.ts`
   - Tests: `src/auth/middleware.test.ts`

5. **Add login/logout endpoints**: Create API endpoints
   - Files to modify: `src/routes/auth.ts`
   - Tests: `src/routes/auth.test.ts`

## Testing
### Unit Tests
- AuthService: OAuth2 flow, token validation
- SessionManager: Session creation, expiration, validation
- AuthMiddleware: Session validation, error handling

### Integration Tests
- Complete login flow
- Session persistence
- Logout flow
- Session expiration

### Test Data
- Mock OAuth2 provider responses
- Test user accounts
- Test session data

## Dependencies
- oauth2-client library
- redis client library
- express (for middleware)

## Status
- [x] Story analyzed
- [x] Codebase reviewed
- [x] Technical design complete
- [x] Implementation steps defined
- [x] Testing strategy defined
- [ ] Ready for implementation
```

**Example Issue Comment (Plan Summary):**
```
## Implementation Plan Created

Plan document: `.plans/PROJ-123-user-authentication.plan.md`

### Approach
- OAuth2 authentication with Google
- Redis-based session management
- Middleware for session validation

### Key Implementation Steps
1. Set up OAuth2 library and configuration
2. Implement AuthService for OAuth2 flow
3. Create SessionManager for session handling
4. Add AuthMiddleware for request validation
5. Create login/logout API endpoints

### Testing Strategy
- Unit tests for each component
- Integration tests for complete flows
- Session expiration and error handling tests

Ready for implementation.
```

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data in documents
   - **AGENTS.md Optional**: Commands work without AGENTS.md. Standards apply regardless of whether AGENTS.md exists.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Prerequisites Must Pass**: Do not proceed if MCP validation fails or story doesn't exist. STOP and report the issue.
3. **Story Validation**: Story must have sufficient detail (description, 3+ acceptance criteria). If missing, STOP and ask for clarification.
4. **Document Type Decision**: Determine if Spec, Plan, or both are needed. If unclear, ask user.
5. **Spec File Naming**: Use format `specs/{FEATURE_DOMAIN}/spec.md` where {FEATURE_DOMAIN} is kebab-case
   - Feature domains are conceptual groupings (e.g., `user-authentication`, `payment-processing`)
   - Ask user for feature domain name if unclear
6. **Plan File Naming**: Use format `.plans/{TASK_KEY}-{kebab-case-description}.plan.md`
   - Example: `PROJ-123-user-authentication.plan.md`
7. **Required Sections**:
   - Spec must include: Feature header, Blueprint (Context, Architecture, Anti-Patterns), Contract (DoD, Guardrails, Scenarios)
   - Plan must include: Story, Context, Scope, Acceptance Criteria, Technical Design, Implementation Steps, Testing, Dependencies, Status
8. **Codebase Analysis**: Must search for similar implementations before designing. Don't reinvent patterns that already exist.
9. **Spec vs Plan Content**:
   - Spec = State (how feature works permanently)
   - Plan = Delta (what changes for this task)
   - Don't duplicate content between them
10. **Same-Commit Rule**: When updating existing spec, remind user to commit spec changes with code changes
11. **File Identification**: Must specify exact file paths. Use relative paths from project root.
12. **Test Strategy**: Must include unit tests, integration tests, test data. Follow existing patterns.
13. **Error Handling**: If analysis reveals blockers or missing information, STOP and ask specific questions.
14. **Document Summary**: Post summary to issue tracker after creation. If posting fails, note it but don't fail the command.

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- Spec guidance: See `specs/README.md` for template and when to create/update specs
- Plan file location: `.plans/{TASK_KEY}-*.plan.md` (referenced in `start-task.md` and `complete-task.md`)
- **Plan File Selection**: If multiple files match the pattern `.plans/{TASK_KEY}-*.plan.md`:
  - Use the most recently modified file (check file modification time)
  - If modification time cannot be determined, use the first file found alphabetically
  - Report which file was selected: "Using plan file: {filename}"
- Story format: User story format ("As a... I want... So that...") as used in `create-task.md`
- File naming: Kebab-case for all filenames
- ASDLC patterns: The Spec, The PBI, Living Specs (available via ASDLC MCP server)

### Output
1. **Spec Document** (if creating spec): Structured markdown file at `specs/{FEATURE_DOMAIN}/spec.md` containing:
   - Blueprint: Context, Architecture, Anti-Patterns
   - Contract: Definition of Done, Regression Guardrails, Scenarios
   - Permanent living specification that evolves with code

2. **Plan Document** (if creating plan): Structured markdown file at `.plans/{TASK_KEY}-{description}.plan.md` containing:
   - Story details and context
   - Technical design and architecture
   - Step-by-step implementation guide
   - Testing strategy
   - Dependencies and status tracking
   - Transient document discarded after merge

3. **Issue Comment**: Summary posted to the issue tracker with:
   - Link to spec/plan file
   - Brief approach summary
   - Key sections or implementation steps

The documents should provide clear guidance for implementation while maintaining appropriate granularity (Spec = permanent contracts, Plan = transient steps).
