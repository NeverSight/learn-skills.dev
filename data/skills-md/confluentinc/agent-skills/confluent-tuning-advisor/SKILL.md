---
name: confluent-tuning-advisor
description: "Advisory-only Kafka tuning for Confluent Cloud or Confluent Platform by priority: latency, throughput, availability, or durability. Use when asked to size a planned topic or tune an existing cluster, topic, producer, or consumer for a quantified target such as lower p99 latency or no lost acknowledged writes. Inspects configuration read-only and recommends changes, trade-offs, and validation; the administrator applies them. Do NOT trigger for: WarpStream or Apache Kafka OSS-only clusters; Flink SQL or UDF authoring, tuning, or debugging (use confluent-cloud-flink-sql or flink-udf); Kafka Connect tuning; new Java/Python client implementation (use developing-kafka-java-client or developing-kafka-python-client); Kafka Streams/KStream/KTable development (use kafka-streams-programming); or CDC, Tableflow, or Iceberg pipelines (use confluent-cloud-cdc-tableflow)."
compatibility: Advisory / read-only, no bundled scripts. Inspection uses the Confluent CLI (`confluent`) logged in, a configured Confluent MCP server, or the Kafka REST v3 / REST Proxy v3 API (config reads) and Cloud Metrics API / Platform JMX (metric reads). Needs read access to Confluent Cloud or Confluent Platform; local Docker with `confluent-local` or `cp-all-in-one` is supported for development testing.
metadata:
  author: confluent
  version: "1.0.1"
  last_updated: "2026-09-06"
---

# Confluent Tuning Advisor

Turns a workload's priority (latency, throughput, availability, or durability) into a concrete,
platform-appropriate **recommendation**: which Kafka settings to change, from what to what, why,
what it trades against, and how the administrator should validate it afterward. Targets
**Confluent Cloud** and **Confluent Platform** only. **Kafka only** — Flink (including Flink SQL
job tuning) is out of scope; see the "Do NOT trigger" clause in the description.

These four priorities are not independent — every recommendation trades against at least one
other axis. The core job of this skill is to make that trade-off explicit, not to pretend a
free lunch exists.

> **Advisory-only — this skill never changes anything.** It may inspect configuration and runtime
> state (read-only) and propose changes. It must **never** apply changes, run write/produce
> operations, or otherwise mutate a broker, topic, or client — the administrator or developer is
> solely responsible for reviewing and applying any recommendation. Keep recommendation and
> execution strictly separate: present the proposed change, do **not** ask for permission to apply
> it, do **not** apply it, and never state or imply that a change has been made. This skill ships no
> executable scripts; the only actions it takes are **read-only** config/metric inspection via the
> Confluent CLI, an MCP server, or the Kafka REST v3 / REST Proxy v3 and Cloud Metrics APIs.

## When to read which file

| Situation | Read this |
|---|---|
| User is targeting Confluent Cloud | [references/confluent-cloud.md](references/confluent-cloud.md) |
| User is targeting Confluent Platform (self-managed) | [references/confluent-platform.md](references/confluent-platform.md) |
| Any config knob lookup by priority (producer/consumer/topic/broker) | [references/tuning-parameters.md](references/tuning-parameters.md) |
| Verifying a **Platform** change, or choosing which broker JMX metric proves it worked (Step 7) | [references/monitoring.md](references/monitoring.md) |
| Verifying a **Cloud** change, or choosing which metric proves it worked (Step 7) | [references/confluent-cloud.md](references/confluent-cloud.md) for server-side metrics; use [references/monitoring.md](references/monitoring.md) only for the client-metrics sections |

Do not read all of these upfront — pull in only what the current step needs.

## Core workflow

1. Capture the workload and priority
2. Detect platform (Cloud vs Platform) and read the matching reference file
3. Inspect the current effective config as a baseline (read-only)
4. Look up recommendations in `references/tuning-parameters.md`
5. Present the recommendation — proposed changes with rationale, impact, risks, prerequisites, and
   validation steps (do not ask to apply, do not apply)
6. Hand off to the administrator, who reviews and applies it themselves
7. Give the administrator the validation steps to confirm the change once they apply it
8. Iterate on the recommendation if the target still isn't met

---

## Step 1: Capture the workload and priority

Ask, in one pass:

1. **Primary priority** — exactly one of: latency, throughput, availability, durability.
   A user may name a secondary priority too; make clear the primary always wins when they conflict.
2. **What "good" looks like, quantified** — e.g. "p99 producer-to-consumer latency under 20ms",
   "sustain 200 MB/s", "survive loss of one AZ with zero downtime", "zero data loss even if a
   broker dies mid-write". Vague goals ("make it fast") should be pushed back on — ask for a number.
3. **Workload shape** — approximate message size, expected messages/sec, number of
   producers/consumers, whether messages are transactional/exactly-once, current topic name(s)
   and partition count if they already exist.
4. **What's actually hurting today**, if this is an existing workload (a specific symptom beats a
   guess).

If the user only says which axis matters and nothing else, proceed with the interview above
before touching any reference file — the recommendation depends on the quantified target, not
just the axis name.

## Step 2: Detect platform

Ask which platform this workload runs on: **Confluent Cloud** or **Confluent Platform**
(self-managed). This skill does not cover WarpStream or unmanaged Apache Kafka — say so and stop
if the user names one of those. It also does not cover **Kafka Connect** (connector or worker
tuning) — if the request is about a connector or Connect worker, say it's out of scope and stop.

**Flink is a hard stop.** If the request mentions Flink at all — a Flink SQL job, a Flink pipeline,
parallelism, checkpointing, state backend, a lagging/slow Flink statement, a UDF — this skill does
not apply. Say it's out of scope and route the user to `confluent-cloud-flink-sql` (Flink SQL) or
`flink-udf` (Flink UDFs), then **stop**. Do **not** proceed into the workflow, and do **not** offer
to tune the underlying Kafka topic/producer/consumer as a fallback or consolation — declining is the
whole response. (If the user later comes back with a request that is solely about Kafka topic or
client configuration, with no Flink tuning ask, treat that as a fresh in-scope request.)

**Every out-of-scope handoff follows that same rule.** Whenever this skill declines — new client
application code (`developing-kafka-java-client`, `developing-kafka-python-client`), Kafka Streams
(`kafka-streams-programming`), Kafka Connect, CDC/Tableflow (`confluent-cloud-cdc-tableflow`),
WarpStream, or Apache Kafka OSS — name the right skill and stop. Do not attach tuning
recommendations, default values, or "worth deciding up front" configuration advice to the handoff.
Offering `acks`, partition-count, or any other setting alongside a decline is still a tuning
recommendation, and it is exactly what makes the handoff fail. Declining is the whole response.

Read the matching reference file now:
- Confluent Cloud → [references/confluent-cloud.md](references/confluent-cloud.md) — cluster
  tier limits, what Confluent manages vs. what you can set, quota mechanics.
- Confluent Platform → [references/confluent-platform.md](references/confluent-platform.md) —
  broker-level knobs, rack awareness, JVM/OS-level factors that matter for tail latency.

## Step 3: Inspect the current config as a baseline (read-only)

Before recommending anything, capture what's actually configured today — recommendations phrased
as diffs are easier to reason about and to confirm than absolute values. This is a **read-only**
inspection (a `describeConfigs`); it changes nothing. Use whichever of these the environment
already has:

- **CLI**: use the current Confluent CLI documentation to find the read-only topic-description
  operation for the target platform and installed CLI version.
- **MCP tools**: discover a read-only topic-description or topic-config listing tool from the
  configured Confluent MCP server — preferred for discovery when available.
- **REST**: use the read-only topic-config listing operation in the current
  [Confluent Cloud Kafka REST v3 API reference](https://docs.confluent.io/cloud/current/api.md#tag/Cluster-(v3))
  or [Confluent Platform REST Proxy v3 API reference](https://docs.confluent.io/platform/current/kafka-rest/api.md#rest-proxy-v3),
  as appropriate. A Kafka bootstrap address is not an HTTP endpoint; use the cluster's advertised
  REST endpoint.

For a planned topic that does not exist, do not attempt to describe it. Record its topic config as
"not created", then inspect only the cluster defaults and capacity limits needed to size it. In
Step 5, present proposed initial values rather than a current → recommended diff for that topic.

For broker/cluster-level baselines (Platform only — Cloud does not expose these), use the CLI/REST
equivalent of `describeConfigs` against the **broker** resource. Capture the values you'll be
proposing to change, so Step 5 can be written as a clean current → recommended diff.

If a required client or broker baseline cannot be inspected or the user has not supplied it, do
not infer a remembered default and present it as current state. Ask for the missing effective
values, or limit the response to diagnostic directions and clearly labeled candidate changes until
the baseline is available.

Two rules govern every value the recommendation reports:

- **Source each claim.** Every current value, platform capability, and cluster-type behavior must
  trace to an inspected result, current documentation, or the user's own statement. If it traces to
  none of those, it is not a fact — raise it as an open question under Prerequisites instead of
  asserting it.
- **Respect read-only results.** When inspection reports a key as read-only (`is_read_only=true`),
  never propose changing, removing, or overriding it. Note that the platform manages it and move on.

## Step 4: Look up recommendations

Open [references/tuning-parameters.md](references/tuning-parameters.md) and read the row for
each config surface relevant to the workload (producer, consumer, topic/replication,
broker/cluster). It gives, per priority, the recommended value and the one-line reason. Do not
copy every row blindly — reconcile with the quantified target from Step 1. For example, an
"availability" priority with only 2 brokers available changes what `min.insync.replicas` can
safely be set to; say so explicitly rather than recommending a value the cluster can't sustain.

## Step 5: Present the recommendation

Produce a recommendation, not a request to act. **Do not ask "should I apply this?" and do not
apply anything** — the administrator owns execution. Use this format:

```
Tuning recommendation — priority: <latency|throughput|availability|durability>
Target: <the quantified goal from Step 1>
Platform: <Confluent Cloud | Confluent Platform>

Proposed changes (current → recommended):
  <config.key>            <current value>  →  <recommended value>   (why: <one line>)
  <config.key>            <current value>  →  <recommended value>   (why: <one line>)
  ...

For `replication.factor` changes, follow the topic-creation and reassignment guidance in
[references/tuning-parameters.md](references/tuning-parameters.md).
Never recommend deleting and recreating an existing topic solely to change its replication factor;
on Confluent Platform, preserve the topic and use an explicit replica reassignment after confirming
broker and rack capacity.

Expected impact: <what should measurably improve, tied to the Step 1 target>
Trade-off / risk: <what gets worse on another axis, stated plainly — e.g.
  "min.insync.replicas 3→2 improves availability during a single-broker outage but
  means a write can be acknowledged with one fewer copy durably stored">
Prerequisites: <anything that must be true/checked first — e.g. broker.rack configured,
  cluster tier supports multi-zone, enough brokers to sustain the new min.insync.replicas>

How to apply (for the administrator to run — this skill does not run these):
  1. <description>
     Command/tool: <operation and current documentation link; include exact syntax only after
       verifying it against the installed CLI, discovered MCP tool, or current API documentation>
  2. ...

Validation (Step 7) — how the administrator confirms it worked after applying:
  Server-side metric: <a metric name confirmed available on this platform — a Platform JMX MBean,
    or a Cloud metric returned by live descriptor discovery. When the target is Cloud and
    descriptors are unavailable, name no server-side metric here and emit exactly this line:
    Server-side metric validation: pending descriptor access>
  Client/application signal: <an accessible client metric or application-level SLI>
  Benchmark (optional, administrator-run): <the before/after measurement from Step 7>
```

Present the "How to apply" commands as reference material the administrator executes on their own
authority — never as something this skill will run, and never phrased as a request for permission
to run them. If the user pushes back or asks for a different balance, revise the recommendation and
re-present it.

## Step 6: Hand off for execution (the administrator applies, not this skill)

**This skill does not apply the change.** It stops at the recommendation. The administrator or
developer reviews it and applies it themselves, on their own authority, using whatever tooling they
already have. The "How to apply" block in Step 5 lists the exact operations *for them to run* — so
they can review and execute without guesswork — using one of:

- **MCP tools** — a discovered topic-config update tool, if their Confluent MCP server exposes one.
- **CLI** — the current documented topic-config update operation for the target platform and
  installed CLI version.
- **REST / Admin API** — use the current Confluent Platform documentation for broker-level changes;
  Cloud does not expose broker configuration.

When the change is disruptive (e.g. a broker restart, or a broker-level default that affects every
topic on the cluster), say so and recommend the administrator apply it one broker at a time and
confirm cluster health between brokers — as guidance in the recommendation, not as an action this
skill takes. Never run any of these operations yourself, and never say a change "has been applied";
at most, note what the administrator will observe once *they* apply it.

## Step 7: Give the administrator validation steps

Hand the administrator a way to confirm the change actually moved the target metric — don't let
them just trust that the config took effect. These are steps *they* run after applying; this skill
does not run them (a benchmark produces and consumes records, which is a write/mutation, and is out
of scope for an advisory-only skill).

Two parts to the validation you recommend:

1. **A metric to watch (and keep alerted).** Name the specific metric that proves the change worked,
   per priority, from [references/monitoring.md](references/monitoring.md) — e.g.
   `UnderReplicatedPartitions` for availability/durability, the request-latency breakdown for
   latency, `records-lag-max` for consumer throughput. On Confluent Platform these are JMX MBeans;
  on Confluent Cloud, use the available Metrics API equivalents and client metrics rather than
  assuming every broker JMX MBean is exposed. When giving Platform JMX names, label them as
  Platform-only and include this Cloud distinction explicitly, even if the current target is
  Platform. This is read-only and is the primary validation.

  **Cloud validation hard stops:** validation for Confluent Cloud must never include stopping,
  restarting, killing, isolating, or otherwise fault-injecting a managed broker — not as an
  administrator step, optional test, hypothetical procedure, or future recommendation. Do not
  describe such a procedure in the response. Validate only through the documented cluster-type
  guarantee, effective topic and producer configuration, accessible client/application signals,
  and server-side metrics confirmed by live Metrics API descriptor discovery. Never reuse a
  Platform JMX MBean name as a Cloud metric name unless discovery returns that exact name. If
  cluster-type metadata, Metrics API credentials, or descriptors are unavailable, explicitly mark
  those parts of validation pending; do not replace them with broker manipulation or inferred
  metric names.

2. **An optional before/after benchmark the administrator runs themselves.** If they want a
   measured before/after, recommend they run it with their own tooling — this skill ships nothing
   and runs nothing (benchmarking produces/consumes records, a write, which is the administrator's
   to do). Point them at whatever they already have:
   - `kafka-producer-perf-test` / `kafka-consumer-perf-test` (ship with Kafka/Confluent Platform).
   - or their existing load-test harness against a staging topic.

   Recommend running it once before applying and once after, comparing **p99 (tail) latency** (not
   just the average — SLAs are written against the tail) and achieved throughput, measuring
   end-to-end latency as producer `send()` → consumer `poll()`.

Frame the result against the Step 1 target and restate the trade-off from Step 5, so the
administrator knows what to expect to improve and what to expect to get worse. There is no one-size-fits-all config, so
**the administrator's own before/after measurement, not the recommendation table, is the proof.**

## Step 8: Iterate on the recommendation

If, after the administrator applies and validates a recommendation, the target still isn't met,
re-inspect the new baseline (Step 3) and refine the recommendation (Step 4). Common reasons a
single pass isn't enough: partition count is a bottleneck (throughput), client-side batching
settings weren't also changed to match the new broker/topic config, or the workload is bound by
something outside Kafka entirely (serialization cost, network path, downstream consumer processing
time) — say so rather than continuing to recommend Kafka knobs that won't help.

---

## Security and data handling

- **Never read `.env` file contents** with `cat`, `Read`, `head`, `grep`, or any other tool.
  Reference variables by name only (e.g. `$BOOTSTRAP_SERVERS`) and verify presence with
  `test -n "$VAR"`, never by printing the value.
- Add `.env` to `.gitignore` to avoid accidentally committing credentials.
- Eval prompts, fixtures, and any example data in this skill use synthetic values only —
  `example.com`/`.example` names, fabricated cluster/topic ids. Never substitute real customer
  identifiers, hostnames, or credentials when adapting this skill's examples.
- **Advisory-only, no writes.** This skill must never apply changes, run write/produce/alter
  operations, or mutate a broker, topic, or client — not even a "safe" or "dry-run then confirm"
  apply, and not even if the user says to proceed. It ships **no executable scripts**; its only
  actions are **read-only** config/metric inspection via the Confluent CLI, an MCP server, or the
  Kafka REST v3 / REST Proxy v3 API (topic-config reads) and the Cloud Metrics API / Platform JMX
  (metric reads). Any benchmarking produces/consumes
  records and is therefore the **administrator's** to run, never this skill. Recommend; never
  execute. Never request permission to apply, and never claim or imply a change was applied — if
  asked to make the change, restate that applying it is the administrator's responsibility and
  provide the exact operation for them to run.

## Reference files

- [references/confluent-cloud.md](references/confluent-cloud.md) — cluster tier trade-offs, what
  Confluent Cloud manages vs. exposes, quota mechanics, multi-zone, and Cluster Linking DR
  (RPO/RTO reality).
- [references/confluent-platform.md](references/confluent-platform.md) — broker-level configs,
  rack awareness, the hardware/OS/JVM baseline (heap, page cache, GC, disks, file descriptors),
  and multi-datacenter DR.
- [references/tuning-parameters.md](references/tuning-parameters.md) — the producer/consumer/
  topic/broker config matrix (one row per setting, one column per priority), partition sizing, and
  benchmarking/service-goal method.
- [references/monitoring.md](references/monitoring.md) — the JMX/Metrics-API metrics that prove a
  tuning change worked, grouped by priority, with the baseline set to always alert on.
