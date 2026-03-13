---
name: sqlmodel
description: SQLModel - Pydantic + SQLAlchemy combined. This skill should be used when building FastAPI apps with database, creating ORM models, data validation with database persistence, or any Python project needing both validation and ORM. Triggers on "create database model", "add SQLModel", "database with FastAPI", "ORM model", or any SQLModel-related development.
---

# SQLModel - Pydantic + SQLAlchemy in One

One model for both **validation** AND **database**. Created by Sebastián Ramírez (FastAPI creator).

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, database setup, relationship patterns |
| **Conversation** | Entity requirements, relationships needed, validation rules |
| **Skill References** | Patterns from `references/` directory |
| **User Guidelines** | Naming conventions, project structure preferences |

## Clarifications

### Required (ask if not clear)
1. **Database?** PostgreSQL / SQLite / MySQL
2. **Async needed?** Yes (asyncpg/aiosqlite) / No (sync)
3. **Relationships?** One-to-Many / Many-to-Many / None

### Optional (ask if relevant)
4. **Migrations?** Alembic / Manual / None
5. **Framework?** FastAPI / Standalone Python

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| SQLModel Docs | https://sqlmodel.tiangolo.com | Official reference |
| SQLAlchemy Docs | https://docs.sqlalchemy.org | Advanced ORM features |
| Pydantic Docs | https://docs.pydantic.dev | Validation patterns |
| Alembic Docs | https://alembic.sqlalchemy.org | Database migrations |

> **Version Note**: This skill follows SQLModel 0.0.16+ and Pydantic v2 patterns.

## TDD Workflow (Red-Green-Refactor)

**ALWAYS follow TDD when building with SQLModel:**

### The Cycle
```
🔴 RED    → Write a failing test for model/endpoint
🟢 GREEN  → Create minimal model/code to pass
🔄 REFACTOR → Improve code, keep tests green
```

### TDD Example: Hero Model
```python
# Step 1: 🔴 RED - Write test first
def test_create_hero(client):
    response = client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Spider-Boy"

# Step 2: 🟢 GREEN - Create model and endpoint
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str

# Step 3: 🔄 REFACTOR - Add indexes, relationships
```

## Quick Start

```bash
# Initialize project
uv init my-app && cd my-app

# Install SQLModel
uv add sqlmodel

# For FastAPI integration
uv add sqlmodel fastapi "uvicorn[standard]"

# For async support
uv add sqlmodel aiosqlite  # SQLite async
uv add sqlmodel asyncpg    # PostgreSQL async
```

## Core Concept: One Model, Multiple Uses

```python
from sqlmodel import Field, SQLModel

# Base model (shared fields)
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

# Database model (table=True)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Create schema (request body)
class HeroCreate(HeroBase):
    pass

# Read schema (response)
class HeroRead(HeroBase):
    id: int

# Update schema (partial updates)
class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
```

## Basic CRUD Operations

```python
from sqlmodel import Session, select, create_engine

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

# CREATE
def create_hero(session: Session, hero: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# READ (single)
def get_hero(session: Session, hero_id: int) -> Hero | None:
    return session.get(Hero, hero_id)

# READ (list)
def get_heroes(session: Session, skip: int = 0, limit: int = 100) -> list[Hero]:
    statement = select(Hero).offset(skip).limit(limit)
    return session.exec(statement).all()

# UPDATE
def update_hero(session: Session, hero_id: int, hero_update: HeroUpdate) -> Hero | None:
    db_hero = session.get(Hero, hero_id)
    if db_hero:
        hero_data = hero_update.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
    return db_hero

# DELETE
def delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if hero:
        session.delete(hero)
        session.commit()
        return True
    return False
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel, create_engine

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/heroes/", response_model=HeroRead, status_code=201)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

## Workflow Selection

**Starting with SQLModel?** → See [references/basics.md](references/basics.md)

**Building FastAPI + SQLModel?** → See [references/fastapi-integration.md](references/fastapi-integration.md)

**Need relationships (1:N, N:N)?** → See [references/relationships.md](references/relationships.md)

**Database migrations?** → See [references/migrations.md](references/migrations.md)

**Async database?** → See [references/async.md](references/async.md)

## Field Configuration

```python
from sqlmodel import Field

class Hero(SQLModel, table=True):
    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Required with index
    name: str = Field(index=True)

    # Optional with default
    age: int | None = Field(default=None, index=True)

    # Unique constraint
    email: str = Field(unique=True)

    # Foreign key
    team_id: int | None = Field(default=None, foreign_key="team.id")

    # With validation
    power_level: int = Field(ge=0, le=100)

    # Max length (for VARCHAR)
    description: str | None = Field(default=None, max_length=500)
```

## Query Examples

```python
from sqlmodel import select, or_, and_, col

# Basic select
statement = select(Hero)
heroes = session.exec(statement).all()

# Where clause
statement = select(Hero).where(Hero.name == "Spider-Boy")
hero = session.exec(statement).first()

# Multiple conditions (AND)
statement = select(Hero).where(Hero.age >= 18, Hero.age <= 65)

# OR conditions
statement = select(Hero).where(or_(Hero.name == "Spider-Boy", Hero.name == "Deadpond"))

# LIKE query
statement = select(Hero).where(col(Hero.name).contains("Spider"))

# Order by
statement = select(Hero).order_by(Hero.name)
statement = select(Hero).order_by(col(Hero.age).desc())

# Limit and offset
statement = select(Hero).offset(10).limit(5)

# Count
from sqlmodel import func
statement = select(func.count()).select_from(Hero)
count = session.exec(statement).one()
```

## Testing with SQLModel

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",  # In-memory database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

```python
# tests/test_heroes.py
def test_create_hero(client):
    response = client.post("/heroes/", json={
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Spider-Boy"
    assert "id" in data

def test_read_hero(client):
    # Create first
    response = client.post("/heroes/", json={
        "name": "Deadpond",
        "secret_name": "Dive Wilson"
    })
    hero_id = response.json()["id"]

    # Then read
    response = client.get(f"/heroes/{hero_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Deadpond"

def test_read_hero_not_found(client):
    response = client.get("/heroes/999")
    assert response.status_code == 404
```

## Run Tests

```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=app --cov-report=term-missing
```

## Quick Reference

| Need | Solution |
|------|----------|
| Install | `uv add sqlmodel` |
| Create table | `class Hero(SQLModel, table=True)` |
| Primary key | `Field(default=None, primary_key=True)` |
| Foreign key | `Field(foreign_key="table.id")` |
| Index | `Field(index=True)` |
| Unique | `Field(unique=True)` |
| Create tables | `SQLModel.metadata.create_all(engine)` |
| Session | `with Session(engine) as session:` |
| Select all | `session.exec(select(Model)).all()` |
| Get by ID | `session.get(Model, id)` |
| Add | `session.add(obj); session.commit()` |
| Delete | `session.delete(obj); session.commit()` |
| Refresh | `session.refresh(obj)` |

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Missing `table=True` | Model won't create DB table | Add `table=True` to DB models |
| `id: int` without `None` | Can't create new records | Use `id: int \| None = Field(default=None, ...)` |
| Forgetting `session.commit()` | Changes not persisted | Always commit after add/update/delete |
| Not using `model_validate()` | Type conversion issues | Use `Hero.model_validate(hero_create)` |
| Missing `session.refresh()` | Stale data after commit | Refresh to get DB-generated values |
| Circular relationship imports | ImportError | Use `TYPE_CHECKING` and string annotations |

## Before Delivery Checklist

### Model Quality
- [ ] All DB models have `table=True`
- [ ] Primary keys use `Field(default=None, primary_key=True)`
- [ ] Separate schemas: Base, Create, Read, Update
- [ ] Indexes on frequently queried fields

### Database Operations
- [ ] All operations use `session.commit()`
- [ ] New objects refreshed after commit
- [ ] Proper error handling for not found
- [ ] Session dependency yields and closes

### Relationships
- [ ] Foreign keys properly defined
- [ ] `Relationship()` configured both sides
- [ ] Eager loading where needed (`selectinload`)

### Testing
- [ ] In-memory SQLite for tests
- [ ] Dependency override for test session
- [ ] Tests pass: `uv run pytest`
