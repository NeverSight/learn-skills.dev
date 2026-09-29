---
name: backend-development
description: Production-ready Python backend development with FastAPI. Use this skill whenever the user is building a backend API, structuring a Python service, designing domain layers, creating repositories, setting up dependency injection, writing Dockerfiles, configuring CI pipelines, implementing tests, or making any architectural decision about a Python backend. Covers light DDD, SOLID principles, FastAPI patterns, Pydantic validation, structured logging, container security, and testing strategy. Every feature must include its corresponding tests.
---

This skill guides building production-ready Python backends following modern architecture, security, and testing best practices. Every implementation decision should favor simplicity, testability, and strong typing.

## When to Use

Use this skill when:
- Designing or building backend APIs
- Creating FastAPI services
- Implementing repositories, services, or domain logic
- Structuring a Python project with clean architecture
- Writing Dockerfiles or docker-compose configurations
- Setting up CI pipelines
- Writing backend tests

## Architecture

- Python with **strict type hints** on every function, method, and public interface
- **FastAPI** for APIs — automatic validation, OpenAPI docs, dependency injection, async support
- **Pydantic** for all validation and data parsing at boundaries
- **Light DDD** with 4 layers: `domain/`, `application/`, `infrastructure/`, `api/`
- Follow **SOLID** principles — prefer composition over inheritance
- **KISS** — design patterns (repository, factory, builder, singleton, strategy) only when they earn their complexity
- Use **Typer** for CLI scripts (not argparse)
- Configuration from **config.yaml** parsed by Pydantic Settings at startup

## Layers

### `domain/`
- Entities as Pydantic BaseModel
- Value objects
- Repository interfaces as ABCs (`@abstractmethod`)
- Domain-specific error types
- **NEVER**: framework imports, fetch calls, DB queries, FastAPI dependencies

### `application/`
- Services/use cases that orchestrate domain logic
- Depend only on ABCs — never on concrete implementations
- Framework-agnostic: no FastAPI, no SQLAlchemy imports
- Return typed results (Result pattern for expected errors)

### `infrastructure/`
- Repository implementations (SQLAlchemy, Redis, external APIs)
- Database session management
- ORM models and mappers (SQL model <-> domain entity)
- External API clients, SDK integrations
- **The ONLY layer that knows about the outside world**

### `api/`
- FastAPI routers with versioned routes (`/api/v1/`)
- Dependency injection via `Depends()` for DB sessions, repositories, auth
- Pydantic request/response schemas (separate from domain entities)
- Middleware (request ID, logging, CORS)
- Clear tags for Swagger documentation

## Code Principles

- **Type hint everything** — function signatures, return types, class attributes
- **PEP8 naming** — snake_case for functions/variables/modules, PascalCase for classes, UPPER_SNAKE_CASE for constants
- **Ruff** for linting and formatting, **MyPy** in strict mode for type checking
- **Small focused functions** — if it exceeds 20-30 lines, split it
- **OOP for services and repositories** (stateful, injectable dependencies)
- **Functional for mappers, validators, and helpers** (pure transforms, no state)
- **No `utils.py`, `helpers.py`, `common.py`** — use contextual names: `recipe_title_formatter.py`, `date_range_validator.py`
- **Structured logging only** — never use `print()`. Use `structlog` or JSON formatter with proper levels
- **Docstrings** on use cases, ABCs, non-trivial mappers, and public APIs. Not on obvious code

## API Design

- **Versioned routes**: `/api/v1/recipes`, `/api/v1/users`
- **Clear FastAPI tags** for organized Swagger docs
- **Dependency injection** for database sessions, repositories, and current user:
  ```python
  @router.get("/recipes")
  async def list_recipes(service: RecipeService = Depends(get_recipe_service)):
      return await service.list_all()
  ```
- **Consistent error responses**: `{"detail": str, "code": str, "fields": Optional[dict]}`
- **Pagination** for large collections using offset/limit with a standard response wrapper
- **Pydantic schemas** for request bodies and responses — separate from domain entities
- **Lifespan events** for startup/shutdown: DB pool creation, config loading

## Testing — MANDATORY

**Every feature implementation MUST include its corresponding tests.** No feature is complete without tests.

- **pytest** as the testing framework, with **pytest-cov** for coverage
- **pytest-asyncio** for testing async code
- **testcontainers** for integration tests with real infrastructure (PostgreSQL, Redis)
- **FastAPI TestClient** for API-level tests

### Test Organization
```
tests/
  conftest.py          # Shared fixtures
  unit/                # Fast, isolated, no external dependencies
    test_recipe_service.py
    test_recipe_mappers.py
  integration/         # Real infrastructure via testcontainers
    test_recipe_repository.py
  api/                 # Full API tests via TestClient
    test_recipe_endpoints.py
```

### Testing Strategy by Layer
| Layer | Test type | How |
|-------|-----------|-----|
| domain/ | Unit | Pure logic, no mocking needed |
| application/ | Unit | Fake repositories (classes implementing the ABC with in-memory lists) |
| infrastructure/ | Integration | testcontainers with real PostgreSQL |
| api/ | API | FastAPI TestClient with overridden dependencies |

### Coverage
- Target: **80% branch coverage** minimum
- Critical paths (auth, payments): **95%+**
- Run: `pytest --cov=src --cov-report=term --cov-report=html`

## Observability

- **Structured logging** with `structlog` or Python `logging` + JSON formatter
- **Request ID middleware** — generate UUID per request, propagate to all log entries, return in response headers
- **Log levels**:
  - DEBUG: development detail, query parameters
  - INFO: business events (user created, recipe saved)
  - WARNING: recoverable issues (retry succeeded, deprecated endpoint called)
  - ERROR: failures requiring attention (DB connection lost, external API down)
- **Never log**: secrets, passwords, tokens, full request bodies with PII

## Security

- **Validate ALL external inputs** with Pydantic — API payloads, query params, config values, env vars
- **Never expose secrets** in code, config.yaml, logs, or Docker images — inject at runtime via env vars or secret management
- **Dependency vulnerability scanning** — `pip-audit` or `safety` in CI
- **No unsafe shell execution** — use `subprocess` with `shell=False`, sanitize all inputs with `shlex`
- **Input size limits** — set max request body size, max query result limits

## Container Security

Apply these rules to every Dockerfile and docker-compose configuration:

- **Minimal base images** with pinned versions: `python:3.12.3-slim-bookworm` (never `latest`)
- **Non-root execution**: create `appuser`, `USER appuser` in Dockerfile
- **Read-only filesystem**: `--read-only` or `read_only: true` in compose
- **Drop ALL capabilities**: `cap_drop: [ALL]` — add back only what is strictly needed
- **No privilege escalation**: `security_opt: [no-new-privileges:true]`
- **Resource limits**: set `cpus` and `mem_limit` for every container
- **Network isolation**: separate Docker networks for DB, cache, and API tiers
- **No secrets in images**: never `COPY .env`, never `ARG PASSWORD` — inject at runtime
- **Multi-stage builds**: builder stage installs deps, runtime stage copies only the wheel/app
- **Health checks**: `HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1`
- **Reverse proxy**: put nginx/traefik in front — never expose FastAPI directly to the internet
- **Vulnerability scanning**: run `trivy` or `grype` on images in CI
- **Never mount** Docker socket (`/var/run/docker.sock`) or sensitive host paths
- **Least-privilege file permissions**: app directories writable only when necessary
- **Regular updates**: keep base images and dependencies patched

## Project Structure

```
my-service/
├── src/
│   ├── domain/                 # Entities, ABCs, errors
│   ├── application/            # Services, use cases
│   ├── infrastructure/         # Repos, DB, external clients, mappers
│   ├── api/                    # Routers, deps, middleware, schemas
│   └── config.py               # Pydantic Settings parsing config.yaml
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── api/
├── scripts/                    # Typer CLI scripts
├── docs/
├── config.yaml                 # All configuration (GitOps-friendly)
├── pyproject.toml              # Deps, Ruff config, MyPy config
├── Dockerfile                  # Multi-stage, non-root, hardened
├── docker-compose.yml          # With all security measures
├── Makefile                    # run, test, lint, type-check, format, docker-*
├── .github/workflows/ci.yml   # Ruff + MyPy + pytest + coverage
└── README.md
```

## Decision Tree

```
What am I building?
│
├── New feature
│     └── Create: domain entity + repository ABC + service + router + schemas + TESTS
│
├── API endpoint
│     └── FastAPI router in api/ with Pydantic schemas + Depends() injection
│
├── Database access
│     └── ABC in domain/, SQLAlchemy implementation in infrastructure/
│
├── Business logic
│     └── Service in application/, depends only on ABCs
│
├── CLI script
│     └── Typer command in scripts/
│
├── Configuration
│     └── config.yaml + Pydantic Settings model in config.py
│
├── Shared utility
│     └── Contextual name (never utils.py), place in owning module
│
└── Tests
      └── Unit: fake repos → Integration: testcontainers → API: TestClient
```

## Examples

Condensed patterns from a recipes API. Show the shape — extrapolate for your domain.

### Domain Entity + Repository ABC

```python
# domain/recipe.py
from datetime import datetime
from typing import Literal
from pydantic import BaseModel

RecipeStatus = Literal["draft", "published", "archived"]

class Recipe(BaseModel):
    id: str
    title: str
    description: str
    ingredients: list[str]
    cooking_time_minutes: int
    status: RecipeStatus
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

# domain/recipe_repository.py
from abc import ABC, abstractmethod

class RecipeRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[Recipe]: ...

    @abstractmethod
    async def get_by_id(self, recipe_id: str) -> Recipe | None: ...

    @abstractmethod
    async def save(self, recipe: Recipe) -> Recipe: ...

    @abstractmethod
    async def delete(self, recipe_id: str) -> None: ...
```

### Service with Result Pattern

```python
# application/recipe_service.py — framework-agnostic, depends only on ABCs
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T"); E = TypeVar("E")

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    ok: bool = True

@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    ok: bool = False

Result = Ok[T] | Err[E]

class RecipeService:
    def __init__(self, repository: RecipeRepository) -> None:
        self._repo = repository

    async def get_recipe(self, recipe_id: str) -> Result[Recipe, RecipeNotFoundError]:
        recipe = await self._repo.get_by_id(recipe_id)
        if recipe is None:
            return Err(RecipeNotFoundError(recipe_id=recipe_id))
        return Ok(recipe)

    async def create_recipe(self, data: CreateRecipeInput) -> Result[Recipe, RecipeValidationError]:
        errors = _validate(data)
        if errors:
            return Err(RecipeValidationError(fields=errors))
        recipe = Recipe(...)  # build from data
        return Ok(await self._repo.save(recipe))

    async def delete_recipe(self, recipe_id: str) -> Result[None, RecipeNotFoundError]:
        if await self._repo.get_by_id(recipe_id) is None:
            return Err(RecipeNotFoundError(recipe_id=recipe_id))
        await self._repo.delete(recipe_id)
        return Ok(None)
```

### FastAPI Router with Depends

```python
# api/recipe_router.py
from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter(prefix="/api/v1/recipes", tags=["Recipes"])

async def get_recipe_service() -> RecipeService:
    raise NotImplementedError("Wire in app lifespan")

@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: RecipeService = Depends(get_recipe_service),
) -> list[RecipeResponse]:
    recipes = await service.list_recipes()
    return [RecipeResponse.model_validate(r.model_dump()) for r in recipes[offset:offset+limit]]

@router.post("/", response_model=RecipeResponse, status_code=201)
async def create_recipe(
    body: CreateRecipeRequest,
    service: RecipeService = Depends(get_recipe_service),
) -> RecipeResponse:
    result = await service.create_recipe(CreateRecipeInput(**body.model_dump()))
    if not result.ok:
        raise HTTPException(status_code=422, detail="Validation failed")
    return RecipeResponse.model_validate(result.value.model_dump())
```

### Unit Test with Fake Repository

```python
# tests/unit/test_recipe_service.py
import pytest
from datetime import datetime, timezone

class FakeRecipeRepository(RecipeRepository):
    """In-memory list — same ABC as the real SQLAlchemy repo."""
    def __init__(self, recipes: list[Recipe] | None = None) -> None:
        self._recipes = recipes or []
        self._next_id = 1

    async def list_all(self) -> list[Recipe]:
        return list(self._recipes)
    async def get_by_id(self, recipe_id: str) -> Recipe | None:
        return next((r for r in self._recipes if r.id == recipe_id), None)
    async def save(self, recipe: Recipe) -> Recipe:
        saved = recipe.model_copy(update={"id": str(self._next_id)})
        self._next_id += 1
        self._recipes.append(saved)
        return saved
    async def delete(self, recipe_id: str) -> None:
        self._recipes = [r for r in self._recipes if r.id != recipe_id]

@pytest.mark.asyncio
class TestRecipeService:
    async def test_get_recipe_found(self) -> None:
        service = RecipeService(FakeRecipeRepository([_make_recipe()]))
        result = await service.get_recipe("1")
        assert isinstance(result, Ok)
        assert result.value.title == "Pancakes"

    async def test_get_recipe_not_found(self) -> None:
        service = RecipeService(FakeRecipeRepository())
        result = await service.get_recipe("999")
        assert isinstance(result, Err)

    async def test_create_recipe_valid(self) -> None:
        service = RecipeService(FakeRecipeRepository())
        result = await service.create_recipe(
            CreateRecipeInput(title="Pasta", description="Simple", ingredients=["pasta"], cooking_time_minutes=15, author_name="Bob")
        )
        assert isinstance(result, Ok)
        assert result.value.status == "draft"

    async def test_create_recipe_empty_title_fails(self) -> None:
        service = RecipeService(FakeRecipeRepository())
        result = await service.create_recipe(
            CreateRecipeInput(title="", description="", ingredients=["x"], cooking_time_minutes=10, author_name="Bob")
        )
        assert isinstance(result, Err)
        assert "title" in result.error.fields
```
