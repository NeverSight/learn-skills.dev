---
name: platform-engineering
description: >-
  Design, implement, or review runtime/platform concerns including deployment substrate, network,
  infrastructure as code, CI/CD infrastructure, secrets substrate, runtime configuration, and
  operational topology. Start from workload requirements and the project's existing platform.
  Never choose AWS/GCP/Azure/Kubernetes/Terraform/Pulumi or another provider merely because a
  specialist is installed.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Platform Engineering

Translate workload requirements into an operable platform without vendor-first reasoning.

## Workflow

1. Inspect the current runtime, deployment, network, CI/CD, secrets/config, stateful dependencies, and operating constraints.
2. Describe workload needs: execution model, state, connectivity, availability, scaling, security boundaries, deploy frequency, recovery expectations, and cost constraints.
3. Prefer the existing platform when it satisfies the requirement.
4. Choose deployment/IaC/config mechanisms only when a technology decision is actually required; provider availability is not evidence.
5. Separate application behavior from platform plumbing through the project's existing abstractions.
6. Treat runtime configuration, feature flags, and kill switches as operational controls with ownership, safe defaults, auditability, testing, and cleanup.
7. Define deployment/rollback evidence proportionally; route rollout/release closure to finish and recovery behavior to reliability-engineering.

## Stop

Stop when the workload-to-platform mapping, operational ownership, deployment/config behavior, and evidence are clear enough to implement or review safely.
## Reference Guide

Load only the references needed for the current task:

- [iac provider selection](references/iac-provider-selection.md)
- [runtime control](references/runtime-control.md)
- [workload topology](references/workload-topology.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [dependency selection](references/_shared/engineering/dependency-selection.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
