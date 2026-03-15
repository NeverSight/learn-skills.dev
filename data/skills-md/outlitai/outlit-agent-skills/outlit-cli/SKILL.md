---
name: outlit-cli
description: Use when running Outlit CLI commands, setting up Outlit for AI agents, authenticating with Outlit, querying customer data from the terminal, or troubleshooting Outlit CLI issues. Triggers on outlit auth, outlit setup, outlit customers, outlit sql, or any @outlit/cli usage.
---

# Outlit CLI

Customer intelligence from the terminal. Install: `npm i -g @outlit/cli`

All commands support `--help` for full option details.

## Command Reference

| Command | Purpose |
|---------|---------|
| `outlit auth login` | Store API key (interactive or `--key` for CI) |
| `outlit auth logout` | Remove stored key |
| `outlit auth status` | Validate current key |
| `outlit auth whoami` | Print masked key (for scripting) |
| `outlit auth signup` | Open signup in browser |
| `outlit customers list` | List/filter customers with risk signals |
| `outlit customers get <id\|domain>` | Customer details with optional `--include users,revenue,recentTimeline,behaviorMetrics` |
| `outlit customers timeline <id\|domain>` | Activity timeline with channel/event filters |
| `outlit users list` | List/filter users across customers |
| `outlit facts <customer>` | Signals and insights for a customer |
| `outlit search '<query>'` | Natural language search across customer context |
| `outlit sql '<query>'` | SQL against analytics DB (or `--query-file`) |
| `outlit schema [table]` | Describe analytics tables and columns |
| `outlit setup` | Auto-detect and configure AI agents |
| `outlit setup <agent>` | Configure specific agent: `cursor`, `claude-code`, `claude-desktop`, `vscode`, `gemini`, `openclaw` |
| `outlit doctor` | Diagnose CLI version, auth, connectivity, agents |
| `outlit completions <shell>` | Generate shell completions (bash/zsh/fish) |

## Authentication

API key format: `ok_` + 32+ alphanumeric characters.

**Credential priority** (first match wins):
1. `--api-key` flag
2. `OUTLIT_API_KEY` env var
3. `~/.config/outlit/credentials.json` (written by `outlit auth login`)

**Quick auth for CI/scripts:**
```bash
outlit auth login --key ok_your_key_here
# or
export OUTLIT_API_KEY=ok_your_key_here
```

## Output Behavior

- **Interactive terminal:** Pretty tables with colors
- **Piped stdout:** Automatic JSON (no flag needed)
- **`--json` flag:** Force JSON in any context

This means `outlit customers list | jq '.items[].domain'` just works.

## SQL Tables

Available in `outlit sql` and `outlit schema`:

| Table | Contains |
|-------|----------|
| `events` | All tracked events |
| `customer_dimensions` | Customer attributes and metrics |
| `user_dimensions` | User attributes and journey stages |
| `mrr_snapshots` | Revenue over time |

Always run `outlit schema` first to discover columns before writing SQL.

## Common Filters

Most list commands share these filters (check `--help` for specifics):

- `--billing-status PAYING|TRIALING|CHURNED|NONE`
- `--no-activity-in 7d|14d|30d|90d` / `--has-activity-in`
- `--mrr-above <cents>` / `--mrr-below <cents>`
- `--search <term>`
- `--limit <1-100>` / `--cursor <token>` for pagination
- `--order-by <field>` / `--order-direction asc|desc`

## Common Patterns

**At-risk paying customers:**
```bash
outlit customers list --billing-status PAYING --no-activity-in 30d
```

**High-value customer details:**
```bash
outlit customers get acme.com --include users,revenue,behaviorMetrics
```

**Search for churn signals:**
```bash
outlit search 'complaints about pricing' --customer acme.com
```

**Revenue query:**
```bash
outlit sql 'SELECT customer_id, mrr_cents FROM mrr_snapshots ORDER BY mrr_cents DESC LIMIT 10'
```

**Setup all detected agents at once:**
```bash
outlit setup --yes
```
