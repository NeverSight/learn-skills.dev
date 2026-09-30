---
name: otel-upgrade
description: Assess OpenTelemetry package and Collector upgrades across ecosystems. Use when choosing or validating API, SDK, instrumentation, exporter, Collector distribution, component, image, chart, Operator, OCB build, or configuration versions, including compatibility, required changes, telemetry and runtime behavior, and rollout risk.
---

# OpenTelemetry Upgrade

Find the highest stable target supported by the available repository evidence and provide concise, case-specific upgrade advice. Unless the user asks for implementation, assess the upgrade without changing project files.

## Choose the workflow

| Request or repository evidence | Read |
|---|---|
| Package manifests, lockfiles, APIs, SDKs, instrumentation libraries, exporters, plugins, or dependency constraints | [Dependency upgrade](references/dependency-upgrade.md) |
| Collector binaries, images, charts, Operators, configuration, feature gates, components, OCB manifests, builds, or runtime behavior | [Collector upgrade](references/collector-upgrade.md) |
| A custom Collector involving independently versioned or third-party modules | Read the Collector workflow first, then the dependency workflow for relevant module constraints. |

Read only the applicable reference. Read both when the upgrade crosses both surfaces.

## Shared instructions

1. Inspect the repository and runtime evidence before choosing the workflow or assuming the ecosystem.
2. Establish the exact current and candidate versions. Record wrappers, distributions, artifacts, and embedded dependencies separately rather than treating one version as proof of another.
3. Query authoritative registries and tagged primary upstream sources for current stable releases. Record the lookup date. Treat release candidates, beta/alpha packages, nightly artifacts, and untagged source as prereleases unless that package line intentionally publishes with a prerelease identifier; do not silently replace a project's existing experimental package line with a stable package from a different line. If no stable release meets a stated requirement, assess prereleases separately and label them clearly.
4. Distinguish the **latest available** stable release from the **highest validated compatible** candidate. Do not call a candidate validated when the relevant checks could not run.
5. Preserve the user's working tree by validating in a temporary copy, worktree, or equivalent isolated environment. Start with the latest stable candidate. If it fails, diagnose the cause and test selected lower versions when useful; do not assume compatibility is monotonic.
6. Connect upstream changes to this repository's actual usage and available downstream contracts. Treat unavailable consumers, environments, and exact-version coverage as unverified.
7. Use applicable specialized skills only when they are available. Otherwise use primary upstream sources and repository evidence, and report any resulting verification gaps.

Dependency resolution, compilation, configuration acceptance, and passing tests establish different and limited kinds of evidence. State exactly what each result demonstrates.

## Report

Keep the report concise and tailored to the repository.

```markdown
## Recommendation

Recommend upgrading `<subject>` from `<current>` to `<target>`, remaining on `<current>`, or deferring the upgrade. Explain the evidence, effort, and risk.

## Relevant Findings

- `<Material finding>` — explain its effect on this repository and any required action.

## Proposed Upgrade Path

Give the smallest coordinated sequence of dependency, artifact, code, configuration, and rollout changes.

## Validation

State the exact candidates, artifacts, configurations, platforms, and checks covered, their results, and what those results demonstrate.

## Remaining Risk

Mention only material behavior, environments, integrations, consumers, or artifacts that could not be verified. Omit this section when no material unverified areas were identified.
```

Link material upstream claims to authoritative release notes, documentation, or source. If the latest available version is not the highest validated compatible version, name both and explain the blocker.
