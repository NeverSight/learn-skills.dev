---
name: architect-python-uv-batch
description: Use when scaffolding production-ready Python uv batch or worker projects with Docker required by default.
---

# Architect: Python + uv Batch

Use this skill for non-API Python projects that run as CLI or scheduled jobs, especially data/PDF processing pipelines.
Docker is required by default for this runnable base architect skill. Only allow `NO_DOCKER=yes` when the user explicitly asks for a local-only exception.

## Inputs

Collect these values:
- `PROJECT_NAME`: kebab-case repo/folder name.
- `MODULE_NAME`: snake_case import package.
- `PYTHON_VERSION`: default `3.12`.
- `USE_RAG`: `yes` or `no`.
- `EMBED_PROVIDER`: `openai` or `sentence-transformers` (default local `sentence-transformers`).
- `NO_DOCKER`: default `no`. Set to `yes` only when user explicitly opts out of containerization.

## Preflight Checks

Run before scaffolding:
```bash
command -v uv >/dev/null && uv --version || echo "uv-missing"
python3 --version
command -v docker >/dev/null && docker --version || echo "docker-missing"
```

Execution modes:
- `production-default`: `uv` + `docker` available; emit and validate container artifacts.
- `local-no-docker`: user explicitly sets `NO_DOCKER=yes`.
- `offline-smoke`: `uv` missing and/or no network; scaffold file structure and stdlib smoke path, then record constraints in `TEST_NOTES.md`.

Production-default contract:
- Must create `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.
- Must include CI image build check.
- Must run at least one containerized smoke command in validation.

## Scaffold Workflow

1. Initialize project (`production-default` or `local-no-docker`):
```bash
uv init --package {{PROJECT_NAME}}
cd {{PROJECT_NAME}}
```
If `offline-smoke` mode is required, create equivalent structure manually and keep commands runnable via:
```bash
PYTHONPATH=src python3 -m {{MODULE_NAME}}.cli ingest-pdf
python3 -m unittest discover -s tests -v
```

2. Add core dependencies:
```bash
uv add pydantic-settings typer rich pypdf pandas orjson
uv add -d pytest ruff mypy
```

3. If `USE_RAG=yes`, add RAG dependencies:
```bash
uv add langchain-text-splitters chromadb
```
- For local embeddings:
```bash
uv add sentence-transformers
```
- For OpenAI embeddings:
```bash
uv add openai
```

4. Create structure:
```text
src/{{MODULE_NAME}}/
  cli.py
  core/config.py
  pipelines/pdf_ingest.py
  pipelines/normalize.py
  rag/chunk.py
  rag/embed.py
  rag/store.py
tests/
  test_ingest.py
data/inbox/
data/processed/
```
If `NO_DOCKER=no`, also create:
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`

5. Wire command entrypoint in `pyproject.toml`:
```toml
[project.scripts]
{{PROJECT_NAME}} = "{{MODULE_NAME}}.cli:main"
```

## Required Defaults

### `src/{{MODULE_NAME}}/core/config.py`
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    environment: str = "development"
    inbox_dir: str = "data/inbox"
    processed_dir: str = "data/processed"
    embed_provider: str = "sentence-transformers"
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai_api_key: str | None = None
    chroma_path: str = ".chroma"


settings = Settings()
```

### `src/{{MODULE_NAME}}/cli.py`
```python
import typer

from {{MODULE_NAME}}.pipelines.pdf_ingest import run_pdf_ingest

app = typer.Typer(no_args_is_help=True)


@app.command("ingest-pdf")
def ingest_pdf() -> None:
    run_pdf_ingest()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
```

### `src/{{MODULE_NAME}}/pipelines/pdf_ingest.py`
```python
import hashlib
from pathlib import Path

from pypdf import PdfReader

from {{MODULE_NAME}}.core.config import settings


def run_pdf_ingest() -> None:
    inbox = Path(settings.inbox_dir)
    out = Path(settings.processed_dir)
    out.mkdir(parents=True, exist_ok=True)
    for pdf_path in inbox.glob("*.pdf"):
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)
        suffix = hashlib.sha1(str(pdf_path).encode("utf-8")).hexdigest()[:8]
        target = out / f"{pdf_path.name}.{suffix}.txt"
        target.write_text(text, encoding="utf-8")
```

### `tests/test_ingest.py` (import-safe for `unittest discover`)
```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from {{MODULE_NAME}}.pipelines.pdf_ingest import run_pdf_ingest
```

### `Dockerfile` (`NO_DOCKER=no`)
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-dev
COPY data ./data

FROM python:3.12-slim AS run
WORKDIR /workspace
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home --shell /bin/bash app
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app /workspace
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/workspace/src"
RUN chown -R app:app /workspace
USER app
CMD ["python", "-m", "{{MODULE_NAME}}.cli", "ingest-pdf"]
```

### `.dockerignore` (`NO_DOCKER=no`)
```gitignore
.git
.venv
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
data/processed
```

### `docker-compose.yml` (`NO_DOCKER=no`)
```yaml
services:
  app:
    build: .
    environment:
      INBOX_DIR: /workspace/data/inbox
      PROCESSED_DIR: /workspace/data/processed
    volumes:
      - ./data:/workspace/data
    command: ["python", "-m", "{{MODULE_NAME}}.cli", "ingest-pdf"]
```
Do not add a `ports:` block by default for batch workers. They are one-shot or background jobs, not HTTP services; use volumes and explicit commands instead.

## CI + Quality

Create `.github/workflows/ci.yml`:
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
      - run: uv sync --frozen --dev
      - run: uv run ruff check .
      - run: uv run ruff check . --select D
      - run: uv run mypy src
      - run: uv run pytest -q
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


- Keep batch jobs idempotent; output paths must be safe to re-run.
- Make output names collision-safe across formats and paths (include extension and a stable suffix/hash).
- Never commit secrets; use `.env` and environment variables.
- Keep processing logic pure where possible, IO at pipeline edges.
- If RAG is optional, keep `rag/*` modules decoupled from non-RAG pipelines.
- Treat `NO_DOCKER=yes` as an explicit exception, not a default path.
- Ensure tests can run via plain `python3 -m unittest discover -s tests -v` without requiring `PYTHONPATH` for imports.
- Ensure `uv.lock` is committed before Docker build; the Dockerfile copies it explicitly for deterministic `uv sync --frozen` installs.
- Ensure any runtime output directories under `/workspace` are writable by the non-root app user.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run ruff check .
uv run ruff check . --select D
uv run mypy src
uv run pytest -q
uv run {{PROJECT_NAME}} ingest-pdf
test -f uv.lock
docker build -t {{PROJECT_NAME}}:local .
docker compose run --rm app
```
`local-no-docker` (`NO_DOCKER=yes`):
```bash
uv run ruff check .
uv run ruff check . --select D
uv run mypy src
uv run pytest -q
uv run {{PROJECT_NAME}} ingest-pdf
```
Fallback (`offline-smoke`):
```bash
PYTHONPATH=src python3 -m {{MODULE_NAME}}.cli ingest-pdf
python3 -m unittest discover -s tests -v
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
