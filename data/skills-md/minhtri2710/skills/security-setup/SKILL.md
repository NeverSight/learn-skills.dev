---
name: security-setup
description: Design and, after explicit approval, implement a local-first security baseline with always-on secret detection, offline-capable dependency and static checks, machine-readable reports, explicit bypasses, and a separately gated optional CI mirror. Use when hardening a repository's local security workflow. Do not use for incident response, cloud security review, or deciding whether a dependency may enter the project.
license: MIT
effort: high
---

# Security Setup

A security baseline is useful only when its boundary is visible: inspect the
repository first, choose checks from evidence, run locally without fetching, and
report both findings and missing evidence. This skill designs that baseline and
can implement it only after the Human approves the planned file changes. It does
not install tools, create CI, touch credentials, commit, push, deploy, or make
other outward changes on its own.

The related `dependency-intake-audit` skill owns package acceptance, lifecycle
script controls, installation boundaries, and dependency-advisory triage. Do not
repeat that doctrine here; this skill only decides how an already evidenced
repository can be checked locally.

## Invocation and authorization boundary

- A normal invocation means **Phase 1: local baseline**. It does not authorize
  writes. First inspect and present the exact paths and commands to be added or
  changed; wait for explicit Human approval before writing them.
- `--ci` is a user-facing request to consider the optional Phase 2 mirror, not
  authorization to write a workflow. It is separately gated, follows a passing
  or explicitly accepted Phase 1, and requires a second explicit Human approval
  before any CI file is created or changed.
- Never infer permission from a shell prompt, `--force`, an existing token, or
  write access. Hook installation, overwriting an existing hook/configuration,
  database warming, credential changes, CI changes, commits, pushes, deploys,
  and other destructive or outward actions require an explicit Human gate.
- If the target repository, language, lockfile, tool, database, CI capability,
  or scanner result is not evidenced, record `Not-Assessed` and name the
  operator prerequisite. Do not invent availability, versions, coverage, or
  successful checks.

## Phase 1 — inspect before selecting

Read-only inspection comes before tool selection. Establish the repository root
and read the manifests, lockfiles, existing pre-commit configuration, security
documentation, CI workflows, and any existing scanner configuration. Check local
availability with `command -v` or the platform equivalent; do not install a
missing tool merely to make the inspection green. If public/private status or a
default branch is needed for a CI decision and the repository does not prove it,
mark it `Not-Assessed`.

Record:

- languages and dependency manifests/lockfiles actually present;
- existing hooks and whether a security hook can be merged without replacing
  unrelated hooks;
- locally available scanners and whether their offline data/rules are present;
- files that would be created, modified, or overwritten;
- operator prerequisites and evidence gaps.

Do not select a scanner because it appears in this skill. Select the smallest set
supported by the observed repository. Use
[references/tool-selection.md](references/tool-selection.md) for the matrix and
offline boundary.

## Phase 1 — local-first baseline

1. **Secrets are the floor.** Configure the selected secret scanner as an
   always-on check. Never path-restrict it: credentials can appear in Markdown,
   JSON, examples, Dockerfiles, or any other staged file. Redact scanner output
   and do not place secret values in terminal output or reports.
2. **Dependencies follow evidence.** Run a dependency scanner only when a
   matching manifest or lockfile is present and its local vulnerability data is
   available. A missing database is an operator prerequisite, not a clean scan.
3. **Static analysis follows language evidence.** Select local rules and
   language-native checks only for languages actually found. Keep rules in the
   repository when the chosen scanner needs them; do not fetch a hosted ruleset
   at hook time.
4. **Every check has a scope decision.** The local runner can use the staged
   file names to decide which checks apply. Secret detection remains always-on;
   lockfile and language checks may be path-triggered; repository-wide security
   paths and workflow/Dockerfile changes can force all applicable checks. The
   scope decision is not proof that the external scanner inspected staged blobs:
   document the actual command and scan target.
5. **Offline means no runtime fetch.** The runner never installs tools,
   warms a database, calls a hosted service, or changes a lockfile. Use scanner
   flags and local rules that make the configured commands offline-capable. A
   database that has not been warmed by an authorized operator is `Not-Assessed`.

The implementation plan may include a local hook, a runner copy, selected-tool
configuration, local rules, and a security summary. Read the source-grounded
shapes in [references/configuration-template.md](references/configuration-template.md)
only after the target repository's evidence has been collected. Do not overwrite
an existing `.pre-commit-config.yaml`, security configuration, or security
summary without explicit approval and a reviewable diff.

## Bypass and failure policy

The runner in `scripts/security_check.py` has one explicit interactive
bypass. `--force` never performs a Git operation and never means force-push: when
a blocking finding exists, it asks for the literal `YES` in an interactive
terminal. It never bypasses a missing required tool, malformed report, timeout,
or other prerequisite gap. The accepted override is recorded in both reports;
non-interactive input, EOF, or any other answer refuses the bypass.

A missing required tool or unusable tool report is not a pass. The runner records
it as `Not-Assessed` and exits non-zero unless the operator explicitly uses
`--allow-missing-tools` for a bounded first-run assessment. That option changes
only the exit decision for missing executables; it does not claim coverage and
the report remains partial. Tool failures, malformed reports, and timeouts are
not converted into missing-tool success.

Use the runner's default report paths unless the operator explicitly declares
other report paths:

```text
python3 scripts/security_check.py
python3 scripts/security_check.py --all
python3 scripts/security_check.py --staged-only
```

- Default mode uses staged-file scope when staged files exist; with no staged
  files it performs a full scan.
- `--all` forces every configured check and `--staged-only` requires staged
  files. They are mutually exclusive.
- `--config`, `--output`, and `--markdown` select the declared configuration and
  report outputs. The runner writes only those two report paths plus temporary
  files used while a check runs.
- Reports contain machine-readable summary, scope decisions, findings, tool
  errors, missing-evidence status, and bypass status. Raw scanner stdout/stderr
  is not copied into reports because it can contain sensitive material.
- Exit `0` means no blocking result under the selected explicit policy; it does
  not mean every category was assessed. Exit `1` means a configured finding
  meets `fail_on`; exit `2` means a required tool/prerequisite, configuration,
  staged-file precondition, or invocation failed. An explicit accepted
  `--force` is reported as `BYPASSED`, not as a clean assessment.

## Phase 2 — optional CI mirror

Do not create CI merely because this source describes a workflow. Only after the
Human explicitly requests the CI phase should the skill inspect the repository's
CI platform, default branch, permissions, selected local commands, and report
artifact policy. Keep the mirror separately gated and use the same local runner
with full-scan semantics. Do not add hosted scanners, credentials, SARIF upload,
network-dependent setup, or permissions that the repository has not explicitly
approved. If a prerequisite is unavailable, leave CI `Not-Assessed` and report
what an operator must decide.

## Verification and completion

Use [references/verification-scenarios.md](references/verification-scenarios.md)
for the bounded no-blind-spot walkthrough. Verify help and unknown-option
behavior before trusting a copied runner. Then report:

- the inspected evidence and selected checks;
- every created, modified, or deliberately omitted path;
- local report results, including `Not-Assessed` categories and missing tools;
- explicit bypasses and their reason/report location;
- CI status (`not requested`, `ready for separate approval`, `Not-Assessed`, or
  implemented only after its own Human gate);
- checks and exit codes, with unavailable operator prerequisites left visible.

No successful scan may be claimed for an unseen target repository. No install,
secret access, hook activation, CI write, commit, push, deploy, or other external
action is implied by this skill's description or by `--ci`.
