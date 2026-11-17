---
name: sdd-plan-review
description: Multi-model consultation for SDD specifications providing structured feedback. Coordinates parallel AI reviewers, synthesizes actionable insights, and categorizes findings by feedback type without modifying specs or executing fixes.
---

# Spec-Driven Development: Plan Review Skill

## Overview

`Skill(sdd-toolkit:sdd-plan-review)` is the multi-perspective feedback stage for Spec-Driven Development. It convenes multiple AI reviewers to provide structured, actionable feedback across key dimensions before any implementation begins.

- Builds shared understanding of spec strengths, risks, and improvement opportunities
- Produces categorized feedback organized by type (Missing Information, Design Concerns, Risk Flags, etc.)
- Synthesizes reviewer perspectives into clear, prioritized insights
- Recommends handoffs to the correct downstream skills instead of applying changes directly

This stage is advisory-only. The output is a structured feedback report and clear guidance on where follow-up work belongs.

## Scope & Responsibilities

**This skill delivers:**
- Multi-model feedback on draft specs across architecture, feasibility, risk, and verification
- Categorized feedback organized by type (Missing Information, Design Concerns, Risk Flags, Enhancement Suggestions, etc.)
- Consolidated findings that highlight reviewer consensus and diverse perspectives
- Advisory recommendations on which downstream skill should address each finding
- Structured reports (Markdown and JSON) that capture review context for the broader workflow

**This skill does not:**
- Edit specifications or apply fixes
- Update spec metadata, journals, or approval status
- Make approval/rejection decisions (provides feedback only)

## Position in the SDD Workflow

```
PLAN → PLAN-REVIEW (consult) → UPDATE/NEXT/VALIDATE
```

- **Entry point:** A draft spec exists and needs multi-perspective feedback.
- **Core activity:** `sdd-plan-review` convenes multiple AI reviewers and synthesizes structured, actionable feedback.

**Role of this skill:** Provide diverse perspectives and categorized feedback before implementation starts. It informs, but never performs, follow-up edits.

## Scope Boundaries

- ✅ **Do:** Convene multi-model reviews, interrogate assumptions, aggregate perspectives, and categorize feedback by type (Missing Information, Design Concerns, Risk Flags, etc.).
- ✅ **Do:** Capture review metadata, feedback categories, and rationale in the generated report so downstream skills have clear guidance.
- ❌ **Don't:** Edit specs, adjust estimates, rewrite acceptance criteria, or change task hierarchies.
- ❌ **Don't:** Update journals, statuses, or frontmatter.
- ❌ **Don't:** Author execution plans or task breakdowns.

## ⚠️ Long-Running Operations

**This skill may run operations that take up to 5 minutes. Be patient and wait for completion.**

### CRITICAL: Avoid BashOutput Spam
- **ALWAYS use foreground execution with 5-minute timeout:** `Bash(command="...", timeout=300000)`
- **WAIT for the command to complete** - this may take the full 5 minutes
- **NEVER use `run_in_background=True` for test suites, builds, or analysis**
- If you must use background (rare), **wait at least 60 seconds** between BashOutput checks
- **Maximum 3 BashOutput calls per background process** - then kill it or let it finish

### Why?
Polling BashOutput repeatedly creates spam and degrades user experience. Long operations should run in foreground with appropriate timeout, not in background with frequent polling.

### Example (CORRECT):
```
# Test suite that might take 5 minutes (timeout in milliseconds)
result = Bash(command="pytest src/", timeout=300000)  # Wait up to 5 minutes
# The command will block here until completion - this is correct behavior
```

### Example (WRONG):
```
# Don't use background + polling
bash_id = Bash(command="pytest", run_in_background=True)
output = BashOutput(bash_id)  # Creates spam!
```

## Core Philosophy

**Diverse Perspectives Improve Quality**: Multiple AI models reviewing a specification catch more issues and provide richer insights than a single review. By consulting different AI CLIs (gemini, codex, cursor-agent) in parallel, we validate design decisions, identify risks, and surface improvement opportunities before costly implementation.

**Feedback, Not Gatekeeping**: This skill provides structured, actionable feedback to inform decision-making, not approval/rejection gatekeeping. The output helps spec authors understand strengths, risks, and opportunities from multiple perspectives.

**Key Benefits:**
- Surfaces specification gaps and improvement opportunities before coding begins
- Validates architecture from multiple expert angles
- Identifies hidden risks and edge cases
- Evaluates implementation feasibility realistically
- Provides diverse perspectives on complex decisions
- Generates categorized, actionable feedback
- Reduces expensive rework and technical debt

## When to Use This Skill

Request `Skill(sdd-toolkit:sdd-plan-review)` when you need multi-perspective feedback on a draft specification:
- New or revised specs that benefit from diverse expert perspectives
- High-risk, high-effort, or multi-team initiatives where blind spots are expensive
- Novel architectures, emerging technologies, or unfamiliar integrations
- Security-sensitive surfaces (auth, PII, critical data flows) that need scrutiny
- Aggressive timelines or estimates that need feasibility validation

**Do NOT request this skill when:**
- The spec is trivial, low-risk, or already well-understood (<5 tasks, standard patterns)
- Implementation is already underway
- You need someone to make direct specification edits
- The work is exploratory, disposable, or prototype-only

**Reminder:** This skill provides structured feedback—decisions about addressing findings flow through the calling agent.

## Decision Guide: Should We Convene a Review?

```
Situation?
├─ Draft spec ready for approval → Engage plan-review (full)
├─ Security-critical area (auth/data/privacy) → Engage plan-review (security)
├─ Feasibility questions or aggressive estimates → Engage plan-review (feasibility)
├─ Major architectural novelty or integration risk → Engage plan-review (full)
├─ Lightweight, low-risk spec → Skip; proceed directly to sdd-next
├─ Work already executing → Use fidelity-review or update workflows instead
└─ Unsure confidence level → Engage plan-review (quick) to gain signal

After the consultation:
├─ Return to calling agent for next steps
```

## Tool Verification

**Before using this skill**, verify the required tools are available:

```bash
sdd list-review-tools
```

**IMPORTANT - CLI Usage Only**:
- ✅ **DO**: Use `sdd review` CLI wrapper commands (e.g., `sdd review`, `sdd list-review-tools`)
- ❌ **DO NOT**: Execute Python scripts directly or call AI CLIs directly (e.g., `python sdd_review.py`, `bash gemini ...`, `codex ...`)

The CLI provides proper error handling, validation, argument parsing, and interface consistency. It orchestrates AI CLI calls automatically. Direct script or AI CLI execution bypasses these safeguards and may fail.

If the verification command fails, ensure the SDD toolkit is properly installed and accessible in your environment.

## Quick Start

### Check Available Tools

```bash
# List which AI CLI tools are installed
sdd list-review-tools

# Expected output:
# ✓ Available (2):
#   gemini
#   codex
# ✗ Not Available (1):
#   cursor-agent
```

### Basic Review

```bash
# Review a spec with automatic tool detection
sdd review user-auth-001

# Review with specific type
sdd review user-auth-001 --type full

# Quick review (fast, basic checks only)
sdd review user-auth-001 --type quick

# Security-focused review
sdd review user-auth-001 --type security

# Feasibility check (estimates, dependencies)
sdd review user-auth-001 --type feasibility
```

## Quick Reference: Common Commands

| Command | Purpose | Typical Duration |
|---------|---------|------------------|
| `sdd list-review-tools` | Check which AI CLIs are installed | Instant |
| `sdd review <spec> --type quick` | Fast completeness check | 10-15 min |
| `sdd review <spec> --type full` | Comprehensive analysis | 20-30 min |
| `sdd review <spec> --type security` | Security vulnerability scan | 15-20 min |
| `sdd review <spec> --type feasibility` | Estimate & dependency validation | 10-15 min |

## Typical Workflow

1. **Request the consultation**
   ```bash
   sdd review myspec --type full
   ```
   - Confirm the correct review type and tools, run once per major draft.

2. **Interpret the feedback report**
   - Review categorized findings organized by feedback type
   - Note reviewer consensus and diverse perspectives
   - Identify priority findings that need addressing

3. **Prepare the advisory handoff**
   - Summarize key findings and improvement opportunities
   - Prioritize feedback by category and severity
   - Recommend downstream actions based on findings

## Outputs

- **Feedback report (Markdown):** Automatically saved to `specs/.reviews/<spec-id>-review-<type>.md` and printed to stdout; captures categorized findings, reviewer perspectives, and recommended handoffs.
- **JSON summary:** Automatically saved alongside the Markdown as `specs/.reviews/<spec-id>-review-<type>.json`; includes feedback categories, participating tools, and issue catalog for orchestration.
- **Exit codes for automation:**
  - `0`: Review completed successfully with feedback
  - `1`: Review failed (configuration, tool errors)
  - `2`: Critical feedback items found (for CI/CD integration)

## Feedback Categories

Review findings are organized into structured categories to make feedback actionable:

### Missing Information
Identifies gaps where the spec needs more detail for successful implementation.

**Examples:**
- "Task 2.3 lacks acceptance criteria - unclear when task is complete"
- "Authentication flow missing error handling details"
- "Database migration steps not specified in Phase 3"
- "No rollback strategy defined for deployment tasks"

### Design Concerns
Highlights architectural or design choices that may need reconsideration.

**Examples:**
- "Tight coupling between auth module and user service may hinder testing"
- "Synchronous API calls in task 1.4 could create bottlenecks under load"
- "Consider event-driven pattern instead of polling for real-time updates"
- "Circular dependency between modules A and B needs resolution"

### Risk Flags
Surfaces potential security, performance, or reliability risks.

**Examples:**
- "Admin endpoints lack authentication checks (security risk)"
- "No rate limiting on public API (DoS vulnerability)"
- "Storing passwords in plaintext violates security best practices"
- "Missing input validation could allow SQL injection"
- "No monitoring for critical payment processing flow"

### Feasibility Questions
Raises concerns about estimates, dependencies, or implementation approach.

**Examples:**
- "Task 3.2 estimated at 2 hours but involves complex OAuth integration (likely 6-8 hours)"
- "Phase 2 assumes legacy API has endpoint X - need to verify availability"
- "Database migration in task 4.1 requires DBA access - confirm permissions"
- "Timeline assumes 3 developers but team currently has 2"

### Enhancement Suggestions
Proposes improvements that aren't critical but would strengthen the spec.

**Examples:**
- "Consider adding health check endpoints for monitoring"
- "Could benefit from batch processing for large datasets"
- "Adding retry logic would improve resilience"
- "Documentation task for API endpoints would help future maintenance"

### Clarification Requests
Identifies ambiguous language or unclear requirements.

**Examples:**
- "What does 'performant' mean in acceptance criteria? Need specific metrics"
- "Task 2.1 says 'update user profile' - which fields are in scope?"
- "'Handle errors gracefully' is vague - specify retry strategy, logging, user messaging"
- "Does 'mobile support' include tablets or just phones?"

## Review Types

### Overview Table

| Type | Models | Duration | Dimensions Emphasized | Use When |
|------|--------|----------|----------------------|----------|
| **quick** | 2 | 10-15 min | Completeness, Clarity | Simple specs, time-constrained, low-risk changes |
| **full** | 3-4 | 20-30 min | All 6 dimensions | Complex specs, moderate-to-high risk, novel architecture |
| **security** | 2-3 | 15-20 min | Risk Management | Auth/authz, data handling, API security, compliance |
| **feasibility** | 2-3 | 10-15 min | Feasibility | Tight deadlines, resource constraints, uncertain scope |

### Quick Review

**Focus**: Basic completeness and clarity
**Models**: 2 tools (diverse perspectives)
**Best For**: Simple specs, low-risk changes, time pressure

**What it checks:**
- All required sections present
- Tasks clearly described with acceptance criteria
- Dependencies explicitly stated
- Basic verification steps exist
- No obvious gaps or ambiguities

**Skip detailed analysis of:**
- Architecture soundness
- Performance implications
- Security edge cases
- Implementation complexity

### Full Review

**Focus**: Comprehensive analysis across all dimensions
**Models**: 3-4 tools (architecture, security, implementation, integration perspectives)
**Best For**: Complex specs, moderate-to-high risk, cross-team changes, novel patterns

**What it checks:**
- **Completeness**: All sections present, sufficient detail, no gaps
- **Clarity**: Clear descriptions, acceptance criteria, unambiguous language
- **Feasibility**: Realistic estimates, achievable dependencies, proper sizing
- **Architecture**: Sound design, proper abstractions, scalability, maintainability
- **Risk Management**: Risks identified, edge cases covered, failure modes handled
- **Verification**: Comprehensive testing plan, verification steps, quality gates

**Most thorough review type** - use when cost of failure is high.

### Security Review

**Focus**: Security vulnerabilities and risks
**Models**: 2-3 tools (offensive, defensive, compliance perspectives)
**Best For**: Auth/authz, data handling, API security, regulated domains, PII/PHI

**What it checks:**
- Authentication and authorization design
- Input validation and sanitization
- Secrets management (API keys, passwords, tokens)
- Access control and principle of least privilege
- Audit logging and monitoring
- Data encryption (at rest, in transit)
- SQL/command injection prevention
- CSRF/XSS protections
- Rate limiting and DoS protection
- Compliance requirements (GDPR, HIPAA, SOC2)

**Emphasizes risk_management dimension** in scoring.

### Feasibility Review

**Focus**: Implementation realism and estimate accuracy
**Models**: 2-3 tools (optimist, realist, pessimist perspectives)
**Best For**: Tight deadlines, resource constraints, uncertain requirements, large efforts

**What it checks:**
- Time estimates realistic for each task
- Required skills present in team
- Dependencies actually exist and are accessible
- External APIs/services available and documented
- Performance requirements achievable with approach
- Complexity accurately assessed (not underestimated)
- Blockers identified and mitigated
- Resource requirements feasible (compute, storage, budget)

**Identifies underestimated tasks** and impossible requirements.

## Review Dimensions

Every review examines specs across **6 dimensions** to structure feedback:

1. **Completeness**
   - All sections present
   - Sufficient detail for implementation
   - No missing requirements or undefined dependencies
   - Acceptance criteria for all tasks

2. **Clarity**
   - Clear, unambiguous descriptions
   - Specific acceptance criteria
   - Well-defined task boundaries
   - No vague or confusing language

3. **Feasibility**
   - Realistic time estimates
   - Achievable dependencies
   - Required skills available
   - No impossible requirements

4. **Architecture**
   - Sound design decisions
   - Proper abstractions
   - Scalability considerations
   - Low coupling, high cohesion

5. **Risk Management**
   - Risks identified
   - Edge cases covered
   - Failure modes addressed
   - Mitigation strategies present

6. **Verification**
   - Comprehensive test plan
   - Verification steps defined
   - Quality gates established
   - Testing gaps identified

These dimensions help organize feedback into actionable categories. Reviewers provide specific findings and suggestions within each dimension rather than numerical scores.

## The Review Workflow

### Phase 1: Preparation

**Before running review, ensure:**

1. **Check tool availability**
   ```bash
   sdd list-review-tools
   ```
   - Need at least 1 tool installed
   - 2+ tools recommended for multi-model review
   - All 3 tools ideal for comprehensive analysis

2. **Load specification**
   - Spec must be complete (not draft fragments)
   - JSON format required
   - Frontmatter should include complexity/risk metadata

3. **Select review type**
   - Auto-selected based on spec metadata
   - Or explicitly specify with `--type` flag
   - See Decision Tree above for guidance

**The tool automatically:**
- Detects which AI CLI tools are available
- Parses spec frontmatter and content
- Determines appropriate review scope
- Selects models based on review type

### Phase 2: Execute Review

**Multi-model consultation (parallel execution):**

```bash
sdd review user-auth-001 --type full
```

**What happens:**
1. **Initiate each model review** with enforced critical framing
2. **Call all AI CLI tools simultaneously** (ThreadPoolExecutor)
3. **Collect responses** as they complete (timeouts: 60-120s per tool)
4. **Handle failures gracefully** (continue with successful responses)
5. **Parse responses** (JSON extraction with fallback strategies)

**Progress indicators:**
```
Reviewing specification: user-auth-001.json
Using 3 tool(s): gemini, codex, cursor-agent

Starting full review...
✓ gemini completed (15.2s)
✓ codex completed (22.5s)
✗ cursor-agent timeout (120s)

Review Complete
Execution time: 120.1s
Models responded: 2/3
```

**Automatic error handling:**
- Timeouts → Automatic retries with backoff
- Rate limits → Sequential mode fallback
- Auth failures → Skip tool with clear message
- Parse failures → Use other model responses

### Phase 3: Interpret Results

**Understanding the report:**

**Feedback Organization:**
The report groups findings by category (Missing Information, Design Concerns, Risk Flags, Feasibility Questions, Enhancement Suggestions, Clarification Requests) to make them actionable.

**Reviewer Consensus:**
- **Strong consensus**: Multiple reviewers identified the same issue
- **Diverse perspectives**: Different reviewers raised different concerns
- **Conflicting views**: Reviewers disagree (both perspectives documented)

**Priority Levels:**
- **CRITICAL**: Security vulnerabilities, blockers, data loss risks → **Address immediately**
- **HIGH**: Design flaws, missing information, quality issues → **Address before implementation**
- **MEDIUM**: Improvements, unclear requirements → **Consider addressing**
- **LOW**: Nice-to-have enhancements → **Note for future**

**Example findings:**
```
📋 Feedback Summary:

### Risk Flags (CRITICAL)
1. Missing authentication on admin endpoints
   Priority: CRITICAL | Flagged by: gemini, codex
   Impact: Unauthorized access to sensitive operations
   Recommendation: Add JWT validation middleware to routes

### Feasibility Questions (HIGH)
2. Time estimates may be unrealistic for Phase 2
   Priority: HIGH | Flagged by: codex
   Impact: Timeline risk - complex OAuth integration underestimated
   Recommendation: Revisit estimates for tasks 2.3-2.5 (suggest +50%)

### Missing Information (MEDIUM)
3. Error handling strategy not defined
   Priority: MEDIUM | Flagged by: gemini
   Impact: Unclear how failures should be handled
   Recommendation: Add error handling details to affected tasks
```

### Phase 4: Synthesize Findings & Recommend Handoffs

1. **Organize feedback by category and priority**
   - Group findings by category (Missing Information, Design Concerns, Risk Flags, etc.)
   - Prioritize within each category by CRITICAL / HIGH / MEDIUM / LOW
   - Note reviewer consensus and diverse perspectives

2. **Identify the type of downstream work**
   - Structural or architectural redesign
   - Documentation, metadata, or acceptance criteria updates
   - Additional planning or investigation needed
   - Additional audits (security review, validation)

3. **Capture the feedback summary**
   - Highlight key findings and improvement opportunities
   - Note areas of consensus and areas where reviewers disagree
   - Return the path to the JSON report for full context

## Advanced Topics

### Error Handling

**Automatic recovery:**

| Error Type | Tool Behavior | User Impact |
|------------|---------------|-------------|
| **Timeout** (>120s) | Retry with backoff (2 attempts) | Longer wait, usually succeeds |
| **Rate limit** (HTTP 429) | Wait + retry, or sequential mode | Slower execution |
| **Auth failure** (401/403) | Skip tool, continue with others | Reduced confidence |
| **Network error** | Retry 2x with backoff | Usually recovers |
| **Parse failure** | Use other model responses | No impact if ≥2 models succeed |

**Partial results:**

| Scenario | Outcome | Confidence |
|----------|---------|------------|
| 3/3 tools succeed | Full review | High |
| 2/3 tools succeed | Continue with 2 | Medium (noted in report) |
| 1/3 tools succeed | Continue with 1 | Low (single-model warning) |
| 0/3 tools succeed | Review fails | Error with troubleshooting |

## Best Practices

### When to Review

**Always review:**
- High-risk or high-priority specs
- Security-sensitive implementations (auth, data, payments)
- Novel architecture or technology choices
- Before final approval and team commitment

**Consider reviewing:**
- Medium complexity (≥ 10 tasks)
- Cross-team dependencies
- Specs with aggressive timelines
- Unclear or novel requirements

**Skip review:**
- Simple specs (< 5 tasks)
- Well-understood patterns (CRUD operations)
- Low-risk internal refactorings
- Trivial bug fixes

### Review Quality Tips

**For best results:**

1. **Review complete specs, not fragments**
   - All phases defined
   - Tasks described
   - Dependencies stated
   - Verification steps present

2. **Use appropriate review type**
   - Quick: Simple, low-risk
   - Full: Complex, moderate-to-high risk
   - Security: Auth/data handling
   - Feasibility: Tight timelines

3. **Address issues by priority**
   - CRITICAL → Must fix before proceeding
   - HIGH → Should fix, significant impact
   - MEDIUM → Consider, nice-to-have
   - LOW → Note for future improvements

4. **Don't blindly accept all feedback**
   - Consider context and tradeoffs
   - Models may misunderstand requirements
   - Use judgment on disagreements
   - Recommend when issues might be deferred

### Coordinating Follow-Up Work

**Prioritization guide for addressing feedback:**

```
CRITICAL findings:
  - Security vulnerabilities
  - Blocking dependencies
  - Data loss risks
  - Compliance violations
  → Address immediately before implementation

HIGH findings:
  - Design flaws
  - Missing information
  - Unrealistic estimates
  - Quality concerns
  → Address before implementation begins

MEDIUM findings:
  - Unclear requirements
  - Missing optimizations
  - Incomplete documentation
  → Consider addressing; may defer with rationale

LOW findings:
  - Nice-to-have improvements
  - Edge case enhancements
  - Future considerations
  → Note for future work; safe to defer
```

**Balance perspectives:**

When models disagree:
1. Review each perspective and note context differences.
2. Identify root causes or assumptions driving the disagreement.

Remember to include the JSON file path at the end of your report back.
