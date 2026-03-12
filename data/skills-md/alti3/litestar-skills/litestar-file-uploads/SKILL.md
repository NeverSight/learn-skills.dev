---
name: litestar-file-uploads
description: Handle Litestar multipart file uploads securely with `UploadFile`, typed multipart models, multi-file inputs, request body limits, and storage-safe processing patterns. Use when accepting single or multiple uploaded files in request bodies, especially multipart form-data endpoints. Do not use for generic request parsing, static asset serving, or download response behavior.
---

# File Uploads

## Execution Workflow

1. Decide whether the endpoint truly needs multipart file transport.
2. Choose the input shape: single `UploadFile`, typed multipart model, `dict[str, UploadFile]`, or `list[UploadFile]`.
3. Declare multipart explicitly with `Body(media_type=RequestEncodingType.MULTI_PART)`.
4. Validate filename, content type, size expectations, and field layout before expensive processing.
5. Stream or hand off large files to storage/services without unbounded memory use.
6. Keep upload parsing and validation at the transport edge; move persistence and scanning into services.

## Core Rules

- Treat every uploaded file as untrusted input.
- Type uploads explicitly with `UploadFile` or multipart container models.
- Prefer typed multipart models when field names and structure are known.
- Use `dict[str, UploadFile]` or `list[UploadFile]` only when the field layout is dynamic or intentionally loose.
- Keep request size limits explicit with `request_max_body_size` when defaults are not sufficient.
- Avoid reading whole files into memory unless the endpoint contract is small and bounded.
- Keep upload endpoints aligned with `litestar-requests` for broader request-parsing concerns.

## Decision Guide

- Use a single `UploadFile` when one file is the entire body contract.
- Use a typed dataclass or model when multipart mixes files and ordinary fields.
- Use `dict[str, UploadFile]` when filenames/field names are dynamic and validation is minimal.
- Use `list[UploadFile]` when the files are homogeneous and field names do not matter.
- Use async file reads in async handlers and direct `data.file.read()` in sync handlers.
- Lower `request_max_body_size` for sensitive upload endpoints unless a larger bound is justified.

## Reference Files

Read only the sections you need:

- For single-file uploads, typed multipart models, multi-file forms, and async vs sync upload handling, read [references/upload-patterns.md](references/upload-patterns.md).
- For request body limits, `UploadFile` internals, safe processing guidance, and test patterns, read [references/limits-and-testing.md](references/limits-and-testing.md).

## Recommended Defaults

- Prefer multipart models when the field layout is fixed.
- Keep upload endpoints narrow and purpose-built.
- Validate metadata before scanning, persisting, or transforming the file.
- Leave the global body-size limit in place unless a route has a documented reason to override it.
- Return only minimal safe metadata to clients after upload.

## Anti-Patterns

- Using multipart uploads when plain JSON or form data would do.
- Accepting unbounded file bodies without a front-door size limit.
- Reading large files fully into memory by default.
- Returning internal temp-file paths or unsafe metadata to clients.
- Mixing storage, scanning, and persistence logic directly into the route handler.
- Treating `dict[str, UploadFile]` as the default when the form shape is actually known.

## Validation Checklist

- Confirm multipart media type is declared explicitly.
- Confirm the chosen upload shape matches the real form contract.
- Confirm body-size limits are appropriate for the endpoint.
- Confirm async vs sync file access matches the handler style.
- Confirm large uploads do not exhaust memory unexpectedly.
- Confirm invalid or unexpected files fail with deterministic client errors.
- Confirm upload metadata returned to clients is minimal and safe.

## Cross-Skill Handoffs

- Use `litestar-requests` for non-file request parsing and mixed request contract design.
- Use `litestar-responses` for download and file-serving behavior after upload.
- Use `litestar-testing` for multipart and size-limit regression coverage.
- Use `litestar-security` when upload endpoints need auth, secret transport, or strict policy enforcement.

## Litestar References

- https://docs.litestar.dev/latest/usage/requests.html#file-uploads
- https://docs.litestar.dev/latest/usage/requests.html
