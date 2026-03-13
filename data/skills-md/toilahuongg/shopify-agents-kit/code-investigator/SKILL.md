---
name: code-investigator
description: Comprehensive code investigation and audit tool. Discovers all project features, then dispatches parallel subagents to analyze issues, risks, dead code, missing functionality, and redundancies. Produces a prioritized risk report. Use this skill when the user asks to "investigate code", "audit project", "find risks", "check code quality", "analyze codebase", "what's wrong with this code", "project health check", "code review entire project", "find dead code", "find redundant code", or any request for a thorough codebase analysis.
---

# Code Investigator

Systematic codebase investigation using parallel subagents. Discover all features, analyze risks, and produce a prioritized action report.

## Workflow

### Phase 1: Feature Discovery

Use the Task tool with `subagent_type=Explore` to map the entire project:

1. Identify project type (framework, language, architecture pattern)
2. List all features/modules with file locations
3. Map dependencies (package.json, requirements.txt, go.mod, etc.)
4. Identify entry points, routes, API endpoints
5. Note configuration files, environment setup, CI/CD

Output a structured feature inventory:

```
## Feature Inventory
| # | Feature/Module | Files | Description |
|---|---------------|-------|-------------|
| 1 | Authentication | src/auth/* | OAuth + session |
| 2 | Product CRUD  | src/products/* | Admin API |
...
```

Present this inventory to the user before proceeding to Phase 2.

### Phase 2: Parallel Investigation

Launch **multiple Task subagents in a single message** to investigate concurrently. Each subagent focuses on one investigation area. See [references/investigation-areas.md](references/investigation-areas.md) for detailed checklists per area.

Required subagents (launch all in parallel):

| Subagent | Type | Focus |
|----------|------|-------|
| Security Auditor | `tech-lead` | Vulnerabilities, injection risks, auth gaps, secret exposure |
| Dead Code Detector | `Explore` | Unused exports, unreachable code, orphan files, unused dependencies |
| Architecture Reviewer | `tech-lead` | Pattern violations, circular deps, coupling issues, missing abstractions |
| Error & Edge Case Analyzer | `Explore` | Missing error handling, unhandled promises, race conditions |
| Dependency Auditor | `Bash` | `npm audit`, outdated packages, license issues, duplicate deps |
| Test Coverage Analyzer | `Explore` | Missing tests, untested critical paths, test quality |

Optional subagents (based on project type):

| Subagent | Type | When |
|----------|------|------|
| Performance Profiler | `tech-lead` | Web apps, APIs with DB queries |
| TypeScript Strictness | `Explore` | TS projects with `any` usage |
| API Contract Checker | `Explore` | Projects with REST/GraphQL APIs |
| Accessibility Auditor | `Explore` | Frontend projects |

Each subagent prompt must include:
- The feature inventory from Phase 1
- Specific checklist items from references/investigation-areas.md
- Instruction to rate each finding: CRITICAL / HIGH / MEDIUM / LOW
- Instruction to provide file path and line number for each finding

### Phase 3: Report Synthesis

Collect all subagent results and compile into a single prioritized report.

#### Report Structure

```markdown
# Code Investigation Report
**Project:** [name] | **Date:** [date] | **Files Analyzed:** [count]

## Executive Summary
[2-3 sentences: overall health, top concerns, immediate actions needed]

## Critical Findings (Act Immediately)
| # | Finding | Category | File:Line | Impact | Recommendation |
|---|---------|----------|-----------|--------|----------------|

## High Priority
| # | Finding | Category | File:Line | Impact | Recommendation |
|---|---------|----------|-----------|--------|----------------|

## Medium Priority
| # | Finding | Category | File:Line | Impact | Recommendation |
|---|---------|----------|-----------|--------|----------------|

## Low Priority / Improvements
| # | Finding | Category | File:Line | Impact | Recommendation |
|---|---------|----------|-----------|--------|----------------|

## Dead Code & Redundancies
| # | Item | Type | File:Line | Safe to Remove? |
|---|------|------|-----------|-----------------|

## Missing Functionality
| # | Gap | Why It Matters | Suggested Implementation |
|---|-----|----------------|--------------------------|

## Dependency Health
| Package | Current | Latest | Risk | Action |
|---------|---------|--------|------|--------|

## Metrics Summary
- Total findings: X (Critical: X, High: X, Medium: X, Low: X)
- Dead code items: X
- Missing features: X
- Vulnerable dependencies: X
```

#### Sorting Rules

1. **CRITICAL**: Security vulnerabilities, data loss risks, crashes in production
2. **HIGH**: Bugs likely to affect users, missing auth checks, unhandled errors in critical paths
3. **MEDIUM**: Code smells, minor security issues, performance concerns, missing tests
4. **LOW**: Style issues, minor refactoring opportunities, nice-to-have improvements

## Key Guidelines

- Never guess - always verify by reading actual code before reporting a finding
- Include file path and line number for every finding
- Distinguish between confirmed issues and potential concerns
- Do not report style preferences as issues unless they cause real problems
- Group related findings to avoid duplicate reports
- If a subagent finds nothing in its area, report that as a positive signal
