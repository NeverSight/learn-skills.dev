---
name: neo4j-ontology-skill
description: Author and validate Neo4j Ontology Graph Specification (ontology graph spec)
  documents. Use when writing or editing an ontology, defining nodes and relationships with
  properties, Neo4jType data types, constraints (key/unique/must_exist), labels, and endpoint
  cardinality, in YAML or JSON, or validating an ontology document against the live-resolved
  spec schema. Does NOT handle Cypher or loading an ontology into a database — use
  neo4j-cypher-skill. Does NOT cover generic graph data modeling advice — use
  neo4j-modeling-skill.
compatibility: uv required to run scripts/validate.py (PEP 723 inline deps)
version: 1.0.1
---

## When to Use

- Authoring an ontology document (Neo4j Ontology Graph Specification) from a domain description
- Editing existing ontology YAML/JSON: nodes, relationships, properties, types, constraints, cardinality, extensions
- Validating an ontology document against the spec schema

## When NOT to Use

- **Cypher queries, or loading/applying an ontology into a database** → `neo4j-cypher-skill` (ontology Cypher procedures do not exist yet — later work there)
- **Generic graph modeling advice (node vs property vs label, anti-patterns, supernodes)** → `neo4j-modeling-skill`

---

## Authoring Workflow

### Step 1 — Gather domain intent

Identify what is being modeled: entity types (nodes), connections (relationships + direction), properties per element, identifying keys, mandatory fields, cardinality. If the domain or required shape is unclear, ask the user what is being modeled and which questions the ontology must answer. Do NOT guess a domain.

### Step 2 — Draft the document

YAML or JSON per user preference; default YAML (more readable). Apply the Core Facts below. Load [references/format-reference.md](references/format-reference.md) when anything beyond the minimal example is needed (full `labels` object, constraint objects, extensions, full data-type grammar).

### Step 3 — Validate

```bash
# From the skill directory:
uv run scripts/validate.py <document.{yaml,yml,json}>
# From the repo root:
uv run neo4j-ontology-skill/scripts/validate.py <document.{yaml,yml,json}>
```

Exit 0 = valid · exit 1 = schema violations (one line per field path) · exit 2 = parse/read/fetch error. PEP 723 script — `uv` resolves deps (jsonschema, pyyaml) itself.

The validator fetches the schema live — nothing is vendored. Resolution order: `--schema <path-or-url>` (explicit, no fallback) → the document's own `schema` field when it is a URL → the published `current` alias → transitional repo raw fallback. The document's `schema` URL decides which version it validates against: set it to the published versioned URL of the version being authored (older versions validate against their published schema).

### Step 4 — Fix and re-validate

Fix every reported error; re-run Step 3. Repeat until exit 0. Validation is MANDATORY — never present an ontology as done with a non-zero exit.

---

## Core Facts

- Required root fields: `schema`, `id` (unique ontology id string), `version` (STRING — user-defined revision label; quote it in YAML: `version: "1"`). Root rejects unknown fields (`additionalProperties: false`).
- `schema` value: the published URL of the version being authored, e.g. `https://neo4j.com/docs/ontology-graph-spec/1.0.0/schema.json`. Root key is plain `schema`, NOT `$schema`.
- `nodes` / `relationships` are maps keyed by LOCAL IDS, not labels/types. Label lives in `label` or `labels.identifier`; relationship type lives in `type`. Endpoints reference node ids (`from.node` / `to.node`) — label renames never break references.
- `label: X` is shorthand for `labels: {identifier: X}`. Use the full `labels` object only when `implied` or `optional` labels exist.
- Type tokens come from the Neo4jType enum exactly — case-sensitive. Tokens incl. `STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`, `DATE`, `DURATION`, `POINT`, `UUID`; temporal tokens contain a space (`ZONED DATETIME`, `LOCAL TIME`); parameterized tokens use angle brackets (`LIST<STRING>`, `VECTOR<FLOAT32>`). `UUID` and `VECTOR<...>` have no LIST arm. No unions, no nested lists. `dimension` (integer|null) sits on the property, paired with VECTOR types.
- Constraints — two forms:
  - Flags on a property: `key: true`, `unique: true`, `must_exist: true` (snake_case — NOT `mustExist`). Single-property shorthands; `key` = unique + exists per Neo4j key-constraint semantics.
  - Object form: `constraints` is a MAP id → constraint object `{type: EXISTS|KEY|PROPERTY_TYPE|UNIQUE, properties: [p1, ...], name: optional}` — required for composites (≥ 2 properties) and nameable constraints. `properties` must name properties declared on the SAME element.
- Endpoint cardinality: `count` exact, or `min_count`/`max_count` ranged; absent = unconstrained (0..*).
- Extensions: fixed `extensions` shape per element — node: `indexes`/`display`/`custom`; relationship: `indexes`/`custom`; root: `tables`/`mappings`/`custom`; labels/property/constraint/index: `custom` only. Unknown extension keys rejected. `custom` is free-form — arbitrary owner data, never validated by the spec schema.
- Absent means none — never write empty maps/lists (`properties: {}`, `aliases: []`, `custom: {}`); omit them.

## Minimal Example

`library.ontology.yaml` — 2 nodes, 1 relationship:

```yaml
schema: "https://neo4j.com/docs/ontology-graph-spec/1.0.0/schema.json"
id: library
version: "1"
name: Library
nodes:
  author:
    label: Author
    properties:
      id: { type: STRING, key: true }
      name: { type: STRING, must_exist: true }
  book:
    label: Book
    properties:
      isbn: { type: STRING, key: true }
relationships:
  wrote:
    type: WROTE
    from: { node: author, max_count: 1 }
    to: { node: book }
```

Validates exit 0 via `scripts/validate.py`. Full YAML+JSON worked examples in [references/format-reference.md](references/format-reference.md).

---

## References

Load on demand:

- [references/format-reference.md](references/format-reference.md) — full field reference: every node/relationship/property/endpoint field, `labels` object, constraint objects, extension shapes, data-type grammar, gotchas, YAML+JSON examples
- Published schema base: `https://neo4j.com/docs/ontology-graph-spec/` — immutable `/<version>/schema.json` per spec version, moving alias `/current/schema.json`

## Spec Status

Published: the ONT-31 URLs above are live and are the canonical schema source. If the published host is unreachable, the validator falls back to the raw schema from `neo4j/ontology-graph-spec` main (moving). Ontology Cypher procedures do not exist yet; applying an ontology to a database is out of scope here.

---

## Checklist

- [ ] Root fields `schema`, `id`, `version` present; `version` a quoted string; `schema` = the published versioned URL under plain `schema` key
- [ ] No unknown root fields; no `$schema`
- [ ] `nodes`/`relationships` keyed by local ids; relationship `from`/`to` reference node ids
- [ ] Every node has `label` or `labels.identifier`
- [ ] Type tokens exact from the Neo4jType enum (case-sensitive; spaced temporal tokens); `dimension` on the property with VECTOR types
- [ ] Flags only for single-property constraints; object form (`type` ∈ EXISTS/KEY/PROPERTY_TYPE/UNIQUE) for composites/named; constraint `properties` exist on the same element
- [ ] Extension keys match the element's fixed shape; arbitrary data only under `custom`
- [ ] No empty maps/lists written
- [ ] `uv run scripts/validate.py <file>` exits 0 (every reported error fixed and re-validated)
