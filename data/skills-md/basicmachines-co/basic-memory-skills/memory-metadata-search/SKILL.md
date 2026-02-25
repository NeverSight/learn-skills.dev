---
name: memory-metadata-search
description: "Structured metadata search for Basic Memory: query notes by custom frontmatter fields using equality, range, array, and nested filters. Use when finding notes by status, priority, confidence, or any custom YAML field rather than free-text content."
---

# Memory Metadata Search

Find notes by their structured frontmatter fields instead of (or in addition to) free-text content. Any custom YAML key in a note's frontmatter beyond the standard set (`title`, `type`, `tags`, `permalink`, `schema`) is automatically indexed as `entity_metadata` and becomes queryable.

## When to Use

- **Filtering by status or priority** — find all notes with `status: draft` or `priority: high`
- **Querying custom fields** — any frontmatter key you invent is searchable
- **Range queries** — find notes with `confidence > 0.7` or `score between 0.3 and 0.8`
- **Combining text + metadata** — narrow a text search with structured constraints
- **Tag-based filtering** — find notes tagged with specific frontmatter tags
- **Schema-aware queries** — filter by nested schema fields using dot notation

## Two Tools, Two Patterns

| Tool | Use When |
|------|----------|
| `search_by_metadata` | Metadata filters only, no text query needed |
| `search_notes` | Combining a text query with metadata filters |

Both accept the same filter syntax.

## Filter Syntax

Filters are a JSON dictionary. Each key targets a frontmatter field; the value specifies the match condition. Multiple keys combine with **AND** logic.

### Equality

```json
{"status": "active"}
```

### Array Contains (all listed values must be present)

```json
{"tags": ["security", "oauth"]}
```

### `$in` (match any value in list)

```json
{"priority": {"$in": ["high", "critical"]}}
```

### Comparisons (`$gt`, `$gte`, `$lt`, `$lte`)

```json
{"confidence": {"$gt": 0.7}}
```

Numeric values use numeric comparison; strings use lexicographic comparison.

### `$between` (inclusive range)

```json
{"score": {"$between": [0.3, 0.8]}}
```

### Nested Access (dot notation)

```json
{"schema.version": "2"}
```

### Quick Reference

| Operator | Syntax | Example |
|----------|--------|---------|
| Equality | `{"field": "value"}` | `{"status": "active"}` |
| Array contains | `{"field": ["a", "b"]}` | `{"tags": ["security", "oauth"]}` |
| `$in` | `{"field": {"$in": [...]}}` | `{"priority": {"$in": ["high", "critical"]}}` |
| `$gt` / `$gte` | `{"field": {"$gt": N}}` | `{"confidence": {"$gt": 0.7}}` |
| `$lt` / `$lte` | `{"field": {"$lt": N}}` | `{"score": {"$lt": 0.5}}` |
| `$between` | `{"field": {"$between": [lo, hi]}}` | `{"score": {"$between": [0.3, 0.8]}}` |
| Nested | `{"a.b": "value"}` | `{"schema.version": "2"}` |

**Rules:**
- Keys must match `[A-Za-z0-9_-]+` (dots separate nesting levels)
- Operator dicts must contain exactly one operator
- `$in` and array-contains require non-empty lists
- `$between` requires exactly `[min, max]`

## Using `search_by_metadata`

Metadata-only search. Results are scoped to entity-level items.

```python
# All notes with status "in-progress"
search_by_metadata(filters={"status": "in-progress"})

# High-priority specs in a specific project
search_by_metadata(
    filters={"type": "spec", "priority": {"$in": ["high", "critical"]}},
    project="research",
    limit=10,
)

# Notes with confidence above a threshold
search_by_metadata(filters={"confidence": {"$gt": 0.7}})

# Paginate through results
search_by_metadata(filters={"type": "meeting"}, limit=10, offset=20)
```

## Using `search_notes` with Metadata

Combine text search with structured filters by passing `metadata_filters`, `tags`, or `status` alongside the text `query`.

```python
# Text search narrowed by metadata
search_notes("authentication", metadata_filters={"status": "draft"})

# Filter-only (empty query string)
search_notes("", metadata_filters={"type": "spec"})

# Convenience shortcuts for tags and status
search_notes("planning", status="active")
search_notes("", tags=["security", "oauth"])

# Mix text, tag shortcut, and advanced filter
search_notes(
    "oauth flow",
    tags=["security"],
    metadata_filters={"confidence": {"$gt": 0.7}},
)
```

**Merging rules:** `tags` and `status` are convenience shortcuts merged into `metadata_filters` via `setdefault`. If the same key exists in `metadata_filters`, the explicit filter wins.

## Tag Search Shorthand

The `tag:` prefix in a query converts to a tag filter automatically:

```python
# These are equivalent:
search_notes("tag:tier1")
search_notes("", tags=["tier1"])

# Multiple tags (comma or space separated) — all must match:
search_notes("tag:tier1,alpha")
```

## Example: Custom Frontmatter in Practice

A note with custom fields:

```markdown
---
title: Auth Design
type: spec
tags: [security, oauth]
status: in-progress
priority: high
confidence: 0.85
---

# Auth Design

## Observations
- [decision] Use OAuth 2.1 with PKCE for all client types #security
- [requirement] Token refresh must be transparent to the user

## Relations
- implements [[Security Requirements]]
```

Queries that find it:

```python
# By status and type
search_by_metadata(filters={"status": "in-progress", "type": "spec"})

# By numeric threshold
search_by_metadata(filters={"confidence": {"$gt": 0.7}})

# By priority set
search_by_metadata(filters={"priority": {"$in": ["high", "critical"]}})

# By tag shorthand
search_notes("tag:security")

# Combined text + metadata
search_notes("OAuth", metadata_filters={"status": "in-progress"})
```

## Guidelines

- **Use metadata search for structured queries.** If you're looking for notes by a known field value (status, priority, type), metadata filters are more precise than text search.
- **Use text search for content queries.** If you're looking for notes *about* something, text search is better. Combine both when you need precision.
- **Custom fields are free.** Any YAML key you put in frontmatter becomes queryable — no schema or configuration required.
- **Multiple filters are AND.** `{"status": "active", "priority": "high"}` requires both conditions.
- **Prefer `search_by_metadata` for filter-only queries.** It's purpose-built and returns entity-level results. Use `search_notes` with empty query only when you also need text search features.
- **Dot notation for nesting.** Access nested YAML structures with dots: `{"schema.version": "2"}` queries the `version` key inside a `schema` object.
- **Tags shortcut is convenient but limited.** `tags` and `status` are sugar for common fields. For anything else, use `metadata_filters` directly.
