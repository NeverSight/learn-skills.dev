---
name: api-tester
description: Fires real HTTP requests and validates responses against expectations — status code, JSON field values (dot-notation paths), latency budget, content-type — with stdlib urllib, no requests library, no curl subprocess. Use to verify endpoints from CI or an agent session, smoke-test a deploy, or prove an API behaves as documented before building on it.
when_to_use: After deploying or modifying an API, before writing a client against a third-party endpoint, or as a health-check gate in CI. NOT a load tester or a full contract-test framework; it validates one request/response at a time, deterministically.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [api, http, testing, backend, ci-gate]
---

# API Tester

Agents write API calls; this proves the server answers what you expect.

## Commands

```bash
python3 scripts/api_tester.py https://api.example.com/health
python3 scripts/api_tester.py URL --expect-status 200 --expect-json ok=true
python3 scripts/api_tester.py URL --expect-json data.user.id=42
python3 scripts/api_tester.py URL --method POST --body '{"x":1}' \
    --header "Authorization: Bearer $TOKEN"
python3 scripts/api_tester.py URL --max-latency-ms 500 --json
```

## Checks

| Check | Flag | Gate |
|---|---|---|
| Status code | `--expect-status` (default 200) | exit 1 on mismatch |
| JSON fields | `--expect-json key=value` (repeatable, dot paths) | exit 1 on mismatch or missing |
| Latency | `--max-latency-ms` | exit 1 over budget |
| Reachability | — | exit 2 when the host is down |

## Pairs with

`env-gate` (is the environment configured), `verification-before-completion`
(the discipline that makes you run this before claiming the endpoint works),
`webapp-testing` (when the surface is a page, not JSON).
