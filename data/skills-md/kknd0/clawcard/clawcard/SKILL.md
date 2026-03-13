---
name: clawcard
description: Manage Privacy.com virtual cards — create, list, freeze, unfreeze, close cards and check login status. Use this skill when the user asks about virtual cards, payment cards, or ClawCard operations.
license: MIT
---

# ClawCard CLI Assistant

You are helping the user manage their Privacy.com virtual cards via ClawCard.

## Prerequisites

Install ClawCard first:

```bash
npm install -g clawcard
```

Then authenticate:

```bash
clawcard login
```

## Available Commands

| Command | Usage |
|---------|-------|
| `clawcard burner <amount> -m <merchant>` | Create a single-use burner card |
| `clawcard create -n <name> -l <limit> [-c <category>]` | Create a reusable card |
| `clawcard use <id>` | Unfreeze a card |
| `clawcard done <id>` | Freeze a card after payment |
| `clawcard done <id> --fail` | Freeze + cancel spending limit |
| `clawcard list [--state active\|frozen\|closed] [--month YYYY-MM]` | List cards |
| `clawcard show <id>` | Show card details |
| `clawcard update <id> [--name N] [--limit L] [--category C]` | Update a card |
| `clawcard close <id>` | Permanently close a card |
| `clawcard categories` | List merchant categories |
| `clawcard transactions [--card ID] [--since 7d] [--limit 20] [--status approved] [--merchant name]` | Show transaction history |

## Instructions

Based on the user's request, execute the appropriate ClawCard command(s) using the Bash tool. Key rules:

1. **Always check login status first** — if not logged in, tell the user to run `clawcard login`
2. **Burner amounts round up** — $25.01 becomes $26
3. **Card IDs are UUIDs** — copy them exactly from `clawcard list` output
4. **`close` is permanent** — confirm with the user before closing
5. **Categories support prefix match** — `din` matches `dining`, `ent` matches `entertainment`
6. **spendLimit is in dollars** — no conversion needed
7. All output must be in **English**

If the user asks to see their cards, run `clawcard list`.
If the user asks about transactions or spending history, run `clawcard transactions`.
