---
name: skos-taxonomy
displayName: SKOS Taxonomist
description: Design, apply, and maintain SKOS taxonomies for joelclaw agent workflows. Use when defining concept schemes, classifying agent inputs/outputs, mapping to external vocabularies, or integrating taxonomy metadata with Typesense retrieval.
version: 0.1.0
author: Joel Hooks
tags: [joelclaw, skos, taxonomy, agents, typesense, retrieval, knowledge]
---

# SKOS Taxonomist

Design operational taxonomies with SKOS so Panda and all sub-agents classify work consistently, retrieve better context, and avoid tag soup.

This skill is for execution, not theory: define concepts, classify agent data, validate constraints, and wire taxonomy fields into Typesense.

## When to Use

Use this skill when any request involves:

- "taxonomy", "SKOS", "controlled vocabulary", "concept scheme"
- classifying agent interactions, runs, docs, memory, events, or tasks
- designing or revising `concept_ids` / `primary_concept_id` contracts
- mapping joelclaw concepts to another vocabulary
- deciding whether SKOS is needed or a simpler tag model is enough

## Primary Outcomes

1. A versioned SKOS concept scheme with stable concept URIs.
2. Agent-classification rules that produce deterministic concept metadata.
3. Typesense field mappings that support lexical, faceted, and hybrid retrieval.
4. Governance rules for candidate concepts, alias drift, deprecation, and mappings.

## Non-Negotiable SKOS Rules (Normative)

Follow these in every scheme:

1. `skos:Concept` and `skos:ConceptScheme` are distinct classes.
2. `skos:broader` is **not** transitive; use transitive super-property semantics (`skos:broaderTransitive`) for closure queries.
3. `skos:prefLabel` max one value per language tag for a resource.
4. `skos:prefLabel`, `skos:altLabel`, and `skos:hiddenLabel` are pairwise disjoint for the same resource+language form.
5. `skos:related` is disjoint with `skos:broaderTransitive`.
6. Mapping relations are for cross-scheme linking. `skos:exactMatch` is transitive and should be used sparingly.
7. `skos:closeMatch` is intentionally non-transitive.
8. `skos:Collection` / `skos:OrderedCollection` are for grouping; they are disjoint with `skos:Concept`.

If any of these fail, stop and fix data before rollout.

## JoelClaw Operational Scheme (Workload v1)

Define a dedicated scheme for workload classification:

- Scheme URI: `joelclaw:scheme:workload:v1`
- Taxonomy version string: `workload-v1`
- Concept URI pattern: `joelclaw:concept:<top-level>[:<subconcept>]`
- Notation style: upper snake or dotted operational codes (stable and immutable)

### Top-Level Concepts (Required)

| Notation | URI | Purpose |
|---|---|---|
| `PLATFORM` | `joelclaw:concept:platform` | Runtime/platform infrastructure and hosting substrate |
| `INTEGRATION` | `joelclaw:concept:integration` | External system connections, APIs, webhooks, adapters |
| `TOOLING` | `joelclaw:concept:tooling` | CLI/dev tooling, operator commands, local automation |
| `PIPELINE` | `joelclaw:concept:pipeline` | Inngest/event workflows, ingestion and processing chains |
| `BUILD` | `joelclaw:concept:build` | Code implementation, tests, CI/CD, packaging |
| `KNOWLEDGE` | `joelclaw:concept:knowledge` | Docs, memory, taxonomy, retrieval context |
| `COMMS` | `joelclaw:concept:comms` | Messaging channels, notifications, agent/user communication |
| `OBSERVE` | `joelclaw:concept:observe` | OTEL/logging/metrics/diagnostics/reliability telemetry |
| `META` | `joelclaw:concept:meta` | Governance, ADRs, policies, lifecycle and process controls |

### Core Turtle Skeleton

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix jcw: <joelclaw:> .

jcw:scheme:workload:v1 a skos:ConceptScheme ;
  skos:prefLabel "JoelClaw Workload Taxonomy v1"@en ;
  skos:definition "Operational workload taxonomy for Panda and sub-agents."@en ;
  skos:hasTopConcept
    jcw:concept:platform,
    jcw:concept:integration,
    jcw:concept:tooling,
    jcw:concept:pipeline,
    jcw:concept:build,
    jcw:concept:knowledge,
    jcw:concept:comms,
    jcw:concept:observe,
    jcw:concept:meta .

jcw:concept:pipeline a skos:Concept ;
  skos:inScheme jcw:scheme:workload:v1 ;
  skos:topConceptOf jcw:scheme:workload:v1 ;
  skos:notation "PIPELINE" ;
  skos:prefLabel "Pipeline"@en ;
  skos:altLabel "workflow"@en, "event flow"@en ;
  skos:definition "Durable event-driven processing sequences."@en ;
  skos:scopeNote "Use for Inngest functions, ingest chains, and orchestration logic."@en ;
  skos:narrower jcw:concept:pipeline:ingest, jcw:concept:pipeline:enrichment ;
  skos:related jcw:concept:observe, jcw:concept:build .
```

## Agent Classification Contract

Every sub-agent output that can be stored/retrieved must emit:

- `primary_concept_id` (single canonical concept URI)
- `concept_ids` (ordered list: primary first, then secondary)
- `taxonomy_version`
- `concept_source` (`rules|llm|backfill|manual|fallback`)
- `classification_confidence` (0-1 float, optional but recommended)

Recommended envelope:

```json
{
  "primary_concept_id": "joelclaw:concept:pipeline:ingest",
  "concept_ids": [
    "joelclaw:concept:pipeline:ingest",
    "joelclaw:concept:knowledge",
    "joelclaw:concept:observe"
  ],
  "taxonomy_version": "workload-v1",
  "concept_source": "rules",
  "classification_confidence": 0.88
}
```

### Classification Procedure

1. Normalize candidate labels (`trim`, lowercase, slugify, punctuation collapse).
2. Match against `prefLabel`, then `altLabel`, then `hiddenLabel` alias tables.
3. Disambiguate using `scopeNote` and neighboring concepts (`broader`, `related`).
4. Emit one primary concept plus optional secondary concepts.
5. If unresolved, map to a controlled fallback concept and log unmapped labels.
6. Emit OTEL metadata for mapping diagnostics (`mapped_count`, `unmapped_count`, `taxonomy_version`).

## SKOS-XL (When Labels Need First-Class Metadata)

Use SKOS-XL only when label objects need metadata or relationships:

- acronym/abbreviation management with provenance
- per-label source attribution
- multilingual/transliteration workflows with label-level auditing
- label-to-label relationships (deprecated term -> replacement term)

If labels are plain synonyms only, stay with core SKOS labels.

### SKOS-XL Example

```turtle
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix jcw: <joelclaw:> .

jcw:label:comms:imessage a skosxl:Label ;
  skosxl:literalForm "iMessage"@en .

jcw:concept:comms:imessage skosxl:altLabel jcw:label:comms:imessage .
```

## Mapping to External Vocabularies

Use mapping properties across schemes, not inside one scheme:

- `skos:exactMatch`: interchangeable meaning (rare, high bar)
- `skos:closeMatch`: near-equivalent, safe default for most interop
- `skos:broadMatch` / `skos:narrowMatch`: granularity mismatch
- `skos:relatedMatch`: associative cross-scheme link

### Internal Cross-Scheme Example (Workload -> Existing Docs Scheme)

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix jcw: <joelclaw:> .
@prefix jcd: <jc:> .

jcw:concept:build skos:closeMatch jcd:docs:programming .
jcw:concept:observe skos:broadMatch jcd:docs:operations .
jcw:concept:knowledge skos:relatedMatch jcd:docs:education .
```

Mapping guardrails:

1. Start with `closeMatch`; escalate to `exactMatch` only with explicit review.
2. Do not chain `exactMatch` blindly across multiple schemes.
3. Review inferred collisions caused by transitive/symmetric mapping behavior.

## Collections and Ordered Collections

Use collections for non-hierarchical grouping:

- `skos:Collection` for thematic bundles (example: all communication channels)
- `skos:OrderedCollection` for deterministic sequences (example: escalation stages)

Do not encode hierarchy with collections. Use `broader`/`narrower` for taxonomy structure.

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix jcw: <joelclaw:> .

jcw:collection:comms-channels a skos:Collection ;
  skos:prefLabel "Comms channels"@en ;
  skos:member
    jcw:concept:comms:telegram,
    jcw:concept:comms:slack,
    jcw:concept:comms:imessage .
```

## URI and Notation Policy (`joelclaw:`)

1. URI local parts are lowercase kebab or colon-separated operational paths.
2. `skos:notation` is immutable once released.
3. Never repurpose a concept URI. Deprecate old URI and add mappings.
4. Keep human names in labels, not in IDs.
5. Encode scheme version in scheme URI and metadata, not in every concept URI unless required.

Recommended patterns:

- `joelclaw:scheme:workload:v1`
- `joelclaw:concept:observe:otel`
- `joelclaw:collection:agent-lifecycle`
- `joelclaw:label:meta:adr`

## Typesense Integration Contract

Treat SKOS as source-of-truth semantics and Typesense as retrieval runtime.

### Field Mapping

| SKOS | Typesense field | Type | Notes |
|---|---|---|---|
| Concept URI | `id` | `string` | Canonical identifier |
| `skos:inScheme` | `scheme_id` | `string` facet | Filter by scheme/version |
| `skos:notation` | `notation` | `string` facet | Operational code lookups |
| `skos:prefLabel` | `pref_label` | `string` | Primary lexical form |
| `skos:altLabel` | `alt_labels` | `string[]` | Alias lookup/query expansion |
| `skos:hiddenLabel` | `hidden_labels` | `string[]` | Misspelling/legacy term recovery |
| `skos:definition` | `definition` | `string` | Long-form semantic context |
| `skos:scopeNote` | `scope_note` | `string` | Disambiguation guidance |
| `skos:broader` | `broader_ids` | `string[]` facet | Direct parents |
| `skos:narrower` | `narrower_ids` | `string[]` facet | Direct children |
| `skos:related` | `related_ids` | `string[]` facet | Lateral associations |
| Mapping props | `exact_match_ids`, `close_match_ids`, etc. | `string[]` | Cross-scheme links |
| Version/governance | `taxonomy_version`, `state` | `string` facet | Rollout control |

For retrievable entities (docs, memory, events), also persist:

- `primary_concept_id`
- `concept_ids` (`string[]`, faceted)
- `concept_source`
- `taxonomy_version`
- `context_prefix`, `source_entity_id`, `evidence_tier`, `parent_evidence_id` (where applicable)

### Query Patterns

Classification candidate lookup:

```bash
curl -s "http://localhost:8108/collections/taxonomy_concepts/documents/search?q=ingest+pipeline&query_by=pref_label,alt_labels,scope_note,definition&per_page=10" \
  -H "X-TYPESENSE-API-KEY: panda-typesense-key"
```

Concept-constrained retrieval:

```bash
curl -s "http://localhost:8108/collections/documents/documents/search?q=*&query_by=content&filter_by=concept_ids:=[joelclaw:concept:pipeline] && taxonomy_version:=workload-v1&per_page=20" \
  -H "X-TYPESENSE-API-KEY: panda-typesense-key"
```

Operational notes:

1. Use `q=*` when filtering/faceting without lexical query terms.
2. Keep concept fields faceted for fast filters and diagnostics.
3. Synonyms operate on `q` tokens, not `filter_by` values; concept IDs must be canonical.
4. For transitive hierarchy retrieval, precompute ancestor closures into a dedicated field (example: `ancestor_concept_ids`).

### Local Access Troubleshooting

If `localhost:8108` is unreachable, port-forward first:

```bash
kubectl port-forward -n joelclaw svc/typesense 8108:8108
```

## Quality Gates and Validation

Run these checks before shipping taxonomy changes:

1. Label integrity:
   - one `prefLabel` per language per concept
   - no overlap among pref/alt/hidden labels
2. Structural integrity:
   - every concept in exactly one expected scheme (or explicit multi-scheme design)
   - no accidental hierarchy cycles
   - `broader` and `narrower` coherence
3. Mapping integrity:
   - mapping links only target external scheme concepts
   - `exactMatch` reviewed and justified
4. Runtime integrity:
   - `concept_ids` coverage target met (>=95% for new records)
   - unmapped labels observable in OTEL

Recommended operational probes:

- `joelclaw otel search "concept_ids|primary_concept_id|taxonomy_version" --hours 24`
- `joelclaw recall "<query>" --category <mapped-category>`
- `joelclaw docs search "<query>" --concept <concept-uri>`

## Governance Workflow

1. Propose concept as `candidate` with `scopeNote`, not canonical.
2. Check collisions against existing labels and aliases.
3. Validate impact on classifier rules and retrieval filters.
4. Promote to `canonical` only after review and observed usage.
5. Deprecate by state transition + mapping hints, never by URI reuse.
6. Version changes explicitly (`workload-v1` -> `workload-v2`) with migration notes.

## Anti-Patterns

Do not do these:

1. "Tag soup" growth: free-form tags affecting retrieval without concept mapping.
2. Using `exactMatch` as a convenience synonym.
3. Treating collection membership as hierarchy.
4. Building deep trees without retrieval use-cases.
5. Skipping `scopeNote` then trying to fix ambiguity downstream with prompts only.

## When SKOS Is Overkill

Use a simpler tagging/enum model when all are true:

1. Fewer than ~30 stable labels.
2. No hierarchy/mapping requirements.
3. No multilingual or alias governance needs.
4. Labels are not reused across systems.
5. Retrieval quality does not depend on concept semantics.

If any of those stop being true, migrate to SKOS before scaling.

## Research-Derived Operational Guidance

Use SKOS metadata to improve retrieval quality in agent pipelines:

1. Metadata-aware retrieval pipelines can materially improve multi-hop QA accuracy (for example, reported F1/EM gains in Multi-Meta-RAG benchmarks).
2. Controlled vocabularies plus free text generally improve precision/recall versus text-only querying in domain IR studies.
3. Practical implication for joelclaw: always combine lexical/vector retrieval with concept filtering or re-ranking signals when classification confidence is high.

## References

- W3C SKOS home: https://www.w3.org/2004/02/skos/
- W3C SKOS Reference (normative): https://www.w3.org/TR/skos-reference/
- W3C SKOS Primer: https://www.w3.org/TR/skos-primer/
- W3C SKOS Use Cases and Requirements: https://www.w3.org/TR/skos-ucr/
- Typesense collections API: https://typesense.org/docs/30.1/api/collections.html
- Typesense search API: https://typesense.org/docs/30.1/api/search.html
- Typesense vector search: https://typesense.org/docs/30.1/api/vector-search.html
- Typesense synonyms: https://typesense.org/docs/30.1/api/synonyms.html
- Multi-Meta-RAG (metadata-aware RAG): https://arxiv.org/abs/2406.13213
- Controlled vocabulary + text query expansion study (PubMed): https://pubmed.ncbi.nlm.nih.gov/21893678/
- Hybrid controlled vocabulary + text retrieval study (PubMed): https://pubmed.ncbi.nlm.nih.gov/23459623/
