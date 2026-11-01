---
name: source-reliability-and-extraction-resilience
description: Guides agents through source reliability and extraction resilience. Use when upstream systems are flaky, slow, rate-limited, late, or operationally unreliable and ingestion behavior must remain safe and observable.
---

# Source Reliability And Extraction Resilience

## Overview

Use this skill when the real risk is upstream instability rather than downstream modeling. It helps agents design safe ingestion behavior around outages, late data, flaky responses, inconsistent source states, and operational dependencies.

## When to Use

- unstable upstream systems
- intermittent extraction failures
- delayed source availability
- rate-limited or timeout-prone sources
- ingestion designs that must survive source incidents

Do not assume source availability is constant just because the contract exists.

## Workflow

1. Characterize the upstream failure modes.
   Include:
   - outages
   - late availability
   - inconsistent snapshots
   - timeout behavior
   - partial responses

2. Define safe extraction behavior.
   Decide:
   - retry policy
   - timeout handling
   - quarantine behavior
   - when to fail closed versus publish partial data

3. Add observability around the source, not only the pipeline.

4. Bound replay and catchup behavior for upstream recovery scenarios.

5. Document human-operable recovery steps.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The source team says it is reliable." | Reliability claims still need runtime evidence and safe fallback behavior. |
| "We can just retry more." | More retries can worsen load, mask incidents, or still produce partial bad state. |
| "Partial data is better than stale data." | That depends on the business contract and must be explicit. |

## Red Flags

- no documented source failure modes
- partial-source behavior is undefined
- the pipeline can publish partial data without warning
- source recovery depends on tribal knowledge

## Verification

- [ ] Upstream failure modes are characterized
- [ ] Extraction and publish behavior under failure is explicit
- [ ] Source health is observable separately from downstream success
- [ ] Recovery and catchup rules are documented
