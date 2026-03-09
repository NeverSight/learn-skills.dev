---
name: test-orchestrator
description: Orchestrate and coordinate different test types in proper order
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Test Orchestrator

Orchestrate and coordinate different test types in proper execution order based on dependencies, speed, and reliability.

## When to use me

Use this skill when:
- Setting up CI/CD pipelines with multiple test types
- Coordinating test execution across teams or systems
- Optimizing test execution order for speed and reliability
- Managing test dependencies and prerequisites
- Creating integrated test workflows
- Balancing test coverage with execution time

## What I do

- **Test execution orchestration**:
  - Determine optimal test execution order
  - Manage dependencies between test types
  - Coordinate parallel and sequential execution
  - Handle test environment setup and teardown

- **Dependency management**:
  - Smoke tests must pass before integration tests
  - Unit tests should run before functional tests
  - Performance tests require stable environment
  - Security scans need deployed application
  - Chaos experiments require monitoring in place

- **Resource optimization**:
  - Run fast tests first for quick feedback
  - Parallelize independent test suites
  - Allocate resources based on test requirements
  - Queue expensive tests for appropriate environments

- **Integration with development workflow**:
  - Pre-commit test orchestration
  - Pull request validation workflow
  - Release candidate testing pipeline
  - Production deployment validation

## Test Execution Order Principles

1. **Fast feedback first**: Unit → Integration → E2E
2. **Prerequisite validation**: Smoke → Functional → Performance  
3. **Environment dependency**: Local → CI → Staging → Production
4. **Risk progression**: Low-risk → High-risk tests
5. **Resource allocation**: Lightweight → Heavyweight tests

## Examples

```bash
# Full test orchestration pipeline
npm run test:orchestrate:full      # Complete test orchestration

# Development workflow orchestration
npm run test:orchestrate:dev       # Developer local testing
npm run test:orchestrate:commit    # Pre-commit validation
npm run test:orchestrate:pr        # Pull request validation

# Release orchestration
npm run test:orchestrate:release   # Release candidate testing
npm run test:orchestrate:deploy    # Deployment validation

# Environment-specific orchestration
npm run test:orchestrate:ci        # CI pipeline orchestration
npm run test:orchestrate:staging   # Staging environment testing
npm run test:orchestrate:production # Production testing

# Test type coordination
npm run test:orchestrate -- --include unit,integration,e2e
npm run test:orchestrate -- --exclude performance,chaos
npm run test:orchestrate -- --parallel integration,e2e
```

## Output format

```
Test Orchestration Results:
──────────────────────────────
Orchestration Plan: Release Candidate Validation
Environment: Staging
Total Test Suites: 8
Estimated Duration: 25 minutes

Execution Plan:
1. ✅ Environment Setup (2 minutes)
   - Deploy release candidate
   - Configure test environment
   - Load test data

2. ✅ Smoke Tests (1 minute) [PREREQUISITE]
   - Application health checks
   - Database connectivity
   - External service availability

3. ✅ Unit Tests (3 minutes) [PARALLEL GROUP A]
   - 1,247 tests across 42 modules
   - Fast feedback, high confidence

4. ✅ Integration Tests (5 minutes) [PARALLEL GROUP A]
   - 324 API integration tests
   - Database interaction tests
   - External service integration

5. ✅ E2E Tests (8 minutes) [SEQUENTIAL - depends on 3,4]
   - 45 critical user workflows
   - Cross-browser validation (Chrome, Firefox)
   - Mobile responsive testing

6. ✅ Performance Tests (4 minutes) [SEQUENTIAL - depends on 5]
   - Load testing: 1000 concurrent users
   - Response time validation
   - Resource utilization monitoring

7. ✅ Security Tests (2 minutes) [PARALLEL GROUP B]
   - Vulnerability scanning
   - Authentication testing
   - Authorization validation

8. ✅ Final Validation (1 minute)
   - Test result aggregation
   - Quality gate evaluation
   - Deployment readiness assessment

Dependency Graph:
  smoke → unit ───┐
  smoke → integration ─┐
        unit → e2e ────┤
  integration → e2e ───┼→ performance
                 e2e → security ─┐
                                 └→ final

Resource Allocation:
  - Parallel Group A (unit, integration): 4 CPU cores
  - Parallel Group B (security): 2 CPU cores  
  - Sequential (e2e, performance): 8 CPU cores
  - Memory: 16GB allocated

Quality Gates:
  - All smoke tests must pass: ✅
  - Unit test coverage > 80%: ✅ (92%)
  - Integration tests 100% pass: ✅
  - E2E critical paths 100% pass: ✅
  - Performance SLA met: ✅
  - No critical security issues: ✅

Orchestration Outcome: ✅ All quality gates passed
Recommendation: Proceed with production deployment
```

## Notes

- Test orchestration balances speed, reliability, and coverage
- Design orchestration based on test pyramid principles
- Implement circuit breakers to stop expensive tests if prerequisites fail
- Consider test flakiness in orchestration decisions
- Monitor orchestration metrics for optimization opportunities
- Document orchestration workflows for team understanding
- Version control orchestration configurations
- Allow manual override for exceptional cases
- Integrate with monitoring and alerting systems
- Continuously refine orchestration based on feedback
