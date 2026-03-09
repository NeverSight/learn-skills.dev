---
name: testing-performance
description: Test application performance and load handling
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Performance Testing

Test application speed, responsiveness, stability, and scalability under various load conditions.

## When to use me

Use this skill when:
- Preparing for traffic spikes or seasonal loads
- Testing application scalability
- Identifying performance bottlenecks
- Validating SLAs (Service Level Agreements)
- Comparing performance before/after changes
- Capacity planning and infrastructure sizing
- Ensuring user experience under load

## What I do

- Load testing: Simulate expected user traffic
- Stress testing: Find breaking points and limits
- Spike testing: Test sudden traffic surges
- Endurance testing: Check for memory leaks over time
- Scalability testing: Verify horizontal/vertical scaling
- Configuration testing: Optimize performance settings
- Benchmarking: Compare against baseline metrics

## Examples

```bash
# Load testing tools
npx autocannon -c 100 -d 60 https://app.example.com
wrk -t12 -c400 -d30s https://app.example.com
k6 run script.js                     # Grafana k6
jmeter -n -t testplan.jmx -l results.jtl

# Performance monitoring
npm run test:perf                   # Custom performance suite
lighthouse https://app.example.com --output json
webpagetest test https://app.example.com

# Stress testing
artillery run stress.yml
npx loadtest -n 10000 -c 100 https://api.example.com

# Memory and CPU profiling
node --inspect script.js
python -m cProfile script.py
go test -bench=. -benchmem
```

## Output format

```
Performance Test Results:
──────────────────────────────
Load Test (100 concurrent users, 5 minutes):
  ✅ Average Response Time: 245ms (< 500ms target)
  ✅ 95th Percentile: 412ms
  ✅ Throughput: 1,234 req/sec
  ✅ Error Rate: 0.1% (< 1% target)
  ⚠️ CPU Usage: 85% (approaching limit)

Stress Test (Breaking Point):
  ❌ System fails at 850 concurrent users
  ⚠️ Database connection pool exhausted at 800 users
  ✅ Graceful degradation observed

Memory Usage (24-hour endurance):
  ⚠️ Memory leak detected: +2MB/hour
  ❌ OutOfMemory after 18 hours

Summary: Meets most performance targets, needs memory leak fix
```

## Notes

- Establish performance baselines before testing
- Test in production-like environments
- Monitor system resources during tests
- Consider network latency and geography
- Test with realistic data volumes
- Automate performance regression testing
- Document performance requirements and SLAs
- Use APM (Application Performance Monitoring) tools
