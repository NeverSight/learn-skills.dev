---
name: infrahub-managing-checks
description: >-
  Creates, modifies and debugs Infrahub check definitions — Python validation logic, GraphQL queries, and YAML-driven tests for proposed change pipelines.
  TRIGGER when: writing validation checks, creating Python checks, building data quality guards for proposed changes, writing or running tests for a check, modifying or extending an existing check, debugging why a check fails, passes when it should not, or flags the wrong nodes.
  DO NOT TRIGGER when: designing schemas, querying live data, building transforms or generators.
argument-hint: "[check-name] [description...]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Check Creator

## Overview

Expert guidance for creating Infrahub checks. Checks are
user-defined validation logic (Python + GraphQL) that run as
part of a proposed change pipeline. If a check logs any
errors, the proposed change cannot be merged.

## Project Context

Infrahub config:
!`cat .infrahub.yml 2>/dev/null || echo "No .infrahub.yml found"`

Existing checks:
!`find . -name "*.py" -path "*/checks/*" 2>/dev/null | head -20`

Existing queries:
!`find . -name "*.gql" -path "*/queries/*" 2>/dev/null | head -20`

## When to Use

- Writing validation logic for proposed changes
- Creating data quality guards (e.g., rack collision
  detection)
- Building global checks that validate all objects of a type
- Building targeted checks that validate specific grouped
  objects
- Debugging check failures or understanding the check
  lifecycle

## Rule Categories

<!-- markdownlint-disable MD013 -->

| Priority | Category | Prefix | Description |
| -------- | -------- | ------ | ----------- |
| CRITICAL | Architecture | `architecture-` | Three components, global vs targeted, execution flow |
| CRITICAL | Python Class | `python-` | InfrahubCheck base class, validate(), log_error/log_info |
| HIGH | API Reference | `api-` | Class attributes, instance properties, methods, lifecycle, and which API surfaces a rejection (a GraphQL error is a 200) |
| HIGH | Registration | `registration-` | .infrahub.yml config, query name matching, parameters |
| MEDIUM (HIGH for `patterns-shared-module`) | Patterns | `patterns-` | Error collection, shared utilities, scoped validation, relationship-traversal validation, sharing a module across artifact types |
| HIGH | Testing | `testing-` | Resources Testing Framework (YAML-driven tests), infrahubctl check commands, which repository commit a proposed change's checks run |

<!-- markdownlint-enable MD013 -->

## Schema Features This Skill Depends On

A check is only useful if it can fetch and validate
the right data. Most check failures at deploy time
are actually schema-side gaps:

| If the check... | The schema (or .infrahub.yml) must... | See |
| --------------- | ------------------------------------- | --- |
| Reads an attribute via GraphQL | Expose it on the schema node with the same name (`name__value`-shaped paths) | [../infrahub-managing-schemas/rules/attribute-defaults-and-types.md](../infrahub-managing-schemas/rules/attribute-defaults-and-types.md) |
| Walks a relationship to validate related objects | Have both sides of the relationship defined with matching identifiers; otherwise the traversal returns nothing | [../infrahub-managing-schemas/rules/relationship-identifiers.md](../infrahub-managing-schemas/rules/relationship-identifiers.md) |
| Validates a node against a related node's state (child vs parent lifecycle, peer consistency) | Fetch the related node's comparison attribute in the query by traversing the relationship; a check runs one query with no lazy fetch | [rules/patterns-relationship-traversal.md](./rules/patterns-relationship-traversal.md) |
| Is targeted (per-object) | Register a `CoreStandardGroup` as `targets:` in `.infrahub.yml` and map `parameters:` to bind GraphQL variables | [rules/registration-config.md](./rules/registration-config.md) |
| Needs the GraphQL response keyed to typed nodes | Select `id` and `__typename` in the query — the SDK relies on both | [../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md) |
| Should never block a merge but only annotate | Use `self.log_info()` instead of `log_error()`; `log_warning()` does not exist | [rules/python-validate.md](./rules/python-validate.md) |

## Before writing Python

If a cheaper layer can express the constraint, use it.
A schema constraint runs at load time on every write
path; a Python check runs only inside the proposed-
change pipeline, so bad data created via other paths
slips through. Walk this short ladder before reaching
for `InfrahubCheck`:

| Signal | Cheaper layer | See rule |
| ------ | ------------- | -------- |
| Validating uniqueness, presence, allowed values, or regex on a single attribute | Schema constraint (`uniqueness_constraints`, `optional: false`, `kind: Dropdown` choices, `regex`) | [yagni-python-validator-vs-schema-constraint](../infrahub-auditing-repo/rules/yagni-python-validator-vs-schema-constraint.md) |
| Check whose body is a GraphQL query plus a single `if len(...) > 0: raise` | One `.gql` file plus 5 lines of Python | [yagni-redundant-check-that-graphql-can-answer](../infrahub-auditing-repo/rules/yagni-redundant-check-that-graphql-can-answer.md) |
| Enforcing that a relationship is single-peered or non-optional | Schema `cardinality: one`, `kind: Parent` / `Component`, `optional: false` | [yagni-python-validator-vs-schema-constraint](../infrahub-auditing-repo/rules/yagni-python-validator-vs-schema-constraint.md) |

Only when none of these apply should you write a
Python check. The cross-node business rules,
out-of-band reconciliations, and stateful assertions
in [rules/python-validate.md](./rules/python-validate.md)
are the legitimate use cases.

When the check reads objects through the SDK (rather than only its GraphQL
query), type those calls with generated protocol classes rather than string
kinds — `client.get(DcimDevice, ...)`, not `kind="DcimDevice"`. Match the
`--sync` protocol variant to the check's client. See
[protocols-adopt-typed-kinds](../infrahub-common/rules/protocols-adopt-typed-kinds.md).

## Check Basics

Every check has three components:

1. **GraphQL query** (`.gql` file) -- fetches the data to
   validate, and is registered under the top-level
   `queries:` section of `.infrahub.yml`
2. **Python class** -- inherits from `InfrahubCheck`,
   sets `query = "<query_name>"`, implements
   `validate()`
3. **Configuration** -- declared in `.infrahub.yml` under
   `check_definitions` (which does **not** take a
   `query:` field — see below)

```python
from infrahub_sdk.checks import InfrahubCheck


class MyCheck(InfrahubCheck):
    query = "my_query"  # Must match queries[].name in .infrahub.yml

    def validate(self, data: dict) -> None:
        # Validation logic here
        if something_is_wrong:
            self.log_error(
                message="Problem description"
            )
```

> **Where the query is bound:** the Python class
> (`query = "..."`), not `check_definitions`. The
> repository config model uses `extra="forbid"`, so
> putting `query:` under `check_definitions:` makes
> the whole repo config fail validation. This is the
> most common confusion vs. `generator_definitions:`, which
> *does* take a top-level `query:`. See
> [rules/registration-config.md](./rules/registration-config.md).

## Workflow

Follow these steps when creating a check:

1. **Understand the validation goal** — What data
   condition should block a proposed change? Determine
   whether this is a global check (all objects of a
   type) or targeted (specific group). Read
   [rules/architecture-types.md](./rules/architecture-types.md).
2. **Write the GraphQL query** — Create a `.gql` file
   that fetches the data to validate. Read
   [../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)
   for query patterns. If the rule compares a node
   against a related node's state (child vs parent
   lifecycle, peer consistency), the query must fetch
   that related attribute by traversing the relationship
   now — a check runs one query with no later fetch. See
   [rules/patterns-relationship-traversal.md](./rules/patterns-relationship-traversal.md).
3. **Implement the Python class** — Inherit from
   `InfrahubCheck`, implement `validate()`. Read
   [rules/python-validate.md](./rules/python-validate.md)
   for the class pattern and
   [rules/api-reference.md](./rules/api-reference.md)
   for available methods. If the check calls back into
   Infrahub, read
   [rules/api-error-surfaces.md](./rules/api-error-surfaces.md)
   too: a rejected GraphQL request still returns HTTP
   200, so branching on a status code makes the check
   pass on the failure it exists to catch. If the logic
   is shared with a generator or a transform, read
   [rules/patterns-shared-module.md](./rules/patterns-shared-module.md)
   before reaching for a relative import.
4. **Register in .infrahub.yml** — Add the check under
   `check_definitions`. The query name must match the
   Python class `query` attribute. See
   [rules/registration-config.md](./rules/registration-config.md).
5. **Add tests** — Create YAML-driven test definitions
   (smoke, unit, integration) alongside the check so it
   is validated automatically in the proposed change
   pipeline. Read
   [rules/testing-resource-framework.md](./rules/testing-resource-framework.md).
6. **Test locally** — Run `infrahubctl check` to validate
   against a feature branch. See
   [rules/testing-commands.md](./rules/testing-commands.md).
   To run a changed check against an existing proposed
   change, read
   [rules/testing-proposed-change-commit.md](./rules/testing-proposed-change-commit.md):
   the pipeline runs the code at the source branch's
   repository commit, not `main`'s, and a branch rebase
   does not move it on a branch synced with Git.

## Supporting References

- **[reference.md](./reference.md)** -- Class API,
  log_error/log_info (no log_warning), lifecycle,
  `.infrahub.yml` registration (with the no-`query:`
  shape that differs from generator_definitions)
- **[examples.md](./examples.md)** -- Complete check
  patterns (global, targeted, minimal)
- **[../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)**
  -- GraphQL query writing reference
- **[../infrahub-common/infrahub-yml-reference.md](../infrahub-common/infrahub-yml-reference.md)**
  -- .infrahub.yml project configuration
- **[../infrahub-common/rules/](../infrahub-common/rules/)** -- Shared rules
  (git integration, caching gotchas) that apply across all
  skills
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
- **[../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md)**
  -- Schema definitions checks validate against
- **[rules/](./rules/)** -- Individual rules organized by
  category prefix
