---
name: stably-verify
description: |
  Verify that an application works correctly using `stably verify`. Use when
  an AI agent has made code changes and needs to validate the feature works
  in a real browser. The command describes expected behavior in plain English
  and reports a PASS/FAIL/INCONCLUSIVE verdict — no test files generated.
  Triggers on: "verify this works", "stably verify", "check if this works",
  "validate my changes", "verify my feature", "does this work",
  "check the app", "verify the feature".
license: MIT
metadata:
  author: stably
  version: '1.1.0'
---

# Verify App Behavior with stably verify

`stably verify` checks whether your application works correctly by describing expected behavior in plain English. It launches an AI agent that navigates your app in a real browser, interacts with it, takes screenshots, and reports a structured **PASS / FAIL / INCONCLUSIVE** verdict. No test files are generated.

## Pre-flight

**Always run `stably --version` first.** If not found, install with `npm install -g stably` or use `npx stably`. Requires Node.js 20+ and a [Stably account](https://app.stably.ai).

```bash
stably --version
echo "STABLY_API_KEY: ${STABLY_API_KEY:+set}"
echo "STABLY_PROJECT_ID: ${STABLY_PROJECT_ID:+set}"
```

## Usage

```bash
# Verify a feature works
stably verify "the login form accepts email and password and redirects to /dashboard"

# With a specific starting URL
stably verify "the pricing page shows 3 tiers" --url http://localhost:3000/pricing

# Set a budget cap (default: $5)
stably verify "checkout flow completes successfully" --max-budget 10

# Non-interactive mode (for CI or background agents)
stably verify "checkout flow completes" --no-interactive

# Use cloud browser instead of local
stably verify "login works" --browser cloud
```

### Options

| Option | Description |
|--------|-------------|
| `-u, --url <url>` | Starting URL (auto-detected from localhost if omitted) |
| `--max-budget <dollars>` | Budget cap in USD (default: `5`) |
| `--no-interactive` | Skip preflight prompts |
| `--browser <type>` | Browser type: `local` or `cloud` (default: `local`). Also settable via `STABLY_CLOUD_BROWSER=1` |

### Exit Codes

| Code | Verdict | Meaning |
|------|---------|---------|
| `0` | PASS | All requirements verified |
| `1` | FAIL | One or more requirements not met |
| `2` | INCONCLUSIVE | Cannot determine (app unreachable, auth wall, etc.) |

## Iteration Loop

After making code changes, use `stably verify` to check the feature:

1. **Run verify** — `stably verify "description of expected behavior"`
2. **If FAIL** — Read the failure reason and evidence from the output
3. **Fix code** — Modify your application code based on the failure
4. **Re-verify** — Run the same `stably verify` command again
5. **Repeat** until PASS

`stably verify` does not create or modify any files. It only observes and reports. Fix the code yourself based on its findings.

## Composing in Scripts

```bash
# Gate on verification
stably verify "login works" && echo "Feature verified!"

# Handle all three outcomes
stably verify "checkout completes" ; code=$?
if [ $code -eq 0 ]; then echo "PASS";
elif [ $code -eq 1 ]; then echo "FAIL";
else echo "INCONCLUSIVE"; fi
```

## Long-Running Commands (AI Agents)

`stably verify` is AI-powered and can take **several minutes** depending on complexity.

| Agent | Configuration |
|-------|--------------|
| **Claude Code** | `timeout: 600000` on Bash tool |
| **Cursor** | `block_until_ms: 900000` |

## Links

[Docs](https://docs.stably.ai) · [Verify Guide](https://docs.stably.ai/use-cases/verify-with-ai-agents) · [CLI Quickstart](https://docs.stably.ai/stably-cli/quickstart) · [Dashboard](https://app.stably.ai)
