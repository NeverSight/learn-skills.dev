---
name: infrahub-managing-transforms
description: >-
  Creates, modifies and debugs Infrahub transforms that convert data into JSON, text, CSV, or device configs using Python or Jinja2 templates, with YAML-driven tests.
  TRIGGER when: building config generation, data export, format conversion, Jinja2 templates, artifact pipelines, writing or running tests for a transform, modifying or extending an existing transform or template, debugging why a transform renders the wrong output or an artifact fails to generate.
  DO NOT TRIGGER when: designing schemas, writing validation checks, creating generators, querying live data.
argument-hint: "[transform-name] [format]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Transform Creator

## Overview

Expert guidance for creating Infrahub transforms.
Transforms convert Infrahub data into different formats
-- JSON, text, CSV, device configs, or any text-based
output -- using Python classes or Jinja2 templates.

## Project Context

Infrahub config:
!`cat .infrahub.yml 2>/dev/null || echo "No .infrahub.yml found"`

Existing transforms:
!`find . -name "*.py" -path "*/transforms/*" -o -name "*.j2" -path "*/templates/*" 2>/dev/null | head -20`

## When to Use

- Building data transformations (Infrahub data -> another format)
- Generating device configurations from infrastructure data
- Creating CSV reports, cable matrices, or inventory exports
- Rendering Jinja2 templates with query data
- Combining Python logic with Jinja2 rendering
- Connecting transforms to artifacts for automated output
- Changing what an existing transform or template renders
- Debugging wrong output, or an artifact that fails to generate

## Rule Categories

| Priority | Category  | Prefix       | Description                                            |
| -------- | --------- | ------------ | ------------------------------------------------------ |
| CRITICAL | Types     | `types-`     | Python vs Jinja2 choice                                |
| CRITICAL | Python    | `python-`    | InfrahubTransform class                                |
| CRITICAL | Jinja2    | `jinja2-`    | Template syntax, filters                               |
| HIGH     | Hybrid    | `hybrid-`    | Python + Jinja2 combined                               |
| HIGH     | Artifacts | `artifacts-` | Output files, targets                                  |
| HIGH     | API Ref   | `api-`       | Class attrs, methods                                   |
| MEDIUM   | Patterns  | `patterns-`  | Utilities, CSV, shared                                 |
| HIGH     | Testing   | `testing-`   | Resources Testing Framework, transform/render commands |

## Schema Features This Skill Depends On

A transform reads schema-shaped data and produces a
file. Misalignment between the transform and the
schema fails late — at artifact-render time, when
someone is waiting for the output.

| If the transform... | The schema (or .infrahub.yml) must... | See |
| ------------------- | ------------------------------------- | --- |
| Will feed an `artifact_definitions` entry | The target node must `inherit_from: CoreArtifactTarget` so the artifact pipeline can attach to it | [../infrahub-managing-schemas/rules/extension-artifact-target.md](../infrahub-managing-schemas/rules/extension-artifact-target.md) |
| Reads attributes from a node | Define those attributes with their full `__value` access path in GraphQL — silent empty strings come from accessing the node, not the value | [../infrahub-managing-schemas/rules/attribute-defaults-and-types.md](../infrahub-managing-schemas/rules/attribute-defaults-and-types.md) |
| Picks a template per device by platform/role | The schema must expose that platform/role as a real attribute or relationship — string-matching on `display_label` is brittle | [../infrahub-managing-schemas/rules/display-human-friendly-id.md](../infrahub-managing-schemas/rules/display-human-friendly-id.md) |
| Is referenced from `artifact_definitions.transformation` | The transform's registered `name` must match the `transformation:` field exactly — mismatch produces "transformation not found" at render time | [rules/artifacts-definitions.md](./rules/artifacts-definitions.md) |
| Uses Jinja2 (not Python) | Register under `jinja2_transforms` with a top-level `query:` field — `python_transforms` binds query on the class, the two keys are not interchangeable | [rules/api-reference.md](./rules/api-reference.md) |
| Is a Python transform | Carry a `watch:` block naming every first-party module it imports — sibling modules included, since imports are never followed. Without the key, Infrahub cannot trust the dependency list and re-renders the artifacts on every commit | [rules/artifacts-watch-dependencies.md](./rules/artifacts-watch-dependencies.md) |
| Reads a data file at runtime, or includes a template by variable name | Name those paths in `watch.files` — detection cannot see a path that exists only as a string, so the artifacts go stale on a change with no error raised | [rules/artifacts-watch-dependencies.md](./rules/artifacts-watch-dependencies.md) |
| Has its artifacts regenerated by a caller (catalog page, CI job, orchestrator) | That caller must poll `CoreArtifact` until each artifact is body-ready — the POST only queues the regen, and the node exists before its content does | [rules/artifacts-async-regen-polling.md](./rules/artifacts-async-regen-polling.md) |

## Before writing Python

If the transform body is string formatting — f-strings,
concatenation, conditional sections — Jinja2 expresses
the same output in fewer lines, renders directly in
the proposed-change UI, and lives under
`jinja2_transforms` in `.infrahub.yml` instead of
`python_transforms`. Walk this ladder before reaching
for `InfrahubTransform`:

| Signal | Cheaper layer | See rule |
| ------ | ------------- | -------- |
| Transform body is `return f"..."` or `"\n".join([...])` built from query results | Jinja2 template file | [yagni-python-transform-that-could-be-jinja2](../infrahub-auditing-repo/rules/yagni-python-transform-that-could-be-jinja2.md) |
| Transform copies query data verbatim without computation | The GraphQL query alone — no transform needed | Ladder step 1 (drop the requirement); judgment call, no rule |
| Conditionals are `if x: out += ...; else: out += ...` and nothing else | Jinja2 `{% if %}` blocks | [yagni-python-transform-that-could-be-jinja2](../infrahub-auditing-repo/rules/yagni-python-transform-that-could-be-jinja2.md) |

Use Python when the transform parses, computes, or
reshapes — IP/subnet math, hashing, ordered
aggregation, structural JSON re-shaping. See
[rules/python-transform.md](./rules/python-transform.md)
for the legitimate cases.

When the transform reads objects through the SDK, type those calls with
generated protocol classes rather than string kinds — `client.filters(NetworkLink, ...)`,
not `kind="NetworkLink"` — so schema drift breaks attribute reads on the
returned objects at type-check time. Field names passed to `create()` are not
type-checked. See
[protocols-adopt-typed-kinds](../infrahub-common/rules/protocols-adopt-typed-kinds.md).

## Transform Basics

Two types of transforms:

| Type       | Output                                                                                                                                   | Entry Point                     |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| **Python** | Whatever the artifact's `content_type` asks for: a `dict` only under `application/json` or `application/yaml`, a `str` for the other six | `InfrahubTransform.transform()` |
| **Jinja2** | Text                                                                                                                                     | `.j2` template file             |

```python
from infrahub_sdk.transforms import InfrahubTransform

class MyTransform(InfrahubTransform):
    query = "my_query"

    # Returns a dict, so the artifact definition has to declare
    # content_type: application/json (or application/yaml). Under any
    # other content type this dict is stored as str(dict), with no
    # error. See rules/artifacts-definitions.md.
    async def transform(self, data: dict) -> dict:
        device = data["DcimDevice"]["edges"][0]["node"]
        return {"hostname": device["name"]["value"]}
```

## Workflow

Follow these steps when creating a transform:

1. **Choose the transform type** — Python for JSON/dict
   or complex logic, Jinja2 for text templates, hybrid
   for both. Read
   [rules/types-overview.md](./rules/types-overview.md).
2. **Write the GraphQL query** — Create a `.gql` file
   that fetches the data to transform. Read
   [../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)
   for query patterns.
3. **Implement the transform** — For Python, inherit
   from `InfrahubTransform` and implement `transform()`.
   Read [rules/python-transform.md](./rules/python-transform.md).
   For Jinja2, create a `.j2` template. Read
   [rules/jinja2-template.md](./rules/jinja2-template.md).
   For hybrid, read
   [rules/hybrid-python-jinja2.md](./rules/hybrid-python-jinja2.md).
4. **Connect to artifacts** — If the transform output
   should be stored as a file, configure artifact
   definitions. See
   [rules/artifacts-definitions.md](./rules/artifacts-definitions.md).
5. **Register in .infrahub.yml** — Add under
   `python_transforms` or `jinja2_transforms`. See
   [rules/api-reference.md](./rules/api-reference.md).
   Then declare the transform's dependencies with
   `watch.files`: read the entry point's imports and
   runtime file reads, and name every first-party path
   they resolve to. A Python transform should always
   carry the key — `files: []` when it genuinely has no
   dependency beyond its own file. Read
   [rules/artifacts-watch-dependencies.md](./rules/artifacts-watch-dependencies.md),
   which also covers reviewing an existing `watch` block
   for entries that are missing, stale, or wrong.
6. **Add tests** — Create YAML-driven test definitions
   (smoke, unit, integration) alongside the transform so
   it is validated automatically in the proposed change
   pipeline. Read
   [rules/testing-resource-framework.md](./rules/testing-resource-framework.md).
7. **Test locally** — Run `infrahubctl transform` or
   `infrahubctl render` to validate. See
   [rules/testing-commands.md](./rules/testing-commands.md).

## Supporting References

- **[rules/artifacts-definitions.md](./rules/artifacts-definitions.md)**
  -- The eight `content_type` values and how each
  serialises the transform's return value. Authority on
  which return type a content type accepts
- **[reference.md](./reference.md)** -- Class API,
  lifecycle, `.infrahub.yml` registration shapes,
  filter env overview
- **[examples.md](./examples.md)** -- Complete transform
  patterns (Python, Jinja2, hybrid, CSV)
- **[../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)**
  -- GraphQL query writing reference
- **[infrahub-yml-reference.md](../infrahub-common/infrahub-yml-reference.md)**
  -- .infrahub.yml project configuration
- **[../infrahub-common/rules/](../infrahub-common/rules/)** -- Shared rules
  (git integration, caching) across all skills
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
- **[../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md)**
  -- Schema definitions transforms work with
- **[rules/](./rules/)** -- Individual rules by category
