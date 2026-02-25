---
name: customer-centric-design
description: Customer-obsessed design methodology. Use when designing features, validating problems, choosing research methods, or measuring design success.
version: 1.0.0
---

# Customer-Centric Design

This skill guides engineers and designers toward the right methodology for understanding users and validating solutions. It emphasizes solving real problems for real people.

## Use-When

This skill activates when:
- Agent designs a new feature or product
- Agent asks "how do I know this is a real problem?"
- Agent needs to choose between qualitative vs quantitative research
- Agent wants to validate a design before building
- Agent asks "what metrics should I track?"
- Agent receives user feedback requesting a feature
- Agent needs to measure design impact

## Core Rules

- ALWAYS validate the problem exists before designing a solution
- ALWAYS define success metrics before building
- ALWAYS choose methodology based on knowledge gap, not preference
- NEVER assume you know what users need without evidence
- ALWAYS validate design with actual users before shipping

## Common Agent Mistakes

- Building features based on assumptions without problem validation
- Choosing research methods randomly instead of matching to situation
- Tracking vanity metrics that don't correlate with user success
- Skipping user validation because "it's obvious"
- Measuring activity instead of outcomes

## Methodology Decision Tree

Use this decision framework to choose your approach:

```
Is the problem well-understood?
├── YES: Do users already complain about it?
│   ├── YES → Validate with analytics + quick usability test
│   └── NO → Optimize existing flow, measure impact
└── NO: Is this a new problem space?
    ├── YES → Qualitative research (interviews, observations)
    └── UNCERTAIN → Hybrid: qualitative discovery + quantitative validation
```

## Examples

### ✅ Correct

```tsx
// Before: Validating the problem exists
// Step 1: Talk to 5 customers about the pain point
// Step 2: Check support tickets for related issues
// Step 3: Analyze product analytics for drop-off points

// Step 4: Define success metrics BEFORE building
const successMetrics = {
  leading: "time-to-complete",    // What we can move
  lagging: "completion-rate",     // The outcome
  guardrail: "error-rate",        // What we must not hurt
}

// Step 5: Validate with prototype before full build
// Run usability test with 5 users on Figma prototype
```

### ❌ Wrong

```tsx
// Wrong: Building without problem validation
// "Users probably want dark mode, let's add it"

// Wrong: Choosing methodology arbitrarily
// "Let's run a survey" (when you need deep understanding)

// Wrong: Vanity metrics
analytics.track("button-clicks")  // Activity, not outcome

// Wrong: No validation before shipping
// "It looks good, let's ship and see what happens"
```

## References

- [The Mom Test](https://momtestbook.com/) - Customer conversations
- [Inspired: How to Create Products](https://www.amazon.com/Inspired-How-Create-Products-Customers/dp/0521186224)
- [Google HEART Framework](https://www.uxmatters.com/mt/archives/2012/04/selecting-usability-metrics-for-user-experience-design-validation.php)
- [Lean Analytics](https://leananalyticsbook.com/)
