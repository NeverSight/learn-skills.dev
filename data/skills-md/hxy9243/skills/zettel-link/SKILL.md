---
name: zettel-link
description: This skill maintains the Note Embeddings for Zettelkasten, to search notes, retrieve notes, and discover connections between notes.
---

# Zettel Link Skill

This skill provides a suite of idempotent Python scripts to embed, search, and link notes in an Obsidian vault using semantic similarity. All scripts live in `scripts/` and support multiple embedding providers.

The skill should be triggered when the user wants to search notes, retrieve notes, or discover connections between notes.

If the search directory is indexed with embeddings, the skill should prompt the user if they want to create new embeddings.

## Dependencies

- uv 0.10.0+
- Python 3.10+
- One of the following embedding providers:
  - [Ollama](https://ollama.com) with `mxbai-embed-large` (local, default)
  - [OpenAI API](https://platform.openai.com/) with `text-embedding-3-small`
  - [Google Gemini API](https://ai.google.dev/) with `text-embedding-004`

## Overview of Commands

- `uv run scripts/config.py`: Configure the embedding model and other settings.
- `uv run scripts/embed.py`: Embed notes and cache to `.embeddings/embeddings.json`
- `uv run scripts/search.py`: Semantic search over embedded notes
- `uv run scripts/link.py`: Discover semantic connections, output to `.embeddings/links.json`

## Workflow

### Step 0 — Setup and Config

If the `config/config.json` file does not exist, create it:

```bash
uv run scripts/config.py
```

This creates `config/config.json` with defaults:

```json
{
    "model": "mxbai-embed-large",
    "provider": {
        "name": "ollama",
        "url": "http://localhost:11434"
    },
    "max_input_length": 8192,
    "cache_dir": ".embeddings",
    "default_threshold": 0.65,
    "top_k": 5,
    "skip_dirs": [".obsidian", ".trash", ".embeddings", "Spaces", "templates"],
    "skip_files": ["CLAUDE.md", "Vault.md", "Dashboard.md", "templates.md"]
}
```

To use a remote provider:

```bash
# OpenAI
uv run scripts/config.py --provider openai

# Gemini
uv run scripts/config.py --provider gemini

# Custom model
uv run scripts/config.py --provider openai --model text-embedding-3-large
```

To adjust tuning parameters:

```bash
uv run scripts/config.py --top-k 10 --threshold 0.7 --max-input-length 4096
```

### Step 1 — Create Embeddings

```bash
uv run scripts/embed.py --input <directory>
```

This creates `<directory>/.embeddings/embeddings.json` with the embedding cache.

- **Incremental updates**: Only re-embeds files that have been modified since the last run (based on file modification time).
- **Text truncation**: Automatically truncates text to `max_input_length` before embedding.
- **Stale pruning**: Removes entries for files that no longer exist.
- **Force re-embed**: Use `--force` to re-embed everything.

### Step 2 — Semantic Search

```bash
uv run scripts/search.py --input <directory> --query "<query>"
```

This embeds the query using the configured provider and compares it with all cached embeddings, returning the `top_k` most similar notes.

Results are saved to `<directory>/.embeddings/search_results.json`.

### Step 3 — Semantic Connection Discovery

```bash
uv run scripts/link.py --input <directory>
```

This computes cosine similarity for all note pairs and outputs connections above the `default_threshold` to `<directory>/.embeddings/links.json`.

The output includes:
- A flat list of all link pairs with scores
- A per-note grouping for easy lookup

**Tuning**: Adjust `--threshold` to widen or narrow the connection discovery.

## Cache

- **Format**: JSON with metadata envelope (`metadata` + `data`)
- **Location**: `<directory>/.embeddings/embeddings.json`
- **Metadata**: Tracks generation timestamp, model, provider, embedding size
- **Invalidation**: Based on file modification time (`mtime`)
- **Force rebuild**: Delete the cache file or use `--force` flag

## Agent Instructions

When using this skill:

1. Always run `config.py` first if `config/config.json` does not exist.
2. Run `embed.py` before `search.py` or `link.py` — the cache must exist.
3. For remote providers (openai, gemini), ensure the API key environment variable is set (or provide a local `.env` file in the skill directory).
4. All scripts are idempotent and safe to re-run.
