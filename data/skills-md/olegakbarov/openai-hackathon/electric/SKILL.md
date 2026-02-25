---
name: electric
description: Build local-first apps with ElectricSQL (HTTP Postgres sync) and TanStack DB. Use when wiring Electric shapes and proxy routes, configuring electricCollectionOptions, implementing optimistic mutations with txid handshake, or troubleshooting live queries, security, and deployment.
---

# ElectricSQL + TanStack DB

## Overview
Use this skill to implement the Electric + TanStack DB stack for local-first apps. Focus on secure proxying, shape configuration, optimistic write flow, and live queries. The full guide is in `references/electric-docs.md`.

## Golden path
1. Create a project and run migrations.
2. Add an Electric proxy route on the server and inject SOURCE_ID/SECRET.
3. Create Electric collections on the client with `electricCollectionOptions`.
4. Implement write handlers that call the API and return a Postgres txid.
5. Use live queries for reads and joins.
6. Validate performance, auth, and deployment setup.

## Security rules (always)
- Never expose SOURCE_SECRET to the browser.
- Do not call Electric directly from production clients.
- Define shapes server-side; do not allow client-defined tables or WHERE clauses.

## Write path contract
- Optimistic mutation in TanStack DB.
- API writes to Postgres and returns txid.
- Client awaits txid on the Electric stream before dropping optimistic state.

## Shape rules
- Shapes are single-table with optional where/columns.
- Include primary key when using columns.
- Shapes are immutable per subscription; create a new collection for dynamic shapes.

## Troubleshooting
- UI flicker usually means missing txid handshake.
- Slow shapes in dev can be HTTP/1.1 limits; use HTTP/2 proxy or Electric Cloud.
- Ensure proxy forwards Electric query params and preserves headers.

## References
- `references/electric-docs.md` contains the full documentation snapshot.
