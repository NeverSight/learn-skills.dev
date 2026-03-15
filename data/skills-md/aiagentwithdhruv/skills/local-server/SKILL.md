---
name: local-server
description: Run Claude orchestrator locally with Cloudflare tunneling. Use when user asks to run locally, start local server, or test webhooks locally.
---

# Local Server Execution

## Goal
Run the Claude orchestrator locally with Cloudflare tunnel for external webhook access.

## Start Server
```bash
python3 execution/local_server.py
```

Starts FastAPI server on port 8000.

## Cloudflare Tunnel
For external access (webhooks), use Cloudflare tunnel:
```bash
cloudflared tunnel --url http://localhost:8000
```

## Endpoints
Same as Modal deployment:
- `/directive?slug={slug}` - Execute directive
- `/list-webhooks` - List webhooks
- `/general-agent` - General agent tasks

## Development Use
- Faster iteration than Modal deploys
- Full access to local files and credentials
- Real-time debugging with print statements

## Environment
Uses local `.env` file directly (unlike Modal which uses secrets).

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `port` | integer | No | Server port (default: 8000) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `server_url` | string | Local server URL (http://localhost:8000) |
| `tunnel_url` | string | Cloudflare tunnel URL (if enabled) |

### Composable With
Skills that chain well with this one: `add-webhook`

### Cost
Free (local execution)
