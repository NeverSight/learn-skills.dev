---
name: explore-sota
description: Use when building or expanding the SOTA — from an idea, keywords, seed papers, or the existing collection — through MCP search, citation chasing, triage, and digestion of accepted papers.
license: MIT
---

# Explore SOTA

Run the SOTA exploration loop: discover candidate papers, triage them in
`sota/queue.md`, digest the accepted ones, and repeat until the declared
stopping rule is met. Works for long autonomous sessions and for small
targeted expansions alike.

## Read First

- `sota/README.md` — digestion rules and formats
- `sota/queue.md` — the Scope block and the current frontier
- `references/citation-chasing.md` — frontier discipline, anti-echo-chamber
  rules, review scales

## MCP Preflight (hard gate)

Same gate as digest-paper: by capability, never by API key. `arxiv` must
respond AND at least one of `semantic-scholar`, `dblp`, or `openalex`. If the
gate is unmet: STOP and report. A missing key only throttles; a reachable
source being down degrades the cross-check, not a stop. No fallback to model
memory or web scraping.

## Procedure

1. **Scope.** Read the Scope block at the top of `sota/queue.md`. If empty
   or stale, write it now: research question, keywords/synonyms/adjacent
   terms, inclusion and exclusion criteria, review scale (quick-scan ~8–15
   papers / focused-sota ~20–40 / full-survey 50+), stopping rule. In an
   interactive session confirm it with the user; in an autonomous session
   derive it from `README.md` and record it before searching.
2. **Seeds.** Build a diversified seed set: user-named papers, already
   digested papers, seminal works found via MCP search, recent frontier
   papers. Never start from a single author group, venue, or survey.
3. **Search.** Run keyword queries on every configured scholarly MCP — the
   always-on arxiv, semantic-scholar, dblp, and the paper-search aggregator,
   plus openalex when enabled. Short, high-signal queries; record productive
   terms in the Scope block.
4. **Chase.** For each digested seed, fetch outgoing references and
   incoming citations via semantic-scholar — one hop at a time, per
   `references/citation-chasing.md`.
5. **Dedupe.** Before adding a candidate to the queue, check it is not in
   `sota/index.md` or already in `sota/queue.md` (match DOI, arXiv id, S2
   id, then title + first author + year).
6. **Triage.** Add each new candidate to `queue.md` with provenance
   ("found via") and decide against the criteria: `accepted`,
   `rejected: <reason>`, or `pending`. A candidate no MCP can resolve gets
   `unresolvable-via-mcp` and is never cited.
7. **Digest.** For each `accepted` candidate, run the digest-paper skill
   procedure (all-or-nothing). New digests yield new citation leads — feed
   them back into the queue.
8. **Learn.** After each digestion round, add newly learned terminology,
   benchmarks, venues, and author groups to the scope terms and re-search.
9. **Stop.** Before declaring saturation, run the anti-echo-chamber checks
   in `references/citation-chasing.md`. Stop at saturation (a hop yields
   mostly duplicates or out-of-scope work) or at the declared budget — in
   that case record the unexpanded frontier as `pending` rows, never
   silently.
10. Run `make check` and leave no untriaged row before ending the session.

## Rules

- Every candidate enters `queue.md` before any digestion decision; the
  queue is the only frontier record.
- Rejections always carry a reason tied to the exclusion criteria.
- Citation counts and graph centrality are discovery signals, not
  relevance or quality judgments.
- Never pad toward the paper budget: scale targets are budgets, not goals.

## Done When

- No `pending` row remains, or the unexpanded frontier is explicitly
  recorded and reported to the user
- The Scope block reflects the final criteria and the saturation/budget
  outcome
- `make check` passes
