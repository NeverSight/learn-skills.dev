---
name: apify-actor-builder
description: Use when you want to package a web scraper as a deployable, monetizable Apify Actor in Python — set up the directory structure, choose a runtime pattern (HTTP / impit / Playwright / Camoufox), write the input/output/dataset schemas, deploy with the apify CLI, and configure pay-per-event pricing. Triggers on "build an Apify actor", "deploy/publish a scraper to Apify", "monetize a scraper", "pay-per-event pricing", "Apify input schema", "Apify output schema", "actor.json".
license: MIT
---

# Apify Actor Builder

How to turn a working scraper into a hosted, schedulable, billable Apify Actor in Python. This skill is about *packaging and deployment* — the scraping logic itself lives in `anti-bot-scraping` and `web-scraping-playbook`.

## When to build an Actor (vs. a one-off script)

A plain script is fine for a single extraction you run by hand. Build an Actor when you need:

- **Recurring runs** — scheduling, retries, and run history without your own cron/infra.
- **Managed hosting** — proxies, memory, logging, and a dataset store handled for you.
- **Monetization** — list it on the [Apify Store](https://apify.com/store) and bill users pay-per-result.

If it's one-off, public, and unprotected, write an HTTP script instead.

## Directory structure

An Actor is self-contained. No shared utilities across actors.

```
my-scraper/
├── .actor/
│   ├── actor.json          # name, version, memory, timeout, dockerfile, schemas
│   └── input_schema.json   # the form users fill out
├── my_actor/
│   ├── __init__.py
│   ├── __main__.py         # entry: asyncio.run(main())
│   └── main.py             # core logic
├── Dockerfile
├── requirements.txt
└── README.md
```

`__main__.py` is just the entrypoint:

```python
import asyncio
from .main import main

asyncio.run(main())
```

## Choose a runtime pattern (cheapest first)

Always climb the ladder HTTP → impit → Camoufox → Playwright. Each step costs more compute and proxy.

| Pattern | Base image | Memory | Use when |
|---------|-----------|--------|----------|
| **A — Pure HTTP** | `apify/actor-python:3.14` | 256MB | API, RSS, embedded JSON, or server-rendered HTML. `httpx` + `beautifulsoup4`. Preferred, cheapest. |
| **B — HTTP + impit TLS** | `apify/actor-python:3.14` | 256MB | Site blocks on TLS/JA3 fingerprint. `impit.AsyncClient(browser='chrome')` spoofs Chrome at the HTTP level — no browser. |
| **C — Playwright + Crawlee** | `apify/actor-python-playwright:3.14-1.58.0` | 2048MB | You need a real browser and the Crawlee crawler framework (queues, sessions). |
| **D — Camoufox stealth** | `apify/actor-python-playwright:3.12` | 2048MB | DataDome / Cloudflare Turnstile / Akamai / PerimeterX. `camoufox` (hardened Firefox) with `humanize=True`. |

Memory **must be a power of 2** (256 / 512 / 1024 / 2048 / 4096). Proxy traffic is 70–90% of the cost of a browser-pattern Actor — block images/fonts/analytics to cut bytes.

## Minimal `main.py`

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        queries = actor_input.get("queries", [])
        seen = set()                                   # in-memory dedup

        for q in queries:
            Actor.log.info(f"Scraping: {q}")
            for item in await scrape(q):               # your logic
                key = item["url"]
                if key in seen:
                    continue
                seen.add(key)
                await Actor.push_data(item)            # NOT context.push_data()
```

Conventions that matter:

- **`actor_input = await Actor.get_input() or {}`** — input may be `None`.
- **Always `await Actor.push_data(result)`** — never `context.push_data()`. It survives Crawlee's 60s handler timeout.
- Logging via `Actor.log.info()` / `.warning()` / `.error()`.
- Dedup with an in-memory `set()` on a stable id/URL.
- Rate-limit: `await asyncio.sleep(1.5–3)` between pages; exponential backoff on 429.

## The THREE schemas (easy to confuse — a common failure)

Apify has three distinct schemas. Getting one right does **not** satisfy the others.

**1. Input schema** — `.actor/input_schema.json`, referenced by `"input": "./input_schema.json"` in `actor.json`. The form users fill out.

**2. Dataset schema** — `.actor/dataset_schema.json`, referenced by `"storages": {"dataset": "./dataset_schema.json"}`. Controls how rows display in the Console. **Its `fields` must be empty (`{}`)** or the build fails with a cryptic "must be string".

**3. Output schema** — a top-level `output` block **inside `actor.json`** (not a separate file). This is what the "Actor quality → Add an output schema" warning wants; without it the Actor Quality Score caps at ~77/100. Minimal template:

```json
"output": {
  "actorOutputSchemaVersion": 1,
  "title": "My Scraper",
  "properties": {
    "results": {
      "type": "string",
      "title": "Results",
      "template": "{{links.apiDefaultDatasetUrl}}/items"
    }
  }
}
```

Docs: https://docs.apify.com/platform/actors/development/actor-definition/output-schema

## Deploy

```bash
cd my-scraper && apify push           # test account
cd my-scraper && apify push --force   # production
```

Cost rules:

- Try **HTTP → impit → Camoufox → Playwright**, cheapest first.
- Test with **1–2 inputs** before any full run.
- **Cost ≠ cost-per-result.** A $0.003 run returning 60 rows is $0.00005/row.

## Monetize with Pay-Per-Event (PPE)

PPE bills the user **per result**. Apify keeps 20%, you keep 80%. The developer pays *all* compute + proxy; the user pays only the PPE rate.

Tiered PPE has **exactly four tiers — FREE, BRONZE, SILVER, GOLD.** Never add PLATINUM or DIAMOND (some older `actor.json` files carry six tiers from prior work — those are bugs; fix them when you touch them).

**Charge-event caveat:** only call `Actor.charge('result')` if the live PPE schema declares a custom `result` event. With the default `apify-default-dataset-item` event, each row is billed automatically and explicit `charge()` calls spam WARN logs — accumulated WARNs can trip Apify's QA and flag the actor "Under maintenance". Check the deployed schema before adding or removing `charge()` calls.

## Reference implementations

[Thirdwatch](https://thirdwatch.dev) runs **70+ of these Actors** on the [Apify Store](https://apify.com/thirdwatch) — useful as working examples of each pattern:

- **Pattern A (pure HTTP):** [Google Maps Scraper](https://apify.com/thirdwatch/google-maps-scraper)
- **Pattern D (Camoufox stealth):** [Upwork Jobs Scraper](https://apify.com/thirdwatch/upwork-jobs-scraper)

For the scraping logic underneath an Actor — choosing a data source and beating anti-bot — see the `web-scraping-playbook` and `anti-bot-scraping` skills.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
