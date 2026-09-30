---
name: modrinth-api
description: Query Modrinth metadata and verify pinned downloads.
license: MIT
metadata:
  author: "SirEdvin"
  version: "1.1.0"
---

# Modrinth API v2

Use `https://api.modrinth.com/v2` for public project discovery, compatible version
selection, source URLs and download metadata. This is not Modrinth Maven or a
publishing workflow. Public project/search/version reads need no token; private
or user-specific **read** endpoints can require authentication too.

## Safe workflow

1. Send an identifying `User-Agent` on every API request. Use timeouts, check HTTP
   status, and respect `X-Ratelimit-Limit`, `Remaining`, and `Reset` headers; on
   429 wait for the documented reset rather than repeatedly retrying. The documented
   default is 300 requests/minute per IP, not a guaranteed allowance.
2. Search with JSON-encoded, URL-encoded facets. Inner arrays OR terms; outer
   arrays AND groups. Search pagination uses `limit` and `offset` (maximum 100
   hits per request); deduplicate by project ID and verify requested totals.
3. Fetch full projects to read nullable `source_url`, license and project
   compatibility metadata; read dependencies from individual versions. Search hits do not contain `source_url`.
4. List a project's versions using `loaders` and `game_versions` JSON arrays.
   **This v2 endpoint does not document `limit`/`offset` pagination.** Filter the
   returned array locally; never assume `limit=1` selected a stable release.
5. Choose release/beta/alpha policy explicitly, check the version's own loader
   and game-version arrays, then persist the exact version ID. Sort by publication
   timestamp if recency is intended; `version_number` is not guaranteed SemVer.
6. Select the primary file (or first file if none is marked primary per API
   contract), then validate purpose, filename, size and SHA-512. A version can
   include non-runtime files; do not blindly select every JAR or construct a CDN URL.
7. Resolve required dependency versions, optional/incompatible/embedded entries,
   physical sides and licensing before installation. API metadata is not a
   client/server compatibility test or a guarantee an artifact is safe to execute.

## Auth and action boundaries

Public reads should omit `Authorization`. For authorized private reads or writes,
use the endpoint's required PAT/OAuth scopes and account permissions. Keep tokens
in secret storage, never URLs/logs/commits, and never forward them to CDN/source
hosts. A GET is not automatically public; a read-only task must not create,
modify, follow, upload or publish anything. Seek explicit authorization for writes
and read back the exact target after a requested mutation.

## Progressive reference

[Endpoint contracts and safe query examples](references/api-v2-workflows.md)
contains executable read-only curl examples, file-verification rules, official
sources and endpoint-specific verification guidance. API v2 tag endpoints have distinct
schemas; do not treat all responses as objects with a `name` field or infer v3
fields from a moving docs page. Handle 401/403/404/410 and empty arrays explicitly.
