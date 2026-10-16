---
name: ship
description: Learn how to ship a change through merge, CI, release, stage deployment, rollout, verification, rollback and flags.
plain: "Ship by evidence: merge, deploy a candidate, verify it, and roll back to a recorded version when needed."
diagram: |-
  merge
    │ CI
    ▼
  release + deploy stage
    │ canary, checks
    ▼
  promote + readback
    ├ WAIT: missing evidence
    ├ HOLD: needs a decision
    └ rollback: old version
---

# Ship a change

Read `AGENTS.md` first. Use [the project mapping](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/project.md) for commands, approval boundaries, owners and evidence.

## Terms used here

- **Candidate:** the exact commit and deployment version being considered for release.
- **Stage:** a named deployment environment, such as production.
- **Canary:** an isolated deployment used to check a candidate before wider release. The project mapping determines its allowed test traffic.
- **Promotion:** making a checked candidate active.
- **Qualification:** passing the named checks required for that exact version or behavior.
- **Readback:** reading deployed state from the provider to confirm the active version.
- **Adapter:** the implementation that connects the release procedure to a deployment provider.
- **Rollback:** making a recorded earlier version active without rebuilding it. It does not undo stored data or database changes.
- **Flag:** an approved switch that controls whether a behavior is enabled.
- **CI:** continuous integration, the automated checks run for a commit.
- **CLI:** command-line interface, a program called through terminal commands.
- **Effect:** the library for describing work with typed failures and required services.
- **Service:** a named interface for one job.
- **WAIT:** a procedure stop until its named condition has evidence. It is not a running scheduler.
- **HOLD:** a stopped release awaiting a decision. It does not declare a failed check or trigger rollback.

## 1. Read current deployment availability

<!-- deploy-confidence:start -->

Continuous deployment is off.

- Automatic production deploy: off.
- Automatic stage deploy: off.
- Automatic rollback after promotion: off.
- Automatic rollback before promotion: off.
- Provisioned canary stage: off.
- Gradual rollout: off.
- Deploy runner: local (checked with local test fixtures only; not proven in production).

Off means unavailable for operational use, even if code or fixture tests exist.
<!-- deploy-confidence:end -->

## 2. Prepare and merge

Ship one small release per pull request (PR). Keep new behavior behind its approved flag until its required checks pass.

Record the exact candidate commit and deployment version, base version, observed code and infrastructure changes, and release owner. Record the version to restore if the release fails. Use fast commit checks locally. CI runs the full suite against that candidate.

Follow the project's rules for who may merge, branch protection, and the order of dependent pull requests. Do not bypass hooks or put approval policy in merge tooling.

### Merging

When the project uses label-free Kodiak, a ready PR merges itself once required CI passes. Kodiak is the service that merges eligible pull requests. Open a PR only when it is meant to merge; add `NO MERGE` to hold it. Kodiak skips drafts and squash-merges eligible PRs. The lane fixes merge conflicts. Read the project mapping for the order of dependent pull requests and blocking labels.

WAIT[candidate-ci]: stop until the merged commit passes CI and has the required stage checks. A PR proof does not cover a different merged commit.

Read [CI and stage qualification](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/ci-stage.md) and [flags](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/flags.md).

## 3. Release and deploy

Read [runner selection](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/deploy-runner.md) and [deploy keys](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/deploy-key.md). Code, configuration and authorization are separate facts.

Use only deployment features marked on. When automation is off, the authorized owner follows the project's manual path.

Prepare and verify releases concurrently. Changes to the same deployment stage must run one at a time. WAIT[stage-queue]: stop until the authorized release has its turn for that stage. The latest eligible candidate replaces older queued candidates; record that outcome.

Name the exact commit you ship, and respect the stage's quiet windows. Put these guards in the deploy driver, never in a shell wrapper around it.

No release queue or scheduler is implemented here. The authorized owner must enforce the sequence through the project's manual procedure.

Check each release's exact version. Do not wait for another release's post-deploy check. Require an observed plan and read the deployed version back from the provider. Stored data must remain readable by both the candidate and the version that may be restored.

## 4. Roll out and verify

Read [gradual rollout](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/gradual-rollout.md), [canary](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/canary.md) and [post-deploy checks](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/post-deploy-checks.md).

Report code-ready, deployed and behavior-verified separately. Check customer-facing outcomes signed out, as the recipient would.

## 5. Restore or stop

Read [rollback](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/rollback.md) before restoration.

| Stop | Condition needed to continue |
| --- | --- |
| WAIT[release-scope] | Authorization and the target stage are known. |
| WAIT[adapter-qualification] | The required behavior checks have passed for the adapter. |
| WAIT[rollback-target] | The version to restore is recorded and usable. |

Missing evidence stops deployment. An observed failed check follows the project's failure policy. HOLD waits for a decision; it does not trigger rollback.

The release machine tracks deployment states and transitions. Follow its policy for observed failures. Do not expand the approved scope to credentials, infrastructure, data formats, provider writes, or messages to real recipients.

Follow the project's destroy refusal. Rollback makes the previous known-good version active immediately, without rebuilding it or waiting for a fixed observation period. Read the active version back from the provider to verify it. It restores code only.

## 6. Keep one release procedure current

Keep this skill aligned with the available deployment features in the same change. The current implementation has no generated list of recorded releases or generated deployment-availability block.

Read [catalog maintenance](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/catalog-maintenance.md) before changing deployment availability.

Keep this procedure and its references generic. Keep project facts behind [the project mapping](https://github.com/joelhooks/rat-stack/blob/main/skills/ship/references/project.md). Keep executable logic in the owning Effect packages and CLIs.

Skill scripts are thin launchers only. Use the project's maintenance skill to keep dependencies and enforced checks current.

The current implementation has no shared record of blocked release steps. WAIT labels above name manual procedure stops. The scheduler remains unimplemented. Missing evidence stops deployment.
