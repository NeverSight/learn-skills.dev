---
name: dependency-audit
description: "Reviews third-party dependencies for known vulnerabilities, abandonment, license conflicts, and supply-chain risk, and returns risk-ranked findings with upgrade, removal, or mitigation advice. Use when dependencies change, before a release, or during a repository audit. Not for code style review or for upgrading packages."
---

# Dependency Audit

## Purpose
Show which dependencies put the project at risk, how much, and what to do about each, without changing anything.

## When to use
- Use when: dependencies are being added or updated, a release is near, or a repository is being audited.
- Do not use when: the question is about the project's own code (use `security-audit` or a code review skill).

## Inputs
- Required: the dependency manifests and lockfiles.
- Optional: the runtime and its version, vulnerability reports already produced, license policy, and how each dependency is used.
- Assumptions: if vulnerability data needs a network source that is unavailable, state that the vulnerability check is incomplete; do not fill it from memory.

## Process
1. Inventory direct dependencies and the transitive ones that matter, with the versions locked.
2. Check each for known vulnerabilities, deprecation, abandonment, and large version gaps, using supplied reports or data you can reach.
3. Check licenses against the stated policy, and flag unusual sources, install scripts, and unpinned versions.
4. Rate each finding by severity and by reachability: whether the project uses the vulnerable path.
5. Recommend an upgrade, removal, replacement, or mitigation, and note the compatibility risk of each.
6. Separate what is urgent from routine maintenance.

## Rules and heuristics
- Required: state critical findings first and explicitly.
- Required: never claim a package is vulnerable, maintained, or safe without a source you can name. Say "not checked" where that is the truth.
- Required: do not run upgrades or edit manifests unless asked.
- Recommended: an upgrade recommendation names the breaking-change risk and the checks to run after.

## Checks
- Every finding names its source and version.
- Coverage is stated: what was checked and what was not.
- Urgent items are separated from routine ones.

## Output
Return: risk-ranked findings, recommended actions with compatibility notes, a coverage statement, and follow-up verification.

## Completion criteria
- Each finding can be verified from the source it cites.
- The report says what it did not check.
