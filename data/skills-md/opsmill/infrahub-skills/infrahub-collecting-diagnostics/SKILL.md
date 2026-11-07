---
name: infrahub-collecting-diagnostics
description: >-
  Collect a redacted local diagnostic bundle (logs, config, version, state)
  for an OpsMill expert hand-off.
  TRIGGER when: Infrahub is broken/failing/erroring, the user asks for help
  debugging, wants to collect logs/diagnostics, prepares a hand-off for OpsMill
  support, or reports a crash/timeout/connection issue (upgrade failure, stuck
  branch, container CrashLoopBackOff, 500s, OOM).
  DO NOT TRIGGER when: debugging a check, transform, generator, menu, or schema
  in the repository (use the infrahub-managing-* skills), a bundle has already
  been collected and the user wants
  it analyzed (use infrahub-analyzing-diagnostics), filing a public GitHub
  issue (use infrahub-reporting-issues), running operational queries
  (use infrahub-analyzing-data), or planning an upgrade that has not run yet
  (use infrahub-planning-upgrades).
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Diagnostics Collector

## Overview

When an Infrahub user reports a problem, an expert
(OpsMill support, or a senior engineer) needs a
consistent set of artifacts to triage it: logs,
config, version info, and environment state. This
skill runs [`infrahub-collect`](https://docs.infrahub.app/backup/collect/install),
OpsMill's dedicated diagnostic-bundle tool, to
produce that artifact set.

The skill is a **guide around the binary**, not a
hand-rolled collector. It does not diagnose root
cause, does not file a GitHub issue (use
`infrahub-reporting-issues` for that), and does not
mutate Infrahub state — `infrahub-collect` only reads.

## When to Use

Trigger this skill when the user says things like:

- "Infrahub is broken / failing / erroring"
- "Help me debug this"
- "I need to collect logs to send to OpsMill"
- "Something went wrong after the upgrade"
- "My proposed change is stuck"
- "The UI is throwing 500s"

Do not trigger when:

- The user wants to file a public GitHub issue
  (use `infrahub-reporting-issues`)
- The user is asking operational questions about
  data ("how many devices in site X")
  (use `infrahub-analyzing-data`)
- The user wants to audit their schema against
  best practices (use `infrahub-auditing-repo`)

## Workflow

Follow these steps in order. Two user-gates;
everything else is automatic.

### 1. Capture the problem

Ask the user to describe the problem in their own
words if they haven't already. Don't probe yet —
listen for product names, version numbers, error
messages, workflow context. This informs which
`create` flags to add in step 4.

### 2. Install & verify

Check whether the binary is already available:

```bash
infrahub-collect version
```

If it's missing, install it for the user's OS/arch
and confirm again with `infrahub-collect version`
(or `infrahub-collect --help`). See
[rules/install-and-verify.md](rules/install-and-verify.md)
for the exact install command, sudo, and airgap
notes.

### 3. Detect the environment

```bash
infrahub-collect environment detect
```

If detection is ambiguous (multiple Compose projects,
non-default K8s namespace), run
`infrahub-collect environment list` and disambiguate
with `--project=<name>` or `--k8s-namespace=<ns>`.
No Infrahub API token is needed — the tool reuses
existing Docker/kubectl access. See
[rules/deployment-detection.md](rules/deployment-detection.md).

### 4. Create the bundle

```bash
infrahub-collect create
```

Add flags that match the symptom from step 1 —
`--benchmark` for performance/OOM issues,
`--include-queries` for slow/failing DB operations,
`--include-backup` when support asks for a
reproducer. See
[rules/create-flags.md](rules/create-flags.md) for
the full symptom-to-flag mapping.

Partial bundles are expected on degraded
deployments — `create` still exits 0 and records any
collection failures in the manifest. Send the bundle
as-is; do not try to patch gaps by hand.

### 5. Review before sharing (user-gate)

`infrahub-collect` only masks well-known secret key
names (`password`/`secret`/`token`/`key` →
`********`). It does not scrub log or query
contents, or secrets stored under other key names.
Walk the user through scanning `bundle/logs/` and
`bundle/server/` for hostnames, IPs, customer data,
or secrets under non-standard keys, and get explicit
confirmation before sharing. See
[rules/review-before-sharing.md](rules/review-before-sharing.md).

### 6. Share / hand off

Once the user confirms the bundle is safe to share,
send it via the support channel (Discord, Slack,
email). If the user also wants to file a public
GitHub issue, hand off to `infrahub-reporting-issues`
— see
[rules/cross-link-reporting-issues.md](rules/cross-link-reporting-issues.md).
If the user wants a local first-pass analysis of the
bundle (tracebacks, failures, known-issue matching)
before or instead of the expert hand-off, continue
with `infrahub-analyzing-diagnostics` — this skill
only collects; the analyzer owns triage.

## Rule Categories

| Prefix | Category | Description |
| ------ | -------- | ----------- |
| workflow | Workflow | User-gate semantics, step ordering |
| install | Install | Verify/install the `infrahub-collect` binary |
| deployment | Detection | Defer to `environment detect`/`list` |
| create | Create flags | Symptom-to-flag mapping for `create` |
| collection | Collection | Read-only tool, no mutations |
| bundle | Bundle | On-disk `bundle/` layout (reference) |
| review | Review | Key-name masking gap; user review before sharing |
| cross-link | Cross-linking | Hand-off to `infrahub-reporting-issues` |

See [rules/_sections.md](rules/_sections.md) for the
full index.

## Supporting References

- [reference.md](reference.md) — full flag reference,
  bundle layout details, and environment-variable
  notes. **Read in steps 2-4.**
- [examples.md](examples.md) — end-to-end walk-throughs
  for common symptom classes.
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)

## Anti-patterns

- **Running anything that mutates state.** No
  `docker compose down`, no `kubectl delete`.
  `infrahub-collect` is read-only by design; don't
  add commands that aren't.
- **Hand-rolling collection instead of using the
  binary.** No manual `docker compose logs` / `kubectl
  logs` scripting — `infrahub-collect create` already
  covers every service, replica, and log rotation.
- **Skipping the review-before-sharing gate.** The
  tool's masking is key-name-based only; it cannot
  judge what is sensitive to this particular user.
  Only the user can approve sharing the bundle.
- **Claiming root cause.** This skill produces a
  bundle for an expert to triage, not a diagnosis.
  State what was collected; let the expert conclude.
- **Filing a GitHub issue from this skill.** That's
  `infrahub-reporting-issues`. Cross-link, don't
  duplicate.
