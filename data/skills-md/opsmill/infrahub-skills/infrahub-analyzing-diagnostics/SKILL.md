---
name: infrahub-analyzing-diagnostics
description: >-
  Analyze an already-collected infrahub-collect diagnostic bundle —
  traceback and failure triage across service logs, incident correlation,
  and known-issue matching against opsmill/infrahub GitHub issues.
  TRIGGER when: the user says they collected a diagnostic bundle, gives
  you a bundle path, or pastes bundle contents — and asks what's wrong,
  wants the logs or tracebacks analyzed, asks "what does this bundle
  say", wants errors triaged/correlated, or asks whether a crash is a
  known issue.
  DO NOT TRIGGER when: no bundle exists yet — collect one first
  (use infrahub-collecting-diagnostics), filing the issue itself
  (use infrahub-reporting-issues), or querying live data
  (use infrahub-analyzing-data).
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Diagnostics Analyzer

## Overview

`infrahub-collecting-diagnostics` produces a bundle;
this skill is the next step — it reads that bundle
and turns raw logs into a triage report. It parses
`bundle_information.json`, sweeps every service's
logs for error signals (tracebacks, ERROR/CRITICAL
lines, panics, OOM kills, restart evidence),
correlates related errors into incidents, and
searches existing `opsmill/infrahub` GitHub issues
so the user learns whether their crash is already
known before anyone files anything.

The output is a findings report grounded in bundle
evidence — not a fix. The skill is strictly
read-only toward the deployment: it reads files from
an already-collected bundle and runs GitHub
searches; it never touches the running Infrahub
instance and never applies remediation.

## When to Use

Trigger this skill when the user says things like:

- "I collected a bundle — can you tell me what's
  wrong?"
- "Analyze these Infrahub logs / this bundle"
- "What do the tracebacks in the bundle mean?"
- "Is this crash a known Infrahub issue?"
- "Why did the task-worker keep restarting?"

Do not trigger when:

- No bundle exists yet — hand off to
  `infrahub-collecting-diagnostics` to collect one
  first. Do not hand-roll log collection here.
- The user wants to file a bug or feature request
  (use `infrahub-reporting-issues`)
- The user is asking operational questions about
  live data (use `infrahub-analyzing-data`)

## Workflow

Follow these steps in order.

### 1. Ask for the bundle location (user-gate)

Ask the user where the bundle is — never scan the
filesystem for it or assume the collector's default
output directory. A machine often holds several
bundles, and picking the wrong one produces a
confident report about the wrong incident.
Mentioning the default as a hint is fine
(`./infrahub_bundles/` when `--output-dir` wasn't
set), but the user names the path. Skip the question
only when the user already gave a path or pasted the
bundle contents. Once given, confirm it looks like
an `infrahub-collect` bundle — a `bundle/` directory
containing `bundle_information.json`. If there is no
bundle at all, stop and hand off to
`infrahub-collecting-diagnostics`; do not scrape
`docker compose logs`/`kubectl logs` as a substitute.
See
[rules/workflow-ask-bundle-location.md](rules/workflow-ask-bundle-location.md).

### 2. Read the manifest first, then anchor the deployment context

Read `bundle/bundle_information.json` before opening
any log. It records what was collected, what failed,
and for which deployment. Collection failures are
findings in their own right — a service whose logs
could not be collected is often the service that is
down. See
[rules/workflow-manifest-first.md](rules/workflow-manifest-first.md).

Then establish the deployment context — running
Infrahub version, topology (Compose or Kubernetes),
replica counts — and open the report with it. The
version is what later turns a matched GitHub issue
into a conclusion ("already fixed in X.Y.Z —
upgrade" vs "already running the fix — possible
regression"). See
[rules/workflow-deployment-context.md](rules/workflow-deployment-context.md).

### 3. Sweep for error signals

Scan **every** service directory under
`bundle/logs/` — not just the server — for the
signal classes in
[rules/triage-error-signals.md](rules/triage-error-signals.md):
Python tracebacks, ERROR/CRITICAL log lines, panics,
OOM kills, and connection failures. Treat any
`*.previous.log` file as restart evidence and read
its tail — the pre-restart log usually holds the
crash cause
([rules/triage-restart-evidence.md](rules/triage-restart-evidence.md)).
`reference.md` has ready-made grep patterns per
signal class.

If the manifest shows a benchmark was collected
(`create --benchmark`), evaluate it alongside the
logs — the single-CPU score and the storage IOPS of
the Neo4j/PostgreSQL volumes often decide whether a
slowness symptom is a software issue or an
undersized host. If it's absent and the symptom is
performance-shaped, the report must recommend a
next bundle with `--benchmark`. See
[rules/triage-benchmark-results.md](rules/triage-benchmark-results.md).

### 4. Correlate into incidents

Group the raw signals by timestamp and causal chain
into incidents — one incident per underlying
problem, with root errors distinguished from cascade
errors in downstream services. A database OOM at
14:02 followed by server connection errors at 14:02+
is one incident, not two. See
[rules/correlate-into-incidents.md](rules/correlate-into-incidents.md).

### 5. Match against existing GitHub issues

For each incident backed by a traceback or a
distinctive error message, build a search key from
its stable parts (exception class, normalized
message, innermost Infrahub frame — variable IDs,
branch names, and hostnames stripped) and search:

```bash
gh search issues --repo opsmill/infrahub "<stable keywords>"
```

The default search covers open and closed issues —
do not pass `--state`, which would hide one half.

Present the top matches with title, state, and URL —
which is all `gh search issues` returns. The fix
version is not in that output, so open a promising
match for it and compare it against the deployment
context from step 2; when the issue names no version,
say so and leave the upgrade question open. See
[rules/match-stable-search-keys.md](rules/match-stable-search-keys.md)
for key construction and fallbacks when `gh` is
unavailable, and [reference.md](reference.md) for the
command that reads a match, plus the known failure
patterns worth checking before searching — several
common symptoms have well-understood causes that make
the search targeted instead of generic.

### 6. Report findings

Write the findings report: one section per incident,
each with severity, the evidence (bundle file paths
plus quoted excerpts), the correlation reasoning,
and any matching GitHub issues. Every claim must
trace back to a quoted bundle line; unknowns are
stated as unknowns
([rules/report-evidence-per-finding.md](rules/report-evidence-per-finding.md)).
Include in the open questions whether the symptom
reproduces on demand and when it last did — a
reproduced timestamp sharpens the incident window
and tells the next bundle what to capture.
The report recommends next steps but applies none —
no restarts, no config edits
([rules/scope-read-only-analysis.md](rules/scope-read-only-analysis.md)).

### 7. Hand off

Close with the right hand-off for what was found:

- A matching open GitHub issue → point the user to
  it; commenting with their reproduction goes
  through `infrahub-reporting-issues`.
- No match and the user wants to file → hand off to
  `infrahub-reporting-issues`. Never run
  `gh issue create` from this skill.
- Deeper expert help needed → the bundle plus this
  report go to OpsMill support, following the
  review-before-sharing gate from
  `infrahub-collecting-diagnostics`. If the findings
  suggest a reproducer is needed, propose a minimal
  reproducible example first; a full backup
  (`--include-backup`) is the last resort, not the
  default ask.

See
[rules/cross-link-skill-boundaries.md](rules/cross-link-skill-boundaries.md).

## Rule Categories

| Prefix | Category | Description |
| ------ | -------- | ----------- |
| workflow | Workflow | Manifest first; collection failures are findings |
| triage | Triage | Error-signal classes, all services, restart evidence |
| correlate | Correlation | Group signals into incidents; root vs cascade |
| match | Issue matching | Stable search keys against opsmill/infrahub issues |
| report | Reporting | Evidence per finding; unknowns stay unknowns |
| scope | Scope | Analysis only — no mutations, no fixes |
| cross-link | Cross-linking | Hand-offs to sibling skills |

See [rules/_sections.md](rules/_sections.md) for the
full index.

## Supporting References

- [reference.md](reference.md) — signal-class grep
  patterns, per-service log formats, manifest fields,
  and `gh search` recipes. **Read in steps 3-5.**
- [examples.md](examples.md) — end-to-end example:
  bundle excerpts in, findings report out.
- [../infrahub-collecting-diagnostics/reference.md](../infrahub-collecting-diagnostics/reference.md)
  — the authoritative bundle layout produced by
  `infrahub-collect`.
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap.

## Anti-patterns

- **Deducing the bundle location.** No filesystem
  scans, no "newest directory wins", no assuming
  `./infrahub_bundles/`. Ask; the user names the
  path.
- **Diagnosing without evidence.** Every finding
  cites a bundle path and a quoted excerpt. A
  plausible story that no log line supports is
  speculation, and it must be labeled as such.
- **Reporting a flat error list.** Fifty connection
  errors downstream of one database OOM are one
  incident. Correlate before reporting.
- **Searching GitHub with volatile tokens.** Branch
  names, UUIDs, hostnames, and timestamps make
  searches return nothing. Strip them; search the
  stable parts.
- **Fixing instead of analyzing.** No restarts, no
  `docker`/`kubectl` mutations, no config edits.
  Recommendations go in the report; actions go to
  the user or to OpsMill support.
- **Filing a GitHub issue from this skill.** That is
  `infrahub-reporting-issues`. Cross-link, don't
  duplicate its routing and sanitization.
- **Re-collecting by hand when the bundle is
  incomplete.** A partial bundle is expected on a
  degraded deployment; the manifest records the gap.
  If more data is genuinely needed, hand back to
  `infrahub-collecting-diagnostics`.
