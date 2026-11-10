---
name: email
description: "Read, search, compose, organize and synchronize email with a local SQLite cache. Use when managing email or searching cached messages."
license: "MIT"
compatibility: "Release binary ghostpaw-email (no runtime needed); MCP stdio via ghostpaw-email mcp."
---

# email

## Install

Linux/macOS (checks SHA256SUMS and installs ~/.local/bin/ghostpaw-email):

```sh
curl -fsSL https://raw.githubusercontent.com/GhostPawJS/email/main/install.sh | sh
```

Windows x64:

```powershell
irm https://raw.githubusercontent.com/GhostPawJS/email/main/install.ps1 | iex
```

Run tools as `ghostpaw-email ...`; use `~/.local/bin/ghostpaw-email` if it is not on PATH.

Read and search cached email offline. Configure live accounts with email account add before network operations. Inspect messages before replying or changing folders. Confirm recipients and content before sending; trash and folder deletion can remove mail. Credentials use the existing email CLI account configuration or EMAIL_* environment variables.

## Running inside sandboxed agent harnesses

Inside a Codex CLI `--sandbox workspace-write` session, the database and its
parent directory must be inside a writable root, including SQLite's `-wal` and
`-shm` side files. A default DB under `~/.ghostpaw` outside those roots can fail
with `SQLITE_CANTOPEN` or `EPERM` (often exit 70; directory creation failures
may exit 2), even when normal shell permissions allow access. Put the DB inside the workspace with `--db ./state/email.db`,
or set `GHOSTPAW_EMAIL_DB="$PWD/state/email.db"` for CLI/MCP use.

To use an external DB directory, add it when starting the OpenAI Codex CLI
(replace `<dir-with-db>` with its absolute path):

```sh
codex exec --sandbox workspace-write --add-dir <dir-with-db> "Run the GhostPaw CLI"
```

Alternatively, set `sandbox_workspace_write.writable_roots` in
`~/.codex/config.toml` before starting the session:

```toml
[sandbox_workspace_write]
writable_roots = ["/absolute/dir-with-db"]
```


For the compact cheat sheet, run `ghostpaw-email skill --short`.

## Calling tools

MCP: connect to ghostpaw-email, then call a tool by name with its JSON arguments.

CLI: `ghostpaw-email call <tool> '<JSON object>'` or `ghostpaw-email <tool> --parameter value`.

Inspect schemas with `ghostpaw-email describe <tool>`. Use `--db <path>` to select a database.

## mail_read

Read mailbox state: folder list, message queue, thread view, single message body, attachment metadata, or raw EML export.

Use when: Inspect folders, cached messages, threads, attachments or raw message content.

Not for: Use mail_search to find messages by query or mail_organize to change them.

Writes: writes_state.

Nested requirements apply within the parent for the selected action.

| Parameter | Type | Required | Values / description |
| --- | --- | --- | --- |
| view | string | yes | eml. What to read. |
| folder | string | no | Folder path (required for queue/message/attachment/eml). |
| uid | integer | no | Message UID (required for message/attachment/eml). |
| threadId | string | no | Thread ID (required for thread view). |
| partPath | string | no | Part path for a specific attachment (optional for attachment view). |
| limit | integer | no | Maximum messages to return (queue view). |
| unreadOnly | boolean | no | Filter to unread messages only (queue view). |
| refresh | boolean | no | Fetch live folder list from server before returning (folders/queue view). |

Examples:

```sh
ghostpaw-email call mail_read '{"view":"folders"}'
```

## mail_search

Search for messages locally via FTS or remotely via IMAP SEARCH. Returns matching message references.

Use when: Find messages by a local full-text query or a remote IMAP search.

Not for: Use mail_read when the folder and message UID are already known.

Writes: writes_state.

Nested requirements apply within the parent for the selected action.

| Parameter | Type | Required | Values / description |
| --- | --- | --- | --- |
| query | string | yes | Free-text search query or FTS5 expression. |
| folder | string | no | Restrict search to a specific folder. |
| mode | string | no | local, remote. local (default) or remote IMAP SEARCH. |
| since | string | no | ISO date string — only messages after this date. |
| before | string | no | ISO date string — only messages before this date. |
| hasAttachments | boolean | no | Filter to messages with attachments. |
| unreadOnly | boolean | no | Filter to unread messages. |
| limit | integer | no | Maximum number of results. |

Examples:

```sh
ghostpaw-email call mail_search '{"query":"invoice"}'
```

## mail_compose

Compose and send email: send new message, reply, forward, save/update/send a draft.

Use when: Send, reply, forward, or save and manage a draft after its content is agreed.

Not for: Use mail_read to inspect an existing message without sending or saving content.

Writes: writes_state.

Nested requirements apply within the parent for the selected action.

| Parameter | Type | Required | Values / description |
| --- | --- | --- | --- |
| action | string | yes | send_draft. string value. |
| folder | string | no | Source folder (required for reply/forward). |
| uid | integer | no | Source message UID (required for reply/forward/update_draft/send_draft). |
| input | object | no | ComposeInput / ReplyInput / ForwardInput payload. |
| input.from | object | no | Object: address (required), name. |
| input.from.address | string | yes | Email address. |
| input.from.name | string | no | Display name. |
| input.sender | object | no | Object: address (required), name. |
| input.sender.address | string | yes | Email address. |
| input.sender.name | string | no | Display name. |
| input.envelopeFrom | object | no | Object: address (required), name. |
| input.envelopeFrom.address | string | yes | Email address. |
| input.envelopeFrom.name | string | no | Display name. |
| input.replyTo | object | no | Object: address (required), name. |
| input.replyTo.address | string | yes | Email address. |
| input.replyTo.name | string | no | Display name. |
| input.to | array | yes | Recipient addresses. |
| input.to[].address | string | yes | Email address. |
| input.to[].name | string | no | Display name. |
| input.cc | array | no | Recipient addresses. |
| input.cc[].address | string | yes | Email address. |
| input.cc[].name | string | no | Display name. |
| input.bcc | array | no | Recipient addresses. |
| input.bcc[].address | string | yes | Email address. |
| input.bcc[].name | string | no | Display name. |
| input.subject | string | yes | Message subject. |
| input.text | string | no | Plain text body. |
| input.html | string | no | HTML body. |
| input.replyAll | boolean | no | Reply to all original recipients. |
| input.mode | string | no | inline, attachment. string value. |
| input.attachments | array | no | Message attachments. |
| input.attachments[].filename | string | yes | string value. |
| input.attachments[].content | any | yes | Attachment bytes (Buffer in library calls). |
| input.attachments[].mimeType | string | no | string value. |
| input.attachments[].inline | boolean | no | boolean value. |
| input.attachments[].contentId | string | no | string value. |
| input.inReplyTo | string | no | string value. |
| input.references | array | no | Array of string. |
| input.headers | object | no | object value. |

Examples:

```sh
ghostpaw-email call mail_compose '{"action":"send","input":{"to":[{"address":"reader@example.com"}],"subject":"Hello"}}'
ghostpaw-email call mail_compose '{"action":"reply","input":{},"folder":"INBOX","uid":1}'
ghostpaw-email call mail_compose '{"action":"forward","input":{"to":[{"address":"reader@example.com"}]},"folder":"INBOX","uid":1}'
```

## mail_organize

Organize messages: mark read/unread/starred/answered, copy, move, archive, trash, junk, label, or manage folders.

Use when: Change message flags, labels, destinations or folder organization.

Not for: Use mail_read or mail_search when only inspection is requested.

Writes: writes_state.

Nested requirements apply within the parent for the selected action.

| Parameter | Type | Required | Values / description |
| --- | --- | --- | --- |
| action | string | yes | unsubscribe_folder. string value. |
| folder | string | no | Source folder (required for message actions). |
| uids | array | no | Message UIDs to act on. |
| destination | string | no | Destination folder (required for copy/move). |
| labels | array | no | Labels to set/add/remove. |
| path | string | no | Folder path (required for folder actions). |
| oldPath | string | no | Old folder path (required for rename_folder). |
| newPath | string | no | New folder path (required for rename_folder). |

Examples:

```sh
ghostpaw-email call mail_organize '{"action":"mark_read","folder":"INBOX","uids":[1]}'
ghostpaw-email call mail_organize '{"action":"mark_unread","folder":"INBOX","uids":[1]}'
ghostpaw-email call mail_organize '{"action":"star","folder":"INBOX","uids":[1]}'
```

## mail_sync

Manage the IMAP connection lifecycle and sync local state: connect, disconnect, reconnect, sync folders, or refresh the folder list.

Use when: Connect, disconnect, reconnect, refresh folders or synchronize the cache.

Not for: Use mail_read for cached content or the network watch stream for continuous monitoring.

Writes: writes_state.

Nested requirements apply within the parent for the selected action.

| Parameter | Type | Required | Values / description |
| --- | --- | --- | --- |
| action | string | yes | connect, disconnect, reconnect, sync, refresh_folders, watch. string value. |
| folders | array | no | Folders to sync or watch (optional — defaults to all subscribed folders). |
| bodies | string | no | none, missing, all. Body fetch strategy for sync (default: missing). |

Examples:

```sh
ghostpaw-email call mail_sync '{"action":"connect"}'
ghostpaw-email call mail_sync '{"action":"disconnect"}'
ghostpaw-email call mail_sync '{"action":"reconnect"}'
```

## Workflow guides

- `ghostpaw-email skill triage-inbox`: Process a full inbox from scratch: sync to get latest state, read message queue, selectively fetch bodies for decisions, then bulk-organize by priority.
- `ghostpaw-email skill read-and-reply`: Read a message with full thread context, then compose and send a properly-threaded reply with quoted attribution.
- `ghostpaw-email skill connect-and-sync`: Establish or restore an IMAP connection, refresh the folder list, and pull new messages — handling first-run vs incremental scenarios.
- `ghostpaw-email skill search-and-act`: Find messages matching criteria (local FTS first, remote IMAP SEARCH as fallback), verify targets, then act — organize, reply, or present.
- `ghostpaw-email skill compose-and-send`: Full draft lifecycle — save, review, update, then send — plus direct send, reply, and forward with proper threading and forwarded-header blocks.
- `ghostpaw-email skill organize-bulk`: Bulk organize messages across folders — flagging, moving, archiving, labelling — and manage the folder hierarchy as part of the flow.
- `ghostpaw-email skill attachment-workflow`: Discover, inspect, and fetch email attachments on demand; embed attachments in outbound messages; and export or import full .eml files.
- `ghostpaw-email skill recover-from-disruption`: Detect and recover from connection loss or IMAP/SMTP failures — reconnect with back-off, re-sync to reconcile state, and handle auth vs transient errors distinctly.
- `ghostpaw-email skill cli`: Complete existing email CLI guide.

## Principles

- Inspect before changing messages.
- Confirm recipients and content before sending.

## Without the binary

For npm-based environments (Node 24+): `npx -y @ghostpaw/email ...`.

Harnesses that embed it in code can import `@ghostpaw/email` as a library.
