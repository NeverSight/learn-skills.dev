---
name: agent-ready
description: Implements agent-readiness on public sites and docs from Mintlify Agent Score, AFDocs, Is Agentic, Is It Agent Ready, or url-discovery-bench reports, or from server logs of agents 404ing on guessed URLs. Use when asked to "make this agent-ready", "improve Agent Score", "fix llms.txt coverage", "agents keep 404ing on our docs", or when a pasted scorecard is the brief. For docs prose use ghostwriter; for CLI/SDK ergonomics use dx-audit; for agentic product UX use ax-audit; for crawler policy, Next.js markdown routes, and AEO measurement use seo.
compatibility: The verification script needs Bash and curl. Scanner commands need Node.js and npm registry access.
---

# Agent Ready

Turn a public agent-readiness score, or a log of agents failing to navigate, into shipped, verified HTTP and docs changes.

- **IS:** ingesting Mintlify Agent Score / AFDocs, [Is Agentic](https://is-agentic.com/), [Is It Agent Ready](https://isitagentready.com/), or [url-discovery-bench](https://github.com/mintlify/url-discovery-bench) findings, plus server-side evidence of agent 404s, inspecting the repo, implementing the matching protocols, adding tests, and verifying live responses.
- **IS NOT:** rewriting docs prose (`ghostwriter`), package/CLI/SDK ergonomics (`dx-audit`), whether an in-product agent can be trusted (`ax-audit`), or search ranking, crawler policy, and Next.js `llms.txt`/markdown routes (`seo`). Do not vendor [vercel-labs/is-agentic](https://github.com/vercel-labs/is-agentic); that skill retrieves reports. This one implements the product.

## Contents

- [Workflow](#workflow)
- [Reference files](#reference-files)
- [Priority](#priority)
- [Output](#output)
- [Gotchas](#gotchas)
- [Related skills](#related-skills)
- [Sources](#sources)

## Workflow

```text
Agent-ready progress:
- [ ] Step 1: Ingest the report, the agent 404 log, or run scanners against the public URL
- [ ] Step 2: Inspect the existing codebase before any edit
- [ ] Step 3: Inventory every knowledge surface the origin serves and map each finding to a real one; skip surfaces the product does not offer
- [ ] Step 4: Load the matching reference and implement the map first, then failures, then warnings. For Next.js App Router `llms.txt` and markdown routes, load `seo` (that skill's `nextjs-implementation.md` and `answer-engines.md`) instead of a second recipe.
- [ ] Step 5: Add or update tests for every behavior you change
- [ ] Step 6: Verify every public endpoint and machine-readable file you touched (`scripts/check-surfaces.sh`, then the curl recipes for anything it does not cover)
- [ ] Step 7: Report changes, quoted verification, and remaining product decisions
```

A pasted scorecard is the spec. If none is present and the user named a public URL, gather one:

```bash
npx afdocs check <docs-url> --format scorecard --sampling deterministic
npx is-agentic <domain> --json
```

Is It Agent Ready: `POST https://isitagentready.com/api/scan` with `{"url":"<origin>","format":"agent"}`. Prefer the user's pasted report over a new scan when both exist.

Server logs are a brief too. Agents fetch server-side and run no JavaScript, so they never appear in client-side analytics; count requests for `.md` URLs, `llms.txt`, and recognized AI user agents, and treat a stream of 404s from those agents (fetch, 404, guess a sibling path, retry) as the failing check. `references/verification.md` has the log queries and the navigation benchmark.

Step 3 covers the whole origin, not only `/docs`: changelog, release notes, help center, community, and status pages are knowledge agents answer from, and they are usually HTML-only while the docs are ready. Decide per surface whether it gets markdown twins and an index entry; marketing pages do not.

Preserve visual design and existing product behavior. Change discovery, representations, headers, and documented contracts, not the feature set.

Local test suites that cannot reach production are safe to run, fix, and rerun. Do not deploy, change DNS, buy a registry name, or write outside the working tree without authorization.

Done when every in-scope failing check has a code or content change (or an explicit skip with reason), tests cover the new behavior, and Step 6 quotes status, `Content-Type`, and the relevant headers or body from the environment you actually hit.

## Reference files

| File | Read when |
|------|-----------|
| [references/docs-afdocs.md](references/docs-afdocs.md) | Mintlify Agent Score, AFDocs, `llms.txt`, `.md` URLs, the index link in markdown twins, Accept negotiation, page size, auth gates, non-docs knowledge surfaces |
| [references/api-surfaces.md](references/api-surfaces.md) | Is Agentic API findings: JSON errors, OpenAPI, versioning, rate limits, function calling, CLI, MCP |
| [references/site-discovery.md](references/site-discovery.md) | Is It Agent Ready: robots, sitemap, Link headers, DNS-AID, well-known catalogs, bot rules |
| [references/verification.md](references/verification.md) | Step 6: `check-surfaces.sh`, curl recipes, server-log measurement, url-discovery-bench, and what counts as evidence |

## Priority

Agents read markdown fine and fail at navigation. In Mintlify's 2026 benchmark (2,400 tasks, 20 docs sites, Claude and Codex) accuracy held at 94 to 99% in every format while failed requests per task went 2.23 on HTML, 1.42 on plain markdown, 0.11 once each markdown page linked `llms.txt`. Order work accordingly:

1. The map: `llms.txt` on the docs host, a link to it in the first lines of every markdown twin, and `Link` headers that advertise both. Agents request `.md` and `llms.txt` only when they know they exist.
2. Failures the product actually has (docs HTML that agents cannot read, HTML error pages on a real API, gated public docs with no alternate path).
3. Warnings on those same surfaces (`llms.txt` coverage, buried directives, wrong `Content-Type`).
4. Recommended checks that match a surface already in the repo (OpenAPI, MCP, OAuth).
5. Emerging extras (commerce protocols, A2A, DNS-AID) only when the product already offers them or the user asked to add them.

A missing MCP card is not a failure on a site that has no MCP server. Do not invent an API, CLI, or payment protocol to chase points.

## Output

Group work by check. For each: evidence from the report, files changed, exact markup or schema added, verification quote, skip reason if N/A. When the brief was a 404 log or benchmark, quote failed requests per task before and after.

Finish with remaining items that need a product decision, DNS access, or credentials.

## Gotchas

- A `.md` twin has no navigation: the conversion stripped it with the chrome. Emit the `llms.txt` link from the twin route so no page can miss it; a per-page edit drifts.
- Markdown twins are a route in one app. When the changelog or blog lives in a separate marketing app on the same origin, it stays HTML-only without anyone deciding that; walk every app, not only the one with the twin route.
- One `llms.txt` advertised three ways (`rel="llms-txt"` from a proxy, `rel="https://llmstxt.org/rel/llms-txt"` from framework headers, `rel="describedby"` from a layout `<link>`) leaves the scanner reading whichever layer wins on that response. Pick the rel set the scanners probe and emit it from one place.
- `llms.txt` that lists HTML while `.md` twins exist steers agents away from markdown and is scored worse than linking `.md` from the start.
- A directive in `<head>`, nav, or past 50% of the HTML body does not count. Put it in the document body, near the top, server-rendered.
- Returning markdown with `Content-Type: text/plain` or `text/html` is a warn, not a pass. Set `text/markdown; charset=utf-8` and `Vary: Accept`.
- A dashboard with no agent traffic proves nothing: agents run no JavaScript, and Search Console and SERP tools count searchers, not agents. Server logs of `.md`, `llms.txt`, and AI user agent requests are the only readership measure; without a log drain the honest number is No data, not a client-side proxy.
- Bot protection tuned for crawlers (challenge pages, WAF bot rules, tight rate limits on `text/markdown` routes) blocks the agents you are optimizing for, and they cannot pass a challenge. Exempt the machine-readable routes or serve them from paths the rules do not cover.
- Mentioning a CLI or MCP server in `llms.txt` without a published package or live endpoint is a partial that you cannot fix with copy. Ship it or stop advertising it.
- Empty `/.well-known/` documents and stub OpenAPI files fail typed-schema checks. Advertise only what exists.
- Cross-host redirects for `llms.txt` or docs URLs fail agents that do not follow them. Same-host 3xx, or serve the file on the docs host.
- Coverage fail vs curated index: regenerate from the sitemap when the site intends parity; if the index is intentional, say so and do not pad it with marketing URLs.

## Related skills

- `ghostwriter`: page quality after the machine-readable path works
- `seo`: App Router `llms.txt` and markdown routes, sitemaps, robots, crawler policy, and AEO measurement. This skill owns the AFDocs/Is Agentic contract those routes must satisfy.
- `dx-audit`: the CLI or SDK once it exists as a package
- `ax-audit`: in-product agent trust, not public HTTP discovery
- `agents-md`: repo instruction files, not public `llms.txt`

Maintenance only: `evals/evals.json` is for changing this skill, not for a user task.

## Sources

Drew process and check lists from [AFDocs / Agent-Friendly Documentation Spec](https://www.agentdocsspec.com/), [Mintlify Agent Score](https://www.mintlify.com/score), [Is Agentic](https://is-agentic.com/methodology), and [Is It Agent Ready](https://isitagentready.com/llms.txt). Priority order and the navigation findings come from Mintlify's [2026 State of Knowledge Report](https://www.mintlify.com/state-of-knowledge/2026) and its open-source [url-discovery-bench](https://github.com/mintlify/url-discovery-bench). Left their scoring UIs and the official Is Agentic retrieve-a-report skill. Authored the inspect-then-implement loop, skip rules for absent surfaces, and verification contract.
