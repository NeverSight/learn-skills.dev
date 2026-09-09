---
name: oodle-triage
description: Triages production alerts using observability signal. Mode A gathers confirmed-vs-inferred context for a single alert or ticket and updates the tracker; Mode B fans out over alerts that fired in a window, suppresses muted and unrouted noise, dedupes via a stable fingerprint, and files or updates issues idempotently. Correlates alerts to recent changes through the O11y Change Context manifest. Use when investigating an alert or incident, or running scheduled oncall triage.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,observability,oncall,triage,incident,alerts
  globs: ""
  alwaysApply: "false"
---

# Oodle Triage — Right-Side Observability

Turn an alert into evidence, not narrative. This skill gathers production context
and files disciplined tickets. It closes the loop opened on the left: it reads the
[O11y Change Context](../oodle-o11y-context/SKILL.md) manifest on recent PRs to
connect a firing alert to the change that likely caused it.

> **Prime directive:** separate what is *proven* from what is *inferred* at every
> step. A confirmed symptom, a leading hypothesis, and the exact missing evidence
> beats a tidy root-cause story built on correlation. Evidence before assertions.

## Modes

- **Mode A — Triage context:** input is a single alert, a tracker ticket id, or a
  symptom description → produce a context report and optionally update the ticket.
- **Mode B — Auto oncall triage:** input is a time window (and a tracker parent
  issue) → enumerate everything that fired, dedupe, and file/update sub-issues.
  Designed to run on a `/loop` cadence.

If the input names one alert/ticket/symptom, use Mode A. If it asks to triage a
window or "everything that fired," use Mode B (which reuses Mode A per alert).

## Discovery (do this first)

Resolve backends by **capability and tool shape**, never by a hard-coded server
name (names vary: `oodle-ai-us1`, `ap1`, `staging`, `dev`, or customer-custom).

- **Observability MCP** — find tools for alerts/monitors, metric (PromQL) queries,
  logs, and traces. If the suite matches Oodle's shape, use the tight path: select
  the environment that owns the service, and load a matching `load_skill__*`
  workflow when one fits the problem (e.g. Kubernetes debugging, alert-noise
  analysis) **before** low-level calls.
- **Issue-tracker MCP** — find the tracker in use. Linear is the worked example
  below; Jira is the analog (issue → sub-issue, states, comments map across).
- If a backend is missing, do what the available signal allows and state the gap.

## Mode A — Triage context

1. **Establish ground truth, in writing.** If given a ticket, fetch it for scope.
   Pin service/component, cluster/env, pod(s), container, and the precise **time
   window** before querying anything. Convert the window to **both UTC and the
   reporter's local zone** — mixing them silently is a classic error.
2. **Confirm the symptom with hard signals** before theorizing: restart/OOM
   reason, error rate, latency, resource usage vs limit, event logs. State the
   confirmed symptom in one line; everything after is explanation.
3. **Learn the instrumentation from the code.** Read the relevant service code for
   the *actual* metric names, log strings, and span attributes — do not guess
   them. Note explicitly **what is and isn't captured**; knowing what is missing
   reveals which questions the telemetry cannot answer.
4. **Triangulate across telemetry** — don't lean on one source. Metrics (grouped
   by every dimension that localizes blame: service, tenant, operation, pod,
   status), logs from **caller and callee** on the path (read ERROR/WARN and
   access logs, widen the filter if a reported log isn't found), traces end to
   end, and profiles for resource incidents.
5. **Correlate with recent changes (loop closes here).** Find recent PRs touching
   the alerting service (via the GitHub or Linear MCP, or the `gh` CLI when no
   GitHub MCP is present) and read their
   [O11y Change Context](../oodle-o11y-context/SKILL.md) blocks. `watch` items
   and `type` focus the hypotheses (a `watch: N+1 ...` becomes the leading
   hypothesis); `guarded-by` confirms the alert↔code link; `gaps` explains
   evidence the telemetry was never built to provide.
6. **Track and label every finding `Confirmed | Inferred | Unknown`.** A
   configured ceiling or default is not a measurement; co-occurrence is not
   causation. Actively try to **falsify the leading hypothesis with one
   measurement** — eliminating a candidate is worth more than adding support.
7. **When confirmation is impossible, stop and produce a ranked missing-evidence list:**
   for each item, which hypothesis it would confirm/refute, where it likely lives,
   and whether it is accessible. Then ask to unblock the top item rather than
   guessing past it.

**Output** — a short, honest report: confirmed **Symptom** (with UTC+local
timestamps), **Attribution** (who/what/where, to the extent proven), **Leading
hypothesis** (proven vs inferred, plainly), **Ruled out** (with the measurement),
**Missing evidence** (the ranked list). Offer to post it as a comment on the
tracker ticket.

## Mode B — Auto oncall triage

Run Mode A's investigation per alert, wrapped in enumerate → suppress → dedupe →
file. Match-check strictly precedes any create so reruns never double-file.

1. **Enumerate what fired** in the window — the alert instances that reached the
   **firing** state. **Never treat a pending/for-not-yet-satisfied condition as a
   fire:** it sends no notification and must not be triaged or filed. Confirm a
   real fire from the alert-state signal or trigger history.
2. **Enrich** each: still-active now, noise category (flapping/storm/perpetual/
   auto-resolving/boundary) and trigger count over ~7d, **muted?** (an active
   muting rule whose matchers all match this alert's monitor + scope), and
   **routed?** (does the monitor page anyone, or is it unrouted).
3. **Suppress muted and unrouted alerts** — they are not actionable oncall signal.
   Do not file them. If a stale ticket exists for a now-muted or now-unrouted
   alert, close it with a comment stating the reason (muting rule id + matchers,
   or unrouted monitor id). Suppress the specific instance, not a whole alert
   class — routing is per-monitor per-env.
4. **Collapse storms** — many series of one monitor firing together become **one**
   logical alert → one ticket, not N.
5. **Investigate** each distinct fired alert with Mode A, depth scaled to
   severity. Manifest correlation feeds probable-cause and suggested-fix.
6. **Dedupe & file** against the tracker by **semantic match anchored on the
   fingerprint** (env + monitor + scope): no match → create; match open → comment
   the new occurrence; match closed → reopen and comment. Set priority from
   severity. Retry a failed write once; never leave a half-created duplicate.
   Rerunning the same window is idempotent.

## Fingerprint block

Every filed ticket carries a stable fingerprint so future runs match it. Keep the
format constant:

```
## Fingerprint
- env: <env>
- monitor: <monitor id/name>
- scope: <key=value scope labels>
- links: <deep links to the backend>
```

## Genericity vs Oodle-tight

The **discipline** is vendor-neutral: confirmed-vs-inferred labeling, firing-only
enumeration, suppressing muted/unrouted noise, storm collapse, fingerprint dedup,
and manifest correlation apply to any backend. The **mechanics** are backend-
specific: Oodle exposes an `ALERTS`-style state metric, `muting_rules` with typed
matchers, and a monitor routing flag; a different vendor's MCP supplies its own
equivalents. Use the equivalent where it exists; skip a step where the concept is
genuinely absent — never invent a mechanic a backend does not have.

For the Oodle CLI path when deeper queries help, lean on
[oodle-metrics](../oodle-metrics/SKILL.md),
[oodle-logs](../oodle-logs/SKILL.md), and
[oodle-traces](../oodle-traces/SKILL.md) rather than restating them here.
