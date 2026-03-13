---
name: deep-review
description: Multi-agent quality improvement review with constructive feedback. Provides suggestions for best practices, code quality, alternatives, and performance optimization.
location: managed
dependencies:
  - context
  - preflight
  - domain-registry
allowed-tools:
  - ToolSearch
  - Read
  - Glob
  - Grep
  - Bash(git *)
  - Bash(ls *)
  - Task
  - Skill
  - Write
  - Bash(mkdir *)
---

# Deep Review: Multi-Agent Quality Improvement Framework

Execute this skill to get constructive feedback and improvement suggestions through balanced expert analysis.

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke context skill (always), then preflight if confidence is low
1. **Populate review scope** from working_scope
2. **Spawn reviewer agents in parallel** for comprehensive feedback
3. **Aggregate suggestions** from all reviewers with proper weighting
4. **Generate improvement report** with actionable recommendations
5. **Save report** to `.outputs/review/`

**Note:** This is a review for improvement, not pass/fail verification.

---

## Dependency Check

Before executing any step, verify all required skills are present:

```
[skills-root]/context/SKILL.md
[skills-root]/preflight/SKILL.md
[skills-root]/domain-registry/README.md
```

Where `[skills-root]` is the parent of this skill's directory. Resolve with `ls ../` from this skill's location.

If any required file is missing → **stop immediately** and output:

```
⚠ Missing required skills for deep-review:

  {missing-skill}
    Expected: {skills-root}/{missing-skill}/SKILL.md

Install the missing skill(s):
  git clone https://github.com/mikeng-io/agent-skills /tmp/agent-skills
  cp -r /tmp/agent-skills/skills/{missing-skill} {skills-root}/

Or install the full suite at once:
  cp -r /tmp/agent-skills/skills/ {skills-root}/
```

All dependencies present → proceed to Step 0.

---

## Step 0: Scope & Context Resolution

**Context (always required):**

Invoke `Skill("context")` first. It classifies the artifact, detects domains from domain-registry, and determines routing confidence:

```yaml
context_report:
  artifact_type: ""  # code | financial | marketing | creative | research | mixed
  domains: []        # matched domain names from domain-registry
  routing: ""        # parallel-workflow | debate-protocol | deep-council
  confidence: ""     # high | medium | low
```

**Preflight (conditional — triggered by context confidence):**

Invoke `Skill("preflight")` only if `context_report.confidence == "low"` OR one or more signals remain unresolved:
- Artifact is not clearly identified
- Intent is ambiguous (what aspect to improve?)
- Domains could not be detected
- Scope is too broad

Preflight fills exactly the gaps context could not resolve (max 3 questions, one at a time):

```yaml
scope_clarification:
  artifact: ""       # what to review
  intent: "review"
  domains: []        # supplements context_report.domains
  constraints: []    # explicit areas to focus on (e.g., "performance", "security")
  confidence: ""     # high | medium
```

If `context_report.confidence == "high"` → skip preflight entirely.

**Merge into working scope:**
```yaml
working_scope:
  artifact: ""            # files, topics, or description of what to review
  domains: []             # from context_report (authoritative), supplemented by preflight
  concerns: []            # from context signals and scope_clarification.constraints
  context_summary: ""     # combined description for reviewer agent prompts
```

Use `working_scope` throughout this skill.

---

## Step 1: Populate Review Scope

Using `working_scope` from Step 0, populate the review context:

```yaml
review_context:
  files: []              # from working_scope.artifact
  artifacts: []          # additional artifacts from working_scope
  topics: []             # key topics from context_report
  concerns: []           # from working_scope.concerns
  intent: ""             # from working_scope — what user wants to improve
  domain_inference: []   # from working_scope.domains
```

---

## Step 2: Spawn Reviewer Agents in Parallel

Spawn reviewer sub-agents in parallel using the Task tool.

### Reviewer Distribution

```yaml
reviewer_selection:
  always_spawn:
    - Best Practices Expert (weight varies by domain)
    - Alternative Approaches Expert

  domain_driven_spawn:
    - Read domain-registry to select domain experts matching conversation signals
    - Each selected domain adds one domain expert reviewer
    - Replace Code Quality Reviewer with domain-appropriate quality reviewer
      (e.g., financial → Financial Accuracy Reviewer, design → Visual Quality Reviewer)

  fallback_if_no_domain_match:
    - Code Quality Reviewer (30% weight)
    - Performance Optimizer (15% weight)

execution:
  mode: parallel
  max_concurrent: 4
  capability: high
```

### Agent Templates

#### Best Practices Expert
```
Weight: 35%
Purpose: Suggest industry best practices and standards
Capability: high

You are a BEST PRACTICES EXPERT. Your role is to suggest improvements based on industry standards and best practices.

## Your Mindset
"This works, but here's how to make it follow best practices and be more maintainable."

## Focus Areas
- Industry standards and conventions
- Framework/language-specific best practices
- Design principles (SOLID, DRY, KISS, etc.)
- Security best practices
- Accessibility standards (if applicable)
- Testing best practices

## Context to Review
{conversation_context}

## Your Scope
{scope_description}

## Output Format (JSON)
{
  "agent": "best-practices",
  "suggestions": [
    {
      "category": "Security | Architecture | Testing | Documentation | etc.",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "current_approach": "What's being done now",
      "best_practice": "What the industry standard is",
      "suggestion": "Specific improvement to make",
      "rationale": "Why this is better",
      "example": "Code example or reference (if applicable)",
      "resources": ["Links to documentation, standards, guides"]
    }
  ],
  "overall_assessment": "General feedback on alignment with best practices"
}
```

#### Code Quality Reviewer
```
Weight: 30%
Purpose: Improve code quality, readability, and maintainability
Capability: high

You are a CODE QUALITY REVIEWER. Your role is to suggest improvements for readability, maintainability, and code health.

## Your Mindset
"This code works, but here's how to make it clearer, more maintainable, and easier to work with."

## Focus Areas
- Code readability and clarity
- Naming conventions
- Function/method size and complexity
- Code organization and structure
- Documentation and comments
- Error handling patterns
- Code duplication (DRY violations)
- Magic numbers/strings

## Context to Review
{conversation_context}

## Output Format (JSON)
{
  "agent": "code-quality",
  "suggestions": [
    {
      "category": "Readability | Maintainability | Organization | Documentation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "location": "File path and line number (if applicable)",
      "issue": "What could be improved",
      "suggestion": "Specific improvement",
      "before": "Current code pattern (if applicable)",
      "after": "Improved code pattern (if applicable)",
      "impact": "How this improves code quality"
    }
  ],
  "code_health_score": "Assessment of overall code health",
  "positive_aspects": ["What's already good"]
}
```

#### Alternative Approaches Expert
```
Weight: 20%
Purpose: Suggest different approaches and trade-offs
Capability: high

You are an ALTERNATIVE APPROACHES EXPERT. Your role is to present different ways to solve the same problem with trade-off analysis.

## Your Mindset
"The current approach works, but here are alternative solutions with their pros and cons."

## Focus Areas
- Different design patterns
- Alternative architectures
- Different technology choices
- Simpler solutions
- More scalable approaches
- Different frameworks/libraries
- Trade-offs between approaches

## Context to Review
{conversation_context}

## Output Format (JSON)
{
  "agent": "alternative-approaches",
  "alternatives": [
    {
      "name": "Name of alternative approach",
      "description": "What this approach involves",
      "pros": ["Advantages of this approach"],
      "cons": ["Disadvantages of this approach"],
      "when_to_use": "Scenarios where this is better",
      "complexity": "HIGH | MEDIUM | LOW",
      "example": "Code example or reference (if applicable)"
    }
  ],
  "current_approach_assessment": {
    "strengths": ["What's good about current approach"],
    "weaknesses": ["What could be better"],
    "verdict": "When current approach is appropriate"
  }
}
```

#### Performance Optimizer
```
Weight: 15%
Purpose: Identify performance optimization opportunities
Capability: high

You are a PERFORMANCE OPTIMIZER. Your role is to identify opportunities for performance improvements.

## Your Mindset
"This works, but here's how to make it faster, more efficient, or more scalable."

## Focus Areas
- Algorithm complexity (Big O)
- Database query optimization
- Caching opportunities
- Lazy loading vs eager loading
- Resource utilization (memory, CPU, network)
- Bottlenecks and hot paths
- Scalability considerations
- Frontend performance (if applicable)

## Context to Review
{conversation_context}

## Output Format (JSON)
{
  "agent": "performance",
  "optimizations": [
    {
      "category": "Algorithm | Database | Caching | Resource | Scalability",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "current_complexity": "O(n^2), 500ms response time, etc.",
      "opportunity": "What can be optimized",
      "suggestion": "Specific optimization",
      "expected_improvement": "How much faster/better",
      "trade_offs": ["What you give up for this optimization"],
      "effort": "HIGH | MEDIUM | LOW"
    }
  ],
  "performance_assessment": "Overall performance analysis",
  "premature_optimization_warning": "Areas where optimization might not be worth it"
}
```

---

## Step 3: Aggregate Suggestions

After all reviewer agents complete, aggregate their suggestions:

### Categorize by Priority

```yaml
high_priority:
  - Suggestions marked as HIGH priority
  - Security concerns from best practices
  - Critical code quality issues

medium_priority:
  - Suggestions marked as MEDIUM priority
  - Maintainability improvements
  - Alternative approaches to consider

low_priority:
  - Nice-to-have improvements
  - Minor optimizations
  - Style preferences
```

### Identify Common Themes

Look for suggestions mentioned by multiple reviewers:
- If 2+ reviewers mention same issue → Highlight as important
- If reviewers conflict → Present both viewpoints
- If reviewers agree → Emphasize consensus

### Build Summary Table

| Aspect | Assessment | Key Suggestions |
|--------|------------|-----------------|
| Best Practices | Strong/Moderate/Weak | Top 3 suggestions |
| Code Quality | Score/10 | Top 3 improvements |
| Architecture | Appropriate/Consider Alternatives | Alternative approaches |
| Performance | Good/Needs Optimization | Top optimizations |

---

## Step 4: Generate Review Report

Generate a markdown report with this structure:

```markdown
# Deep Review Report

**Review Type:** Quality Improvement
**Reviewed At:** {timestamp}
**Scope:** {what_was_reviewed}
**Reviewers:** 4 expert agents

---

## Executive Summary

{2-3 paragraphs summarizing key findings and recommendations}

**Overall Assessment:** {High quality / Good with room for improvement / Needs work}

**Top 3 Recommendations:**
1. {Most important suggestion}
2. {Second most important}
3. {Third most important}

---

## Review Summary

| Aspect | Assessment | Priority Suggestions |
|--------|------------|---------------------|
| Best Practices | {assessment} | {count} suggestions |
| Code Quality | {score}/10 | {count} improvements |
| Alternatives | {count} options | {count} trade-offs |
| Performance | {assessment} | {count} optimizations |

---

## High Priority Suggestions

### {Category}: {Suggestion Title}

**Priority:** HIGH
**Suggested by:** {Agent name(s)}

**Current Approach:**
{What's being done now}

**Suggestion:**
{Specific improvement to make}

**Rationale:**
{Why this is important}

**Example:**
```{language}
// Before
{current_code_pattern}

// After
{improved_code_pattern}
```

**Impact:** {Expected benefit}

{Repeat for each high-priority suggestion}

---

## Medium Priority Suggestions

{Same format as high priority, grouped by category}

---

## Alternative Approaches

### Alternative 1: {Approach Name}

**Description:** {What this involves}

**Pros:**
- {Advantage 1}
- {Advantage 2}

**Cons:**
- {Disadvantage 1}
- {Disadvantage 2}

**When to Use:** {Scenarios where this is better}

**Complexity:** {HIGH/MEDIUM/LOW}

{Repeat for each alternative}

---

## Performance Optimization Opportunities

### {Optimization Title}

**Category:** {Algorithm/Database/Caching/etc.}
**Priority:** {HIGH/MEDIUM/LOW}
**Effort:** {HIGH/MEDIUM/LOW}

**Current Performance:**
{Metrics or complexity}

**Optimization:**
{Specific suggestion}

**Expected Improvement:**
{How much better}

**Trade-offs:**
- {What you give up}

{Repeat for each optimization}

---

## Positive Aspects

**What's Already Good:**
- {Positive aspect 1}
- {Positive aspect 2}
- {Positive aspect 3}

**Strengths to Maintain:**
- {Strength 1}
- {Strength 2}

---

## Resources & References

**Best Practices:**
- {Link to standard/guide}
- {Link to documentation}

**Alternative Approaches:**
- {Link to pattern description}
- {Link to comparison}

**Performance:**
- {Link to optimization guide}
- {Link to benchmarking tool}

---

## Next Steps

**Recommended Action Plan:**

1. **Immediate (High Priority):**
   - [ ] {Action item 1}
   - [ ] {Action item 2}

2. **Short Term (Medium Priority):**
   - [ ] {Action item 3}
   - [ ] {Action item 4}

3. **Long Term (Low Priority):**
   - [ ] {Action item 5}
   - [ ] {Action item 6}

**Estimated Impact:**
- Code Quality: {improvement estimate}
- Maintainability: {improvement estimate}
- Performance: {improvement estimate}
```

---

## Step 5: Save Report

## Artifact Output

Save to `.outputs/review/{YYYYMMDD-HHMMSS}-review-{slug}.md` with YAML frontmatter:

```yaml
---
skill: deep-review
timestamp: {ISO-8601}
artifact_type: review
domains: [{domain1}, {domain2}]
quality_assessment: "High quality | Good with room for improvement | Needs work"
context_summary: "{brief description of what was reviewed}"
session_id: "{unique id}"
---
```

Also save JSON companion: `{timestamp}-review-{slug}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/review/ | head -1
```

**QMD Integration (optional, progressive enhancement):**
```bash
qmd collection add .outputs/review/ --name "deep-review-artifacts" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

**Output Structure:**
```
.outputs/review/
├── 20260130-143000-review-report.md
└── 20260130-143000-review-report.json
```

---

## Configuration (Optional)

```yaml
# .outputs/review/config.yaml

review:
  # Reviewer weights
  weights:
    best_practices: 0.35
    code_quality: 0.30
    alternatives: 0.20
    performance: 0.15

  # Priority thresholds
  high_priority_threshold: 0.8
  medium_priority_threshold: 0.5

  # Output options
  include_code_examples: true
  include_resources: true
  max_suggestions_per_category: 10
```

**Environment Variables:**
```bash
export DEEP_REVIEW_OUTPUT_DIR=".outputs/review/"
export DEEP_REVIEW_INCLUDE_EXAMPLES="true"
```

---

## Notes

- **Constructive Focus:** This is about improvement, not criticism
- **No Verdict:** No pass/fail - only suggestions
- **Actionable:** All suggestions include specific actions
- **Balanced:** Includes positive aspects, not just problems
- **Conversation-Driven:** Extracts context from what was discussed
- **Domain-Agnostic:** Works for any domain (code, design, content, etc.)
- **Parallel Execution:** All reviewers run simultaneously for speed
- **Multi-Model**: For cross-model review confidence, see `deep-council`
- **Domain-Aware**: Reviewer distribution adapts to detected domains via domain-registry
- **Context Routing**: If the artifact is complex or multi-domain, invoke the `context` skill first to classify artifact type and determine optimal routing (parallel-workflow vs debate-protocol vs deep-council)
- **DeepWiki (optional)**: For code artifacts, invoke `Skill("deepwiki")` before spawning reviewers if the codebase has a Devin-indexed wiki — provides architectural context that improves domain expert quality. Non-blocking; skip if unavailable.
