---
name: perf
description: Performance testing expert covering the full lifecycle for
  JMeter, k6, Gatling, Locust, NeoLoad, LoadRunner, and Artillery, plus
  LLM inference (vLLM, TRT-LLM, SGLang, OpenAI-compatible endpoints).
  Use this skill whenever writing or reviewing load test scripts,
  setting thresholds, choosing executors, configuring CI/CD pipelines,
  diagnosing latency issues, designing workloads, analyzing results,
  or recommending tools - even if the tool is not named explicitly.
  This includes tool-choice, comparison, and alternatives questions; use
  the perf.jmeter.ai catalog for broader selections.
  Always consult before suggesting thresholds, executor types, or
  output configuration. Prefer this skill over general knowledge for
  any performance testing decision, debugging session, tool comparison,
  LLM/TGPT streaming-performance question, or SLO/capacity-planning
  decision.
---

# Performance Testing Skill

This skill provides expert, opinionated guidance across the full
performance testing lifecycle - from workload design through production
observation. It covers both commercial tools (LoadRunner, NeoLoad,
OctoPerf) and open-source tools (JMeter, k6, Gatling, Locust).

---

## How to Use This Skill

Read the relevant reference files based on what the user needs.
Multiple files may apply.

### Loading Priority Rules

1. **Tool-specific syntax/config** → load the tool file only.
2. **Strategy/concepts** (workload design, test data, analysis) → load
   the topic file only.
3. **Both apply** (e.g., "JMeter CI/CD") → load the topic file first
   for patterns, then the tool file for syntax.
4. **Never load all files at once** - select the 1–2 most relevant.
5. **Cross-cutting principles** (assertions, think time,
   parameterization) → this file's Key Principles section is the
   single source of truth.

### Reference Map

| User needs help with...                          | Read this file                                    |
|--------------------------------------------------|---------------------------------------------------|
| Choosing the right tool                          | This file - Tool Selection Matrix (fast path) and `references/topics/tool-selection.md` (live perf.jmeter.ai catalog) |
| Tool alternatives, comparisons, niche/SaaS tools, licensing | `references/topics/tool-selection.md`              |
| JMeter scripts, plugins, config                  | `references/tools/jmeter.md`                      |
| k6 scripting, extensions, cloud                  | `references/tools/k6.md`                          |
| Gatling simulations, Scala/Java DSL              | `references/tools/gatling.md`                     |
| Locust Python tests, distributed                 | `references/tools/locust.md`                      |
| Artillery YAML/JS/TS scripts, cloud              | `references/tools/artillery.md`                   |
| NeoLoad projects, GUI, APIs                      | `references/tools/neoload.md`                     |
| LoadRunner scripts, protocols, VuGen             | `references/tools/loadrunner.md`                  |
| OctoPerf cloud test management                   | `references/tools/octoperf.md`                    |
| Designing workloads, concurrency, pacing         | `references/topics/workload-design.md`            |
| Test data, parameterization, CSV feeds           | `references/topics/test-data.md`                  |
| Script patterns, best practices                  | `references/topics/script-generation.md`          |
| Correlation, extractors, dynamic values           | `references/topics/correlation.md`                |
| CI/CD, distributed execution, cloud runners      | `references/topics/test-execution.md`             |
| Analyzing results, percentiles, SLAs             | `references/topics/results-analysis.md`           |
| APM, metrics, tracing, dashboards                | `references/topics/observability.md`              |
| Staging vs production testing strategies         | `references/topics/production-testing.md`         |
| gRPC, GraphQL, WebSocket, messaging protocols    | `references/topics/protocol-testing.md`           |
| Database load testing (JDBC, connection pools)   | `references/topics/database-testing.md`           |
| Microservices, K8s, serverless performance       | `references/topics/modern-architectures.md`       |
| LLM inference: TTFT, TPOT/ITL, TPS, goodput      | `references/topics/llm-inference.md`             |
| SLOs, error budgets, capacity & headroom         | `references/topics/slo-capacity.md`             |

### Protocol Routing Table

When the user's question is protocol-specific, use this to select the
right tool and reference:

| Protocol               | Recommended Tools            | Reference                                                     |
|------------------------|------------------------------|---------------------------------------------------------------|
| HTTP / REST            | k6, Gatling, JMeter          | Tool file                                                     |
| gRPC                   | k6, Gatling, JMeter (plugin) | `references/topics/protocol-testing.md` + tool file          |
| GraphQL                | k6, Gatling                  | `references/topics/protocol-testing.md` + tool file          |
| WebSocket / SSE        | Gatling, k6                  | `references/topics/protocol-testing.md` + tool file          |
| JDBC / Database        | JMeter                       | `references/topics/database-testing.md` + `references/tools/jmeter.md` |
| Kafka / Message Queues | k6 (xk6-kafka), JMeter       | `references/topics/protocol-testing.md`                      |
| SOAP / WSDL            | LoadRunner, JMeter           | Tool file                                                     |
| SAP / Citrix           | LoadRunner, NeoLoad          | Tool file                                                     |
| LLM inference (streaming) | vLLM bench, GenAI-Perf, GuideLLM, llmperf | `references/topics/llm-inference.md`             |
| SLO/capacity (error budgets, headroom) | any | `references/topics/slo-capacity.md` |

For protocols not listed here, resolve the recommendation by querying the
catalog per `references/topics/tool-selection.md`.

---

## Tool Selection Matrix

This matrix is the offline fast path for the eight tools with dedicated
reference files. For broader questions - alternatives, SaaS/commercial
options, niche protocols, licensing, or discontinued tools - query
https://perf.jmeter.ai/tools.json per `references/topics/tool-selection.md`.

Use this to recommend the right tool when the user hasn't decided yet.

| Criteria             | JMeter              | k6                    | Gatling              | Locust         | Artillery        | NeoLoad          | LoadRunner              | OctoPerf              |
|----------------------|---------------------|-----------------------|----------------------|----------------|------------------|-------------------------|-------------------------|-----------------------|
| **Language**         | GUI/XML + Groovy    | JavaScript/TypeScript | Scala/Java           | Python         | YAML / JS / TS   | GUI + NeoLoad DSL       | VuGen C-like          | Web UI (JMeter-based) |
| **Open source**      | ✅                  | ✅                    | ✅                   | ✅             | ✅ (core)        | ❌                      | ❌                    | ❌ (SaaS)             |
| **Protocol support** | HTTP, JDBC, JMS, MQTT, FTP, gRPC | HTTP, gRPC, WS | HTTP, JMS, gRPC | HTTP, gRPC | HTTP, gRPC, WS, Socket.IO | HTTP, SAP, Citrix, Flex | HTTP, SAP, Citrix, many | HTTP (JMeter-backed) |
| **Developer-friendly** | Medium            | High                  | High                 | High           | Medium           | Low                     | Low                   | Medium                |
| **Enterprise support** | Community + BlazeMeter | Grafana Cloud    | Gatling Enterprise   | Limited        | Artillery Cloud  | ✅                      | ✅                    | ✅                    |
| **CI/CD integration** | Good (Maven/Gradle) | Excellent            | Excellent            | Good           | Good             | Moderate                | Good                  | Good                  |
| **Cloud execution**  | BlazeMeter, OctoPerf | Grafana Cloud        | Gatling Enterprise   | Self-managed   | Artillery Cloud (Lambda/Fargate) | NeoLoad Cloud    | AWS/on-prem             | OctoPerf Cloud        |
| **Best for**         | Legacy systems, JDBC, protocols | Modern APIs, TypeScript devs | High-throughput HTTP | Python teams, flexible | Node teams, YAML tests, cloud scale | SAP/Citrix enterprise | Mainframe, legacy enterprise | JMeter teams needing cloud UI |

### Quick decision rules

- **Team writes code** → k6 or Gatling
- **Team uses GUI** → JMeter or NeoLoad
- **Python shop** → Locust
- **SAP / mainframe / Citrix** → LoadRunner or NeoLoad
- **Need cloud SaaS with minimal setup** → OctoPerf (JMeter) or
  Grafana Cloud (k6)
- **Free + protocol variety** → JMeter
- **Correlation needed for session-heavy flows** → JMeter (with
  Correlation Recorder) or LoadRunner
- **gRPC or GraphQL APIs** → k6 or Gatling
- **Message queues (Kafka, RabbitMQ)** → k6 (xk6-kafka) or JMeter
- **Node shop / prefer YAML over code** → Artillery (YAML, JS, TS; easy Lambda/Fargate cloud scale)

---

## Common Mistakes by Tool

These are the mistakes that cause silent CI failures, misleading
results, or test collapse at scale. Flag them proactively whenever
reviewing scripts or diagnosing problems - users often don't know to
ask about them.

### k6

- **`check()` without `thresholds`** - checks log pass/fail but do
  NOT fail the test run. Without thresholds, CI always reports green
  regardless of latency. Always add `thresholds` to `options`.
- **Data loaded inside `default()`** - loading CSV or JSON inside the
  VU function runs on every iteration, causing massive per-iteration
  overhead and OOM at scale. Always use `SharedArray` in the init
  scope.
- **`shared-iterations` for user journeys** - VUs race to claim
  iterations and may skip steps, producing incomplete journey metrics.
  Use `per-vu-iterations` for any multi-step flow.
- **No `sleep()` between steps** - 100 VUs with zero think time
  generates the absolute maximum RPS for that iteration time, far
  exceeding what 100 real concurrent users produce. Always add
  realistic think time.
- **`console.log` in `default()`** - causes 30–50% throughput drop
  under load. Use custom metrics (`Counter`, `Trend`) instead.
- **Hardcoded `BASE_URL`** - use `__ENV.BASE_URL` for environment
  portability.

### JMeter

- **Listeners enabled in non-GUI runs** - View Results Tree, Aggregate
  Report etc. buffer all samples in memory during headless runs,
  causing memory leak and eventual crash. Disable all listeners before
  CI execution; use `-l results.jtl` for output.
- **Missing correlation on session-heavy apps** - JSESSIONID, CSRF
  tokens, ViewState, OAuth codes must be extracted and reused. Without
  correlation, the test fails for every user after the first.
- **Hardcoded thread counts** - parameterize via JMeter properties
  (`${__P(threads,10)}`) so CI can override without editing the JMX.
- **Zero think time** - never reflects real user behavior; always add
  at minimum a Constant Timer (300–500ms) between samplers.
- **Throughput Controller % mode misuse** - percentage applies per
  iteration of the parent controller, not globally. Most users expect
  global percentage; use `Total Executions` mode instead or be
  explicit.

### Gatling

- **Blocking calls inside `exec()`** - any blocking I/O inside an exec
  block stalls the entire Akka actor, killing simulation concurrency.
  Use Gatling's async feed/session API exclusively.
- **Missing `.check()` on responses** - without checks, 4xx and 5xx
  responses are silently counted as successful. Always add at minimum
  `.check(status.is(200))`.
- **Fixed `pause()` values** - use `uniformPaused(min, max)` or
  `normalPausedWithPercentageDuration` for realistic think time
  distribution.

### Locust

- **`self.client` without `catch_response=True`** - by default, Locust
  marks any HTTP response as success regardless of status code. Use
  `with self.client.get(..., catch_response=True) as r:` and call
  `r.failure()` explicitly.
- **Unequal task weights without intent** - tasks default to equal
  weight; if your user journey has unequal step frequency, set weights
  explicitly or the journey ratio will be wrong.
- **Master + workers on same machine** - causes resource contention
  that skews both throughput and latency measurements. Always run
  workers on separate machines or containers for distributed tests.

### Artillery

- **No `ensure` block** - without `ensure`, Artillery reports metrics
  but always exits 0, so CI never fails on latency or error spikes.
  Always add `ensure.thresholds` (or `conditions`) for SLA gates.
- **`arrivalRate` mistaken for concurrency** - it is new users per
  second (open model). On a slow backend, pending VUs pile up unbounded.
  Set `maxVusers` to cap real concurrency, or use `arrivalCount`.
- **Strict captures aborting VUs** - captures are strict by default;
  a missed extractor stops the whole VU. Only set `strict: false`
  when a downstream 404 is acceptable.
- **`payload.order: sequence` in distributed runs** - sequential CSV
  consumption breaks under Lambda/Fargate workers (each has its own
  copy). Use the default `random` ordering for distributed tests.
- **Zero `think` time** - 1 VU/sec with no think time fires the
  maximum RPS for the journey; add `think` to model real pacing.
- **Forgetting `http.response_time` is TTFB** - latency metrics are
  time-to-first-byte by default. Enable `config.http.extendedMetrics`
  for full download timing (`http.total.*`) when that matters.

---

## Concept Mapping Across Tools

Use this when users are migrating between tools or asking how a
concept from one tool maps to another. Claude should always provide
the specific mapping rather than a generic explanation.

| Concept          | JMeter                  | k6                      | Gatling                  | Locust                   | Artillery                | LoadRunner          |
|------------------|-------------------------|-------------------------|--------------------------|--------------------------|--------------------------|---------------------|
| Virtual user     | Thread                  | VU                      | User                     | User                     | VU (arrival per sec)     | Vuser               |
| Test plan        | .jmx file               | .js / .ts script        | Simulation class         | .py file                 | .yml / .js / .ts script  | VuGen script (.usr) |
| User entrypoint  | Thread Group            | `default()` function    | `scenario()`             | task methods             | `flow` in scenario       | `Action()`          |
| Concurrency ctrl | Thread Group settings   | executor                | `inject()`               | `spawn_rate`             | `maxVusers` / `arrivalRate` | Vuser Group         |
| Think time       | Constant/Uniform Timer  | `sleep()`               | `pause()`                | `time.sleep()`           | `think`                  | `lr_think_time()`   |
| Inline assertion | Response Assertion      | `check()`               | `.check()`               | `catch_response`         | `afterResponse` hooks    | `lr_eval_string()`  |
| SLA enforcement  | Duration Assertion      | `thresholds`            | Assertions (Enterprise)  | custom + exit code       | `ensure` plugin          | SLA definition      |
| Correlation      | Regex / CSS Extractor   | `res.json()` / regex    | `.check()` + `saveAs()`  | `response.text` + regex  | `capture` (json/xpath/regexp/header) | `web_reg_save_param`|
| Data feed        | CSV Data Set Config     | `SharedArray`           | `feeder`                 | CSV reader               | `payload` / `variables`  | `lr_paramarr()`     |
| Grouping         | Transaction Controller  | `group()`               | `group()`                | task sets                | `name` on scenario       | Transaction         |
| Distributed      | Controller + Agents     | k6 cloud / k6 operator  | Gatling Enterprise       | master + workers         | Lambda / Fargate workers | Load Generator      |
| Results output   | .jtl (CSV/XML)          | JSON / InfluxDB / cloud | simulation.log           | CSV / Locust web UI      | JSON / HTML report       | .lrr file           |

---

## Threshold Starting Points

These are community baselines - always tell the user to adjust these
to their actual SLA requirements. Never present them as universal
targets.

| Endpoint type    | p95       | p99        | Error rate | Notes                              |
|------------------|-----------|------------|------------|------------------------------------|
| Web page (HTML)  | < 3000ms  | < 5000ms   | < 1%       | Aligns with Google CWV LCP < 2.5s  |
| REST API         | < 500ms   | < 1000ms   | < 1%       | Common industry baseline           |
| Auth / Login     | < 300ms   | < 500ms    | < 0.1%     | Stricter - security-sensitive path |
| Search / Query   | < 800ms   | < 1500ms   | < 0.5%     | Varies heavily by dataset size     |
| Write (POST/PUT) | < 800ms   | < 1500ms   | < 0.5%     | Includes DB write latency          |
| Checkout/Payment | < 1000ms  | < 2000ms   | < 0.1%     | Stricter - revenue-critical path   |
| Background/async | < 5000ms  | < 10000ms  | < 2%       | Batch jobs, async processors       |

**k6 specific:** Always define both `http_req_duration` AND
`http_req_waiting` as separate thresholds. `http_req_waiting`
(TTFB) isolates server-side latency from network overhead - it is
the first metric to check when diagnosing high p95. Always include
`checks: ['rate>0.99']`.

**JMeter specific:** Add both a Response Assertion and a Duration
Assertion per sampler. Never rely on listener output alone for
CI pass/fail; use the JMeter exit code driven by assertions.

---

## Performance Testing Lifecycle Overview

Always think through these phases when helping a user - they often ask
about one phase but need context from others.

```
1. PLAN
   └─ Workload design → concurrency model → SLA targets → test type
       → references/topics/workload-design.md

2. DATA
   └─ Identify variables → parameterization strategy → data generation
       → references/topics/test-data.md

3. SCRIPT
   └─ Record or code → correlation → parameterization → assertions
       → references/topics/script-generation.md + tool-specific file

4. EXECUTE
   └─ Local → distributed → CI/CD → cloud burst → monitoring hooks
       → references/topics/test-execution.md

5. OBSERVE
   └─ APM → metrics → logs → traces → dashboards
       → references/topics/observability.md

6. ANALYZE
   └─ Throughput, latency percentiles, errors → bottleneck ID → report
       → references/topics/results-analysis.md

7. PRODUCTION
   └─ Canary testing → shadow load → chaos → synthetic monitoring
       → references/topics/production-testing.md
```

---

## Common Performance Test Types

| Test Type        | Goal                                  | Key Metric                              |
|------------------|---------------------------------------|-----------------------------------------|
| **Load**         | Validate system at expected load      | Response time, throughput, error rate   |
| **Stress**       | Find the breaking point               | Max VUs before degradation, error onset |
| **Soak/Endurance** | Detect memory leaks, slow degradation | Resource trend over time (hours)      |
| **Spike**        | Behavior under sudden traffic burst   | Recovery time, error spike              |
| **Capacity**     | Find max sustainable load             | Throughput ceiling at SLA thresholds    |
| **Smoke**        | Quick sanity check                    | Single VU - no errors                   |
| **Breakpoint**   | Incremental ramp until failure        | Failure threshold VU count              |

---

## Key Principles to Always Apply

1. **Never test against production blindly** - always have a rollback
   plan and alerting in place.
2. **Baseline first** - always establish a baseline before stress or
   soak runs.
3. **Think time and pacing matter** - unrealistic zero-think-time tests
   produce misleading results.
4. **Parameterize everything** - hardcoded credentials, tokens, and IDs
   will fail at scale.
5. **Assertions are not optional** - tests without assertions are just
   generating traffic, not validating behavior.
6. **Isolate the system under test** - shared environments invalidate
   results.
7. **Correlate dynamic values** - session tokens, CSRF, ViewState etc.
   must be extracted and reused.

---

## Asking the Right Questions

When a user brings a performance problem, ask (or infer) these before
prescribing a solution:

- What is the **target concurrency** (VUs or RPS)?
- What is the **SLA** (e.g., p95 < 500ms, error rate < 1%)?
- What is the **protocol** (HTTP/REST, gRPC, JDBC, WebSocket)?
- Is the app **stateful** (session-based) or **stateless**
  (token-based)?
- Where will tests **run from** (local, CI, cloud)?
- What **environment** is being tested (dev, staging, prod)?
- Is there an **APM tool** in place (Datadog, Dynatrace, Grafana,
  New Relic)?