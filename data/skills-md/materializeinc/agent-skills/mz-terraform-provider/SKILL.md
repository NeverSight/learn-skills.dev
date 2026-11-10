---
name: mz-terraform-provider
description: >-
  Using the Materialize Terraform provider to manage Materialize resources
  declaratively. Covers clusters, sources (Kafka, Postgres, MySQL, SQL
  Server), sinks (Kafka, Iceberg), connections, materialized views,
  indexes, tables, roles, grants, secrets, network policies, and
  cloud-only resources (users, SSO, SCIM, app passwords). Use this skill
  whenever the user asks about writing Terraform for Materialize, creating
  or configuring Materialize resources with Terraform, importing existing
  Materialize objects into Terraform state, configuring the Materialize
  provider for Cloud or self-managed, setting up RBAC or grants via
  Terraform, creating connections or sources in Terraform, or
  troubleshooting Terraform plan/apply issues with Materialize resources.
  Also trigger when the user mentions materialize_cluster,
  materialize_source_kafka, materialize_connection_postgres, or any
  other materialize_* resource type.
metadata:
  source: https://github.com/MaterializeInc/terraform-provider-materialize
  verified-against: 44c8487d0f6c
---

# Materialize Terraform Provider

The `MaterializeInc/materialize` Terraform provider manages Materialize resources declaratively. It works with both Materialize Cloud (SaaS) and self-managed deployments.

This skill deliberately does not duplicate the per-resource argument reference. The provider auto-generates complete documentation for every resource and data source from its schema, and that is the source of truth. This skill tells you where that reference lives and carries only the knowledge the generated docs do not: provider setup, cross-resource patterns, import workflows, and gotchas.

## Where the Authoritative Reference Lives

The generated docs are in the provider repository and on the Terraform Registry:

- Repository: `docs/` in [terraform-provider-materialize](https://github.com/MaterializeInc/terraform-provider-materialize)
- Registry: <https://registry.terraform.io/providers/MaterializeInc/materialize/latest/docs>

File naming is mechanical, so you can construct the path for any resource without a catalog:

| You need | Read this file in the provider repo |
|----------|--------------------------------------|
| Resource `materialize_<name>` | `docs/resources/<name>.md` |
| Data source `materialize_<name>` | `docs/data-sources/materialize_<name>.md` |
| Provider arguments | `docs/index.md` |
| Migration guides | `docs/guides/` (e.g., `materialize_source_table.md`) |

For example, `materialize_source_kafka` is documented in `docs/resources/source_kafka.md`. Every generated page includes a full argument reference, attribute reference, import syntax, and usually an example.

**Never guess resource arguments.** Read the generated doc for the resource before writing configuration. When the provider is installed locally, `terraform providers schema -json` gives the exact schema as ground truth.

## Provider Configuration

### Materialize Cloud (SaaS)

```hcl
provider "materialize" {
  password       = var.materialize_password  # app password
  default_region = "aws/us-east-1"
}
```

### Self-Managed

```hcl
provider "materialize" {
  host     = "materialized"
  port     = 6875
  username = "materialize"
  database = "materialize"
  password = var.mz_password
  # Use "require" (or stricter, e.g. "verify-full") against any TLS-enabled
  # deployment. "disable" is only appropriate for a local, non-TLS instance.
  sslmode  = "require"
}
```

### OIDC/SSO Authentication (Self-Managed)

```hcl
provider "materialize" {
  host     = "materialized"
  port     = 6875
  username = var.oidc_username
  password = var.oidc_id_token
  database = "materialize"
  options = {
    oidc_auth_enabled = "true"
  }
}
```

All arguments have environment variable equivalents: `MZ_HOST`, `MZ_PORT`, `MZ_USER`, `MZ_DATABASE`, `MZ_PASSWORD`, `MZ_SSLMODE`, `MZ_DEFAULT_REGION`.

**Important:** Self-managed mode does not support Frontegg-dependent resources (app passwords, users, SSO, SCIM). Those only work against Materialize Cloud.

## Resource Map

A category map of what exists, so you know what to look up. Names only; read the generated doc for arguments.

- **Compute**: `materialize_cluster` (`materialize_cluster_replica` is deprecated, use `materialize_cluster` with `size`)
- **Namespaces**: `materialize_database`, `materialize_schema`
- **Connections**: `materialize_connection_{kafka,postgres,mysql,sqlserver,aws,ssh_tunnel,confluent_schema_registry,aws_privatelink,iceberg_catalog}`
- **Sources**: `materialize_source_{kafka,postgres,mysql,sqlserver,load_generator}`
- **Source tables** (the recommended model, tables defined separately from sources): `materialize_source_table_{kafka,postgres,mysql,sqlserver,webhook}`
- **Sinks**: `materialize_sink_{kafka,iceberg}`
- **Views and tables**: `materialize_materialized_view`, `materialize_view`, `materialize_index`, `materialize_table`, `materialize_type`
- **Security**: `materialize_role`, `materialize_secret`, `materialize_network_policy`, `materialize_grant_system_privilege`
- **Object grants**: one resource per object type (`materialize_cluster_grant`, `materialize_database_grant`, `materialize_schema_grant`, `materialize_table_grant`, and so on), each taking `role_name`, `privilege`, and the object reference. `materialize_*_grant_default_privilege` variants set privileges on future objects.
- **Cloud-only (Frontegg)**: `materialize_user`, `materialize_app_password`, `materialize_sso_*`, `materialize_scim_*`, `materialize_region`
- **System configuration**: `materialize_system_parameter`, `materialize_role_parameter`
- **Data sources**: read-only lists of the above (clusters, sources, views, roles, etc.), plus `materialize_egress_ips`, `materialize_current_cluster`, `materialize_current_database`. All support `region` filtering.

## Cross-Resource Patterns

These conventions apply across most resources and are easy to miss reading one doc page at a time.

### One worked example

Connection, source, and source table compose through nested reference blocks, and credentials come from secrets:

```hcl
resource "materialize_connection_kafka" "kafka" {
  name              = "kafka_conn"
  security_protocol = "SASL_SSL"
  sasl_mechanisms   = "SCRAM-SHA-256"

  kafka_broker {
    broker = "broker1.example.com:9092"
  }

  sasl_username {
    text = "my_user"
  }

  sasl_password {
    secret {
      name = materialize_secret.kafka_password.name
    }
  }
}

resource "materialize_source_kafka" "events" {
  name         = "events_source"
  cluster_name = materialize_cluster.analytics.name

  kafka_connection {
    name = materialize_connection_kafka.kafka.name
  }
}

resource "materialize_source_table_kafka" "events_table" {
  name  = "events"
  topic = "events-topic"

  source {
    name = materialize_source_kafka.events.name
  }

  format {
    avro {
      schema_registry_connection {
        name = materialize_connection_confluent_schema_registry.sr.name
      }
    }
  }

  envelope {
    upsert = true
  }
}
```

### Conventions

- **Qualified names**: most resources expose a read-only `qualified_sql_name` (`database.schema.object`). Cross-resource reference blocks take `name`, `database_name`, `schema_name`, with the latter two defaulting to `materialize` and `public`.
- **Secret or text**: credential arguments accept either inline `text` or a `secret {}` reference block, as in the example above. Prefer secrets.
- **Common arguments**: most resources support `database_name`, `schema_name`, `comment`, `ownership_role`, and `region`; connections additionally support `validate`.
- **Identify by name**: `materialize_cluster` and `materialize_schema` support `identify_by_name = true`, which uses the object name as the state ID instead of the internal Materialize ID. Useful for blue/green deployments where clusters are swapped without changing Terraform state.
- **Write-only arguments** (Terraform 1.11+): `materialize_role.password_wo` and `materialize_secret.value_wo` (with their `*_wo_version` counterparts) never enter Terraform state. Regular sensitive values are hidden from plan output but still stored in state.

## Importing Existing Resources

```bash
terraform import materialize_cluster.my_cluster <region>:<cluster_id>
# or with identify_by_name:
terraform import materialize_cluster.my_cluster <region>:name:<cluster_name>
```

Each generated resource doc shows the exact import format. Find object IDs in the `mz_catalog` system tables (`mz_clusters`, `mz_databases`, `mz_schemas`, `mz_sources`, `mz_sinks`, `mz_views`, `mz_connections`, `mz_secrets`, `mz_roles`).

## Common Gotchas

- **Cloud vs self-managed**: Frontegg-dependent resources (users, SSO, SCIM, app passwords) fail against self-managed instances.
- **Database without public schema**: `materialize_database` does not auto-create a `public` schema. Create one explicitly if needed.
- **Source table migration**: the inline `table {}` block in source resources is deprecated in favor of separate `materialize_source_table_*` resources. See `docs/guides/materialize_source_table.md` in the provider repo.
- **Webhook sources**: `materialize_source_webhook` is legacy. New webhooks should use `materialize_table` with webhook support, though automated migration is not yet available.
- **Cluster replicas deprecated**: use `materialize_cluster` with `size` for managed clusters.
- **Secrets in state**: values marked sensitive are hidden from plan output but stored in state. Use the write-only (`*_wo`) arguments on Terraform 1.11+ to keep them out of state entirely.

## Keeping This Skill Up to Date

The per-resource reference never goes stale here because it is not duplicated here: the generated docs in the provider repo are always current for the release they ship with. The `verified-against` value in the frontmatter records the provider commit the curated content (patterns, gotchas, resource map) was last verified against. To refresh:

1. Diff the provider repository from that commit to current `main`, focusing on new or deprecated resources, `docs/guides/`, and CHANGELOG entries.
2. Update the resource map, patterns, and gotchas here if behavior changed.
3. Bump `verified-against` to the new commit SHA.
