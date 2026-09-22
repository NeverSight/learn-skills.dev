---
name: twitterapi-io
description: "twitterapi.io fetch: tweets, profiles, replies, quotes, threads, search."
allowed-tools: Bash(./scripts/twitterapi-io:*)
---

# twitterapi-io

Use the local skill script for read-only twitterapi.io access.

This skill exists to make common twitterapi.io reads simple and low-noise instead of rebuilding custom API calls each time.

## Quick rules

- Use this skill only for reads.
- Do not improvise posting/like/reply/delete flows.
- Prefer compact JSON output by default.
- Use `--raw` only when you actually need full API objects.
- Prefer the official docs links in `references/links.md` when validating endpoint behavior.

## Local setup

Prefer the skill-local script over any global CLI install.
Prefer a saved config file over shell-exported environment variables.

No package install is required for the local script. Use:

```bash
<skill-path>/scripts/twitterapi-io
```

Primary config path:

```bash
~/.config/twitterapi-io/config.json
```

Recommended one-time setup:

```bash
<skill-path>/scripts/setup-api-key.sh
```

That writes the API key to the config file so later reads work without needing to source `.env`.

## Commands

### Show built-in help

```bash
<skill-path>/scripts/twitterapi-io help
```

### Authenticate once

```bash
<skill-path>/scripts/setup-api-key.sh
```

You can also use env as an override or fallback, or use `auth --api-key` only when command-history exposure is acceptable:

```bash
export TWITTERAPI_IO_KEY='YOUR_KEY'
<skill-path>/scripts/twitterapi-io auth --api-key YOUR_KEY
```

### Fetch one tweet

```bash
<skill-path>/scripts/twitterapi-io tweet --url 'https://x.com/jack/status/20'
```

or:

```bash
<skill-path>/scripts/twitterapi-io tweet --id 20
```

### Fetch one user

```bash
<skill-path>/scripts/twitterapi-io user --username OpenAI
```

### Fetch recent tweets for a user

```bash
<skill-path>/scripts/twitterapi-io user-tweets --username OpenAI --limit 10
```

Include replies:

```bash
<skill-path>/scripts/twitterapi-io user-tweets --username OpenAI --limit 10 --include-replies
```

### Fetch replies to a tweet

```bash
<skill-path>/scripts/twitterapi-io replies --url 'https://x.com/jack/status/20' --limit 20
```

Optional unix-time filters:

```bash
<skill-path>/scripts/twitterapi-io replies --id 20 --since-time 1741219200 --until-time 1741305600 --limit 20
```

### Fetch quote tweets

```bash
<skill-path>/scripts/twitterapi-io quotes --id 20 --limit 20
```

### Fetch thread context

```bash
<skill-path>/scripts/twitterapi-io thread-context --id 20 --limit 40
```

### Fetch mentions for a user

```bash
<skill-path>/scripts/twitterapi-io mentions --username OpenAI --limit 20
```

### Advanced search

```bash
<skill-path>/scripts/twitterapi-io search --query 'AI agents -filter:replies' --from-user OpenAI --within-time 24h --max-tweets 50
```

Use `Top` results when needed:

```bash
<skill-path>/scripts/twitterapi-io search --query 'AI agents' --queryType Top --max-pages 2
```

Use explicit unix-time operators when needed:

```bash
<skill-path>/scripts/twitterapi-io search --query '$BTC' --since-time 1741219200 --until-time 1741305600 --max-tweets 50
```

## Workflow

1. Read `references/links.md` if you need the underlying official twitterapi.io docs links.
2. Use the local skill script.
3. Ensure the API key exists in `~/.config/twitterapi-io/config.json` or via env.
4. Use `tweet`, `user`, `user-tweets`, `replies`, `quotes`, `thread-context`, `mentions`, or `search` as needed.
5. Keep reads narrow and intentional.

## Expected outputs

The CLI returns JSON. Parse it instead of scraping human text.

Default output is compact and low-noise.
Use `--raw` when full endpoint payloads are actually needed.

## Files

- Package repo: `https://github.com/robin-liquidium/twitterapi-io-cli`
- Launcher: `scripts/twitterapi-io`
- Python implementation: `scripts/twitterapi_io.py`
- Credential setup helper: `scripts/setup-api-key.sh`
- Official docs links: `references/links.md`
- Config storage: `~/.config/twitterapi-io/config.json`
- `.env` is optional fallback only; it is not the preferred long-term setup.

## When to stop and ask

Stop and ask before:
- adding write/posting capabilities
- adding login-cookie flows
- adding broad/high-cost scraping defaults
- changing how API key storage works
