---
name: dd-android-sdk
description: Route Datadog Android SDK upgrades to the migration instructions for the project's current and target major versions.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,android-sdk,android,kotlin,gradle,rum,logs,trace,session-replay,migration
  globs: "**/build.gradle,**/build.gradle.kts,**/libs.versions.toml"
---

# Datadog Android SDK Upgrades

Version-specific migrations for Android applications using the Datadog SDK.

## Skills

| Task | Skill |
|------|-------|
| Upgrade from v2 to v3 | `dd-android-sdk/upgrade-v3` |

## Routing

**Upgrading from v2 to v3** (including non-null user IDs,
`RumResourceMethod`, `GlobalRum` changes, full custom upload URLs, or explicit
feature enablement):

**Immediately read** [upgrade-v3/SKILL.md](upgrade-v3/SKILL.md) and follow it;
do not perform the migration from memory or from this routing file alone.

For a source/target major-version pair not listed above, do not apply another
version's instructions. Explain that this skill does not yet contain that
migration route and consult the current official migration documentation before
proposing changes.
