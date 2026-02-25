---
name: lemonsqueezy
description: Manage a Lemon Squeezy store from the command line. Use when the user needs to query or manage orders, subscriptions, customers, license keys, checkouts, discounts, webhooks, or any other Lemon Squeezy resource. Provides token-efficient output optimized for AI agents.
---

# Lemon Squeezy CLI

`lmsq` is a CLI for the [Lemon Squeezy API](https://docs.lemonsqueezy.com/api) with 62 operations across 22 resource types.

## When to use this skill

Use this when the user asks you to:
- Query or manage Lemon Squeezy resources (orders, subscriptions, customers, products, etc.)
- Check subscription statuses, order details, or license key states
- Create checkouts, discounts, or webhooks
- Activate, validate, or deactivate license keys
- Refund orders or subscription invoices
- Generate invoices

## Prerequisites

Install the CLI if not already available:

```bash
npm install -g lmsq
```

Or run without installing: `npx lmsq <command>`

## Authentication

Set the API key via environment variable (preferred for agents):

```bash
export LEMONSQUEEZY_API_KEY=lsq_live_xxxxxxxxxxxx
```

Or authenticate persistently:

```bash
lmsq auth login --key lsq_live_xxxxxxxxxxxx
```

Resolution order: `--api-key` flag > `LEMONSQUEEZY_API_KEY` env var > `~/.config/lemonsqueezy-cli/config.json`

**Exception:** `lmsq licenses activate/validate/deactivate` uses the public License API and requires no authentication.

## Output for agents

When called from a non-TTY shell (which is how agents call it), output is automatically token-efficient flat `key: value` text with no colors or decoration.

**Always minimize token usage by choosing the right output mode:**

| Mode | Use when | Tokens |
|------|----------|--------|
| `--pluck <field>` | You need a single value from a single resource | ~1 |
| `--count` | You need the total number of matching resources | ~3 |
| `--only-ids` | You need a list of IDs | ~5 per resource |
| `--fields a,b,c` | You need a few specific attributes | ~20 per resource |
| (default) | You need all attributes | ~150 per resource |
| `--json` | You need structured data for parsing | ~200 per resource |

**Do not use `--json-raw` unless the user specifically asks for the raw JSON:API response.** It costs ~2,000 tokens per resource.

## Command patterns

All resources follow consistent patterns:

```bash
lmsq <resource> list [--store-id <id>] [--filters] [-p <page>] [-s <size>]
lmsq <resource> get <id>
lmsq <resource> create [--required-options] [--optional-options]
lmsq <resource> update <id> [--options]
lmsq <resource> delete <id>
```

### Common flags on every command

| Flag | Effect |
|------|--------|
| `--json` | Flattened JSON output |
| `-f, --fields a,b` | Return only specific attributes |
| `--api-key <key>` | Override the stored API key |
| `--color` / `--no-color` | Force or disable color |

### List command flags

| Flag | Effect |
|------|--------|
| `-p, --page <n>` | Page number (default: 1) |
| `-s, --page-size <n>` | Results per page (default: 5, max: 100) |
| `--only-ids` | One ID per line |
| `--count` | Just the total count |
| `--first` | Return only the first result |

### Get command flags

| Flag | Effect |
|------|--------|
| `--pluck <field>` | Return just the bare value of one field |

## Examples

```bash
# Check how many active subscriptions exist
lmsq subscriptions list --status active --count

# Get a customer's email
lmsq customers get 456 --pluck email

# List recent orders with key fields
lmsq orders list --page-size 10 --fields status,total,user_email

# Get all active subscription IDs
lmsq subscriptions list --status active --only-ids --page-size 100

# Check a subscription's status
lmsq subscriptions get 789 --pluck status

# Create a checkout link
lmsq checkouts create --store-id 1 --variant-id 1

# Refund an order
lmsq orders refund 12345

# Pause a subscription
lmsq subscriptions update 789 --pause void

# Resume a paused subscription
lmsq subscriptions update 789 --unpause

# Activate a license key (no auth needed)
lmsq licenses activate --key XXXXX-XXXXX-XXXXX --instance-name "server-1"

# Validate a license key (no auth needed)
lmsq licenses validate --key XXXXX-XXXXX-XXXXX
```

## Available resources

See [references/COMMANDS.md](references/COMMANDS.md) for the full command reference with all resources, subcommands, and their options.

Quick overview:

| Resource | Actions |
|----------|---------|
| `auth` | login, logout, status |
| `user` | (show current user) |
| `stores` | list, get |
| `customers` | list, get, create, update, archive |
| `products` | list, get |
| `variants` | list, get |
| `prices` | list, get |
| `files` | list, get |
| `orders` | list, get, invoice, refund |
| `order-items` | list, get |
| `subscriptions` | list, get, update, cancel |
| `subscription-invoices` | list, get, generate, refund |
| `subscription-items` | list, get, update, usage |
| `usage-records` | list, get, create |
| `discounts` | list, get, create, delete |
| `discount-redemptions` | list, get |
| `license-keys` | list, get, update |
| `license-key-instances` | list, get |
| `checkouts` | list, get, create |
| `webhooks` | list, get, create, update, delete |
| `affiliates` | list, get |
| `licenses` | activate, validate, deactivate |

## Lemon Squeezy documentation

If you need to understand platform behavior beyond what the CLI covers:

- [Help docs](https://docs.lemonsqueezy.com/help) — how Lemon Squeezy works (billing, subscriptions, license keys, etc.)
- [API reference](https://docs.lemonsqueezy.com/api) — full API documentation with field descriptions and response schemas
- [Guides](https://docs.lemonsqueezy.com/guides) — tutorials and integration walkthroughs

## Tips

- Use `lmsq <command> --help` to see all options for any command.
- Most list commands support `--store-id` to filter by store.
- List commands support `--include <resources>` for related data (e.g. `--include customer,order-items`).
- For subscriptions: `--cancelled` (via update) cancels at end of billing period; `cancel` cancels immediately.
- Pause modes: `--pause void` (loses access) vs `--pause free` (keeps access).
- License key special values: `--activation-limit unlimited`, `--expires-at never`.
- Discount amount types: `--amount-type percent` (e.g. 20 = 20% off) vs `--amount-type fixed` (e.g. 500 = $5.00 off).
