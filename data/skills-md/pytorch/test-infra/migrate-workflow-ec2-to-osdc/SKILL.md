---
name: migrate-workflow-ec2-to-osdc
description: Step-by-step playbook for migrating a pytorch/pytorch .github/workflows/*.yml from EC2 to OSDC (ARC) runners — covers both dial-up and 100% opt-in patterns, with the inputs that must be plumbed through _linux-build.yml / _linux-test.yml. Use when migrating a workflow off EC2 onto on-site data center / EKS-hosted self-hosted runners (OSDC / ARC), enabling the ARC experiment, or wiring up `use-arc` / `runner_prefix` / `ci-docker-hash` / `python-version` / `compiler` / `cuda-version` inputs.
---

# Migrating a workflow from EC2 to OSDC

OSDC (= ARC = on-site data center, EKS-hosted self-hosted runners) replaces EC2 runners. Migration touches the workflow file *and* requires a few inputs to flow into the reusable `_linux-build.yml` / `_linux-test.yml` so the OSDC code paths (`build-osdc`, `test-osdc`) activate. EC2 paths (`build`, `test`) and OSDC paths gate on `inputs.use-arc` (`!inputs.use-arc` vs `inputs.use-arc`), so flipping that input swaps execution lanes.

This playbook is for workflows that **call the reusable `_linux-build.yml` / `_linux-test.yml`** (e.g. `test-b200.yml`, `pull.yml`, `trunk.yml`, `tsan.yml`, `operator_microbenchmark.yml`). Standalone OSDC workflows (raw ARC label + `container:` directive) follow a different pattern not covered here.

## Decide: dial-up vs. 100% opt-in

| Pattern | When to use | Example |
|---|---|---|
| **Dial-up** (preferred) | Existing workflow with broad coverage; you want to ramp OSDC adoption via labels like `pull.yml`/`trunk.yml`. | `test-b200.yml` (PR #181544) |
| **100% opt-in** | Workflow is meant to *always* run on OSDC (e.g. testing the single B200 we own on EKS). | `operator_microbenchmark.yml`, `attention_op_microbenchmark.yml` (B200 jobs) |

The two pieces — `runner_prefix` and `use-arc` — **must move together**. Hardcoding one but driving the other off the determinator is a bug.

## Migration steps (dial-up pattern)

Worked reference: PR #181544 / commit `f156b7ddfd1` ("Migrate smoke test on B200 to OSDC"). The diff was 10 lines.

### 1. Make sure `get-label-type` opts into the ARC experiment

In the `get-label-type` job that calls `_runner-determinator.yml`, add:

```yaml
check_experiments: arc,lf
```

Without this the determinator won't consider the ARC experiment and `use-arc` will always be `false`.

### 2. Plumb five inputs into the build job

On the call to `./.github/workflows/_linux-build.yml`:

```yaml
with:
  runner_prefix: "${{ needs.get-label-type.outputs.label-type }}"  # likely already present
  ...existing inputs...
  ci-docker-hash: ${{ needs.get-label-type.outputs.ci-docker-hash }}
  use-arc: ${{ needs.get-label-type.outputs.use-arc == 'true' }}
  python-version: "3.10"     # match the docker-image-name's python
  compiler: gcc11            # match the docker-image-name's compiler
  cuda-version: "13.0"       # match the docker-image-name's cuda (or "cpu" for CPU)
```

`ci-docker-hash` is the `git rev-parse HEAD:.ci/docker` hash that the determinator computes. `_linux-build.yml` appends it to the ghcr.io image tag (`ghcr.io/pytorch/<docker-image-name>-<hash>`); without it the OSDC build pulls the unhashed tag, which may not exist or may resolve to a stale image. The build job must have `needs: get-label-type` for this expression to resolve.

The last three (`python-version` / `compiler` / `cuda-version`) feed `setup-linux` so it can configure the OSDC container env. Read them off the existing `docker-image-name` (e.g. `pytorch-linux-jammy-cuda13.0-cudnn9-py3-gcc11` → py3.10 / gcc11 / cuda13.0).

### 3. Add `get-label-type` to the test job's `needs` and plumb the use-arc + setup-linux inputs

On the call to `./.github/workflows/_linux-test.yml`:

```yaml
needs:
  - <existing-build-job>
  - get-label-type           # add this
with:
  ...existing inputs...
  use-arc: ${{ needs.get-label-type.outputs.use-arc == 'true' }}
  python-version: "3.10"
  compiler: gcc11
  cuda-version: "13.0"
```

The test job needs a direct `needs: get-label-type` dependency to read its outputs (it can't rely on transitive `needs` through the build job). `ci-docker-hash` is **not** an input to `_linux-test.yml` — the test job picks the right image up via `needs.<build>.outputs.docker-image`.

### 4. Drop the OSDC-incompatible inputs

If the EC2 path used inputs that don't apply on OSDC (e.g. `aws-role-to-assume:` for ECR pulls), remove them. OSDC has its own AWS role wired into `setup-linux` (`arn:aws:iam::308535385114:role/arc`) and pulls images from `ghcr.io/pytorch`, not ECR.

In #181544 this meant deleting:
```yaml
aws-role-to-assume: arn:aws:iam::308535385114:role/gha_workflow_s3_and_ecr_read_only
```

### 5. Verify

- `gh workflow run` or push a PR with the relevant `ciflow/*` tag.
- Look for the `build-osdc` / `test-osdc` jobs running (they're separate jobs in `_linux-build.yml` / `_linux-test.yml`, gated on `inputs.use-arc`). When `use-arc` is `false`, the original `build` / `test` jobs run instead.

## Migration steps (100% opt-in pattern)

For a job that should always run on OSDC, hardcode `runner_prefix` and `use-arc` instead of pulling them from the determinator. The build job still needs `ci-docker-hash` from `get-label-type`, so keep `needs: get-label-type`:

```yaml
needs: get-label-type
with:
  runner_prefix: "mt-"
  ci-docker-hash: ${{ needs.get-label-type.outputs.ci-docker-hash }}
  use-arc: true
  python-version: "3.10"
  compiler: gcc11
  cuda-version: "13.0"
```

Both jobs (build *and* test) need the `use-arc` + `python-version` / `compiler` / `cuda-version` inputs; only the build job needs `ci-docker-hash`. The build job's `runner:` stays as the EC2 label (e.g. `linux.r7i.4xlarge`); `_linux-build.yml`'s `build-osdc` job translates that to the right ARC runner via `map_ec2_to_arc.py`.

Reference: `operator_microbenchmark.yml` jobs `opmicrobenchmark-build-b200` / `opmicrobenchmark-test-b200`.

## What the inputs do (mental model)

`_linux-build.yml` and `_linux-test.yml` each define **two jobs**:

- `build` / `test` — EC2 path. Runs directly on the runner host VM. Gated on `!inputs.use-arc`.
- `build-osdc` / `test-osdc` — OSDC path. Runs inside a `container:` from `ghcr.io/pytorch/${docker-image-name}${ci-docker-hash ? '-' + ci-docker-hash : ''}`. Gated on `inputs.use-arc`.

The OSDC jobs call `setup-linux` with `use-arc: true` and pass `python-version` / `compiler` / `cuda-version` so the container env matches the build environment. That's why the migration must pass these three inputs — `setup-linux` errors out without them on the OSDC path. `ci-docker-hash` is what pins the ghcr.io image tag to a specific `.ci/docker` tree state so the build doesn't drift onto an unhashed (or wrong) image.

## Common gotchas

- **Forgetting `check_experiments: arc,lf`** → `use-arc` is always `false`, so OSDC never activates and you'll think the migration silently failed.
- **Forgetting `needs: get-label-type` on the test job** → `${{ needs.get-label-type.outputs.use-arc }}` evaluates to empty, dial-up doesn't engage.
- **Forgetting `ci-docker-hash` on the build job** → OSDC pulls the unhashed ghcr.io tag (`<docker-image-name>` with no `-<hash>` suffix), which may not exist or may resolve to a stale image. The failure mode is a `manifest unknown` pull error in the OSDC container step.
- **Plumbing `ci-docker-hash` from `needs.get-label-type.outputs.*` without adding `needs: get-label-type`** → the expression resolves to empty, so it's a silent no-op equivalent to not setting it at all.
- **Mismatched `python-version` / `compiler` / `cuda-version` vs. `docker-image-name`** → container has one toolchain, `setup-linux` configures another, build fails confusingly.
- **Leaving `aws-role-to-assume:` for ECR** → harmless on OSDC (it's only used by EC2 path) but stale and misleading; remove it.
- **Mixing patterns** (dynamic `runner_prefix` + hardcoded `use-arc: true`, or vice versa). Pick one pattern and apply it consistently.
