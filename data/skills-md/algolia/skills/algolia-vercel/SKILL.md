---
name: algolia-vercel
description: >-
  The Algolia side of a Vercel Marketplace integration: which Algolia variables
  it injects, what the Algolia CLI and the browser each need them to be named,
  and how to reach a validated first search. Use when the user is on Vercel and
  wants Algolia added from the Marketplace — "set up Algolia on Vercel", "vercel
  integration add algolia" — or when Marketplace-injected ALGOLIA_APP_ID /
  ALGOLIA_SEARCH_API_KEY / ALGOLIA_WRITE_API_KEY need to be wired into an app and
  proven with a query. Vercel's own mechanics — teams, plans, terms, billing,
  environment commands — belong to the Vercel docs, not here. Do NOT use
  merely because a project is Next.js — Next.js alone does not mean Vercel. Do
  NOT use when the user has a standalone Algolia application they intend to keep.
  Do NOT use for records, settings, synonyms, rules or keys on an existing
  application (algolia-cli), for search UI (instantsearch), for read-only search
  and analytics (algolia-mcp), or for accounts created outside Vercel
  (algolia-quickstart).
license: MIT
metadata:
  author: algolia
  version: "1.0"
---

# Algolia on Vercel

The Vercel Marketplace can create an Algolia application and inject its credentials into a project. This skill covers the **Algolia** half of that: what the injected variables mean, what to rename them to, which index to search, and what counts as proof that search works.

The **Vercel** half is Vercel's to document. Send every question about teams, linking, installing the integration, plans, terms, billing, prefixes, and environment commands to:

- <https://vercel.com/docs/cli/integration>
- <https://vercel.com/docs/cli/env>
- `vercel integration guide algolia --framework <your framework>` — the integration's own live wiring guide, and the source of truth for the variable names it currently injects

## When to Apply

- The user is on Vercel and wants Algolia from the Marketplace, or names `vercel integration add algolia`
- Marketplace-injected `ALGOLIA_*` variables exist and need to reach the Algolia CLI, the server, or the browser
- A Vercel-provisioned Algolia application needs its first successful query

Do **not** apply when:

- The project is Next.js but nothing indicates Vercel hosting — check for `.vercel/`, a linked project, or `vercel.json`, or ask
- The user has a **standalone** Algolia application they intend to keep. It stays standalone; moving it is a migration they have to ask for
- The work is records, settings, synonyms, rules or keys on an existing application → `algolia-cli`
- The work is search UI and credentials already exist → `instantsearch`
- The account is created outside Vercel → `algolia-quickstart`

## Rules

Read a rule before running its phase. Each carries an `impact` — editorial severity, telling you which to read first, not runtime enforcement.

| Impact   | Rule                                                 | What it protects                                                            |
| -------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| CRITICAL | `rules/credentials-write-key-never-reaches-the-browser.md` | Variable correspondence, and the write key staying out of the client bundle |
| HIGH     | `rules/data-additive-example-index.md`               | The user's existing records, when a demo index is tempting                  |
| MEDIUM   | `rules/validate-search-returns-hits.md`              | The claim you make about the search matching what the query returned        |

## Workflow

**1. Get an Algolia application.**

If the project already has a connected Algolia resource — its configured environment variables are where that shows up — reuse it. Do not create a second one, and do not sign up for a standalone Algolia account just to obtain keys.

If there is none and the user wants one from the Marketplace, the entry point is `vercel integration add algolia`. Read `vercel integration guide algolia --framework <your framework>` and the Vercel docs above for the current flags, plan and region values, metadata keys, and injected variable names — they are live data, so do not write them from memory. Which team is billed, which project the resource connects to, which environments it covers, and accepting the provider terms are the user's decisions and Vercel's mechanics; follow Vercel's flow rather than a recipe here.

Name the environment you are targeting explicitly on every Vercel environment command, and use that same one throughout.

**2. Map the variables.** The injected names are not the names the Algolia CLI or a browser bundle read. Apply `rules/credentials-write-key-never-reaches-the-browser.md`.

The CLI reads its credentials from the environment, so no `algolia auth login` is needed on this path — but it does have to be present: `algolia --version`, or run it through `npx @algolia/cli` ([install](https://www.algolia.com/doc/tools/cli/get-started/overview/)).

**3. Point at data.** Search the index the user already has. Seed a small example index only when the requested search has nothing to run against *and* the user agreed to a demo — `rules/data-additive-example-index.md`.

**4. Validate, then report what happened.** Query with the search-only key and report the actual result — `rules/validate-search-returns-hits.md`.

If the user asked for search UI, keep going: hand the index name, the record shape and the credential *variable* names (never key values) to `instantsearch`.

## Stop and Ask

Ask once for anything below you do not already have an answer to. An answer already given counts; re-confirming it is noise.

| Ambiguity                                            | Ask                                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- |
| An Algolia application may already exist              | Reuse the existing application, or have Vercel provision and bill a separate one? |
| Nothing in the application to search                  | Seed a small example index, or point at data you already have?                    |
| The environment to target                             | Which environment should this be wired for?                                       |

Vercel's own decisions — team, project, plan, terms — surface through its flow; relay what it asks and wait rather than answering for the user.

## Companion Skills

Referencing a skill does not install it, and none of these is a prerequisite. Offer the command once, when the next step needs it:

| Next step                                         | Skill                        | Install                                                            |
| --------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------ |
| Build the search UI                               | `instantsearch`              | `npx skills add algolia/skills --skill instantsearch`              |
| Records, settings, synonyms, rules, keys, backups | `algolia-cli`                | `npx skills add algolia/skills --skill algolia-cli`                |
| Crawl a site into the index                       | `algolia-crawler`            | `npx skills add algolia/skills --skill algolia-crawler`            |
| Plan a full implementation                        | `algolia-discovery-planning` | `npx skills add algolia/skills --skill algolia-discovery-planning` |

## Source Note

The prioritized prefixed-rule layout is modelled on the public [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) format. Algolia adapted it; this is not an endorsed or adopted Vercel skill.

Algolia commands were verified against Algolia CLI 1.17.0. Injected variable names come from the live integration and change without notice — read them from `vercel integration guide algolia --framework <your framework>` and the project's configured environment at run time.
