---
name: pravidhi-ddgs-internet-search
description: Perform web searches using DuckDuckGo. Features soft-failure mode, generic environment support, and context-safe output.
license: MIT
compatibility: Requires Python 3.9+ and internet access.
metadata:
  version: "1.0.0"
  tags: "search, duckduckgo, research, web, python"
---

# Internet Search Skill (DDGS)

> **Developed and maintained by [Pravidhi](https://pravidhi.net)**

This skill performs internet searches using the DuckDuckGo Search library. It is designed to be low-friction and context-safe for AI agents.

## Prerequisite: Installation

This skill requires the `duckduckgo-search` library. Install it in your agent's active Python environment.

```bash
pip install duckduckgo-search
```

## Usage

**Standard Search:**
Execute the script using your active Python interpreter.

```bash
# Syntax: python scripts/search.py -q "QUERY" -m MAX_RESULTS

python scripts/search.py -q "AI funding 2026" -m 3
```

**Safe Mode (Use if getting timeouts):**
The script includes a `--safe` flag that adds extra delay (3s) and disables aggressive backends.

```bash
python scripts/search.py -q "latest linux kernel features" -m 5 --safe
```

## Known Limitations & Troubleshooting

> **Warning:** This skill relies on scraping DuckDuckGo. It is not an official API.

1.  **Rate Limiting / IP Blocking:**
    * **Symptom:** `429 Too Many Requests` or `Ratelimit` errors.
    * **Cause:** Cloud/Datacenter IPs (AWS, GCP) are often flagged by DuckDuckGo.
    * **Fix:** Wait 60 seconds. Try the `--safe` flag. If persistent, use a residential proxy or switch to an API-based skill.

2.  **Soft Failures:**
    * The script is designed to "soft fail". Instead of crashing with a non-zero exit code, it will return a JSON object with `status: error`. Agents should parse the JSON output to handle errors gracefully.

## References

* [CLI_OPTIONS.md](references/CLI_OPTIONS.md) - Script argument reference.