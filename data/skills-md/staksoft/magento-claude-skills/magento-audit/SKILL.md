---
name: magento-audit
description: >-
  Performance audit of a Magento 2 / Mage-OS / Adobe Commerce storefront: full-page cache
  misses and cacheable="false" leaks, Varnish/Redis configuration, indexer modes and cron
  health, TTFB, payload sizes, and Core Web Vitals. Use this skill whenever the user says a
  Magento store is slow, asks to audit/review/check storefront performance, mentions FPC or
  cache hit rate, X-Magento-Cache-Debug, Varnish not caching, high TTFB, stuck or realtime
  indexers, cron problems, or Core Web Vitals / PageSpeed scores for a Magento or Mage-OS
  site. Works from a URL alone, from a codebase alone, or both. For writing or fixing module
  code, use the magento-module skill instead.
---

# Magento 2 / Mage-OS Storefront Performance Audit

Audit procedure for Magento storefront performance. The output is always a severity-ranked
markdown report ([references/scoring.md](references/scoring.md)) where every finding
carries verbatim evidence and an exact fix — never a list of generic tips.

The cardinal rule: **audit caching first.** Until full-page cache works, every other
number (TTFB, CWV, server load) is measuring the wrong thing. Most "Magento is slow"
reports are FPC failures with a different hat on.

## Pick the mode

| You have | Mode | Tools |
|---|---|---|
| A store URL | **URL mode** | `scripts/check-headers.py`, browser/Lighthouse if available |
| The codebase (and ideally a running install) | **Codebase mode** | `scripts/scan-layout.py`, env.php, `bin/magento` CLI |
| Both | **Combined** — do URL mode first, use codebase mode to explain what it found | both |

Ask for the missing half only if the findings demand it (e.g. URL mode shows MISSes →
request codebase access to find the killer); otherwise audit what you have and record the
gap in the report's "Not audited" section.

## URL mode

1. Collect 3–5 **public** URLs: homepage, a category page, a product page, a CMS page.
   Never test cart/checkout/account pages for cache hits — they are uncacheable by design.
2. Run the header check (stdlib-only Python, two requests per URL so the second is warm):

   ```bash
   python scripts/check-headers.py https://store.example/ https://store.example/some-category \
       [--insecure]   # for local/dev self-signed certs
   ```

   It measures TTFB cold/warm, payload size, compression, and parses
   `X-Magento-Cache-Debug` / `Age` / Varnish headers into pre-classified findings.
3. Interpret with [references/fpc-audit.md](references/fpc-audit.md) — particularly the
   header table and what a warm MISS means.
4. Frontend layer: read [references/frontend-perf.md](references/frontend-perf.md); run
   Lighthouse/PageSpeed if available, otherwise estimate from the fetched HTML (script/CSS
   counts, LCP image preload, lazy-loading mistakes, third-party tags).

## Codebase mode

1. **FPC killers** — scan layout XML for `cacheable="false"`:

   ```bash
   python scripts/scan-layout.py /path/to/magento [--include-vendor] [--json]
   ```

   Severity is pre-classified (default.xml → critical, catalog/CMS handles → critical,
   checkout/customer → info). For runtime killers the scan can't see
   (`isScopePrivate`, session starts in frontend blocks), follow
   [references/fpc-audit.md](references/fpc-audit.md).
2. **env.php and stack** — read `app/etc/env.php` against
   [references/server-config.md](references/server-config.md): cache/session backends and
   Redis DB separation, `http_cache_hosts`, deploy mode, OPcache. Never quote secrets
   (passwords, keys) from env.php into the report — name the key, not the value.
3. **Indexers & cron** — with a running install:

   ```bash
   bin/magento indexer:show-mode      # any 'realtime' on production = finding
   bin/magento indexer:status
   bin/magento cache:status           # full_page enabled?
   bin/magento deploy:mode:show
   ```

   plus the `cron_schedule` checks in
   [references/indexers-cron.md](references/indexers-cron.md). Without a running install,
   audit `crontab.xml` groups and env.php `cron_consumers_runner` statically and note the
   rest as not-audited.

## Write the report

Assemble findings using the template and scoring rubric in
[references/scoring.md](references/scoring.md). Non-negotiables:

- Every finding: verbatim evidence (header value, file:line, CLI output) + one concrete
  fix + effort estimate.
- Rank by impact-per-effort. A critical FPC leak outranks ten image optimizations.
- Include the "Working as intended" section — name the scary-looking-but-correct things
  (uncached checkout, cold-request slowness) so nobody "fixes" them.
- Include "Not audited" — what this mode couldn't see.
- For dev/staging targets, downgrade production-only findings (developer mode, exposed
  debug headers) to info and say absolute timings need re-measuring on production.

## Audit, don't fix

The deliverable is the report. Don't start editing layout XML or env.php unless the user
asks for fixes — then switch to the `magento-module` skill conventions for any code
changes, and re-run the relevant script afterwards to prove the finding is gone.

## Pairing with live data

If the elgentos `magento2-dev-mcp` MCP server is connected, prefer it for reading *merged*
layout/config when chasing an FPC killer — Magento merges XML across modules and themes,
and the single-file view can mislead.
