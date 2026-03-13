---
name: skill-orchestrator
description: This skill orchestrates programming tasks by analyzing available Claude Code skills and creating execution plans. It should be used when working on any coding task that could benefit from multiple specialized skills. The skill supports two execution modes selected by user - manual (Claude executes with explicit skill references) or delegated (tasks sent to sub-agents with skills).
---

# Skill Orchestrator

This skill provides intelligent orchestration of programming tasks by analyzing available Claude Code skills and creating structured execution plans with skill assignments for each step.

## Purpose

Transform programming requests into actionable plans that leverage the full power of available Claude Code skills. Instead of working in isolation, this skill ensures optimal skill selection and either guides manual execution or delegates to specialized sub-agents.

## When to Use This Skill

This skill should be activated when:
- Receiving a programming or development task that involves multiple steps
- A task could benefit from specialized skills (testing, architecture, frontend, backend, etc.)
- Complex features requiring different expertise domains
- Refactoring or optimization tasks spanning multiple concerns
- Building new applications or significant features
- User explicitly requests orchestrated/planned approach to coding

## Orchestration Workflow

### Phase 1: Task Analysis

Upon receiving a programming task:

1. **Parse the request** to identify:
   - Core objective (what needs to be built/fixed/improved)
   - Technical domain(s) involved (frontend, backend, database, etc.)
   - Complexity level (simple, moderate, complex)
   - Dependencies between subtasks

2. **Scan available skills** by referencing `references/skills_catalog.md` to identify:
   - Directly applicable skills
   - Potentially useful supporting skills
   - Skills that might be needed for quality assurance

### Phase 2: Plan Creation

Create a structured execution plan and **save it to a file** for tracking progress.

#### Plan File Location

Save the plan to a file in the project directory:
- Default filename: `EXECUTION_PLAN.md`
- Alternative: `docs/EXECUTION_PLAN.md` if docs folder exists
- For multiple plans: `EXECUTION_PLAN_[feature-name].md`

#### Plan Format with Checkboxes

Use GitHub-flavored markdown checkboxes for tracking step completion:

```markdown
# Execution Plan: [Task Name]

## Overview
- **Objective**: [Clear statement of goal]
- **Complexity**: [Simple/Moderate/Complex]
- **Total Steps**: [Number]
- **Execution Mode**: [Manual/Delegated] (explain why)
- **Created**: [Date/Time]

## Progress

### Step 1: [Step Name]
- [ ] **Status**: Pending
- **Skill**: `[skill-name]` - [Brief reason for selection]
- **Action**: [What needs to be done]
- **Inputs**: [What this step needs]
- **Outputs**: [What this step produces]
- **Dependencies**: [Previous steps required, if any]

### Step 2: [Step Name]
- [ ] **Status**: Pending
- **Skill**: `[skill-name]`
- **Action**: [What needs to be done]
- **Inputs**: [What this step needs]
- **Outputs**: [What this step produces]
- **Dependencies**: Step 1

---

## Completion Summary
- [ ] All steps completed
- [ ] Quality review passed
- [ ] Final deliverables confirmed
```

#### Updating the Plan File

As steps are executed, update the plan file:
1. Change `- [ ]` to `- [x]` when a step completes
2. Update status from "Pending" to "Completed" or "In Progress"
3. Add notes or issues encountered under each step if relevant

Example of completed step:
```markdown
### Step 1: Design Auth Architecture
- [x] **Status**: Completed
- **Skill**: `backend-architect`
- **Action**: Design authentication flow, token strategy, middleware structure
- **Outputs**: Architecture document created at `docs/auth-architecture.md`
- **Notes**: Chose JWT with refresh tokens for stateless auth
```

### Phase 3: Mode Selection

Present the plan to the user and ask for execution mode preference:

**Manual Mode** (recommended for):
- Learning and understanding the process
- Tasks requiring frequent user input
- Exploratory or experimental work
- Smaller tasks (< 5 steps)

**Delegated Mode** (recommended for):
- Well-defined, larger tasks
- Parallel-executable steps
- Time-sensitive work
- Repetitive patterns across multiple files

Ask user:
> "Plan ready. Execute in **manual mode** (I work step-by-step, showing each skill) or **delegated mode** (sub-agents handle steps in parallel)?"

### Phase 4: Execution

#### Manual Mode Execution

For each step in the plan:

1. **Read the step from the plan file** to get the exact skill name

2. **Verify skill name** - CRITICAL: Before activating any skill:
   - Open the plan file and read the **Skill** field for the current step
   - Copy the exact skill name as written in the plan
   - Do NOT use a different skill or guess the skill name
   - The skill name in the plan is the source of truth

3. **Announce the step and skill**:
   ```
   ## Step N: [Step Name]
   **Using skill**: `[skill-name]` (as specified in plan)
   ```

4. **Activate the skill** using the Skill tool with the EXACT name from the plan
   - Example: If plan says `backend-architect`, use exactly `backend-architect`
   - Do NOT substitute with similar skills (e.g., don't use `backend-development:backend-architect` if plan says `backend-architect`)

5. **Execute the step** following the activated skill's guidance

6. **Update plan file** - Mark step as completed:
   - Change `- [ ]` to `- [x]`
   - Update status to "Completed"
   - Add any relevant notes

7. **Report completion** with outputs produced

8. **Proceed to next step** or ask for user guidance if issues arise

**Important**: Skills in the plan were carefully selected during planning. Always use the specified skill - if a skill is unavailable, notify the user rather than substituting another skill.

#### Delegated Mode Execution

For delegated execution:

1. **Read the plan file** to get all steps and their exact skill names

2. **Identify parallelizable steps** - steps with no dependencies on each other

3. **Verify skill names** - CRITICAL: Before launching any sub-agent:
   - Read the **Skill** field for each step directly from the plan file
   - Use the EXACT skill name as written - do not modify or guess
   - The plan file is the source of truth for skill selection

4. **Launch sub-agents** using the Task tool with appropriate agent types:
   - Include the EXACT skill name from the plan in the prompt
   - Explicitly instruct sub-agent: "You MUST use the skill `[exact-skill-name]` as specified"
   - Specify exact inputs and expected outputs
   - Set clear success criteria

5. **Monitor and coordinate** - collect results and handle any failures

6. **Update plan file** after each step completes:
   - Mark completed steps with `[x]`
   - Add notes from sub-agent execution

7. **Report aggregate results** when all steps complete

Example delegation prompt:
```
Execute [step description].

IMPORTANT: You MUST use the skill `[skill-name]` exactly as specified.
Do NOT substitute with a different skill.

Skill to use: [skill-name]
Inputs: [specific inputs]
Expected output: [what to produce]
Success criteria: [how to verify completion]
```

**Important**: Sub-agents must use the exact skill specified in the plan. If a skill is unavailable, the sub-agent should report failure rather than substituting another skill.

## Skill Selection Guidelines

### By Task Type

| Task Type | Primary Skills | Supporting Skills |
|-----------|---------------|-------------------|
| New feature | `frontend-developer`, `backend-architect` | `typescript-pro`, `test-automator` |
| Bug fix | `debugger` | `code-reviewer` |
| Refactoring | `code-reviewer` | `typescript-pro`, `performance-engineer` |
| API development | `backend-architect`, `api-design-principles` | `graphql-architect` |
| Testing | `test-automator`, `tdd-orchestrator` | `javascript-testing-patterns` |
| Performance | `performance-engineer` | `code-reviewer` |
| Security | `security-auditor` | `code-reviewer` |
| Documentation | `docs-architect`, `tutorial-engineer` | `api-documenter` |
| Deployment | `deployment-engineer` | `security-auditor` |

### Selection Criteria

When choosing between similar skills, prioritize:
1. **Specificity** - more specialized skill over general
2. **Task alignment** - skill description matches task requirements
3. **Quality assurance** - include review/testing skills for critical tasks

## Using Bundled Resources

### References

#### Skills Catalog (`references/skills_catalog.md`)

Complete catalog of available skills organized by category. Load when:
- Analyzing a new task
- Needing to find the best skill for a specific subtask
- User asks what skills are available

```bash
Read references/skills_catalog.md
```

To find skills for a specific domain:
```bash
grep -A 5 "Backend" references/skills_catalog.md
```

#### Orchestration Patterns (`references/orchestration_patterns.md`)

Common patterns for combining skills effectively. Load when:
- Planning complex multi-skill workflows
- Deciding between manual and delegated modes
- Optimizing skill combinations

## Examples

### Example 1: Building a REST API Feature

**User request**: "Add user authentication to my Express.js API"

**Plan saved to**: `EXECUTION_PLAN_auth.md`

```markdown
# Execution Plan: User Authentication API

## Overview
- **Objective**: Implement JWT-based authentication for Express.js API
- **Complexity**: Moderate
- **Total Steps**: 5
- **Execution Mode**: Manual (security-critical, needs review)
- **Created**: 2024-01-15 10:30

## Progress

### Step 1: Design Auth Architecture
- [ ] **Status**: Pending
- **Skill**: `backend-architect` - Architecture design expertise
- **Action**: Design authentication flow, token strategy, middleware structure
- **Inputs**: Project requirements, existing codebase structure
- **Outputs**: Architecture document, API endpoints specification
- **Dependencies**: None

### Step 2: Implement Auth Endpoints
- [ ] **Status**: Pending
- **Skill**: `nodejs-backend-patterns` - Node.js implementation patterns
- **Action**: Create login, register, refresh token endpoints
- **Inputs**: Architecture from Step 1
- **Outputs**: Auth route handlers, JWT utilities
- **Dependencies**: Step 1

### Step 3: Create Auth Middleware
- [ ] **Status**: Pending
- **Skill**: `typescript-pro` - TypeScript expertise
- **Action**: Implement JWT verification middleware
- **Inputs**: JWT utilities from Step 2
- **Outputs**: Auth middleware, type definitions
- **Dependencies**: Step 2

### Step 4: Security Review
- [ ] **Status**: Pending
- **Skill**: `security-auditor` - Security audit capabilities
- **Action**: Audit implementation for vulnerabilities
- **Inputs**: All auth code from Steps 2, 3
- **Outputs**: Security report, fixes applied
- **Dependencies**: Steps 2, 3

### Step 5: Write Tests
- [ ] **Status**: Pending
- **Skill**: `test-automator` - Test automation expertise
- **Action**: Create auth endpoint tests
- **Inputs**: Implemented endpoints
- **Outputs**: Test suite, coverage report
- **Dependencies**: Steps 2, 3

---

## Completion Summary
- [ ] All steps completed
- [ ] Security review passed
- [ ] Test coverage > 80%
```

### Example 2: Frontend Component Development

**User request**: "Create a dashboard with charts and data tables"

**Plan saved to**: `EXECUTION_PLAN_dashboard.md`

```markdown
# Execution Plan: Dashboard Component

## Overview
- **Objective**: Build interactive dashboard with visualizations
- **Complexity**: Moderate
- **Total Steps**: 4
- **Execution Mode**: Delegated (components can be built in parallel)
- **Created**: 2024-01-15 14:00

## Progress

### Step 1: Dashboard Layout
- [ ] **Status**: Pending | ⚡ Parallelizable with Steps 2, 3
- **Skill**: `frontend-developer` - React/frontend expertise
- **Action**: Create responsive dashboard grid layout
- **Inputs**: Design requirements
- **Outputs**: Dashboard container component
- **Dependencies**: None

### Step 2: Chart Components
- [ ] **Status**: Pending | ⚡ Parallelizable with Steps 1, 3
- **Skill**: `frontend-developer` - React/frontend expertise
- **Action**: Implement chart components using charting library
- **Inputs**: Data schema for charts
- **Outputs**: Chart components with props interface
- **Dependencies**: None

### Step 3: Data Table Component
- [ ] **Status**: Pending | ⚡ Parallelizable with Steps 1, 2
- **Skill**: `frontend-developer` - React/frontend expertise
- **Action**: Create sortable, filterable data table
- **Inputs**: Table data structure
- **Outputs**: DataTable component
- **Dependencies**: None

### Step 4: Integration & Polish
- [ ] **Status**: Pending
- **Skill**: `frontend-design` - UI/UX design expertise
- **Action**: Integrate components, add styling, ensure responsiveness
- **Inputs**: All components from Steps 1-3
- **Outputs**: Complete dashboard
- **Dependencies**: Steps 1, 2, 3

---

## Completion Summary
- [ ] All steps completed
- [ ] Responsive design verified
- [ ] Cross-browser testing passed
```

## Best Practices

1. **Always save the plan to a file** using the Write tool before execution
2. **Present the plan and file location** to the user before execution
3. **Get explicit mode confirmation** from user
4. **Update the plan file** as steps complete (change `[ ]` to `[x]`)
5. **Include quality assurance steps** (testing, review) in plans
6. **Mark skill usage clearly** at each step
7. **Report progress** after each step completion
8. **Handle failures gracefully** - propose alternatives if a step fails, update plan with notes
9. **Parallelize when possible** in delegated mode to save time
10. **Keep the plan file as source of truth** for tracking overall progress

## Troubleshooting

### Skill Not Available

If a planned skill is not available:
1. Check `references/skills_catalog.md` for alternatives
2. Propose substitute skill to user
3. Proceed with manual implementation if no suitable skill exists

### Step Failure

If a step fails:
1. Report the failure with details
2. Analyze cause (missing dependencies, incorrect inputs, etc.)
3. Propose fix or alternative approach
4. Get user confirmation before proceeding

### Complex Dependencies

For tasks with complex dependencies:
1. Create a dependency graph
2. Identify critical path
3. Suggest phased approach if needed
4. Consider breaking into multiple orchestration sessions
