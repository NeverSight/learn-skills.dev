---
name: domain-check
version: 1.0.0
description: Check domain availability via Vercel and buy/manage domains via Vercel CLI
---

# Domain Check & Buy (Vercel)

Check domain availability, pricing, and purchase — all via Vercel.

## Quick Reference

```bash
# Check availability + pricing for a name across TLDs
domain-check myproject

# Check specific TLDs
domain-check myproject com,io,dev,app,ai

# Buy a domain (interactive — needs pty:true)
npx vercel domains buy mydomain.com

# List your owned domains
npx vercel domains list

# Inspect a domain you own
npx vercel domains inspect mydomain.com

# Add domain to a Vercel project
npx vercel domains add mydomain.com my-project

# Transfer a domain into Vercel
npx vercel domains transfer-in mydomain.com
```

## How It Works

### Availability Check (`domain-check`)

Uses the Vercel Registrar API (`/v1/registrar/domains/{domain}/price`):
- `purchasePrice: null` → domain is **taken**
- `purchasePrice: <number>` → domain is **available** at that price

```
$ domain-check myproject
Checking: myproject
-----------------------------------------------------------
DOMAIN                    STATUS         BUY PRICE    RENEWAL
-----------------------------------------------------------
myproject.com             ❌ Taken       -            $11.25
myproject.io              ✅ Available   $46.00       $46.00
myproject.dev             ✅ Available   $13.00       $13.00
-----------------------------------------------------------
Prices from Vercel Registrar
```

### Buying (`npx vercel domains buy`)

Interactive command — requires `pty: true` when calling from exec.

```bash
# Example exec call
exec(command: "npx vercel domains buy myproject.dev", pty: true, timeout: 30)
```

The CLI will show price and ask for confirmation before charging.

### API Direct (for scripts)

```bash
VERCEL_TOKEN=$(jq -r '.token' ~/.local/share/com.vercel.cli/auth.json)
TEAM=$(jq -r '.currentTeam // empty' ~/.local/share/com.vercel.cli/config.json)
TEAM_PARAM="${TEAM:+?teamId=$TEAM}"

# Check price/availability
curl -s "https://api.vercel.com/v1/registrar/domains/example.com/price${TEAM_PARAM}" \
  -H "Authorization: Bearer $VERCEL_TOKEN"
# Returns: { "years": 1, "purchasePrice": 11.25, "renewalPrice": 11.25, "transferPrice": 11.25 }
# purchasePrice: null = taken, number = available

# Buy via API
curl -s -X POST "https://api.vercel.com/v1/registrar/domains${TEAM_PARAM}" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}'
```

## Vercel CLI Domain Commands

| Command | Description |
|---------|-------------|
| `npx vercel domains list` | Show all domains |
| `npx vercel domains inspect <domain>` | Domain info (owned domains only) |
| `npx vercel domains buy <domain>` | Purchase (interactive) |
| `npx vercel domains add <domain> <project>` | Add to Vercel project |
| `npx vercel domains move <domain> <dest>` | Transfer to another team |
| `npx vercel domains transfer-in <domain>` | Transfer in to Vercel |
| `npx vercel domains remove <domain>` | Remove from team |

## Typical TLD Pricing (Vercel)

| TLD | ~Price/yr |
|-----|-----------|
| .com | $11.25 |
| .dev | $13 |
| .app | $15 |
| .co | $27 |
| .io | $46 |
| .ai | $140 |
| .org | $9.99 |
| .net | $13.50 |
| .xyz | $13 |

## Auth

Requires Vercel CLI authentication (`npx vercel login`). Token is read from `~/.local/share/com.vercel.cli/auth.json`.

Team ID is auto-detected from Vercel CLI config, or set `VERCEL_TEAM_ID` env var to override. If neither is set, the personal account is used.

## Notes

- Vercel registrar API replaced the old v4 domains/price endpoint (sunsetted Nov 2025)
- `domains inspect` only works for domains you own — use the price API for availability
- `.ai` domains are expensive ($140/yr) across all registrars
- When buying via CLI, use `pty: true` for the interactive confirmation prompt
