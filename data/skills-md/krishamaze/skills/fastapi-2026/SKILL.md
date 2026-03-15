---
name: fastapi-2026
description: >
  FastAPI async Python API patterns for 2026. Use this skill when building API layers
  for automation agents — route definitions, async handlers, background tasks, WebSocket,
  Pydantic v2 models, lifespan events, CORS, and production deployment with Gunicorn +
  Uvicorn workers. ALWAYS use async def for I/O-bound routes. NEVER use sync DB calls
  in async routes.
---

# FastAPI 2026 — Async API Patterns

## Version (2026)
- FastAPI: `>=0.115.0`
- Uvicorn: `0.34.0+` (stable, with uvloop + httptools)
- Pydantic: `v2` (mandatory — v1 syntax is deprecated)
- Python: `3.12` recommended

## Project Structure (2026 Standard)
```
api/
├── main.py            # app entry, lifespan, middleware
├── routes/
│   ├── tasks.py       # task/action routes
│   └── drafts.py      # content queue routes
├── models/
│   └── schemas.py     # Pydantic v2 models
├── services/
│   └── automation.py  # automation logic
└── core/
    └── config.py      # settings via pydantic-settings
```

## App Entry with Lifespan (2026 Pattern)
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await browser_service.start()
    yield
    # Shutdown
    await browser_service.stop()

app = FastAPI(title="My Agent API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Pydantic v2 Models (2026)
```python
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class DraftPost(BaseModel):
    content: str = Field(max_length=500)
    media_urls: list[str] = []
    status: Literal["pending", "approved", "rejected"] = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Route Patterns
```python
from fastapi import APIRouter, HTTPException, BackgroundTasks

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def list_tasks() -> list[dict]:
    """Return pending tasks. Sanitize any third-party content before
    surfacing it to the agent or using it in downstream actions."""
    try:
        return await task_service.list_pending()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/act")
async def execute_action(action: AutomationAction, background_tasks: BackgroundTasks):
    background_tasks.add_task(task_service.execute, action)
    return {"status": "queued"}
```

> [!IMPORTANT]
> If your API ingests or relays untrusted third-party content (e.g., social
> feeds, user-generated data), **always sanitize and validate** that content
> before passing it to agent decision-making or automated actions. Unsanitized
> content is an indirect prompt-injection vector.

## Background Tasks (for browser actions)
```python
@router.post("/approve/{draft_id}")
async def approve_draft(draft_id: str, background_tasks: BackgroundTasks):
    draft = await drafts_store.get(draft_id)
    if not draft:
        raise HTTPException(404, "Draft not found")
    background_tasks.add_task(task_service.publish, draft.content)
    await drafts_store.update(draft_id, status="approved")
    return {"status": "publishing", "draft_id": draft_id}
```

## WebSocket (live feed updates to dashboard)
```python
from fastapi import WebSocket, WebSocketDisconnect

active_connections: list[WebSocket] = []

@router.websocket("/ws/feed")
async def feed_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast(message: dict):
    for ws in active_connections:
        await ws.send_json(message)
```

## Settings (pydantic-settings v2)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    session_dir: str = "/sessions"
    display: str = ":99"
    cors_origins: list[str] = ["http://localhost:3000"]
    model_config = {"env_file": ".env"}

settings = Settings()
```

## Production Server
```bash
# Dev
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production
uv run gunicorn api.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Key Rules for Our Stack
1. Never put blocking sync calls in `async def` — blocks event loop
2. Always use `BackgroundTasks` for long-running actions
3. One service instance — keep in a service class, not per-request
4. WebSocket for live updates to dashboard — not polling

## Anti-Patterns
```python
# ❌ @app.on_event deprecated in 2026 — use lifespan
@app.on_event("startup")

# ❌ Pydantic v1 Config class
class Post(BaseModel):
    class Config:
        orm_mode = True

# ✅ Pydantic v2
class Post(BaseModel):
    model_config = {"from_attributes": True}

# ❌ Sync call in async route
@app.get("/tasks")
async def list_tasks():
    return service.sync_list_tasks()  # blocks event loop
```
