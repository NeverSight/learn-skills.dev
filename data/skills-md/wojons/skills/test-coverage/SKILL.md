---
name: test-coverage
description: Measure and report test coverage across all test types
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Test Coverage

Measure, analyze, and report test coverage across all test types, including code coverage, requirement coverage, risk coverage, and quality attribute coverage.

## When to use me

Use this skill when:
- Assessing overall test effectiveness
- Identifying coverage gaps in testing strategy
- Reporting test coverage to stakeholders
- Planning test improvement initiatives
- Validating test completeness for releases
- Comparing actual vs planned test coverage
- Tracking coverage trends over time

## What I do

- **Multi-dimensional coverage analysis**:
  - Code coverage: statements, branches, functions, lines
  - Requirement coverage: functional and non-functional requirements
  - Risk coverage: high-risk areas and scenarios
  - Quality attribute coverage: performance, security, usability, etc.
  - User scenario coverage: user journeys and workflows

- **Coverage measurement**:
  - Automated coverage collection from test execution
  - Manual coverage assessment for exploratory testing
  - Integration with test management tools
  - Historical coverage trend analysis

- **Gap analysis and recommendations**:
  - Identify under-tested areas and components
  - Recommend test type mix adjustments
  - Suggest coverage improvement strategies
  - Prioritize coverage gaps based on risk

- **Reporting and visualization**:
  - Generate coverage reports for different stakeholders
  - Create coverage dashboards and visualizations
  - Track coverage against targets and benchmarks
  - Provide coverage insights for decision making

## Coverage Dimensions

1. **Code Coverage**: What code is executed by tests?
2. **Requirement Coverage**: What requirements are validated by tests?
3. **Risk Coverage**: What risks are mitigated by tests?
4. **Scenario Coverage**: What user scenarios are tested?
5. **Data Coverage**: What data variations are tested?
6. **Configuration Coverage**: What configurations are tested?

## Examples

```bash
# Measure overall test coverage
npm run test:coverage:measure       # Comprehensive coverage measurement
npm run test:coverage:report        # Generate coverage report

# Specific coverage types
npm run test:coverage:code          # Code coverage analysis
npm run test:coverage:requirements  # Requirement coverage analysis
npm run test:coverage:risks         # Risk coverage analysis
npm run test:coverage:scenarios     # Scenario coverage analysis
npm run test:coverage:data          # Data coverage analysis

# Integration with test types
npm run test:coverage -- --include unit,integration,e2e
npm run test:coverage -- --exclude performance,security
npm run test:coverage -- --type functional
npm run test:coverage -- --type nonfunctional

# Coverage visualization
npm run test:coverage:visualize     # Generate coverage visualizations
npm run test:coverage:dashboard     # Coverage dashboard
npm run test:coverage:trends       # Coverage trend analysis

# Coverage targets
npm run test:coverage:targets       # Check against coverage targets
npm run test:coverage:gaps         # Identify coverage gaps
```

## Output format

```
Test Coverage Analysis Report
──────────────────────────────
Project: Customer Portal v1.3
Analysis Period: Last 30 days
Test Types Included: 8 of 12

Overall Coverage Summary:
  - Code Coverage: 78% (target: 80%)
  - Requirement Coverage: 92% (target: 95%)
  - Risk Coverage: 85% (target: 90%)
  - Scenario Coverage: 88% (target: 85% ✓)
  - Quality Attribute Coverage: 72% (target: 75%)

Code Coverage Detail:
  - Statements: 82% (45,210/55,134)
  - Branches: 71% (12,345/17,390)
  - Functions: 85% (3,456/4,067)
  - Lines: 80% (38,765/48,456)

By Test Type Contribution:
  Unit Tests:
    - Code Coverage: 65% primary contributor
    - Fastest feedback, highest volume
    
  Integration Tests:
    - Code Coverage: +12% incremental
    - API and database coverage
    
  E2E Tests:
    - Code Coverage: +1% incremental  
    - User journey coverage
    
  Security Tests:
    - Requirement Coverage: +15% security requirements
    - No code coverage contribution

Requirement Coverage:
  Functional Requirements: 145/150 (97%)
    - Missing: FR-23 (reporting export), FR-45 (bulk update)
    
  Non-Functional Requirements: 28/35 (80%)
    - Missing: NFR-12 (concurrent users), NFR-18 (data retention)

Risk Coverage:
  High Risks: 8/10 covered (80%)
    - Uncovered: R-05 (payment failure), R-09 (data corruption)
    
  Medium Risks: 22/25 covered (88%)
  Low Risks: 45/50 covered (90%)

Scenario Coverage:
  User Journeys: 15/18 covered (83%)
    - Uncovered: Guest checkout, Account deletion
    
  Business Processes: 8/10 covered (80%)
  Admin Flows: 6/8 covered (75%)

Coverage by Component:
  - Authentication: 95% (excellent)
  - User Management: 88% (good)
  - Billing: 65% (needs improvement)
  - Reporting: 45% (poor)
  - API Gateway: 92% (good)

Coverage Gaps Analysis:
  Critical Gaps:
    1. Billing module has low test automation
    2. Reporting features largely untested
    3. Payment failure scenarios not covered
  
  Moderate Gaps:
    1. Admin flows need more test coverage
    2. Edge cases in user management
  
  Minor Gaps:
    1. Some utility functions untested
    2. Legacy code with no recent test updates

Test Type Effectiveness:
  - Most Effective: Unit tests (high coverage, fast)
  - Best for Risk Coverage: Integration tests
  - Best for User Confidence: E2E tests
  - Most Impactful for Quality: Security & performance tests

Recommendations:
  1. Increase unit test coverage in billing module to 80%
  2. Add integration tests for reporting functionality
  3. Implement security tests for payment processing
  4. Create E2E tests for guest checkout scenario
  5. Review and update test targets for next quarter

Trend Analysis:
  - Code coverage increased from 72% to 78% this quarter
  - Requirement coverage stable at 92%
  - Risk coverage improved from 80% to 85%
  - Positive trend overall, but billing module declining
```

## Notes

- Coverage metrics should inform, not drive, testing decisions
- Different coverage types matter for different contexts
- High coverage doesn't guarantee high quality, but low coverage often indicates risk
- Balance coverage metrics with other quality indicators
- Use coverage data to guide test improvement, not as a punitive measure
- Consider coverage context (legacy code vs new development)
- Automate coverage collection where possible
- Review coverage regularly, not just before releases
- Share coverage insights with development teams
- Use coverage as one input among many for quality assessment
