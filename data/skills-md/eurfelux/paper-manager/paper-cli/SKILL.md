---
name: paper-cli
description: >
  Guide for using the `paper` CLI tool — a local academic paper management system with AI-powered
  vector search. Use this skill whenever the user wants to manage academic papers, create knowledge
  bases, add files (PDF, TXT, MD, TEX, etc.) to a knowledge base, search papers semantically, configure embedding models,
  or manage literature metadata and notes. Also trigger when the user mentions "paper" CLI,
  knowledge bases for research, literature management, or wants to query their paper collection.
  Even if the user just says something like "add this PDF", "add this text file", or "search my papers" in a project
  that uses paper-manager, this skill should activate.
---

# paper CLI — Academic Paper Management

`paper` is a local-first CLI tool for managing academic papers with AI-powered semantic search. It stores data in SQLite databases and uses FAISS vector stores for similarity search.

## Core Concepts

### Scope: User vs Project

Every resource (config, knowledge base, literature) lives in one of two scopes:

- **Project scope** (default): stored in `./.paper-manager/` — tied to the current directory, good for project-specific paper collections
- **User scope** (`--user` flag): stored in `~/.paper-manager/` — shared across all projects, good for a personal paper library

Project-level config overrides user-level config. When looking up a knowledge base or literature, the tool checks project scope first, then falls back to user scope.

### Data Hierarchy

```
Config (embedding models)
  └── Knowledge Base (has a name, description, and embedding model)
        └── Literature (a paper with metadata, source file, and vector embeddings)
              └── Notes (key-value pairs for personal annotations)
```

You must configure an embedding model before creating a knowledge base, and you must create a knowledge base before adding literature.

## Troubleshooting: Installation & Setup

The user should already have `paper` installed and configured. Only use this section if something is missing.

### Installation (if `paper` command is not found)

```bash
npm install -g paper-manager    # or: pnpm add -g paper-manager
```

Requires **Node.js >= 24**. Verify with `paper --version`.

### Config setup (if commands fail due to missing config)

```bash
# If data directory is missing or incomplete, initialize it first
paper config init [--user]

# Set up an embedding model (OpenAI-compatible provider)
paper config set embeddingModels '{"my-model": {"provider": "openai", "model": "text-embedding-3-small", "apiKey": "sk-...", "dimensions": 1536}}' --user

# Set a default model so you don't have to specify it every time
paper config set defaultEmbeddingModelId my-model --user
```

The embedding model config fields:

- `provider`: currently only `"openai"` (works with any OpenAI-compatible API)
- `model`: the model name (e.g., `"text-embedding-3-small"`)
- `baseUrl`: optional custom API endpoint
- `apiKey`: API key for the provider
- `dimensions`: embedding vector dimensions (e.g., 1536)
- `batchSize`: optional max number of texts per embedding API request (set this if your provider limits batch size)

## Command Reference

### paper config — Configuration Management

```bash
paper config init [--user]              # Initialize data directory (config, db, subdirs)
paper config list [--user]              # Show all config (merged or user-only)
paper config get <key> [--user]         # Get a specific config value
paper config set <key> <value> [--user] # Set a config value (value is parsed as JSON, falls back to string)
paper config remove <key> [--user]      # Remove a config key
```

Config keys:

- `embeddingModels` — a JSON object of `{ [modelId]: { provider, model, baseUrl?, apiKey, dimensions, batchSize? } }`
- `defaultEmbeddingModelId` — which model ID to use when none is specified

### paper kb — Knowledge Base Management

```bash
# Create a knowledge base (requires an embedding model in config)
paper kb create <name> -d <description> [-e <embedding-model-id>] [--user]

# List knowledge bases
paper kb list [--user | --all]

# Remove a knowledge base and ALL its data (literatures, PDFs, vectors)
paper kb remove <id>

# Semantic search across a knowledge base
paper kb query <id> <query-text> [-k <top-k>]   # default top-k is 5
```

The `<id>` for knowledge bases is a UUID assigned at creation time. Use `paper kb list` to find it.

### paper lit — Literature Management

```bash
# Add a paper (extracts content, splits text, creates embeddings)
# Supports PDF, TXT, MD, TEX, and other text-based formats
paper lit add <kb-id> <file-path> [-t <title>]
# Title defaults to the filename (without extension) if not specified

# List papers in a knowledge base
paper lit list <kb-id>

# Show full details of a paper
paper lit show <kb-id> <lit-id>

# Update paper metadata
paper lit update <kb-id> <lit-id> [options]
#   -t, --title <title>
#   --title-translation <translation>
#   -a, --author <author>
#   --abstract <abstract>
#   --summary <summary>
#   --url <url>
#   --keywords <comma-separated-keywords>

# Remove a paper (deletes DB record, source file; vectors remain in store)
paper lit remove <kb-id> <lit-id>
```

### paper lit note — Literature Notes

Notes are key-value string pairs attached to a literature entry — useful for personal annotations.

```bash
paper lit note list <lit-id>                    # List all notes
paper lit note set <lit-id> <key> <value>       # Set a note
paper lit note remove <lit-id> <key>            # Remove a note
```

Note: the note commands take `<lit-id>` directly (not `<kb-id> <lit-id>`).

## Common Workflows

### Start a new research project

1. `paper kb create "my-project" -d "Papers about X"` — create a project-scoped KB
2. `paper lit add <kb-id> ./paper.pdf -t "Paper Title"` — add papers (also works with .txt, .md, .tex)
3. `paper kb query <kb-id> "your research question"` — search

### Manage paper metadata

1. `paper lit list <kb-id>` — find the literature ID
2. `paper lit update <kb-id> <lit-id> -a "Author Name" --keywords "ML,NLP"`
3. `paper lit note set <lit-id> takeaway "Key insight from this paper"`

## Important Notes

- All IDs (knowledge base, literature) are UUIDs — always use `list` commands to look them up
- Adding a paper (`lit add`) extracts the file content (PDF or text), splits it into chunks, and creates vector embeddings — this calls the embedding API and may take some time
- Text files have a 10 MB size limit
- The `kb remove` command is destructive: it deletes the knowledge base, all its literatures, source files, and vector stores
- The `--user` flag on `config`/`kb create` controls scope; omitting it uses project scope
- Config values passed to `config set` are parsed as JSON first; if JSON parsing fails, the raw string is stored
