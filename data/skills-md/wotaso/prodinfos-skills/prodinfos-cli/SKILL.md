---
name: prodinfos-cli
description: Use Prodinfos CLI as the deterministic, bounded interface for analytics queries, exports, and SDK validation in coding-agent workflows.
license: MIT
homepage: https://github.com/wotaso/prodinfos-skills
metadata: {"author":"wotaso","version":"1.0.0","prodinfos-target":"@prodinfos/cli","prodinfos-supported-range":"^0.1.0","openclaw":{"emoji":"📈","homepage":"https://github.com/wotaso/prodinfos-skills","requires":{"bins":["prodinfos"]},"install":[{"id":"npm","kind":"node","package":"@prodinfos/cli","bins":["prodinfos"],"label":"Install Prodinfos CLI (npm)"}]}}
---

# Prodinfos CLI

## Use This Skill When

- querying product analytics for a Prodinfos project
- validating whether SDK instrumentation landed correctly
- answering onboarding, paywall, survey, retention, or export questions without raw SQL

## Supported Versions

- Skill pack: `1.0.0`
- Target package: `@prodinfos/cli`
- Supported range: `^0.1.0`
- If a future CLI major changes commands or flags in incompatible ways, split to a sibling skill such as `prodinfos-cli-v1`

See [Versioning Notes](references/versioning.md).

## Non-Goals

- Do not generate raw SQL.
- Do not request unbounded raw event dumps.
- Do not include debug data unless the user explicitly asks for it.

## Safety Rules

- Always scope by project: `--project <id>`.
- Always scope by time: `--last` or explicit `since/until`.
- Prefer high-level query endpoints over raw exports.
- Keep groupings and result sets bounded.
- Treat release-only data as the default.
- For generated docs or help text, use tenant developer voice (`your workspace`, `your project`) and avoid provider-centric wording such as `our SaaS`.

## Query Priorities

Prefer these command families first:

- `funnel`
- `conversion-after`
- `paths-after`
- `retention`
- `survey`
- `timeseries`
- `breakdown`
- `generic`

Only use `events export` when the user explicitly needs raw CSV.

## Data Fidelity Rules

- CLI and dashboard both query the API. There is no separate CLI-only analytics source.
- Sequence-sensitive and cohort-sensitive queries stay on raw events.
- Aggregate-backed reads are acceptable only when the API reports that plan shape.
- `runtimeEnv` is auto-attached by the SDK. Do not invent a separate mode field.

## One-Time Setup

Preferred:

```bash
npm i -g @prodinfos/cli
prodinfos setup --token <readonly_token>
```

Alternatives:

```bash
prodinfos login --readonly-token <readonly_token>
prodinfos login --clerk-jwt <clerk_jwt>
```

## Output Mode

- Prefer `--format json` for automation or agent reasoning.
- Use `--format text` for short human summaries.
- Use `timeseries --viz table` when exact values matter.
- Use `timeseries --viz chart` or `svg` when a trend scan is enough.

## Validation Loop

After SDK rollout or query changes, validate with a few stable reads:

```bash
prodinfos schema events --project <id> --limit 200
prodinfos goal-completion --project <id> --start onboarding:start --complete onboarding:complete --last 30d
prodinfos get onboarding-journey --project <id> --last 30d --format text
```

## Missing Capability Loop

If the requested fetch is impossible with the current CLI surface:

1. State that the capability is missing.
2. Do not pretend another command is equivalent if it is not.
3. Submit CLI feedback with a reproducible gap report.

```bash
PRODINFOS_CLI_ENABLE_WRITE_COMMANDS=true prodinfos feedback submit \
  --category feature \
  --message "Missing CLI functionality: <short capability>" \
  --context "Requested fetch: <what user asked>; attempted command: <command>" \
  --meta '{"expected":"<expected output>","actual":"CLI has no command or endpoint"}'
```

## References

- [Versioning Notes](references/versioning.md)
- [Dedicated Events Playbook](references/playbooks/dedicated-events.md)
- [Event Placement Playbook](references/playbooks/event-placement.md)
- [Paywall Journey Playbook](references/playbooks/paywall-journey.md)
- [Store Review Playbook](references/playbooks/store-review.md)
- [CLI Use Cases Playbook](references/playbooks/usecases.md)
