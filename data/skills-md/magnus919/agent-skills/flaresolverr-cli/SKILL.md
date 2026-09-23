---
name: flaresolverr-cli
description: >-
  Use a small FlareSolverr JSON CLI for browser-backed GET and POST requests, readiness
  checks, and session lifecycle management when a site requires Cloudflare or DDoS-GUARD
  challenge handling. Do not use this skill for unrelated requests; route to the nearest
  named specialist.
license: MIT
compatibility: Python 3.8+ (stdlib only). Requires a running FlareSolverr instance; FLARESOLVERR_SERVER defaults to http://localhost:8191.
metadata:
  tags: flaresolverr, cloudflare, proxy, anti-bot, headless-browser, web-scraping
  sources: https://github.com/FlareSolverr/FlareSolverr, https://hub.docker.com/r/flaresolverr/flaresolverr
---

# FlareSolverr CLI

Use this CLI with a running private FlareSolverr service when ordinary HTTP requests encounter a browser challenge. It sends JSON commands to FlareSolverr's `/v1` API.

## Quick Start

```sh
export FLARESOLVERR_SERVER="http://localhost:8191"
python3 scripts/flaresolverr-cli health
```

`FLARESOLVERR_SERVER` is optional and defaults to `http://localhost:8191`. Use `--server URL` to override it for one command and `--timeout SECONDS` to set the HTTP timeout; the default is 60 seconds.

## Commands

```text
flaresolverr-cli [--server URL] [--timeout SECONDS] health
flaresolverr-cli [--server URL] [--timeout SECONDS] get URL [--session ID]
flaresolverr-cli [--server URL] [--timeout SECONDS] post URL [--session ID] [--data FORM_BODY]
flaresolverr-cli [--server URL] [--timeout SECONDS] session create
flaresolverr-cli [--server URL] [--timeout SECONDS] session list
flaresolverr-cli [--server URL] [--timeout SECONDS] session destroy [SESSION_ID]
```

`health` is a readiness probe that sends the `sessions.list` JSON command to `/v1`; it does not call `GET /health`.

`get` sends `request.get`. `post` sends `request.post` and includes `FORM_BODY` as `postData` when `--data` is supplied. `--session ID` adds the given session to either request. Session commands create, list, or destroy FlareSolverr sessions; omitting `SESSION_ID` from `session destroy` sends an empty session value.

## Output And Errors

Successful commands print one JSON result to stdout. Request failures print a JSON error to stderr and return a nonzero status.

## Requirements

Python 3.8+ with no pip dependencies and a running FlareSolverr instance. Keep the service private and use it only for sites you are authorized to access.

## References

- [scripts/flaresolverr-cli](scripts/flaresolverr-cli) - Stdlib-only CLI implementation.
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) - Service and API documentation.
