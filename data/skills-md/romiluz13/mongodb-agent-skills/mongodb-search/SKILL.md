---
name: mongodb-search
description: MongoDB Search engine architecture, query composition, and search operations. Use when creating Search indexes, writing $search or $searchMeta pipelines, choosing analyzers, tuning lexical relevance, handling Search alerts/metrics, deploying Search in Community, or orchestrating hybrid search with $rankFusion/$scoreFusion. Triggers on "MongoDB Search", "Atlas Search", "$search", "$searchMeta", "autocomplete", "synonyms", "facet", "compound", "search score", "highlight", "storedSource", "returnStoredSource", "returnScope", "mongot", "searchCoordinator", "Search Max Fields Indexed", "nGram fields", "$rankFusion", "$scoreFusion", and "hybrid search".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.2.0"
---

# MongoDB Search: Engine, Relevance, and Operations

MongoDB Search guidance for Atlas and self-managed deployments. This skill contains **24 rules across 6 categories**. It focuses on deployment routing, index/mapping guardrails, query composition, hybrid orchestration, and production operations.

## Critical Warning

> Search behavior is release-sensitive. Before applying any advanced pattern, confirm deployment track (Atlas vs local Atlas vs self-managed Community), MongoDB version, and feature status (GA/Preview/Public Preview).

## When to Apply

Use this skill when you are:
- Creating or updating Search indexes and mappings
- Building `$search` and `$searchMeta` pipelines
- Choosing analyzers, autocomplete settings, synonyms, and facets
- Debugging relevance quality or response shape (`highlight`, `returnStoredSource`, `returnScope`)
- Triaging Search alerts, metrics, and index build failures
- Deploying Search on MongoDB Community (`mongot`, `searchCoordinator`)
- Orchestrating hybrid retrieval with `$rankFusion` and `$scoreFusion`

## Scope Boundary with `mongodb-ai`

This skill owns search engine semantics and operations. Hand off to `mongodb-ai` when the request is primarily about:
- Embedding model/provider compatibility (including Voyage `input_type`)
- RAG ingestion/chunking and agent-memory design
- Vector retrieval tuning strategies centered on model behavior

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Deployment Modes and Release Gates | CRITICAL | `deploy-` | 5 |
| 2 | Index Architecture and Mappings | CRITICAL | `index-` | 6 |
| 3 | Query Composition and Relevance | CRITICAL | `query-` | 5 |
| 4 | Hybrid and Vector Interop | HIGH | `hybrid-` | 3 |
| 5 | Operations and Troubleshooting | HIGH | `ops-` | 4 |
| 6 | Skill Boundary Rules | MEDIUM | `boundary-` | 1 |

## Quick Reference

### 1. Deployment Modes and Release Gates (CRITICAL) - 5 rules
- `deploy-track-detection` - Detect Atlas vs local Atlas vs Community before commands
- `release-status-gating` - Tag guidance as GA/Preview/Public Preview
- `community-preview-safety` - Check current release status before recommending Community Search for production
- `community-prereqs-mongot-auth` - Replica set, keyfile auth, and `searchCoordinator` user requirements
- `community-mongot-health-check` - Validate `mongot` health and queryability before tuning

### 2. Index Architecture and Mappings (CRITICAL) - 6 rules
- `index-static-vs-dynamic-mappings` - Prefer static mappings, constrain dynamic scope
- `index-fields-limit-guardrail` - Respond to Search Max Fields Indexed alerts
- `index-ngram-limit-guardrail` - Control nGram/edgeGram/autocomplete field growth
- `index-analyzer-selection` - Align analyzer and tokenizer with operator intent
- `index-synonyms-lifecycle` - Safe synonym source design and update behavior
- `index-facet-field-typing` - Correct facet-compatible field typing

### 3. Query Composition and Relevance (CRITICAL) - 5 rules
- `query-compound-structure` - Use `must`/`should`/`mustNot`/`filter` correctly
- `query-operator-selection` - Pick `text` vs `phrase` vs `autocomplete` vs `queryString`
- `query-score-tuning` - Tune scoring intentionally with measurable guardrails
- `query-return-shape` - Use `highlight`, `returnStoredSource`, and `returnScope` correctly
- `query-facet-pipelines` - Prefer `$searchMeta` for facet-only metadata

### 4. Hybrid and Vector Interop (HIGH) - 3 rules
- `hybrid-lexical-prefilter-routing` - Route simple vs advanced prefilters correctly
- `hybrid-fusion-stage-gates` - Enforce version and stage limits for fusion operators
- `hybrid-strategy-selection` - Choose fusion-only vs two-stage retrieval thoughtfully

### 5. Operations and Troubleshooting (HIGH) - 4 rules
- `ops-alerts-and-metrics-runbook` - Alert-to-action runbook for top Search incidents
- `ops-index-build-failure-triage` - Structured triage for Pending/Building/Stale/Failed
- `ops-log-driven-debugging` - Debug with explain, metrics, and health signals
- `ops-reindex-change-management` - Safe rollout and rollback for index definition updates

### 6. Skill Boundary Rules (MEDIUM) - 1 rule
- `boundary-handoff-to-mongodb-ai` - Transfer provider/model concerns to `mongodb-ai`

## Docs Quick Map

See `references/docs-navigation.md` for release-sensitive routing and boundary checks.

## Production Readiness Checklist

- Confirm deployment track and MongoDB version before selecting syntax.
- Confirm release status for every feature (GA/Preview/Public Preview).
- Confirm index definitions are constrained and alert-safe.
- Confirm query design (`compound`, operator choice, scoring) with explain and metrics.
- Confirm hybrid stage/version compatibility before rollout.
- Confirm boundary handoff to `mongodb-ai` for provider/model semantics.
