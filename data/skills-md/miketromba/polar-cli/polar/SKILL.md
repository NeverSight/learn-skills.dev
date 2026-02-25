---
name: polar
description: Use the Polar CLI to manage products, subscriptions, customers, orders, checkouts, license keys, webhooks, and other resources on the Polar (polar.sh) platform. Use when the user asks to interact with Polar, manage SaaS billing, create checkouts, issue license keys, or query monetization data from the command line.
---

# Polar CLI

Unofficial CLI for [Polar](https://polar.sh) with full API parity. Optimized for both developers and AI agents.

## When to use

Use this CLI when you need to:

- Manage Polar resources (products, customers, subscriptions, orders, etc.)
- Create or inspect checkouts and checkout links
- Issue, validate, or manage license keys
- Ingest events or query usage-based billing meters
- Set up webhooks
- Script or automate Polar workflows from the terminal

## Install

```bash
npm install -g @miketromba/polar-cli
```

The CLI is also available via `npx @miketromba/polar-cli`, or install with yarn/pnpm/bun.

## Authentication

```bash
# Interactive login (token is stored locally)
polar auth login --token <access-token>

# Or set the environment variable (preferred for CI/scripts/agents)
export POLAR_ACCESS_TOKEN=polar_at_xxx
```

Get an access token at https://polar.sh/settings.

Check auth status:

```bash
polar auth status
```

## Command grammar

All commands follow this pattern:

```
polar <resource> <action> [id] [--flags]
```

Examples:

```bash
polar products list
polar customers get <id>
polar subscriptions create --customer-id <id> --product-id <id>
polar checkouts create --products <product-id>
polar webhooks delete <id> --yes
```

Run `polar --help` for all resources. Run `polar <resource> --help` for actions and examples.

## Output formats

The CLI auto-detects the environment:

| Context | Default format | Description |
|---------|---------------|-------------|
| TTY (interactive) | `table` | Human-readable columns with color |
| Piped / non-TTY | `compact` | `key=value` one-liners, minimal tokens |

Override with `-o <format>`:

| Format | Flag | Use case |
|--------|------|----------|
| compact | `-o compact` | AI agents, scripting |
| json | `-o json` | Programmatic consumption |
| jsonl | `-o jsonl` | Streaming, `jq` pipelines |
| csv | `-o csv` | Export, spreadsheets |
| tsv | `-o tsv` | Unix tools (`cut`, `awk`) |
| id | `-o id` | Pipe IDs to other commands |
| count | `-o count` | "How many?" queries |
| table | `-o table` | Human-readable |

### Parsing compact output

Compact format is optimized for AI agents:

```
products 1-5/42 page=1
  [1] id=prod_123 name="Pro Plan" isRecurring=true prices=1
  [2] id=prod_456 name="Starter" isRecurring=true prices=1
next: polar products list --page 2 --limit 5
```

### Field selection

```bash
polar customers list --fields id,email,name
polar products get <id> --detail    # Full detail view
```

## Common workflows

### List and filter resources

```bash
polar products list
polar products list --query "Pro" --limit 5
polar customers list --email user@example.com
polar subscriptions list --active --product-id <id>
polar orders list --customer-id <id> --output json
```

### Create resources

```bash
polar customers create --email user@example.com --name "Jane Doe"
polar products create --name "Pro Plan" --prices '[{"amount":2999,"currency":"usd","recurringInterval":"month"}]'
polar checkouts create --products <product-id> --customer-email user@example.com
polar discounts create --name "20% Off" --type percentage --amount 20 --duration once
polar webhooks create --url https://example.com/hook --events order.created,subscription.created
```

### Update and delete

```bash
polar products update <id> --name "Enterprise Plan"
polar customers update <id> --name "Jane Smith"
polar customers delete <id> --yes    # --yes required for destructive actions
```

### License keys

```bash
polar license-keys list
polar license-keys validate --key XXXX-XXXX --organization-id <org-id>
polar license-keys activate --key XXXX-XXXX --organization-id <org-id> --label "Prod Server"
```

### Usage-based billing

```bash
polar meters list
polar events ingest --events '[{"name":"api_call","externalCustomerId":"user_123"}]'
polar metrics get --start-date 2025-01-01 --end-date 2025-01-31 --interval month
```

### Pagination

```bash
polar products list --limit 50 --page 2
polar products list --first 3         # Shorthand: --limit 3 --page 1
polar products list --all             # Fetch all pages
```

### Pipe patterns

```bash
# Get all product IDs
polar products list -o id

# Count active subscriptions
polar subscriptions list --active -o count

# Export customers as JSON
polar customers list --all -o json > customers.json

# Pipe to jq
polar orders list -o jsonl | jq '.totalAmount'
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `POLAR_ACCESS_TOKEN` | Access token (overrides stored credential) |
| `POLAR_ORGANIZATION_ID` | Default organization ID |
| `POLAR_SERVER` | `production` or `sandbox` |
| `POLAR_OUTPUT` | Default output format |

## Key global flags

| Flag | Short | Description |
|------|-------|-------------|
| `--output <format>` | `-o` | Output format |
| `--fields <list>` | `-f` | Comma-separated field selection |
| `--detail` | `-d` | Full detail view |
| `--org <id>` | | Organization ID override |
| `--yes` | `-y` | Skip confirmation prompts |
| `--quiet` | `-q` | Data only, no hints or headers |
| `--server <name>` | `-s` | `production` or `sandbox` |

## Resources

For the full list of resources and their operations, see [reference.md](reference.md).

## Official Polar documentation

For deeper understanding of Polar platform concepts, API behaviors, scopes, webhook events, or feature guides, fetch the official docs index:

```
https://polar.sh/docs/llms.txt
```

This is a machine-readable index of all Polar documentation. Use it when you need to:

- Understand how a Polar feature works (e.g., usage-based billing, seat-based pricing, trials)
- Check required API scopes for an operation
- Look up webhook event payloads and lifecycle
- Find guides for specific workflows (e.g., checkout sessions, license key validation)
- Verify API behavior or constraints that the CLI wraps

Fetch the index, find the relevant doc URL, then fetch that page for full details.
