---
name: add-concept
description: Add or change a node in the Runpod concept graph (plugins/runpod/skills/runpod-usage/concepts/*.yaml), including process nodes that explain how something works step by step. Use when asked to add a concept, add a rule to one, document how a Runpod flow works, or fix a node. Covers duplicate checks, choosing the kind, finding public sources, writing the file, validating, and checking the graph. Pairs with the write-guide skill, which keeps the skills and docs linked to the concepts.
---

# Add a concept to the graph

Each node is one YAML file in `plugins/runpod/skills/runpod-usage/concepts/`
(called `concepts/` below). The format, kinds, relation types and writing style
are defined in `concepts/README.md`. Read it before writing; this
skill is the procedure, not the format.

Every file is public-facing. Everything in it must be safe to show a customer
and backed by a public source. The validator enforces this.

## 1. Check it doesn't already exist

Search ids, names and aliases before creating anything:

```bash
grep -ril "<term>" plugins/runpod/skills/runpod-usage/concepts/
cd ontology/tools && pnpm build:sqlite && pnpm query concept "<term>"   # resolves names and aliases
pnpm query search "<term>"                                     # finds rules that mention it
```

- If the idea is a fact about an existing concept, add a **rule** to that file instead of a new node.
- If it is a new field or state of an existing resource, add it to that file's `fields` or `states`.
- Create a new file only for a thing a customer or agent names on its own, or for a flow that spans concepts.

## 2. Pick the kind

| If it is… | kind | Example |
|---|---|---|
| Something with its own id and CRUD in the API | `resource` | pod, template |
| Part of a resource with no CRUD of its own | `component` | worker, container-disk |
| Read-only reference data | `catalog` | gpu-type, data-center |
| Something you do with a resource | `capability` | pod-ssh-access |
| Runpod hardware a resource runs on | `infrastructure` | machine |
| Charges or credit | `billing` | pod-billing |
| A cap or quota | `limit` | api-rate-limit |
| A Runpod SDK or CLI | `tool` | flash |
| Something Runpod references but doesn't own | `external` | container-image |
| How something works, in order, across concepts | `process` | pod-deployment |

Set `is_a` for a kind-of parent (`cpu-pod` is_a `pod`). Set `part_of` for the
whole it belongs to (`worker` part_of `serverless-endpoint`). Top-level
resources, catalogs, billing roots, tools and limits sit `part_of:
runpod-platform`.

## 3. Find public sources first

Write only what a public source supports:

| Source | Where | Cite as |
|---|---|---|
| REST v2 spec | `testdata/runpod-migrate/v2-openapi.json` | `source: rest-v2-spec`, `ref: Schema.field` |
| Public docs | the `runpod/docs` repo, or docs.runpod.io | `source: public-docs`, `url: https://docs.runpod.io/<path>` |
| Skills in this repo | `plugins/runpod/skills/` | `source: skill`, `path: plugins/runpod/skills/...` |
| A read-only request you ran | the live API | `source: live-probe`, `ref:` the request, `seen:` the date |

If no public source supports a claim, leave it out. Don't cite internal
documents, internal ids or private repositories. Don't create billable
resources to verify a claim without asking first.

## 4. Write the file

Copy the shape of a similar file (`pod.yaml` for a resource, `machine.yaml` for
infrastructure, `pod-deployment.yaml` for a process) and fill in:

1. `id` (kebab-case; the file is `<id>.yaml`), `name`, `kind`, `summary` (one or two customer-facing sentences), `product`, `is_a`, `part_of`, `aliases`.
2. `surfaces`: the REST v2 schema and paths, GraphQL names from the public reference, MCP tools, `runpodctl` commands, console page.
3. `fields` and `states` if the concept has them. With a REST v2 schema, every field must exist on that schema or its create/update request.
4. `relations`, from the closed set in `concepts/README.md`.
5. `rules`: one fact per rule, with an id of `<concept-id>.<slug>`. Write one to three sentences an agent can act on. Point `applies_to` at the fields, states or actions the rule constrains. Put related rules on other concepts in `see:` instead of restating them.

For a **process**, add `steps` in order. Each step has an `id`, `title`,
`description`, the `concepts` it involves and the `rules` that govern it. Steps
link to rules that already exist on the concepts. Put only the facts that
belong to the flow as a whole on the process itself, such as
`pod-deployment.stock-is-not-your-machine`.

Style: plain present tense, code identifiers in backticks, "Runpod" spelled
correctly, and no words like "currently" or "not yet". The full list is in
`concepts/README.md` under "Writing style".

Don't use `#` comments: `pnpm format` rewrites the file from its data and
refuses a file with a comment, since it would drop it. Put the context in a
`note` on the evidence instead.

## 5. Validate and look at it

```bash
cd ontology/tools
pnpm format              # canonical style; CI runs format:check
pnpm validate --strict   # must report 0 errors and 0 warnings
pnpm test
pnpm build:graph         # open ../build/graph.html
```

Common validator errors:

| Error | Fix |
|---|---|
| `... is not a concept` | A relation, `is_a`, `part_of`, field `ref` or step names a missing id. |
| `applies_to field:x, which ... does not declare` | Add the field, or point at one that exists. |
| `mentions an internal ...` | Restate the rule from a public source, or delete it. |
| `is time-bound` | Say what holds, and put the date in evidence as `seen`. |
| `YAML does not parse` | Quote any item inside `[ ]` or `{ }` that contains a comma, `[]`, `{}`, `: ` or `#`. |

In the graph, find the node, check that its links make sense, and read its
panel once as a customer would.

## 6. Link a guide

Every concept must be covered by at least one skill, reference doc or golden path;
`pnpm check:guides` fails otherwise. Follow the `write-guide` skill
(`.claude/skills/write-guide/SKILL.md`) to extend an existing doc or write a new one, and to
check that the docs already covering the concept still agree with its rules.

## 7. Commit

Commit the concept file, plus any other files you linked from or to, with a
Conventional Commits message that says what the node explains, for example
`docs(concepts): explain why a stopped pod may not restart`.
