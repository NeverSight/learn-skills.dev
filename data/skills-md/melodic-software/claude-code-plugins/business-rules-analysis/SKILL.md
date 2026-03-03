---
name: business-rules-analysis
description: "Business rules elicitation and analysis techniques. Covers rule types (constraints, derivations, inferences), decision tables, rule templates, and policy documentation. Use when identifying business policies, constraints, calculations, and decision logic during requirements elicitation."
allowed-tools: Read, Write, Glob, Grep, Task
---

# Business Rules Analysis

Comprehensive framework for eliciting, documenting, and validating business rules during requirements discovery.

## When to Use This Skill

**Keywords:** business rules, policies, constraints, calculations, derivations, inferences, decision tables, decision logic, rule templates, validation rules, authorization rules, computation rules, condition-action, if-then rules

**Use this skill when:**

- Identifying business policies and constraints
- Documenting calculation and derivation rules
- Creating decision tables for complex logic
- Eliciting authorization and validation rules
- Translating policies into requirement statements
- Analyzing rule interactions and conflicts
- Validating rule completeness and consistency

## Business Rule Categories

### Structural Rules (Facts)

Define the nature of things and relationships:

```yaml
structural_rules:
  definition: "Rules that define terms, concepts, and their relationships"

  types:
    terms:
      description: "Definitions of business concepts"
      example: "A 'Premium Customer' is a customer who has spent more than $10,000 in the last 12 months"

    facts:
      description: "Assertions about the business domain"
      example: "Each Order must have exactly one Customer"

    relationships:
      description: "How concepts relate to each other"
      example: "A Customer may have zero or more Orders"

  documentation_template:
    term: "{Term} is defined as {definition}"
    fact: "{Subject} {verb} {object}"
    relationship: "{Entity A} {cardinality} {Entity B}"
```

### Derivation Rules (Computations)

Calculate or derive values from other data:

```yaml
derivation_rules:
  definition: "Rules that compute values from other information"

  types:
    calculations:
      description: "Mathematical computations"
      example: "Order Total = Sum of (Line Item Quantity × Unit Price)"

    aggregations:
      description: "Summary calculations across sets"
      example: "Monthly Revenue = Sum of all Order Totals for the month"

    transformations:
      description: "Data conversions"
      example: "Full Name = First Name + ' ' + Last Name"

  documentation_template:
    calculation: "{Result} = {formula}"
    with_conditions: "IF {condition} THEN {Result} = {formula}"
```

### Constraint Rules (Restrictions)

Limit what can happen or exist:

```yaml
constraint_rules:
  definition: "Rules that restrict or mandate conditions"

  types:
    mandatory:
      description: "Must always be true"
      example: "Every Order must have at least one Line Item"

    prohibited:
      description: "Must never occur"
      example: "An Order cannot be shipped to a country on the embargo list"

    conditional:
      description: "Restrictions that apply under certain conditions"
      example: "IF Customer is under 18 THEN alcohol products cannot be ordered"

    range:
      description: "Numeric or value boundaries"
      example: "Order Quantity must be between 1 and 999"

  documentation_template:
    must: "{Subject} must {condition}"
    must_not: "{Subject} must not {condition}"
    if_then: "IF {condition} THEN {subject} {must/must not} {action}"
```

### Action Rules (Behaviors)

Define what should happen when conditions are met:

```yaml
action_rules:
  definition: "Rules that trigger actions based on conditions"

  types:
    authorization:
      description: "Who can do what"
      example: "Only Managers can approve orders over $5,000"

    triggers:
      description: "Events that initiate actions"
      example: "When inventory falls below reorder point, create purchase order"

    workflows:
      description: "Sequences of actions"
      example: "After order is placed, send confirmation email, then notify warehouse"

  documentation_template:
    authorization: "{Role} may/must/must not {action} {object} [when {condition}]"
    trigger: "WHEN {event} THEN {action}"
    workflow: "AFTER {event}, {action1}, THEN {action2}"
```

### Inference Rules (Deductions)

Derive new facts from existing information:

```yaml
inference_rules:
  definition: "Rules that infer new information from existing facts"

  types:
    classification:
      description: "Categorize based on criteria"
      example: "IF Customer lifetime value > $50,000 THEN Customer is 'VIP'"

    status:
      description: "Determine state based on conditions"
      example: "IF all line items shipped THEN Order status is 'Complete'"

    eligibility:
      description: "Determine if conditions are met"
      example: "Customer is eligible for discount IF loyalty points > 1000"

  documentation_template:
    inference: "IF {conditions} THEN {conclusion}"
    classification: "{Entity} is classified as {category} WHEN {criteria}"
```

## Decision Tables

For complex rules with multiple conditions:

```yaml
decision_table:
  structure:
    conditions: "Rows listing input conditions"
    actions: "Rows listing possible actions"
    rules: "Columns combining conditions and actions"

  example:
    name: "Order Discount Rules"
    conditions:
      C1: "Customer Type"
      C2: "Order Amount"
      C3: "Payment Method"

    actions:
      A1: "Apply Discount %"
      A2: "Free Shipping"

    rules:
      R1:
        C1: "VIP"
        C2: "> $500"
        C3: "Any"
        A1: "20%"
        A2: "Yes"

      R2:
        C1: "Regular"
        C2: "> $100"
        C3: "Credit Card"
        A1: "10%"
        A2: "No"

      R3:
        C1: "Any"
        C2: "Any"
        C3: "Any"
        A1: "0%"
        A2: "No"
```

### Decision Table Template

```text
┌─────────────────────────────────────────────────────────────┐
│ Decision Table: {Name}                                      │
├─────────────────┬───────┬───────┬───────┬───────┬───────────┤
│ CONDITIONS      │  R1   │  R2   │  R3   │  R4   │  Default  │
├─────────────────┼───────┼───────┼───────┼───────┼───────────┤
│ {Condition 1}   │   Y   │   Y   │   N   │   N   │     -     │
│ {Condition 2}   │   Y   │   N   │   Y   │   N   │     -     │
├─────────────────┼───────┼───────┼───────┼───────┼───────────┤
│ ACTIONS         │       │       │       │       │           │
├─────────────────┼───────┼───────┼───────┼───────┼───────────┤
│ {Action 1}      │   X   │       │   X   │       │           │
│ {Action 2}      │       │   X   │   X   │       │     X     │
└─────────────────┴───────┴───────┴───────┴───────┴───────────┘
```

## Rule Documentation Templates

### Standard Rule Template

```yaml
rule_template:
  id: "BR-{domain}-{number}"
  name: "{descriptive name}"
  category: "constraint|derivation|inference|action|structural"
  statement: "{clear, unambiguous rule statement}"

  source:
    origin: "{stakeholder, document, regulation}"
    date: "{when identified}"
    authority: "{who can change this rule}"

  conditions:
    - "{condition 1}"
    - "{condition 2}"

  actions:
    - "{action if conditions met}"

  exceptions:
    - "{exception case}"

  examples:
    positive:
      - "{example where rule applies}"
    negative:
      - "{example where rule does not apply}"

  related_rules:
    - "{BR-xxx}"

  validation:
    testable: true
    test_approach: "{how to verify}"

  metadata:
    priority: "high|medium|low"
    volatility: "stable|volatile"
    enforcement: "automatic|manual"
```

### SBVR-Style Template

Semantics of Business Vocabulary and Business Rules (OMG standard):

```yaml
sbvr_template:
  vocabulary:
    term: "{term}"
    definition: "{meaning in business context}"

  structural_rule:
    format: "It is obligatory/permitted/forbidden that {statement}"
    example: "It is obligatory that each order has at least one line item"

  operative_rule:
    format: "If {condition} then {consequence}"
    example: "If order total exceeds $1000 then manager approval is required"
```

## Elicitation Techniques

### Rule Discovery Questions

```yaml
discovery_questions:
  constraints:
    - "What must always be true?"
    - "What must never happen?"
    - "What limits or boundaries exist?"
    - "What conditions must be met before X?"

  calculations:
    - "How is X calculated?"
    - "What formula determines Y?"
    - "What data is needed to compute Z?"

  authorizations:
    - "Who can approve this?"
    - "What permissions are needed?"
    - "Who has the authority to change this?"

  triggers:
    - "What causes this to happen?"
    - "What happens when X occurs?"
    - "What events initiate this process?"

  exceptions:
    - "Are there any special cases?"
    - "What happens if conditions aren't met?"
    - "What overrides this rule?"
```

### Document Analysis

```yaml
document_sources:
  primary:
    - "Policy manuals"
    - "Regulatory documents"
    - "Contracts and agreements"
    - "Procedure documents"

  secondary:
    - "Exception logs"
    - "Help desk tickets"
    - "Training materials"
    - "System documentation"

  indicators:
    must_words: ["must", "shall", "required", "mandatory"]
    prohibition_words: ["must not", "cannot", "prohibited", "forbidden"]
    condition_words: ["if", "when", "unless", "except", "provided that"]
    calculation_words: ["equals", "calculated", "derived", "sum of"]
```

## Rule Validation

### Completeness Checks

```yaml
completeness_validation:
  questions:
    - "Are all conditions specified?"
    - "Is the default case defined?"
    - "Are exceptions documented?"
    - "Is the rule source identified?"
    - "Can the rule be tested?"

  checklist:
    - "[ ] All terms defined in glossary"
    - "[ ] All conditions explicit"
    - "[ ] Actions clearly specified"
    - "[ ] Exceptions documented"
    - "[ ] Examples provided"
    - "[ ] Source and authority identified"
```

### Consistency Checks

```yaml
consistency_validation:
  rule_conflicts:
    - "Do any rules contradict each other?"
    - "Are there overlapping conditions with different outcomes?"

  terminology:
    - "Are terms used consistently across rules?"
    - "Do definitions match glossary?"

  coverage:
    - "Are there gaps in the decision logic?"
    - "Is the rule set complete for all scenarios?"
```

## Rule Traceability

```yaml
traceability:
  upstream:
    - "Source document/stakeholder"
    - "Business objective supported"
    - "Regulation/policy reference"

  downstream:
    - "Requirements implementing this rule"
    - "Test cases validating this rule"
    - "System components enforcing this rule"

  matrix:
    format: "Rule ID → Requirement ID → Test ID → Component ID"
```

## Output Format

### Business Rules Catalog

```yaml
rules_catalog:
  domain: "{domain}"
  version: "1.0"
  last_updated: "{ISO-8601}"

  glossary:
    - term: "Premium Customer"
      definition: "Customer with lifetime value > $50,000"

  rules:
    - id: "BR-ORD-001"
      name: "Minimum Order Quantity"
      category: "constraint"
      statement: "Order quantity must be at least 1"
      enforcement: "automatic"
      priority: "high"

    - id: "BR-ORD-002"
      name: "VIP Discount Calculation"
      category: "derivation"
      statement: "VIP customers receive 20% discount on orders over $100"
      formula: "Discount = OrderTotal × 0.20 IF CustomerType = 'VIP' AND OrderTotal > 100"

  decision_tables:
    - name: "Shipping Method Selection"
      conditions: [...]
      actions: [...]
      rules: [...]

  validation_summary:
    total_rules: 25
    by_category:
      constraint: 12
      derivation: 5
      inference: 4
      action: 4
    conflicts_found: 0
    gaps_identified: 2
```

## Integration Points

### With Other Elicitation Commands

```bash
# Discover rules during interviews
/requirements-elicitation:interview --focus "business-rules"

# Extract rules from documents
/requirements-elicitation:extract --source "policies.pdf" --type "rules"

# Validate rules with stakeholders
/requirements-elicitation:simulate --domain "orders" --focus "rule-validation"
```

### Rule-to-Requirement Transformation

```yaml
transformation:
  constraint_to_requirement:
    rule: "Order quantity must be between 1 and 999"
    requirement: "System shall validate that order quantity is within range 1-999"

  derivation_to_requirement:
    rule: "Order Total = Sum of (Quantity × Unit Price)"
    requirement: "System shall calculate order total as sum of line item amounts"

  authorization_to_requirement:
    rule: "Only Managers can approve orders over $5,000"
    requirement: "System shall require Manager role for approval of orders exceeding $5,000"
```

## References

For detailed techniques:

- [Rule Elicitation Techniques](references/rule-elicitation-techniques.md)
- [Decision Table Patterns](references/decision-table-patterns.md)
- [Rule Conflict Resolution](references/rule-conflict-resolution.md)

## Version History

- v1.0.0 (2025-12-26): Initial release - Business Rules Analysis skill

---

**Last Updated:** 2025-12-26
