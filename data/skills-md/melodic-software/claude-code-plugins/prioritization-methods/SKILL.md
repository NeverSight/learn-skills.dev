---
name: prioritization-methods
description: "Requirements prioritization techniques including MoSCoW, Kano Model, WSJF (SAFe), and Wiegers' Value/Cost/Risk matrix. Provides scoring frameworks, trade-off analysis, and priority visualization. Use when ranking requirements by business value, customer impact, or implementation efficiency."
allowed-tools: Read, Write, Glob, Grep, Task
---

# Requirements Prioritization Methods

Comprehensive guide to prioritization techniques for requirements and features.

## When to Use This Skill

**Keywords:** prioritization, priority, MoSCoW, Kano model, WSJF, weighted shortest job first, value cost risk, Wiegers, priority matrix, must have should have, delighters, basic needs, performance features, cost of delay

**Use this skill when:**

- Ranking requirements by business value
- Choosing between competing features
- Allocating limited development capacity
- Communicating priority decisions to stakeholders
- Balancing customer satisfaction vs implementation effort
- Making trade-off decisions in product planning

## Prioritization Methods Overview

| Method | Best For | Complexity | Stakeholder Input |
| ------ | -------- | ---------- | ----------------- |
| **MoSCoW** | Quick categorization, MVP scope | Low | Low |
| **Kano Model** | Customer satisfaction analysis | Medium | High (surveys) |
| **WSJF** | Agile/SAFe environments, flow optimization | Medium | Medium |
| **Wiegers' Matrix** | Quantitative value/cost analysis | High | Medium |
| **Opportunity Scoring** | JTBD-aligned prioritization | Medium | High (surveys) |

## MoSCoW Method

### Categories

```yaml
moscow:
  must:
    definition: "Non-negotiable for this release"
    criteria:
      - "System won't work without it"
      - "Legal/regulatory requirement"
      - "Core to value proposition"
    typical_percentage: "60% of effort"

  should:
    definition: "Important but not critical"
    criteria:
      - "Significant value, but workarounds exist"
      - "Key stakeholder expectations"
      - "Competitive parity"
    typical_percentage: "20% of effort"

  could:
    definition: "Nice to have if time permits"
    criteria:
      - "Enhances user experience"
      - "Low effort, incremental value"
      - "Differentiator but not essential"
    typical_percentage: "20% of effort"

  wont:
    definition: "Explicitly out of scope for now"
    criteria:
      - "Agreed to defer, not rejected"
      - "Future consideration"
      - "Resource constraints"
    note: "Document for future reference"
```

### Application

```yaml
moscow_process:
  1. List all requirements
  2. Start with MUST - be strict (if everything is MUST, nothing is)
  3. Move to WON'T - explicitly exclude
  4. Distribute remaining between SHOULD and COULD
  5. Validate: MUSTs should be ~60% of capacity

  warning_signs:
    - "All requirements are MUST" → Be stricter
    - "No WON'Ts" → You're avoiding hard decisions
    - "MUSTs exceed capacity" → Re-evaluate or reduce scope
```

## Kano Model

### Feature Categories

```yaml
kano_categories:
  basic:
    name: "Basic (Must-Be)"
    description: "Expected features - absence causes dissatisfaction"
    examples:
      - "Website loads without errors"
      - "Login works correctly"
      - "Data is saved reliably"
    satisfaction_curve: "Only prevents dissatisfaction, doesn't create satisfaction"

  performance:
    name: "Performance (One-Dimensional)"
    description: "More is better - linear satisfaction"
    examples:
      - "Page load speed"
      - "Storage capacity"
      - "Number of integrations"
    satisfaction_curve: "Linear relationship to investment"

  excitement:
    name: "Excitement (Delighters)"
    description: "Unexpected features that create delight"
    examples:
      - "AI-powered suggestions"
      - "Personalized experience"
      - "Innovative shortcuts"
    satisfaction_curve: "High satisfaction, low expectation"

  indifferent:
    name: "Indifferent"
    description: "Features users don't care about"
    examples:
      - "Technical implementation details"
      - "Over-engineered features"
    action: "Deprioritize or remove"

  reverse:
    name: "Reverse"
    description: "Features some users actively dislike"
    examples:
      - "Mandatory tutorials"
      - "Intrusive notifications"
    action: "Make optional or remove"
```

### Kano Survey Method

```yaml
kano_survey:
  question_pair:
    functional: "How would you feel if [feature] was present?"
    dysfunctional: "How would you feel if [feature] was absent?"

  answer_options:
    - "I would like it"
    - "I expect it"
    - "I'm neutral"
    - "I can tolerate it"
    - "I dislike it"

  interpretation_matrix:
    # Functional → Dysfunctional → Category
    "Like → Dislike": "Excitement"
    "Like → Neutral": "Excitement"
    "Expect → Dislike": "Basic"
    "Neutral → Neutral": "Indifferent"
    "Like → Like": "Questionable (inconsistent)"
```

### Kano Visualization

```text
SATISFACTION
    ↑
    │           ╱ Excitement (Delighters)
    │         ╱
    │       ╱
    │     ╱
────┼─────────────── Performance
    │     ╲
    │       ╲
    │         ╲
    │           ╲ Basic (Must-Be)
    │
    └─────────────────────────────→ FULFILLMENT
         Not implemented    Fully implemented
```

## WSJF (Weighted Shortest Job First)

### Formula

```yaml
wsjf:
  formula: "WSJF = Cost of Delay / Job Size"

  cost_of_delay:
    components:
      user_value: "Value to end users/customers"
      time_criticality: "How much value decays with time"
      risk_reduction: "Risk/opportunity enabled by feature"

    formula: "CoD = User Value + Time Criticality + Risk Reduction"

  job_size:
    definition: "Relative effort to implement"
    scale: "Fibonacci (1, 2, 3, 5, 8, 13)"
```

### WSJF Scoring Template

```yaml
wsjf_example:
  feature: "Mobile App Offline Mode"

  cost_of_delay:
    user_value:
      score: 8
      rationale: "Highly requested by field workers"
    time_criticality:
      score: 5
      rationale: "Competitor launching similar feature in Q2"
    risk_reduction:
      score: 3
      rationale: "Reduces support tickets for connectivity issues"
    total_cod: 16

  job_size:
    score: 5
    rationale: "Moderate complexity, known patterns"

  wsjf_score: 3.2  # 16 / 5

  interpretation: "High priority - good value for effort"
```

### WSJF Comparison Table

| Feature | User Value | Time Crit | Risk Reduction | CoD | Size | WSJF | Rank |
| ------- | ---------- | --------- | -------------- | --- | ---- | ---- | ---- |
| Offline Mode | 8 | 5 | 3 | 16 | 5 | 3.2 | 1 |
| Dark Theme | 5 | 1 | 1 | 7 | 2 | 3.5 | 2 |
| Export PDF | 6 | 3 | 2 | 11 | 8 | 1.4 | 3 |

## Wiegers' Value/Cost/Risk Method

### Scoring Dimensions

```yaml
wiegers_method:
  dimensions:
    value:
      question: "What relative benefit does this provide?"
      scale: 1-9
      perspective: "Customer/business value"

    penalty:
      question: "What's the relative penalty of NOT having this?"
      scale: 1-9
      perspective: "Risk of omission"

    cost:
      question: "What's the relative cost to implement?"
      scale: 1-9
      perspective: "Development effort"

    risk:
      question: "What's the relative technical risk?"
      scale: 1-9
      perspective: "Uncertainty, complexity"

  formula: |
    Priority = (Value × ValueWeight + Penalty × PenaltyWeight) /
               (Cost × CostWeight + Risk × RiskWeight)

  default_weights:
    value: 2
    penalty: 1
    cost: 1
    risk: 0.5
```

### Wiegers Template

```yaml
wiegers_example:
  feature: "Two-Factor Authentication"

  scores:
    value: 7      # High security value
    penalty: 9    # Major penalty if missing (compliance risk)
    cost: 5       # Moderate implementation effort
    risk: 3       # Known patterns, low risk

  calculation:
    numerator: (7 × 2) + (9 × 1) = 23
    denominator: (5 × 1) + (3 × 0.5) = 6.5
    priority: 3.54

  interpretation: "High priority due to strong penalty for omission"
```

## Opportunity Scoring (JTBD)

### Importance vs Satisfaction

From the JTBD framework:

```yaml
opportunity_scoring:
  formula: "Opportunity = Importance + (Importance - Satisfaction)"

  data_collection:
    survey_questions:
      importance: "How important is it to [outcome]? (1-10)"
      satisfaction: "How satisfied are you with current ability? (1-10)"

  interpretation:
    score_15_20: "High opportunity - underserved"
    score_10_15: "Moderate opportunity"
    score_5_10: "Low opportunity - well served"
    score_below_5: "Over-served - deprioritize"

  example:
    outcome: "Quickly find relevant products"
    importance: 9
    satisfaction: 4
    score: 14  # 9 + (9-4)
    interpretation: "Moderate-high opportunity"
```

## Choosing a Method

```yaml
method_selection:
  use_moscow_when:
    - "Quick decisions needed"
    - "Stakeholders familiar with method"
    - "Defining MVP scope"
    - "Binary in/out decisions"

  use_kano_when:
    - "Understanding customer satisfaction drivers"
    - "Product differentiation focus"
    - "Have access to customer surveys"
    - "Balancing basic vs delighter features"

  use_wsjf_when:
    - "Agile/SAFe environment"
    - "Flow-based delivery"
    - "Economic decision-making"
    - "Comparing features of varying sizes"

  use_wiegers_when:
    - "Need quantitative justification"
    - "Multiple stakeholder perspectives"
    - "High-stakes prioritization decisions"
    - "Want to weight multiple factors"

  use_opportunity_when:
    - "JTBD-based product development"
    - "Customer research available"
    - "Finding underserved needs"
    - "Outcome-focused roadmap"
```

## Combining Methods

```yaml
combined_approach:
  step_1: "Use MoSCoW for initial categorization"
  step_2: "Apply Kano to understand SHOULD/COULD items better"
  step_3: "Use WSJF or Wiegers to rank within categories"
  step_4: "Validate with Opportunity Scoring against customer data"

  example_workflow:
    - "All MUSTs go to backlog (non-negotiable)"
    - "Kano analysis on SHOULDs reveals 3 delighters"
    - "WSJF ranking of delighters prioritizes by value/effort"
    - "Final backlog ordered with business justification"
```

## Output Format

### Priority Report Template

```yaml
priority_report:
  domain: "{domain}"
  method: "{method used}"
  date: "{ISO-8601}"

  summary:
    total_requirements: 25
    high_priority: 8
    medium_priority: 10
    low_priority: 7

  detailed_ranking:
    - rank: 1
      requirement_id: "REQ-001"
      title: "Two-Factor Authentication"
      method_score: 3.54
      rationale: "High penalty for omission, compliance requirement"

    - rank: 2
      requirement_id: "REQ-015"
      title: "Mobile Offline Mode"
      method_score: 3.2
      rationale: "High user value, competitive pressure"

  visualization: |
    [Mermaid or ASCII chart showing priority distribution]

  recommendations:
    - "Immediate focus on top 5 high-priority items"
    - "Consider deferring low-priority items with high cost"
    - "Re-evaluate in 2 weeks based on new information"
```

## Related Commands

- `/prioritize` - Apply prioritization methods to requirements
- `/gaps` - Identify missing requirements before prioritizing
- `/export` - Export prioritized requirements

## References

**For detailed guidance:**

- [MoSCoW Details](references/moscow-method.md) - Full MoSCoW application guide
- [Kano Survey Templates](references/kano-surveys.md) - Survey design and analysis
- [WSJF Worksheets](references/wsjf-worksheets.md) - Scoring templates

**External:**

- Karl Wiegers' "Software Requirements"
- SAFe Framework WSJF guidance
- Noriaki Kano's research on customer satisfaction

## Version History

- v1.0.0 (2025-12-26): Initial release - Prioritization Methods skill

---

**Last Updated:** 2025-12-26
