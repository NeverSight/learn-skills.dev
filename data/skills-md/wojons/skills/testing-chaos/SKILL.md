---
name: testing-chaos
description: Run chaos engineering tests to build resilient systems
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Chaos Testing

Run chaos engineering experiments to build resilient systems by intentionally injecting failures and observing system behavior.

## When to use me

Use this skill when:
- Building highly available and resilient systems
- Testing failure recovery and auto-remediation
- Validating disaster recovery plans
- Ensuring graceful degradation under stress
- Testing monitoring and alerting systems
- Building confidence in production resilience
- Preparing for unexpected failure scenarios

## What I do

- **Failure injection experiments**:
  - Network latency and packet loss
  - Service dependency failures
  - Resource exhaustion (CPU, memory, disk)
  - Database connection failures
  - Third-party API outages

- **Resilience validation**:
  - Circuit breaker pattern testing
  - Retry and backoff strategy validation
  - Fallback and default behavior testing
  - Load shedding and rate limiting
  - Failover and redundancy testing

- **Coordination with other testing**:
  - Builds on performance and load testing
  - Complements disaster recovery testing
  - Informs reliability and availability testing
  - Validates monitoring and observability

- **Experiment design**:
  - Hypothesis-driven experimentation
  - Blast radius containment
  - Progressive fault injection
  - Automated experiment orchestration

## Examples

```bash
# Chaos engineering tools
npm run test:chaos:start           # Start chaos experiments
npm run test:chaos:stop            # Stop all chaos experiments
npm run test:chaos:status          # Check experiment status

# Specific failure injections
npm run test:chaos:network         # Network failure injection
npm run test:chaos:service         # Service dependency failures
npm run test:chaos:resource        # Resource exhaustion
npm run test:chaos:database        # Database failures

# Integration with other tests
npm run test:performance -- --chaos # Performance under failure
npm run test:reliability -- --chaos # Reliability with faults

# Experiment scenarios
npm run test:chaos:scenario:api-outage      # API dependency outage
npm run test:chaos:scenario:db-failover     # Database failover
npm run test:chaos:scenario:latency-spike   # Network latency spike
npm run test:chaos:scenario:memory-leak     # Memory pressure

# Safety controls
npm run test:chaos:safety-check    # Pre-experiment safety check
npm run test:chaos:rollback        # Emergency rollback
```

## Output format

```
Chaos Test Results:
──────────────────────────────
Experiment: Database Primary Node Failure
Hypothesis: System will failover to replica within 30 seconds
Blast Radius: Staging environment, canary deployment
Duration: 15 minutes

Experiment Execution:
  1. Baseline metrics collected
  2. Database primary node terminated (simulated)
  3. System behavior observed for 10 minutes
  4. Metrics compared to baseline

Results:
  ✅ Failover Time: 22 seconds (within 30s target)
  ✅ Data Consistency: No data loss detected
  ✅ User Impact: 15% error rate during failover (acceptable)
  ✅ Recovery: Automatic, no manual intervention required
  ✅ Monitoring: Alerts triggered within 45 seconds

System Behavior Under Failure:
  - API response time increased from 150ms to 850ms during failover
  - Error rate spiked to 15% for 45 seconds
  - Read-only operations continued uninterrupted
  - Write operations queued and retried successfully

Integration with Other Testing:
  - Performance testing: Established baseline for comparison
  - Reliability testing: Validated MTTR (Mean Time To Recovery)
  - Monitoring testing: Alert effectiveness verified
  - Disaster recovery: Automated failover confirmed

Safety Controls:
  - Automatic rollback on critical failure thresholds
  - Manual abort available throughout
  - Canary deployment limited impact
  - Post-experiment verification passed

Lessons Learned:
  1. Need to improve connection pooling during failover
  2. Alert thresholds should be adjusted for transient failures
  3. User-facing error messages during failover need improvement
  4. Database health checks could be more frequent

Recommendation:
  - System demonstrates good resilience to database failures
  - Implement suggested improvements from lessons learned
  - Schedule regular chaos experiments (monthly)
  - Expand blast radius gradually as confidence increases
```

## Notes

- Start with small, controlled experiments
- Always have a rollback plan and automatic abort mechanisms
- Test in staging before production
- Document hypotheses and validate outcomes
- Use feature flags to control chaos injection
- Monitor system metrics closely during experiments
- Learn from failures and improve system design
- Chaos testing complements, doesn't replace, other testing
- Consider business impact and schedule experiments appropriately
- Build a culture of resilience, not just technical fixes
