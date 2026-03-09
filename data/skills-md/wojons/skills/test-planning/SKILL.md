---
name: test-planning
description: Create comprehensive test plans considering all test types and dependencies
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Test Planning

Create comprehensive test plans considering all test types, dependencies, risks, and project constraints to ensure effective quality assurance.

## When to use me

Use this skill when:
- Starting new projects or major features
- Planning testing strategy for releases
- Allocating testing resources and timelines
- Defining quality gates and acceptance criteria
- Coordinating testing across teams or systems
- Balancing test coverage with project constraints
- Documenting testing approach for stakeholders

## What I do

- **Test strategy development**:
  - Analyze project requirements and risks
  - Select appropriate test types based on context
  - Define test objectives and success criteria
  - Establish quality gates and metrics

- **Resource planning**:
  - Estimate testing effort and timeline
  - Allocate human and technical resources
  - Plan test environment requirements
  - Schedule test execution phases

- **Risk-based planning**:
  - Identify high-risk areas requiring focused testing
  - Prioritize test coverage based on impact and likelihood
  - Plan exploratory testing for unknown risks
  - Design contingency plans for test failures

- **Integration planning**:
  - Coordinate with development and deployment schedules
  - Plan test data management and environment setup
  - Schedule test execution in CI/CD pipelines
  - Coordinate with other teams and stakeholders

## Test Planning Components

1. **Test Objectives**: What are we trying to achieve?
2. **Test Scope**: What's included and excluded?
3. **Test Approach**: How will testing be conducted?
4. **Test Schedule**: When will testing happen?
5. **Resources**: Who and what is needed?
6. **Deliverables**: What will be produced?
7. **Risks and Mitigations**: What could go wrong?

## Examples

```bash
# Generate test plans
npm run test:plan:generate          # Generate comprehensive test plan
npm run test:plan:strategy          # Create test strategy document
npm run test:plan:estimate          # Estimate testing effort

# Feature-specific planning
npm run test:plan:feature -- "user-authentication"
npm run test:plan:release -- "v2.1.0"

# Context-aware planning
npm run test:plan -- --context mvp --type saas
npm run test:plan -- --context production --type enterprise

# Integration with project management
npm run test:plan:export -- --format jira    # Jira import format
npm run test:plan:export -- --format csv      # CSV for spreadsheets
npm run test:plan:export -- --format markdown # Markdown documentation

# Risk-based planning
npm run test:plan:risks            # Risk assessment and planning
npm run test:plan:coverage         # Test coverage planning
```

## Output format

```
Comprehensive Test Plan
──────────────────────────────
Project: E-Commerce Platform v2.1
Stage: Beta → Production Release
Planning Date: 2024-03-15

Test Objectives:
  - Validate new checkout flow functionality
  - Ensure backward compatibility with existing features
  - Meet performance SLAs for peak traffic
  - Maintain security compliance (PCI-DSS)
  - Provide confidence for production release

Test Scope:
  Included:
    - New checkout API and UI
    - Payment gateway integration updates
    - Order processing enhancements
    - User notification system
  
  Excluded:
    - Legacy admin panel (separate release)
    - Mobile app updates (different team)
    - Third-party analytics integration

Test Approach:
  Test Pyramid Implementation:
    - Unit Tests: 80% coverage on new code (estimated: 250 tests)
    - Integration Tests: API and database integration (estimated: 75 tests)
    - E2E Tests: Critical user journeys (estimated: 25 scenarios)
  
  Specialized Testing:
    - Performance: Load testing with 2000 concurrent users
    - Security: PCI-DSS compliance validation
    - Accessibility: WCAG 2.1 AA compliance
    - Compatibility: Chrome, Firefox, Safari, mobile browsers

Test Schedule:
  Week 1-2: Development & Unit Testing
  Week 3: Integration Testing & API Validation
  Week 4: E2E Testing & User Acceptance
  Week 5: Performance & Security Testing
  Week 6: Final Validation & Production Readiness

Resource Allocation:
  - Developers: 3 (unit & integration tests)
  - QA Engineers: 2 (E2E & exploratory testing)
  - Performance Engineer: 1 (load testing)
  - Security Specialist: 1 (compliance validation)
  - Environments: Dev, CI, Staging, Performance Lab

Test Environment Requirements:
  - Staging environment matching production configuration
  - Test database with production-like data volume
  - Payment gateway sandbox accounts
  - Load testing infrastructure
  - Security scanning tools

Quality Gates:
  1. All unit tests pass (CI gate)
  2. Integration tests 100% pass (CI gate)
  3. E2E critical paths 100% pass (staging gate)
  4. Performance SLAs met (performance gate)
  5. No critical security vulnerabilities (security gate)
  6. User acceptance sign-off (UAT gate)

Risk Assessment:
  High Risk:
    - Payment processing integration (mitigation: extended sandbox testing)
    - Database migration (mitigation: rollback testing)
  
  Medium Risk:
    - Checkout UI changes (mitigation: extensive E2E testing)
    - Performance under load (mitigation: progressive load testing)
  
  Low Risk:
    - Notification system updates (mitigation: smoke testing)

Dependencies:
  - Development completion by Week 2
  - Staging environment availability
  - Test data preparation
  - Third-party service sandbox access
  - Performance testing window (off-peak hours)

Success Metrics:
  - Defect detection rate > 90%
  - Test automation coverage > 70%
  - Mean time to defect resolution < 8 hours
  - Zero critical defects in production first week

Contingency Plans:
  - Schedule buffer: 1 week for unexpected issues
  - Rollback procedure documented and tested
  - Feature flags for gradual rollout
  - Monitoring plan for production release

Deliverables:
  - Test strategy document
  - Test cases and automation scripts
  - Test execution reports
  - Defect tracking and resolution
  - Release readiness assessment
  - Lessons learned document
```

## Notes

- Test plans should be living documents, updated as needed
- Involve stakeholders in test planning process
- Balance comprehensive planning with agility
- Consider both functional and non-functional requirements
- Document assumptions and constraints explicitly
- Align test planning with business objectives
- Use historical data to improve planning accuracy
- Communicate test plan clearly to all involved parties
- Review and adjust plans based on actual progress
- Capture lessons learned for future planning improvements
