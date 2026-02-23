---
name: fastapi-coder
description: Build FastAPI applications with async patterns, Pydantic validation, dependency injection, and modern Python API practices.
allowed-tools: Read Write Edit Grep Glob Bash WebSearch
---

# FastAPI Coder

## Core Principles

| Principle | Application |
|-----------|-------------|
| **Async-First** | Use async/await everywhere, sync only when required |
| **Type Safety** | Pydantic models for all request/response data |
| **Dependency Injection** | Use `Depends()` for shared logic, not global state |
| **OpenAPI-Driven** | Schema generates automatically; keep it clean |
| **Separation of Concerns** | Routes → Services → Repositories |

## Project Structure

```
app/
├── main.py              # FastAPI app initialization
├── api/
│   ├── __init__.py
│   ├── deps.py          # Shared dependencies
│   └── routes/          # Route handlers by domain
│       ├── users.py
│       └── items.py
├── core/
│   ├── config.py        # Settings via pydantic-settings
│   ├── security.py      # Auth utilities
│   └── exceptions.py    # Custom exceptions
├── models/              # Pydantic schemas
│   ├── user.py
│   └── item.py
├── services/            # Business logic
│   └── user_service.py
├── repositories/        # Data access
│   └── user_repo.py
└── tests/
    ├── conftest.py      # Shared fixtures
    └── test_users.py
```

## Essential Patterns

### Route Handler

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.api.deps import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user."""
    return await service.create(user_in)
```

### Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Dependencies

```python
from typing import Annotated
from fastapi import Depends, Header, HTTPException
from app.core.security import verify_token

async def get_current_user(
    authorization: Annotated[str, Header()],
) -> User:
    token = authorization.removeprefix("Bearer ")
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
```

### Service Layer

```python
from app.repositories.user_repo import UserRepository
from app.models.user import UserCreate, UserResponse

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create(self, user_in: UserCreate) -> UserResponse:
        # Business logic here
        existing = await self.repo.get_by_email(user_in.email)
        if existing:
            raise ValueError("Email already registered")
        return await self.repo.create(user_in)
```

### Exception Handling

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

### Background Tasks

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str):
    # Async email sending
    ...

@router.post("/users/")
async def create_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
):
    user = await create_user_in_db(user_in)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
```

## Database Integration

### SQLAlchemy 2.0 Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://...", echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
```

### Repository Pattern

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

## Authentication Patterns

### JWT Authentication

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm="HS256")

async def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
```

## Testing Patterns

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users/", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepass123",
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Quality Checklist

- [ ] All routes have response_model and status_code
- [ ] Pydantic models for all request/response data
- [ ] Dependencies for shared logic (auth, db, services)
- [ ] Service layer separates business logic from routes
- [ ] Repository pattern for data access
- [ ] Custom exceptions with proper handlers
- [ ] Async database operations
- [ ] Background tasks for non-blocking operations
- [ ] Comprehensive tests with httpx AsyncClient
- [ ] Type hints throughout
