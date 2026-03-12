---
name: vector-db-launch
description: Start the Native Python ChromaDB background server. Use when semantic search returns connection refused on port 8110, or when the user wants to enable concurrent agent read/writes.
---
# Vector DB Launch (Python Native Server)

ChromaDB provides the vector database backend for semantic search. If configured for Option C (Native Server) in `vector_profiles.json`, the database must be running as a background HTTP service to be accessed by `operations.py`.

## When You Need This

- **RAG ingest fails** with connection refused to `127.0.0.1:8110`
- **Semantic search** hangs or fails to connect
- The user has explicitly selected **Option 2 (Python Native Server)** during `vector-db-init`

## Pre-Flight Check

```bash
# Check if ChromaDB is already running
curl -sf http://127.0.0.1:8110/api/v1/heartbeat > /dev/null && echo "✅ ChromaDB running" || echo "❌ ChromaDB not running"
```

If it prints "✅ ChromaDB running", you're done. If not, proceed.

## Launching the Server (Native Python)

The ChromaDB server runs as a background Python process. 

It binds to the `${chroma_host}:${chroma_port}` defined in your active profile inside `.agent/learning/vector_profiles.json` (defaults to `127.0.0.1:8110`). Its data volume is mounted from the path defined by the profile's `${chroma_data_path}`.

### Step 1: Start the Service via CLI
Instruct the user to start the server as a background process using `nohup` or `&` so it does not block their terminal. Example:

```bash
chroma run --host 127.0.0.1 --port 8110 --path .vector_data &
```

### Step 2: Verify Connection
After the user confirms the server is running, verify it via API:

```bash
curl -sf http://127.0.0.1:8110/api/v1/heartbeat
```

It should return a JSON response containing a timestamp `{"nanosecond heartbeat": ...}`.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `chroma: command not found` | The user hasn't run the `vector-db-init` skill yet. Run it to `pip install chromadb`. |
| Port 8110 already in use | Another process (or zombie chroma process) is using the port. `lsof -i :8110` to find and kill it. |
| Permission Denied for data directory | Ensure the user has write access to the `.vector_data` directory. |

## Alternative: In-Process Mode
If the user decides they do not want to run a background server, you can instruct them to set `chroma_host` to an empty string `""` in their profile in `.agent/learning/vector_profiles.json`. 

The `operations.py` library will automatically fallback to "Option A" (`PersistentClient`) and initialize the database locally inside the python process without needing this skill.
