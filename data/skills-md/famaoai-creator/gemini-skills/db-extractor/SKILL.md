---
name: db-extractor
description: Extract schema and sample data from databases for analysis.
status: implemented
arguments:
  - name: db
    short: d
    type: string
    required: true
  - name: query
    short: q
    type: string
  - name: out
    short: o
    type: string
category: Utilities
last_updated: '2026-02-13'
tags:
  - analytics
  - data-engineering
  - gemini-skill
---

# Db Extractor

Extract schema and sample data from databases for analysis.

## Usage

node db-extractor/scripts/extract.cjs [options]

## Troubleshooting

| Error                          | Cause                              | Fix                                               |
| ------------------------------ | ---------------------------------- | ------------------------------------------------- |
| `Cannot find module 'sqlite3'` | Native module not built            | Run `npm rebuild sqlite3`                         |
| `SQLITE_CANTOPEN`              | Database file not found or locked  | Check file path and permissions                   |
| `SQLITE_BUSY`                  | Database locked by another process | Close other connections, retry                    |
| `SQLITE_CORRUPT`               | Database file corrupted            | Restore from backup, run `PRAGMA integrity_check` |
| `Error: ...node-pre-gyp...`    | Binary incompatibility             | Run `npm rebuild sqlite3 --build-from-source`     |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
