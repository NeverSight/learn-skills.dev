---
name: dependency-intake-audit
description: Decide whether a package may enter the project, install it without letting its lifecycle scripts run unreviewed, and triage what the audit reports. Use when adding, upgrading, or replacing a dependency, when an audit or advisory bot reports findings, or when a lockfile diff needs review. Do not use for choosing between libraries on features alone.
---

# Dependency Intake Audit

An install runs someone else's code on this machine before any of it is imported,
and an advisory audit only knows about vulnerabilities that have already been
reported. Intake is therefore a judgment about the package and its publisher, not
a green check from a scanner.

## 1. Earn the dependency

A few lines, the standard library, or an already-installed package beats a new
name. When one is genuinely needed, judge it on ownership, maintenance activity,
release age, provenance, the size of its transitive graph, and whether the name is
a typosquat of a popular package (`cross-env` against `crossenv`). A package
published days ago, or newly transferred, is the shape of a supply-chain attack.

## 2. Find the installation boundary

Do not assume npm, and do not treat the nearest manifest as the install root. Use
the workspace root that owns the lockfile, or an independent nested project only
when it sits outside that workspace. There, corroborate the declared package
manager, the committed lockfile, and what CI actually runs. Stop and ask when they
disagree or when competing lockfiles exist at the same root; picking one silently
splits the dependency graph. Pin the manager version and use its own frozen or
immutable install command, never another manager's.

## 3. Gate lifecycle scripts before the first install

Never discover a package's install scripts by running an ordinary install with
unverified client defaults. Bootstrap with dependency scripts disabled or under a
documented default-deny policy, read the exact script source at the exact version,
approve only the packages that genuinely need to build, commit that policy at the
installation boundary, then verify with a clean frozen install. Blanket approval
is not a policy.

Manager defaults here change fast, so read the pinned client's own documentation
rather than trusting remembered flags; the settings to look for are npm's
`ignore-scripts` and `strict-allow-scripts`, pnpm's `approve-builds`, `allowBuilds`
and `strictDepBuilds`, and Yarn's `enableScripts` with per-package
`dependenciesMeta.<package>.built`.

## 4. Triage findings by reachability, not by count

| Severity | Reachable in a runtime, build, test, or deploy path | Verdict |
| --- | --- | --- |
| critical or high | yes | fix now: update, patch, or replace |
| critical or high | no, confirmed unused | does not block; backlog row with a removal condition |
| critical or high | fix unavailable | look for a workaround or replacement; otherwise record the exception with its removal condition |
| moderate | runtime | blocks the next dependency change; backlog row until then |
| moderate | dev-only | track in the backlog |
| low | any | batch with the next dependency update |

Ask whether the vulnerable function is actually called, whether the package is
runtime or dev-only, and whether the deployment context makes it exploitable at
all. A deferral without a written reason is an unrecorded decision.

## 5. Remediate by hand

Never run forced remediation (`npm audit fix --force` or its equivalent): it
crosses declared ranges and lands upgrades nobody read. Take one dependency per
change, read the changelog rather than the version number, review the lockfile
diff along with the manifest and any script-policy change, and run the tests.
Verify registry signatures and provenance where the manager supports it, and treat
their absence as a reason to look closer, not as proof of compromise.
