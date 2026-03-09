---
name: testing-integration
description: Run integration tests for component interactions
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Integration Testing

Test interactions between multiple components, modules, or services.

## When to use me

Use this skill when:
- Components have been unit tested and need to work together
- Testing API contracts between services
- Verifying database interactions work correctly
- Checking third-party service integrations
- Ensuring microservices communicate properly
- Validating data flows through the system

## What I do

- Identify integration points between components
- Set up test environments with real or test databases
- Configure service connections and API endpoints
- Test data flow between integrated components
- Verify error handling across component boundaries
- Check contract compliance between services
- Validate end-to-end workflows without UI

## Examples

```bash
# Run integration tests
npm run test:integration     # Node.js integration tests
pytest tests/integration/    # Python integration tests
go test -tags=integration    # Go integration tests

# Test specific integrations
npm run test:integration -- --grep "database"
pytest tests/integration/test_api_client.py

# Run with test containers for external services
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Output format

```
Integration Test Results:
──────────────────────────────
✅ API Service ↔ Database
  ✓ User data persists correctly
  ✓ Transaction rollback on failure

❌ Payment Service ↔ Banking API
  ✗ Authentication token refresh fails
  ✗ Currency conversion rate mismatch

⚠️ Email Service ↔ Queue
  ⚠️ Message retention period too short

Summary: 8 passed, 2 failed, 1 warning
```

## Notes

- Integration tests are slower than unit tests
- Use test databases or in-memory databases
- Mock only external third-party services
- Test happy paths and error scenarios
- Clean up test data between tests
- Consider using test containers for external dependencies
- Focus on contract testing for microservices
