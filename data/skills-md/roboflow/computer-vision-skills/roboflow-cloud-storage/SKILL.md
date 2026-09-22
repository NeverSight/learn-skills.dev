---
name: roboflow-cloud-storage
description: Use when connecting cloud storage (AWS S3 / S3-compatible or Google Cloud Storage) to Roboflow to mirror images into a workspace — creating storage credentials, defining datasources (bucket-mirror configs), selecting objects with glob rules, validating access, and running/scheduling mirror jobs.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Cloud Storage (Datasources & Credentials)

Mirror a cloud bucket's contents into a Roboflow workspace so new objects flow
in automatically. Two pieces work together:

- **Credential** — the secret Roboflow uses to reach the bucket (stored,
  masked server-side, reusable across datasources).
- **Datasource** — a *bucket-mirror configuration*: which bucket (via a
  credential), which objects (glob rules), and how they sync. "Datasource" is
  the user-facing name; the platform stores it as a bucket-mirror config.

> Imports land at the **workspace** level. The datasource API cannot target a
> specific project/dataset today.

> Only want to run a model/Workflow over the files and collect the outputs,
> without importing anything into Roboflow? That is batch processing — see the
> `roboflow-batch-processing` skill. Mirroring composes with it too: imported
> files become Asset Library images, and bulk predictions over them run as
> Asset Library batch processing jobs (same skill).

## Fast path — one call

`connect_cloud_storage` does the whole flow in one shot: (optionally) create a
credential, create the datasource, validate access, and start the first mirror
run. Prefer it for new setups.

- Reuse a credential: pass `credential_id` (from `credentials_list`).
- Create a new credential: pass `credential_name` + `credential_type` (the
  secret is collected securely out-of-band — see Security).
- Describe the datasource so it can be created first: `bucket_type` (`s3`/`gcs`),
  `bucket_name`, `region`, plus optional `mirror_configs` glob rules (see
  Datasources). The datasource must exist before anything can be validated or
  triggered — there is nothing to mirror without it.
- `trigger` (default true) starts a mirror run **only if validation passes**;
  triggering consumes credits.
- Returns `{credentialId, credentialCreated, datasourceId, validation,
  triggered, batchIds?}`. If a new credential was created but a later step
  failed, you get `status: "partial"` with the ids so you can clean up with
  `credentials_delete` / `datasource_delete`.

## Credentials

### Security — secrets never enter the chat
The secret (keys, service-account JSON, password) is collected **out-of-band**
via MCP elicitation, never as a tool argument and never in the transcript or
model context. `credentials_list` returns only masked, non-secret fields.
If your client can't elicit securely, the tool returns
`manual_entry_required` with a URL to create the credential in the app
(`app.roboflow.com/<workspace>/settings/datasources`), then call
`credentials_list` to get its id.

### Credential types

| `credential_type` | Provider | Secret fields collected |
|---|---|---|
| `IAM` | AWS S3 | `accessKeyId`, `secretAccessKey`, `sessionToken?` |
| `AssumeRole` | AWS S3 | `roleArn`, `externalId`, `sessionName?` |
| `AssumeRoleWithWebIdentity` | AWS S3 | `roleArn`, `webIdentityAudience`, `webIdentityRoleArn`, `externalId`, `sessionName?` |
| `gcs` | Google Cloud Storage | `projectId`, `credentialFile` (full service-account JSON) |
| `usernamePassword` | S3-compatible | `username`, `password` |
| `apiKey` | S3-compatible | `apiKey` |

> **AWS PrivateLink (`require_vpce`)** requires an
> `AssumeRoleWithWebIdentity` credential; the server rejects the datasource
> otherwise.

## Datasources

### Bucket
- `bucket_type`: `s3` or `gcs`
- `bucket_name` (no scheme/path), `region` (e.g. `us-east-1`)
- `endpoint`: custom URL for S3-compatible providers (S3 only)

### Mirror rules (`mirror_configs`)
Optional list; omit to mirror the **whole bucket** with default settings. Each
rule selects a subset and controls sync behavior:

- **`glob_patterns`** (list) — the key field. Selects objects, e.g.
  `["images/**/*.jpg", "batch-*/**"]`. Set it to avoid importing unwanted files
  or to split a bucket into multiple rules. Omit only when you truly want
  everything.
- `glob_file_path` — alternative: path to a manifest file in the bucket whose
  lines list object paths to import.
- `id` — rule id (auto-generated; pass an existing id on update to edit in place).
- `settings` (omitted keys use server defaults):
  - `removeOrphanedSourcesWhenDisappeared` (default true) — delete mirrored
    images when the source object is removed.
  - `namingStrategy` (`fullPath`|`fileName`|`eTag`|`metadata`, default
    `fullPath`); `namingStrategyMetadataKey` required when `metadata`.
  - `updateImageWhenNewer` (true) / `updateImageStrategy` (`overwrite`).
  - `updateMetadataWhenNewer` (true) / `updateMetadataStrategy`
    (`mergeBucketWins` default; also `overwrite`|`merge`|`mergeUserWins`|
    `untilFirstChange`|`append`).
  - `runScheduledEvery` (hours, default 0 = off) — >0 enables a recurring mirror
    (fixed 24h cadence today; only on/off is honored).

## Lifecycle & validation

1. **Create** (`datasource_create`, or `connect_cloud_storage`). Nothing is
   mirrored yet.
2. **Validate** (`datasource_validate`) — checks `listFiles`, `headFile`,
   `getFile`, and per-rule `headGlobFile`; returns `{checks, errors}`. Run it to
   self-diagnose a bad credential/bucket **before** triggering.
3. **Trigger** (`datasource_trigger`) — starts the mirror job; **consumes
   compute/storage credits**. Returns `{batchIds}`.
4. **Poll** (`datasource_job_get` with a `batchId`) — `status`
   (running/completed/failed), per-stage `counters`, `errors`, timestamps.

**Update** (`datasource_update`): only fields you pass change; to change the
bucket pass `bucket_type` + `bucket_name` + `region` together.
**Delete** (`datasource_delete`): removes the config, **not** already-mirrored
images. Deleting a credential still referenced by a datasource makes its runs
fail.

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `connect_cloud_storage` | End-to-end: credential + datasource + validate + first run |
| `credentials_list` | List masked cloud-storage credentials |
| `credentials_create` | Create a credential (secret collected securely out-of-band) |
| `credentials_delete` | Delete a credential |
| `datasources_list` / `datasource_get` | List / inspect datasource configs |
| `datasource_create` / `datasource_update` / `datasource_delete` | Manage a datasource |
| `datasource_validate` | Check bucket access before a run |
| `datasource_trigger` | Start a mirror run (consumes credits) |
| `datasource_job_get` | Poll a mirror run's status and counters |

## Related Pages

- `roboflow://skills/roboflow-data-management/SKILL` — what to do with the images once mirrored (tags, splits, versions, search)
- `roboflow://skills/roboflow-product-navigation/SKILL` — the app's `settings/datasources` page
