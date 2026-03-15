---
name: deep-audit
description: Multi-agent standards and compliance auditing with pass/fail verdicts. Checks against security, accessibility, code standards, regulatory requirements, and performance benchmarks.
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

# Deep Audit: Multi-Agent Standards & Compliance Framework

Execute this skill to audit work against standards and compliance requirements with formal pass/fail verdicts.

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke context skill (always), then preflight if confidence is low
1. **Populate audit scope** from working_scope
2. **Spawn auditor agents in parallel** for comprehensive checking
3. **Aggregate violations** from all auditors
4. **Generate audit report** with PASS/FAIL verdict
5. **Save report** to `.outputs/audit/`

**Note:** This is a formal audit with pass/fail verdict, not improvement suggestions.

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
⚠ Missing required skills for deep-audit:

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
- Standards or compliance requirements cannot be inferred
- Domains could not be detected
- Scope is too broad to audit meaningfully

Preflight fills exactly the gaps context could not resolve (max 3 questions, one at a time):

```yaml
scope_clarification:
  artifact: ""       # what to audit
  intent: "audit"
  domains: []        # supplements context_report.domains
  constraints: []    # explicit standards, compliance requirements, focus areas
  confidence: ""     # high | medium
```

If `context_report.confidence == "high"` → skip preflight entirely.

**Merge into working scope:**
```yaml
working_scope:
  artifact: ""            # files, topics, or description of what to audit
  domains: []             # from context_report (authoritative), supplemented by preflight
  standards: []           # inferred from domains, artifact type, and any explicit constraints
  compliance: []          # inferred from context + scope_clarification
  context_summary: ""     # combined description for auditor agent prompts
```

Use `working_scope` throughout this skill.

---

## Step 1: Populate Audit Scope

Using `working_scope` from Step 0, populate the audit context:

```yaml
audit_context:
  files: []              # from working_scope.artifact
  artifacts: []          # additional artifacts from working_scope
  topics: []             # key topics from context_report
  standards: []          # from working_scope.standards
  compliance: []         # from working_scope.compliance
  domain_inference: []   # from working_scope.domains
```

**Infer audit requirements from working_scope:**
- Explicit standards (e.g., "WCAG 2.1", "OWASP Top 10") → carry forward from constraints
- Compliance needs (e.g., "GDPR compliance", "SOC2") → from compliance field
- Domain context (e.g., "healthcare app" → HIPAA) → from domain-registry mapping
- File types (e.g., `.tsx` → accessibility) → from artifact_type in context_report

---

## Step 2: Spawn Auditor Agents in Parallel

Spawn auditor sub-agents in parallel using the Task tool.

### Auditor Distribution

```yaml
auditor_selection:
  step_1_read_domain_registry:
    - Read domain-registry/domains/technical.md
    - Read domain-registry/domains/business.md
    - Read domain-registry/domains/creative.md

  step_2_match_signals:
    - Match conversation signals against each domain's trigger_signals
    - Select all matching domains (minimum 2)

  step_3_map_to_auditors:
    - Each selected domain → spawn corresponding expert_role as auditor
    - Weight distribution: 30% to primary domain, remainder shared equally

  fallback_if_technical_signals:
    - Security Auditor (30%)
    - Accessibility Auditor (25%)
    - Code Standards Auditor (20%)
    - Regulatory Auditor (15%)
    - Performance Auditor (10%)

  examples:
    - marketing artifact → Brand Compliance Auditor + Legal Auditor + Audience Fit Auditor
    - financial document → Financial Accuracy Auditor + Regulatory Auditor + Risk Auditor
    - design system → Visual Standards Auditor + Accessibility Auditor + Brand Auditor

execution:
  mode: parallel
  max_concurrent: 5
  capability: high
```

### Agent Templates

#### Security Auditor
```
Weight: 30%
Purpose: Check security standards and vulnerabilities
Capability: high

You are a SECURITY AUDITOR. Your role is to check for security vulnerabilities and standards compliance.

## Your Mindset
"Does this meet security standards? Are there vulnerabilities?"

## Standards to Check
- OWASP Top 10
- CWE (Common Weakness Enumeration)
- Security best practices
- Authentication/authorization
- Input validation
- Data encryption
- Secrets management

## Context to Audit
{conversation_context}

## Your Scope
{scope_description}

## Output Format (JSON)
{
  "agent": "security-auditor",
  "verdict": "PASS | FAIL",
  "violations": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "standard": "OWASP A03:2021 | CWE-79 | etc.",
      "category": "Injection | XSS | Authentication | etc.",
      "location": "File path and line number",
      "violation": "Description of the violation",
      "evidence": "Code snippet or reference",
      "remediation": "How to fix",
      "resources": ["Links to documentation"]
    }
  ],
  "passed_checks": [
    "List of security checks that passed"
  ],
  "overall_security_score": "0-100"
}
```

#### Accessibility Auditor
```
Weight: 25%
Purpose: Check accessibility standards compliance
Capability: high

You are an ACCESSIBILITY AUDITOR. Your role is to check for accessibility compliance.

## Your Mindset
"Is this accessible to all users? Does it meet WCAG standards?"

## Standards to Check
- WCAG 2.1 (Level A, AA, AAA)
- ARIA best practices
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- Focus management
- Semantic HTML

## Context to Audit
{conversation_context}

## Output Format (JSON)
{
  "agent": "accessibility-auditor",
  "verdict": "PASS | FAIL",
  "wcag_level": "A | AA | AAA",
  "violations": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "standard": "WCAG 2.1.1 | WCAG 1.4.3 | etc.",
      "category": "Perceivable | Operable | Understandable | Robust",
      "location": "File path and line number",
      "violation": "Description of the violation",
      "impact": "Who is affected (screen reader users, keyboard users, etc.)",
      "remediation": "How to fix",
      "resources": ["Links to WCAG documentation"]
    }
  ],
  "passed_checks": [
    "List of accessibility checks that passed"
  ],
  "overall_accessibility_score": "0-100"
}
```

#### Code Standards Auditor
```
Weight: 20%
Purpose: Check code style and standards compliance
Capability: high

You are a CODE STANDARDS AUDITOR. Your role is to check for code style and standards compliance.

## Your Mindset
"Does this follow the project's coding standards?"

## Standards to Check
- Applicable language-specific coding standards
- Applicable linting rules and tools for the detected language
- Formatting and style rules for the detected language
- Naming conventions
- File organization
- Documentation requirements
- Test coverage thresholds

## Context to Audit
{conversation_context}

## Output Format (JSON)
{
  "agent": "code-standards-auditor",
  "verdict": "PASS | FAIL",
  "violations": [
    {
      "severity": "HIGH | MEDIUM | LOW",
      "standard": "applicable coding standard | linting rule | etc.",
      "category": "Style | Formatting | Naming | Documentation",
      "location": "File path and line number",
      "violation": "Description of the violation",
      "current": "Current code pattern",
      "expected": "Expected code pattern",
      "remediation": "How to fix"
    }
  ],
  "passed_checks": [
    "List of standards checks that passed"
  ],
  "overall_compliance_score": "0-100",
  "test_coverage": {
    "current": "85%",
    "required": "80%",
    "status": "PASS | FAIL"
  }
}
```

#### Regulatory Auditor
```
Weight: 15%
Purpose: Check regulatory compliance requirements
Capability: high

You are a REGULATORY AUDITOR. Your role is to check for regulatory compliance.

## Your Mindset
"Does this meet regulatory requirements?"

## Standards to Check
- GDPR (data privacy)
- HIPAA (healthcare)
- SOC2 (security controls)
- PCI-DSS (payment card industry)
- COPPA (children's privacy)
- Industry-specific regulations

## Context to Audit
{conversation_context}

## Output Format (JSON)
{
  "agent": "regulatory-auditor",
  "verdict": "PASS | FAIL",
  "regulations_applicable": ["GDPR", "HIPAA", etc.],
  "violations": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "regulation": "GDPR Article 17 | HIPAA §164.308 | etc.",
      "category": "Data Privacy | Security | Consent | etc.",
      "location": "File path or process",
      "violation": "Description of the violation",
      "legal_risk": "Potential consequences",
      "remediation": "How to fix",
      "resources": ["Links to regulation documentation"]
    }
  ],
  "passed_checks": [
    "List of compliance checks that passed"
  ],
  "overall_compliance_score": "0-100"
}
```

#### Performance Auditor
```
Weight: 10%
Purpose: Check performance benchmarks and SLAs
Capability: high

You are a PERFORMANCE AUDITOR. Your role is to check if performance meets benchmarks.

## Your Mindset
"Does this meet performance standards and SLAs?"

## Standards to Check
- Response time requirements
- Core Web Vitals (LCP, FID, CLS)
- Load time benchmarks
- Database query performance
- API latency targets
- Resource usage limits
- Scalability requirements

## Context to Audit
{conversation_context}

## Output Format (JSON)
{
  "agent": "performance-auditor",
  "verdict": "PASS | FAIL",
  "violations": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "standard": "Core Web Vitals | SLA | Benchmark",
      "category": "Response Time | Load Time | Resource Usage",
      "metric": "LCP | TTFB | Query Time | etc.",
      "current_value": "2.5s | 500ms | etc.",
      "required_value": "2.5s | 200ms | etc.",
      "violation": "Description of the violation",
      "impact": "User experience impact",
      "remediation": "How to fix"
    }
  ],
  "passed_checks": [
    "List of performance checks that passed"
  ],
  "overall_performance_score": "0-100",
  "core_web_vitals": {
    "lcp": {"value": "2.1s", "threshold": "2.5s", "status": "PASS"},
    "fid": {"value": "50ms", "threshold": "100ms", "status": "PASS"},
    "cls": {"value": "0.05", "threshold": "0.1", "status": "PASS"}
  }
}
```

---

## Step 3: Aggregate Violations

After all auditor agents complete, aggregate their findings:

### Determine Overall Verdict

```yaml
verdict_logic:
  FAIL:
    - Any CRITICAL violation
    - 3+ HIGH severity violations
    - Any regulatory violation (CRITICAL/HIGH)

  CONCERNS:
    - 1-2 HIGH severity violations
    - Multiple MEDIUM violations
    - All checks passed but warnings exist

  PASS:
    - No CRITICAL or HIGH violations
    - Only MEDIUM/LOW violations (acceptable)
    - All critical checks passed
```

### Violation Summary

```yaml
by_severity:
  critical: [count]
  high: [count]
  medium: [count]
  low: [count]

by_category:
  security: [count]
  accessibility: [count]
  code_standards: [count]
  regulatory: [count]
  performance: [count]

blocking_violations: [violations that cause FAIL]
```

### Build Summary Table

| Auditor | Verdict | Violations | Score |
|---------|---------|------------|-------|
| Security | PASS/FAIL | Critical: 0, High: 2 | 85/100 |
| Accessibility | PASS/FAIL | Critical: 1, High: 0 | 70/100 |
| Code Standards | PASS/FAIL | High: 0, Medium: 5 | 92/100 |
| Regulatory | PASS/FAIL | Critical: 0, High: 0 | 100/100 |
| Performance | PASS/FAIL | High: 1, Medium: 2 | 78/100 |

---

## Step 4: Generate Audit Report

Generate a markdown report with this structure:

```markdown
# Deep Audit Report

**Audit Type:** Standards & Compliance
**Audited At:** {timestamp}
**Scope:** {what_was_audited}
**Auditors:** 5 specialist auditors

---

## Overall Verdict: {PASS | CONCERNS | FAIL}

**Audit Score:** {weighted_average}/100

**Summary:**
- ❌ {count} CRITICAL violations → {BLOCKS DEPLOYMENT}
- ⚠️  {count} HIGH violations → {SHOULD FIX}
- ⚠️  {count} MEDIUM violations → {RECOMMENDED FIX}
- ℹ️  {count} LOW violations → {NICE TO FIX}

**Blocking Issues:** {count} violations prevent passing

---

## Audit Summary

| Auditor | Verdict | Critical | High | Medium | Low | Score |
|---------|---------|----------|------|--------|-----|-------|
| Security | {PASS/FAIL} | {n} | {n} | {n} | {n} | {n}/100 |
| Accessibility | {PASS/FAIL} | {n} | {n} | {n} | {n} | {n}/100 |
| Code Standards | {PASS/FAIL} | {n} | {n} | {n} | {n} | {n}/100 |
| Regulatory | {PASS/FAIL} | {n} | {n} | {n} | {n} | {n}/100 |
| Performance | {PASS/FAIL} | {n} | {n} | {n} | {n} | {n}/100 |

**Overall Score:** {weighted_average}/100

---

## Critical Violations (Must Fix)

### ❌ {Category}: {Violation Title}

**Severity:** CRITICAL
**Standard:** {OWASP A03:2021 | WCAG 2.1.1 | etc.}
**Auditor:** {auditor_name}

**Violation:**
{Description of the violation}

**Location:**
{File path and line number}

**Evidence:**
```{language}
{Code snippet showing the violation}
```

**Impact:**
{What happens if not fixed}

**Remediation:**
```{language}
{Code showing how to fix}
```

**Resources:**
- {Link to standard documentation}
- {Link to remediation guide}

{Repeat for each critical violation}

---

## High Severity Violations (Should Fix)

{Same format as critical, grouped by category}

---

## Medium Severity Violations (Recommended Fix)

{Same format, possibly summarized if many}

---

## Low Severity Violations (Nice to Fix)

{Summarized list}

---

## Passed Checks ✅

**Security:**
- ✅ No SQL injection vulnerabilities
- ✅ Proper authentication implementation
- ✅ HTTPS enforced

**Accessibility:**
- ✅ Semantic HTML used
- ✅ Alt text on images
- ✅ Keyboard navigation works

**Code Standards:**
- ✅ Linting rules followed
- ✅ Test coverage >80%
- ✅ Documentation present

**Regulatory:**
- ✅ GDPR consent implemented
- ✅ Data encryption at rest

**Performance:**
- ✅ Core Web Vitals pass
- ✅ API response <200ms

---

## Compliance Status

### GDPR Compliance
**Status:** {COMPLIANT | NON-COMPLIANT | PARTIALLY COMPLIANT}
**Issues:** {count} violations

### WCAG 2.1 Level AA
**Status:** {COMPLIANT | NON-COMPLIANT}
**Issues:** {count} violations

### OWASP Top 10
**Status:** {SAFE | VULNERABLE}
**Issues:** {count} vulnerabilities

---

## Remediation Plan

**Immediate (CRITICAL - Must fix before deployment):**
- [ ] Fix {violation 1}
- [ ] Fix {violation 2}

**Short Term (HIGH - Should fix this sprint):**
- [ ] Fix {violation 3}
- [ ] Fix {violation 4}

**Medium Term (MEDIUM - Fix in next release):**
- [ ] Fix {violation 5}
- [ ] Fix {violation 6}

**Long Term (LOW - Fix when convenient):**
- [ ] Fix {violation 7}

**Estimated Effort:**
- CRITICAL fixes: {hours/days}
- HIGH fixes: {hours/days}
- MEDIUM fixes: {hours/days}

---

## Re-Audit Recommendation

{If FAIL or CONCERNS:}
**Re-audit required after fixing:**
- All CRITICAL violations
- All HIGH violations (recommended)

{If PASS:}
**Next audit recommended:**
- After major changes
- Before production deployment
- Quarterly compliance check
```

---

## Step 5: Save Report

## Artifact Output

Save to `.outputs/audit/{YYYYMMDD-HHMMSS}-audit-{slug}.md` with YAML frontmatter:

```yaml
---
skill: deep-audit
timestamp: {ISO-8601}
artifact_type: audit
domains: [{domain1}, {domain2}]
verdict: PASS | FAIL | CONCERNS        # if applicable
context_summary: "{brief description of what was reviewed}"
session_id: "{unique id}"
---
```

Also save JSON companion: `{timestamp}-audit-{slug}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/audit/ | head -1
```

**QMD Integration (optional, progressive enhancement):**
```bash
qmd collection add .outputs/audit/ --name "deep-audit-artifacts" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

**Output Structure:**
```
.outputs/audit/
├── 20260130-143000-audit-report.md
└── 20260130-143000-audit-report.json
```

---

## Configuration (Optional)

```yaml
# .outputs/audit/config.yaml

audit:
  # Auditor weights
  weights:
    security: 0.30
    accessibility: 0.25
    code_standards: 0.20
    regulatory: 0.15
    performance: 0.10

  # Severity thresholds
  fail_on:
    critical: 1    # Fail if any CRITICAL
    high: 3        # Fail if 3+ HIGH

  # Standards to check
  standards:
    security: ["OWASP Top 10", "CWE"]
    accessibility: ["WCAG 2.1 AA"]
    code: ["applicable linting rules", "applicable formatting tools"]
    regulatory: ["GDPR"]
    performance: ["Core Web Vitals"]
```

**Environment Variables:**
```bash
export DEEP_AUDIT_OUTPUT_DIR=".outputs/audit/"
export DEEP_AUDIT_WCAG_LEVEL="AA"
export DEEP_AUDIT_FAIL_ON_CRITICAL="true"
```

---

## Notes

- **Formal Verdict:** This is pass/fail auditing, not suggestions
- **Standards-Based:** Checks against established standards
- **Compliance Focus:** Regulatory and legal requirements
- **Blocking:** CRITICAL violations block deployment
- **Conversation-Driven:** Infers standards from context
- **Domain-Agnostic:** Works for any domain with standards
- **Parallel Execution:** All auditors run simultaneously
- **Multi-Model**: For cross-model audit confidence, see `deep-council`
- **Domain-Aware**: Auditor selection adapts to domain context via domain-registry
- **Context Routing**: If the artifact is complex or multi-domain, invoke the `context` skill first to classify artifact type and determine optimal routing (parallel-workflow vs debate-protocol vs deep-council)
- **DeepWiki (optional)**: For code artifacts, invoke `Skill("deepwiki")` before spawning auditors if the codebase has a Devin-indexed wiki — provides architectural context that improves standards mapping. Non-blocking; skip if unavailable.
