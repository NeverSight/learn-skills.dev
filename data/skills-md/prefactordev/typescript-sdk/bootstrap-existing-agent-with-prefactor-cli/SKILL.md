---
name: bootstrap-existing-agent-with-prefactor-cli
description: Use when an existing agent needs Prefactor resources created via the Prefactor CLI before SDK instrumentation is added.
---

# Bootstrap Existing Agent With Prefactor CLI

Set up Prefactor resources for an already-working agent before instrumentation code changes.

Core principle: provision first, instrument second.

## Coding Assistant Usage

Apply this skill first when the user asks to:

- "set up Prefactor for this existing agent"
- "create Prefactor environment/agent/instance"
- "use CLI to bootstrap Prefactor"
- "prepare IDs and env vars before instrumentation"

After this skill completes:

1. If provider is supported, continue with `skills/instrument-existing-agent-with-prefactor-sdk/SKILL.md`.
2. If provider is unsupported, continue with `skills/create-provider-package-with-core/SKILL.md`.
3. Return a copy/paste block with exported env vars and the selected package.

## Inputs You Need

- Prefactor API token (for CLI profile)
- Base URL (optional, defaults to Prefactor cloud)
- Account ID
- Target provider/framework (`langchain`, `ai`, `openclaw`, or custom)
- Human-readable names for environment and agent
- Working directory to store config (recommended: repo root)

## CLI Workflow

Before running CLI commands, choose package first, then install required Prefactor package(s).

- Use whichever package manager the project already uses (`bun`, `npm`, `pnpm`, or `yarn`).
- Install `@prefactor/cli` for bootstrap commands.

`prefactor` command requirement:

- The `prefactor` command comes from the npm package `@prefactor/cli`.
- If the command is not globally available, run it via the package manager launcher (`bunx @prefactor/cli`, `npx @prefactor/cli`, `pnpm dlx @prefactor/cli`, or `yarn dlx @prefactor/cli`).
- Use `prefactor help` or `prefactor <group> help` for command details.

Examples:

```bash
# bun
bun add @prefactor/cli

# npm
npm install @prefactor/cli

# pnpm
pnpm add @prefactor/cli

# yarn
yarn add @prefactor/cli
```

Run these in order:

```bash
prefactor profiles add default [base-url] --api-token <api-token>
prefactor accounts list
prefactor environments create --name <env-name> --account_id <account-id>
prefactor agents create --name <agent-name> --environment_id <environment-id>
prefactor agent_instances register \
  --agent_id <agent-id> \
  --agent_version_external_identifier <agent-version-id> \
  --agent_version_name <agent-version-name> \
  --agent_schema_version_external_identifier <schema-version-id> \
  --update_current_version
```

Profile notes:

- `<profile-name>` is any key like `default`, `staging`, or `prod`.
- Select profile with `--profile <name>`.
- When using launchers, prefix commands consistently (for example `npx @prefactor/cli profiles add ...`).

Config resolution notes:

- CLI config resolution order is:
  1. `./prefactor.json`
  2. `~/.prefactor/prefactor.json`
  3. if none exists, profile creation writes `./prefactor.json`
- Global CLI install does not make config global; command working directory still controls which config file is used.

Collect and persist these IDs from command output:

- `environment_id`
- `agent_id`
- `agent_instance_id`

## Package Selection

Choose package by provider:

- LangChain -> `@prefactor/langchain`
- AI SDK -> `@prefactor/ai`
- OpenClaw -> `@prefactor/openclaw`
- Custom/unsupported provider -> use `skills/create-provider-package-with-core/SKILL.md`

When handing off to SDK instrumentation, import helpers from that selected package directly, for example:

```ts
import { init, withSpan, shutdown } from '@prefactor/ai';
// or '@prefactor/langchain'
```

Do not mix adapter `init` with `withSpan`/`shutdown` from `@prefactor/core` unless an explicit tracer is passed.
This guidance targets adapter-style integrations (`@prefactor/ai`, `@prefactor/langchain`) and does not change `@prefactor/openclaw` plugin runtime behavior.

If you have identified and selected an existing package, use `skills/instrument-existing-agent-with-prefactor-sdk/SKILL.md`

## Runtime Environment Variables

Produce this output for the user after setup:

```bash
export PREFACTOR_API_URL="<api-url>"
export PREFACTOR_API_TOKEN="<api-token>"
export PREFACTOR_AGENT_ID="<agent-id>"
```

Use the created `agent_id` for `PREFACTOR_AGENT_ID`.

## Verification

- Confirm CLI commands succeeded without HTTP/auth errors.
- Confirm IDs were returned and captured.
- Confirm package selection matches provider.
- Confirm env vars match created resources.
- Confirm `prefactor.json` is ignored by git (`git check-ignore prefactor.json`, `git status --short`).

## Common Mistakes

- Instrumenting code before creating Prefactor resources.
- Using account ID where environment ID is required.
- Forgetting to propagate created `agent_id` to `PREFACTOR_AGENT_ID`.
- Picking `@prefactor/core` directly when a built-in adapter exists.
- Running commands from the wrong directory and reading/writing the wrong `prefactor.json`.
- Committing `prefactor.json` (contains API tokens).
