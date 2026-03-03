---
name: gap-analysis
description: Analyze requirements for completeness, missing areas, and gaps. Uses domain checklists, NFR categories, and INVEST criteria to identify what's missing from elicited requirements.
allowed-tools: Read, Glob, Grep, Write, Task
---

# Gap Analysis Skill

Analyze requirements for completeness and identify missing areas.

## When to Use This Skill

**Keywords:** gap analysis, completeness, missing requirements, coverage, validation, INVEST, NFR check, requirement gaps

Invoke this skill when:

- Checking if elicited requirements are complete
- Validating coverage across requirement categories
- Identifying missing non-functional requirements
- Preparing requirements for specification
- Quality gate before specification export

## Gap Detection Methods

### 1. Category Coverage

Check coverage across standard requirement categories:

```yaml
categories:
  functional:
    - user_management
    - data_management
    - processing
    - integration
    - reporting
    - notifications

  non_functional:
    - performance
    - security
    - usability
    - reliability
    - scalability
    - maintainability
    - accessibility

  constraints:
    - technical
    - business
    - regulatory
    - resource
    - timeline

  assumptions:
    - environmental
    - user_behavior
    - dependencies
```

### 2. NFR Completeness

Ensure non-functional requirements are specified:

```yaml
nfr_checklist:
  performance:
    - response_time_defined: false
    - throughput_defined: false
    - capacity_defined: false

  security:
    - authentication_specified: false
    - authorization_specified: false
    - data_protection_specified: false

  usability:
    - accessibility_considered: false
    - learning_curve_addressed: false
    - error_handling_defined: false

  reliability:
    - uptime_target_set: false
    - error_recovery_defined: false
    - backup_strategy_specified: false

  scalability:
    - growth_projection_defined: false
    - scaling_strategy_specified: false
```

### 3. INVEST Criteria

Evaluate requirements against INVEST:

```yaml
invest_criteria:
  independent:
    description: "Requirement can be developed independently"
    check: "Are there circular dependencies?"

  negotiable:
    description: "Details can be negotiated"
    check: "Is the requirement too prescriptive?"

  valuable:
    description: "Delivers value to stakeholders"
    check: "Is the business value clear?"

  estimable:
    description: "Can be estimated for effort"
    check: "Is scope clear enough to estimate?"

  small:
    description: "Can be completed in a sprint"
    check: "Is the requirement too large?"

  testable:
    description: "Can be verified when implemented"
    check: "Are acceptance criteria defined?"
```

### 4. Domain-Specific Checklists

Apply domain-appropriate checklists:

```yaml
domain_checklists:
  e-commerce:
    - product_catalog
    - shopping_cart
    - checkout
    - payment
    - order_management
    - inventory
    - shipping
    - returns

  authentication:
    - login
    - registration
    - password_reset
    - session_management
    - mfa
    - sso
    - permissions

  reporting:
    - data_sources
    - filters
    - visualizations
    - export
    - scheduling
    - access_control
```

## Gap Detection Workflow

### Step 1: Load Current Requirements

Read existing requirements from:

- `.requirements/{domain}/` folder
- Interview results
- Document extractions
- Simulation outputs

### Step 2: Apply Checklists

For each checklist:

1. Check if category is covered
2. Note missing or weak areas
3. Assess severity of gaps

### Step 3: Assess Severity

```yaml
gap_severity:
  critical:
    definition: "Requirement area essential for system viability"
    examples: ["No security requirements", "No data validation"]
    action: "Must address before proceeding"

  major:
    definition: "Significant gap that affects quality"
    examples: ["No performance targets", "No error handling"]
    action: "Should address soon"

  minor:
    definition: "Nice to have, not essential"
    examples: ["No accessibility beyond basic", "Limited internationalization"]
    action: "Address if time permits"
```

### Step 4: Generate Recommendations

For each gap:

- Describe what's missing
- Suggest how to fill the gap
- Recommend elicitation technique

## Output Format

### Gap Analysis Report

```yaml
gap_analysis:
  session_id: "GAP-{timestamp}"
  domain: "{domain}"
  analyzed_date: "{ISO-8601}"

  requirements_analyzed:
    total: {number}
    from_interviews: {number}
    from_documents: {number}
    from_simulations: {number}

  coverage_summary:
    functional: 80%
    non_functional: 45%
    constraints: 60%
    assumptions: 30%

  gaps_identified:
    critical:
      - category: security
        gap: "No authentication requirements"
        recommendation: "Interview security stakeholder or run simulation"
        suggested_technique: interview

    major:
      - category: performance
        gap: "No response time targets"
        recommendation: "Define SLAs with business stakeholder"
        suggested_technique: interview

    minor:
      - category: accessibility
        gap: "Only basic WCAG coverage"
        recommendation: "Consider WCAG 2.1 AA compliance"
        suggested_technique: domain-research

  nfr_coverage:
    performance: partial
    security: missing
    usability: covered
    reliability: partial
    scalability: missing

  invest_assessment:
    independent: 85%
    negotiable: 90%
    valuable: 95%
    estimable: 70%
    small: 75%
    testable: 60%

  recommendations:
    - priority: high
      action: "Conduct security-focused interview"
      gaps_addressed: [security, authentication, authorization]

    - priority: medium
      action: "Define performance SLAs"
      gaps_addressed: [performance, scalability]

  ready_for_specification: false
  blocker_gaps: [security, authentication]
```

## Gap Categories

### Missing Functional Areas

Common functional gaps:

- Error handling not specified
- Edge cases not covered
- Integration points unclear
- Notification requirements missing
- Reporting requirements absent

### Missing NFRs

Common NFR gaps:

- No performance targets
- Security requirements vague
- Accessibility not considered
- No availability targets
- Scalability undefined

### Missing Constraints

Common constraint gaps:

- Technical constraints undocumented
- Budget constraints unclear
- Timeline not specified
- Regulatory requirements missing

### Missing Assumptions

Common assumption gaps:

- User expertise level undefined
- Environmental assumptions unstated
- Dependency assumptions hidden

## Delegation

For filling gaps, delegate to:

- **interview-conducting**: For stakeholder interviews
- **stakeholder-simulation**: For solo gap filling
- **domain-research**: For domain-specific requirements

## Output Location

Save gap analysis to:

```text
.requirements/{domain}/analysis/GAP-{timestamp}.yaml
```

## Related

- `elicitation-methodology` - Parent hub skill
- `interview-conducting` - Fill gaps via interviews
- `stakeholder-simulation` - Fill gaps via simulation
- `domain-research` - Research domain requirements
