---
name: testing-level-selector
description: Select appropriate testing level based on project stage
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Testing Level Selector

Determine appropriate testing strategy based on project stage (POC, MVP, Alpha, Beta, Production) and project type (hobby, group, SaaS, enterprise).

## When to use me

Use this skill when:
- Starting a new project and need testing guidance
- Transitioning between project stages (MVP → Beta → Production)
- Determining testing investment for different project types
- Balancing testing effort with project resources and risks
- Planning testing strategy for team or organization

## What I do

1. **Analyze Project Context**
   - Determine project stage: POC, MVP, Alpha, Beta, Soft Launch, Full Launch
   - Identify project type: Hobby, Group, Small SaaS, Enterprise
   - Assess risk tolerance and quality requirements
   - Consider team size and resources available

2. **Recommend Testing Strategy**
   - Map project context to appropriate testing levels
   - Suggest specific test types and coverage
   - Recommend testing tools and frameworks
   - Provide implementation roadmap

3. **Generate Testing Plan**
   - Create prioritized test execution plan
   - Suggest automation strategy
   - Recommend quality gates and metrics
   - Provide risk-based testing approach

## Project Stage Definitions

**POC (Proof of Concept)**: Validate technical feasibility
**MVP (Minimum Viable Product)**: Core functionality for early users
**Alpha**: Internal testing with basic features
**Beta**: External testing with target audience
**Soft Launch**: Limited production release
**Full Launch**: Full production release

## Project Type Definitions

**Hobby Project**: Personal learning, no users/customers
**Group Project**: Small team, collaborative, limited users
**Small SaaS**: Business application, paying customers
**Enterprise**: Large scale, mission critical, compliance requirements

## Examples

```bash
# No direct commands - this is a strategic skill
# Use by asking questions about your project:

"What testing should I do for a Beta-stage Small SaaS?"
"What's appropriate for a hobby project MVP?"
"Enterprise POC testing requirements?"
```

## Output format

```
Testing Strategy Recommendation:
──────────────────────────────
Project Context:
  Stage: Beta
  Type: Small SaaS
  Risk: Medium-High (paying customers)
  Team: 5 developers, 1 QA

Recommended Testing Levels:

Essential (Must Have):
  ✅ Unit Testing: 80%+ coverage on critical paths
  ✅ Integration Testing: API & database integration
  ✅ E2E Testing: Critical user workflows (login, checkout)
  ✅ API Testing: All public endpoints
  ✅ Security Testing: Basic vulnerability scanning
  ✅ Performance Testing: Load testing for expected traffic

Recommended (Should Have):
  ⚠️ Accessibility Testing: Basic WCAG compliance
  ⚠️ Cross-Browser Testing: Top 3 browsers
  ⚠️ Mobile Testing: Responsive design validation

Optional (Could Have):
  🔄 Stress Testing: Breaking point analysis
  🔄 Usability Testing: User feedback sessions
  🔄 Compatibility Testing: Older browser support

Implementation Roadmap:
  1. Week 1-2: Set up unit & integration testing
  2. Week 3-4: Add E2E for critical paths
  3. Week 5-6: Implement security & performance testing
  4. Ongoing: Expand test coverage based on priorities

Quality Gates:
  - Unit tests pass before merge
  - Integration tests pass before staging
  - E2E tests pass before production
  - Zero critical security vulnerabilities
```

## Notes

- Testing investment should match project risk and stage
- Start with foundation (unit tests) and build up
- Automate repetitive tests, keep manual for exploratory
- Adapt strategy based on feedback and changing requirements
- Consider regulatory requirements for specific industries
- Balance test coverage with development velocity
- Review and adjust testing strategy regularly
