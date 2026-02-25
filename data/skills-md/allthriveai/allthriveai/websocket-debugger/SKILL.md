---
name: websocket-debugger
description: Debug Django Channels WebSocket issues including connection failures, authentication, message handling, Redis pub/sub, and real-time streaming. Use when troubleshooting WebSocket not connecting, messages not received, connection dropped, or streaming not working.
allowed-tools: Read, Grep, Glob, Bash
---

# WebSocket Debugger

Analyzes and debugs Django Channels WebSocket issues in this project.

## Project Context

- WebSocket framework: Django Channels
- ASGI server: Daphne (in Docker)
- Message broker: Redis (channel layer)
- Authentication: JWT tokens via middleware
- Main consumer: `core/agents/consumers.py`
- Routing: `core/agents/routing.py`
- Middleware: `core/agents/middleware.py`

## WebSocket Architecture

```
Client (React)
    ↓ WebSocket connect
    ↓ ws://localhost:8000/ws/chat/<conversation_id>/
ASGI (Daphne)
    ↓ TokenAuthMiddleware (JWT auth)
ChatConsumer
    ↓ Redis channel group
    ↓ Celery task queue
LangGraph Agent
    ↓ Stream responses
    ↓ Redis pub/sub
ChatConsumer → Client
```

## When to Use

- "WebSocket not connecting"
- "Connection rejected/closed"
- "Messages not being received"
- "Streaming not working"
- "Authentication failing on WebSocket"
- "Redis channel issues"
- "Code 4001/4003 errors"

## Connection Close Codes

| Code | Meaning |
|------|---------|
| 4001 | Authentication failed - user not authenticated |
| 4003 | CORS/Origin not allowed |
| 4004 | Rate limited |
| 4005 | Invalid message format |

## Debugging Approach

### 1. Check Connection
```javascript
// Frontend: Check WebSocket readyState
// 0 = CONNECTING, 1 = OPEN, 2 = CLOSING, 3 = CLOSED
console.log(ws.readyState);
```

### 2. Verify Authentication
- Check JWT token is valid and not expired
- Verify token is passed correctly in query params or headers
- Check `TokenAuthMiddleware` is processing token

### 3. Check CORS/Origin
- Verify `CORS_ALLOWED_ORIGINS` in Django settings
- Check browser console for CORS errors
- Origin must match exactly (including port)

### 4. Verify Redis Connection
```bash
# Check Redis is running
docker compose exec redis redis-cli ping

# Monitor Redis pub/sub
docker compose exec redis redis-cli monitor
```

### 5. Check Channel Layer
```python
# Django shell - test channel layer
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
# Should not be None
```

## Common Issues

**WebSocket connection refused:**
```bash
# Check Daphne is running
docker compose logs web | grep -i daphne

# Verify ASGI config
# config/asgi.py should have ProtocolTypeRouter
```

**4001 Authentication error:**
```python
# Check middleware chain in config/asgi.py
application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
```

**Messages not received:**
```bash
# Check Celery worker is processing
docker compose logs celery

# Check Redis channel groups
docker compose exec redis redis-cli keys "asgi:*"
```

**Connection drops after 60s:**
- Implement heartbeat/ping-pong
- Check for proxy timeouts (nginx, load balancer)

## Key Files to Check

```
core/agents/
├── consumers.py      # ChatConsumer - main WebSocket handler
├── routing.py        # WebSocket URL patterns
├── middleware.py     # JWT authentication middleware
├── tasks.py          # Celery tasks for message processing
└── ws_connection_tokens.py  # Connection token management

config/
├── asgi.py           # ASGI application config
└── settings.py       # CHANNEL_LAYERS, CORS settings

frontend/src/
├── services/websocket.ts  # WebSocket client
└── hooks/useChat.ts       # Chat hook with WS
```

## Testing WebSocket

```bash
# Test script
python scripts/test_websocket.py

# Manual test with websocat
websocat "ws://localhost:8000/ws/chat/test-123/?token=YOUR_JWT"

# Or using wscat
wscat -c "ws://localhost:8000/ws/chat/test-123/" -H "Authorization: Bearer YOUR_JWT"
```

## Docker Logs

```bash
# Web server (Daphne) logs
docker compose logs -f web

# Redis logs
docker compose logs -f redis

# Celery worker logs
docker compose logs -f celery
```
