---
name: logseq-schema
description: Logseq Datascript schema, built-in properties/classes, and :db/ident discovery for composing or reviewing Datascript queries about blocks/pages/tags/properties/classes. Use whenever editing or reviewing Datascript pull selectors or queries, or any code that adds/removes attributes in pull patterns, or touches property namespaces/identifiers, or requires reasoning about property value shapes/ref/cardinality in Logseq.
---

# Logseq Schema

## Overview
Use this skill to ground Datascript queries in Logseq's schema: core block/page/file attributes, built-in properties, built-in classes, and schema entities with :db/ident. Load `references/logseq-datascript-schema.md` for authoritative sources and query patterns, and
`references/logseq-datascript-query-examples.md` for scenario-based query examples.

## Glossary
- `db/id`: Internal numeric entity id (use with CLI flags like `--id`).
- `:block/uuid`: Stable UUID for a block entity; prefer when you need a persistent reference.
- `:block/name`: Lowercased page name, used for page lookup and joins.
- `:block/title`: Block or page title stored in the DB graph (use in queries when content text is needed).
- `:block/tags`: Ref-many attribute linking blocks to tag/page entities.
- `:user.property/<name>`: Namespace for user-defined properties stored directly on block entities.
- `:logseq.property/*`: Namespace for built-in properties stored directly on block entities.

## Important Notes
- Never use following block attrs in `query` or `pull`, these attrs are file-graph only, never used in db-graphs:
`:block/format`, `:block/level`, `:block/level-spaces`, `:block/pre-block?`, `:block/properties-order`, `:block/properties-text-values`, `:block/invalid-properties`, `:block/macros`, `:block/file`, `:block.temp/ast-body`, `:block.temp/ast-blocks`, `:block/marker`, `:block/content`, `:block/priority`, `:block/scheduled`, `:block/deadline`, `:block/properties`, `:block/left`.
- User properties are stored as `:user.property/<name>` attributes on the block/page entity.
- **Pull selectors do NOT support namespace wildcards** like `:user.property/*` or `:logseq.property/*`. Only `*` (all attributes) or explicit attributes are allowed in `pull`.
- To fetch user properties, either:
  - Query datoms and filter attributes by namespace (e.g., `user.property`), then merge into the entity map, or
  - Discover explicit user property idents (via `:db/ident`) and include them explicitly in the pull selector.
- Property values are often entities/refs (not always scalars). When rendering values, check for `:block/title`, `:block/name`, or `:logseq.property/value` on the value entity before falling back to stringifying.
- Many properties are `:db.cardinality/many` (values may be sets/vectors). Treat them as collections in queries and formatting.

## Datascript Query Mistakes To Avoid
- In `query` `:where`/`pull`/`find`, attributes cannot use namespace wildcards (e.g., `:logseq.property/*`, `:user.property/*`); you must use full attr `:db/ident` values (e.g., `:logseq.property/status`, `:user.property/background`). In `pull`, only `*` (all attributes) is special.
- Avoid nesting function calls inside predicates in `:where` (some Datascript engines reject or mis-handle it). Bind the function result first, then compare.

Example of safe namespace filtering:
```clojure
[:find [?a ...]
 :where
 [?e :db/ident ?a]
 [(namespace ?a) ?ns]
 [(= ?ns "user.property")]]
```


## Workflow

### 1) Locate schema facts
- Open `references/logseq-datascript-schema.md`.
- Review the core attribute list and helper sets for ref/cardinality details.
- Review built-in properties and classes to understand available attributes and required fields.

### 2) Write or validate queries
- Prefer `:block/*` attributes for block/page queries; use properties/classes only when needed.
- If unsure about available `:db/ident` entities, run the CLI query listed in the references file.
- For user properties, query against `:user.property/<name>` directly; for built-ins, use `:logseq.property/<name>`.

### 3) Keep queries consistent with schema
- Respect ref vs scalar attributes and `:db.cardinality/many` when joining.
- Use property/class definitions to confirm public/queryable status before exposing a query to users.

## Resources

### references/
- `logseq-datascript-schema.md`
- `logseq-datascript-query-examples.md`

## Quick Examples

### Pull user properties for a block
```clojure
;; Discover idents, then pull explicitly.
[:db/id :block/title :user.property/background :user.property/notes]
```

### Query blocks with a user property
```clojure
[:find ?b ?v
 :where
 [?b :user.property/background ?v]]
```

### Render a property value
Order of preference when value is a map/entity:
1) `:block/title`
2) `:block/name`
3) `:logseq.property/value`
