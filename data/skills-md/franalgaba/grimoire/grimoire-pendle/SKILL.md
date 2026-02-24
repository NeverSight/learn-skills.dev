---
name: grimoire-pendle
description: Fetches Pendle Hosted SDK metadata using the Grimoire venue CLI. Use when you need supported chains, aggregators, markets, assets, or market token details.
---

# Grimoire Pendle Skill

Use this skill to inspect Pendle metadata and preflight Pendle routing configuration before running spells.

Preferred invocations:

- `grimoire venue pendle ...`
- `npx -y @grimoirelabs/cli venue pendle ...` (no-install)
- `bun run packages/cli/src/index.ts venue pendle ...` (repo-local)
- `grimoire-pendle ...` (direct binary from `@grimoirelabs/venues`)

Recommended preflight:

- `grimoire venue doctor --adapter pendle --chain 1 --rpc-url <rpc> --json`

## Commands

- `grimoire venue pendle info [--base-url <url>] [--format <auto|json|table>]`
- `grimoire venue pendle chains [--base-url <url>] [--format <auto|json|table>]`
- `grimoire venue pendle supported-aggregators --chain <id> [--base-url <url>] [--format <auto|json|table>]`
- `grimoire venue pendle markets [--chain <id>] [--active <true|false>] [--base-url <url>] [--format <auto|json|table>]`
- `grimoire venue pendle assets [--chain <id>] [--type <PT|YT|LP|SY>] [--base-url <url>] [--format <auto|json|table>]`
- `grimoire venue pendle market-tokens --chain <id> --market <address> [--base-url <url>] [--format <auto|json|table>]`

## Examples

```bash
grimoire venue pendle info --format table
grimoire venue pendle chains
grimoire venue pendle supported-aggregators --chain 1 --format json
grimoire venue pendle markets --chain 1 --active true --format table
grimoire venue pendle assets --chain 8453 --type PT --format table
grimoire venue pendle market-tokens --chain 8453 --market 0x... --format json
```

## Notes

- Default API base URL is `https://api-v2.pendle.finance/core`.
- Override base URL with `--base-url` or `PENDLE_API_BASE_URL`.
- Use `--format json` for automation and nested payloads.
- Pendle `swap` currently supports `mode: exact_in` only.
- Aggregators are disabled by default in adapter actions unless explicitly enabled.
- For Pendle token outputs (`assetOut`, `outputs`), use bare address literals (`0x...`) and not quoted strings (`\"0x...\"`).
- Quoted address-like token values trigger validator code `QUOTED_ADDRESS_LITERAL`.
- `max_slippage` is validated as integer bps in `[0, 10000]` and converted to decimal (`bps / 10000`) before API requests.
