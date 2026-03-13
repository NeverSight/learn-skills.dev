---
name: pinecone-quickstart
description: Interactive Pinecone quickstart for new developers. Choose between two paths - Database (create an integrated index, upsert data, and query using Pinecone MCP + Python) or Assistant (create a Pinecone Assistant for document Q&A). Use when a user wants to get started with Pinecone for the first time or wants a guided tour of Pinecone's tools.
---

# Pinecone Quickstart

Welcome! This skill walks you through your first Pinecone experience using the tools available to you. In this quickstart,
you will learn how to do a simple form of semantic search over some example data.

## Prerequisites

Before starting either path, verify the API key works by calling `list-indexes` via the Pinecone MCP. If it succeeds, proceed. If it fails, ask the user to set their key:

- Terminal: `export PINECONE_API_KEY="your-key"`
- Or create a `.env` file in the project root: `PINECONE_API_KEY=your-key`

Then retry `list-indexes` to confirm.

## Step 0: Choose Your Path

Ask the user which path they want:

- **Database** – Build a vector search index. Best for developers who want to store and search embeddings. Uses the Pinecone MCP + a Python upsert script.
- **Assistant** – Build a document Q&A assistant. Best for users who want to upload files and ask questions with cited answers. No code required.

---

## Path A: Database Quickstart

For each step, explain to the user what will happen. An overview is here:

1. Check if MCP is set
2. Create an integrated index with MCP
3. Upsert sample data using the bundled script (9 sentences across productivity, health, and nature themes)
4. Run a semantic search query and explore further queries
5. Optionally try reranking
6. Offer the complete standalone script

### Step 1 – Verify MCP is Available

The prerequisite check already called `list-indexes`. If it succeeded, the MCP is working — proceed to Step 2.

If it failed because MCP tools were unavailable (not an auth error):
- Tell the user the MCP server needs to be configured
- Point them to: https://docs.pinecone.io/reference/tools/mcp

### Step 2 – Create an Integrated Index

Use the MCP `create-index-for-model` tool to create a serverless index with integrated embeddings:

```
name: quickstart-skills
cloud: aws
region: us-east-1
embed:
  model: llama-text-embed-v2
  fieldMap:
    text: chunk_text
```

**Explain to the user what's happening:**
- An *integrated index* uses a built-in Pinecone embedding model (`llama-text-embed-v2`)
- This means you send plain text and Pinecone handles the embedding automatically
- The `field_map` tells Pinecone which field in your records contains the text to embed

Wait for the index to become ready before proceeding. Waiting a few seconds is sufficient.

### Step 3 – Upsert Sample Data

Run the bundled upsert script to seed the index with sample records.

If `PINECONE_API_KEY` is set in the environment:
```bash
uv run scripts/upsert.py --index quickstart-skills
```

If using a `.env` file:
```bash
uv run --env-file .env scripts/upsert.py --index quickstart-skills
```

**Explain to the user what's happening:**
- The script uploads 9 sample records across three themes: **productivity** (getting work done), **health** (feeling unwell), and **nature** (outdoors/wildlife)
- The dataset is intentionally varied so semantic search can show its value — the queries below use completely different words than the records, but the right ones still surface
- Each record has an `_id`, a `chunk_text` field (the text that gets embedded), and a `category` field
- This is the same structure you'd use for your own data — just replace the records

### Step 4 – Query with the MCP

Use the MCP `search-records` tool to run the first semantic search:

```
index: quickstart-skills
namespace: example-namespace
query:
  topK: 3
  inputs:
    text: "getting things done efficiently"
```

Display the results in a clean table: ID, score, and `chunk_text`.

**Explain to the user what's happening:**
- Notice the query shares no keywords with the records — but it surfaces the productivity sentences
- That's semantic search: it finds meaning, not just matching words
- You sent plain text — Pinecone embedded the query using the same model as the index

**Offer to explore further:** Ask the user if they'd like to try another query to see the effect more clearly:
- Option A: `"feeling under the weather"` — should surface the health records
- Option B: `"wildlife spotting outside"` — should surface the nature records
- Option C: No thanks, move on

Run whichever query they choose and display the results the same way. If they want to try both, do both. After each result, point out which theme surfaced and why.

If they decline or are done exploring, proceed to Step 5 or offer to skip ahead to the complete script.

### Step 5 – Try Reranking (Optional)

Ask the user if they want to try reranking.

If yes, use `search-records` again with reranking enabled:

```
rerank:
  model: bge-reranker-v2-m3
  rankFields: [chunk_text]
  topN: 3
```

**Explain**: Reranking runs a second-pass model over the results to improve relevance ordering.

### Step 6 – Wrap Up

Congratulate the user on completing the quickstart. Ask if they'd like a standalone Python script that does everything in one go — create index, upsert, query, and rerank.

If yes, copy it to their working directory:

```bash
cp scripts/quickstart_complete.py ./pinecone_quickstart.py
```

Tell the user:
- The script is at `./pinecone_quickstart.py`
- Run it with: `uv run pinecone_quickstart.py`
- It uses `uv` inline dependencies — no separate install needed
- They can swap in their own `records` list to build something real

---

## Path B: Assistant Quickstart

Guide the user through the Pinecone Assistant workflow using the existing assistant skills:

### Step 1 – Check for Documents

Before anything else, ask the user if they have files to upload. Pinecone Assistant accepts `.pdf`, `.md`, `.txt`, and `.docx` files — a single file or a folder of files both work.

**If they have files:** ask for the path and proceed to Step 2.

**If they don't have files:** offer two options:
- **Generate sample docs** — create a few short markdown files in `./sample-docs/` so they can complete the quickstart right now. Ask what topics they'd like (or default to: a product FAQ, a short how-to guide, and a brief company overview). Write 3 files, each 150–250 words.
- **Come back later** — let them know they can return once they have documents and pick up from Step 2.

### Step 2 – Create an Assistant

Invoke `pinecone-assistant` or run (add `--env-file .env` if using a `.env` file):
```bash
uv run ../pinecone-assistant/scripts/create.py --name my-assistant
```

Explain: The assistant is a fully managed RAG service — upload documents, ask questions, get cited answers.

### Step 3 – Upload Documents

Invoke `pinecone-assistant` or run (add `--env-file .env` if using a `.env` file):
```bash
uv run ../pinecone-assistant/scripts/upload.py --assistant my-assistant --source ./your-docs
```

Explain: Pinecone handles chunking, embedding, and indexing automatically — no configuration needed.

### Step 4 – Chat with the Assistant

Invoke `pinecone-assistant` or run (add `--env-file .env` if using a `.env` file):
```bash
uv run ../pinecone-assistant/scripts/chat.py --assistant my-assistant --message "What are the main topics in these documents?"
```

Explain: Responses include citations with source file and page number.

### Next Steps for Assistant

- Invoke `pinecone-assistant` to keep the assistant up to date as documents change
- Use the assistant skill to retrieve raw context snippets for custom workflows
- Every assistant is also an MCP server — see https://docs.pinecone.io/guides/assistant/mcp-server

---

## Troubleshooting

**`PINECONE_API_KEY` not set**

Terminal environments:
```bash
export PINECONE_API_KEY="your-key"
```
IDEs that don't inherit shell variables: create a `.env` file in the project root:
```
PINECONE_API_KEY=your-key
```
Then use `uv run --env-file .env` when running scripts. Restart your IDE/agent session after setting.

**MCP tools not available**
- Verify the Pinecone MCP server is configured in your IDE's MCP settings
- Check that `PINECONE_API_KEY` is set before the MCP server starts

**Index already exists**
- The upsert script is safe to re-run — it will upsert over existing records
- Or delete and recreate: use `pc index delete -n quickstart-skills` via the CLI

**`uv` not installed**
See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Further Reading

- Quickstart docs: https://docs.pinecone.io/guides/get-started/quickstart
- Integrated indexes: https://docs.pinecone.io/guides/index-data/create-an-index
- Python SDK: https://docs.pinecone.io/guides/get-started/python-sdk
- MCP server: https://docs.pinecone.io/reference/tools/mcp
