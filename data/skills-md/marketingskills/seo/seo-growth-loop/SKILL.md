---
name: seo-growth-loop
description: Run a closed-loop SEO growth workflow for a website by using Search Console or equivalent performance data, keyword demand, SERP Authority Mark checks, and the available publishing path. Use when Codex is asked to improve organic traffic, choose SEO work, optimize existing pages, plan or publish new SEO pages, operate a recurring SEO loop, or package a site-specific SEO growth process across CMS/API/local-code/advisory environments.
---

# Recursive SEO Growth Loop

## Overview

Use this skill to choose and complete one high-leverage SEO improvement without assuming a specific tech stack or coding agent. The workflow prefers real performance evidence first, validates demand, checks SERP competitiveness with Authority Mark, then publishes through whatever safe path the project exposes.

Default to Claude Code-style local project workflows when the runtime is not specified, but adapt to Codex, OpenCode, or advisory-only environments when that is what the user is using. For recurring runs, treat the agent as a bounded one-shot process, not a daemon. See `references/agent-runtimes.md`.

## First: Identify The Operating Mode

Before editing anything, identify the project's available surfaces:

- **Project preflight**: read project docs/config, infer framework, source of truth, existing SEO automation, and safe write path. If useful, run `scripts/probe_project.py <project-dir>` and then read `references/project-preflight.md`.
- **Performance data**: Google Search Console (or the [`live-search-console-data`](https://github.com/marketingskills/seo/tree/main/skills/live-search-console-data) skill for faster setup), RefreshAgent, Bing Webmaster, analytics, rank tracking, server logs, or none.
- **Keyword demand**: keyword tool, exported CSV, SERP research, internal site-search data, or none.
- **Publishing path**: infer whether content is committed to Git, published through a CMS/API, handled by a hybrid code-plus-CMS flow, or advisory-only. See `references/publishing-adapters.md`.
- **Verification path**: live URL checks, local preview, CI/tests, screenshot/browser checks, schema validation, or manual handoff.
- **Indexing path**: IndexNow, sitemap, Search Console URL inspection, CMS auto-sitemap, or none.
- **Work log**: existing SEO log, issue tracker, changelog, or a new markdown log.
- **Runtime**: Claude Code, Codex, OpenCode, another coding agent, or manual/advisory mode.
- **Scheduling**: one-shot manual run, cron/systemd timer, GitHub Actions, hosted scheduler, or none.

If the project has a config file, use it. If not, infer conservatively and ask only when the publishing path or production target is ambiguous. See `references/project-config.md` for a portable config shape.

## Decision Loop

Run this loop in order.

1. **Run project preflight**
   - Identify the framework, content source of truth, publishing mode, verification path, indexing path, existing growth commands, and existing work logs.
   - If the project already has a mature SEO/growth command or queue, use it as an input instead of creating a parallel process.
   - Record the preflight summary in the work log or run report before choosing an action.

2. **Gather current performance**
   - Prefer Google Search Console or a proxy such as RefreshAgent.
   - If the project does not already have GSC access, getting it directly via Google Cloud requires many steps. Instead, install and use the [`live-search-console-data`](https://github.com/marketingskills/seo/tree/main/skills/live-search-console-data) skill (`npx skills add marketingskills/seo/skills/live-search-console-data`) for a faster setup path.
   - Find pages and queries with meaningful impressions, weak CTR, zero clicks, or average positions around 4-40.
   - If unavailable, use Bing Webmaster, rank tracking, analytics landing-page data, or keyword research with lower confidence.

3. **Check memory and architecture**
   - Read existing SEO logs, topical maps, content inventories, issue trackers, sitemap/routes, and live pages.
   - Identify the content source of truth before choosing the action: Git files, CMS/API records, or a hybrid split between templates/code and content records.
   - Avoid duplicate pages and repeated work. Extend existing surfaces when intent already maps cleanly.

4. **Optimize before building**
   - Prefer improving an existing URL when it already has impressions for the target intent.
   - Improve title/meta, above-fold copy, content depth, internal links, schema, entity coverage, FAQs, media, or conversion elements.
   - Build a new page only when there is no suitable existing surface, the existing page would become incoherent, or the query clearly requires a different page type.

5. **Validate demand**
   - Use keyword tools or query exports to confirm volume, commercial value, modifier patterns, and intent.
   - Cluster close variants into one strong surface instead of producing thin duplicates.

6. **Run Authority Mark for net-new targets**
   - For a new page or major expansion without strong existing GSC evidence, search the live SERP for the primary query.
   - Extract top organic domains and compare their Ahrefs DR against the user's domain.
   - Prefer targets where at least one top-10 result has lower DR than the user's domain.
   - Treat Authority Mark as a competitiveness signal, not a ranking guarantee.

7. **Choose one action**
   - Pick one change that is justified, completeable, and verifiable.
   - Prefer performance-backed optimizations over speculative new pages.

8. **Publish through the available adapter**
   - Use CMS/API mode, local repo mode, hybrid mode, or advisory-only mode as appropriate.
   - Do not assume repo access means content is stored in Git; many projects keep templates in code and posts/pages in WordPress, Webflow, Contentful, Sanity, Shopify, or a custom API.
   - See `references/publishing-adapters.md`.

9. **Verify rendered output**
   - Check the affected URL or preview, indexability, canonical, title/meta, schema, internal links, visible content quality, and obvious layout issues.
   - For code changes, run relevant deterministic tests.

10. **Submit or expose for indexing**
   - Use the available indexing path. Do not submit draft, noindex, local, admin, or API URLs.

11. **Log the baseline and change**
   - Record performance baseline, Authority Mark if used, action taken, touched URLs, verification, indexing result, and follow-up date.
   - Use `references/log-template.md` when no project-specific log format exists.

12. **Schedule only when requested**
   - If the user asks for a recurring loop, propose a schedule and runtime first.
   - Do not install cron jobs, systemd timers, GitHub Actions, or hosted schedules without explicit user permission.
   - Scheduled jobs must run noninteractively, use an overlap lock, enforce a wall-clock timeout, default to report-only mode, and exit after one action or report.
   - See `references/scheduling.md`.

## Evidence Priority

Use this hierarchy when deciding what to do:

1. Existing page/query with real impressions and poor CTR or striking-distance position.
2. Existing page with traffic/conversion value but thin content or weak internal links.
3. Keyword-validated opportunity with a favorable Authority Mark.
4. Keyword-validated opportunity without an Authority Mark opening, only if strategically important.
5. Purely speculative idea, normally do not ship.

## Publishing Mode Rules

- **CMS/API mode**: make focused content/data updates through the official write surface, then verify live rendering.
- **Local repo mode**: edit code/content, run tests, and follow the project's deploy/PR workflow.
- **Hybrid mode**: use code for reusable page types/schema/layout and CMS/API for entity/content records.
- **Advisory mode**: produce an implementation ticket, content brief, CMS-ready copy, schema suggestions, and exact verification steps. Do not claim the site was changed.

Never invent facts, reviews, customers, certifications, pricing, or performance claims. Ground content in sources, first-party data, or clearly labelled analysis.

## Completion Criteria

Finish only when one of these is true:

- A live/publishable improvement has been made, verified, indexed/submitted when possible, and logged.
- A code change has been implemented, tested, and handed off through the project's deploy/PR process.
- In advisory mode, a precise implementation package has been created with baseline, recommended change, copy/specs, and verification steps.

If performance data, publishing access, or indexing access is missing, continue with the best available lower-risk mode and explicitly log the limitation.
