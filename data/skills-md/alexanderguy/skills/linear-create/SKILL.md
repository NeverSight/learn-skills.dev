---
name: linear-create
description: Create well-structured Linear issues, projects, or initiatives
argument-hint: "[description] [--from-doc]"
---

# Linear Create

Use this skill to create properly structured Linear artifacts. Based on the scope of work, this skill will create the appropriate combination of issues, projects, and/or initiatives.

## Prerequisites

Before doing anything else, verify the `linear` subagent is available by checking if it appears in your available agent types. If it is not available, inform the user:

> The Linear integration is not available. Please ensure the Linear MCP server is configured and try again.

Do not proceed with any other phases until this check passes.

## Phase 1: Document Discovery

When the user provides `--from-doc` or mentions a planning document, search for scribe-managed documents:

1. Look for `PRODUCT.md`, `ARCHITECTURE.md`, `IMPLEMENTATION.md` in:
   - Repository root
   - `docs/` directory

2. If no documents are found, ask the user:
   > I couldn't find any planning documents. Do you have a document you'd like me to reference?

3. When a document is found, read it and extract:
   - Features or work items mentioned
   - Technical context and constraints
   - Scope indicators (timeline mentions, complexity signals)

Use extracted information to:
- Pre-populate issue descriptions with relevant context
- Propose appropriate artifact types based on scope
- Ask targeted follow-up questions for gaps not covered by the document

## Phase 2: Analyze Input

Determine what the user wants to create:

1. **Explicit request**: User specifies artifact type ("create an issue for...", "create a project for...")
2. **From document**: User provides `--from-doc` to extract work items from planning documents
3. **Freeform**: User describes work without specifying type

For freeform input, estimate the scope:

| Scope | Duration | Artifact |
|-------|----------|----------|
| Small | 1-3 days | Single issue |
| Medium | 1-2 weeks | Project with issues |
| Large | Quarter+ | Initiative with projects |

Present your assessment to the user and confirm before proceeding.

## Phase 3: Interview

If information is missing, ask targeted questions. Keep interviews brief and focused.

### For Issues

Required information:
- What problem does this solve or what value does it add?
- How will we know it's done? (acceptance criteria)

Optional:
- Are there technical constraints or dependencies?
- Which team should own this?

### For Projects

Required information:
- What is the goal/outcome of this project?
- What is the target timeframe?
- Who should lead this project?

Optional:
- What teams are involved?
- What are the key milestones?

### For Initiatives

Required information:
- What strategic objective does this serve?
- Who is the executive owner?
- What projects should be included?

## Phase 4: Draft Content

Create drafts following these conventions:

### Issue Format

**Title**: Clear and actionable. Verb phrases are preferred, but sentences or noun phrases are acceptable when they provide clarity.

- Good: "Add retry logic for failed API calls"
- Good: "Fix race condition in transaction verification"
- Good: "Create market validation track for <product-name>"
- Bad: "API retry" (too vague)
- Bad: "Bug in transactions" (not actionable)

**Description**:

```
# Background

<Context and what triggered this work. Optional for simple tasks.>

# Outcome

<What success looks like, with checkboxes for specific conditions>

- [ ] <Specific, testable condition>
- [ ] <Another condition>
```

For simple tasks, you can omit `# Background` and use only `# Outcome` with checkboxes.

**Labels and Priority**:

- Set priority based on urgency and impact
- Apply labels for categorization (e.g., bug, feature, tech-debt) if the workspace uses them
- Ask the user about priority and labels if not specified

When appropriate, use subsections under `# Outcome` to organize related items:

```
# Outcome

## Questions

- [ ] What are the key takeaways?
- [ ] Which parts apply to our strategy?

## Tasks

- [ ] Document findings
- [ ] Present to team
```

### Project Format

**Name**: Outcome-focused description
- Good: "User authentication with SSO support"
- Good: "Get 10 customer leads for <product-name> through direct outreach"
- Bad: "Auth work"

**Description**: Goal, scope, and any constraints.

For validation or experiment projects, use the Hypothesis/Experiment/Steps pattern:

```
Hypothesis - <What you believe to be true>

Experiment
<Experiment name>

* <Step 1>
* <Step 2>
* <Step 3>
```

**Milestones**: Key checkpoints showing progression toward the goal. Examples:

- Completion states: "Target list ready", "Outreach completed", "Analysis complete"
- Phase labels: "MVP", "Full implementation", "Polish and launch"

### Initiative Format

**Name**: Strategic objective

**Description**: Include as much information as needed to convey the business goal and how success will be measured. If unsure what to include, prompt the user for guidance.

## Phase 5: Review and Adjust

Present the complete draft to the user:

```
I propose creating:

**Project**: Add user authentication
- Lead: <to be assigned>
- Target: <target-quarter>
- Milestones:
  1. Basic auth flow complete
  2. SSO integration complete

**Issues**:
1. "Set up authentication database schema"
2. "Implement login/logout flow"
3. "Integrate SSO provider"
4. "Add session management"
   - Blocked by: #2

Would you like to adjust anything before I create these?
```

Allow the user to:
- Adjust titles or descriptions
- Change the structure (e.g., "make #3 and #4 one issue")
- Add or remove items
- Specify assignees or teams

## Phase 6: Create in Linear

### Workspace Discovery

Before creating artifacts, query the Linear workspace:

- **Teams**: Always query available teams and ask the user which team should own issues or projects
- **Projects**: Query existing projects if the user mentions adding to an existing project
- **Initiatives**: Query existing initiatives if linking to one

Example queries:

```
Task(description="Query Linear teams", prompt="List available teams in the workspace", subagent_type="linear")
Task(description="Query Linear projects", prompt="List active projects in team <team-name>", subagent_type="linear")
Task(description="Query Linear initiatives", prompt="List initiatives", subagent_type="linear")
```

Present options to the user when multiple choices exist.

### Creating Artifacts

After user approval, create artifacts using the `linear` subagent:

1. **Create container first** (initiative or project)
2. **Create issues** in dependency order
3. **Set blocking relationships** between issues
4. **Add issues to project** (if applicable)
5. **Add projects to initiative** (if applicable)

Example subagent calls:

```
Task(description="Create Linear project", prompt="Create a project titled 'User authentication with SSO support' with target date <target-date>, description: '<description>'", subagent_type="linear")

Task(description="Create Linear issue", prompt="Create an issue titled 'Set up authentication database schema' with description: '<desc>' and acceptance criteria: '<ac>', add to project <project-id>", subagent_type="linear")

Task(description="Set issue dependency", prompt="Set issue <issue-B-id> as blocked by <issue-A-id>", subagent_type="linear")
```

Report created artifacts to the user with their URLs.

## Error Handling

If Linear creation fails:

1. Report the error to the user with any details provided by the API
2. List what was successfully created before the failure (with URLs if available)
3. Do not proceed with dependent artifacts if a parent fails (e.g., don't create issues if project creation failed)
4. Ask if they want to retry or adjust the request

## Quality Reminders

- Issues should be self-contained and handoff-ready at any moment
- A single issue should take no more than 2-3 days to implement
- Use many tickets if needed for clarity; they're cheap
- Status updates in tickets reduce interruptions

If an issue looks like it will take more than 3 days, suggest breaking it down.

## Common Patterns

### Bug Report to Issue

```
User: "The login page crashes when you enter special characters"

Issue:
  Title: Fix login page crash on special character input
  Description:
    # Background

    Login page crashes when users enter special characters in the
    username or password field.

    Steps to reproduce:
    1. Navigate to /login
    2. Enter "user@test" in username
    3. Page crashes

    # Outcome

    - [ ] Special characters in username field do not cause crash
    - [ ] Special characters in password field do not cause crash
    - [ ] Input is properly sanitized before processing
```

### Feature Request to Project and Issues

```
User: "We need to add dark mode to the application"

Project: Add dark mode theme support
  Target: 2 weeks
  Milestones:
    1. Theme infrastructure complete
    2. All components themed

Issues:
  1. "Add theme context and toggle component"
  2. "Define dark mode color palette"
  3. "Update core components for theme support"
     - Blocked by: #1, #2
  4. "Add theme persistence to user preferences"
     - Blocked by: #1
```

### Validation Project

```
User: "We need to validate if customers want our new <product-name> product"

Project: Get 10 customer leads for <product-name> through direct outreach
  Lead: <to be assigned>
  Target: 2 weeks
  Description:
    Hypothesis - Teams we know and can reach out to have a need for <product-name>.

    Experiment
    Direct Outreach

    - [ ] Create list of targets
    - [ ] Create collateral if needed
    - [ ] Create strategy for outreach including any templates
    - [ ] Execute outreach
    - [ ] Conduct customer interviews
    - [ ] Analyze results

  Milestones:
    1. Target list and collateral ready
    2. Outreach completed
    3. Customer interviews recorded
    4. Analysis complete

Issues:
  1. "Create target list for <product-name> outreach"
  2. "Create outreach collateral and templates"
  3. "Execute outreach campaign"
     - Blocked by: #1, #2
  4. "Conduct and record customer interviews"
     - Blocked by: #3
  5. "Analyze results and present findings"
     - Blocked by: #4
```

### Strategic Goal to Initiative

```
User: "We need to expand our platform to support enterprise customers"

Initiative: Enterprise platform expansion
  Owner: <executive-owner>
  Target: <target-quarter>

Projects:
  1. "Multi-tenant architecture" - Isolate customer data and resources
  2. "Enterprise SSO integration" - Support SAML and OIDC providers
  3. "Admin dashboard" - Self-service management for enterprise admins
  4. "Audit logging" - Compliance-ready activity tracking
```

### Planning Document to Issues

```
User: "Create issues from our product doc" or "--from-doc"

[Skill searches for PRODUCT.md, ARCHITECTURE.md, IMPLEMENTATION.md]
[Finds PRODUCT.md with feature descriptions]

Skill: I found PRODUCT.md which describes the following features:
  - User authentication with SSO
  - Usage metrics dashboard
  - Export functionality

Based on the document, I propose:

**Project**: User authentication with SSO support
  (From PRODUCT.md: "Users need secure login with enterprise SSO...")

**Issues**:
  1. "Implement basic email/password authentication"
     # Background
     From PRODUCT.md: Users need secure login...

     # Outcome
     - [ ] Users can register with email/password
     - [ ] Users can log in and log out

  2. "Integrate SAML SSO provider"
     ...

Which features would you like me to create issues for?
```
