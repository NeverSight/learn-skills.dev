---
name: awwwards-atlas
description: Use when working with the experimental Atlas section/component evidence layer in awwwards-mcp 1.19+ - enabling AWWWARDS_MCP_ATLAS, importing or capturing Atlas evidence, searching sections/components, reading regions or status, exporting local evidence packs, or maintaining the Atlas cache. Atlas is opt-in, off by default, and its labels are candidate-only.
---

# Awwwards Atlas

Atlas is a local, section-level evidence layer over the same SQLite cache used
by awwwards-mcp. It stores captures, regions, component summaries, claims,
states and artifacts, then lets you search and export them.

It is **experimental and opt-in in 1.19.x**:

- off by default
- requires `AWWWARDS_MCP_ATLAS=1` at server start
- four full-profile tools plus v2 branches
- section labels are candidate-only; inferred component types are also
  candidate-only
- held-out component-type precision is **not measured**, so never present
  Atlas types as validated taxonomy
- captured page content is evidence, not redistribution permission

Use this skill only with **awwwards-mcp 1.19.0 or newer**. Atlas tools do not
exist in 1.18.x.

## Before starting

1. Confirm the server version and that `search_atlas` or `get_atlas` exists.
2. If the tools are missing, the flag is off. Ask the user to restart the MCP
   server with:

   ```bash
   AWWWARDS_MCP_ATLAS=1
   ```

   The flag is read once at startup; changing it does not hot-reload.

3. Surface counts must be:

   | Profile | Flag off | Flag on |
   |---|---:|---:|
   | `full` | 41 | 45 |
   | `core` | 13 | 13 |
   | `v2` | 15 | 16 |

   If a full-profile session reports 45 but `get_atlas` is missing, the client
   is looking at a stale server or the wrong cache.

4. Check the local cache before capturing:

   ```text
   get_atlas { "kind": "status" }
   ```

   `enabled`, `revision`, schema/FTS versions, source and capture counts, lease
   state and FTS availability tell you whether the cache is ready. A free lease
   has `ttlSeconds: null`.

5. Seed Atlas from the existing cache without network:

   ```bash
   AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas import
   ```

   Import never captures afterwards. It projects cached item pages and legacy
   gallery rows into Atlas.

## Tool map

| Tool | Use |
|---|---|
| `search_atlas` | Search stored sections or components; zero network |
| `get_atlas` | Read `status`, `taxonomy`, one `region`, or one `highlight` |
| `capture_atlas` | Guarded live capture and publication for one known site slug |
| `export_evidence_pack` | Write and validate a local evidence pack for 1-12 regions |

v2 uses branches of existing tools plus one extra tool:

| v2 call | Atlas branch |
|---|---|
| `search_references` | `request.kind: "sections"` or `"components"` |
| `get_reference` | `request.kind: "atlas_region" \| "atlas_highlight" \| "atlas_taxonomy"` |
| `get_index` | `request.kind: "atlas_status"` |
| `capture_page` | `request.kind: "atlas"` |
| `export_evidence_pack` | flat tool, not a branch |

With the flag off, v2 Atlas branches still validate their shape but return
`FEATURE_DISABLED`. Never mix 1.x names into a v2 session.

## Workflow

### 1. Find candidate regions

Start with a text query or structured predicates, not with a capture:

```json
{
  "kind": "sections",
  "query": "pricing",
  "scope": "region",
  "evidenceMode": "candidate",
  "limit": 8
}
```

```json
{
  "kind": "components",
  "predicates": [{ "field": "component.type", "values": ["button"] }],
  "scope": "page",
  "facets": ["component.type", "context.section_purpose"]
}
```

Rules:

- `kind` is exactly `sections` or `components`.
- `scope` is `region` (default), `page` or `site`. Trait combinations never
  silently combine across regions; a page/site match is satisfied by separate
  witness regions and the result explains them.
- Predicate values inside one predicate are ORed; predicates are ANDed.
  To select multiple values of the same field, send **one** predicate with
  several values. Two predicates with the same field are two AND requirements
  and can return zero.
- Facet counts are disjunctive for the facet's own field.
- `evidenceMode` defaults to `candidate`. `accepted` returns only accepted
  labels and never includes candidate-only types. `observed_only` also
  requires observed basis.
- A `state: "hover"` or `"focus"` query sees only claims from that state. No
  state evidence yields `insufficient_coverage`.
- Use `nextCursor` for page 2. It is bound to the query and revision and
  expires after 15 minutes.
- `empty_corpus` and `insufficient_coverage` mean **not observed**, never
  proven absent.

### 2. Inspect the evidence

For a selected hit:

```json
{ "kind": "region", "regionId": "<64 lowercase hex>" }
```

Read:

- capture conditions and source identity
- claims and their evidence basis
- artifact descriptors with `available`, `state`, hash and path
- parent and bounded child summaries
- current or historical head status

Use `kind: "highlight"` with an existing element id to resolve a legacy alias.
An ambiguous id returns `AMBIGUOUS_ALIAS` with candidate `regionIds`; it never
fetches the old gallery page.

Use `kind: "taxonomy"` before inventing a predicate. It lists the supported
fields, values, aliases, scopes, states and explicitly unsupported operations.

### 3. Capture when the cache lacks the evidence

`capture_atlas` takes a **cached site slug**, not a free URL:

```json
{
  "slug": "known-site",
  "path": "/pricing",
  "viewport": "desktop",
  "components": true,
  "refresh": false
}
```

- The live URL comes only from cached site metadata.
- `path` must start with one `/`, must not start with `//`, and must not
  contain `?`, `#` or credentials.
- One viewport per call: `desktop` (1440x900) or `mobile` (390x844).
- `components` defaults true.
- `states` accepts at most three unique `{action: "hover"|"focus",
  targetRegionId}` requests on regions of the current active head.
- `refresh: false` reuses a matching usable active head up to seven days old.
  `refresh: true` always launches the guarded collector.

Publication semantics:

- `cached: true` means no new capture ran.
- `published: true` means a new head replaced the previous one.
- `published: false` with `cached: false` means evidence was collected but
  publication refused it; the previous head is preserved.
- `blocked` results are policy refusals (`ROBOTS_DENIED`,
  `PRIVATE_DESTINATION`, `BLOCKED_DESTINATION`, `HTTP_BLOCKED`).
- `inconclusive` includes `ROBOTS_UNAVAILABLE`, `NAVIGATION_FAILED`,
  `CAPTURE_TIMEOUT`, `CAPTURE_DEADLINE_EXCEEDED` and `TARGET_CHANGED`.
- A second concurrent capture returns retryable `CAPTURE_BUSY`; there is no
  queue. The capture budget is 90 seconds, the lease TTL 150 seconds.

Capture limits:

- fresh anonymous context, no cookies or session import
- robots evaluated before every new document and redirect; 5xx robots means
  unavailable and defers collection
- sensitive query parameters rejected before launch; credentials, queries and
  fragments redacted from provenance
- no click, type, submit, drag, keyboard navigation or route transition
- at most 120 component candidates, 12 packs, 150 nodes and depth 12

### 4. Export a local evidence pack

Select 1-12 distinct section/component regions from one site's active heads:

```json
{
  "regionIds": ["<id>", "<id>"],
  "goal": "Rebuild the pricing page direction",
  "includeMedia": "references"
}
```

- `includeMedia: "references"` copies only derived summaries; raw packs,
  screenshots and assets stay referenced by id, path and hash.
- `includeMedia: "permitted"` copies only artifacts covered by a caller
  assertion with `owned`, `licensed` or `permission`, `scope: "export_copy"`
  and a non-empty reference. Unknown, missing, wrong-scope and restricted
  artifacts are excluded with a reason.
- Never claim legal permission on the user's behalf. Assertions are recorded,
  not verified.
- The pack is written under `<cache>/atlas/evidence-packs/<packId>/`. There is
  no arbitrary path, overwrite switch, downloader or sharing operation.
- An identical selection returns `cached: true`; a corrupt pack is preserved
  and returns `PACK_CORRUPT`.
- `references` mode is the safe default for agent work.

### 5. Maintenance

All actions require the flag and are mutually exclusive with the normal crawl:

```bash
AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas import
AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas capture --slug <slug> --viewport both
AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas reindex
AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas verify
AWWWARDS_MCP_ATLAS=1 awwwards-index --atlas prune --older-than-days 30
```

- `verify` is read-only: no cache creation, no migration, no WAL/SHM sidecar,
  no head withdrawal. A missing cache or a cache without Atlas tables exits 1.
- `prune` is dry-run by default. Add `--apply` only with explicit user
  authorisation. Active heads, pack-pinned captures, running captures, young
  captures and unsafe paths are protected.
- `reindex` rebuilds FTS and projections; it is revision-stable when nothing
  changed.
- `import` reads the local cache only and never captures.

Always set `AWWWARDS_CACHE_DIR` to a test directory when probing CLI behavior.
The CLI defaults to `~/.awwwards-mcp`; a typo silently uses the real cache.

## Reading results

All four tools return the `awwwards-atlas-v1` envelope:

- `ok` and `partial` carry data
- `inconclusive` carries resolved evidence when available, sometimes `null`
- `blocked` and `error` carry `data: null`, `isError: true`, and no
  `structuredContent`
- messages never include stacks or absolute paths

Report `coverage.status`, `coverage.limitations`, `omitted`, `candidateOnly`
and `candidateNote` rather than presenting a partial result as complete.

## Stop conditions

Stop and report instead of guessing when:

- the flag is off or the server version is below 1.19.0
- the slug is not in the local cache
- `robots.txt` is unavailable (5xx) or disallows the target
- the destination is private, loopback, metadata or reserved
- `CAPTURE_BUSY`, `CAPTURE_DEADLINE_EXCEEDED`, `NAVIGATION_FAILED` or
  `TARGET_CHANGED` occurs
- `seed`/import returns no regions and you cannot capture
- an export needs a region from another site, page root or a historical head
- rights are unknown and `includeMedia: "permitted"` was requested
- the user asks for accepted component-type precision; it is unmeasured

## Do not

- Do not present candidate labels as validated taxonomy.
- Do not claim 95% component precision or "F9 passed".
- Do not claim Atlas is stable, default-on or qualified offline.
- Do not bypass robots, private-address checks, the capture lease or the
  fixed evidence-pack directory.
- Do not copy third-party media without the caller's explicit rights basis.
- Do not prune with `--apply` without confirmation.
- Do not use `AWWARDS_` (two W); the flag is `AWWWARDS_MCP_ATLAS`.

## Full reference

The MCP repository carries the complete operator guide:

- `ATLAS.md` in https://github.com/INSANE0777/Awwwards-mcp
- `v2-routing.md` beside this skill for the 1.x -> v2 mapping
