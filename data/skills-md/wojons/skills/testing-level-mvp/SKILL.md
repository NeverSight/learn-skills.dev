---
name: testing-level-mvp
description: Testing strategy for Minimum Viable Product
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# MVP Testing Strategy

Balanced testing approach for Minimum Viable Product with early users, focusing on core functionality reliability.

## When to use me

Use this skill when:
- Building first usable version for early adopters
- Validating product-market fit
- Releasing to limited user base (alpha/beta testers)
- Balancing speed with basic quality assurance
- Establishing foundation for future testing

## What I do

**Core Philosophy**: "Good enough" quality for early users. Focus on core functionality reliability over completeness.

**Essential Testing (Must Have)**:

1. **Unit Testing Foundation**
   - Critical business logic and algorithms
   - Complex or error-prone code
   - Core domain models and services
   - Target: 60-70% coverage on critical paths

2. **Integration Testing**
   - Key external integrations (database, payment, auth)
   - API contract testing for critical endpoints
   - Data persistence and retrieval
   - Error handling across boundaries

3. **Manual End-to-End Testing**
   - Core user workflows (signup, key feature, payment)
   - Happy path validation
   - Basic error scenarios
   - No full test automation required

4. **Basic Security Testing**
   - Authentication and authorization
   - Input validation on public endpoints
   - Dependency vulnerability scanning
   - Sensitive data protection

**Optional Testing (Add as needed)**:

- Performance testing for expected load
- Cross-browser testing for primary browser
- Basic accessibility (if public-facing)
- Smoke testing for deployment validation

**Project-Specific Adjustments**:

- **Hobby MVP**: Light unit testing, manual E2E
- **SaaS MVP**: Full essential suite, add performance
- **Enterprise MVP**: All essential plus compliance checks

## Examples

```bash
# MVP Testing Commands
npm run test:unit              # Unit tests for critical paths
npm run test:integration       # Key integration tests
npm run test:e2e:manual        # Manual test checklist

# Security basics
npm audit                     # Dependency vulnerabilities
npm run lint:security         # Basic security linting

# Deployment validation
npm run test:smoke            # Smoke tests after deployment

# Manual testing checklist
# 1. User registration flow
# 2. Core feature usage
# 3. Payment processing (if applicable)
# 4. Error handling scenarios
```

## Output format

```
MVP Testing Strategy:
──────────────────────────────
Testing Focus Areas:

Core User Journeys (3):
  ✅ User Registration & Onboarding
  ✅ Primary Feature Usage
  ✅ Basic Settings Management

Quality Metrics:
  - Unit Test Coverage: 72% (critical paths)
  - Integration Tests: 15 key scenarios
  - Manual E2E Tests: 5 core workflows
  - Security: No critical vulnerabilities

Testing Infrastructure:
  ✅ Unit test framework configured
  ✅ Basic CI/CD pipeline
  ⚠️ E2E automation not yet implemented
  ✅ Dependency vulnerability scanning

Risk Assessment:
  High Risk Areas:
    - Payment processing (manual testing only)
    - Data export feature (limited testing)
  
  Medium Risk:
    - User profile management
    
  Low Risk:
    - Static content pages

Recommendation:
  - Implement E2E automation for payment flow
  - Add performance testing if user growth exceeds 100
  - Expand unit testing as features stabilize
```

## Notes

- MVP users are more tolerant of bugs but expect core functionality to work
- Focus testing on "job to be done" not edge cases
- Document known issues and limitations
- Establish feedback loop with early users
- Build testing foundation that can scale
- Balance test automation with development velocity
- Consider A/B testing for feature validation
- Prepare to pivot based on user feedback
