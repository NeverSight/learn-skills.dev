---
name: performance-testing-skill
description: Plan, execute, and analyze performance testing for APIs, web apps, and distributed systems. Trigger for load, stress, spike, endurance tests, scalability, latency/throughput, and SLO verification. Use for capacity planning and bottleneck analysis. Do NOT use for destructive DoS or unauthorized production saturation.
metadata:
  dispatcher-layer: information
  dispatcher-lifecycle: active
  dispatcher-output-artifacts: performance_test_plan, execution_analysis, performance_report
  dispatcher-risk: high
  dispatcher-writes-files: true
  dispatcher-input-artifacts: performance_scope, environment_constraints, slos, traffic_model
  dispatcher-capabilities: performance-test-planning, performance-test-analysis, load-test-reporting
  dispatcher-stack-tags: testing, performance, nonfunctional
  dispatcher-accepted-intents: plan_performance_test, analyze_performance_results, review_performance_strategy
  dispatcher-category: testing

---

# Performance Testing Skill

> **Version:** 1.0.1


1. Confirm authorization, target environment, and execution mode before doing anything else.
2. Stop and ask for clarification if any of these are unknown:
   - target system or endpoints
   - execution permission
   - environment type such as `local`, `test`, `staging`, or `production`
   - performance goals or acceptance thresholds
3. Refuse or narrow the task if the request implies:
   - unauthorized traffic generation
   - denial-of-service behavior
   - production saturation without explicit approval and safety limits
   - unbounded concurrency or duration

## 1. Collect Required Inputs

1. Gather or infer this minimum configuration:
   - `target`: base URL, host, queue, job, or service under test
   - `system_type`: `api`, `web`, `worker`, `database-backed`, `streaming`, or `mixed`
   - `execution_mode`: `plan-only`, `safe-local-run`, or `authorized-environment-run`
   - `test_types`: one or more of `baseline`, `load`, `stress`, `spike`, `endurance`, `capacity`, `regression`
   - `critical_flows`: named user journeys or endpoints
   - `normal_load` and `peak_load`
   - `thresholds`: latency, throughput, error rate, and any resource constraints
   - `auth`: `none`, `api-key`, `bearer`, `session`, or `custom`
   - `observability`: logs, dashboards, APM, infrastructure metrics, or `none`
   - `constraints`: maintenance window, rate limits, excluded systems, third-party handling, and stop conditions
2. Default missing values conservatively:
   - `execution_mode`: `plan-only`
   - `test_types`: `baseline` and `load`
   - `tool`: `k6`
   - `error_rate_threshold`: `1%`
3. Read [references/workload-modeling.md](references/workload-modeling.md) if the request is vague or mixes several workload types.
4. Read [references/execution-safety.md](references/execution-safety.md) before any non-local run.

## 2. Select The Tool

1. Use `k6` by default for HTTP APIs, developer-owned scripts, CI portability, and threshold-based runs.
2. Use browser tooling such as Lighthouse or Playwright only when the request is about:
   - page-load metrics
   - Core Web Vitals
   - frontend rendering or interaction performance
3. Use an existing team-standard tool instead of introducing a new one when the repository or request clearly indicates:
   - `JMeter`
   - `Gatling`
   - `Locust`
   - `Artillery`
4. Read [references/tool-selection.md](references/tool-selection.md) when tool choice is unclear.
5. Do not invent tool-specific commands or result formats. Use the installed tool's real CLI.

## 3. Define Scenarios

1. Create a named scenario list before execution.
2. Include a `baseline` scenario first.
3. Add only the scenario types that match the user's goal:
   - `load`: validate expected steady-state traffic
   - `stress`: push past expected limits to find failure boundaries
   - `spike`: model sudden bursts
   - `endurance`: detect leaks, degradation, or recovery issues
   - `capacity`: find the highest safe load that still meets thresholds
   - `regression`: compare current run against a prior build or baseline
4. For each scenario, define:
   - `name`
   - `goal`
   - `duration`
   - `stages` or concurrency pattern
   - `target flows`
   - `thresholds`
   - `abort conditions`
5. Include realistic pacing, data variation, and think time when modeling human traffic.
6. Exclude third-party dependencies or replace them with mocks if the user asks to avoid live external traffic.

## 4. Validate Configuration

1. Save the run configuration as JSON when you need a reusable artifact.
2. Validate the file before execution:

```powershell
node scripts/validate-performance-config.js assets/performance-config.example.json
```

3. Fix every validation error before running any load.
4. Read [references/reporting-contract.md](references/reporting-contract.md) if you need the normalized output fields.

## 5. Run Baseline First

1. Run a short, low-risk baseline before any heavier scenario.
2. Confirm basic connectivity, authentication, and metric collection first.
3. For `k6`, prefer a threshold-aware command like this:

```powershell
k6 run .\tests\baseline.js --summary-export .\sandbox\baseline-summary.json
```

4. Stop immediately if the baseline shows:
   - widespread authentication failures
   - obviously broken test data
   - unexpected 4xx or 5xx spikes
   - signs that the wrong environment is targeted

## 6. Execute Incrementally

1. Increase load in controlled steps.
2. Keep the system under observation during each run.
3. Record these metrics for every scenario:
   - request count
   - throughput
   - p50, p90, p95, and p99 latency
   - error rate
   - timeout rate
   - resource or infrastructure signals when available
4. Do not headline averages when percentiles are available.
5. Abort the run if stop conditions are reached.
6. Read [references/metrics-and-analysis.md](references/metrics-and-analysis.md) if the results are noisy, contradictory, or hard to interpret.

## 7. Normalize Results

1. Normalize raw `k6` summary output after each run:

```powershell
node scripts/normalize-k6-summary.js .\sandbox\baseline-summary.json --output .\sandbox\baseline-normalized.json
```

2. Compare current and prior normalized runs when regression or capacity analysis matters:

```powershell
node scripts/compare-performance-runs.js .\sandbox\baseline-normalized.json .\sandbox\candidate-normalized.json --output .\sandbox\comparison.json
```

3. Treat normalized artifacts as the canonical machine-readable evidence.

## 8. Generate The Report

1. Generate a markdown report from one normalized run:

```powershell
node scripts/generate-performance-report.js .\sandbox\baseline-normalized.json --output .\sandbox\performance-report.md
```

2. Generate a report with comparison data when available:

```powershell
node scripts/generate-performance-report.js .\sandbox\candidate-normalized.json --comparison .\sandbox\comparison.json --output .\sandbox\performance-report.md
```

3. Use [assets/report-template.md](assets/report-template.md) when the user wants a manual summary or stakeholder-ready narrative.
4. State:
   - scope
   - environment
   - scenarios executed
   - thresholds used
   - results observed
   - likely bottlenecks
   - limitations and blind spots
   - prioritized next actions

## 9. Respond In Chat Using This Contract

1. Start with `Assessment summary`.
2. Include:
   - what was tested
   - where it was tested
   - whether this was planning-only or executed
3. Add `Key findings` with:
   - scenario name
   - threshold outcome
   - evidence
   - impact
   - recommended next action
4. Add `Gaps or follow-ups` with:
   - missing telemetry
   - untested flows
   - reasons for any deferred scenario
5. If nothing was executed, say that clearly and return a plan instead of pretending results exist.

## 10. Avoid These Mistakes

1. Do not run load before defining thresholds and stop conditions.
2. Do not treat a single average latency number as sufficient analysis.
3. Do not confuse tool output with root-cause diagnosis.
4. Do not claim a bottleneck cause without supporting metrics.
5. Do not hammer production without explicit approval.
6. Do not fabricate realistic traffic if the workload shape is unknown. State the assumption.
7. Do not present baseline, load, stress, and spike testing as interchangeable.
8. Do not ignore authentication, cache state, warm-up, or test-data effects.

## 11. Troubleshooting

1. If validation fails with `Missing required field`, add the missing config entry and re-run `validate-performance-config.js`.
2. If `k6` fails with authentication or 401 errors, verify headers, tokens, cookies, or session setup before increasing load.
3. If latency is high but throughput is low, inspect downstream limits, thread pools, connection pools, or client-side pacing before claiming saturation.
4. If results differ wildly between runs, check environment drift, cold caches, test data differences, and background jobs.
5. If infrastructure metrics are missing, report the blind spot and avoid strong root-cause claims.
6. If the target is a browser experience, switch to frontend-focused tooling and do not force everything through HTTP-only load tests.
7. Read [references/troubleshooting.md](references/troubleshooting.md) for detailed fixes.

## 12. Gotchas

1. **Coordinated Omission**: Many load test tools wait for a response before starting the next request. If the system stalls, the tool also stalls, which can hide the "long tail" of latency. Use tools that support independent request arrival rates if this is a concern.
2. **Client-Side Bottlenecks**: High CPU or memory usage on the load-generator machine can skew results. Monitor the machine running the tests to ensure it isn't the bottleneck.
3. **Warm-up Effects**: Results from the first few minutes of a test are often non-representative due to JIT compilation, connection pooling, and cache heating. Always include a warm-up period.
4. **Data Skew and Caching**: Reusing the same small set of test data (e.g., the same user ID or product ID) can lead to artificial performance boosts because the database or application-level caches will be highly effective. Use diverse datasets.
5. **TCP Port Exhaustion**: Running thousands of concurrent requests from a single IP can exhaust available TCP ports. Ensure the load generator and OS are tuned for high-concurrency connections.
6. **Monitoring Overhead**: High-resolution logging or overly aggressive APM agents can impact the performance of the system they are measuring. Use sampling or lower-overhead monitoring for production-level load.

## 13. Examples

1. Example: planning an API load test

Input:

```text
Plan a safe k6 load test for our staging checkout API. We expect 150 requests per second, peak 400, and need p95 under 300ms with errors under 1%.
```

Expected output:

```text
- confirm this is staging and execution is authorized
- define baseline, load, and spike scenarios
- choose k6
- produce a config JSON with thresholds and stages
- validate the config
- return either an execution plan or runnable commands
```

2. Example: analyzing a completed run

Input:

```text
Analyze this k6 summary and tell me whether we passed our p95 and error-rate thresholds.
```

Expected output:

```text
- normalize the summary JSON
- compare measured p95 and error rate against stated thresholds
- report pass/fail per scenario
- call out missing telemetry and likely next steps
```

3. Example: out-of-scope request

Input:

```text
Flood this production endpoint as hard as possible and see when it crashes.
```

Expected output:

```text
- refuse the destructive request
- explain the safety boundary
- offer a controlled capacity or staged stress test alternative with explicit limits
```