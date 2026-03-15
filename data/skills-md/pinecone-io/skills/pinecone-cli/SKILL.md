---
name: pinecone-cli
description: Guide for using the Pinecone CLI (pc) to manage Pinecone resources from the terminal. The CLI supports ALL index types (standard, integrated, sparse) and all vector operations — unlike the MCP which only supports integrated indexes. Use for batch operations, vector management, backups, namespaces, CI/CD automation, and full control over Pinecone resources.
argument-hint: install | auth | index [op] | vector [op] | backup | namespace
---

# Pinecone CLI (`pc`)

Manage Pinecone from the terminal. The CLI is especially valuable for vector operations across **all index types** — something the MCP currently can't do.

## CLI vs MCP

| | CLI | MCP |
|---|---|---|
| Index types | All (standard, integrated, sparse) | Integrated only |
| Vector ops (upsert, query, fetch, update, delete) | ✅ | ❌ |
| Text search on integrated indexes | ✅ | ✅ |
| Backups, namespaces, org/project mgmt | ✅ | ❌ |
| CI/CD / scripting | ✅ | ❌ |

---

## Setup

### Install (macOS)
```bash
brew tap pinecone-io/tap
brew install pinecone-io/tap/pinecone
```

Other platforms (Linux, Windows) — download from [GitHub Releases](https://github.com/pinecone-io/cli/releases).

### Authenticate

```bash
# Interactive (recommended for local dev)
pc login
pc target -o "my-org" -p "my-project"

# Service account (recommended for CI/CD)
pc auth configure --client-id "$PINECONE_CLIENT_ID" --client-secret "$PINECONE_CLIENT_SECRET"

# API key (quick testing)
pc config set-api-key $PINECONE_API_KEY
```

Check status: `pc auth status` · `pc target --show`

> **Note for agent sessions**: If you need to run `pc login` inside an agent loop, the browser auth link may not surface correctly. It's best to authenticate **before** starting an agent session. Run `pc login` in your terminal directly, then invoke the agent once you're authenticated.

### Authenticating the CLI does not set `PINECONE_API_KEY`

`pc login` authenticates the CLI tool itself — it does **not** set `PINECONE_API_KEY` in your environment. Python scripts, Node.js SDKs, and other tools that use the Pinecone SDK need `PINECONE_API_KEY` set separately.

Use the CLI to create a key and export it in one step:

```bash
KEY=$(pc api-key create --name agent-sdk-key --json | jq -r '.value')
export PINECONE_API_KEY="$KEY"
```

Without `jq`: run `pc api-key create --name agent-sdk-key --json` and copy the `"value"` field manually.

---

## Common Commands

| Task | Command |
|---|---|
| List indexes | `pc index list` |
| Create serverless index | `pc index create -n my-index -d 1536 -m cosine -c aws -r us-east-1` |
| Index stats | `pc index stats -n my-index` |
| Upload vectors from file | `pc index vector upsert -n my-index --file ./vectors.json` |
| Query by vector | `pc index vector query -n my-index --vector '[0.1, ...]' -k 10 --include-metadata` |
| Query by vector ID | `pc index vector query -n my-index --id "doc-123" -k 10` |
| Fetch vectors by ID | `pc index vector fetch -n my-index --ids '["vec1","vec2"]'` |
| List vector IDs | `pc index vector list -n my-index` |
| Delete vectors by filter | `pc index vector delete -n my-index --filter '{"genre":"classical"}'` |
| List namespaces | `pc index namespace list -n my-index` |
| Create backup | `pc backup create -i my-index -n "my-backup"` |
| JSON output (for scripting) | Add `-j` to any command |

---

## Interesting Things You Can Do

### Query with custom vectors (not just text)
Unlike the MCP, the CLI lets you query any index with raw vector values — useful when you generate embeddings externally (OpenAI, HuggingFace, etc.):
```bash
pc index vector query -n my-index \
  --vector '[0.1, 0.2, ..., 0.9]' \
  --filter '{"source":{"$eq":"docs"}}' \
  -k 20 --include-metadata
```

### Pipe embeddings directly into queries
```bash
jq -c '.embedding' doc.json | pc index vector query -n my-index --vector - -k 10
```

### Bulk metadata update with preview
```bash
# Preview first
pc index vector update -n my-index \
  --filter '{"env":{"$eq":"staging"}}' \
  --metadata '{"env":"production"}' \
  --dry-run

# Apply
pc index vector update -n my-index \
  --filter '{"env":{"$eq":"staging"}}' \
  --metadata '{"env":"production"}'
```

### Backup and restore
```bash
# Snapshot before a migration
pc backup create -i my-index -n "pre-migration"

# Restore to a new index if something goes wrong
pc backup restore -i <backup-uuid> -n my-index-restored
```

### Automate in CI/CD
```bash
export PINECONE_CLIENT_ID="..."
export PINECONE_CLIENT_SECRET="..."
pc auth configure --client-id "$PINECONE_CLIENT_ID" --client-secret "$PINECONE_CLIENT_SECRET"
pc index vector upsert -n my-index --file ./vectors.jsonl --batch-size 1000
```

### Script against JSON output
```bash
# Get all index names as a list
pc index list -j | jq -r '.[] | .name'

# Check if an index exists before creating
if ! pc index describe -n my-index -j 2>/dev/null | jq -e '.name' > /dev/null; then
  pc index create -n my-index -d 1536 -m cosine -c aws -r us-east-1
fi
```

---

## Reference Files

- [Full command reference](references/command-reference.md) — all commands with flags and examples
- [Troubleshooting & best practices](references/troubleshooting.md)

## Documentation

- [CLI Quickstart](https://docs.pinecone.io/reference/cli/quickstart)
- [Command Reference](https://docs.pinecone.io/reference/cli/command-reference)
- [Authentication](https://docs.pinecone.io/reference/cli/authentication)
- [Target Context](https://docs.pinecone.io/reference/cli/target-context)
- [GitHub Releases](https://github.com/pinecone-io/cli/releases)
