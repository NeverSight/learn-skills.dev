---
name: testing-strategy
description: Comprehensive testing strategy covering unit, integration, E2E, security, accessibility, and performance testing
license: Apache-2.0
---

# Testing Strategy Skill

## Purpose
Defines comprehensive testing approaches ensuring code quality, security, accessibility, and performance through automated and manual testing.

## Testing Pyramid
- 70% Unit Tests (fast, isolated, many)
- 20% Integration Tests (moderate speed, component interaction)
- 10% E2E Tests (slow, full user journeys)

## Unit Testing Standards
- Minimum 80% code coverage
- 100% coverage for critical paths
- Test all public APIs and error handling
- Use AAA pattern (Arrange, Act, Assert)

## Integration Testing
- Database queries and transactions
- API endpoint functionality
- External service integration
- Cache behavior

## E2E Testing (Playwright/Cypress)
- Critical user journeys
- Form submissions
- Cross-browser compatibility
- Responsive design verification

## Security Testing
1. SAST — CodeQL, ESLint security plugins
2. Dependency Scanning — npm audit, Dependabot
3. DAST — OWASP ZAP scans
4. Common vulnerability tests (SQLi, XSS, CSRF)

## Accessibility Testing (WCAG 2.1 AA)
- Keyboard navigation
- Screen reader compatibility
- Color contrast (4.5:1 normal, 3:1 large)
- axe-core automated checks

## Performance Testing
- LCP < 2.5s, FID < 100ms, CLS < 0.1
- Lighthouse performance audits
- Load testing under peak conditions

## CI Pipeline Integration
```yaml
steps:
  - Run linter
  - Run unit tests with coverage
  - Run integration tests
  - Run E2E tests
  - Security scan
  - Lighthouse CI
```

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
