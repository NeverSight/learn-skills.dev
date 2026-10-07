---
name: monomind-onboarding
description: "Complete or audit .monomind/workflow.md through a repository-owner or project-lead policy interview. Use when the profile is absent, contains UNRESOLVED values, needs explicit collaboration, integration, test, CI/CD, release, or continuity decisions, or fails a policy readiness gate. Do not use once the profile passes or to execute code tasks."
---

# Monomind Repository Onboarding

Resolve the repository policy needed for the requested boundary. Distinguish
verified facts, approved decisions, and unresolved questions.

## Scope discovery

1. Identify the task, repository, approver, active instructions, current profile,
   and boundary: Build, Integration, or Release. Read-only assessment needs no
   completed gate. Do not onboard unrelated repositories merely because the
   plugin is installed.
2. Reuse prior evidence and approvals. Inspect checked-in instructions,
   commands, CI, ownership, and continuity sources only as needed for missing
   fields at this boundary. Do not interview about deployment for a merge-only
   task. Read [references/policy-principles.md](references/policy-principles.md)
   only when a policy tradeoff needs its additional guidance.
3. If writing is requested, use this task's exclusive linked worktree from the
   approved base. Reuse an existing task worktree; never edit the protected base
   branch or another task's workspace. A profile change does not grant authority
   to publish, merge, install packages, or deploy.

## Establish or refresh the profile

When project-local workflow is installed, its bundled script preserves existing
instructions/profile:

```bash
python3 <workflow-skill-dir>/scripts/adopt.py apply --repo <repository>
```

For first adoption with an explicitly approved alternative base, pass
`--base <remote/branch>`; this records the base in the new profile. It cannot
override a different recorded base. If the profile already exists, preserve
approved values and add only required missing fields reported by the checker.
Informational template links do not become policy requirements.

Without the workflow skill, draft the relevant policy areas with unknowns
marked `UNRESOLVED`, and report that persistent adoption and machine-checked
readiness remain outstanding. Do not claim certification.

## Resolve missing decisions

Run the one requested gate to discover its unresolved fields:

```bash
python3 <workflow-skill-dir>/scripts/adopt.py check --gate <build|integration|release> --repo <repository>
```

This includes structural checks and lower-boundary requirements; do not run all
gates just to repeat them. Build covers implementation policy; Integration adds
review, CI, evidence, and merge policy; Release adds deployment and recovery.

Present verified facts with sources. Ask short grouped questions only for
remaining policy choices. The owner, project lead, or named delegate decides
policy and approves not-applicable decisions; a missing file is not proof that
a gate is optional. Existing session authorization remains valid. If no
authorized answer exists, retain `UNRESOLVED` and identify who must decide.

Write confirmed values using:

```text
<verified value> — evidence: <project-relative path or command>
<policy value> — approved by <role/name>, <date>; decision: <path or URL>
NOT_APPLICABLE — <approved specific reason>
UNRESOLVED — decision required from <role>
```

Keep secrets and personal data out. Point to existing authoritative documents;
do not copy large policies. The project's own context and handoff locations
take precedence over optional external context tools.

## Certify and finish

After relevant values change, rerun the requested gate once. Report its result,
remaining fields/decision owners, changed files, and next step. A failed gate
blocks that boundary, not unrelated read-only work. No response means no new
approval. Commit or publish only as authorized.

Policy schema v2 supports legacy unversioned profiles. Unknown versions require
a compatible workflow/plugin; do not silently rewrite approval records to make
a gate pass. The optional trusted SessionStart hook uses the same bundled
parser/schema, defaults to Build, and is silent in unadopted repositories.
A repository can select the reminder boundary or dismiss it using
`.monomind/onboarding.json`; see the workflow adoption reference when configuring
that optional hook. This affects reminders only, never readiness gates.
