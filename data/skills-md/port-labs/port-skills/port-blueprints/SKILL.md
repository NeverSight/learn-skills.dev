---
name: port-blueprints
description: "Model a Port context lake data model using blueprints, defining identifiers, titles, icons, properties, relations, and calculation, mirror, or aggregation properties, then author them with the raw Port API. Use when asked to create a Port blueprint, define a Port data model, add a property to a blueprint, relate two blueprints, add a calculation property, add a mirror property, or add an aggregation property."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,blueprints,data-model,reference
  summary: Model your context lake with Port blueprints, properties, and relations
---

# Port blueprints

A blueprint is Port's schema primitive. It defines a type of asset in the
context lake (a `service`, a `package`, a `cluster`, anything), the
properties that describe it, and how it relates to other blueprints. Every
entity in Port's context lake is an instance of a blueprint, the same way a
database row is an instance of a table schema.

## Use this skill when

Use this skill to design or edit a Port data model: creating a new blueprint,
adding or typing a property, relating two blueprints, or adding a
calculation, mirror, or aggregation property. It is reference-only, built
from the static blueprint JSON schema and the raw Port API, so it works
without a live Port account or Port MCP server connected. Without
credentials it still produces valid blueprint JSON the user can apply later.

Out of scope: workflows (`port-workflows`),
scorecards (`port-scorecards`), integration mapping (`port-integrations`),
the Terraform/Pulumi provider reference (`port-terraform`, pointed to in
[Step 6](#step-6---create-or-update-the-blueprint-via-the-api)), and deciding
*what* to model and how blueprints should relate at the data-model-design
level (`port-context-lake` owns that; this skill is the JSON mechanics it
points to).

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- To apply changes without MCP: a `CLIENT_ID`/`CLIENT_SECRET` pair (**...**
  menu > **Credentials** in the Port app), exchanged for a bearer token at
  `POST https://api.port.io/v1/auth/access_token`.
- If Port's MCP server is connected, this skill can use it to read the
  current blueprint (`list_blueprints`) and apply the result directly
  (`upsert_blueprint`) instead of you copying JSON in by hand; the raw API
  calls below always work as a fallback. Search
  `search_port_knowledge_sources` for anything this skill doesn't cover.

## Step 1 - Check whether the blueprint already exists

Precondition: you have a bearer token.
Action: `GET /v1/blueprints/<identifier>`. `200` means it exists, edit it
instead of duplicating it. `404` means it's safe to create.
Fallback: no credentials yet. Draft the JSON and tell the user to verify
uniqueness before applying it.

## Step 2 - Decide the blueprint's identity

Precondition: you know what real-world asset this blueprint represents.
Action: pick an `identifier` (unique, ≤100 characters, immutable after
creation), a human-readable `title`, and an `icon` from Port's
[built-in icon set](https://docs.port.io/build-your-software-catalog/customize-integrations/configure-data-model/setup-blueprint/#full-icon-list).
Fallback: if the asset isn't precisely named yet, ask, or default to a
camelCase noun (`microservice`, `cloudResource`) and flag it as a guess.

## Step 3 - Define properties

Precondition: you know what data this asset needs to carry.
Action: for each field, add a typed entry under `schema.properties` and, if
mandatory, its key to `schema.required`. See
[references/property-types.md](references/property-types.md) for the full
type system: `string`, `number`, `boolean`, `array`, `object`, string
formats (`url`, `email`, `user`, `team`, `date-time`, `timer`, `yaml`,
`markdown`), `enum`, and meta-properties.
Fallback: if the data actually belongs to a different asset, use a relation
([Step 4](#step-4---add-relations-if-this-asset-connects-to-others)) instead
of duplicating it.

## Step 4 - Add relations if this asset connects to others

Precondition: entities of this blueprint need to reference entities of
another blueprint (ownership, dependency, hierarchy).
Action: add a `relations` entry pointing at the target blueprint's
identifier. See [references/relations.md](references/relations.md) for the
single vs. many distinction and the `required`/`many` constraint.
Fallback: if the target blueprint doesn't exist yet, create it first,
relations require an existing target.

## Step 5 - Add computed properties if useful

Precondition: a value can be derived from this blueprint's own properties, or
from related entities, instead of being ingested directly.
Action: use a calculation property (JQ over existing properties), a mirror
property (pull a value from a related entity), or an aggregation property
(count/sum/average across related entities). See
[references/calculation-properties.md](references/calculation-properties.md).
Fallback: if the source property doesn't exist yet, add it first.

## Step 6 - Create or update the blueprint via the API

Precondition: you have a bearer token and a complete blueprint JSON body.
Action: use the endpoints below. Prefer `PATCH` for additive changes to avoid
clobbering unrelated fields.

| Operation | Method | Path |
|---|---|---|
| Create | `POST` | `/v1/blueprints` |
| Fully replace | `PUT` | `/v1/blueprints/{identifier}` |
| Update (additive) | `PATCH` | `/v1/blueprints/{identifier}` |
| Read | `GET` | `/v1/blueprints/{identifier}` |
| Delete | `DELETE` | `/v1/blueprints/{identifier}` |

```bash
curl -L -X POST 'https://api.port.io/v1/blueprints' \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H 'Content-Type: application/json' \
  --data @blueprint.json
 ```

Fallback: a `422` usually means `required` lists a property that isn't in
`properties`, or a relation `target` that doesn't exist yet. Fix the JSON and
retry, don't silently drop the failing field.

If the user's Port account is managed with Terraform or Pulumi instead of raw
API calls, use the `port-terraform` skill, it owns that reference in depth
and the blueprint JSON shape maps directly onto it.

## Examples

Ready-to-apply templates:

- [assets/basic-service-blueprint.json](assets/basic-service-blueprint.json): a single blueprint, a valid `POST /v1/blueprints` body, with primitive and formatted string properties.
- [assets/blueprint-with-relations.json](assets/blueprint-with-relations.json): a JSON array of two blueprints (`team`, then `microservice`), `POST` them in order, showing a required single relation and a self-referencing many relation.
- [assets/blueprint-with-calculation-property.json](assets/blueprint-with-calculation-property.json): a blueprint with a calculation property, a mirror property, and an aggregation property. Assumes a `kubernetesCluster` and an `incident` blueprint already exist as relation/aggregation targets.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `422` on create/update | `required` references a missing property, or a relation `target` doesn't exist | Create the target first; keep `required` in sync with `properties` |
| Property type change is rejected or corrupts data | Property types are immutable after creation | Create a new property with the right type, [migrate data](https://docs.port.io/build-your-software-catalog/customize-integrations/configure-data-model/migrate-data/), delete the old one |
| Relation rejected with `many` and `required` both `true` | Port forbids that combination | A required relation must be single (`many: false`) |
| Calculation property returns `null` | JQ references a missing path, or a relation title (`.relations.x.title`) under persistent calculation | Test the JQ against a real entity payload; use a mirror property for relation titles |
| New property invisible in the UI table | New properties are hidden by default in table views | Toggle it on with **Manage properties**; this doesn't affect the API or ingested data |

## Quick reference

- Blueprint top-level keys: `identifier`, `title`, `description`, `icon`,
  `schema` (`properties`, `required`), `calculationProperties`,
  `mirrorProperties`, `relations`, `ownership`.
- Property types: `string`, `number`, `boolean`, `array`, `object`, plus
  string formats. Full list: [references/property-types.md](references/property-types.md).
- Relation shape: `{ "title", "target", "required", "many" }`. Details:
  [references/relations.md](references/relations.md).
- Derived properties: calculation (JQ), mirror (path into a relation),
  aggregation (count/sum/average/min/max/median). Details:
  [references/calculation-properties.md](references/calculation-properties.md).
- Auth: `POST /v1/auth/access_token` with `clientId`/`clientSecret`.
