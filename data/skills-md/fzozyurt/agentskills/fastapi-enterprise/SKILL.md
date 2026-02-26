---
name: fastapi-enterprise
description: Expert guidance for building production-ready FastAPI applications with modular architecture where each business domain is an independent module with own routes, models, schemas, services, cache, and migrations. Uses UV + pyproject.toml for modern Python dependency management, project name subdirectory for clean workspace organization, structlog (JSON+colored logging), pydantic-settings configuration, auto-discovery module loader, async SQLAlchemy with PostgreSQL, per-module Alembic migrations, Redis/memory cache with module-specific namespaces, central httpx client, OpenTelemetry/Prometheus observability, conversation ID tracking (X-Conversation-ID header+cookie), conditional Keycloak/app-based RBAC authentication, DDD/clean code principles, and automation scripts for rapid module development. Use when user requests FastAPI project setup, modular architecture, independent module development, microservice architecture, async database operations, caching strategies, logging patterns, configuration management, authentication systems, observability implementation, or enterprise Python web services. Supports max 3-4 route nesting depth, cache invalidation patterns, inter-module communication via service layer, and comprehensive error handling workflows.
license: Complete terms in LICENSE.txt
---

# FastAPI Enterprise Development - Modular Architecture

Enterprise-grade FastAPI with **modular architecture**: each business domain is an independent module with own database tables, cache namespace, routes, and migrations. Modern Python tooling (UV + pyproject.toml) for fast dependency management.

## Quick Start

### Initialize Project

```bash
# Create modular FastAPI project with UV
python scripts/init_project.py --name my_api --auth keycloak --with-example-module

# Result:
# my_api/                    ← Project name subdirectory
# ├── src/
# │   ├── app.py             ← Main application
# │   ├── core/              ← Shared infrastructure (logging, DB, cache, module loader)
# │   ├── middleware/        ← Conversation tracking, auth
# │   └── routes/            ← Core routes (health, metrics)
# ├── modules/               ← Independent modules
# │   └── users/             ← Example: own routes, models, cache, migrations
# ├── pyproject.toml         ← UV configuration
# ├── config/                ← YAML configurations
# └── scripts/               ← Automation (create_module.py)

# Install and run
cd my_api
uv sync                      # Install dependencies (10-100x faster than pip)
cp .env.example .env
uv run uvicorn src.app:app --reload
```

### Create Independent Module

```bash
# Generate new module with complete structure
uv run python scripts/create_module.py --name orders

# Auto-creates:
# modules/orders/
# ├── __init__.py          ← Router export (auto-discovered)
# ├── routes/              ← /api/v1/orders endpoints
# ├── models/              ← SQLAlchemy models (own tables)
# ├── schemas/             ← Pydantic validation
# ├── services/            ← Business logic
# ├── cache/               ← Module-specific cache (orders:* prefix)
# ├── enums/               ← Module-specific enums
# └── alembic/             ← Module-specific migrations
```

### Minimal Modular App

```python
# src/app.py
from fastapi import FastAPI
from src.core.config import settings
from src.core.logging import configure_logging
from src.core.cache import cache_manager
from src.core.module_loader import discover_modules
from src.middleware.conversation_middleware import ConversationMiddleware

# Configure logging (JSON/colored)
configure_logging(environment=settings.ENVIRONMENT)

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(ConversationMiddleware)  # UUID tracking

@app.on_event("startup")
async def startup():
    await cache_manager.connect()  # Redis or memory
    discover_modules(app)           # Auto-register all modules

@app.get("/")
async def root():
    return {"message": "Welcome"}
```

## Core Capabilities

### 1. Modular Architecture ⭐
- **Independent Modules**: Each module owns DB tables, cache keys, routes
- **Auto-Discovery**: Modules in `modules/` automatically registered
- **Service-Layer Communication**: Inter-module calls via services (no direct model imports)
- **Per-Module Migrations**: Each module has own Alembic history
- **Enforced Boundaries**: `modules.users.services.UserService` ✅ | `from modules.users.models import User` ❌

[Module Patterns Guide](references/module-patterns.md)

### 2. Modern Python Tooling (UV + pyproject.toml) ⭐
- **UV**: 10-100x faster than pip, Rust-based package manager
- **pyproject.toml**: PEP 518/621 standard, replaces requirements.txt
- **uv.lock**: Reproducible builds across environments
- **Project Subdirectory**: All files in `my_api/` (clean workspace)
- **Export**: `uv export --format requirements-txt > requirements.txt` when needed

[Project Structure](references/project-structure.md)

### 3. Flexible Caching ⭐
- **Redis** (production): Distributed, persistent cache
- **Memory** (development): Zero dependencies, instant setup
- **Module Namespaces**: `users:123`, `orders:456` (no collisions)
- **Cache Decorators**: `@cached(prefix="products", ttl=1800)`
- **Invalidation**: Time-based (TTL), event-based (on update), pattern-based (`users:*`)

[Cache Patterns](references/cache-patterns.md)

### 4. Structured Logging (structlog)
- **JSON** (production): Structured logs for aggregation (ELK, Splunk)
- **Colored Console** (development): Human-readable with syntax highlighting
- **Conversation ID**: UUID in all logs from `ConversationMiddleware`
- **Request/Response**: Automatic logging with duration, status code
- **External APIs**: Conversation ID propagated to downstream services

[Logging Patterns](references/logging-patterns.md)

### 5. Type-Safe Configuration
- **pydantic-settings**: OS environment variables with type validation
- **YAML**: `config/development.yml` and `config/production.yml`
- **Variable Substitution**: `${DATABASE_PASSWORD}` from environment
- **CONFIG_ENV Switcher**: Toggle between dev/prod configs

[Configuration Patterns](references/configuration-patterns.md)

### 6. Async Database (SQLAlchemy 2.0)
- **Async**: Full asyncio support with `asyncpg` driver
- **PostgreSQL-Optimized**: JSONB, arrays, full-text search
- **Per-Module Tables**: Each module creates own tables
- **Central Session**: `src/core/db.py` session factory used by all modules and Alembic

[Database Patterns](references/database-patterns.md)

### 7. Per-Module Migrations (Alembic)
- **Independent Histories**: `modules/users/alembic/`, `modules/orders/alembic/`
- **Async Template**: Configured for async SQLAlchemy
- **Auto-Generation**: `alembic revision --autogenerate`
- **Run All**: `python scripts/run_migrations.py --all`

[Alembic Setup](references/alembic-setup.md)

### 8. Central HTTP Client (httpx)
- **Async**: Connection pooling, timeouts, retries
- **Conversation ID**: Auto-propagated to `X-Conversation-ID` header
- **YAML Configs**: Base URLs from `config/*.yml`
- **Request Logging**: All external API calls logged

[HTTPx Patterns](references/httpx-patterns.md)

### 9. Observability
- **Conversation Tracking**: UUID from header/cookie, appears in all logs
- **Prometheus Metrics**: `/metrics` endpoint (request count, latency, errors)
- **OpenTelemetry** (optional): Distributed tracing (Jaeger, Zipkin)
- **Health Check**: `/health` with DB connectivity status

[Observability Patterns](references/observability-patterns.md)

### 10. Authentication (Conditional)

**AI MUST ASK**: *"Keycloak authentication (JWT from external IdP) or app-based RBAC (database-backed roles)?"*

- **Keycloak**: JWT validation, role extraction, Keycloak OpenID integration
- **App-based**: Custom JWT, database roles/permissions, user management
- **Middleware**: Token validation, `request.state.current_user` injection
- **Role Decorators**: `@requires_role("admin")`

[Authentication Patterns](references/authentication-patterns.md)

## Automation Scripts

### init_project.py
Initialize complete project with modular structure:
```bash
python scripts/init_project.py --name my_api --auth keycloak --with-example-module
```

### create_module.py
Generate new independent module:
```bash
uv run python scripts/create_module.py --name products
```

### create_endpoint.py
Add endpoint to existing module:
```bash
uv run python scripts/create_endpoint.py --module users --service auth --method post --path login
```

### create_model.py
Create SQLAlchemy model + Alembic migration:
```bash
uv run python scripts/create_model.py --module products --name Product
```

### validate_structure.py
Check project compliance:
```bash
uv run python scripts/validate_structure.py
```

## Module Independence Rules

### ✅ DO:
- **Service Layer Communication**: `from modules.users.services.user_service import UserService`
- **Module Namespaces**: `users:cache:123`, `orders:cache:456`
- **Own Tables**: Each module creates own database tables
- **Own Migrations**: Separate Alembic history per module

### ❌ DON'T:
- **Direct Model Imports**: `from modules.users.models.user import User` (use service instead)
- **Shared Tables**: No `ForeignKey("users.id")` across modules (store as regular int)
- **Cross-Module Cache**: Don't access other module's cache directly

[Clean Code Standards](references/clean-code-standards.md)

## Resources

### Reference Documentation
- [Project Structure](references/project-structure.md) - Directory layout, UV setup
- [Module Patterns](references/module-patterns.md) - Independent module development
- [Cache Patterns](references/cache-patterns.md) - Redis/memory caching strategies
- [Routing Patterns](references/routing-patterns.md) - Auto-discovery, module loader
- [Logging Patterns](references/logging-patterns.md) - Structlog configuration
- [Configuration Patterns](references/configuration-patterns.md) - pydantic-settings, YAML
- [Database Patterns](references/database-patterns.md) - Async SQLAlchemy, CRUD
- [Alembic Setup](references/alembic-setup.md) - Per-module migrations
- [HTTPx Patterns](references/httpx-patterns.md) - Central HTTP client
- [Observability Patterns](references/observability-patterns.md) - Conversation tracking, metrics
- [Authentication Patterns](references/authentication-patterns.md) - Keycloak vs app-based
- [Clean Code Standards](references/clean-code-standards.md) - DDD, no duplication
- [Error Handling Workflow](references/error-handling-workflow.md) - Systematic debugging

### Automation Scripts
- `scripts/init_project.py` - Initialize complete project
- `scripts/create_module.py` - Generate new module
- `scripts/create_endpoint.py` - Add endpoint to module
- `scripts/create_model.py` - Create model + migration
- `scripts/validate_structure.py` - Check project compliance

### Examples
- [Complete Usage Examples](references/EXAMPLES.md) - 6 full examples (module creation, cache usage, auth, metrics, etc.)

## License

MIT License - See [LICENSE.txt](LICENSE.txt) for complete terms.
