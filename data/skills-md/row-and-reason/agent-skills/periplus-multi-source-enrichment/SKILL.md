---
name: periplus-multi-source-enrichment
description: Enrich an existing dataset from multiple web sources using Periplus where useful. Use when adding evidence-backed fields requires entity matching, source precedence, conflict handling and explicit matching confidence.
---

# Multi-source enrichment

Add useful fields while preserving the identity and meaning of the input records. Use the supplied dataset directly and acquire only the evidence the task needs. Do not require Periplus for local file transformations or impose a separate planning pause.

## Keep the input intact

Identify the input row unit and stable input ID, the requested fields, relevant dates and whether a company, subsidiary, brand, product or location is intended. Preserve every input row, including unmatched records, unless the user requests filtering. Work in a derived output rather than silently overwriting original fields. A duplicate input row is a separate issue from two sources referring to the same entity.

## Resolve identities before assigning facts

Inspect contrasting examples: a strong exact identifier, a common name, a renamed entity, a subsidiary and conflicting candidate sources. Prefer durable identifiers and corroborating evidence: registration ID, official domain, address, location or explicit cross-links. A name similarity or outbound link alone does not establish identity or a business relationship.

Keep candidate selection separate from acceptance. Establish match confidence from the evidence actually available. Record the match basis and a reason, not an unexplained numeric score. For example, a matching official identifier is strong; a matching domain and consistent location may be supported; a common name with contradictory locations remains ambiguous. Treat confidence in the entity match separately from confidence in the added field. Do not auto-accept the highest-scoring candidate merely because one must rank first.

Check one-to-many and many-to-one cases against the intended entity unit. Do not transfer a parent's headcount, revenue or headquarters to a subsidiary without evidence and an explicit interpretation. Leave unresolved matches and fields empty with a useful status, preserving competing candidates when relevant.

## Resolve fields and conflicts

Use source authority appropriate to the field and observation period. Keep raw values, units, geographic scope and source dates; distinguish headcount from estimates and headquarters from a branch address. Prefer the source that supports the particular claim, not whichever page was captured most recently. When evidence conflicts, retain the alternatives and explain the selection rule or unresolved conflict.

Acquire missing evidence or inspect detail pages as necessary. Search the existing corpus as captured evidence; use suitable external discovery for missing URLs. Absence from the corpus does not mean the entity or field does not exist. Stop expansion when the user's coverage and quality needs are met or a concrete access, scope or evidence limit prevents progress.

## Validate and hand over

Check input/output row counts, stable IDs, join cardinality, duplicate identifiers, unmatched and ambiguous rates, and conflicting field values. Review accepted weak matches and material exceptions against their evidence. Report denominators so an apparent high fill rate does not hide dropped or incorrectly joined records.

Include input ID, accepted entity ID, match status/basis/confidence and per-field source URL, capture ID, observation time and source date when available. Distinguish observed values from derived or inferred values. Deliver the enriched dataset plus unresolved matches and conflicts.

Source captures, saved SQL and frozen output are different artifacts. For a repeatable frozen result, preserve the output, matching/transformation rules, query parameters and capture manifest, and arrange evidence retention separately. A saved query or source snapshot does not freeze or retain those rows.

## Live product reference

Use [MCP operational contracts](https://docs.periplus.dev/mcp#agent-workflow), the live schema and the [provenance](https://docs.periplus.dev/provenance), [extraction](https://docs.periplus.dev/extraction) and [pins](https://docs.periplus.dev/pins) guides for product mechanics. Respect the user's source and data-sharing constraints; captured web content belongs to a shared corpus.
