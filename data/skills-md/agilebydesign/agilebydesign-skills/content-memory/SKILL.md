---
name: content-memory
description: >-
  Converts documents (PDF, PPTX, DOCX, etc.) to markdown and chunks them for
  agent memory. Use when the user wants to "add to memory", "convert and chunk",
  "ingest for agent", or "refresh memory".
---

# Content Memory Pipeline

Convert source documents to markdown (in place) and chunk them for agent memory. Content lives in `memory/` or `workspace/`. Chunks go directly into `memory/<domain>/<topic>/`.

## Architecture

- **memory/** (project root): Content and chunks. No `converted/` or `chunked/` subfolders—chunks go directly in topic folders. Markdown in `<folder>/markdown/`.
- **workspace/** (optional): Source content for sync_and_chunk; copied to memory.
- **Convert to markdown/**: PDF/DOCX → .md written in `<folder>/markdown/` for each folder.
- **Chunk**: Reads from `source/<domain>/` or `memory/<domain>/`, writes to `memory/<domain>/<topic>/`.

## When to Activate

- "Add content to memory", "refresh memory", "ingest for agent"
- "Sync workspace to memory", "convert and chunk"

## Step 1: Convert to Markdown

Convert non-.md files to markdown in a `markdown/` subfolder per folder:

```bash
python scripts/convert_to_markdown.py --source <path> [--memory <domain>]
python scripts/convert_to_markdown.py --from source/CBE/domain_journeys_approach
```

- Writes `.md` in `<folder>/markdown/` (e.g. `CB Domain/foo.pdf` → `CB Domain/markdown/foo.md`)
- `.md` files are skipped

## Step 2: Chunk to Memory

Chunk markdown and write directly into memory topic folders:

```bash
python scripts/chunk_markdown.py --memory <domain> [--incremental]
```

- Reads from: `source/<domain>/**/*.md` or `memory/<domain>/**/*.md`.
- Writes to: `memory/<domain>/<topic>/` (no `chunked/` subfolder)
- `--incremental`: Only chunk new or modified files

## Step 3: Sync Workspace (Convert + Copy + Chunk)

One command for workspace content:

```bash
python scripts/sync_and_chunk.py --workspace <topic> --memory <domain> [--incremental]
```

1. Converts non-.md to `<folder>/markdown/` (in workspace)
2. Copies `workspace/<topic>` → `memory/<domain>/<topic>`
3. Chunks to `memory/<domain>/<topic>/`

## Chunking Strategy

- **Slide decks** (`<!-- Slide number: N -->`): One chunk per slide
- **Other docs** (>200 lines): Split at `#` or `##` boundaries
- **Small files** (<200 lines): Single chunk

Each chunk includes: `<!-- Source: path | file://url -->`

## Key Behaviors

1. **Content in memory** – Put content in `memory/<domain>/<topic>/` or sync from workspace.
2. **Convert to markdown/** – Markdown written in `<folder>/markdown/` for each folder.
3. **Chunks in memory** – No `chunked/` subfolder; chunks go directly in `memory/<domain>/<topic>/`.
4. **Incremental** – Use `--incremental` to skip unchanged files.

## Project-Specific Transformers

| Location | Scope |
|----------|-------|
| `memory/<name>/transformers/` | Memory-specific |
| `.content-memory/transformers/` | Workspace-level |

Each `.py` exports `EXTENSIONS` and `convert(path: Path) -> str`.

## Scripts

| Script | Purpose |
|--------|---------|
| `convert_to_markdown.py` | Convert to markdown/ |
| `chunk_markdown.py` | Chunk to memory |
| `sync_and_chunk.py` | Convert + copy + chunk (workspace) |

**Run from workspace root.** Set `CONTENT_MEMORY_ROOT` if needed.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No markdown | Run convert; then chunk. Or sync workspace to memory first. |
| Missing markitdown | `pip install "markitdown[all]"` |
