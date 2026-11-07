---
name: port-terraform
description: >-
  Author and manage Port blueprints, entities, scorecards, and self-service
  actions with the official Terraform provider (port-labs/port-labs).
  Covers provider setup and auth, every resource type (port_blueprint,
  port_entity, port_scorecard, port_action, port_webhook, port_integration,
  port_aggregation_properties), the create/update/delete/import lifecycle,
  and known limitations that produce broken or silently wrong config. Use
  when asked to "add a Port resource to Terraform", "manage Port as code",
  "write a port_blueprint/port_entity/port_action/port_scorecard resource",
  "import a Port blueprint into Terraform state", or "why did my Port
  terraform apply not do what I expected".
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,terraform,iac,reference
  summary: Manage Port resources as code with the Terraform provider
---

# Port Terraform provider

Port's Terraform provider (`port-labs/port-labs`) lets you define blueprints,
entities, scorecards, self-service actions, webhooks, and integration
mappings as `.tf` resources, the same way you'd define any other piece of
infrastructure. This skill is reference-only: static knowledge about the
provider's resource schema, drawn from the current v2.x provider and Port's
Terraform docs. It doesn't need a live Port account or Port MCP server to
produce correct HCL, only a real account and API credentials to actually
`terraform apply` it.

Out of scope: the underlying Port concepts (property types, relation
semantics) are owned by the `port-blueprints` skill; self-service action
JSON schema and invocation method payload templating aren't covered by a
skill in this repo yet. This skill only covers how those concepts map onto
Terraform arguments. Pulumi is Port's
other IaC provider, briefly noted in [Step 1](#step-1---set-up-the-provider),
but not covered in depth here.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time working with Port.
- The [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli) (or [OpenTofu](https://opentofu.org/docs/intro/install/), a drop-in alternative, swap `terraform` for `tofu`).
- A Port account and a `client_id`/`client_secret` pair, from **...** menu > **Credentials** in the Port app, or the [API docs](https://docs.port.io/build-your-software-catalog/custom-integration/api#find-your-port-credentials).
- No Port MCP server or CLI is required to write or apply the `.tf` files this skill produces. If one is connected, use it to check the current live state (`list_blueprints`) before writing HCL that should match it, and search `search_port_knowledge_sources` for anything this skill doesn't cover.

## Step 1 - Set up the provider

Precondition: no `port` provider block exists in the working directory yet.
Action: add a `terraform` block pinning `port-labs/port-labs`, and a
`provider "port"` block with credentials from environment variables, then
run `terraform init`:

```hcl
terraform {
  required_providers {
    port = {
      source  = "port-labs/port-labs"
      version = "~> 2.4.0"
    }
  }
}

provider "port" {
  client_id = "" # or set the environment variable PORT_CLIENT_ID
  secret    = "" # or set the environment variable PORT_CLIENT_SECRET
  base_url  = "https://api.port.io"
}
 ```

```bash
terraform init
 ```

Fallback: if the user's stack is Python, TypeScript, JavaScript, or Go
instead of HCL, Port also ships a Pulumi provider with the same `Entity`
resource concept. Point them at
[docs.port.io's Pulumi page](https://docs.port.io/build-your-software-catalog/custom-integration/iac/pulumi/)
instead of forcing Terraform.

## Step 2 - Model data with `port_blueprint`

Precondition: the context lake needs a new type, or an existing blueprint needs
to move under Terraform management.
Action: write a `port_blueprint` resource with `identifier`, `title`, typed
`properties`, and any `relations` to other blueprints. See
[references/resource-reference.md](references/resource-reference.md) for
the full property-type and relation argument tables, and
[assets/blueprint.tf](assets/blueprint.tf) for a complete example.
Fallback: if a relation's `target` blueprint doesn't exist yet, define it
first, `port_blueprint.relations` requires an existing target and Terraform
won't infer creation order across two relations pointing at each other
without an explicit `depends_on`.

## Step 3 - Populate the context lake with `port_entity`

Precondition: a blueprint exists (via Terraform or otherwise) and you need
to create, update, or manage a specific instance of it.
Action: write a `port_entity` resource with `blueprint`, `title`, an
explicit `identifier`, and `properties`/`relations` matching the blueprint's
schema. See [assets/entity.tf](assets/entity.tf) for single and many
relations together.
Fallback: if you're bringing an entity that already exists in Port under
Terraform management, don't start from a partial definition, see
[Limitations #3](references/limitations.md) first: unspecified properties
get overridden with empty values, not left alone.

## Step 4 - Add scorecards with `port_scorecard`

Precondition: entities of a blueprint need a maturity or readiness score.
Action: write a `port_scorecard` resource with `blueprint`, `rules`
(`identifier`, `title`, `level`, `query`), and optionally custom `levels`.
Each rule's `query.conditions` is a list of `jsonencode()`'d condition
objects, not native HCL. See
[assets/scorecard.tf](assets/scorecard.tf).
Fallback: if a rule's `level` doesn't match one of the scorecard's `levels`
(or the defaults `Basic`/`Bronze`/`Silver`/`Gold` when `levels` is omitted),
`terraform apply` rejects the rule, define the levels first.

## Step 5 - Add self-service actions and automations with `port_action`

Precondition: users need a form to trigger a backend (self-service action),
or an event in Port needs to trigger one automatically (automation).
Action: write a `port_action` resource with exactly one of
`self_service_trigger` / `automation_trigger`, and exactly one invocation
method block (`webhook_method`, `github_method`, `gitlab_method`,
`azure_method`, `kafka_method`, `upsert_entity_method`, or
`integration_method`). See
[references/resource-reference.md](references/resource-reference.md) for
the full trigger and invocation-method argument tables, and
[assets/action.tf](assets/action.tf) for a self-service action plus an
automation in one file.
Fallback: if a `user_properties` entity-picker `dataset` mixes a static rule
with a `jq_query` rule, don't use the native HCL `dataset` block, wrap the
whole thing in `jsonencode()`, see
[Limitations #1](references/limitations.md).

## Step 6 - Sync webhooks, integrations, and aggregations

Precondition: you need a custom inbound webhook (`port_webhook`), to bring
an already-installed Ocean integration's mapping under version control
(`port_integration`), or to add computed count/average properties across
related entities (`port_aggregation_properties`).
Action: see the per-resource argument tables in
[references/resource-reference.md](references/resource-reference.md).
`port_integration` manages an *existing* installation only, always
`terraform import` it first (Step 7).
Fallback: a `port_aggregation_properties` property returns `null` or `0`
with no error when more than one relation path connects the two blueprints
and `path_filter` isn't set, see
[Limitations #2](references/limitations.md).

## Step 7 - Import existing Port resources into Terraform state

Precondition: a blueprint, entity, scorecard, action, webhook, integration,
or aggregation property already exists in Port and needs to come under
Terraform management.
Action: add a resource block (even an empty one to start), then run
`terraform import <resource_type>.<name> "<id>"` with the ID format from the
[import table](references/resource-reference.md#lifecycle-create-update-delete-import),
then `terraform plan` to check for drift before the next `apply`.
Fallback: if the resource block doesn't match the imported state,
`terraform plan` shows the mismatch as drift to fix, and applying it will
overwrite (or empty out) the real Port resource, don't apply until the plan
shows no unexpected changes.

## Examples

Complete, standalone `.tf` files (each includes its own `terraform` and
`provider` block):

- [assets/blueprint.tf](assets/blueprint.tf): two related blueprints, all five property-group types.
- [assets/entity.tf](assets/entity.tf): entities wired up with a single relation and a many relation.
- [assets/action.tf](assets/action.tf): a self-service create action with a webhook backend, plus an automation.
- [assets/scorecard.tf](assets/scorecard.tf): custom levels and multiple JQ-based rules.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `port_action` config rejected, or built from a stale example | Top-level `user_properties`/`operation` on `port_action` is the deprecated v1.x shape | Nest under `self_service_trigger` or `automation_trigger`, see [Limitations #6](references/limitations.md) |
| Entity-picker dataset doesn't filter correctly | Mixed static and `jq_query` rules in a native HCL `dataset` block | `jsonencode()` the whole `dataset` object, see [Limitations #1](references/limitations.md) |
| Aggregation property is `null`/`0` with no error | Ambiguous relation path between blueprints | Add `path_filter`, see [Limitations #2](references/limitations.md) |
| Updating an existing entity wipes properties you didn't touch | `port_entity` uses create/override, not merge | Reproduce the entity's full current state in the resource body |
| `terraform destroy` fails on a blueprint | Entities exist that weren't created by this Terraform state | Set `force_delete_entities = true` before destroying |
| Changing a property's `type` is blocked | `blueprint_property_type_change_protection` defaults to `true` | Add a new property with the right type, migrate data, remove the old one, don't disable the protection |
| Drift wipes a resource right after `terraform import` | Resource block doesn't match the real imported state | Reconcile the block with `terraform plan` before the first `apply` |

## Quick reference

- Provider: `provider "port" { client_id, secret, base_url }`, or
  `PORT_CLIENT_ID`/`PORT_CLIENT_SECRET` env vars.
- Resources: `port_blueprint`, `port_entity`, `port_scorecard`,
  `port_action`, `port_webhook`, `port_integration`,
  `port_aggregation_properties`.
- Property groups (blueprint and entity): `string_props`, `number_props`,
  `boolean_props`, `object_props`, `array_props`.
- Relation groups (entity only): `single_relations`, `many_relations`.
- Action triggers: `self_service_trigger` (`CREATE`/`DAY-2`/`DELETE`) or
  `automation_trigger` (event-based). Exactly one per action.
- Action invocation methods: `webhook_method`, `github_method`,
  `gitlab_method`, `azure_method`, `kafka_method`, `upsert_entity_method`,
  `integration_method`. Exactly one per action.
- Import ID formats: full table in
  [references/resource-reference.md](references/resource-reference.md#lifecycle-create-update-delete-import).
- Full argument reference:
  [references/resource-reference.md](references/resource-reference.md).
  Known gotchas: [references/limitations.md](references/limitations.md).
