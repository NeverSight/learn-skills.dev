---
name: python-backend
description: >
  Complete FastAPI production system. PROACTIVELY activate for: (1) Project structure
  (scalable layout), (2) Pydantic schemas (input/output separation), (3) Dependency injection,
  (4) Async database with SQLAlchemy, (5) JWT authentication, (6) Error handling patterns,
  (7) Docker deployment, (8) Gunicorn + Uvicorn production, (9) Rate limiting, (10) Testing with httpx.
  Provides: Project templates, schema patterns, auth setup, Docker config.
  Ensures production-ready FastAPI applications.
auto_load:
  enabled: true
  triggers:
    keywords: [fastapi, sqlalchemy, django, flask, api, rest, endpoint, orm, database]
    file_patterns: ["**/models/**/*.py", "**/schemas/**/*.py", "**/services/**/*.py"]
  priority: high
  load_with: [python-fundamentals]
---

# Python Backend

Expert-level Python backend patterns for FastAPI, Django, Flask, and SQLAlchemy. Use this skill for building REST APIs, database patterns, dependency injection, and backend architecture.

## When to Use This Skill

- Building REST APIs with FastAPI or Django
- Working with SQLAlchemy or Django ORM
- Implementing dependency injection
- Designing API endpoints and versioning
- Handling authentication and authorization
- Database optimization patterns

---

## FastAPI Patterns

### Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    model_config = {'str_strip_whitespace': True}
```

### Dependency Injection

```python
from typing import Annotated
from fastapi import Depends, HTTPException

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    user = await verify_token(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[AsyncSession, Depends(get_db)]

@app.get("/me")
async def get_me(user: CurrentUser, db: DB):
    return user
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@app.post("/users/")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    db_user = await crud.create_user(db, user)
    background_tasks.add_task(send_welcome_email, user.email)
    return db_user
```

### Exception Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message}
    )
```

### Lifespan Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
```

---

## SQLAlchemy 2.0 Patterns

### Modern Declarative Syntax

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")
```

### Async Queries

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
```

### Eager Loading

```python
from sqlalchemy.orm import selectinload, joinedload

# Prevent N+1 queries
stmt = select(User).options(
    selectinload(User.posts),  # Separate query
    joinedload(User.profile)   # JOIN
)
```

### Pagination

```python
from sqlalchemy import func, select

async def get_users_paginated(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20
) -> tuple[list[User], int]:
    # Count total
    count_stmt = select(func.count()).select_from(User)
    total = await db.scalar(count_stmt)

    # Get page
    stmt = select(User).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users, total
```

---

## Django Patterns

### Prevent N+1 Queries

```python
# BAD - N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # 1 query per user!

# GOOD - select_related for FK
users = User.objects.select_related('profile').all()

# GOOD - prefetch_related for M2M/reverse FK
posts = Post.objects.prefetch_related('tags', 'comments').all()
```

### Atomic Updates

```python
from django.db.models import F

# BAD - Race condition
article = Article.objects.get(pk=1)
article.views += 1
article.save()

# GOOD - Atomic update
Article.objects.filter(pk=1).update(views=F('views') + 1)
```

### Complex Queries

```python
from django.db.models import Q

# OR query
users = User.objects.filter(
    Q(is_staff=True) | Q(is_superuser=True)
)

# Combined conditions
users = User.objects.filter(
    Q(email__endswith='@company.com') &
    (Q(is_active=True) | Q(is_staff=True))
)
```

### Efficient Checks

```python
# BAD - Loads all objects
if len(User.objects.filter(email=email)) > 0:
    ...

# GOOD - Efficient existence check
if User.objects.filter(email=email).exists():
    ...
```

### Bulk Operations

```python
# BAD - N queries
for user_data in users_data:
    User.objects.create(**user_data)

# GOOD - 1 query
User.objects.bulk_create([
    User(**data) for data in users_data
])
```

### Transactions

```python
from django.db import transaction

@transaction.atomic
def transfer_funds(from_account, to_account, amount):
    from_account.balance = F('balance') - amount
    from_account.save()
    to_account.balance = F('balance') + amount
    to_account.save()
```

---

## API Design

### RESTful Conventions

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET | /users | List all | 200 + array |
| GET | /users/:id | Get one | 200 / 404 |
| POST | /users | Create | 201 + created |
| PUT | /users/:id | Replace | 200 / 404 |
| PATCH | /users/:id | Update | 200 / 404 |
| DELETE | /users/:id | Delete | 204 / 404 |

### Nested Resources

```
GET    /users/:userId/orders          # User's orders
POST   /users/:userId/orders          # Create order for user
GET    /users/:userId/orders/:orderId # Specific order
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Resources | Plural nouns | `/users`, `/orders` |
| Actions | Verbs (rare) | `/auth/login`, `/reports/generate` |
| Query params | snake_case | `?page_size=20` |
| Request/Response | camelCase | `{ "firstName": "John" }` |

### Versioning Strategies

| Strategy | Example | When to Use |
|----------|---------|-------------|
| URL Path | `/v1/users` | Most common, clear |
| Header | `Accept: application/vnd.api+json;version=1` | Clean URLs |
| Query | `/users?version=1` | Simple but messy |

**Recommended:** URL path (`/api/v1/...`)

### Response Format

#### Success
```json
{
  "data": { "id": "123", "name": "John" },
  "meta": { "timestamp": "2025-01-01T00:00:00Z" }
}
```

#### List with Pagination
```json
{
  "data": [{ "id": "1" }, { "id": "2" }],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

#### Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "fields": { "email": "Invalid format" }
  }
}
```

### Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource missing |
| 409 | Conflict | Duplicate/state conflict |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many | Rate limited |
| 500 | Server Error | Unexpected error |

### Pagination Patterns

#### Offset-based (Simple)
```
GET /users?page=2&page_size=20
```

#### Cursor-based (Scalable)
```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

| Pattern | Pros | Cons |
|---------|------|------|
| Offset | Simple, jump to page | Slow on large datasets |
| Cursor | Consistent, fast | No page jumping |

### Filtering & Sorting

```
# Filter
GET /users?status=active&role=admin

# Sort
GET /users?sort=created_at:desc,name:asc

# Search
GET /users?q=john

# Combined
GET /users?status=active&sort=name:asc&page=1&page_size=20
```

### API Documentation (OpenAPI)

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

---

## Result Pattern (No Exceptions in Core)

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]

async def get_user(user_id: int) -> Result[User, str]:
    user = await db.get(User, user_id)
    if user is None:
        return Err("User not found")
    return Ok(user)

# Usage
match await get_user(123):
    case Ok(user):
        print(f"Found: {user.name}")
    case Err(error):
        print(f"Error: {error}")
```

---

## Best Practices

### Do's
- Use plural nouns for resources
- Return created/updated resource
- Include pagination metadata
- Document with OpenAPI
- Version from day one
- Use Pydantic for validation
- Prefer async for I/O operations

### Don'ts
- Use verbs in resource names
- Return different formats per endpoint
- Expose internal IDs/structures
- Ignore backward compatibility
- Skip error code standards
- Use bare except clauses

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Django Documentation](https://docs.djangoproject.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
