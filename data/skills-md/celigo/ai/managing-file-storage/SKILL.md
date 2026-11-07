---
name: managing-file-storage
description: Manage Celigo Storage -- the file and folder store built into integrator.io that flows, MCP servers, trading partners and people share -- plus Storage Query (read-only SQL over stored files) and the Celigo-hosted SFTP file server. Covers stable item ids, integration system folders, upload, move, copy, merge and replace, the recycle bin and the storage quota. Use when uploading, finding, organizing, restoring or purging stored files, reading the storage quota, querying a stored CSV, JSON or Parquet file, or giving a trading partner SFTP access.
---

<!-- TIER:1 -->

# Managing File Storage

Celigo Storage is file storage built into integrator.io: files and folders an account keeps next to its integrations, with no S3 bucket or SFTP host of its own. Four kinds of consumer share it:

- **Flows** read and write storage folders through file steps on a Celigo APIs connection
- **MCP servers** publish a stored file as a read-only resource
- **Trading partners** log in to the Celigo-hosted SFTP file server; each partner account is rooted in a storage folder
- **People** upload, download, and organize files

Two add-ons sit on top: **Storage Query** runs one read-only SQL `SELECT` over stored files ([references/storage-query.md](references/storage-query.md)), and the **file server** gives partners SFTP logins into storage folders ([references/file-server.md](references/file-server.md)).

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Manage Stored Files below:

- **Celigo MCP tools** (`list_storage_items`, `upsert_storage_item`, `restore_storage_item`, `get_storage_file_download_url`, `cancel_storage_upload`, `delete_resource`) -- [references/mcp.md](references/mcp.md)
- **The `celigo` CLI** (`celigo storage`, `celigo recycle-bin`, `celigo file-server`) -- [references/cli.md](references/cli.md)

Storage Query and the file server have no MCP tools: use the CLI or the REST API.

Listing, searching, reading metadata, downloading, reading the quota, and running a Storage Query only read. Uploading, replacing content, creating folders, renaming, moving, copying, merging, deleting, restoring, and purging write to the account. A purge can't be undone, and neither can a content replace once it finalizes.

## The Storage Model

### Items are addressed by id, not by path

Every file and folder has an `_id`; files and folders share one id space. Everything that points at storage pins that id: a flow step's folder, an MCP server's `resources[]._fileId`, a partner account's `_homeFolderId`.

- **Rename, move, and content replace keep the `_id`**, so references keep working. A restore from the recycle bin keeps it too.
- **Copy creates a new `_id`.** So does deleting a file and uploading a new one with the same name: old references don't follow it. To change a referenced file, replace its content.
- **Names are unique among the live items of one folder** -- files and folders share the namespace, matching is case-sensitive, and a pending upload already holds its name. A duplicate is refused with 409 `STORAGE_ITEM_ALREADY_EXISTS`. A deleted item releases its name.
- **Paths are names.** A path such as `/Order to cash/inbound/orders.csv` is built from folder names. Storage Query, path-scoped API tokens, and the `custom` scope of a Celigo APIs connection match paths, so renaming or moving a folder changes what those paths reach.

### Integration (system) folders

Creating an integration creates a folder at the storage root named after it, with `isSystem: true`, the integration's `_integrationId`, and `integrationName`.

- **The folder itself is protected.** Renaming, moving, copying, deleting or purging it is refused with 403 `STORAGE_SYSTEM_ITEM_PROTECTED` ("System items cannot be modified or deleted").
- **Everything inside it is ordinary.** Folders and files created in it carry its `_integrationId`; moving an item in or out sets or clears it.
- **It follows the integration.** Deleting the integration sends the folder and everything in it to the recycle bin, and purging the integration from the bin purges the folder too. Before deleting an integration, move out any files that must outlive it.

### Content, environment, and quota

Stored files belong to the environment they were created in, and nothing crosses environments ([getting-started > Sandbox vs Production](../getting-started/SKILL.md#sandbox-vs-production)). The quota is one figure for the whole account:

| Field | Meaning |
|---|---|
| `activeUsage` | Bytes of active and pending files |
| `recycleBinUsage` | Bytes of deleted files still in the recycle bin |
| `totalUsage` | The two together -- the figure checked when anything is uploaded |
| `maxAllowedUsage` | The licensed allowance |
| `hardLimit` | Allowance plus the licensed overage buffer (the allowance itself when overage is disabled). At it, uploads fail with `STORAGE_QUOTA_EXCEEDED` |
| `isOverage`, `overage` | Whether, and by how many bytes, `totalUsage` is past the allowance |

Folders cost nothing. A copy costs its size. Moves and renames change nothing. **A delete changes nothing either**: the bytes move from `activeUsage` to `recycleBinUsage` and still count until the item is purged (or the 30 days run out). The usage is also reported per environment.

### Uploads and the pending state

Bytes never pass through the API: an upload or replace returns short-lived presigned S3 URLs, and the bytes go straight to them -- one PUT for up to 5 GB, a multipart upload beyond that. A file starts `pending` and turns `active` once its bytes land, usually within seconds. While it's pending it can't be downloaded, moved, copied, renamed, or queried, and it holds its name and reserved quota. A multipart upload of a new file that's abandoned stays pending until it's cancelled.

### Access

Access is checked per item: an item the caller can't reach answers 403, and a merge, for example, needs delete access on the source folder and write access on the destination. Two credentials can be confined to folder paths:

- **A service API token**, with `_fileStoragePaths` -- up to seven paths, each starting and ending with `/`, each granting that folder and everything beneath it. It's exclusive with full access ([managing-api-tokens](../managing-api-tokens/SKILL.md)).
- **A Celigo APIs connection** with `accessScope.type: "custom"` and `accessScope._fileStoragePaths` -- prefixes, with `/` granting everything and no wildcards. A `custom` scope with no paths has no storage access.

Both match folder names, so renaming a granted folder breaks the grant.

## Quick Reference

### Which Operation

| You want to | Operation | `_id` | Notes |
|---|---|---|---|
| Change a file's bytes and keep every reference | Replace content | kept | No undo once it finalizes; the previous content stays downloadable until then |
| Rename or describe | Rename | kept | Only `name` and `description` are editable |
| Put an item in another folder | Move | kept | A folder's contents re-anchor asynchronously; quota unchanged |
| Get a second, independent file | Copy | new | Files only; default name `Clone - <name>`; costs its size |
| Fold one folder into another | Merge | kept, unless the name collides | Folders only; runs as a background job. A same-name file overwrites the destination's file, and the source file's `_id` is lost; the source folder is removed, not sent to the bin |
| Remove, recoverably | Delete | -- | 30 days in the recycle bin; still counts toward the quota |
| Undo a delete | Restore | original | 409 when the name was taken meanwhile: restore under a new name |
| Free the space for good | Purge | -- | Irreversible; a folder's subtree goes with it |

### Item Fields

| Field | Meaning |
|---|---|
| `_id` | The item's identity -- what every reference holds |
| `type` | `file` or `folder`, fixed at creation |
| `name`, `description` | The only editable fields (`name` up to 256 characters, `description` up to 1000) |
| `_parentId` | The containing folder; `null` at the account root |
| `_integrationId`, `integrationName` | The integration whose system folder holds the item (`integrationName` only on the system folder itself) |
| `isSystem` | `true` on platform-created, protected folders |
| `status` | `pending` until an upload or replace lands, then `active` |
| `size`, `mimeType` | Bytes (always `0` for folders) and the media type recorded at upload |
| `deletedAt`, `deletedBy` | Recycle-bin items only: when, and by whom -- a user id, or `cascadeDelete` for a descendant of a deleted folder |

## Related Skills

- **configuring-exports** ([Quick Reference](../configuring-exports/SKILL.md#quick-reference)) -- reading a storage folder in a flow (`HTTPExport` in file mode), `file.skipDelete`
- **configuring-imports** ([Quick Reference](../configuring-imports/SKILL.md#quick-reference)) -- writing files to a storage folder (`HTTPImport` in file mode)
- **configuring-connections** ([Quick Reference](../configuring-connections/SKILL.md#quick-reference)) -- the Celigo APIs connection a storage step runs on
- **building-mcp-servers** ([How to Build an MCP Server](../building-mcp-servers/SKILL.md#how-to-build-an-mcp-server)) -- publishing a stored file as an MCP resource
- **building-b2b** ([Quick Reference](../building-b2b/SKILL.md#quick-reference)) -- parsing EDI files that partners drop on the hosted SFTP server
- **managing-api-tokens** ([Access Scope Decision Matrix](../managing-api-tokens/SKILL.md#access-scope-decision-matrix)) -- tokens confined to storage folder paths
- **managing-integrations** ([Quick Reference](../managing-integrations/SKILL.md#quick-reference)) -- what deleting or restoring an integration does to its contents

<!-- TIER:2 -->

## How to Manage Stored Files

### 1. Find the item and its id

List a folder's direct children (the account root by default), or search names across the whole account. Search matches any word of the query -- hyphens split words -- so a specific name returns unrelated hits as well: confirm the hit by its containing folder (`location`), or list that folder. An integration's files sit under its system folder: list the root and match `_integrationId`.

Read a file's metadata, including its `path` breadcrumb, by id. Folder metadata comes from the listing of the folder's parent.

### 2. Check the quota before a large upload

Read the account's usage: compare `totalUsage` with `hardLimit` (and `maxAllowedUsage` for the overage buffer). If space is short, purge what the recycle bin holds (step 7) before uploading -- deleting alone frees nothing.

### 3. Upload a file or create a folder

Name the destination folder by id; omit it for the account root. A name already held by a live item in that folder is refused (409) -- to update that file, replace its content instead (step 5). Read the item back until its `status` is `active` before you use it.

### 4. Organize: rename, move, copy, merge

- **Rename** changes `name` (and `description`); the `_id` stays.
- **Move** re-parents an item -- one, or up to 100 at once. A name collision in the destination is refused; send a new name in the same move. A folder can't move into itself or a descendant, and an item can't "move" to the folder it's already in.
- **Copy** duplicates a file into a folder under a new `_id`. Name it when the destination already holds a `Clone - <name>` file.
- **Merge** moves a folder's contents into another folder, then removes the source folder. It runs in the background and returns a job receipt, so list the destination to see it finish. A file whose name is free in the destination keeps its `_id`. A file whose name the destination already holds overwrites that file: the destination file keeps its `_id` but takes the source's content, the old content is gone, and the source file's `_id` disappears -- nothing goes to the recycle bin. List both folders and compare names before merging.

### 5. Replace a file's content (keep every reference)

Replace the bytes of an existing file: its `_id`, name, folder, and every reference stay. The file is `pending` until the new bytes land, and the old content stays downloadable until then. After that the old bytes are gone -- the recycle bin covers deletes, not replaces -- so copy or download the file first if the old content may be needed. A second replace started while one is in flight is refused with 409 `STORAGE_ITEM_REPLACE_CONFLICT`.

### 6. Download a file or a whole folder

A file downloads from a short-lived presigned URL; `expiresIn` gives its lifetime in seconds. A whole folder downloads as one zip, built before the response and rooted at the folder's name; pending files are skipped. Treat a presigned URL as a credential while it lives: hand it to the user or fetch it promptly, and never log or store it.

### 7. Delete, restore, purge

**Before deleting, find what uses the item** -- no public check lists it, and a delete is never blocked by references: flow steps and tokens that point at the item are left dangling and fail at run time. Look for the item's id in flow steps on Celigo APIs connections that read or write its folder, in MCP servers' `resources[]._fileId`, and in file-server partner accounts' `_homeFolderId`. The one block: a folder that is, or contains, a partner account's home folder is refused with 403 `STORAGE_SFTP_HOME_FOLDER_PROTECTED` until that account is deleted or re-pointed.

- **Delete** sends the item to the recycle bin for 30 days. A folder's delete takes its whole subtree; the bin then lists only the folder, and its descendants come back or are purged with it.
- **Restore** returns an item to its original folder with its original `_id`; a folder brings back what was deleted with it, its contents following asynchronously. A descendant removed by its folder's delete can't be restored on its own -- restore the folder. If a live item took the name meanwhile, the restore is refused with 409 `STORAGE_ITEM_ALREADY_EXISTS` and the item stays in the bin: restore it under a new name, or rename the item that took it.
- **Purge** deletes a bin item for good and frees its bytes; purging a folder purges its subtree. Purge only what the user has confirmed.

Deleted storage items appear in the account's recycle bin as `StorageItem` entries, but they're restored and purged through Celigo Storage -- the bin's generic routes refuse them. `deletedAt` and `deletedBy` on a bin entry say when and by whom an item was deleted.

### 8. Use stored files in a flow

A flow reaches Celigo Storage through a **Celigo APIs connection** (`assistant: "integratorceligoapi"`) and file steps in folder mode -- `HTTPExport` or `HTTPImport` with `http.type: "file"` -- that address a folder, never a single file. The step shapes are in **configuring-exports** and **configuring-imports**.

- **The connection needs `accessScope` on create**: for storage, `type: "custom"` with the `_fileStoragePaths` the flow uses. The connection document never carries the scope; it's read from `GET /v1/accessScope/connections/{_id}`. A `custom` scope without paths makes every storage step fail with 401 at run time.
- **A file-mode export deletes each source file after it processes it successfully**, unless `file.skipDelete` is `true`. Set it when anything else still needs the file: a second flow, a partner downloading from that folder, or a file an MCP server publishes.
- **EDI** parses from a storage folder like any file transport: put the EDI profile (`_ediProfileId`) on the file-mode export ([building-b2b](../building-b2b/SKILL.md)).

### 9. Query a file with SQL

Storage Query runs one read-only `SELECT` over stored CSV, TSV, JSON, NDJSON, or Parquet files, without downloading them or building a flow. It needs its own license entitlement, and every submit draws on an account-wide rate budget. See [references/storage-query.md](references/storage-query.md).

### 10. Give a trading partner SFTP access

The file server gives each partner an SFTP login rooted in a storage folder: what a partner uploads lands there, and what you put there is what the partner can download. It needs a license add-on and a full-access API token, and partner passwords never pass through chat. See [references/file-server.md](references/file-server.md).

<!-- TIER:3 -->

## Pre-Submit Checklist

- [ ] The item was found by `_id`, and a search hit was confirmed by its folder -- never acted on by name alone
- [ ] To change a referenced file, you're replacing its content, not deleting and re-uploading it
- [ ] The old content of a file you're replacing is copied or downloaded, if anyone may need it
- [ ] Before a delete or a folder move: what references the item (flow steps, MCP server resources, partner home folders) is known, and the user confirmed
- [ ] A purge is confirmed by the user, item by item
- [ ] Before a merge: no file name exists in both folders, or the user accepts that the source's file overwrites the destination's
- [ ] Before a large upload: `totalUsage` plus the file fits under `hardLimit`
- [ ] A flow that reads a storage folder that anything else also uses sets `file.skipDelete: true`
- [ ] A Celigo APIs connection for storage carries `accessScope` with the folder paths it needs
- [ ] An upload or replace has finished (`status: "active"`) before the file is used

## Gotchas

1. **Delete plus re-upload is a new item.** The new file gets a new `_id`, and every reference to the old one dangles. Replace the content instead; a restore from the bin keeps the old `_id`.
2. **Deleting frees no space.** Deleted bytes count toward the quota until they're purged (or expire after 30 days). To get under the limit, purge.
3. **A replace has no undo.** Once the new bytes land, the old ones are gone: the recycle bin only holds deleted items.
4. **References don't block a delete.** Flow steps and tokens pointing at the item go dangling, and no public dependency check lists what uses it. Only a partner's home folder refuses deletion.
5. **The integration's folder goes with the integration.** Deleting an integration sends its system folder and all its files to the recycle bin, and purging the integration purges them.
6. **A file-mode export deletes what it reads.** `file.skipDelete` defaults to `false`; a folder shared with another flow, a partner, or an MCP server needs `true`.
7. **Paths are names, ids are identities.** Storage Query paths and the folder paths on tokens and Celigo APIs connections stop matching when a folder is renamed or moved; references by id don't.
8. **Search is broad.** It matches any word of the query, across the whole account. Confirm a hit by its folder before acting on it.
9. **Pending items are locked.** Until an upload or replace lands, the file can't be downloaded, moved, renamed, copied, or queried. An abandoned multipart upload of a new file holds its name and quota until cancelled; never cancel a replace.
10. **Merge overwrites and removes without the bin.** A same-name file replaces the destination file's content, and the source file's `_id` disappears; the source folder is removed outright. None of it goes to the recycle bin, so compare the two folders' names and check what referenced the source folder and its files by id first.
11. **System folders can't be touched.** Not renamed, moved, copied, deleted, or purged -- not even by an administrator. Work inside them.

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| 409 `STORAGE_ITEM_ALREADY_EXISTS` | A live item in that folder has the name (an upload, create, rename, move, copy, or restore) | Pick another name, move or copy with a new name, restore under a new name -- or replace the existing file's content |
| 403 `STORAGE_SYSTEM_ITEM_PROTECTED` ("System items cannot be modified or deleted") | The item is an integration's system folder | Work inside the folder; it goes away with its integration |
| 403 `STORAGE_SFTP_HOME_FOLDER_PROTECTED` | The folder is, or contains, a file-server partner's home folder | Delete the partner account or point it at another folder first |
| 403 `STORAGE_PRESIGNED_URL_ACTIVE` | Deleting a pending single-PUT upload whose URL is still live | Wait for the URL to expire, then delete |
| 409 `STORAGE_ITEM_REPLACE_CONFLICT` | Another replace of the file is still in flight | Wait for it to finish, then replace again |
| `STORAGE_QUOTA_EXCEEDED` | `totalUsage` reached `hardLimit` | Purge the recycle bin or delete and purge files; then retry |
| 404 `STORAGE_PARENT_NOT_FOUND` ("Parent folder not found") | The folder id names nothing in this environment -- deleted, merged away, or from another environment | Find the folder again by listing |
| 422 `STORAGE_PARENT_NOT_FOLDER` | A file's id was given where a folder belongs | Use the containing folder's id |
| Item stuck `pending` | An upload or replace never completed | A new file: cancel it if it was a multipart upload, or delete it once its upload URL has expired, then upload again. A replace: the file keeps its previous content -- run the replace again (409 `STORAGE_ITEM_REPLACE_CONFLICT` means the abandoned one hasn't expired yet) |
| A storage step fails with 401 at run time | The Celigo APIs connection's `custom` scope has no `_fileStoragePaths`, or none covering the folder | Add the folder's path to the connection's scope |
