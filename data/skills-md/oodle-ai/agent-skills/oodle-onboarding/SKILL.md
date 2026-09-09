---
name: oodle-onboarding
description: This skill should be used when the user asks to "set up oodle integration", "onboard to oodle", "integrate kubernetes with oodle", "connect AWS to oodle", "install oodle collector", or mentions setting up observability with Oodle. Discovers the environment, recommends matching integrations from available setup specs, and executes step-by-step installation. Not for querying existing metrics, logs, or traces (use /oodle-metrics-query, /oodle-logs, /oodle-traces instead).
version: 1.0.0
---

# Oodle Onboarding — Integration Setup

Integrate infrastructure with the Oodle observability platform using `oodle integrations` commands. Actively discover the environment to recommend integrations and adapt setup steps. The setup spec is a blueprint — it defines the approach and parameters, but execution adapts based on what the codebase and environment reveal.

## Prerequisites

Before starting any onboarding work, verify the Oodle CLI is installed and authenticated. Run these checks at the beginning of every session:

### Step 1: Check if the CLI is installed

```bash
oodle version
```

If the command is not found, install it:

```bash
brew install oodle-ai/oodle/oodle
```

If `brew` is not available, fall back to:

```bash
go install github.com/oodle-ai/oodle-cli/cmd/oodle@latest
```

### Step 2: Check if the CLI is authenticated

```bash
oodle auth status
```

If not authenticated or the status shows an error, run interactive login:

```bash
oodle auth login
```

This opens a browser for OAuth login. The user must complete the browser flow — prompt them to do so and wait for confirmation. After login succeeds, verify with `oodle auth status`.

**Note:** `oodle integrations list-setup-specs` and `oodle integrations get-setup-spec` do NOT require authentication. Use these to discover available integrations and fetch setup instructions even before auth is configured. All other integration commands require valid credentials — complete the auth steps above before proceeding past step 2 in the Command Execution Order.

## Command Execution Order

Follow this sequence for every integration onboarding request:

1. **Identify the integration type.** If the user named one (e.g., "kubernetes", "aws-cloudwatch"), use it. Otherwise, run environment discovery to detect present infrastructure and recommend matching integrations (see `references/environment-discovery.md`).
2. **Fetch available setup specs** — run `oodle integrations list-setup-specs -o json` (no auth required) to confirm the type exists and cross-reference against discovery results.
3. **Fetch integration records** — run `oodle integrations list -o json` to extract: (a) the `type` field (lowercase it for step 4), (b) `collectorDomain`/`logsCollectorDomain` for helm values, (c) instance ID from the domain pattern. Then run `oodle api-keys list -o json` to find an existing API key, or `oodle api-keys create --name <name> --scopes <scopes>` to create one if none exist. Requires authentication — if not configured, complete Prerequisites steps 1–2 first.
4. **Fetch the setup spec** — run `oodle integrations get-setup-spec <type-lowercase> -o json`. This is the **blueprint** for integration, not a rigid script. It defines the general approach, required tools, and parameters.
5. **Discover the environment in depth** — probe the codebase, running services, and existing configs. Use findings to resolve parameters and adapt the spec's steps (see `references/environment-discovery.md`).
6. **Collect remaining parameters** — after discovery, ask the user for anything that could not be auto-detected. Group questions together.
7. **Execute the setup** — work through the spec's steps, adapting each one based on discovery results. Confirm with the user before every non-read-only command. Review `references/gotchas.md` before executing.
8. **Validate the integration** — run `oodle integrations list -o json` and check the status.
9. **Verify data presence** on the Oodle side (see `references/post-install-validation.md`).

For failure scenarios, consult `references/failure-handling.md`.

## Quick Reference

| Task | Command | Auth required? |
|------|---------|----------------|
| Discover available setup specs | `oodle integrations list-setup-specs -o json` | No |
| Discover available setup specs (table) | `oodle integrations list-setup-specs` | No |
| Get setup spec | `oodle integrations get-setup-spec <type> -o json` | No |
| Get setup spec (YAML) | `oodle integrations get-setup-spec <type> -o yaml` | No |
| List configured integrations | `oodle integrations list -o json` | Yes |
| List configured integrations (table) | `oodle integrations list` | Yes |
| List API keys | `oodle api-keys list -o json` | Yes |
| Create API key | `oodle api-keys create --name <name> --scopes <scopes> -o json` | Yes |

Aliases: `oodle integration`, `oodle integ`

## Common Operations

### Discovering available integration types

```bash
# CORRECT — discover all types with setup specs (no auth required)
oodle integrations list-setup-specs -o json

# CORRECT — table output for display (no auth required)
oodle integrations list-setup-specs

# WRONG — guessing integration types without checking
oodle integrations get-setup-spec some-random-type -o json
```

### Listing configured integrations

```bash
# CORRECT — check which integrations are already configured (requires auth)
oodle integrations list -o json

# CORRECT — table output for display
oodle integrations list
```

### Fetching a setup spec

```bash
# CORRECT — fetch spec for a known type (no auth required)
oodle integrations get-setup-spec kubernetes -o json

# WRONG — hardcoding setup steps instead of fetching the spec
kubectl apply -f <hardcoded-collector-manifest>   # never hardcode a manifest source; fetch the spec instead
```

### Executing setup steps (adapting the blueprint)

The spec defines what needs to happen. Discover the current state before each step and adapt:

```bash
# CORRECT — check existing state, then adapt
kubectl get namespace oodle-system 2>/dev/null && echo "Already exists, skipping" || kubectl create namespace oodle-system

# CORRECT — existing release? upgrade instead of install
helm list -n oodle-system | grep oodle && helm upgrade ... || helm install ...

# CORRECT — show the command and ask for confirmation before running
echo "I will run: kubectl create namespace oodle-system"
# [wait for user confirmation]
kubectl create namespace oodle-system

# WRONG — blindly running spec commands without checking existing state
kubectl create namespace oodle-system  # fails if already exists

# WRONG — running destructive commands without confirmation
kubectl delete namespace oodle-system
```

### Validating the integration

```bash
# CORRECT — check integration status after setup
oodle integrations list -o json

# CORRECT — check pods are running (for Kubernetes integrations)
kubectl get pods -n oodle-system

# WRONG — assuming success without verification
echo "Integration complete!"
```

## Best Practices

### Always fetch the latest setup spec

Run `oodle integrations get-setup-spec <type> -o json` at the start of every onboarding session. Never cache or reuse a previously fetched spec — requirements and steps change as the platform evolves. Treat the spec as a blueprint: it defines what needs to happen and what parameters are required, but adapt the exact commands and values based on environment discovery.

### Resolve parameters by discovery first, ask second

Collect all required parameters before starting execution. Check these sources in order:
1. **Environment discovery** — probe actively: `kubectl config current-context` for cluster name, `helm list` for existing releases, process lists for running collectors, config files in the codebase for endpoints, env vars for API keys.
2. **The user's request** — the user may have specified values in the prompt.
3. **Ask the user** — only for what could not be auto-detected. Group remaining questions together.

### Confirm before creating or modifying resources

Show the command to be run and wait for user confirmation before executing any command that creates, modifies, or deletes resources. Read-only commands (list, get, describe) do not need confirmation. **Redact secrets in the displayed command** — show the redacted version for confirmation, then run the unredacted version internally. For commands that require secret values (e.g., `helm install --set apiKey=...`), prefer passing secrets via temp files, stdin, or environment variables rather than command-line arguments to avoid shell history exposure.

### Handle existing resources gracefully

If a resource already exists (namespace, Helm release, ConfigMap), skip the creation step and note it was already present. Do not fail or attempt to delete and recreate.

### Redact secrets in output

Never display full API keys, tokens, or passwords. Show only the first and last 4 characters (e.g., `oodl...k9x2`). When rendering config templates from the spec, redact secret values before showing to the user.

### One step at a time

Execute setup steps sequentially. Verify each step succeeded before moving to the next. If a step fails, diagnose the issue and suggest a fix — do not continue to the next step.

### Present a summary when done

After all steps complete and validation passes, present a summary:
- Integration type and name
- What was installed/configured
- Current status
- How to check status later (`oodle integrations list`)

## References

- `references/environment-discovery.md` — infrastructure detection and setup step adaptation
- `references/gotchas.md` — critical gotchas to review before executing setup
- `references/post-install-validation.md` — verifying data presence with query skills
- `references/failure-handling.md` — troubleshooting common failure scenarios
- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli) — source of the `oodle` binary
- [Oodle docs](https://docs.oodle.ai) — product documentation
- [oodle-cli skill](../oodle-cli/SKILL.md) — core CLI usage, auth, output formats
