---
name: open-knowledge-format
description: >-
  Define knowledge bundles with Google's Open Knowledge Format (OKF) v0.1. Use when the
  user mentions OKF, Open Knowledge Format, Google's knowledge format, LLM wiki bundles,
  agent knowledge packs, creating OKF bundles, validating OKF documents, or converting
  knowledge into the OKF standard. Do not use this skill for unrelated requests; route to
  the nearest named specialist.
license: MIT
compatibility: Portable across any AgentSkills-compatible harness. The validation
  script requires Python 3.8+ with PyYAML (pip install PyYAML). All examples use standard
  markdown — readable in any editor or terminal.
metadata:
  spec-version: '1.0'
  skills: okf, open-knowledge-format, knowledge-format, agent-knowledge, llm-wiki
  tags: okf, knowledge-format, google, ai-agents, markdown, knowledge-management
---

# Open Knowledge Format (OKF) — v0.1

Google Cloud published the [Open Knowledge Format v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/) on **June 12, 2026** — an open specification that formalizes the [LLM-wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) into a portable, vendor-neutral format for AI agent knowledge.

**The design is intentionally minimal:** a directory of markdown files with YAML frontmatter. No schema registry, no central authority, no required tooling.

> "If you can `cat` a file, you can read OKF; if you can `git clone` a repo, you can ship it."

## Core Concepts

| Concept | Definition |
|---------|------------|
| **Knowledge Bundle** | A self-contained directory tree of markdown files. The unit of distribution. |
| **Concept** | A single unit of knowledge — one markdown file. May describe a table, a metric, a playbook, an API, or any idea. |
| **Concept ID** | The file path with `.md` stripped (e.g. `tables/users.md` has ID `tables/users`). |
| **Frontmatter** | YAML block at the top of each file with structured metadata. |
| **Body** | Standard markdown content after the frontmatter. |
| **Link** | A markdown link from one concept to another — expresses relationships. |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Spec summary | You need the full OKF v0.1 specification, conformance criteria, and field definitions | `references/spec-summary.md` |
| Bundle architecture | You're creating or structuring an OKF bundle — directory layout, index files, cross-linking conventions | `references/bundle-architecture.md` |
| Use cases | You need real-world examples, third-party implementations, and adoption patterns | `references/use-cases.md` |

## Scripts

| Script | Purpose | Load when |
|--------|---------|-----------|
| `okf-bundle-validate.py` | Validate an OKF bundle directory — checks frontmatter, required fields, reserved filenames, and cross-link integrity | You've created or modified an OKF bundle and want to verify conformance |

## Assets

| Asset | Purpose | Path |
|-------|---------|------|
| Concept template | A template markdown file with all recommended frontmatter fields and body sections | `assets/concept-template.md` |
| Example bundle | A minimal but complete OKF bundle showing directory structure, index files, and cross-linked concepts | `assets/example-bundle/` |

## Bundle Structure

```
path/to/bundle/
├── index.md                      # Optional. Directory listing for progressive disclosure.
├── log.md                        # Optional. Chronological update history.
├── <concept>.md                  # A concept at the bundle root.
└── <subdirectory>/               # Subdirectories organize concepts into groups.
    ├── index.md
    ├── <concept>.md
    └── <subdirectory>/
        └── …
```

Files named `index.md` and `log.md` are **reserved** — they have defined semantics and must not be used for concept documents.

## Frontmatter Fields

```yaml
---
type: <Type name>                  # REQUIRED
title: <Optional display name>
description: <Optional one-line summary>
resource: <Optional canonical URI for the underlying asset>
tags: [<tag>, <tag>, …]            # Optional
timestamp: <ISO 8601 datetime>     # Optional last-modified time
# … other producer-defined key/value pairs
---
```

**Required:** `type` — a short string identifying the kind of concept. Types are NOT registered centrally. Producers pick descriptive values; consumers tolerate unknown types gracefully.

**Conventional body sections:**

| Heading | Purpose |
|---------|---------|
| `# Schema` | Structured description of an asset's columns/fields |
| `# Examples` | Concrete usage examples, often as code blocks |
| `# Citations` | External sources backing claims in the body |

## Cross-linking

Concepts link to each other via standard markdown links:

- **Absolute (bundle-relative):** Begin with `/`, relative to bundle root. Recommended — stable when documents move.
- **Relative:** Standard markdown relative paths.

A link from concept A to concept B asserts a relationship. The specific kind (references, depends-on, joins-with) is conveyed by the surrounding prose, not by the link syntax.

**Consumers MUST tolerate broken links** — a link whose target doesn't exist is not malformed; it may represent not-yet-written knowledge.

## Conformance

A bundle is **conformant** with OKF v0.1 if:

1. Every non-reserved `.md` file contains parseable YAML frontmatter
2. Every frontmatter block contains a non-empty `type` field
3. Reserved filenames (`index.md`, `log.md`) follow their defined structure

**Consumers MUST NOT reject a bundle for:** missing optional frontmatter fields, unknown `type` values, unknown frontmatter keys, broken cross-links, or missing `index.md` files.

## Relationship to Other Formats

| Format | How OKF Differs |
|--------|----------------|
| **Karpathy's LLM Wiki** | OKF specifies the interoperability surface — required fields, reserved filenames, conformance criteria |
| **Obsidian / Notion vaults** | OKF is format-only — no tooling, no runtime, no UI. Any editor works |
| **AGENTS.md / CLAUDE.md** | OKF is multi-file, hierarchical, cross-linked — not a single convention file |
| **Metadata-as-code repos** | OKF standardizes the file format so different producers and consumers interoperate |
| **Domain schemas (Avro, Protobuf, OpenAPI)** | OKF references them — it does not subsume or replace them |

## Quick Start

```bash
# 1. Create a bundle directory
mkdir my-knowledge && cd my-knowledge

# 2. Create a concept file
cat > datasets/sales.md << 'EOF'
---
type: BigQuery Dataset
title: Sales
description: All sales-related tables for the retail business.
tags: [sales]
timestamp: 2026-06-18T00:00:00Z
---
The sales dataset contains [orders](/tables/orders.md) and [customers](/tables/customers.md).
EOF

# 3. Add an index for navigation
cat > index.md << 'EOF'
# Knowledge Bundle

* Sales Dataset (`datasets/sales.md`) - Retail sales data in an example OKF bundle
EOF

# 4. Validate your bundle
python3 scripts/okf-bundle-validate.py .
```

## Gotchas

- **Type values are not registered centrally.** Pick descriptive types (`BigQuery Table`, `Playbook`, `Metric`). Consumers should handle unknown types gracefully.
- **File path is the identity.** Renaming a file changes its concept ID. Use stable paths or add redirects in documentation.
- **`index.md` uses no frontmatter** (except optionally at the bundle root for `okf_version`). The body is a markdown list with links.
- **`log.md` date headings must be ISO 8601** (`YYYY-MM-DD`).
- **Cross-links are untyped.** The relationship semantics live in the prose, not in the link syntax. Graph builders treat all links as directed edges.
- **OKF does not specify a tag-browsing format.** Producers that want tag aggregation should synthesize it at consumption time by scanning frontmatter.
- **OKF v0.1 is a draft.** The spec will evolve. Minor bumps add backward-compatible features; major bumps may break required fields. Consumers should do best-effort consumption on unknown versions.
