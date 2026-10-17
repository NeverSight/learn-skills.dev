---
name: algolia-audit
description: >
  Entry point for auditing, reviewing, or health-checking an EXISTING Algolia implementation. Use when the ask sounds like: "audit our search", "review our setup", "is this configured correctly", "health check", "we inherited this implementation", "something seems off with search", "search quality got worse", "check our Algolia before launch", or any troubleshooting of an implementation that already exists and mostly works. This skill routes to the deep skills (algolia-index-configuration, algolia-data-modeling, algolia-events-insights, algolia-release-qa) and enforces the checks that catch symptom-free defects — the class of issue that never errors and never fails a demo. Do NOT use for net-new builds; start with algolia-discovery-planning. Do NOT use for live account operations; use algolia-cli or algolia-mcp for the live calls and this skill to direct and interpret them.
license: MIT
metadata:
  author: algolia
  version: "0.1"
---

# Algolia Audit

Use this skill FIRST when reviewing an existing Algolia implementation. Its core premise: **the costliest configuration defects are symptom-free.** The store works, queries return, nothing errors — and the settings are still wrong in ways that quietly cost relevance, analytics integrity, security, and revenue. An audit that only investigates visible breakage will systematically miss them.

## Customer-Facing Standard

- Audit against what correct looks like, not against whether anything is visibly failing. "It works" is not evidence that it is right.
- Capture the current live state (settings, replica settings, sample hit payloads, a rendered page) before proposing any change, so every finding has a before/after.
- Lead the report with the highest-severity findings; state what was checked, what was not, and what evidence backs each finding.
- When live Algolia data, settings, or account inspection is needed, use the Algolia CLI, Algolia MCP, or official Algolia skills for the live operation, then apply this skill to interpret results.
- Distinguish defects (wrong against documented practice) from preferences (defensible alternatives), and say which is which. Do not reclassify a defect as a preference to avoid the work of fixing it.

## Official Companion Skills

Route deep work to the focused skills — read them, don't reinvent them:

- `algolia-index-configuration` for settings correctness: searchable attributes, custom ranking, faceting completeness, replicas, typo tolerance, retrieval hygiene. Its Settings Audit Checklist is the core of any config review.
- `algolia-data-modeling` for record-shape questions: ranking-signal precision and bucketing, variant strategy, public-response allowlist, effective-price contract.
- `algolia-events-insights` for the event pipeline: attribution chain, duplicate-event rules, InstantSearch auto-event behavior, loader correctness.
- `algolia-release-qa` for the final evidence-led report format and its Finish Gates (page startup, mobile width, captured payloads, claims audit).
- `algolia-cli` / `algolia-mcp` for every live read or write.

## Workflow

1. Inventory the surfaces in scope: indices and replicas, frontend page(s), event pipeline, API keys.
2. Capture live evidence before judging anything: primary settings, EACH replica's settings, a public-key query's raw hit payload, a facet-stats request for every numeric attribute the UI ranges over, and the rendered page (desktop and ~375px) with its console.
3. Read `algolia-index-configuration` and `algolia-data-modeling` before scoring the configuration — check the live state against their standards, not against memory or against "does it error".
4. Run the symptom-free checklist below. Every item must end in one of: verified correct, defect (with fix), or explicitly deferred with a reason the customer accepted.
5. Fix, then re-verify each fix against live state — settings read-back, live queries, rendered page, captured event payloads. A write-up claim without live evidence is not a fix.
6. Report via `algolia-release-qa` conventions: severity-led findings, evidence per finding, tests run and not run, residual risk.

## The Symptom-Free Checklist

Each of these passes every demo and every "does it error" test while being wrong. Check all of them, live:

- **Ranking tie-breakers**: does a near-unique numeric (raw popularity, raw sales) lead `customRanking`, making every later signal inert? Correct practice: bucket the leading signal, keep a complete ordered chain. Adding one availability flag is not a chain.
- **Searchable facets**: is every high-cardinality picker facet (brand, merchant) declared `searchable(attr)` AND wired to search-within-facet in the UI, AND does a live facet-value search work? All three, or it's a defect.
- **Hierarchy**: do records carry hierarchical category data while the index or UI filters on a flat mixed-level list? That is a defect to fix (level facets + hierarchical widget), not a stylistic preference.
- **Facet stats vs filtering**: for every numeric attribute the UI offers a range over — request `facets: ["<attr>"]` and confirm non-empty stats. Raw `filters` working proves nothing; `filterOnly()` does not produce stats.
- **Retrieval hygiene**: query with the public search key and read the actual hit payload. Internal ranking inputs (popularity, sales velocity, margin) present is a finding, even bucketed.
- **Replica parity**: fetch each replica's settings and diff against the primary. Replicas inherit at creation only; a replica that "looks configured" can be missing its sort criterion entirely or carrying stale drift.
- **Event pipeline truth**: capture actual outbound Insights payloads. Count them (duplicates are a finding), and inspect `index` (never a hardcoded name; `undefined` is a failed implementation), `queryID`, `objectID`, and position.
- **Page startup and mobile**: the page renders with zero blocking console errors, and works at ~375px without horizontal overflow. One uncaught loader error can blank the whole experience while every settings check passes.
- **Key scope**: which key does the frontend ship, and what can it do? A write-capable key in page source is a critical finding; an app-wide search key deserves a documented decision versus a secured/index-restricted key.

## Anti-Patterns

- Auditing only what a user or test can see failing. The audit exists precisely for what doesn't fail visibly.
- Clearing a checklist item because the surrounding feature "works" (filters work ≠ facet stats exist; page loads ≠ events attributable).
- Diagnosing a defect correctly and then deferring it as a preference or business decision without the customer actually deciding.
- Trusting the implementation's own comments, docs, or previous audit claims over live state.
- Rewriting working, defensible choices because the auditor would have built it differently — findings need a standard they violate, not a taste difference.
- Finishing without re-verifying your own report's claims against the live index and rendered page.

## Output Contract

Deliver a severity-led audit report: per finding — what is wrong, the standard it violates, live evidence, the fix applied (or proposed), and post-fix verification evidence. Separate: defects fixed, defects proposed, deliberate deferrals with owner, preferences noted without action, and residual risk (what could not be inspected). Every symptom-free checklist item appears with an explicit verdict.
