---
name: infrahub-common
description: >-
  Shared references and cross-cutting rules for all Infrahub skills — GraphQL syntax, .infrahub.yml format, and common patterns.
  DO NOT TRIGGER directly — loaded automatically by other Infrahub skills when they need shared references.
user-invocable: false
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Common References

This skill contains shared resources referenced by all other
Infrahub skills. It is not meant to be invoked directly.

## Contents

- **`graphql-queries.md`** — Infrahub GraphQL query syntax,
  filters, nested queries, and pagination patterns
- **`infrahub-yml-reference.md`** — `.infrahub.yml`
  configuration file format and field reference
- **`marketplace-reference.md`** — Infrahub Marketplace:
  reusing published schemas and collections via
  `infrahubctl marketplace get`, discovery with
  `infrahubctl marketplace list` / `search` / `show`, and
  airgap fallback. Reuse before modelling from scratch.
- **`netbox-vs-infrahub.md`** — Field-by-field
  migration appendix for engineers porting NetBox
  queries, templates, or overlay data
- **`metadata-lineage.md`** — Value metadata (`source`,
  `owner`, `is_protected`): what each field means, how
  to set it in object files, and why `source` does not
  control edit access
- **`profiles-and-templates.md`** — The Profiles vs
  Object Templates distinction and mechanics
- **`rules/`** — Cross-cutting rules shared across skills:
  - Branch-first data CRUD (default to a branch, not the default branch)
  - Caching display labels in queries
  - Python environment and connectivity checks
  - Git integration and deployment patterns
  - Dry-running a changed `.gql` query against the live
    schema before merge, and which `infrahubctl` command
    does it for a transform, check or generator
  - Recovery from partial repository syncs
  - Generated file protocol conventions
  - `schema.graphql` as `infrahubctl graphql
    export-schema` output — re-exported, never
    hand-edited
  - Adopting generated protocols for typed SDK calls
  - Information-source priority (skill content first,
    with a concrete last-resort procedure for consulting
    `docs.infrahub.app` on a genuine gap)
