---
name: api-fetcher
description: Fetch data from REST/GraphQL APIs securely.
status: implemented
category: Integration & API
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
  - integration
---

# Api Fetcher

Fetch data from REST/GraphQL APIs securely.

## Usage

node api-fetcher/scripts/fetch.cjs [options]

## Options

| Flag        | Alias | Type   | Required | Description                    |
| ----------- | ----- | ------ | -------- | ------------------------------ |
| `--url`     | `-u`  | string | Yes      | Target URL                     |
| `--method`  | `-m`  | string | No       | HTTP method (default: GET)     |
| `--headers` | `-H`  | string | No       | JSON string of request headers |
| `--body`    | `-b`  | string | No       | JSON string of request body    |
| `--out`     | `-o`  | string | No       | Output file path               |

## Troubleshooting

| Error                                     | Cause                                | Fix                                                               |
| ----------------------------------------- | ------------------------------------ | ----------------------------------------------------------------- |
| `Invalid headers: Unexpected token`       | Malformed JSON in `--headers`        | Ensure valid JSON: `--headers '{"Authorization":"Bearer token"}'` |
| `Invalid request body: Unexpected token`  | Malformed JSON in `--body`           | Validate JSON before passing                                      |
| `ECONNREFUSED`                            | Target server is down or unreachable | Check URL and network connectivity                                |
| `ETIMEDOUT`                               | Request timed out                    | Verify server availability, check firewall rules                  |
| `ENOTFOUND`                               | DNS resolution failed                | Check URL spelling, verify DNS settings                           |
| `Request failed with status code 4xx/5xx` | Server returned an error             | Check authentication, request format, API docs                    |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
