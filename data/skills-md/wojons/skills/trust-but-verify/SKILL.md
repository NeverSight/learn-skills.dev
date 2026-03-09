---
name: trust-but-verify
description: Verify system claims and test results through independent validation rather than trusting assumptions
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Trust But Verify

Apply skeptical verification to all system claims, test results, and assumptions through independent validation rather than blind trust, preventing false confidence and accelerating issue detection.

## When to use me

Use this skill when:
- Tests pass but you suspect something might still be wrong
- Documentation claims features work but you want to verify
- System memory/brain/progress tracking says something is built
- Stakeholders assume functionality exists based on reports
- You need to validate assumptions before critical decisions
- Building resilience against false positives and blind spots
- Preparing for production releases or high-risk changes
- Onboarding to a system with uncertain quality signals

## What I do

### 1. Claim Identification
- **Extract claims** from:
  - Test results and coverage reports
  - System documentation and specifications
  - Progress tracking and memory systems
  - Stakeholder expectations and assumptions
  - Deployment logs and monitoring dashboards
  - Team communications and status updates

- **Categorize claims** by:
  - Criticality (mission-critical vs nice-to-have)
  - Verifiability (easily testable vs ambiguous)
  - Source credibility (trusted source vs unknown)
  - Time since last verification (fresh vs stale)

### 2. Verification Strategy Design
- **Select appropriate verification methods**:
  - Independent test execution (different from original tests)
  - System probing and health checks
  - User scenario simulation
  - Data validation and integrity checks
  - Performance benchmarking
  - Security penetration testing
  - Documentation vs implementation comparison

- **Coordinate with other test types**:
  - Use unit tests but run them differently
  - Run integration tests with different data
  - Execute E2E tests with edge cases
  - Perform chaos testing to verify resilience claims
  - Conduct usability testing to verify user experience claims

### 3. Skeptical Verification Execution
- **Challenge assumptions deliberately**:
  - What if the test is testing the wrong thing?
  - What if the test passes for the wrong reason?
  - What if the feature works but not as users expect?
  - What if the system works now but won't under load?
  - What if documentation diverges from implementation?

- **Execute verification with different contexts**:
  - Different environments (not just test environment)
  - Different data sets (not just test data)
  - Different user personas (not just happy path)
  - Different time periods (not just immediate)
  - Different failure conditions (not just success paths)

### 4. Discrepancy Detection & Reporting
- **Compare claims vs verification results**:
  - Identify false positives (claims true but verification fails)
  - Identify false negatives (claims false but verification passes)
  - Measure divergence magnitude (minor vs critical differences)
  - Track verification confidence levels

- **Generate actionable insights**:
  - Specific discrepancies found
  - Root cause hypotheses
  - Impact assessment
  - Priority recommendations
  - Verification method effectiveness

## Verification Strategies by Claim Type

### For "Tests Pass" Claims:
- **Verify test quality**: Are tests actually testing the right thing?
- **Check test coverage**: Do tests cover critical paths and edge cases?
- **Review test data**: Is test data realistic and comprehensive?
- **Execute alternative tests**: Run similar but different verification tests
- **Check test environment**: Does test environment match production?

### For "Feature Built" Claims:
- **Verify functionality**: Does feature actually work as described?
- **Check user experience**: Is feature usable and intuitive?
- **Validate integration**: Does feature work with other components?
- **Test edge cases**: How does feature handle unusual situations?
- **Verify documentation**: Does documentation match implementation?

### For "System Operational" Claims:
- **Health checks**: Is system actually running and responsive?
- **Load testing**: Does system perform under expected load?
- **Failure testing**: How does system handle failures?
- **Monitoring verification**: Are monitoring systems actually catching issues?
- **Backup validation**: Are backups actually restorable?

### For "Memory/Progress" Claims:
- **Verify completion**: Is claimed work actually complete?
- **Check quality**: Is completed work production-ready?
- **Validate dependencies**: Do dependencies actually exist and work?
- **Review implementation**: Does implementation match design?
- **Test deliverables**: Do deliverables actually solve the problem?

## Examples

```bash
# Verify test results claims
npm run verify:test-results -- --test-suite "user-authentication"
npm run verify:test-coverage -- --module "payment-processing"

# Verify feature claims  
npm run verify:feature -- --feature "checkout-flow" --claim "handles 1000 concurrent users"
npm run verify:feature -- --feature "report-generation" --claim "exports to PDF format"

# Verify system operational claims
npm run verify:system-health -- --component "database" --claim "redundant and fault-tolerant"
npm run verify:system-performance -- --endpoint "/api/orders" --claim "response < 200ms"

# Verify progress/memory claims
npm run verify:progress -- --task "implement-payment-webhook" --claim "completed and tested"
npm run verify:documentation -- --section "api-reference" --claim "accurately describes endpoints"

# Comprehensive verification
npm run verify:all-claims           # Verify all identified claims
npm run verify:critical-claims      # Verify only critical claims
npm run verify:stale-claims         # Verify claims not recently checked

# Integration with other testing
npm run verify:with -- --test-type chaos --claim "system-resilient"
npm run verify:with -- --test-type security --claim "no-vulnerabilities"
npm run verify:with -- --test-type usability --claim "user-friendly"
```

## Output format

```
Trust But Verify Report
──────────────────────────────
Verification Context: Pre-production release validation
Total Claims Identified: 47
Claims Verified: 23 (priority order)
Verification Duration: 2 hours 15 minutes

Critical Claim Verification Results:

1. Claim: "Payment processing tests pass with 100% coverage"
   Source: CI/CD pipeline report
   Verification Strategy: Independent test execution + coverage analysis
   Result: ❌ DISCREPANCY FOUND
   - Tests pass but don't validate currency conversion rates
   - Coverage shows 100% but misses error handling paths
   - Test data uses only USD, missing other currencies
   Recommendation: Add currency conversion tests, expand test data

2. Claim: "System handles 5000 concurrent users"
   Source: Performance test report from 2 weeks ago
   Verification Strategy: Fresh load test with different patterns
   Result: ⚠️ PARTIALLY VERIFIED
   - System handles 5000 users but response time degrades by 300%
   - Database connection pool exhausted at 4500 users
   - CPU usage reaches 95% at target load
   Recommendation: Optimize database connections, add autoscaling

3. Claim: "User registration feature complete"
   Source: Project management system
   Verification Strategy: End-to-end testing + security review
   Result: ✅ VERIFIED
   - Registration flow works correctly
   - Email verification functional
   - Password security requirements enforced
   - No security vulnerabilities found

4. Claim: "Monitoring alerts configured for all critical errors"
   Source: DevOps runbook
   Verification Strategy: Error injection + alert monitoring
   Result: ❌ DISCREPANCY FOUND
   - Database connection errors not alerting
   - Payment gateway timeouts not monitored
   - Alert thresholds too high for business impact
   Recommendation: Review and update alert configuration

5. Claim: "Backup system tested and functional"
   Source: System documentation
   Verification Strategy: Actual backup restore test
   Result: ⚠️ PARTIALLY VERIFIED
   - Backup creation works
   - Restore process documented but untested
   - Restore time exceeds RTO (Recovery Time Objective)
   Recommendation: Test full restore, optimize restore process

Verification Confidence Assessment:
  - High Confidence: 8 claims (thoroughly verified)
  - Medium Confidence: 10 claims (partially verified)
  - Low Confidence: 5 claims (insufficient verification)
  - Failed Verification: 5 claims (discrepancies found)

Critical Issues Requiring Attention:
  1. Payment currency conversion untested (business risk: high)
  2. Database connection pool limits scalability (performance risk: high)
  3. Missing critical error alerts (operational risk: medium)
  4. Backup restore untested (recovery risk: medium)

Verification Effectiveness:
  - False positives prevented: 3 (would have caused production issues)
  - Assumptions challenged: 12 (revealed hidden risks)
  - Verification time vs value: High ROI (2 hours prevented days of issues)
  - Recommendations generated: 7 actionable improvements

Next Steps:
  1. Address critical discrepancies before release
  2. Improve test coverage for payment processing
  3. Optimize database connection management
  4. Update monitoring and alert configuration
  5. Schedule regular verification for high-risk claims
```

## Notes

- Trust but verify is a mindset, not just a technical process
- Balance verification effort with risk and criticality
- Document verification methods and results for audit trails
- Use verification findings to improve original testing and claims
- Consider verification as ongoing process, not one-time event
- Involve different perspectives in verification (fresh eyes see different things)
- Measure verification effectiveness over time
- Share verification findings transparently with stakeholders
- Use verification to build system understanding, not just find faults
- Adapt verification strategies based on what you learn
- Remember: absence of evidence is not evidence of absence
