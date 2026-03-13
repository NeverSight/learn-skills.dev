---
name: architect-python-uv-fastapi-sqlalchemy
description: Use when scaffolding production-ready FastAPI services with uv, SQLAlchemy, Alembic, Postgres, Docker, and CI gates.
---

# Architect: Python + uv + FastAPI + SQLAlchemy

Use this skill when the user wants a production API scaffold in Python with modern packaging (`uv`), database migrations, containerization, and CI.
Docker is required by default for this runnable base architect skill. Only allow `NO_DOCKER=yes` when the user explicitly asks for a local-only exception.

## Inputs

Collect these values first:
- `PROJECT_NAME`: kebab-case repository/folder name.
- `MODULE_NAME`: import-safe module name (usually snake_case).
- `PYTHON_VERSION`: default `3.12`.
- `DATABASE_URL`: runtime DB URL.
- `NO_DOCKER`: default `no`. Set `yes` only when user explicitly opts out of containerization.

Use these version defaults unless user requests otherwise:
- `uv` latest stable via `astral-sh/setup-uv`
- Python `3.12`
- `postgres:16-alpine`

## Preflight Checks

Run before scaffolding:
```bash
command -v uv >/dev/null && uv --version || echo "uv-missing"
python3 --version
command -v docker >/dev/null && docker --version || echo "docker-missing"
```

Execution modes:
- `production-default`: create and validate container artifacts (`NO_DOCKER=no`).
- `local-no-docker`: skip container files only when user explicitly sets `NO_DOCKER=yes`.
- `offline-smoke`: tools/network constrained; scaffold structure and report verification limits.

Production-default contract:
- Must create `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.
- Must include CI image build check.
- Must run containerized smoke validation.

## Scaffold Workflow

1. Initialize project:
```bash
uv init --package {{PROJECT_NAME}}
cd {{PROJECT_NAME}}
```

2. Install runtime and dev dependencies:
```bash
uv add fastapi "uvicorn[standard]" sqlalchemy asyncpg alembic pydantic-settings
uv add -d pytest pytest-asyncio httpx ruff mypy
```

3. Create source layout:
```text
src/{{MODULE_NAME}}/
  api/routes/health.py
  core/config.py
  db/base.py
  db/session.py
  main.py
tests/
```

4. Initialize Alembic and wire metadata:
```bash
uv run alembic init alembic
```
- Set `alembic.ini` `sqlalchemy.url` to `${DATABASE_URL}`.
- In `alembic/env.py`, import `Base.metadata` from `src/{{MODULE_NAME}}/db/base.py`.

5. Add infrastructure and CI files (`NO_DOCKER=no`):
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `.github/workflows/ci.yml`
If `NO_DOCKER=yes`, document this exception in project notes and keep non-container validation.

## Required File Templates

### `src/{{MODULE_NAME}}/core/config.py`
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    app_name: str = "api"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/app"


settings = Settings()
```

### `src/{{MODULE_NAME}}/db/base.py`
```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

### `src/{{MODULE_NAME}}/db/session.py`
```python
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from {{MODULE_NAME}}.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
```

### `src/{{MODULE_NAME}}/api/routes/health.py`
```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
```

### `src/{{MODULE_NAME}}/main.py`
```python
from fastapi import FastAPI

from {{MODULE_NAME}}.api.routes.health import router as health_router

app = FastAPI(title="{{PROJECT_NAME}}")
app.include_router(health_router)
```

### `Dockerfile`
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:3.12-slim AS run
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home --shell /bin/bash app
COPY --from=build /app/.venv /app/.venv
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
ENV PATH="/app/.venv/bin:$PATH"
USER app
EXPOSE 8000
CMD ["uvicorn", "{{MODULE_NAME}}.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `.dockerignore`
```gitignore
.git
.venv
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
*.pyc
dist
build
```

### `docker-compose.yml`
```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 5s
      retries: 20
    volumes:
      - pg_data:/var/lib/postgresql/data

  api:
    build: .
    environment:
      DATABASE_URL: postgresql+asyncpg://app:app@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"

volumes:
  pg_data:
```
Keep `ports: - "8000:8000"` on the `api` service so the host can reach the app. If documenting direct `docker run` usage for the API image, include `-p 8000:8000` and the required `DATABASE_URL`; `docker compose` remains the default local path because it provides the database too.

### `.github/workflows/ci.yml`
```yaml
name: ci
on:
  push:
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
      - name: Install deps
        run: uv sync --frozen --dev
      - name: Ruff
        run: uv run ruff check .
      - name: Ruff Docstrings
        run: uv run ruff check . --select D
      - name: Mypy
        run: uv run mypy src
      - name: Pytest
        run: uv run pytest -q
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: {{PROJECT_NAME}}:ci
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Keep async DB stack consistent (`sqlalchemy.ext.asyncio` + `asyncpg`).
- Never hardcode secrets; use environment variables and `.env`.
- Ensure Alembic migrations are generated and committed.
- Ensure container runs as non-root user.
- Prefer `docker compose` in docs and scripts.
- Treat `NO_DOCKER=yes` as an explicit exception, not default behavior.
- Ensure `uv.lock` is committed before Docker build; the Dockerfile copies it explicitly for deterministic `uv sync --frozen` installs.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


Run and fix failures before finishing:
```bash
uv run ruff check .
uv run ruff check . --select D
uv run mypy src
uv run pytest -q
uv run alembic upgrade head
test -f uv.lock
docker build -t {{PROJECT_NAME}}:local .
docker compose up -d --build
docker compose ps
curl http://localhost:8000/healthz
```
`local-no-docker` (`NO_DOCKER=yes`):
```bash
uv run ruff check .
uv run ruff check . --select D
uv run mypy src
uv run pytest -q
uv run alembic upgrade head
```
Fallback (`offline-smoke`):
```bash
python3 -m compileall src
test -f Dockerfile || echo "docker-artifacts-missing-in-offline-smoke"
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
