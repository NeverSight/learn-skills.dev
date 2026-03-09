---
name: nansen-search
description: Search for tokens, wallets, or entities by name or address. Use when you have a token name and need the full address, or want to find an entity.
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash(nansen:*)
---

# Search

```bash
# Search for a token by name
nansen research search "jupiter" --type token

# Search for an entity / person
nansen research search "Vitalik" --type entity --limit 5

# Lookup by address
nansen research search "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

# Agent pattern — get token address from name
nansen research search "bonk" --type token --fields address,name,symbol,chain
```

## Tips

- Search is case-insensitive.
- Use `--type token` or `--type entity` to narrow results.
- After getting an address, use workflow skills like `nansen-token-analysis` or `nansen-wallet-analysis` for full analysis.
- For agent self-discovery: `nansen schema` returns the full JSON schema of every command and return field.

## Flags

| Flag | Purpose |
|------|---------|
| `--type` | Filter: `token` or `entity` |
| `--chain` | Filter by chain |
| `--limit` | Number of results (default 25, max 50) |
| `--fields` | Select specific fields |
| `--table` | Human-readable table output |
