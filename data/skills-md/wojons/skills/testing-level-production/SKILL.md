---
name: testing-level-production
description: Testing strategy for production deployment
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Production Testing Strategy

Comprehensive testing approach for production applications with real users, revenue, and reputation at stake.

## When to use me

Use this skill when:
- Releasing to general public or paying customers
- Handling sensitive data or financial transactions
- Scaling to thousands or millions of users
- Meeting regulatory or compliance requirements
- Maintaining brand reputation and user trust
- Operating mission-critical business applications

## What I do

**Core Philosophy**: "Production-grade" quality with comprehensive risk mitigation. Assume failures will happen and test accordingly.

**Comprehensive Testing Suite**:

1. **Automated Unit Testing**
   - All business logic and critical code paths
   - High code coverage (80-90%+)
   - Fast execution for developer feedback
   - Integrated into CI/CD pipeline

2. **Integration Testing**
   - All external service integrations
   - Database transactions and data consistency
   - API contract testing
   - Error handling and recovery scenarios

3. **End-to-End Automation**
   - Critical user workflows automated
   - Cross-browser and cross-platform testing
   - Visual regression testing
   - Performance benchmark testing

4. **Performance & Load Testing**
   - Load testing at 2-3x expected traffic
   - Stress testing to find breaking points
   - Endurance testing for memory leaks
   - Performance regression detection

5. **Security Testing**
   - Regular vulnerability scanning
   - Penetration testing (annual or per major release)
   - Authentication and authorization testing
   - Compliance validation (GDPR, HIPAA, PCI-DSS as applicable)

6. **Accessibility Testing**
   - WCAG compliance (AA level for public sites)
   - Screen reader and keyboard navigation
   - Regular audits with automated and manual testing

7. **Compatibility Testing**
   - Browser and device matrix testing
   - Operating system compatibility
   - Network condition simulation

8. **Usability Testing**
   - User experience validation
   - A/B testing for feature optimization
   - User feedback integration

**Advanced Testing Practices**:

- Chaos engineering (failure injection)
- Canary deployments and feature flag testing
- Blue-green deployment testing
- Disaster recovery and failover testing
- Monitoring and observability validation

## Examples

```bash
# Production Testing Commands
npm run test:ci                 # Full CI test suite
npm run test:coverage           # Coverage reporting
npm run test:e2e                # Automated E2E tests

# Performance testing
npm run test:performance:load   # Load testing
npm run test:performance:stress # Stress testing

# Security scanning
npm run test:security:scan      # Vulnerability scanning
npm run test:security:audit     # Security audit

# Accessibility
npm run test:accessibility      # WCAG compliance

# Compatibility
npm run test:compatibility      # Cross-browser testing

# Deployment validation
npm run test:smoke:production   # Production smoke tests
npm run test:canary             # Canary deployment tests
```

## Output format

```
Production Testing Strategy:
──────────────────────────────
Quality Gates & Requirements:

✅ Unit Testing:
  - Coverage: 92% (target > 85%)
  - Tests: 2,847 passing
  - Execution time: 42 seconds

✅ Integration Testing:
  - Test Scenarios: 324
  - External Services: 8 integrated
  - Data Consistency: Verified

✅ E2E Automation:
  - Critical Paths: 18 automated workflows
  - Cross-browser: Chrome, Firefox, Safari, Edge
  - Mobile: iOS & Android responsive

✅ Performance:
  - Load Capacity: 10,000 concurrent users
  - Response Time: < 500ms (95th percentile)
  - Uptime Target: 99.95% SLA

✅ Security:
  - Vulnerabilities: 0 critical, 2 medium
  - Penetration Test: Last completed 30 days ago
  - Compliance: GDPR, PCI-DSS Level 4

✅ Accessibility:
  - WCAG 2.1 AA: 94% compliant
  - Screen Readers: NVDA, JAWS, VoiceOver tested
  - Keyboard Navigation: Fully accessible

Monitoring & Observability:
  - Application Performance Monitoring: Configured
  - Error Tracking: Real-time alerts
  - User Analytics: Feature usage tracking

Risk Mitigation:
  - Canary Deployments: 5% traffic initially
  - Feature Flags: Gradual rollout capability
  - Rollback Procedure: Tested quarterly
  - Disaster Recovery: RTO 4 hours, RPO 15 minutes

Recommendation:
  - All quality gates met for production release
  - Monitor performance metrics during peak hours
  - Schedule next penetration test in 90 days
```

## Notes

- Production testing is continuous, not one-time
- Automate everything that can be automated
- Monitor production metrics as ultimate test
- Have rollback plans and practice them
- Test failure scenarios, not just success paths
- Consider different user segments and patterns
- Balance comprehensive testing with release velocity
- Learn from production incidents to improve testing
- Maintain test environments that match production
- Document and review testing strategy regularly
