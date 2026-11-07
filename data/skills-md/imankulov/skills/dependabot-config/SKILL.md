---
name: dependabot-config
description: |
  Audit, design, or update GitHub Dependabot configuration in `.github/dependabot.yml`.
  Use when reviewing whether Dependabot is configured correctly, reducing dependency
  PR noise, grouping updates, setting schedules or cooldowns, covering monorepos and
  package ecosystems, or documenting blocked upgrades. Also use when asked for
  Dependabot best practices or why Dependabot opens too many or too few PRs.
  Do NOT use for processing, testing, fixing, or merging an existing queue of
  Dependabot pull requests; use the dependabot-prs skill for that.
metadata:
  imankulov.skills-sh-group: Security
  imankulov.skills-sh-order: "20"
  imankulov.claude-display-name: Dependabot Configuration
  imankulov.claude-category: development
  imankulov.claude-keywords: "dependabot,dependencies,configuration,security,agent-skills"
---

# Dependabot Configuration

Audit the repository before proposing policy. A short configuration can be correct;
add settings only when they solve an observed problem or express a deliberate policy.

## Establish scope and policy

1. Read repository instructions, `.github/dependabot.yml`, manifests, lockfiles,
   workspace definitions, CI workflows, CODEOWNERS, and open Dependabot PRs.
2. Map every maintained package ecosystem and manifest location to a Dependabot
   `updates` entry. Account for monorepo roots, generated or vendored manifests, private
   registries, and the repository's default branch.
3. Report the current behavior and concrete gaps before editing.
4. Use Balanced as the default policy when the user has not selected one. State the
   proposed policy and its practical effects before editing. For an audit-only request,
   recommend changes without applying them. Preserve explicit repository policy and
   the user's choices; ask only when a material tradeoff remains unresolved.

### Policy profiles

These profiles choose update behavior, not whether to create an issue, worktree, or PR.
All profiles fix invalid or missing ecosystem coverage and preserve security updates.
When presenting a choice, explain the expected review effort and release delay using
the repository's actual queue and test boundaries:

| Profile | Update behavior | Choose it when |
| --- | --- | --- |
| Balanced (default) | Weekly runs at an explicit time and local timezone; grouped patch/minor version updates within each ecosystem; majors separate; a seven-day release cooldown where supported; ecosystem labels. Fewer routine PRs, with several dependencies reviewed and rolled back together. | You want less weekly review work and can wait a week before considering ordinary new releases. |
| Minimal (existing defaults) | Fix coverage while preserving existing schedules, grouping, cooldowns, and labels. For newly covered ecosystems, follow existing repository settings or GitHub defaults. Does not deliberately reduce PR volume. | You want the smallest configuration change or want to choose update policy separately. |
| Strict | Longer cooldowns, narrower allow rules, explicit ownership, and tighter version-PR limits, with values chosen for the repository. Less update traffic, but slower adoption and a greater chance of a blocked queue. | You have limited review capacity or dependencies that need substantial validation. |

Use "default" for Balanced, the skill's default. Minimal preserves repository settings
and GitHub defaults, which may change over time. Cooldowns delay version updates, not
security updates; verify the security implications of any Strict allow or ignore rules.
Adapt grouping to packages that can be tested and rolled back together, and retain
existing stronger release-age controls unless the user chooses otherwise.

## Audit rules

- Verify `version: 2`, ecosystem identifiers, manifest paths, YAML shape, and whether
  the package-manager version is supported. Retrieve the current GitHub options
  reference before relying on defaults or recently added keys.
- Treat a workspace lockfile as one update surface. Avoid overlapping `directory` or
  `directories` entries for the same ecosystem and target branch.
- Check that path-filtered CI runs for every file a Dependabot PR changes. A green PR is
  weak evidence when the relevant workflow was skipped.
- Check workflows for ordinary Actions secrets or write-token assumptions. Dependabot
  runs receive a read-only `GITHUB_TOKEN` by default and read from Dependabot secrets,
  not Actions secrets. Prefer hermetic PR checks; duplicate only genuinely required,
  least-privilege test credentials into Dependabot secrets.
- Compare the schedule with the team's review capacity. Set `day`, `time`, and
  `timezone` when predictability helps; stagger expensive ecosystems when appropriate.
- Use ecosystem `groups` for dependencies that can be tested and rolled back together.
  Group routine patch/minor updates by default in the balanced profile; keep majors and
  known migration-heavy packages separate.
- Prefer same-ecosystem groups. Use `multi-ecosystem-groups` only when components form
  one deployable unit and a single combined rollback is desirable.
- Inspect `open-pull-requests-limit` in light of grouping. The limit applies per update
  entry to version PRs, not security PRs; a low limit can hide later updates behind a
  blocked queue.
- Configure `cooldown` as a release-age control for version updates. It does not delay
  security updates. Confirm which cooldown keys the ecosystem supports before writing
  SemVer-specific values.
- Preserve default security-update behavior. `target-branch`, `ignore`, `allow`, and
  grouping can affect version and security updates differently; verify the current
  documentation for each selected option.
- Use CODEOWNERS or supported assignment settings when dependency PRs otherwise lack an
  accountable reviewer.
- Never enable `insecure-external-code-execution` merely to make an update succeed.
  Explain the credential-exposure tradeoff and require explicit approval.

## Grouping pattern

Use this shape only after adapting it to the discovered ecosystem and test boundaries:

```yaml
groups:
  routine-production:
    dependency-type: "production"
    update-types: ["minor", "patch"]
    patterns: ["*"]
  routine-development:
    dependency-type: "development"
    update-types: ["minor", "patch"]
    patterns: ["*"]
```

Group order matters: a dependency goes into the first matching group. Use
`exclude-patterns` for packages that need dedicated validation. `dependency-type` is
not supported by every ecosystem, so omit it rather than inventing unsupported syntax.

## Blocked upgrades

Add an `ignore` only after reproducing a concrete incompatibility and obtaining the
user's decision. Prefer the narrowest version range or update type that prevents the
known failure. Put a compact comment beside it containing:

- why the upgrade is blocked;
- the date or upstream issue/document that supports the decision;
- what must become true before removing the ignore.

Do not use an undocumented permanent ignore as backlog disposal. For a blocked security
update, present mitigation or replacement options and make the exception conspicuous.

## Deliverable

For an audit, report coverage, noise/control issues, security implications, CI gaps,
and a prioritized recommendation. For an edit, show the chosen policy, change only the
configuration and directly related documentation, validate YAML, run the repository's
metadata or lint checks, and explain how the next Dependabot run will differ.

## References

- [GitHub option notes](references/github-options.md) — load before editing advanced
  grouping, cooldown, ignore, or branch behavior
