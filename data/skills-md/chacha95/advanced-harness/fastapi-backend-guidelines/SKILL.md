---
name: fastapi-backend-guidelines
description: FastAPI backend development guidelines for Python async applications. Domain-Driven Design with FastAPI routers, SQLModel/SQLAlchemy ORM, repository pattern, service layer, async/await patterns, Pydantic validation, and error handling. Use when creating APIs, routes, services, repositories, or working with backend code.
---

# FastAPI Backend Development Guidelines

## Purpose

Comprehensive guide for modern FastAPI development with async Python, emphasizing Domain-Driven Design, layered architecture (Router → Service → Repository), SQLModel ORM, and async best practices.

## When to Use This Skill

- Creating new API routes or endpoints
- Building domain services and business logic
- Implementing repositories for data access
- Setting up database models with SQLModel
- Async/await patterns and error handling
- Organizing backend code with DDD
- Pydantic validation and DTOs
- Python async best practices

---

## Quick Start

### New API Route Checklist

Creating an API endpoint? Follow this checklist:

- [ ] Define route in `backend/api/v1/routers/{domain}.py`
- [ ] Use FastAPI dependency injection for session
- [ ] Use `get_read_session_dependency` for reads, `get_write_session_dependency` for writes
- [ ] Call service layer (don't access repository directly)
- [ ] Use Pydantic DTOs for request/response
- [ ] Handle errors with custom exceptions
- [ ] Add proper HTTP status codes
- [ ] Use async/await throughout
- [ ] Document with docstrings
- [ ] Use type hints on all parameters

### New Domain Feature Checklist

Creating a new domain? Set up this structure:

- [ ] Create `backend/domain/{domain}/` directory
- [ ] Create `model.py` - SQLModel database models with ULID ID generation
- [ ] Create `repository.py` - Data access layer extending BaseRepository
- [ ] Create `service.py` - Business logic layer
- [ ] Create DTOs in `backend/dtos/{domain}.py`
- [ ] Create router in `backend/api/v1/routers/{domain}.py`
- [ ] Register router in `main.py`
- [ ] Follow async patterns throughout
- [ ] Add enums to `backend/domain/user/enums.py` if needed

---

## Project Structure Quick Reference

Your YGS backend structure:

```
backend/
  backend/
    main.py                  # FastAPI app creation with lifespan

    api/
      v1/
        routers/             # API route handlers
          admin.py           # Dashboard, members, matching
          auth.py            # Login, signup, OAuth
          match.py           # Match weeks, history
          user.py            # User management
          upload.py          # S3 presigned URLs

    domain/                  # Domain-Driven Design
      user/
        model.py             # User, UserProfile, UserLifestyle, etc.
        repository.py        # UserRepository, UserDataLoader
        service.py           # UserService
        enums.py             # All domain enums
      auth/
        service.py           # AuthService (JWT, Firebase, Kakao)
        repository.py        # AuthRepository
      admin/
        model.py             # ConsultSchedule
        service.py           # AdminService
        repository.py        # AdminRepository
        matching_service.py  # MatchingService (scoring algorithm)
      match/
        model.py             # MatchWeek, MatchHistory, MatchFeedback
        service.py           # MatchService
        repository.py        # MatchRepository
      llm/
        matching_service.py  # LLM-enhanced matching
      shared/
        base_repository.py   # Generic BaseRepository

    dtos/                    # Pydantic DTOs
      admin.py               # Dashboard, member DTOs
      auth.py                # Login, signup, OAuth DTOs
      match.py               # Match week, history DTOs
      user.py                # User, profile DTOs
      llm_match.py           # LLM matching DTOs

    db/
      orm.py                 # Read/Write session management

    core/
      config.py              # Pydantic Settings configuration

    middleware/              # Middleware
      error_handler.py       # ErrorHandlerMiddleware
      admin_auth.py          # Admin authentication

    utils/                   # Utilities
      s3.py                  # S3 presigned URLs
      s3_private.py          # Private user data S3
      firebase.py            # Firebase verification
      password.py            # bcrypt hashing
      excel.py               # Excel export

    error/                   # Custom exceptions
      __init__.py            # AppException, NotFoundError, etc.
```

---

## Common Imports Cheatsheet

```python
# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

# SQLModel & SQLAlchemy
from sqlmodel import select, or_, and_, col
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func, desc
from sqlalchemy.orm import selectinload

# Database
from backend.db.orm import get_write_session_dependency, get_read_session_dependency

# Pydantic
from pydantic import BaseModel, Field, field_validator, EmailStr

# Your domain
from backend.domain.user.model import User, UserProfile
from backend.domain.user.service import UserService
from backend.dtos.user import UserResponse, UserCreateRequest
from backend.error import NotFoundError, ForbiddenError, UnauthorizedError

# Type hints
from typing import List, Optional, Dict, Any

# ID generation
from ulid import ULID
```

---

## Topic Guides

### 🏗️ Layered Architecture

**Three-Layer Pattern:**
1. **Router Layer**: API endpoints, request validation, response formatting
2. **Service Layer**: Business logic, orchestration, domain rules
3. **Repository Layer**: Data access, queries, database operations

**Key Concepts:**
- Routers call Services (never Repositories directly)
- Services orchestrate business logic
- Repositories handle all database operations
- Each layer has clear responsibilities
- Async/await throughout the stack
- Read/Write session separation

**[📖 Complete Guide: resources/layered-architecture.md](resources/layered-architecture.md)**

---

### 🛣️ API Routes & Routers

**PRIMARY PATTERN: FastAPI Routers**
- Create routers in `backend/api/v1/routers/`
- Use dependency injection for sessions
- Use `get_read_session_dependency` for GET requests
- Use `get_write_session_dependency` for POST/PATCH/DELETE
- Follow REST conventions
- Use appropriate HTTP methods and status codes
- Async route handlers

**Router Structure:**
```python
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.db.orm import get_read_session_dependency, get_write_session_dependency

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_read_session_dependency),
) -> UserResponse:
    service = UserService(session)
    return await service.get_user(user_id)

@router.post("", status_code=201)
async def create_user(
    request: UserCreateRequest,
    session: AsyncSession = Depends(get_write_session_dependency),
) -> UserResponse:
    service = UserService(session)
    return await service.create_user(request)
```

**[📖 Complete Guide: resources/api-routes.md](resources/api-routes.md)**

---

### 🗄️ Database & ORM

**SQLModel + SQLAlchemy:**
- SQLModel for models (combines SQLAlchemy + Pydantic)
- Async sessions with asyncpg driver
- Read/Write session separation with caching
- Repository pattern for all queries
- ULID-based ID generation with prefixes

**Model Pattern:**
```python
from sqlmodel import SQLModel, Field, Column, DateTime, Text
from datetime import datetime, timezone
from ulid import ULID

def generate_user_id() -> str:
    """Generate user ID with prefix."""
    return f"usr_{ULID()}"

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(
        default_factory=generate_user_id,
        primary_key=True,
        max_length=30,
    )
    phone: str = Field(sa_column=Column(Text, nullable=False, unique=True))
    name: str = Field(sa_column=Column(Text, nullable=False))
    gender: GenderEnum = Field(sa_column=Column(Text, nullable=False))

    # Soft delete pattern
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
        default=None,
    )

    # Timestamps
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
```

**[📖 Complete Guide: resources/database-orm.md](resources/database-orm.md)**

---

### 📦 Domain-Driven Design

**Domain Organization:**
- Each domain in `backend/domain/{name}/`
- Contains: `model.py`, `repository.py`, `service.py`
- Clear separation of concerns
- Business logic in services
- Data access in repositories

**Your Domains:**
- **user**: User management (User, UserProfile, UserLifestyle, UserPreference, etc.)
- **auth**: Authentication (JWT, Firebase, Kakao OAuth)
- **admin**: Admin dashboard, member management, consultations
- **match**: Match weeks, history, feedback
- **llm**: LLM-enhanced matching with Gemini
- **shared**: BaseRepository, common utilities

**[📖 Complete Guide: resources/domain-driven-design.md](resources/domain-driven-design.md)**

---

### 🔄 Service Layer

**Service Pattern:**
- Business logic orchestration
- Domain rule enforcement
- Calls repositories for data
- Returns DTOs, not models directly
- Transaction management
- Uses asyncio.gather for parallel queries

**Service Structure:**
```python
class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._user_repo = UserRepository(session)
        self._profile_repo = UserProfileRepository(session)
        self._data_loader = UserDataLoader(session)

    async def get_user_detail(self, user_id: str) -> UserDetailResponse:
        # Use UserDataLoader for N+1 prevention
        user_with_relations = await self._data_loader.load_user_with_relations(
            user_id,
            load_profile=True,
            load_photos=True,
        )
        if not user_with_relations:
            raise NotFoundError(f"User {user_id} not found")
        return self._to_detail_response(user_with_relations)
```

**[📖 Complete Guide: resources/service-layer.md](resources/service-layer.md)**

---

### 💾 Repository Pattern

**Repository Pattern:**
- Encapsulates data access
- Extends BaseRepository for CRUD
- Domain-specific queries
- Returns domain models
- All queries are async
- Soft delete support

**Repository Structure:**
```python
from backend.domain.shared.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def find_by_phone(self, phone: str) -> Optional[User]:
        stmt = select(User).where(
            User.phone == phone,
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

**UserDataLoader Pattern (N+1 Prevention):**
```python
@dataclass
class UserWithRelations:
    user: User
    profile: Optional[UserProfile] = None
    lifestyle: Optional[UserLifestyle] = None
    photos: List[UserPhoto] = field(default_factory=list)

class UserDataLoader:
    async def load_user_with_relations(
        self,
        user_id: str,
        load_profile: bool = False,
        load_photos: bool = False,
    ) -> Optional[UserWithRelations]:
        # Build queries based on flags
        queries = [self._load_user(user_id)]
        if load_profile:
            queries.append(self._load_profile(user_id))
        if load_photos:
            queries.append(self._load_photos(user_id))

        # Execute all queries in parallel
        results = await asyncio.gather(*queries)
        # ... combine results
```

**[📖 Complete Guide: resources/repository-pattern.md](resources/repository-pattern.md)**

---

### 📝 DTOs & Validation

**Pydantic DTOs:**
- Request/Response data transfer objects
- Validation with Pydantic
- Separate from domain models
- Located in `backend/dtos/`
- Use field_validator for enum validation

**DTO Pattern:**
```python
from pydantic import BaseModel, Field, field_validator
from backend.domain.user.enums import GenderEnum, UserStatusEnum

class AdminBasicInfoUpdateRequest(BaseModel):
    """Request DTO for updating basic user info (admin only)."""

    name: Optional[str] = Field(None, description="User name")
    status: Optional[str] = Field(None, description="User status")
    is_admin: Optional[bool] = Field(None, description="Admin flag")
    birth_year: Optional[int] = Field(None, ge=1940, le=2010, description="Birth year")

    model_config = {"extra": "forbid"}  # Reject unknown fields

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_values = [e.value for e in UserStatusEnum]
            if v not in valid_values:
                raise ValueError(f"Invalid status: {v}. Valid: {valid_values}")
        return v
```

**[📖 Complete Guide: resources/dtos-validation.md](resources/dtos-validation.md)**

---

### ⚡ Async/Await Patterns

**Async Best Practices:**
- Use async/await throughout
- Async database sessions
- Proper session cleanup
- Avoid blocking operations
- Use asyncio.gather for parallel queries

**Async Patterns:**
```python
# Parallel queries with asyncio.gather
async def get_dashboard_data(self) -> dict:
    # Run all queries in parallel
    total, monthly, weekly, today = await asyncio.gather(
        self._get_total_count(),
        self._get_monthly_count(),
        self._get_weekly_count(),
        self._get_today_count(),
    )
    return {
        "total_members": total,
        "monthly_members": monthly,
        "weekly_members": weekly,
        "today_members": today,
    }
```

**[📖 Complete Guide: resources/async-patterns.md](resources/async-patterns.md)**

---

### 🚨 Error Handling

**Error Handling Strategy:**
- Custom exception classes in `backend/error/`
- HTTP exception mapping via ErrorHandlerMiddleware
- Middleware for error handling
- Consistent error responses

**Error Pattern:**
```python
# backend/error/__init__.py
class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotFoundError(AppException):
    pass

class ForbiddenError(AppException):
    pass

class UnauthorizedError(AppException):
    pass

# In service
if not user:
    raise NotFoundError(f"User {user_id} not found")

# ErrorHandlerMiddleware handles conversion to HTTP response
# NotFoundError → 404, ForbiddenError → 403, etc.
```

**[📖 Complete Guide: resources/error-handling.md](resources/error-handling.md)**

---

### 📚 Complete Examples

**Full working examples:**
- Complete domain (model + repository + service + router)
- CRUD operations with async
- Complex queries with SQLModel
- Firebase/Kakao authentication patterns
- S3 presigned URL generation
- Pagination and filtering
- N+1 prevention with UserDataLoader

**[📖 Complete Guide: resources/complete-examples.md](resources/complete-examples.md)**

---

## Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Understand architecture | [layered-architecture.md](resources/layered-architecture.md) |
| Create API routes | [api-routes.md](resources/api-routes.md) |
| Work with database | [database-orm.md](resources/database-orm.md) |
| Organize domains | [domain-driven-design.md](resources/domain-driven-design.md) |
| Build services | [service-layer.md](resources/service-layer.md) |
| Create repositories | [repository-pattern.md](resources/repository-pattern.md) |
| Validate requests | [dtos-validation.md](resources/dtos-validation.md) |
| Use async patterns | [async-patterns.md](resources/async-patterns.md) |
| Handle errors | [error-handling.md](resources/error-handling.md) |
| See full examples | [complete-examples.md](resources/complete-examples.md) |

---

## Core Principles

1. **Layered Architecture**: Router → Service → Repository (never skip layers)
2. **Domain-Driven Design**: Organize by domain, not by type
3. **Async Everything**: Use async/await throughout the stack
4. **Repository Pattern**: All data access through repositories
5. **Service Layer**: Business logic in services, not routers or repositories
6. **DTOs for API**: Use Pydantic DTOs for request/response
7. **Type Hints**: Explicit types on all functions and parameters
8. **Error Handling**: Custom exceptions, middleware for HTTP mapping
9. **Read/Write Split**: Separate sessions for read and write operations
10. **Dependency Injection**: Use FastAPI's Depends() for sessions
11. **ULID IDs**: Use ULID with entity prefixes (usr_, mw_, mh_, etc.)
12. **Soft Delete**: Use deleted_at timestamp instead of hard deletes
13. **N+1 Prevention**: Use asyncio.gather and DataLoader patterns

---

## Quick Reference: New Domain Template

```python
# backend/domain/myfeature/model.py
from sqlmodel import SQLModel, Field, Column, DateTime, Text
from datetime import datetime, timezone
from typing import Optional
from ulid import ULID

def generate_myfeature_id() -> str:
    return f"mf_{ULID()}"

class MyFeature(SQLModel, table=True):
    __tablename__ = "my_feature"

    id: str = Field(
        default_factory=generate_myfeature_id,
        primary_key=True,
        max_length=30,
    )
    name: str = Field(sa_column=Column(Text, nullable=False))

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
        default=None,
    )

# backend/domain/myfeature/repository.py
from backend.domain.shared.base_repository import BaseRepository
from sqlmodel.ext.asyncio.session import AsyncSession

class MyFeatureRepository(BaseRepository[MyFeature]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MyFeature)

    async def find_by_name(self, name: str) -> Optional[MyFeature]:
        stmt = select(MyFeature).where(
            MyFeature.name == name,
            MyFeature.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

# backend/domain/myfeature/service.py
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.error import NotFoundError

class MyFeatureService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = MyFeatureRepository(session)

    async def get_feature(self, id: str) -> MyFeatureResponse:
        feature = await self._repository.get_by_id(id)
        if not feature:
            raise NotFoundError(f"Feature {id} not found")
        return MyFeatureResponse.model_validate(feature)

# backend/dtos/myfeature.py
from pydantic import BaseModel, Field
from datetime import datetime

class MyFeatureResponse(BaseModel):
    id: str
    name: str
    created_at: datetime

class MyFeatureCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

# backend/api/v1/routers/myfeature.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.db.orm import get_read_session_dependency, get_write_session_dependency

router = APIRouter(prefix="/myfeature", tags=["myfeature"])

@router.get("/{id}")
async def get_feature(
    id: str,
    session: AsyncSession = Depends(get_read_session_dependency),
) -> MyFeatureResponse:
    service = MyFeatureService(session)
    return await service.get_feature(id)

@router.post("", status_code=201)
async def create_feature(
    request: MyFeatureCreateRequest,
    session: AsyncSession = Depends(get_write_session_dependency),
) -> MyFeatureResponse:
    service = MyFeatureService(session)
    return await service.create_feature(request)
```

---

## Related Skills

- **nextjs-frontend-guidelines**: Frontend patterns that consume this API
- **error-tracking**: Error tracking with Sentry (backend integration)
- **pytest-backend-testing**: Testing patterns for FastAPI backends

---

**Skill Status**: Modular structure with progressive loading for optimal context management
