---
name: databricks-api
description: "Top-level router for Databricks platform REST APIs and the Python SDK. Use for any Databricks API or SDK task: Unity Catalog (catalogs, schemas, tables, grants, lineage, quality monitors), Jobs and Workflows, SQL warehouses and statement execution, Model Serving and AI Gateway, Delta Sharing, Genie, Marketplace, or file management on volumes and DBFS. Also use when you're not sure which Databricks API owns the task."
---

# Databricks API Reference

> Compressed from official Databricks docs. Two-tier routing: this file points you to a domain,
> each domain's SKILL.md points you to the right bucket file for your task.

**Grounding rule:** every endpoint path, field name, enum value, and permission you emit must come from a bucket file you've read—verified, not recalled. When a bucket leaves a question open, read the operation's raw doc in `{domain}/_docs/raw/`.

## Quick Routing

| What are you trying to do?                                          | Domain            | Entry point                       |
| ------------------------------------------------------------------- | ----------------- | --------------------------------- |
| Manage catalogs, schemas, tables, volumes, grants, sharing, lineage | **Unity Catalog** | `unity-catalog/SKILL.md`          |
| List or distribute data products, manage private exchanges          | **Marketplace**   | `marketplace/SKILL.md`            |
| Execute SQL, manage warehouses, query history                       | **SQL**           | `sql/SKILL.md`                    |
| Create or manage jobs, workflows, runs, compliance                  | **Jobs**          | `jobs-and-workflows/SKILL.md`     |
| Serve models, manage endpoints, AI Gateway, provisioned throughput  | **Model Serving** | `model-serving/SKILL.md`          |
| AI data assistant — Genie spaces, conversations, evals              | **Genie**         | `genie/SKILL.md`                  |
| Upload, download, manage files (Files API + DBFS)                   | **File Mgmt**     | `file-management/SKILL.md`        |
| Manage shares, recipients, providers, activation, federation        | **Delta Sharing** | `delta-sharing/SKILL.md`          |

Not yet covered (fall back to official docs): Knowledge Assistants, Apps, Compute, Workspace, IAM, Secrets, Pipelines (DLT/Lakeflow), and Dashboards (Lakeview). The roadmap lives in README.md.

## Auth (all domains)

### REST — all requests

```
Authorization: Bearer <PAT-or-OAuth-token>
Base URL: https://<workspace-host>
```

For account-level APIs (metastore admin, user management):

```
Base URL: https://accounts.cloud.databricks.com
```

### Python SDK

```bash
export DATABRICKS_HOST=https://<workspace-host>
export DATABRICKS_TOKEN=dapi...
```

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()  # auto-detects from env or .databrickscfg

# For account-level APIs:
from databricks.sdk import AccountClient
a = AccountClient()
```

### Auth patterns

- **Local dev:** PAT via env var or `.databrickscfg` profile
- **Deployed Apps (OAuth M2M):** Service principal with client_id + client_secret
- **Notebooks:** Auto-auth via runtime (no config needed in DBR 13.1+)
