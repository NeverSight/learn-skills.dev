---
name: pdf-brain-ingest
displayName: PDF Brain Ingest
description: "Ingest PDF/Markdown/TXT files into joelclaw's docs memory pipeline with Inngest durability, run monitoring, and OTEL verification. Use when adding docs, backfilling from manifest, reconciling coverage, or recovering stuck docs-ingest runs. Triggers on: 'ingest pdf', 'ingest markdown', 'docs add', 'pdf-brain ingest', 'backfill books', 'docs reconcile'."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, docs, pdf, markdown, ingest, inngest, typesense, memory]
---

# PDF Brain Ingest (Joelclaw)

This is the joelclaw-native replacement for `pdf-brain + swarm queue` operations.

Use `joelclaw docs` and Inngest events instead of ad hoc queue workers:
- `docs/ingest.requested` -> `docs-ingest`
- `docs/backlog.requested` -> batch queueing from manifest
- `docs/backlog.drive.requested` -> scheduled backlog driver with queue depth gates
- `docs/ingest.janitor.requested` -> stuck-run detection and recovery

## Core Workflow

### 1) Preflight

```bash
joelclaw status
joelclaw inngest status
joelclaw docs status
```

If registration is stale:

```bash
joelclaw inngest sync-worker --restart
```

### 2) Single File Ingest

```bash
joelclaw docs add "/absolute/path/to/file.pdf"
joelclaw docs add "/absolute/path/to/file.md"
```

Optional metadata:

```bash
joelclaw docs add "/absolute/path/to/file.pdf" \
  --title "Readable Title" \
  --tags "manifest,catalog-fill" \
  --category programming
```

Supported types: `pdf`, `md`, `txt`.

### 3) Bulk Backfill From Manifest

Queue a controlled batch:

```bash
joelclaw send docs/backlog.requested -d '{
  "maxEntries": 24,
  "booksOnly": true,
  "onlyMissing": true,
  "includePodcasts": false,
  "idempotencyPrefix": "manual"
}'
```

Let the driver decide based on queue depth:

```bash
joelclaw send docs/backlog.drive.requested -d '{
  "reason": "manual backfill kick",
  "maxEntries": 24,
  "force": false
}'
```

### 4) Monitor + Verify

```bash
joelclaw runs --count 20 --hours 1
joelclaw run <run-id>
joelclaw docs list --limit 20
joelclaw docs show <doc-id>
joelclaw docs search "your query"
joelclaw docs context <chunk-id> --mode snippet-window
```

### 5) Coverage Reconcile

```bash
joelclaw docs reconcile --sample 20
```

Use `content_equivalent` coverage to detect false-missing churn caused by path/category aliasing.

### 6) OTEL Verification

```bash
joelclaw otel search "docs.file.validated" --hours 1
joelclaw otel search "docs.taxonomy.classified" --hours 1
joelclaw otel search "docs.chunks.indexed" --hours 1
joelclaw otel search "docs.path.aliases.updated" --hours 24
```

### 7) Recovery / Maintenance

```bash
joelclaw send docs/ingest.janitor.requested -d '{"reason":"manual janitor sweep"}'
joelclaw docs enrich <doc-id>
joelclaw docs reindex --doc <doc-id>
joelclaw docs reindex
```

## Legacy Mapping (Old -> Joelclaw)

- `pdf-brain add <file> --enrich` -> `joelclaw docs add <absolute-path>`
- `pdf-brain ingest <dir> --enrich` -> `joelclaw send docs/backlog.requested -d '{...}'`
- `swarm queue submit pdf-ingest '{"path":"..."}'` -> `joelclaw docs add <absolute-path>`
- `pdf-brain-worker (nice -n10, concurrency 1)` -> built into `docs-ingest` + backlog driver + janitor

## Acquisition Handoff (aa-book -> Inngest, end to end)

Use the event workflow so acquisition, inference, download, and docs queueing stay durable:

```bash
joelclaw send pipeline/book.download -d '{
  "query": "designing data-intensive applications",
  "format": "pdf",
  "reason": "memory backfill"
}'
```

Behavior:
- Runs `aa-book search`
- Uses `pi` inference (Sonnet 4.6 model alias from system-bus model registry) to select MD5
- Runs `aa-book download <md5> <outputDir>`
- Emits `docs/ingest.requested`
- Emits `pipeline/book.downloaded`

Optional direct MD5 mode:

```bash
joelclaw send pipeline/book.download -d '{
  "md5": "0123456789abcdef0123456789abcdef",
  "outputDir": "/Users/joel/clawd/data/pdf-brain/incoming"
}'
```

For full operator details and troubleshooting traces, see:
- `references/operator-guide.md`
