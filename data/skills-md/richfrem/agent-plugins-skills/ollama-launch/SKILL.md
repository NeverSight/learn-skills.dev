---
name: ollama-launch
description: Start and verify the local Ollama LLM server. Use when Ollama is needed for RLM distillation, seal snapshots, embeddings, or any local LLM inference — and it's not already running. Checks if Ollama is running, starts it if not, and verifies the health endpoint.
---
# Ollama Launch

Ollama provides local LLM inference for RLM distillation (seal phase summarization) and embeddings.

## When You Need This

- **Seal fails** with `Connection refused` to `127.0.0.1:11434`
- **RLM distillation** shows `[DISTILLATION FAILED]` for new files
- Any tool that calls the Ollama API locally

## Pre-Flight Check

```bash
# Check if Ollama is already running
curl -sf http://127.0.0.1:11434/api/tags > /dev/null && echo "✅ Ollama running" || echo "❌ Ollama not running"
```

If running, you're done. If not, proceed.

## Start Ollama

```bash
# Start Ollama in the background
ollama serve &>/dev/null &

# Wait and verify (2-3 seconds)
sleep 3
curl -sf http://127.0.0.1:11434/api/tags > /dev/null && echo "✅ Ollama ready" || echo "❌ Ollama failed to start"
```

## Verify Model Available

For RLM distillation, the project uses model you define in .env

```bash
# List available models
ollama list

# If the model is missing, pull it
ollama pull qwen2:7b
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Connection refused` after start | Wait longer (`sleep 5`), model may be loading |
| `ollama: command not found` | Ollama not installed — ask user to install from https://ollama.com |
| Port 11434 already in use | Another process on that port — `lsof -i :11434` to identify |

## Integration Points

- **Learning Loop Seal Phase**: RLM synthesis calls Ollama for distillation
- **RLM Factory**: `/rlm-factory:distill` requires Ollama for batch summarization
- **Embeddings**: Any tool that needs local vector embeddings
