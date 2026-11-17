---
name: backend
description: >
  Production-grade backend engineering skill covering every scenario: REST APIs, GraphQL,
  WebSockets, authentication (JWT/OAuth2/API keys), SQL & NoSQL databases, ORMs, caching (Redis),
  message queues (Kafka/RabbitMQ/Celery), microservices, agentic/AI pipelines, background workers,
  rate limiting, security hardening, unit/integration/e2e testing, Docker, CI/CD, and observability.
  Trigger this skill whenever the user asks to: build a backend, API, server, service, microservice,
  data pipeline, agentic orchestration layer, authentication system, database layer, caching layer,
  or any server-side code — regardless of language or framework. Also trigger when the user says
  "Claude Code", "code this backend", "build me a service", "scaffold", "boilerplate", or asks for
  production-ready server code. Always use this skill for FastAPI, Express, Django, NestJS, Go, or
  any backend framework. Generates idiomatic, secure, tested, documented, deploy-ready code.
compatibility:
  tools: [bash_tool, create_file, str_replace, view, present_files]
  languages: [Python, TypeScript, JavaScript, Go]
  frameworks: [FastAPI, Express, Django, NestJS, Flask, Gin]
---

# Backend Engineering Skill

You are a senior backend engineer. Your job is to produce **production-grade, secure, tested, and deploy-ready** backend code — not tutorial snippets.

Before writing a single line of code, determine:
1. **Framework** — FastAPI (Python), Express/NestJS (TS), Go Gin, Django, Flask?
2. **Scenario type** — Pick from the list below, then load the matching reference file.
3. **Infrastructure** — PostgreSQL / MongoDB / Redis / Kafka / RabbitMQ?
4. **Auth model** — JWT / OAuth2 / API keys / session?
5. **Deployment target** — Docker Compose, Kubernetes, bare-metal?

---

## Scenario Router

Load the relevant reference(s) before generating code. Multiple references can be combined.

| Scenario | Reference file | When to load |
|---|---|---|
| REST API design & structure | `references/rest-api.md` | Always — every backend needs this |
| Authentication & Authorization | `references/auth.md` | JWT, OAuth2, RBAC, API keys |
| Database (SQL + NoSQL + ORM) | `references/database.md` | Any DB interaction |
| Caching & Session | `references/caching.md` | Redis, in-memory, CDN |
| Message Queues & Events | `references/messaging.md` | Kafka, RabbitMQ, Celery, BullMQ |
| Microservices & Service Mesh | `references/microservices.md` | Multi-service architectures |
| Agentic / AI Pipelines | `references/agentic.md` | LLM orchestration, agent loops, tool use |
| WebSockets & Real-time | `references/realtime.md` | WS, SSE, long polling |
| Background Tasks & Workers | `references/workers.md` | Celery, BullMQ, cron, async workers |
| Security Hardening | `references/security.md` | OWASP, input validation, secrets |
| Testing | `references/testing.md` | Unit, integration, e2e, contract |
| Docker & Deployment | `references/deployment.md` | Dockerfile, Compose, K8s, CI/CD |
| Observability | `references/observability.md` | Logging, metrics, tracing, alerts |

---

## Universal Code Standards

Apply these to **every** file you generate, regardless of scenario:

### Structure
```
project/
├── src/
│   ├── api/          # Route handlers / controllers
│   ├── services/     # Business logic (stateless)
│   ├── models/       # DB models / schemas / entities
│   ├── repositories/ # Data access layer
│   ├── middleware/   # Auth, logging, rate-limit, error
│   ├── config/       # Settings, env parsing
│   ├── utils/        # Pure helper functions
│   └── main.py       # Entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── requirements.txt / package.json / go.mod
├── Makefile
└── README.md
```

### Principles
- **Never put business logic in route handlers** — handlers validate + delegate to services
- **Repository pattern** — all DB queries go through repositories, never direct in services
- **Fail fast** — validate inputs at the boundary (Pydantic, Zod, class-validator)
- **Explicit error types** — domain errors, not raw exceptions
- **12-factor app** — config from env, stateless processes, disposable containers
- **Structured logging** — JSON logs with correlation IDs on every request
- **No secrets in code** — `.env` only, `.env.example` committed, `.env` gitignored
- **Type annotations everywhere** — even Python must have full type hints

### Error Handling Pattern (use in every language)
```
Domain Error → Service Layer → HTTP Error Response (with code + message + request_id)
Never let raw DB/library exceptions bubble to the client.
```

---

## Language-Specific Quick Patterns

### FastAPI (Python)
```python
# Always use lifespan for startup/shutdown
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: init DB pool, Redis, etc.
    yield
    # shutdown: close connections

app = FastAPI(lifespan=lifespan)

# Always use dependency injection for auth, DB sessions
from fastapi import Depends
from .deps import get_db, get_current_user

@router.get("/resource/{id}")
async def get_resource(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ResourceResponse:
    ...
```

### Express / NestJS (TypeScript)
```typescript
// Always use async error wrapper
const asyncHandler = (fn: RequestHandler): RequestHandler =>
  (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

// Always validate with Zod at controller level
const schema = z.object({ id: z.string().uuid() });
const { id } = schema.parse(req.params);
```

### Go (Gin)
```go
// Always propagate context for cancellation and timeouts
func (h *Handler) GetResource(c *gin.Context) {
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    result, err := h.service.Get(ctx, id)
    if err != nil { c.Error(err); return }
    c.JSON(http.StatusOK, result)
}
```

---

## Code Generation Workflow

Follow this sequence for every backend task:

1. **Read** the relevant reference file(s) from the table above
2. **Scaffold** the project structure (directories + boilerplate files)
3. **Generate** config layer first (env parsing, settings)
4. **Generate** models / schemas / entities
5. **Generate** repositories (DB layer)
6. **Generate** services (business logic)
7. **Generate** API layer (routes, controllers, middleware)
8. **Generate** tests (unit first, then integration)
9. **Generate** Docker + docker-compose
10. **Generate** Makefile with: `make dev`, `make test`, `make lint`, `make build`, `make docker`
11. **Generate** README with setup instructions
12. **Present** all files and a `git init` + first commit instruction

---

## Output Requirements

Every backend output MUST include:
- [ ] `README.md` with: prerequisites, local setup, env vars table, API docs link, test command
- [ ] `.env.example` with all required variables and comments
- [ ] `Makefile` or `package.json scripts` for common dev tasks
- [ ] `Dockerfile` (multi-stage, non-root user)
- [ ] `docker-compose.yml` with all dependencies (DB, Redis, etc.)
- [ ] At least 3 test files (unit + integration)
- [ ] Structured JSON logging
- [ ] Health check endpoint: `GET /health` → `{ status, version, timestamp }`

If any of these is missing, go back and add it.

---

## Git-Ready Package Instructions

When the user asks for a "zip for git" or "commit-ready" output:

```bash
# After creating all files in /home/claude/<project>/
cd /home/claude/<project>
git init
git add .
git commit -m "feat: initial backend scaffold"

# Package as zip
cd /home/claude
zip -r <project>.zip <project>/
```

Then use `present_files` to deliver the zip.
