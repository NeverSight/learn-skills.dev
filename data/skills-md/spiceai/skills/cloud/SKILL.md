---
name: cloud
description: Manage Spice.ai Cloud resources through spice cloud, the Management API, and the management MCP server (https://api.spice.ai/mcp) — projects, project forks, deployments, monitors, data reactions, secrets, API keys, and organization members. Use for Cloud project lifecycle (including fork, copy, or move to another region or cluster), deployments (including from a GitHub repository), instance logs, connecting an agent to Spice Cloud over MCP, creating or updating alerts, notification destinations, disabling monitors, alert troubleshooting, organization context, regions, and infrastructure automation. Use sql, search, chat, or sdk for runtime data and inference APIs, and terraform for infrastructure as code.
---

# Spice.ai Cloud Management

Manage Spice.ai Cloud resources through the Management API (control plane) at `https://api.spice.ai`. Create and fork projects, trigger deployments, configure monitors and data reactions, manage secrets and API keys, and administer organization members.

**Renamed in Aug 2026:** apps are now **projects**. The `/v1/projects` routes are canonical; every `/v1/apps` route is still served as a legacy alias (marked deprecated in the OpenAPI spec). Only the list envelope differs — `GET /v1/projects` returns `{"projects": [...]}`, `GET /v1/apps` returns `{"apps": [...]}`. Project-management scopes stay `apps:*`; monitors and reactions have separate scopes below.

## Version Compatibility

Written against the Spice.ai Cloud Management API checked on October 6, 2026, for projects running **Spice v2.4.x** (checked against v2.4.0-rc.2). Two versions matter:

- **The project's runtime**: each deployment resolves the runtime from the project's `update_channel` (`stable`, `preview`, `nightly`) and `version` range unless `image_tag` pins it. Stable can trail the latest OSS release, so check `GET /v1/projects/{projectId}` and the [changelog](https://docs.spice.ai/changelog) before recommending a runtime feature. Cloud APIs have runtime minimums — the MCP API needs v2.0.0+ and `/v1/nsql` needs v2.1.0+.
- **The API surface**: Cloud API changes are dated by the changelog month, not by a runtime release.

| Old | Change | Use instead |
| --- | --- | --- |
| `/v1/apps/...` routes, `apps` list key | Deprecated in Aug 2026 (still served) | `/v1/projects/...`, `projects` key |
| `cname` on create | Deprecated | `region` (`us-east-1`, `us-west-2`) or `cluster_name` |
| `storage_claim_size_gb` | Deprecated | `storage_size_gb` |
| `image_tag` on a non-Enterprise plan | Rejected (`403 image_tag_requires_enterprise`) | `update_channel` and `version` |
| `-models` image tags (e.g. `1.5.0-models`) | Removed in v2.0.0 | Omit `image_tag` (Enterprise: a tag from `/v1/container-images`) |
| Spicepod `version: v1beta1` | Removed in v2.0.0 | `version: v2` (`v1` still loads, auto-migrated) |

## CLI and API interfaces

Use `spice cloud` when the user wants the installed CLI, the Management API below for HTTP
automation, and the [management MCP server](#management-mcp-server) when an agent works through MCP tool calls. Inspect `spice cloud --help` and subcommand help before selecting commands: CLI releases
and the continuously updated Cloud API do not necessarily expose the same operations.

Keep project, deployment, region, monitor, secret, API-key, and member identifiers consistent across
both interfaces. Use the active organization only after checking it matches the user's target.
Runtime SQL, search, and model inference use project endpoints and project API keys; route those
tasks to `sql`, `search`, `chat`, or `sdk`. SDK runtime clients do not replace the Management API.
See the [Cloud CLI reference](https://spiceai.org/docs/cli/reference/cloud) and [Cloud API overview](https://docs.spice.ai/api).

## Authentication

All endpoints except `GET /v1/health` take a Bearer token: a **personal access token** (create at [spice.ai/account/tokens](https://spice.ai/account/tokens), choosing the organization and scopes) or an **OAuth 2.0 client-credentials** access token (create the client under organization **Settings → OAuth Clients**).

```bash
# OAuth client credentials → access token (response: access_token, token_type, expires_in: 3600)
curl -X POST https://spice.ai/api/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "<client-id>", "client_secret": "<client-secret>", "grant_type": "client_credentials"}'

curl -H "Authorization: Bearer $SPICE_API_TOKEN" https://api.spice.ai/v1/projects
```

Required scopes are listed per endpoint below. A write scope includes its read scope, and `*` grants all. Project API keys authenticate the runtime data plane, not the Management API.

### Organization Context

A request acts on the organization the credential was minted against. Send `X-Org-Name: <org-handle>` to act on another: personal access tokens can name any organization the user belongs to, while OAuth clients are pinned to their own (`403 org_assertion_mismatch`). `GET /v1/orgs` (Aug 2026, scope `apps:read`) lists the caller's organizations with its role in each.

## Management MCP server

The management MCP server at `https://api.spice.ai/mcp` (Streamable HTTP) exposes the Management API as tools such as `create_project`, `connect_project_repository`, `create_project_deployment`, `get_project_deployment`, `list_project_instances`, and `get_project_instance_logs`. The `spiceai` plugin includes it as `spice-cloud`. Sign in once from the client's MCP menu (browser OAuth, no client ID needed), or send a management token with the API's scopes in `Authorization: Bearer`. Pass each tool's `org` (a handle from `list_orgs`); without it a call uses the token's organization. Read `tools/list` for the current tools and arguments.

It is not a project's runtime MCP endpoint (`<project endpoint>/v1/mcp` with the project API key), which queries data. Never send a project API key to `api.spice.ai`, or a management token to a project endpoint.

Before connecting a client or deploying through it, read [references/management-mcp.md](references/management-mcp.md): client configuration, scopes per tool, the create → connect a GitHub repository → deploy → status → instance logs workflow, pause and resume, and error codes.

## Health Check

```bash
curl https://api.spice.ai/v1/health
# {"status":"ok","timestamp":"2026-09-17T15:13:40.251Z"}
```

No authentication required.

## Regions

List deployment regions. Pass the `region` value (`us-east-1` or `us-west-2`) when creating projects.

```bash
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  https://api.spice.ai/v1/regions
```

**Scope:** `apps:read`

**Response:** `regions` (each with `name`, `region`, `provider`, `providerName`, `isDefault`, `disabled`) and `default`.

## Projects

Manage Spice.ai Cloud projects.

| Operation      | Method   | Path                             | Scope         |
| -------------- | -------- | -------------------------------- | ------------- |
| List projects  | `GET`    | `/v1/projects`                   | `apps:read`   |
| Create project | `POST`   | `/v1/projects`                   | `apps:write`  |
| Get project    | `GET`    | `/v1/projects/{projectId}`       | `apps:read`   |
| Update project | `PUT`    | `/v1/projects/{projectId}`       | `apps:write`  |
| Delete project | `DELETE` | `/v1/projects/{projectId}`       | `apps:delete` |
| Fork project   | `POST`   | `/v1/projects/{projectId}/forks` | `apps:write`  |
| List forks     | `GET`    | `/v1/projects/{projectId}/forks` | `apps:read`   |
| Connect GitHub repository (Oct 2026) | `PUT` | `/v1/projects/{projectId}/repository` | `apps:write` |
| List instances (Oct 2026) | `GET` | `/v1/projects/{projectId}/instances` | `apps:read` |
| Instance logs (Oct 2026) | `GET` | `/v1/projects/{projectId}/instances/{instanceName}/logs?tail=N` | `apps:read` |

### Create Project

```bash
curl -X POST https://api.spice.ai/v1/projects \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-project",
    "region": "us-west-2",
    "description": "Production analytics project",
    "visibility": "private"
  }'
```

| Field            | Type   | Required | Notes                                                                      |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------- |
| `name`           | string | Yes      | 4–38 chars, letters/numbers/hyphens; unique per org (case-insensitive)     |
| `region`         | string | Yes*     | `us-east-1` or `us-west-2` (from `/v1/regions`)                            |
| `cluster_name`   | string | No       | Dedicated cluster from `GET /v1/clusters`; use instead of `region`         |
| `description`    | string | No       |                                                                            |
| `visibility`     | string | No       | `public` or `private` (default: `private`)                                 |
| `tags`           | object | No       | Key-value pairs                                                            |
| `update_channel` | string | No       | `stable`, `preview`, or `nightly`                                          |

\* Provide `region` or `cluster_name` for a Spice-managed project; omitting every placement field creates an unattached standalone (Cloud Connect) project. **Deprecated:** `cname` (an internal CNAME such as `us-east-1-prod-aws-data`) — use `region`.

**Status codes:** `201` created (the response includes `id` and the data-plane `endpoint`), `400` validation error, `409` name conflict, `429` rate limited

### Update Project

```bash
curl -X PUT https://api.spice.ai/v1/projects/{projectId} \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "update_channel": "stable",
    "version": "2.x"
  }'
```

Updatable fields: `description`, `visibility`, `production_branch`, `tags`, `spicepod` (YAML string or JSON object), `update_channel` (`stable` | `preview` | `nightly`), `version` (runtime semver range, e.g. `2.x`), `image_tag`, `replicas`, `resources`, `executor`, `region`, `cluster_name`, `storage_size_gb` (**deprecated:** `storage_claim_size_gb`).

- Without an `image_tag` pin, each deployment resolves the runtime from `update_channel` and the `version` range. Stable can trail the latest OSS release — the [changelog](https://docs.spice.ai/changelog) lists the runtime each channel runs, so check it before relying on a new runtime feature.
- `image_tag` pins the runtime. It requires the Enterprise plan (`403 image_tag_requires_enterprise`) and must be a published version for the channel (`400 invalid_stable_image_tag`). Send `null` to clear a pin.
- `replicas` and `resources` are capped by plan limits (`GET /v1/limits`).

### Delete Project

```bash
curl -X DELETE https://api.spice.ai/v1/projects/{projectId} \
  -H "Authorization: Bearer $SPICE_API_TOKEN"
```

Deletes the project and tears down its runtime resources. Returns `204`.

### Fork Project (Sep 2026)

Create a project from another's config via `POST /v1/projects/{projectId}/forks` (`apps:write`); list with `GET .../forks`. Optional body fields: `name`, `region`, `cluster_name`, `scheduler_state_location` (required for a distributed source). The fork is **not deployed**; check `shared_state` before `POST /v1/projects/{forkId}/deployments`. Project responses include `forked_from`. Portal: **Create Project → Fork a project** or **Settings → Forks**.

```bash
curl -X POST https://api.spice.ai/v1/projects/123/forks \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "analytics-west", "region": "us-west-2"}'
```

Details (what is copied, GitHub-connected sources, status codes): [references/project-forks.md](references/project-forks.md).

## Deployments

Deploy the project's current spicepod.

| Operation         | Method | Path                                                  | Scope               |
| ----------------- | ------ | ----------------------------------------------------- | ------------------- |
| List deployments  | `GET`  | `/v1/projects/{projectId}/deployments`                | `deployments:read`  |
| Get deployment    | `GET`  | `/v1/projects/{projectId}/deployments/{deploymentId}` | `deployments:read`  |
| Create deployment | `POST` | `/v1/projects/{projectId}/deployments`                | `deployments:write` |

### List Deployments

```bash
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  "https://api.spice.ai/v1/projects/{projectId}/deployments?limit=10&status=succeeded"
```

| Parameter | Default | Description                                                       |
| --------- | ------- | ----------------------------------------------------------------- |
| `limit`   | 20      | Results per page (max 100), most recent first                     |
| `status`  | —       | Filter: `queued`, `in_progress`, `succeeded`, `failed`, `created` |

`created` marks a superseded historical record. A `failed` deployment carries `error_code` and `error_message`: `insufficient_cpu`, `insufficient_memory`, `insufficient_storage`, and `insufficient_instances` are retriable; `pod_exceeds_node_capacity`, `unable_to_start`, and `internal_error` are terminal.

### Create Deployment

```bash
curl -X POST https://api.spice.ai/v1/projects/{projectId}/deployments \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "main",
    "commit_sha": "abc123",
    "commit_message": "Add sales dataset"
  }'
```

| Field            | Type    | Required | Notes                                                    |
| ---------------- | ------- | -------- | -------------------------------------------------------- |
| `image_tag`      | string  | No       | Runtime tag override (Enterprise plan; published version) |
| `channel`        | string  | No       | `stable`, `preview`, or `nightly`                        |
| `replicas`       | integer | No       | 1-10                                                     |
| `branch`         | string  | No       | Source branch                                            |
| `commit_sha`     | string  | No       | Source commit                                            |
| `commit_message` | string  | No       | Deployment description                                   |
| `debug`          | boolean | No       | Enable debug mode                                        |

Returns `202` with the `queued` deployment; poll `GET .../deployments/{deploymentId}` for status. A project connected to a GitHub repository deploys `spicepod.yaml` from the head of its production branch, read when the deployment is created. Returns `409` if a deployment is already in progress, and `400` if the project has no spicepod or is paused (resume with `POST /v1/projects/{projectId}/resume`).

## Monitors and data reactions

Monitors evaluate runtime metrics or dataset status; data reactions fire on matching Drasi queries. List both when asked for project alerts. Use the Management API Bearer token and a project ID from `GET /v1/projects`, not a project API key.

For template selection, condition units, multi-destination notifications, pause/resume behavior, event history, test notifications, or troubleshooting, read `references/monitoring.md` before acting.
Project monitor templates are released for managed projects; availability depends on project capabilities, not early access. LLM failures need models, refresh errors need acceleration, and CPU needs a finite CPU limit. New p95 monitors remain unavailable; use p99.

| Resource | Base path | Read scope | Write scope / update role |
| --- | --- | --- | --- |
| Monitor | `/v1/projects/{projectId}/monitors` | `monitors:read` | `monitors:write`; PATCH requires org admin |
| Data reaction | `/v1/projects/{projectId}/reactions` | `reactions:read` | `reactions:write`; PATCH requires org membership |

On either base path, `GET` lists, `POST` creates, and `GET`, `PATCH`, or `DELETE /{alertId}` operates
on one UUID. **Update existing alerts in place with PATCH**, preserving their IDs and history.
Lists return `{"monitors":[...]}` or `{"reactions":[...]}`. A project outside the credential's org
returns `404`. The cloud helper script has no commands for these routes; use HTTP directly.

```bash
PROJECT_ID=123
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  "https://api.spice.ai/v1/projects/$PROJECT_ID/monitors"
ALERT_ID="<uuid-from-list>"
# A spec supplied to PATCH replaces the spec; send the complete desired condition.
curl -X PATCH "https://api.spice.ai/v1/projects/$PROJECT_ID/monitors/$ALERT_ID" \
  -H "Authorization: Bearer $SPICE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"spec":{"op":"GT","threshold":0.05,"window":"5m","sustainSecs":300,"severity":"critical"}}'
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  "https://api.spice.ai/v1/projects/$PROJECT_ID/monitors/$ALERT_ID"
```

PATCH accepts `name`, nullable `description`, `status` (`active`/`disabled`), `templateId`, complete `spec`, `targets` (or legacy singular `target`), and `recipientUserIds`. Omitted fields are preserved. A different template requires its spec and approval to change the signal.
After every mutation, GET the same ID and verify the requested fields and destinations. `active`
means enabled configuration, not proof of healthy signal evaluation or notification delivery.

Create either kind with `name`, `templateId`, and `spec` containing `op` (`GT`, `GEQ`, `LT`, `LEQ`, `EQ`, `NEQ`) and numeric `threshold`. Disable via PATCH `{"status":"disabled"}` and verify with GET.
Reaction templates are `task_history_error`, `task_history_timeout`, `task_history_slow` (milliseconds), `dataset_row_match`, and `dataset_query`.

`dataset_row_match` needs `spec.dataset`, `column`, and `value`, or nonempty `conditions` with dataset, column, and comparison per condition. `dataset_query` needs `spec.query` and `dataset` or `datasets`; `queryLanguage` defaults to `gql` (`cypher` also works). Dataset reactions conventionally use `{"op":"EQ","threshold":0}`. Creating any reaction requires a ready Drasi data source. Optional `spec.model` transforms results with a spicepod model; monitors reject it.

`targets` supports one email, one Slack, and one HTTPS destination together (three maximum).
On PATCH it replaces the destination set; omit it to preserve destinations. A singular `target`
replaces the set with that one destination. HTTP tokens are write-only; read the reference before
changing a webhook. Without explicit recipients, manual API creation emails the credential's user
(org owner for machine credentials). Creation provisions a live alert and may notify recipients.
Keep `includeDetails` off for sensitive data. Names are unique across both kinds (`409`); the shared
limit is 20 non-deleted alerts, including disabled ones.

Create returns `201`, PATCH returns `200`, and delete returns `200 {"ok":true}`. A paused project refuses creation with `409`. On PATCH `409 monitor_changed`, GET and reconcile concurrent edits.
On PATCH `502`, saved configuration may have changed while backend update failed: GET and retry the update. On delete `502`, the item is hidden but backend cleanup failed: retry the same ID.

### Cluster monitors

Cluster monitors (`cluster_cpu`, `cluster_memory`, `cluster_availability`) are managed per cluster at `/v1/clusters/{clusterId}/monitors`, where `{clusterId}` is the `cluster_name` from `GET /v1/clusters` (e.g. `spicehq-main`). `GET` lists (`{"monitors":[...]}`) and `GET /{alertId}` gets one with `monitors:read` plus org membership; `POST` creates (`201`), `PATCH /{alertId}` updates the rule, destination, or `status` (`active`/`disabled`), and `DELETE /{alertId}` deletes (`200 {"ok":true}`) with `monitors:write` plus org admin. `{alertId}` is a UUID. Creation needs `name`, `templateId`, and `spec` with `op` and numeric `threshold` (same `window`/`sustainSecs`/`severity` defaults as project monitors); names are unique per cluster (`409`). The portal serves equivalent session-authenticated routes under `/api/orgs/{orgName}/clusters/{clusterId}/alerts`, not scriptable with `$SPICE_API_TOKEN`.

## Secrets

Manage project secrets (encrypted at rest). Values are always masked in API responses. Deploy again for changes to reach the runtime.

| Operation     | Method   | Path                                         | Scope           |
| ------------- | -------- | -------------------------------------------- | --------------- |
| List secrets  | `GET`    | `/v1/projects/{projectId}/secrets`           | `secrets:read`  |
| Get secret    | `GET`    | `/v1/projects/{projectId}/secrets/{name}`    | `secrets:read`  |
| Create/Update | `POST`   | `/v1/projects/{projectId}/secrets`           | `secrets:write` |
| Delete secret | `DELETE` | `/v1/projects/{projectId}/secrets/{name}`    | `secrets:write` |

### Create or Update Secret

```bash
curl -X POST https://api.spice.ai/v1/projects/{projectId}/secrets \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "OPENAI_API_KEY", "value": "sk-..."}'
```

Upsert operation — creates if new, updates if exists. Name must start with a letter or underscore; letters, numbers, and underscores only. Reference it in the spicepod as `${ secrets:OPENAI_API_KEY }`.

### Delete Secret

```bash
curl -X DELETE https://api.spice.ai/v1/projects/{projectId}/secrets/OPENAI_API_KEY \
  -H "Authorization: Bearer $SPICE_API_TOKEN"
```

## API Keys

Each project has two API keys (primary and secondary) for zero-downtime rotation. Regenerating a key immediately invalidates the old one.

| Operation      | Method | Path                                | Scope        |
| -------------- | ------ | ----------------------------------- | ------------ |
| Get API keys   | `GET`  | `/v1/projects/{projectId}/api-keys` | `apps:read`  |
| Regenerate key | `POST` | `/v1/projects/{projectId}/api-keys` | `apps:write` |

### Regenerate API Key

```bash
# Regenerate primary key (default)
curl -X POST https://api.spice.ai/v1/projects/{projectId}/api-keys \
  -H "Authorization: Bearer $SPICE_API_TOKEN"

# Regenerate secondary key ("key_number": 0 regenerates both)
curl -X POST https://api.spice.ai/v1/projects/{projectId}/api-keys \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key_number": 2}'
```

`key_number`: `0` (both), `1` (primary, default), `2` (secondary). Responses return `api_key` (primary) and `api_key_2` (secondary).

### Using API Keys with Runtime

Runtime (data-plane) requests go to the project's `endpoint` (returned by `GET /v1/projects/{projectId}`, host e.g. `us-west-2-prod-aws-data.spiceai.io`), with the API key in the `X-API-Key` header. The host `data.spiceai.io` is a region-agnostic alias that only reaches `us-east-1` projects.

```bash
ENDPOINT="https://<project-endpoint-host>"  # the project's endpoint

# SQL query: raw SQL body (a JSON body needs "parameters": [], else 400)
curl "$ENDPOINT/v1/sql" \
  -H "X-API-Key: <api-key>" \
  -H "Content-Type: text/plain" \
  -d "SELECT * FROM my_dataset LIMIT 10"

# Chat (OpenAI-compatible; model is a name from the spicepod)
curl "$ENDPOINT/v1/chat/completions" \
  -H "X-API-Key: <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"model": "my_model", "messages": [{"role":"user","content":"Hello"}]}'

# Search
curl "$ENDPOINT/v1/search" \
  -H "X-API-Key: <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"datasets": ["my_dataset"], "text": "search query"}'
```

## Members

Manage organization members. Roles: `owner`, `admin`, `member`, `viewer` (read-only). Managing members requires `admin` or `owner`; only owners can assign, change, or remove `admin` and `owner`. Owners cannot be modified or removed (`403`).

| Operation     | Method   | Path                     | Scope            |
| ------------- | -------- | ------------------------ | ---------------- |
| List members  | `GET`    | `/v1/members`            | `members:read`   |
| Add member    | `POST`   | `/v1/members`            | `members:write`  |
| Update roles  | `PATCH`  | `/v1/members/{memberId}` | `members:write`  |
| Remove member | `DELETE` | `/v1/members/{memberId}` | `members:delete` |

`{memberId}` is the member's `user_id`.

### Add Member

```bash
curl -X POST https://api.spice.ai/v1/members \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "jdoe", "roles": ["member"]}'
```

`roles` defaults to `["member"]`. The user needs an existing Spice.ai account (`404` if not found); returns `409` if already a member. Change roles with `PATCH` and a body of `{"roles": ["admin"]}`.

### Remove Member

```bash
curl -X DELETE https://api.spice.ai/v1/members/{memberId} \
  -H "Authorization: Bearer $SPICE_API_TOKEN"
```

## Container Images

List runtime image tags (the source of the Terraform `spiceai_container_images` data source). Only needed when pinning `image_tag`, which requires the Enterprise plan.

```bash
# Stable channel (default); use channel=enterprise for enterprise images
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  "https://api.spice.ai/v1/container-images?channel=stable"
```

**Scope:** `apps:read`

**Response:** `images` (each with `name`, `tag`, `channel`) and `default` (the default tag). Use a returned `tag` as `image_tag` rather than guessing one.

## Common Workflows

### Create and Deploy a Project

```bash
# 1. List regions
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  https://api.spice.ai/v1/regions

# 2. Create project
curl -X POST https://api.spice.ai/v1/projects \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "analytics-project", "region": "us-west-2"}'

# 3. Add secrets (use the project ID from step 2)
curl -X POST https://api.spice.ai/v1/projects/123/secrets \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "PG_PASS", "value": "secret123"}'

# 4. Set the spicepod (YAML string or JSON object)
curl -X PUT https://api.spice.ai/v1/projects/123 \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"spicepod": {"version": "v2", "kind": "Spicepod", "name": "analytics-project",
       "datasets": [{"from": "postgres:public.orders", "name": "orders",
         "params": {"pg_host": "db.example.com", "pg_user": "analytics", "pg_pass": "${ secrets:PG_PASS }"}}]}}'

# 5. Deploy
curl -X POST https://api.spice.ai/v1/projects/123/deployments \
  -H "Authorization: Bearer $SPICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"branch": "main", "commit_message": "Initial deployment"}'

# 6. Check deployment status (or GET .../deployments/{deploymentId})
curl -H "Authorization: Bearer $SPICE_API_TOKEN" \
  "https://api.spice.ai/v1/projects/123/deployments?limit=1"
```

### Copy or Move a Project to Another Region

Fork into the target region, fix any `shared_state`, deploy the fork, then point clients at the fork's `endpoint` and API keys. To finish a **move**, delete the source only after the user confirms. Full steps: [references/project-forks.md](references/project-forks.md#copy-or-move-a-project-to-another-region).

### Rotate API Keys (Zero Downtime)

Read the current keys (`GET /v1/projects/123/api-keys`), regenerate the secondary key (`POST` with `{"key_number": 2}`), move clients to it, then regenerate the primary (`{"key_number": 1}`). Clients never hold a revoked key.

## Using the Helper Script

A helper script is bundled at `scripts/spice-cloud.sh` (relative to this skill directory) for common operations. It calls the canonical `/v1/projects` routes; the older `*-app` command names still work as aliases.

```bash
export SPICE_API_TOKEN="your-token"
bash scripts/spice-cloud.sh list-projects
bash scripts/spice-cloud.sh create-project my-project us-west-2
bash scripts/spice-cloud.sh fork-project 123 analytics-west us-west-2   # name/region optional
bash scripts/spice-cloud.sh list-forks 123
bash scripts/spice-cloud.sh deploy 123
bash scripts/spice-cloud.sh add-secret 123 DB_PASSWORD secret123
bash scripts/spice-cloud.sh list-deployments 123
bash scripts/spice-cloud.sh get-api-keys 123
```

## Present Results to User

When presenting management API results: show project IDs/names in a table; for a fork, name the source, that it is not deployed yet, and any `shared_state`; show deployment status (`queued`/`in_progress`/`succeeded`/`failed`) with `error_code`/`error_message` on failure; show monitor/reaction IDs, names, statuses, and template IDs (omit notification targets unless needed); never display secret values; warn on API keys; give the data-plane `endpoint` and portal link `https://spice.ai/<org>/<project>`.

## Troubleshooting

| Issue                               | Solution                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------- |
| `401 Unauthorized`                  | Check `$SPICE_API_TOKEN` is a valid PAT, or an OAuth access token within its `expires_in`   |
| `403` `insufficient_scope`          | Reissue the token or OAuth client with the scope from the endpoint tables above             |
| `403` `forbidden` / `org_forbidden` | Role too low (viewers are read-only) / `X-Org-Name` names an org the caller can't reach    |
| `403 image_tag_requires_enterprise` | Omit `image_tag`; select the runtime with `update_channel` and `version` instead            |
| `404 Project not found`             | Verify `projectId` with `GET /v1/projects` in the right organization                        |
| `409 Conflict` on create project    | Project name already exists (names compare case-insensitively)                              |
| Fork errors (`fork_*`, `scheduler_state_location_*`) | See [references/project-forks.md](references/project-forks.md#fork-error-codes) |
| `409` on deployment                 | A deployment is already in progress; wait for it to complete                                |
| `409 github_connected` on update    | The project deploys `spicepod.yaml` from its GitHub repository; change it there, then deploy |
| `400` on deployment                 | Project has no spicepod, is paused (`POST .../resume`), or `image_tag` isn't a published version for the channel |
| `400` on create secret              | Secret name must start with letter/underscore; letters, numbers, underscores only           |
| Deployment `failed`                 | Check `error_code`: `insufficient_*` codes are retriable; the others are terminal           |
| Runtime requests fail for a `us-west-2` project | Send them to the project's `endpoint`; `data.spiceai.io` only reaches `us-east-1`  |

## Documentation

[Management API](https://docs.spice.ai/api/management-api/management) · [OpenAPI](https://api.spice.ai/openapi.json) · [Runtime API](https://docs.spice.ai/api) · [Changelog](https://docs.spice.ai/changelog) · [spice.ai](https://spice.ai)
