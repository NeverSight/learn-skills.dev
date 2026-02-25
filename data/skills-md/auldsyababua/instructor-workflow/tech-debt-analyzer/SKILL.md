---
name: tech-debt-analyzer
description: This skill should be used when analyzing technical debt in a codebase, documenting code quality issues, creating technical debt registers, or assessing code maintainability. Use this for identifying code smells, architectural issues, dependency problems, missing documentation, security vulnerabilities, and creating comprehensive technical debt documentation.
---

# Technical Debt Analyzer

## Overview

Systematically identify, analyze, document, and track technical debt in JavaScript/TypeScript codebases. This skill provides automated analysis tools, comprehensive debt categorization frameworks, and documentation templates to maintain a technical debt register.

## Core Workflow

### 1. Automated Analysis

Run automated scripts to detect technical debt indicators across the codebase.

#### Code Smell Detection

Identify code quality issues using the automated detector:

```bash
python3 scripts/detect_code_smells.py src --output markdown
```

The script analyzes:
- **Large Files:** Files exceeding 500 lines
- **Complex Functions:** High cyclomatic complexity (>10) or long functions (>50 lines)
- **Debt Markers:** TODO, FIXME, HACK, XXX, BUG comments
- **Console Statements:** Debug statements left in code
- **Weak Typing:** Use of `any` type in TypeScript
- **Long Parameters:** Functions with >5 parameters
- **Deep Nesting:** Code nested >4 levels deep
- **Magic Numbers:** Hardcoded numeric values

**Output Example:**
```
# Technical Debt Analysis Report

**Files Analyzed:** 127
**Total Lines:** 15,432
**Total Issues:** 89

### Issues by Severity
- HIGH: 23
- MEDIUM: 41
- LOW: 25

## Large Files (12 issues)
### High Priority
- src/components/Dashboard.tsx (847 lines): File too large
- src/services/DataProcessor.ts (623 lines): File too large
...
```

#### Dependency Analysis

Examine dependencies for debt indicators:

```bash
python3 scripts/analyze_dependencies.py package.json
```

The script identifies:
- **Deprecated Packages:** Known deprecated libraries (request, tslint, etc.)
- **Duplicate Functionality:** Multiple packages serving same purpose
- **Version Issues:** Overly loose or strict version constraints
- **Security Concerns:** Known vulnerable packages (requires audit data)

**Output Example:**
```
# Dependency Analysis Report

**Package:** expense-tracker
**Dependencies:** 24
**Dev Dependencies:** 18
**Total Issues:** 7

## Deprecated/Outdated Packages (3)
### request [HIGH]
Using deprecated package - use axios, node-fetch, or got instead
- Current version: ^2.88.0

## Duplicate Functionality (2)
### HTTP client [MEDIUM]
Multiple packages for HTTP client: axios, node-fetch
```

### 2. Manual Code Review

Complement automated analysis with manual review for issues that require human judgment.

#### Review Focus Areas

**Architectural Debt:**
- Tight coupling between components
- Missing abstractions
- Poor separation of concerns
- Circular dependencies

**Test Debt:**
- Missing test coverage for critical paths
- Fragile tests coupled to implementation
- No integration or E2E tests
- Slow test execution

**Documentation Debt:**
- Missing README or setup instructions
- No architecture documentation
- Outdated API docs
- Missing ADRs for major decisions

**Performance Debt:**
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Large bundle sizes

**Security Debt:**
- Missing input validation
- No authentication/authorization
- SQL injection vulnerabilities
- XSS vulnerabilities
- Exposed secrets

### 3. Categorize and Assess

Organize findings using the standardized debt categories.

#### Debt Categories

Refer to `references/debt_categories.md` for comprehensive details on:

1. **Code Quality Debt:** Code smells, complexity, duplication
2. **Architectural Debt:** Structure, coupling, abstractions
3. **Test Debt:** Coverage gaps, fragile tests
4. **Documentation Debt:** Missing or outdated docs
5. **Dependency Debt:** Outdated or problematic dependencies
6. **Performance Debt:** Inefficiencies and bottlenecks
7. **Security Debt:** Vulnerabilities and weaknesses
8. **Infrastructure Debt:** DevOps and deployment issues
9. **Design Debt:** UI/UX inconsistencies

#### Severity Assessment

Assign severity based on impact and urgency:

**Critical:**
- Security vulnerabilities
- Production-breaking issues
- Data loss risks
- **Action:** Immediate fix required

**High:**
- Significant performance problems
- Architectural issues blocking features
- High-risk untested code
- **Action:** Fix within current/next sprint

**Medium:**
- Code quality issues in frequently changed files
- Missing documentation
- Outdated dependencies (non-security)
- **Action:** Address within quarter

**Low:**
- Minor code smells
- Optimization opportunities
- Nice-to-have improvements
- **Action:** Address when convenient

#### Priority Matrix

| Impact / Effort | Low Effort | Medium Effort | High Effort |
|----------------|-----------|---------------|-------------|
| High Impact    | Do First  | Do Second     | Plan & Do   |
| Medium Impact  | Do Second | Plan & Do     | Consider    |
| Low Impact     | Quick Win | Consider      | Avoid       |

### 4. Document Findings

Create comprehensive documentation of technical debt.

#### Technical Debt Register

Use the provided template to maintain a debt register:

**Template Location:** `assets/DEBT_REGISTER_TEMPLATE.md`

**Structure:**
```markdown
## DEBT-001: Complex UserService with 847 lines

**Category:** Code Quality
**Severity:** High
**Location:** src/services/UserService.ts

**Description:**
UserService has grown to 847 lines with multiple responsibilities
including authentication, profile management, and notification handling.

**Impact:**
- Business: Slows down feature development by 30%
- Technical: Difficult to test, high bug rate
- Risk: Changes frequently break unrelated functionality

**Proposed Solution:**
Split into separate services:
- AuthenticationService
- UserProfileService
- NotificationService

**Effort Estimate:** 3 days
**Priority Justification:** High churn area blocking new features
**Target Resolution:** Sprint 24
```

**Register Sections:**
1. **Active Debt Items:** Current technical debt needing attention
2. **Resolved Items:** Historical record of fixed debt
3. **Won't Fix Items:** Debt accepted as acceptable trade-off
4. **Trends:** Analysis by category, severity, and age
5. **Review Schedule:** Regular maintenance plan

#### Architecture Decision Records (ADRs)

Document major technical decisions using ADRs to prevent future debt.

**Template Location:** `assets/ADR_TEMPLATE.md`

**When to Create ADRs:**
- Choosing frameworks or libraries
- Architectural changes
- Major refactoring decisions
- Technology migrations
- Performance optimization strategies

**Example:**
```markdown
# ADR-003: Migrate from Moment.js to date-fns

**Status:** Accepted
**Date:** 2024-01-15

## Context
Moment.js is deprecated and increases bundle size by 67KB.
Team needs a modern date library with tree-shaking support.

## Decision
Migrate to date-fns for date manipulation.

## Consequences
- Positive: Reduce bundle by 60KB, modern API, active maintenance
- Negative: Migration effort, learning curve for team
- Technical Debt: None - this resolves existing dependency debt
```

### 5. Prioritize and Plan

Create actionable plans to address technical debt.

#### Prioritization Approach

1. **Critical Items:** Add to current sprint immediately
2. **High Items:** Include in sprint planning
3. **Medium Items:** Add to quarterly roadmap
4. **Low Items:** Opportunistic fixes during related work

#### Time Allocation

**Recommended Allocation:**
- 20% of sprint capacity for technical debt
- Alternating sprints: feature sprint / debt sprint
- Dedicated quarterly "tech health" sprint

#### Tracking Progress

Monitor debt reduction over time:

**Metrics to Track:**
- Total debt items (trend down)
- Debt by severity (critical should be 0)
- Debt age (old debt is concerning)
- Resolution rate (items fixed per sprint)
- New debt rate (items added per sprint)

### 6. Prevention Strategies

Implement practices to minimize new technical debt.

#### Code Review Checklist

Before approving PRs, verify:
- [ ] No code smells introduced (complexity, size, nesting)
- [ ] Tests added/updated with adequate coverage
- [ ] Documentation updated (README, comments, ADRs)
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] No new dependencies without justification
- [ ] Follows team conventions and patterns

#### Automated Prevention

**Linting and Formatting:**
```json
{
  "rules": {
    "complexity": ["error", 10],
    "max-lines-per-function": ["error", 50],
    "max-params": ["error", 5],
    "max-depth": ["error", 4],
    "no-console": "warn"
  }
}
```

**Required Checks:**
- TypeScript strict mode enabled
- Minimum test coverage threshold (80%)
- No high-severity security vulnerabilities
- Bundle size limits enforced

#### Regular Maintenance

**Weekly:**
- Review and triage TODO/FIXME comments
- Update debt register with new findings

**Monthly:**
- Dependency updates (security patches)
- Debt register review
- Plan fixes for high-priority items

**Quarterly:**
- Full codebase debt analysis
- Architecture review
- Major dependency updates
- Trend analysis and strategy adjustment

## Decision Tree

Follow this workflow based on the situation:

**Starting a new analysis?**
→ Run automated scripts (detect_code_smells.py, analyze_dependencies.py)
→ Review output for high-severity issues
→ Conduct manual review for areas scripts can't detect
→ Go to documentation step

**Documenting findings?**
→ Copy DEBT_REGISTER_TEMPLATE.md to project root
→ Add each debt item with full details
→ Categorize by type and assign severity
→ Estimate effort and prioritize
→ Go to planning step

**Planning debt reduction?**
→ Sort by priority matrix (impact/effort)
→ Allocate sprint capacity (20% recommended)
→ Create tickets for top priority items
→ Schedule regular reviews

**Making architectural decisions?**
→ Copy ADR_TEMPLATE.md
→ Document context, options, and decision
→ Identify any debt being incurred
→ Add to debt register if applicable

**Preventing new debt?**
→ Implement code review checklist
→ Configure automated linting/testing
→ Set up regular maintenance schedule
→ Monitor metrics over time

## Tools and Scripts

### detect_code_smells.py

**Purpose:** Automated code quality analysis

**Usage:**
```bash
python3 scripts/detect_code_smells.py [src-dir] [--output json|markdown]
```

**Detects:**
- Large files (>500 lines)
- Complex functions (complexity >10)
- Technical debt markers (TODO, FIXME, HACK)
- Console statements
- Weak TypeScript typing
- Long parameter lists (>5 params)
- Deep nesting (>4 levels)
- Magic numbers

**Output:** Markdown report or JSON for programmatic processing

### analyze_dependencies.py

**Purpose:** Dependency health analysis

**Usage:**
```bash
python3 scripts/analyze_dependencies.py [package.json-path]
```

**Detects:**
- Deprecated packages (request, tslint, node-sass, etc.)
- Duplicate functionality (multiple date libs, http clients, etc.)
- Unsafe version constraints (*, latest)
- Overly strict versions (exact versions without ^ or ~)

**Output:** Markdown report with recommendations

## Reference Documentation

### debt_categories.md

Comprehensive guide to technical debt types with:
- 9 major debt categories
- Indicators and examples for each
- Impact assessment criteria
- Severity level definitions
- Measurement metrics
- Prevention strategies

**Load this reference when:**
- Need detailed examples of specific debt types
- Assessing severity and impact
- Understanding root causes
- Planning prevention strategies

## Documentation Templates

### DEBT_REGISTER_TEMPLATE.md

Complete technical debt register template including:
- Debt item structure
- Status tracking
- Impact assessment format
- Trend analysis sections
- Review schedule

**Use this template to:**
- Start a new debt register
- Standardize debt documentation
- Track debt across team/project

### ADR_TEMPLATE.md

Architecture Decision Record template including:
- Context and problem statement
- Options considered
- Decision rationale
- Consequences (positive and negative)
- Implementation plan

**Use this template to:**
- Document major technical decisions
- Prevent future "why did we do this?" questions
- Track technical debt incurred by decisions

## Best Practices

### Analysis Best Practices

1. **Run analysis regularly** (weekly or bi-weekly)
2. **Combine automated + manual review** for comprehensive coverage
3. **Focus on high-churn areas** first for maximum impact
4. **Involve the team** in debt identification
5. **Be objective** - all codebases have debt

### Documentation Best Practices

1. **Be specific** - include file names, line numbers, examples
2. **Explain impact** - why does this matter?
3. **Propose solutions** - don't just complain, suggest fixes
4. **Estimate effort** - helps with prioritization
5. **Track trends** - is debt increasing or decreasing?

### Remediation Best Practices

1. **Fix critical items immediately** - especially security
2. **Allocate consistent time** - 20% of sprint capacity
3. **Celebrate wins** - track and recognize debt reduction
4. **Don't let perfect be the enemy of good** - incremental improvement
5. **Prevent new debt** - easier than fixing old debt

### Communication Best Practices

1. **Make debt visible** - share metrics with stakeholders
2. **Educate on impact** - connect debt to business outcomes
3. **Get buy-in** - explain ROI of debt reduction
4. **Regular updates** - include in sprint reviews
5. **Avoid blame** - focus on improvement, not fault

## Example Workflow

Complete workflow from analysis to resolution:

**Week 1: Analysis**
```bash
# Run automated analysis
python3 scripts/detect_code_smells.py src --output markdown > debt_analysis.md
python3 scripts/analyze_dependencies.py package.json >> debt_analysis.md

# Manual review of critical areas
# - Authentication logic
# - Payment processing
# - Data models
```

**Week 1-2: Documentation**
```bash
# Create debt register from template
cp assets/DEBT_REGISTER_TEMPLATE.md TECHNICAL_DEBT.md

# Add findings to register with:
# - Category and severity
# - Impact assessment
# - Effort estimation
# - Priority assignment
```

**Week 2: Prioritization**
```
# Team review session
# - Review all high/critical items
# - Discuss quick wins (high impact, low effort)
# - Allocate sprint capacity
# - Create tickets for top 5 items
```

**Weeks 3-6: Remediation**
```
# Sprint work
# - Fix 2-3 debt items per sprint
# - Update debt register as items resolved
# - Create ADRs for major refactoring decisions
# - Monitor metrics
```

**Monthly: Review**
```
# Trend analysis
# - Total debt (should decrease)
# - New debt rate (should be low)
# - Age of oldest items (should decrease)
# - Categories most affected

# Adjust strategy based on trends
```

---

## Success Metrics

Track these metrics to measure debt reduction effectiveness:

**Quantity Metrics:**
- Total debt items (trending down)
- Debt by severity (zero critical)
- Debt items per 1000 LOC

**Quality Metrics:**
- Test coverage (trending up)
- Cyclomatic complexity (trending down)
- Average file/function size (stable or decreasing)

**Velocity Metrics:**
- Debt items resolved per sprint
- New debt items per sprint (should be low)
- Time to resolve (should decrease)

**Business Metrics:**
- Bug rate (should decrease)
- Feature delivery speed (should increase)
- Developer satisfaction (should increase)
