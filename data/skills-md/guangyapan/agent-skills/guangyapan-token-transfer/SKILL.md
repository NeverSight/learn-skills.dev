---
name: guangyapan-token-transfer
description: >
  Integrate and troubleshoot Guangyapan TOKEN uploads for individual
  developers. Use when transferring files from the developer's own Guangyapan
  drive to a receiver-authorized directory with an UploadToken, including
  developer credentials, source-file selection, pre-upload review, upload
  submission, task polling, and transfer results.
---

# Integrate Guangyapan TOKEN transfers

Use the developer API v1.1 contract dated 2026-08-31 as the source of truth. Preserve its host, HTTP method, field names, state values, and actor boundaries.

## Route the task

- For developer and receiver roles, credential setup, request headers, signature generation, and secret handling, read [references/authentication.md](references/authentication.md).
- For source-file browsing or rename, pre-upload review, transfer submission, status polling, and result-list contracts, read [references/transfer-api.md](references/transfer-api.md).
- For errors, duplicate submission, timing, retry decisions, task ownership, and production behavior, read [references/operations.md](references/operations.md).
- Read multiple references only when the task spans those concerns.

## API scope

This skill covers Guangyapan developer TOKEN uploads through `https://dapi.guangyapan.com`:

- Use `/userres/v1` to browse and rename files in the developer's own drive.
- Use `/developer/v1` for pre-upload review, TOKEN transfer, task polling, and result queries.
- Authenticate requests with developer credentials, a unique `nonce`, and the documented signature. Supply the receiver-issued `token_id` only to transfer-related operations.

## Workflow

1. Identify the developer, receiver, target TOKEN directory, and source files. Inspect existing client abstractions before adding another one.
2. Keep signing on a trusted boundary. Generate fresh request headers for every call and model the documented JSON envelope explicitly.
3. Browse the developer's own cloud drive through `/userres/v1` when source IDs are needed. Treat rename as a separate mutating operation requiring user intent.
4. Prefer the documented pre-upload review before a transfer to reduce skipped files. Treat it as a recommendation, not as a declared prerequisite for every upload.
5. When pre-upload review is used, retain its task ID and follow the documented timing recommendations. Retain the upload task ID, poll it to a terminal state, and fetch success or skipped results while they remain available.
6. Test signing with fixed local inputs, state transitions, pagination variants, duplicate-name behavior, ownership failures, and safe retry decisions. Use placeholders rather than real secrets or TOKEN values.

## Non-negotiable constraints

- Never expose `client_secret`, receiver TOKEN values, or reusable signatures in browser bundles, public environment variables, fixtures, logs, examples, or source control.
- Build the signature source in the documented order and hash the raw 16-byte MD5 digest with SHA-512. Hashing the MD5 hexadecimal text is incorrect.
- Generate a unique 16-32 character random `nonce` for each request and never reuse it. Use Unix seconds and keep the caller clock within 300 seconds of the server. Prefer a cryptographically secure random source as implementation guidance.
- Treat `token_id` as authorization to one receiver-selected directory and use it only with the documented transfer operations.
- Do not retry upload submissions blindly. Respect duplicate-submission windows and prefer querying an already-created task when its ID is available.
- Do not make live API calls or initiate a transfer unless the user has supplied the environment and credentials and authorized that external mutation. Generated code and tests should use placeholders by default.

## Contract gaps

- The pre-upload table calls `file_ids` a list of directory IDs, while its example and the upload contract include both file and directory IDs. Preserve a verified implementation or ask the platform to confirm rather than narrowing the field silently.
- A rename example includes `dt: 11`, but the common-header specification does not list `dt`. Do not make it mandatory without platform confirmation or verified existing behavior.
- The file-list example includes `needPlayRecord` and `needSubFolderStat`, but the request-parameter table does not define either field. Do not rely on them without platform confirmation or verified existing behavior.
- The document defines only the production host and does not specify a test host, exhaustive rate limits, retry headers, or complete HTTP error payloads. Do not invent them.
