---
name: performance-load-testing
description: "Performance load testing workflow for realistic workload simulation, bottleneck detection, and saturation behavior analysis. Use when systems need throughput/latency validation before rollout; do not use for non-performance functional acceptance decisions."
---

# Performance Load Testing

## Overview
Use this skill to validate performance under realistic and stress conditions before production risk increases.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Workload realism rules:
  - `references/workload-realism-rules.md`

## Templates And Assets
- Load profile template:
  - `assets/load-profile-template.md`
- Load test report template:
  - `assets/load-test-report-template.md`

## Inputs To Gather
- Critical user flows and traffic distribution.
- Target latency/throughput/error thresholds.
- Environment and dependency readiness.
- Saturation and recovery expectations.

## Deliverables
- Load profile and execution plan.
- Bottleneck evidence and saturation points.
- Release readiness recommendation and fixes.

## Workflow
1. Define workload in `assets/load-profile-template.md`.
2. Validate realism using `references/workload-realism-rules.md`.
3. Execute baseline/peak/stress phases.
4. Document outcomes in `assets/load-test-report-template.md`.
5. Publish remediation and retest plan.

## Quality Standard
- Load profiles represent production-critical behavior.
- Bottlenecks are evidenced and prioritized.
- Saturation behavior and failure modes are understood.

## Failure Conditions
- Stop when test profile misses critical production traffic patterns.
- Stop when results cannot be reproduced or interpreted confidently.
- Escalate when unresolved bottlenecks threaten SLOs.
