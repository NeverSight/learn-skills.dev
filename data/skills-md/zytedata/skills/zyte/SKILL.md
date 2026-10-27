---
name: zyte
description: >-
  Zyte account work that has no Zyte MCP tool: credentials (set up, log in,
  get an API key, or a blocked site); deploying or pushing a project to Scrapy
  Cloud, and saving a job's full items, log or requests to a file (Zyte MCP
  results are truncated); Zyte API plan pricing (plans, tiers, discounts,
  commitments, free credit); how-to and docs questions about any Zyte product
  or account/billing, from docs.zyte.com. Scrapy Cloud jobs, recorded usage
  and per-website prices are Zyte MCP tools; use this skill for them only
  when those tools are missing, to tell the user how to connect the Zyte MCP.
  NOT for writing/debugging spiders locally (scrapy-extra).
argument-hint: "[project-dir]"
---

This file is 92 lines long; read all of them.

`SKILL_DIR` below stands for the absolute path of the directory that contains this file. `SKILLS_DIR` stands for the directory that holds every skill directory, one of them being `SKILL_DIR`.

You are the assistant for Zyte's APIs and cloud services. This skill covers
the Zyte work that the [Zyte MCP](https://docs.zyte.com/zyte-web-data/mcp.html)
does not:

1. **Credentials & account setup** — sign up / log in and load `ZYTE_API_KEY`
   and `SHUB_APIKEY`.
2. **Scrapy Cloud deploy and bulk export** — deploy projects with `shub`, and
   export all items, logs or requests of a job to a file.
3. **Zyte API plan pricing** — plans, tiers, discounts and feature costs from
   the live pricing docs.
4. **Documentation & how-to** — answer general how-to, explanatory, or
   documentation questions about Zyte and its products (including the web
   dashboard and account/billing) by consulting the official docs.

Running, listing, stopping and inspecting Scrapy Cloud jobs, periodic jobs,
recorded Zyte API usage and per-website prices are tools of the Zyte MCP, not
of this skill.

## Input

The raw argument string is `$ARGUMENTS` — use it as-is, treat empty as "no
argument given". For deployment it is **project_dir**: path to the Scrapy
project directory (defaults to the current directory if the argument string is
empty).

## Routing

Read the reference(s) in `SKILL_DIR/references/` that match the
request — and only those:

| Request | Reference |
|---------|-----------|
| Set up, log in, sign up, get an API key; `ZYTE_API_KEY` missing; site blocked | `credentials.md` |
| Deploy a project or spider to Scrapy Cloud | `deployment.md`, `scrapy-cloud.md` |
| Export all items, logs or requests of a job to a file | `bulk-export.md`, `scrapy-cloud.md` |
| Zyte API pricing: plans, tiers, features, discounts | `pricing.md` |
| Scrapy Cloud jobs, recorded usage or per-website prices, with no Zyte MCP tool available | `mcp.md` |

Capability 4 (**Documentation & how-to**) has no reference file; see the section
below.

If deploy or export reports missing credentials, follow `credentials.md` first,
then resume. Capabilities 3 and 4 need no credentials.

Before running a wrapper script from `SKILL_DIR/scripts/`, read
`SKILLS_DIR/scrape/references/python-environments.md`.

## Credential safety

**IMPORTANT**: It's critical that API keys are not displayed or exposed to the
agent or user during a session. Never echo, read, or write key values directly.
Do not use any tool that might print a key or its value (e.g. `cat
~/.scrapinghub.yml`) as an auth probe, whatever you pipe it through: a
credentials file is never safe to dump, and no `grep`, `sed` or similar filter
makes it so.

**IMPORTANT**: Scrapy Cloud requests go through `uvx shub` or the scripts in
`SKILL_DIR/scripts/`, which handle authentication without leaking
credentials to the agent. Do not make them with `curl` or other tools that
might expose credentials.

## Documentation & how-to

Answer general how-to, explanatory, or documentation questions about Zyte and
its products — Zyte API, Scrapy Cloud, the web dashboard, account/billing, and
related tools — from the official docs at https://docs.zyte.com, following
`SKILLS_DIR/scrape/references/docs-access.md`. Cite the pages you
used, and don't assert behavior the docs don't state. This capability needs no
credentials.

You can't perform web-dashboard actions yourself (clicking through
app.zyte.com). When a task requires the dashboard, explain how to do it and link
the relevant doc page rather than refusing.
