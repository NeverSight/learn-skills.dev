---
name: dotld
description: >
  Search domain name availability and registration prices. Use when the user
  mentions domains, TLDs, domain registration, domain availability, or wants
  to find, check, or brainstorm domain names. Runs the dotld CLI to query
  the Dynadot API for real-time pricing and availability.
version: 1.0.8
license: MIT
allowed-tools: Bash(dotld*)
metadata:
  tags: [domains, dns, dynadot]
  openclaw:
    requires:
      bins: [dotld]
      env: [DYNADOT_API_PRODUCTION_KEY]
    primaryEnv: DYNADOT_API_PRODUCTION_KEY
---

# dotld — Domain Availability & Pricing

## Installation

If `dotld` is not already available on the machine, install it:

```bash
curl -fsSL https://raw.githubusercontent.com/tedstonne/dotld/main/scripts/install.sh | bash
```

## Prerequisites

dotld requires a Dynadot production API key. The key is resolved in this order:

1. `--dynadot-key <key>` flag (also auto-saves to config for future runs)
2. `DYNADOT_API_PRODUCTION_KEY` environment variable
3. Saved config at `~/.config/dotld/config.json`

Get a key at: https://www.dynadot.com/account/domain/setting/api.html

If the key is missing, dotld exits with an error and a link to the key page.

## Modes of Operation

### Exact domain lookup

When the input contains a dot, dotld checks that specific domain:

```bash
dotld example.com
```

Output:

```
example.com · Taken
```

Or if available:

```
example.com · $9.99 · https://www.dynadot.com/domain/search?domain=example.com&rscreg=github
```

### Keyword expansion

When the input has no dot, dotld auto-expands across 9 popular TLDs — com, net, org, io, ai, co, app, dev, sh:

```bash
dotld acme
```

Output:

```
acme
├─ acme.com · Taken
├─ acme.net · Taken
├─ acme.org · Taken
├─ acme.io  · $39.99 · https://www.dynadot.com/domain/search?domain=acme.io&rscreg=github
├─ acme.ai  · Taken
├─ acme.co  · Taken
├─ acme.app · Taken
├─ acme.dev · Taken
└─ acme.sh  · Taken
```

### Multiple domains at once

Pass multiple arguments or use `--file`:

```bash
dotld acme.com startup.io mybrand

dotld --file domains.txt
```

## Output Interpretation

- `domain · Taken` — registered, not available
- `domain · $39.99 · https://...` — available with registration price and buy link
- Prices are in USD

## Flags

| Flag | Description |
|------|-------------|
| `--json` | Output structured JSON instead of the tree table |
| `--file <path>` | Read domains from a file (one per line) |
| `--dynadot-key <key>` | Provide API key (auto-saved to config) |
| `--timeout <duration>` | Request timeout, e.g. `5s`, `500ms` (default: `10s`) |
| `--currency USD` | Currency for prices (only USD supported in v1) |

## Workflow Guidance

**User has a specific domain** → run exact lookup:

```bash
dotld coolstartup.com
```

**User has a brand name or keyword** → run keyword expansion:

```bash
dotld coolstartup
```

**User wants to brainstorm** → suggest name variations, then batch-check them:

```bash
dotld coolstartup launchpad rocketship
```

**Present results as a ranked list**: show available domains sorted by price, include buy links. Suggest next steps — open a buy link, check more TLDs, try name variations.

**Batch from file** → when the user has a list:

```bash
dotld --file domains.txt
```

**Structured output** → when parsing results programmatically:

```bash
dotld acme --json
```

## Examples

### Check if a domain is taken

```bash
$ dotld example.com
example.com · Taken
```

### Explore TLDs for a keyword

```bash
$ dotld acme
acme
├─ acme.com · Taken
├─ acme.net · Taken
├─ acme.org · Taken
├─ acme.io  · $39.99 · https://www.dynadot.com/domain/search?domain=acme.io&rscreg=github
├─ acme.ai  · Taken
├─ acme.co  · Taken
├─ acme.app · Taken
├─ acme.dev · Taken
└─ acme.sh  · Taken
```

### JSON output for scripting

```bash
$ dotld example.com --json
{
  "results": [
    {
      "domain": "example.com",
      "available": false,
      "price": null,
      "currency": "USD",
      "buyUrl": null,
      "cached": false,
      "quotedAt": "2026-02-21T00:00:00.000Z"
    }
  ]
}
```
