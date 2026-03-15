---
name: antigravity-bridge
description: Bridge Antigravity AI desktop app to REST API
---

# Antigravity Bridge

Turn Antigravity (free AI desktop app) into a REST API via Chrome DevTools Protocol (CDP).

## Usage

### Mode 1: Bridge API (Q&A)
```bash
# CLI
ag "Your question" [model]

# HTTP
curl -s -X POST http://localhost:19999/chat \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Your question","model":"Claude Opus 4.6 (Thinking)"}'
```

### Mode 2: IDE Agent (project tasks)
```bash
bash scripts/agy_invoke.sh "Task description" [--model opus]
```

## Parameters
- `model`: `opus` (Claude Opus 4.6), `gemini` (Gemini 3.1 Pro), `sonnet` (Claude Sonnet 4.6), `flash` (Gemini 3 Flash), `gpt` (GPT-OSS 120B)

## Examples
```bash
# Health check
curl -s http://localhost:19999/health

# Call Claude Opus
ag "Write a bash script" opus

# IDE agent task
bash scripts/agy_invoke.sh "Fix bug in common.sh" --model sonnet
```

## Requirements
- Mac with Antigravity installed and running
- Antigravity started with `--remote-debugging-port=9229`
- Bridge mode: run `bridge.py`
- IDE mode: Node.js with `ws` package

## Configuration
- Bridge port: `--port` (default: 19999)
- CDP port: `--cdp-port` (default: 9229)
- Host: `localhost` (or set `AG_BRIDGE_HOST` env var)
