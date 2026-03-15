---
name: zeabur-port-mismatch
description: Use when proxy shows dial tcp timeout or i/o timeout. Use when service port doesn't match proxy expectation.
---

# Zeabur Port Mismatch

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Symptom

```
dial tcp 10.x.x.x:3000: i/o timeout
dial tcp 10.x.x.x:80: connection refused
```

## Cause

Proxy expects service on port X, but service listens on port Y.

## Diagnose

1. Check what port proxy expects (from Caddyfile/nginx.conf)
2. Check what port container exposes (Dockerfile `EXPOSE`)

## Common Mismatches

| Proxy expects | Container has | Fix |
|---------------|---------------|-----|
| `:3000` | nginx default `:80` | Change template port to 80 |
| `:80` | app on `:3000` | Change template port to 3000 |

## Fix in Template

```yaml
ports:
  - id: web
    port: 3000  # Match what container actually exposes
    type: HTTP
```

**Check official Dockerfile for `EXPOSE` directive.**

## Headless Service (502 with no listener)

### Symptom

Service is running (no crash), but proxy returns **502 Bad Gateway** permanently.

### Cause

Service does not listen on any HTTP port. Examples: chatbot gateways, background workers, message queue consumers. The template declares an HTTP port but nothing binds to it.

### Fix

Add a lightweight HTTP health check server that runs in the background alongside the main process:

```bash
# Start before main process in startup script
# IMPORTANT: port must match spec.ports[].port in your template
python3 -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status':'ok'}).encode())
    def log_message(self,*a): pass
HTTPServer(('0.0.0.0', 8080), H).serve_forever()
" &
exec my-headless-app
```

## See Also

- `zeabur-template` — template YAML reference for port configuration
- `zeabur-deployment-logs` — check logs to confirm port binding
