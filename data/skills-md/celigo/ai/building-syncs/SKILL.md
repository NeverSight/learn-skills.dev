---
name: building-syncs
description: Build Celigo syncs (Celigo Data Ingestion) -- managed pipelines that replicate many tables from a source application into a data warehouse, with a historical backfill, incremental runs and schema-drift handling. Covers sync versus flow, the sync integration, datasets, destinations, the enable and license gates, runs and resyncs, and sync jobs, errors and events. Use when replicating application data into Snowflake, Google BigQuery, Microsoft SQL Server or NetSuite Analytics Warehouse, or when building, running or troubleshooting a sync.
---

<!-- TIER:1 -->

# Building Syncs

A sync (Celigo Data Ingestion) replicates data from one source application into a data warehouse. It pairs a **source connection** with a **destination** (a warehouse connection plus a database and schema), and its **datasets** choose which tables or objects it copies, which columns, and how each table loads. The first run backfills history from `historicDateTime`; later runs are incremental. Runs happen on a cron schedule or on demand, and each one leaves a read-only **sync job** with per-table children, **run errors**, and **events** for schema drift.

A sync is not a flow. It has no steps, mappings, hooks, filters or routers, it lives in its own kind of integration, and its runs and errors are read through sync jobs, not flow jobs or flow errors.

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Build a Sync below, then the headings of Sync Operations:

- **The `celigo` CLI** (`celigo syncs`, `celigo datasets`, `celigo sync-jobs`) -- [references/cli.md](references/cli.md)
- **Celigo MCP tools** -- [references/mcp.md](references/mcp.md). The deployed Celigo MCP server has no sync, dataset or sync-job tools: build and operate syncs with the CLI, the REST API, or the Celigo UI.

Listing syncs, reading a connection's catalog and columns, and reading jobs, errors, events and usage only read (a catalog or column read can query the source application). Creating or changing a sync or its datasets writes to the account. Two writes reach outside it: **saving a destination** connects to the warehouse and creates the schema if it's missing, and **enabling a sync** starts its schedule -- every run extracts from the source and loads rows into the warehouse, rows that count against the account's Data Ingestion volume.

## Sync or Flow?

Decide this first, and say the limit out loud when a request lands on the wrong side -- never quietly build a flow for someone who asked for a sync.

| The request | Build | Why |
|---|---|---|
| Replicate many tables or objects of an application into a warehouse, with a backfill and incremental updates | **Sync** | The managed case: tables created and kept in step with the source, drift handled per policy |
| Land one export's records in a warehouse table, with no mappings or hooks on the way | **Sync** with an export-backed dataset | Reuses the export's extraction; the sync manages the table |
| Move records between two applications ("sync customers from Shopify to NetSuite") | Flow | A sync's destination is always a warehouse |
| Push warehouse data back into an application (reverse ETL, activation) | Flow | Syncs only load into a warehouse |
| Reshape, map, filter or branch each record on the way in | Flow, or a sync that lands raw data you transform in the warehouse | A sync has no per-record steps |
| React to changes as they happen (webhooks, real-time events, change data capture) | Flow, with a listener or CDC export | A sync runs on a schedule or on demand, never on an event |
| Load into a warehouse the destinations list doesn't name | Flow with a database import | A sync's destination must be a listed warehouse |

The supported warehouses come from the destinations list (`snowflake`, `bigquery`, `mssql`, `nsaw` at the time of writing); read it rather than assume it. A source that offers no catalog can still feed a sync through export-backed datasets.

## The Sync Model

### The sync integration

A sync lives in an integration created with `syncs: true`. The flag is fixed at creation -- an update ignores it in both directions -- so an existing flow integration can never hold syncs, and creating a sync in one is refused ("An integration is suppose to have either flows or syncs but not both."). The rule is only checked on the sync side: a flow created in a sync integration is accepted, so keep flows out of it yourself.

- **`_integrationId` is permanent.** It's required on create, can't be sent on an update, and a sync can't be moved to another integration.
- **Its connections are registered.** Creating a sync, or saving its destination, adds its connections to the integration's `_registeredConnectionIds` and sets `microServices.workerGroup: "DIWorker"` on each connection (a `system` change in the connection's audit log). Deleting the syncs that use a connection clears its worker group.
- **One warehouse type per integration.** All syncs in an integration load into the same destination application ("The destination type for all the syncs under an integration must be same."). A second warehouse type needs its own integration.
- **Syncs block the integration's delete.** An integration that still holds a sync can't be deleted ("sync `<syncId>` must be deleted before you can delete integration `<integrationId>`").

### Sources: catalog datasets and export-backed datasets

Any connection can be a sync's source. What it can offer depends on its catalog -- the list of tables or objects for that connection:

- **Catalog (object mode).** A non-empty catalog means the source offers its tables directly: Salesforce, NetSuite saved searches, NetSuite through SuiteAnalytics Connect (JDBC), and the HTTP connectors in the sources list. Each catalog entry's `name` is the dataset's `externalId`, exactly as returned -- for an HTTP-connector source it's an opaque id, not the table's label (`displayName`).
- **Export-backed datasets.** An empty catalog (`datasets: []`, answered with 200, not an error) means the connection feeds a sync only through exports: a plain HTTP connection, an HTTP connector the sources list doesn't name, or a connection on a different API or version of a listed connector. The catalog also lists the connection's exports; a dataset with `isExport: true` and `externalId` set to an export's `_id` loads that export's records. The export must run on the sync's source connection.

An empty catalog is a signal about the connection, not about the data: don't retry it or tell the user the source has no tables.

### Destinations

The destination block is `_connectionId`, `database`, `schema`, and an optional `tablePrefix`. The warehouse is the destination connection's own type -- `rdbms.type` `snowflake`, `bigquery` or `mssql`, or a NetSuite Analytics Warehouse JDBC connection -- and any other connection is refused ("Invalid destination type and please provide the valid destination type"). For BigQuery, `database` is the GCP project and `schema` the dataset, case preserved; it must be the `rdbms` BigQuery connection, not the Google BigQuery HTTP connector.

- **Send the block complete, in one save.** A partial block is refused in the warehouse's own words -- "SQL Server database is required on sync destination", "BigQuery dataset is required on sync destination" -- except Snowflake, whose partial save reaches the warehouse and fails there.
- **The database must exist; the schema is created if it doesn't.** So a misspelled schema becomes a new schema in the customer's warehouse rather than an error. Confirm both names with the user.
- **Saving reaches the warehouse.** The connection has to work first: against an unreachable host the save can run past 30 seconds and store nothing. Fix the connection rather than trying other names.
- **SQL Server checks identifiers**: start with a letter or underscore; letters, digits, `_` or `$`; at most 128 characters.
- **A database and schema pair backs one sync.** A destination whose `database` and `schema` match another sync's -- compared without regard to case, even on another host, warehouse type or integration -- is refused with "Duplicate destination host found". Give each sync its own schema.
- **A sync's warehouse type is fixed once saved** ("Destination connection type is not same as the previous destination connection type"). Loading into another kind of warehouse means a new sync, in an integration of that type.

### Datasets

One dataset per table or object the sync replicates. All dataset writes go through one bulk PUT of an array:

- **An item with `externalId` creates; an item with `_id` updates.** Both or neither fails the batch. It isn't an upsert: creating an `externalId` the sync already has is refused ("... datasets requested to create are already present"), and so is updating an `_id` from another sync.
- **One bad item fails the whole batch**, including the valid items in it. Datasets the batch doesn't name are left as they are. The response has no body -- read the datasets back.
- **An update replaces `name`, `tableName` and `exportProperties` with what the item carries**, so an item that leaves one out clears it; an omitted `ingestionMode` or `dataElements` keeps its saved value. A partial `{_id, enable: false}` therefore wipes the dataset's table name. Send every item whole: read the dataset, drop `externalId` and the read-only fields (`_userId`, `_syncId`, `enableAllDataElements`, `userActionRequired`, `mismatchSyncConnection`), change what you need, send it back.
- **Nothing is checked against the source at save.** An `externalId` or a column name that isn't in the catalog saves without complaint. Take every `externalId` from the catalog and every column name from the column read.
- **The API saves only what you send.** Selecting a few tables doesn't create disabled datasets for the rest of the catalog.
- **There is no dataset delete.** Set `enable: false`; the dataset stays configured and is skipped by runs.
- **Table names are unique per sync.** An exact duplicate is refused at save. A name that differs only in case saves, but enabling a dataset whose table name matches another's, ignoring case, is refused ("Another dataset in this sync resolves to the same destination table").

Per-dataset fields:

| Field | Meaning |
|---|---|
| `enable` | Replicate on each run. `true` needs an `ingestionMode` |
| `ingestionMode` | `append` adds each run's records and keeps prior rows; `replace` drops and reloads the table each run; `merge` upserts by primary key and needs an enabled `isPrimaryKey` column |
| `tableName` | Destination table name; required for export-backed datasets. Omit to let the platform derive one |
| `exportProperties` | Catalog datasets only: `type: "delta"` (changed records since the last run) or `"all"`, and `delta.dateField` -- one of the column read's `deltaFields` (Salesforce derives it). NetSuite saved searches also need `netsuite.recordType` |
| `dataElements` | Per-column `enable`, `mask`, `isPrimaryKey`, and `transformMode` (`preserve`, `flatten`, `normalize`) with `children` for nested fields. Omit to replicate every column; when sent, it replaces the whole selection |
| `driftPolicy.element` | Overrides the sync's column drift policy for this dataset |

`mask: true` masks a column's values before they load, so the raw values never reach the warehouse; a primary-key column can't be masked, and `transformMode` is only valid on a field with `children`.

### Schema drift

`driftPolicy` says what happens when the source changes between runs:

- `dataset.added` -- tables that appear in the source: `automate` adds and replicates them, `ignore` leaves them out until someone enables them. `dataset.removed` is always `automate`.
- `element.added` -- new columns: `automate` or `ignore`. With `automate`, `objectAdded` (`preserve` or `flatten`) and `arrayAdded` (`preserve` or `normalize`) shape new nested fields; either one with `ignore` is refused. `removed`, `reduced` and `expanded` are always `automate`.

A sync created through the API starts at `dataset.added: "ignore"` with an empty element policy -- read it back, since a sync built another way may hold `automate`. With `automate`, every table the policy adds loads rows that count against the Data Ingestion volume. A full update that omits `driftPolicy`, or sends an empty `dataset` block, keeps the stored `dataset.added` but clears the element settings, so returning to `ignore` takes an explicit `ignore`. What the policy applies is logged as `Schema Drift` events; drift it doesn't automate sets `userActionRequired` on the dataset, which blocks updates to it until resolved in the UI.

### Runs, jobs, errors, and events

A run is queued and returns at once with `syncId` and `flowExecutionGroupId` (the run's correlation key). One run at a time per sync. A normal run is incremental over every enabled dataset; a **resync** drops the delta checkpoint and reloads everything; either can be scoped to some datasets (`datasetIds`), though a scoped normal run is refused unless the account has partial normal sync.

- **Sync jobs** -- one parent job per run (`queued`, `running`, `canceling`, then `completed`, `failed` or `canceled`) with `numExtractedRecords`, `numLoadedRecords`, `numErrors`, `runType`, and a per-table family of child jobs. Job records are kept about 30 days (`purgeAt`).
- **Run errors** -- read-only diagnostics per run: `stage`, `scope`, `source`, `code`, `message`, and the table (`_datasetId`, `tableName`, `_childSyncJobId`). They can't be retried or resolved: fix the cause and run again. A run checks its connections before it extracts, so an unreachable warehouse fails it at stage `init` with `di_ping_failure`.
- **Events** -- `Schema Drift` and `Data Catalog` entries with a `severity`, filterable by run (`flowExecutionGroupId`), table and time; kept for the account's data-retention period.

### The Data Ingestion license

Read the license's `di` block, not a tier table: `enabled`, `volume` (monthly loaded rows included with the edition), `volumeAddOn` (a purchased volume pack), `disableOverage`, and `histLoadEndDate` (a pack's historical-load window). The license is checked when a sync is **enabled**, not when it's created:

- No Data Ingestion entitlement -- enabling is refused (`di_subscription_required`).
- Without a volume pack, each environment can have **one enabled sync** -- enabling another is refused ("You have reached your limit of active syncs. Disable an existing sync or purchase a Data ingestion volume pack to enable more.").
- Past the month's volume while overage is disabled, or past the raised cap during a volume pack's historical-load window -- enabling is refused (`di_usage_limit_exceeded`).

Usage counts records loaded, per sync, per month, and per environment; reading it needs account-administration permission.

## Quick Reference

### Lifecycle

| Stage | What it needs | Refused with |
|---|---|---|
| Container | An integration created with `syncs: true` | -- |
| Draft | `_integrationId` and `source._connectionId` (a real connection). The draft is `disabled: true`, `destination: {}`, `name: ""` | "To create sync integration id is required..." / "Source connection is missing in the request" / "...either flows or syncs but not both." |
| Datasets | One bulk PUT; `externalId` to create, `_id` to update | See Datasets |
| Destination | `_connectionId`, `database`, `schema` together | Type, partial-block, identifier and uniqueness messages under Destinations |
| Enable | Source, complete destination, `historicDateTime`; the license | "Sync can be enabled only when source, destinations are properly defined." / the limit messages |
| Run | A saved destination; enabled; nothing queued or running | "The flow is not present in the sync." / "Sync disabled..." / "Another instance for this sync is already queued or running..." |
| Delete | `disabled: true` | "Cannot delete an enabled sync..." |

## Related Skills

- **building-flows** ([What Starts a Flow](../building-flows/SKILL.md#what-starts-a-flow)) -- app-to-app, per-record, event-driven and warehouse-to-app work, where a sync doesn't fit
- **configuring-exports** ([Quick Reference](../configuring-exports/SKILL.md#quick-reference)) -- the export behind an export-backed dataset
- **configuring-connections** ([Quick Reference](../configuring-connections/SKILL.md#quick-reference)) -- the source connection and the warehouse (`rdbms`) connection a destination uses
- **managing-integrations** ([Quick Reference](../managing-integrations/SKILL.md#quick-reference)) -- integrations, notifications, and the recycle bin
- **getting-started** ([Working on a Live Account](../getting-started/SKILL.md#working-on-a-live-account)) -- confirming the account before the first write

<!-- TIER:2 -->

## How to Build a Sync

### 1. Confirm it's a sync, and read the license

Walk Sync or Flow? above with the user's request. Then read the license's `di` block: `enabled` must be true, and without a volume pack an environment that already has an enabled sync can't enable another. List the account's syncs to see what's enabled where. Read the supported sources and destinations rather than assuming them.

### 2. Find or create the sync integration

List the integrations and pick one created with `syncs: true` whose syncs load into the same kind of warehouse; otherwise create one with `syncs: true` in the create body. Never try to add the flag to an existing integration -- the update answers 200 and keeps its value.

### 3. Pick the source connection and read its catalog

Find the source connection (configuring-connections), then read its catalog. A non-empty `datasets` list is the menu of tables; an empty one means export-backed datasets only -- the same response lists the connection's exports. Agree with the user which tables to replicate.

### 4. Create the draft sync

Create the sync with `_integrationId` and `source._connectionId`, plus a `name`. It's created disabled, with an empty destination. Read it back and check `driftPolicy`.

### 5. Choose the datasets

Read each chosen table's columns, scoped to the draft sync: names, types, constraints, and `deltaFields`, the columns usable as a delta cursor (for an export-backed dataset, the export's record structure). The column read asks the source application live, so it needs a working connection.

Then build one batch: an item per table with `externalId` (from the catalog), a `name`, `enable`, an `ingestionMode`, and the `dataElements` you want (from the column read), or leave `dataElements` out to take every column. For `merge`, mark the key columns `isPrimaryKey`. For delta extraction on a catalog dataset, set `exportProperties: {type: "delta", delta: {dateField: <one of deltaFields>}}`, or `type: "all"` when there's no usable cursor. An export-backed item takes `isExport: true`, `externalId` set to the export's `_id`, a `tableName`, and an explicit `dataElements` list, and no `exportProperties`.

Create the datasets disabled (`enable: false`) while you review them if you prefer; to change one later, send it whole by `_id` (Datasets above). Read the datasets back after every batch.

### 6. Set the destination

Ask which warehouse connection, database and schema to use -- never invent them. Check that the connection's type matches the integration's other syncs, that no other sync uses the same database and schema, and that the connection is online. Then save the three together. The save connects to the warehouse and creates the schema if it's missing, so it can take a while; if it fails, fix the connection.

### 7. Set the schedule, backfill start, and drift policy

- `historicDateTime` -- the earliest record time to backfill from; required before enabling.
- `schedule` -- a 6-field cron with seconds (`"? 0 */6 * * *"`) evaluated in `timezone` (IANA); leave both out for on-demand runs.
- `driftPolicy` -- keep `dataset.added: "ignore"` unless the user wants new source tables replicated automatically; choose `element.added` the same way.

Each is a field of the sync, and every update of the sync replaces the whole document: send it complete (step 9 explains why `disabled` must be in it).

### 8. Review columns for personal data

Before the first run, when nothing has loaded yet, go through each dataset's columns with the user and set `mask: true` on personal data -- email, phone, address, birth date, government and tax ids, bank and card numbers, salary, health -- and on custom fields named like them. Masking can't be combined with a primary key.

### 9. Enable, then run

Enable by sending the sync with `disabled: false`. **Every full update must carry `disabled`:** the PUT replaces the document, and a complete sync whose update leaves `disabled` out comes back enabled, and an enabled sync runs on its schedule. An incomplete sync is refused; so is one the license doesn't cover.

Run it on demand (or wait for the schedule). The run returns at once; one run at a time. Use a resync, or a run scoped to some datasets, when a table needs reloading -- see Sync Operations.

### 10. Watch the first run

Poll the run's sync job until it ends, then read its table family for per-table counts, its errors, and the run's events. Compare `numExtractedRecords` with `numLoadedRecords`: the gap is records that failed to load. A `di_ping_failure` at stage `init` means the run couldn't reach a connection's host -- fix that connection and run again.

## Sync Operations

The operations on a sync beyond building it. Each reference lists its calls under these same headings and names the ones its surface lacks.

- **Read and write** -- list syncs (all, or one integration's), read one, create, replace the whole document, change fields, read its audit log; read, create and update datasets in bulk; read the catalog, columns, sources and destinations
- **Run** -- a normal run, a resync, or either one scoped to chosen datasets
- **Monitor runs** -- list a sync's jobs (by created date), read one, read its per-table family, read its errors (all, or one table's), list the latest job of each sync in an integration, read the sync's events
- **Cancel** -- cancel one job, or every queued and running job of a sync. Cancel is asynchronous: the job shows `canceling`, then `canceled`
- **Pause, change, delete** -- disable to pause (the configuration is kept); delete a disabled sync for good; its datasets go with it
- **Usage and notifications** -- records loaded per sync this month, per month against the license, per environment; subscribe a user to a sync's failure notifications

<!-- TIER:3 -->

## Pre-Submit Checklist

- [ ] The request is a sync, not a flow (a listed warehouse destination, no per-record logic, nothing event-driven or warehouse-to-app)
- [ ] `license.di.enabled` is true, and enabling won't exceed the environment's enabled-sync limit
- [ ] The integration was created with `syncs: true`, and its syncs share this sync's warehouse type
- [ ] Every `externalId` came from the catalog and every column name from the column read
- [ ] Each update item is the whole dataset (`name`, `tableName`, `exportProperties`, `ingestionMode`, `dataElements`), without `externalId`
- [ ] Every `merge` dataset has an enabled, unmasked primary-key column; table names are unique per sync, ignoring case
- [ ] Personal-data columns are masked before the first run
- [ ] The destination's connection, database and schema were confirmed with the user and are sent together; the database exists; no other sync uses the database and schema
- [ ] `driftPolicy.dataset.added` is what the user chose
- [ ] Every full update of the sync carries `disabled` explicitly, plus `historicDateTime`, `schedule`, `timezone`, `destination` and `driftPolicy`
- [ ] Each write was read back

## Gotchas

1. **A full update can enable the sync.** The PUT replaces the document, and a complete sync whose update leaves `disabled` out comes back `disabled: false`, and an enabled sync runs on its schedule. Send `disabled` on every full update.
2. **The PUT clears what it omits.** `schedule`, `timezone`, the destination and the element drift settings go when left out; `description` and `historicDateTime` stay. `dataset.added` keeps its value when omitted, so switching back from `automate` needs an explicit `ignore`. Read, modify, write the whole document.
3. **A partial dataset update wipes fields.** An update item replaces `name`, `tableName` and `exportProperties`; `{_id, enable: false}` leaves the dataset with no table name -- even an export-backed one, whose create requires it.
4. **The datasets PUT isn't an upsert, and it's all or nothing.** Re-creating an existing `externalId` fails the batch, and one bad item rejects the valid ones with it.
5. **Selections aren't verified at save.** Made-up table and column names save fine; only the catalog and the column read are ground truth.
6. **A typo in the schema creates a schema.** Saving the destination creates a missing schema in the warehouse instead of failing. The database, by contrast, must exist.
7. **A database and schema pair belongs to one sync.** Another sync naming the same pair -- in any case, on any host or warehouse type -- is refused with "Duplicate destination host found".
8. **One warehouse type per integration, and per sync for good.** Mixing types in an integration is refused, and a saved destination can't change type.
9. **The container can't be converted.** `syncs: true` is set at creation only; an update answers 200 and ignores it. And a flow created in a sync integration is accepted -- don't put one there.
10. **Deleting a sync is permanent.** It must be disabled first, it never enters the recycle bin, and its datasets go with it. An integration can't be deleted while it holds a sync, and once its syncs have run, the deleted integration can't be purged from the recycle bin while their job records exist (they're kept about 30 days).
11. **Creating a sync changes its connections.** The platform sets `microServices.workerGroup: "DIWorker"` on the source and destination connections and registers them on the integration; deleting the syncs that use a connection clears it. Expect these `system` changes in the connections' audit logs.
12. **The license bites at enable, not create.** Any number of syncs can be built; without a volume pack only one can be enabled per environment.
13. **Sync errors have no retry.** They're read-only diagnostics of a run: fix the cause and run again, scoped to the failed datasets where the account allows it.
14. **An empty catalog isn't an empty source.** It means the connection only supports export-backed datasets.

## Common Errors

The platform's message comes first; the code follows where the API publishes one.

| Error | Cause | Fix |
|---|---|---|
| 422 "An integration is suppose to have either flows or syncs but not both." (`integration_not_for_sync`) | The sync's integration wasn't created with `syncs: true` | Create a new integration with `syncs: true`; an existing one can't be converted |
| 422 "Source connection is missing in the request" (`missing_source_connection`) | `source._connectionId` is missing, or isn't a connection's id | Send a real connection id; an update needs it too |
| 422 "Sync can be enabled only when source, destinations are properly defined." (`sync_not_enabled`) | Enabling without a complete destination or `historicDateTime` | Save the destination and `historicDateTime`, then enable |
| 422 "You have reached your limit of active syncs..." (`di_sync_limit_exceeded`) | The environment already has an enabled sync and the license has no volume pack | Disable the other sync, or the account needs a Data Ingestion volume pack |
| 422 "Invalid destination type and please provide the valid destination type" (`invalid_destination_type`) | The destination connection isn't a supported warehouse type | Use a warehouse connection whose type the destinations list names |
| 422 "SQL Server database is required on sync destination" / "... schema is required ..." (`invalid_destination_sync_config`) | A partial destination block | Send `_connectionId`, `database` and `schema` together |
| 422 "SQL Server schema name is invalid: ..." (`invalid_destination_sync_config`) | The name breaks SQL Server's identifier rule | A letter or underscore first; letters, digits, `_` or `$`; 128 characters at most |
| 422 "Duplicate destination host found" (`duplicate_destination_host`) | Another sync, in any integration, uses the same database and schema, ignoring case | Use a schema of this sync's own |
| 422 "The destination type for all the syncs under an integration must be same." | The integration's other syncs load into another kind of warehouse | Put this sync in an integration for that warehouse type |
| 422 "Destination connection type is not same as the previous destination connection type" | Changing a saved destination to another warehouse type | Build a new sync for the other warehouse |
| 404 "The flow is not present in the sync." (`sync_flow_not_present`) | Running a draft whose destination was never saved | Save the destination, enable, then run |
| 422 "Sync disabled. Please enable your sync and try again." (`invalid_sync`) | Running a disabled sync | Enable it first |
| 409 "Another instance for this sync is already queued or running..." (`sync_job_already_queued`) | A run is already queued or running | Wait for it, or cancel it |
| 400 "Cannot delete an enabled sync. Please disable the sync before deletion." (`sync_delete_not_allowed`) | Deleting an enabled sync | Disable it, then delete |
| 400 "For creation externalId should be provide and for update dataset id should be provided but not both." (`dataset_externalId_id_required`) | An item has both `_id` and `externalId`, or neither | Create with `externalId` only, update with `_id` only |
| 400 "... datasets requested to create are already present. Kindly provide new datasets" | Creating an `externalId` the sync already has | Update that dataset by its `_id` instead |
| 400 "Connection is different for the sync and the export dataset." (`connection_mismatch`) | The export behind an export-backed dataset runs on another connection | Use an export on the sync's source connection |
| 422 "ingestionMode field is required for enabled datasets." (`ingestion_mode_required_for_enabled_datasets`) | `enable: true` with no `ingestionMode` | Set `append`, `replace` or `merge` |
| 422 "You must select a primary key for a merge operation." | `merge` with no enabled `isPrimaryKey` column | Mark the key column(s) |
| 422 "`<column>` cannot have both isPrimaryKey and mask set as true" | A masked primary key | Unmask the key column, or choose another key |
| 400 "Table names should be unique..." (`duplicate_dataset_table_names`) / 422 "Table name - `<name>` already exists for a datasets." (`table_name_already_exists`) | Two datasets with one `tableName` | Give each dataset its own table name |
| 422 "Another dataset in this sync resolves to the same destination table..." | Enabling a dataset whose table name matches another's, ignoring case | Rename one of them |
| 422 "Drift policy element.added should be automate if element.arrayAdded/objectAdded is present" (`drift_policy_invalid_setup`) | `objectAdded` or `arrayAdded` with `element.added: "ignore"` | Drop them, or set `element.added: "automate"` |
| Run error `di_ping_failure` at stage `init` ("Unknown host: ...") | The run couldn't reach a connection's host | Fix the connection, then run again |
| 403 "The job `<syncJobId>` is already in terminal state..." (`sync_job_not_cancellable`) | Canceling a finished job | Nothing to cancel |
| 422 "sync `<syncId>` must be deleted before you can delete integration `<integrationId>`" | Deleting an integration that holds syncs | Disable and delete its syncs first |
| 422 "this document is referenced by ParentSyncJob : `<syncJobId>`" on a recycle-bin purge | The integration's syncs ran, and their job records outlive them | Purge again after the jobs' `purgeAt` (about 30 days after each run); no route deletes job records |
