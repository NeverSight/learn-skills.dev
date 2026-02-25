---
name: analyze-bundle
description: Convert Next.js bundle analyzer data to NDJSON and explore it
allowed-tools: Bash(node *) Bash(head:*) Bash(tail:*) Bash(grep:*) Bash(jq:*) Read
---

# analyze-to-ndjson

Converts Next.js bundle analyzer binary `.data` files into grep/jq-friendly NDJSON.

## Generate the data

```bash
pnpm next experimental-analyze --output
```

This writes binary files to `.next/diagnostics/analyze/data/`.

## Run the converter

```bash
node tools/analyze-to-ndjson.mjs
```

Options:
- `--input <dir>` — source directory (default: `.next/diagnostics/analyze/data`)
- `--output <dir>` — output directory (default: `./analyze-ndjson`)

## Output files

| File | What's in it |
|---|---|
| `modules.ndjson` | Global module registry (`id`, `ident`, `path`) |
| `module_edges.ndjson` | Module dependency graph (`from`, `to`, `kind`: sync/async) |
| `sources.ndjson` | Per-route source tree with sizes and environment flags |
| `chunk_parts.ndjson` | Granular size data: one line per (source, output_file) pair |
| `output_files.ndjson` | Per-route output files with aggregated sizes |
| `routes.ndjson` | Route-level summaries |

## Browsing the output

### Route overview

```bash
# All routes sorted by compressed size
jq -s 'sort_by(-.total_compressed_size)' analyze-ndjson/routes.ndjson
```

### Find large sources

```bash
# Top 10 largest sources (deduplicated by full_path)
jq -s '
  group_by(.full_path)
  | map(max_by(.compressed_size))
  | sort_by(-.compressed_size)
  | .[0:10]
  | .[] | {full_path, compressed_size, size, route}
' analyze-ndjson/sources.ndjson
```

### Client-side JS

```bash
# Largest client JS sources
grep '"client":true' analyze-ndjson/sources.ndjson \
  | grep '"js":true' \
  | jq -s 'sort_by(-.compressed_size) | .[0:10] | .[] | {full_path, compressed_size}'
```

### Module dependencies

```bash
# What does module 42 depend on?
grep '"from":42,' analyze-ndjson/module_edges.ndjson | jq .to

# Who depends on module 42?
grep '"to":42,' analyze-ndjson/module_edges.ndjson | jq .from

# Look up a module by path fragment
grep 'react-dom' analyze-ndjson/modules.ndjson | jq '{id, path}'
```

### Output files for a route

```bash
# Largest output files for the "/" route
grep '"route":"/"' analyze-ndjson/output_files.ndjson \
  | jq -s 'sort_by(-.total_compressed_size) | .[0:10] | .[] | {filename, total_compressed_size, num_parts}'
```

### Directory tree for a route

```bash
# Top-level directories for "/"
grep '"route":"/"' analyze-ndjson/sources.ndjson \
  | jq 'select(.parent_id == null)'
```

### Feeding to an LLM

The NDJSON files are self-contained — each line has all the context needed to understand it. You can pass a whole file or a filtered subset as context:

```bash
# Give an LLM the route summary + the top 20 client sources
cat analyze-ndjson/routes.ndjson > /tmp/context.ndjson
grep '"client":true' analyze-ndjson/sources.ndjson \
  | jq -s 'sort_by(-.compressed_size) | .[0:20] | .[]' -c \
  >> /tmp/context.ndjson
```
