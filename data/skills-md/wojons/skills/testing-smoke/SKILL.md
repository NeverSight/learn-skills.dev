---
name: testing-smoke
description: Run smoke tests to verify basic application functionality
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Smoke Testing

Run quick verification tests to ensure basic functionality works before committing to deeper testing (integration, e2e, regression).

## When to use me

Use this skill when:
- After deployments or environment changes
- Before running extensive test suites
- Validating build integrity
- Checking critical paths work
- As a gate before more expensive testing

## What I do

- **Quick validation** of critical functionality:
  - Application starts and responds
  - Database connections work
  - Authentication system functions
  - Core business logic operates

- **Coordinate with other test types**:
  - Run before integration and e2e tests
  - Serve as gate for regression test suites
  - Validate environment for performance tests
  - Check prerequisites for security scans

- **Implementation approaches**:
  - Minimal test set (5-10 key scenarios)
  - Fast execution (under 2 minutes)
  - High reliability (minimal flakiness)
  - Clear pass/fail criteria

## Examples

```bash
# Run smoke tests
npm run test:smoke              # Full smoke test suite
npm run test:smoke:quick        # Absolute minimum validation

# Deployment validation
npm run test:smoke:production    # Production smoke tests
npm run test:smoke:staging      # Staging environment checks

# Coordinate with other tests
npm run test:smoke && npm run test:integration
npm run test:smoke && npm run test:e2e

# Environment-specific smoke tests
npm run test:smoke:dev          # Development environment
npm run test:smoke:ci           # CI environment validation
```

## Output format

```
Smoke Test Results:
──────────────────────────────
Execution Context: Post-deployment validation
Test Duration: 1m 23s (target < 3 minutes)

Critical Paths Verified:
  ✅ Application Server: Responds on port 3000
  ✅ Database Connection: Can query users table
  ✅ Authentication Service: Login endpoint works
  ✅ Core API: GET /api/health returns 200 OK
  ✅ Cache Layer: Redis connection established

Environment Checks:
  ✅ Environment variables loaded
  ✅ Configuration files valid
  ✅ External services reachable
  ✅ File permissions correct

Next Steps Recommended:
  - Smoke tests passed ✅
  - Proceed with integration testing
  - If failed, investigate before deeper testing

Dependency Status:
  - Unit tests not required for smoke (already fast)
  - Integration tests can proceed if smoke passes
  - E2E tests depend on smoke + integration passing
  - Performance tests require stable environment
```

## Notes

- Smoke tests should be extremely reliable (no flakiness)
- Keep execution time minimal for quick feedback
- Test only critical functionality, not edge cases
- Use idempotent tests that don't leave side effects
- Consider canary deployments with smoke testing
- Implement automatic retry for transient failures
- Document what constitutes "smoke test pass" clearly
- Smoke tests often run in production after deployment
