---
name: pinecone-assistant
description: Create, manage, and chat with Pinecone Assistants for document Q&A with citations. Handles all assistant operations - create, upload, sync, chat, context retrieval, and list. Recognizes natural language like "create an assistant from my docs", "ask my assistant about X", or "upload my docs to Pinecone".
---

# Pinecone Assistant

Pinecone Assistant is a fully managed RAG service. Upload documents, ask questions, get cited answers. No embedding pipelines or infrastructure required.

> All scripts are in `scripts/` relative to this skill directory.
> Run with: `uv run scripts/script_name.py [arguments]`

## Operations

| What to do | Script | Key args |
|---|---|---|
| Create an assistant | `scripts/create.py` | `--name` `--instructions` `--region` |
| Upload files | `scripts/upload.py` | `--assistant` `--source` `--patterns` |
| Sync files (incremental) | `scripts/sync.py` | `--assistant` `--source` `--delete-missing` `--dry-run` |
| Chat / ask a question | `scripts/chat.py` | `--assistant` `--message` |
| Get context snippets | `scripts/context.py` | `--assistant` `--query` `--top-k` |
| List assistants | `scripts/list.py` | `--files` `--json` |

For full workflow details on any operation, read the relevant file in `references/`.

---

## Natural Language Recognition

Proactively handle these patterns without requiring explicit commands:

**Create:** "create an assistant", "make an assistant called X", "set up an assistant for my docs"
→ See [references/create.md](references/create.md)

**Upload:** "upload my docs", "add files to my assistant", "index my documentation"
→ See [references/upload.md](references/upload.md)

**Sync:** "sync my docs", "update my assistant", "keep assistant in sync", "refresh from ./docs"
→ See [references/sync.md](references/sync.md)

**Chat:** "ask my assistant about X", "what does my assistant know about X", "chat with X"
→ See [references/chat.md](references/chat.md)

**Context:** "search my assistant for X", "find context about X"
→ See [references/context.md](references/context.md)

**List:** "show my assistants", "what assistants do I have"
→ Run `uv run scripts/list.py`

---

## Conversation Memory

Track the last assistant used within the conversation:
- When a user creates or first uses an assistant, remember its name
- If user says "my assistant", "it", or "the assistant" → use the last one
- Briefly confirm which assistant you're using: "Asking docs-bot..."
- If ambiguous and multiple exist → ask the user to clarify

---

## Multi-Step Requests

Handle chained requests naturally. Example:

> "Create an assistant called docs-bot, upload my ./docs folder, and ask what the main features are"

1. `uv run scripts/create.py --name docs-bot`
2. `uv run scripts/upload.py --assistant docs-bot --source ./docs`
3. `uv run scripts/chat.py --assistant docs-bot --message "what are the main features?"`

---

## Prerequisites

- `PINECONE_API_KEY` must be available — terminal: `export PINECONE_API_KEY="your-key"`, or add to a `.env` file and run scripts with `uv run --env-file .env scripts/...`
- `uv` must be installed — [install uv](https://docs.astral.sh/uv/getting-started/installation/)
- Get a free API key at: https://app.pinecone.io/?sessionType=signup
