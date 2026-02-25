---
name: plan
description: "[Planning] Use when you need to plan technical solutions that are scalable, secure, and maintainable."
license: MIT
---

# Planning

> **CRITICAL:** Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools needed for plan creation. Use this skill's workflow instead.
> **Planning is collaborative:** Validate plan, ask user to confirm, surface decision questions with recommendations.

Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation.

## Summary

**Goal:** Create detailed technical implementation plans through research, codebase analysis, and solution design.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Research & Analysis | Spawn parallel researcher agents; skip if reports provided |
| 2 | Solution Design | Architecture decisions, trade-offs, approach selection |
| 3 | Implementation Plan | Detailed phases with file ownership and task breakdown |
| 4 | Validation | Review plan quality, surface decision questions |
| 5 | User Approval | Present plan and wait for confirmation before coding |

**Key Principles:**
- Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools
- Planning is collaborative: validate, ask user to confirm, surface decisions with recommendations
- Honor YAGNI, KISS, DRY in all designs

## When to Use

Use this skill when:

- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements
- Assessing technical trade-offs

## Core Responsibilities & Rules

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

### 1. Research & Analysis (**Skip if:** Provided with researcher reports)


**When to skip:** If provided with researcher reports, skip this phase.

#### Core Activities

**Parallel Researcher Agents**

- Spawn multiple `researcher` agents in parallel to investigate different approaches
- Wait for all researcher agents to report back before proceeding
- Each researcher investigates a specific aspect or approach

**Sequential Thinking**

- Use `sequential-thinking` skill for dynamic and reflective problem-solving
- Structured thinking process for complex analysis
- Enables multi-step reasoning with revision capability

**Documentation Research**

- Use `docs-seeker` skill to read and understand documentation
- Research plugins, packages, and frameworks
- Find latest technical documentation using llms.txt standard

**GitHub Analysis**

- Use `gh` command to read and analyze:
  - GitHub Actions logs
  - Pull requests
  - Issues and discussions
- Extract relevant technical context from GitHub resources

**Remote Repository Analysis**
When given GitHub repository URL, generate fresh codebase summary:

```bash
# usage:
repomix --remote <github-repo-url>
# example:
repomix --remote https://github.com/mrgoonie/human-mcp
```

**Debugger Delegation**

- Delegate to `debugger` agent for root cause analysis
- Use when investigating complex issues or bugs
- Debugger agent specializes in diagnostic tasks

#### Best Practices

- Research breadth before depth
- Document findings for synthesis phase
- Identify multiple approaches for comparison
- Consider edge cases during research
- Note security implications early

### 2. Codebase Understanding (**Skip if:** Provided with scout reports)


**When to skip:** If provided with scout reports, skip this phase.

#### Core Activities

**Parallel Scout Agents**

- Use `/scout-ext` (preferred) or `/scout` (fallback) slash command to search the codebase for files needed to complete the task
- Each scout locates files needed for specific task aspects
- Wait for all scout agents to report back before analysis
- Efficient for finding relevant code across large codebases

**Essential Documentation Review**
ALWAYS read these files first:

1. **`./docs/development-rules.md`** (IMPORTANT)
   - File Name Conventions
   - File Size Management
   - Development rules and best practices
   - Code quality standards
   - Security guidelines

2. **`./docs/codebase-summary.md`**
   - Project structure and current status
   - High-level architecture overview
   - Component relationships

3. **`./docs/code-standards.md`**
   - Coding conventions and standards
   - Language-specific patterns
   - Naming conventions

4. **`./docs/design-guidelines.md`** (if exists)
   - Design system guidelines
   - Branding and UI/UX conventions
   - Component library usage

**Environment Analysis**

- Review development environment setup
- Analyze dotenv files and configuration
- Identify required dependencies
- Understand build and deployment processes

**Pattern Recognition**

- Study existing patterns in codebase
- Identify conventions and architectural decisions
- Note consistency in implementation approaches
- Understand error handling patterns

**Integration Planning**

- Identify how new features integrate with existing architecture
- Map dependencies between components
- Understand data flow and state management
- Consider backward compatibility

#### Best Practices

- Start with documentation before diving into code
- Use scouts for targeted file discovery
- Document patterns found for consistency
- Note any inconsistencies or technical debt
- Consider impact on existing features

### 3. Solution Design


#### Core Principles

- **YAGNI** (You Aren't Gonna Need It) - Don't add functionality until necessary
- **KISS** (Keep It Simple, Stupid) - Prefer simple solutions over complex ones
- **DRY** (Don't Repeat Yourself) - Avoid code duplication

#### Design Activities

**Technical Trade-off Analysis**

- Evaluate multiple approaches for each requirement
- Compare pros and cons of different solutions
- Consider short-term vs long-term implications
- Balance complexity with maintainability
- Assess development effort vs benefit
- Recommend optimal solution based on current best practices

**Security Assessment**

- Identify potential vulnerabilities during design phase
- Consider authentication and authorization requirements
- Assess data protection needs
- Evaluate input validation requirements
- Plan for secure configuration management
- Address OWASP Top 10 concerns
- Consider API security (rate limiting, CORS, etc.)

**Performance & Scalability**

- Identify potential bottlenecks early
- Consider database query optimization needs
- Plan for caching strategies
- Assess resource usage (memory, CPU, network)
- Design for horizontal/vertical scaling
- Plan for load distribution
- Consider asynchronous processing where appropriate

**Edge Cases & Failure Modes**

- Think through error scenarios
- Plan for network failures
- Consider partial failure handling
- Design retry and fallback mechanisms
- Plan for data consistency
- Consider race conditions
- Design for graceful degradation

**Architecture Design**

- Create scalable system architectures
- Design for maintainability
- Plan component interactions
- Design data flow
- Consider microservices vs monolith trade-offs
- Plan API contracts
- Design state management

#### Best Practices

- Document design decisions and rationale
- Consider both technical and business requirements
- Think through the entire user journey
- Plan for monitoring and observability
- Design with testing in mind
- Consider deployment and rollback strategies

### 4. Plan Creation & Organization


#### Directory Structure

**Plan Location**
Use `Plan dir:` from `## Naming` section injected by hooks. This is the full computed path.

**Example:** `plans/251101-1505-authentication/` or `ai_docs/feature/MRR-1453/`

**File Organization**

```
{plan-dir}/                                    # From `Plan dir:` in ## Naming
├── research/
│   ├── researcher-XX-report.md
│   └── ...
├── reports/
│   ├── scout-report.md
│   ├── researcher-report.md
│   └── ...
├── plan.md                                    # Overview access point
├── phase-01-setup-environment.md              # Setup environment
├── phase-02-implement-database.md             # Database models
├── phase-03-implement-api-endpoints.md        # API endpoints
├── phase-04-implement-ui-components.md        # UI components
├── phase-05-implement-authentication.md       # Auth & authorization
├── phase-06-implement-profile.md              # Profile page
└── phase-07-write-tests.md                    # Tests
```

#### Active Plan State Tracking

Check the `## Plan Context` section injected by hooks:

- **"Plan: {path}"** = Active plan - use for reports
- **"Suggested: {path}"** = Branch-matched, hint only - do NOT auto-use
- **"Plan: none"** = No active plan

**Pre-Creation Check:**

1. If "Plan:" shows a path → ask "Continue with existing plan? [Y/n]"
2. If "Suggested:" shows a path → inform user (hint only, do NOT auto-use)
3. If "Plan: none" → create new plan using naming from `## Naming` section

**After Creating Plan:**

```bash
# Update session state so subagents get the new plan context:
node .claude/scripts/set-active-plan.cjs {plan-dir}
```

**Report Output Rules:**

1. Use `Report:` and `Plan dir:` from `## Naming` section
2. Active plans use plan-specific reports path
3. Suggested plans use default reports path to prevent old plan pollution

#### File Structure

**Overview Plan (plan.md)**

**IMPORTANT:** All plan.md files MUST include YAML frontmatter. See output standards (section 5) for schema.

**Example plan.md structure:**

```markdown
---
title: "Feature Implementation Plan"
description: "Add user authentication with OAuth2 support"
status: pending
priority: P1
effort: 8h
issue: 123
branch: kai/feat/oauth-auth
tags: [auth, backend, security]
created: 2025-12-16
---

# Feature Implementation Plan

## Overview

Brief description of what this plan accomplishes.

## Phases

| #   | Phase          | Status  | Effort | Link                            |
| --- | -------------- | ------- | ------ | ------------------------------- |
| 1   | Setup          | Pending | 2h     | [phase-01](./phase-01-setup.md) |
| 2   | Implementation | Pending | 4h     | [phase-02](./phase-02-impl.md)  |
| 3   | Testing        | Pending | 2h     | [phase-03](./phase-03-test.md)  |

## Dependencies

- List key dependencies here
```

**Guidelines:**

- Keep generic and under 80 lines
- List each phase with status/progress
- Link to detailed phase files
- Key dependencies

**Phase Files (phase-XX-name.md)**
Fully respect the `./docs/development-rules.md` file.
Each phase file should contain:

- **Context Links** - Links to related reports, files, documentation
- **Overview** - Priority, current status, brief description
- **Key Insights** - Important findings from research, critical considerations
- **Requirements** - Functional and non-functional requirements
- **Architecture** - System design, component interactions, data flow
- **Related Code Files** - Files to modify, create, delete
- **Implementation Steps** - Detailed, numbered steps with specific instructions
- **Todo List** - Checkbox list for tracking
- **Success Criteria** - Definition of done, validation methods
- **Risk Assessment** - Potential issues, mitigation strategies
- **Security Considerations** - Auth/authorization, data protection
- **Next Steps** - Dependencies, follow-up tasks

### 5. Task Breakdown & Output Standards


#### Plan File Format

**YAML Frontmatter (Required for plan.md)**

All `plan.md` files MUST include YAML frontmatter at the top:

```yaml
---
title: "{Brief plan title}"
description: "{One-sentence summary for card preview}"
status: pending  # pending | in-progress | completed | cancelled
priority: P2     # P1 (High) | P2 (Medium) | P3 (Low)
effort: 4h       # Estimated total effort
issue: 74        # GitHub issue number (if applicable)
branch: kai/feat/feature-name
tags: [frontend, api]  # Category tags
created: 2025-12-16
---
```

**Auto-Population Rules**

When creating plans, auto-populate these fields:

- **title**: Extract from task description
- **description**: First sentence of Overview section
- **status**: Always `pending` for new plans
- **priority**: From user request or default `P2`
- **effort**: Sum of phase estimates
- **issue**: Parse from branch name or context
- **branch**: Current git branch (`git branch --show-current`)
- **tags**: Infer from task keywords (e.g., frontend, backend, api, auth)
- **created**: Today's date in YYYY-MM-DD format

**Tag Vocabulary (Recommended)**

Use these predefined tags for consistency:

- **Type**: `feature`, `bugfix`, `refactor`, `docs`, `infra`
- **Domain**: `frontend`, `backend`, `database`, `api`, `auth`
- **Scope**: `critical`, `tech-debt`, `experimental`

#### Task Breakdown

- Transform complex requirements into manageable, actionable tasks
- Each task independently executable with clear dependencies
- Prioritize by dependencies, risk, business value
- Eliminate ambiguity in instructions
- Include specific file paths for all modifications
- Provide clear acceptance criteria per task

**File Management**
List affected files with:

- Full paths (not relative)
- Action type (modify/create/delete)
- Brief change description
- Dependencies on other changes
- Fully respect the `./docs/development-rules.md` file.

#### Workflow Process

1. **Initial Analysis** → Read docs, understand context
2. **Research Phase** → Spawn researchers in parallel, investigate approaches
3. **Synthesis** → Analyze reports, identify optimal solution
4. **Design Phase** → Create architecture, implementation design
5. **Plan Documentation** → Write comprehensive plan in Markdown
6. **Review & Refine** → Ensure completeness, clarity, actionability

#### Output Requirements

**What Planners Do**

- Create plans ONLY (no implementation)
- Provide plan file path and summary
- Self-contained plans with necessary context
- Code snippets/pseudocode when clarifying
- Multiple options with trade-offs when appropriate
- Fully respect the `./docs/development-rules.md` file.

**Writing Style**
**IMPORTANT:** Sacrifice grammar for concision

- Focus clarity over eloquence
- Use bullets and lists
- Short sentences
- Remove unnecessary words
- Prioritize actionable info

**Unresolved Questions**
**IMPORTANT:** List unresolved questions at end

- Questions needing clarification
- Technical decisions requiring input
- Unknowns impacting implementation
- Trade-offs requiring business decisions

#### Quality Standards

**Thoroughness**

- Thorough and specific in research/planning
- Consider edge cases, failure modes
- Think through entire user journey
- Document all assumptions

**Maintainability**

- Consider long-term maintainability
- Design for future modifications
- Document decision rationale
- Avoid over-engineering
- Fully respect the `./docs/development-rules.md` file.

**Research Depth**

- When uncertain, research more
- Multiple options with clear trade-offs
- Validate against best practices
- Consider industry standards

**Security & Performance**

- Address all security concerns
- Identify performance implications
- Plan for scalability
- Consider resource constraints

**Implementability**

- Detailed enough for junior developers
- Validate against existing patterns
- Ensure codebase standards consistency
- Provide clear examples

**Remember:** Plan quality determines implementation success. Be comprehensive, consider all solution aspects.

## MANDATORY: Plan Collaboration Protocol (READ THIS)

- **Do NOT use `EnterPlanMode` tool** — it blocks Write/Edit/Task tools needed to create plan files and launch subagents
- **Do NOT start implementing** — plan only, wait for user approval
- **ALWAYS validate:** After plan creation, execute `/plan-review` to validate the plan
- **ALWAYS confirm:** Ask user to review and approve the plan using `AskUserQuestion` with a recommendation
- **ALWAYS surface decisions:** Use `AskUserQuestion` with recommended options for key architectural/design decisions
- **Planning = Collaboration:** The plan is shaped by user input — never treat it as a unilateral output
- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end
- Sacrifice grammar for concision. List unresolved questions at the end
