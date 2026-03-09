---
name: devils-advocate
description: Challenge ideas, assumptions, and decisions by playing devil's advocate to identify weaknesses and prevent groupthink
license: MIT
compatibility: opencode
metadata:
  audience: developers, product managers, decision-makers
  category: critical-thinking
---

# Devil's Advocate

Systematically challenge ideas, assumptions, designs, and decisions by playing devil's advocate to identify weaknesses, blind spots, and alternative perspectives before committing to a course of action.

## When to use me

Use this skill when:
- A team seems to be converging on a solution without debate
- Important decisions are being made based on consensus rather than evidence
- You need to stress-test ideas before implementation
- Identifying potential failure modes and risks
- Preventing groupthink and confirmation bias
- Evaluating multiple alternatives before choosing
- Preparing for stakeholder challenges or objections
- Building resilience against criticism and failure

## What I do

### 1. Argument Deconstruction
- **Identify core claims and assumptions** in proposals, designs, or decisions
- **Analyze supporting evidence** for strength, relevance, and reliability
- **Map logical connections** between premises and conclusions
- **Detect rhetorical fallacies** and cognitive biases in reasoning
- **Surface implicit beliefs** that aren't explicitly stated

### 2. Counterargument Generation
- **Generate alternative explanations** for the same evidence
- **Propose competing hypotheses** that could also be true
- **Identify contradictory data** or opposing viewpoints
- **Suggest different interpretations** of facts and findings
- **Construct "what if" scenarios** where current thinking is wrong

### 3. Weakness Identification
- **Find logical gaps** in arguments and reasoning
- **Identify unexamined risks** and potential failure modes
- **Spot overconfidence** in predictions or estimates
- **Detect oversimplification** of complex problems
- **Recognize missing perspectives** or stakeholder views

### 4. Alternative Perspective Exploration
- **Adopt different stakeholder viewpoints** (users, customers, regulators, competitors)
- **Consider opposite positions** on controversial issues
- **Explore edge cases** and boundary conditions
- **Apply different mental models** or frameworks
- **Question fundamental premises** rather than just conclusions

## Devil's Advocate Techniques

### For Technical Decisions:
- **Challenge technology choices**: "What if this framework becomes unmaintained?"
- **Question architecture decisions**: "How does this handle ten times the expected load?"
- **Probe security assumptions**: "What attack vectors are we not considering?"
- **Test scalability claims**: "What breaks first under stress?"
- **Examine dependency risks**: "What happens if this third-party service changes?"

### For Product/Feature Decisions:
- **Challenge user assumptions**: "What if users don't behave as we expect?"
- **Question market fit**: "What evidence contradicts our market assumptions?"
- **Probe value propositions**: "Why would customers choose alternatives?"
- **Test business models**: "What assumptions make this revenue model fail?"
- **Examine competitive threats**: "How could competitors easily undermine this?"

### For Process/Operational Decisions:
- **Challenge workflow efficiency**: "What makes this process fragile?"
- **Question measurement validity**: "Are we measuring the right things?"
- **Probe team dynamics**: "What interpersonal issues could derail this?"
- **Test communication plans**: "Where could misunderstandings occur?"
- **Examine incentive alignment**: "What perverse incentives does this create?"

## Examples

```bash
# Challenge a technical design decision
npm run devils-advocate:challenge -- --decision "use-microservices" --context "ecommerce-platform"

# Test a product assumption  
npm run devils-advocate:test -- --assumption "users-want-mobile-app" --data "user-research.json"

# Identify weaknesses in a proposal
npm run devils-advocate:weaknesses -- --proposal "architecture-redesign.pdf" --perspective "security"

# Generate counterarguments for a business case
npm run devils-advocate:counterarguments -- --business-case "expand-to-europe.md" --stakeholder "competitor"

# Comprehensive devil's advocate review
npm run devils-advocate:review -- --document "project-plan.md" --thoroughness high
```

## Output format

```
Devil's Advocate Analysis
──────────────────────────────
Subject: Microservices Architecture Proposal
Date: 2026-02-26
Analysis Duration: 45 minutes

Core Claims Identified:
1. "Microservices will improve development velocity by 40%"
2. "Team autonomy will increase with bounded contexts"
3. "System will be more resilient to failures"
4. "Scaling will be more efficient and cost-effective"
5. "Technology diversity will enable better tool selection"

Argument Analysis:

1. Claim: "Microservices improve development velocity by 40%"
   Supporting Evidence: Case studies from other companies
   
   Devil's Advocate Challenges:
   - Case studies may not apply to our context (different scale, team structure)
   - 40% improvement assumes optimal implementation and mature DevOps
   - Velocity gains may be offset by coordination overhead
   - Microservices introduce new failure modes (network, versioning, data consistency)
   - Learning curve could reduce velocity initially
   
   Alternative Explanation: 
   The perceived velocity improvement may come from better practices 
   (CI/CD, testing) that could be applied to monoliths too.

2. Claim: "Team autonomy increases with bounded contexts"
   Supporting Evidence: Conway's Law, team structure diagrams
   
   Devil's Advocate Challenges:
   - Bounded contexts require clear domain boundaries (do we have them?)
   - Teams need new skills (distributed systems, SRE practices)
   - Increased autonomy may lead to inconsistent standards
   - Cross-team coordination becomes more formal and slower
   - Some domains naturally span multiple services
   
   Alternative Perspective:
   Monolith with modular architecture might provide similar autonomy benefits 
   without operational complexity.

3. Claim: "System more resilient to failures"
   Supporting Evidence: Failure isolation diagrams, redundancy claims
   
   Devil's Advocate Challenges:
   - Distributed systems have MORE failure modes (network partitions, service discovery)
   - Resilience requires sophisticated infrastructure (circuit breakers, retries, fallbacks)
   - Debugging failures across services is harder
   - Data consistency becomes a major challenge
   - Cascading failures possible if dependencies not managed
   
   Contradictory Evidence:
   Many companies report increased operational complexity and failure rates 
   after microservices adoption without proper preparation.

Risk Assessment:
- High Risk: Data consistency across services
- Medium Risk: Operational complexity overwhelming team
- Medium Risk: Cross-team coordination overhead
- Low Risk: Technology choice limitations

Alternative Approaches Worth Considering:
1. Modular monolith with clear internal boundaries
2. Start with coarse-grained services, refine later
3. Hybrid approach: monolith for core domain, services for edge functions
4. Focus on DevOps maturity first, then evaluate service boundaries

Critical Questions Unanswered:
1. What specific metrics will measure "improved velocity"?
2. How will we handle distributed transactions?
3. What is the rollback plan if microservices don't deliver value?
4. How will team structure change to support service ownership?
5. What monitoring and observability investments are needed?

Recommendations:
1. Pilot with one non-critical service first
2. Define clear success metrics before proceeding
3. Invest in foundational capabilities (monitoring, deployment, testing)
4. Consider evolutionary architecture rather than big-bang rewrite
5. Document assumptions and revisit after 3 months

Analysis Value:
- Weaknesses identified: 8 significant, 3 critical
- Alternative perspectives generated: 5 viable alternatives
- Assumptions challenged: 12 core assumptions
- Risk areas highlighted: 3 high-risk areas needing mitigation
- Decision quality improvement: High (prevents potential costly mistake)
```

## Notes

- Devil's advocate is a role, not a personality – it's temporary and purposeful
- The goal is better decisions, not winning arguments or blocking progress
- Balance skepticism with constructive alternatives
- Document challenges and responses for future reference
- Use devil's advocate selectively for important decisions, not every discussion
- The most valuable challenges are those that are hardest to answer
- Pair devil's advocate with other perspectives for balanced analysis
- Time-box devil's advocate analysis to prevent analysis paralysis
- Focus on substance, not style – challenge ideas, not people
- The best devil's advocate questions are those that make everyone think differently