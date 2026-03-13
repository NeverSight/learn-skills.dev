---
name: fastapi-clean-architecture
description: Build FastAPI applications using Clean Architecture principles with proper layer separation (Domain, Infrastructure, API), dependency injection, repository pattern, and comprehensive testing. Use this skill when designing or implementing Python backend services that require maintainability, testability, and scalability.
---

# FastAPI Clean Architecture Skill

## Overview

This skill guides you in building FastAPI applications following Clean Architecture principles, based on production patterns from enterprise financial systems. It emphasizes proper layer separation, dependency injection, repository patterns, and comprehensive testing strategies.

## When to Use This Skill

- Starting a new FastAPI project requiring clean architecture
- Refactoring existing FastAPI code for better maintainability
- Implementing domain-driven design with FastAPI
- Building testable, scalable backend services
- Integrating multiple data sources (PostgreSQL, Redis, external APIs)

## Core Architecture Principles

### Three-Layer Architecture

```
src/
├── api/              # API Layer (Controllers, Routes, DTOs)
├── domain/           # Domain Layer (Business Logic, Entities, Services)
└── infra/            # Infrastructure Layer (Database, External Services)
```

**Layer Responsibilities:**

1. **API Layer** (`src/api/`)
   - HTTP endpoints and routing
   - Request/Response DTOs (Pydantic models)
   - Input validation
   - Authentication/Authorization middleware
   - Error handling and HTTP status codes

2. **Domain Layer** (`src/domain/`)
   - Business entities and value objects
   - Service interfaces (abstract classes)
   - Business rules and validation
   - Domain exceptions
   - Pure business logic (framework-agnostic)

3. **Infrastructure Layer** (`src/infra/`)
   - Database repositories (SQLAlchemy)
   - External API adapters
   - Cache implementations (Redis)
   - File storage adapters
   - Concrete service implementations

### Dependency Flow

```
API Layer → Domain Layer ← Infrastructure Layer
```

**Critical Rules:**
- API depends on Domain (imports domain services/entities)
- Infrastructure implements Domain interfaces
- Domain NEVER imports from API or Infrastructure
- Use dependency injection to wire everything together

## Project Structure Template

```
project-name/
├── src/
│   ├── api/
│   │   ├── path/              # Route modules
│   │   │   ├── users.py
│   │   │   ├── auth.py
│   │   │   └── financial.py
│   │   ├── middlewares/       # Custom middleware
│   │   │   ├── auth.py
│   │   │   └── error_handler.py
│   │   └── schemas/           # Request/Response DTOs
│   │       ├── user.py
│   │       └── financial.py
│   ├── domain/
│   │   ├── modules/           # Business modules
│   │   │   ├── user/
│   │   │   │   ├── entity.py       # User entity
│   │   │   │   ├── service.py      # IUserService (abstract)
│   │   │   │   ├── repository.py   # IUserRepository (abstract)
│   │   │   │   └── exceptions.py   # Domain exceptions
│   │   │   └── financial/
│   │   │       ├── entity.py
│   │   │       ├── service.py
│   │   │       └── value_objects.py
│   │   └── shared/            # Shared domain logic
│   │       ├── base_entity.py
│   │       └── exceptions.py
│   ├── infra/
│   │   ├── database/
│   │   │   ├── alchemist/     # SQLAlchemy implementations
│   │   │   │   ├── modules/
│   │   │   │   │   ├── user/
│   │   │   │   │   │   └── repository.py  # UserRepository
│   │   │   │   │   └── financial/
│   │   │   │   │       └── repository.py
│   │   │   │   └── session.py
│   │   │   └── migrations/    # Database migrations
│   │   ├── adapters/          # External service adapters
│   │   │   ├── auth/
│   │   │   │   └── sso_adapter.py
│   │   │   └── payment/
│   │   │       └── payment_gateway.py
│   │   ├── cache/             # Redis implementations
│   │   │   └── redis_cache.py
│   │   └── services/          # Service implementations
│   │       ├── user_service.py
│   │       └── financial_service.py
│   ├── config/
│   │   ├── settings.py        # Environment configuration
│   │   ├── dependency.py      # DI Container
│   │   └── database.py        # DB configuration
│   └── main.py                # FastAPI app entry point
├── tests/
│   ├── api/                   # API integration tests
│   ├── domain/                # Domain unit tests
│   ├── infra/                 # Infrastructure tests
│   └── conftest.py            # Pytest fixtures
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Implementation Patterns

### 1. Domain Entity Pattern

```python
# src/domain/modules/user/entity.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Domain entity representing a user.

    Pure business logic with no framework dependencies.
    """
    id: int | None
    cpf: str
    name: str
    email: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self) -> None:
        """Business rule: Deactivate user account."""
        if not self.is_active:
            raise UserAlreadyInactiveError(f"User {self.cpf} is already inactive")
        self.is_active = False

    def validate_cpf(self) -> bool:
        """Business rule: Validate CPF format."""
        cleaned = ''.join(filter(str.isdigit, self.cpf))
        return len(cleaned) == 11 and not all(c == cleaned[0] for c in cleaned)
```

### 2. Repository Interface Pattern

```python
# src/domain/modules/user/repository.py
from abc import ABC, abstractmethod
from typing import List

from src.domain.modules.user.entity import User

class IUserRepository(ABC):
    """Abstract repository interface in domain layer.

    Defines contract without implementation details.
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Retrieve user by ID."""
        pass

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> User | None:
        """Retrieve user by CPF."""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create new user."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user."""
        pass

    @abstractmethod
    async def list_active(self, limit: int = 100) -> List[User]:
        """List all active users."""
        pass
```

### 3. Service Interface Pattern

```python
# src/domain/modules/user/service.py
from abc import ABC, abstractmethod
from typing import List

from src.domain.modules.user.entity import User

class IUserService(ABC):
    """Abstract service interface defining business operations."""

    @abstractmethod
    async def register_user(self, cpf: str, name: str, email: str) -> User:
        """Register new user with validation."""
        pass

    @abstractmethod
    async def deactivate_user(self, cpf: str) -> User:
        """Deactivate user account."""
        pass

    @abstractmethod
    async def get_user_profile(self, cpf: str) -> User:
        """Get user profile by CPF."""
        pass
```

### 4. Concrete Repository Implementation

```python
# src/infra/database/alchemist/modules/user/repository.py
from typing import List
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.modules.user.entity import User
from src.domain.modules.user.repository import IUserRepository
from src.infra.database.alchemist.models import UserModel

class UserRepository(IUserRepository):
    """SQLAlchemy implementation of user repository.

    Handles database operations and entity mapping.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        """Retrieve user by ID."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_cpf(self, cpf: str) -> User | None:
        """Retrieve user by CPF."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.cpf == cpf)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, user: User) -> User:
        """Create new user."""
        model = UserModel(
            cpf=user.cpf,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        """Update existing user."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one()
        model.name = user.name
        model.email = user.email
        model.is_active = user.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def list_active(self, limit: int = 100) -> List[User]:
        """List all active users."""
        result = await self._session.execute(
            select(UserModel)
            .where(UserModel.is_active == True)  # noqa: E712
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=model.id,
            cpf=model.cpf,
            name=model.name,
            email=model.email,
            created_at=model.created_at,
            is_active=model.is_active,
        )
```

### 5. Concrete Service Implementation

```python
# src/infra/services/user_service.py
from src.domain.modules.user.entity import User
from src.domain.modules.user.service import IUserService
from src.domain.modules.user.repository import IUserRepository
from src.domain.modules.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCPFError,
)

class UserService(IUserService):
    """Concrete implementation of user service.

    Orchestrates business logic using repository.
    """

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    async def register_user(self, cpf: str, name: str, email: str) -> User:
        """Register new user with validation."""
        # Check if user already exists
        existing_user = await self._repository.get_by_cpf(cpf)
        if existing_user:
            raise UserAlreadyExistsError(f"User with CPF {cpf} already exists")

        # Create and validate entity
        user = User(
            id=None,
            cpf=cpf,
            name=name,
            email=email,
            created_at=datetime.now(),
            is_active=True,
        )

        if not user.validate_cpf():
            raise InvalidCPFError(f"Invalid CPF: {cpf}")

        # Persist
        return await self._repository.create(user)

    async def deactivate_user(self, cpf: str) -> User:
        """Deactivate user account."""
        user = await self._repository.get_by_cpf(cpf)
        if not user:
            raise UserNotFoundError(f"User with CPF {cpf} not found")

        user.deactivate()  # Business logic in entity
        return await self._repository.update(user)

    async def get_user_profile(self, cpf: str) -> User:
        """Get user profile by CPF."""
        user = await self._repository.get_by_cpf(cpf)
        if not user:
            raise UserNotFoundError(f"User with CPF {cpf} not found")
        return user
```

### 6. Dependency Injection Container

```python
# src/config/dependency.py
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from src.infra.database.alchemist.session import get_session
from src.infra.database.alchemist.modules.user.repository import UserRepository
from src.infra.services.user_service import UserService

class Container(containers.DeclarativeContainer):
    """Dependency injection container.

    Wires together all dependencies.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.path.users",
            "src.api.path.auth",
        ]
    )

    # Database
    db_session = providers.Resource(get_session)

    # Repositories
    user_repository = providers.Factory(
        UserRepository,
        session=db_session,
    )

    # Services
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
```

### 7. API Endpoint Implementation

```python
# src/api/path/users.py
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.schemas.user import UserCreateRequest, UserResponse
from src.domain.modules.user.service import IUserService
from src.domain.modules.user.exceptions import UserAlreadyExistsError, InvalidCPFError
from src.config.dependency import Container

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
    request: UserCreateRequest,
    user_service: IUserService = Depends(Provide[Container.user_service]),
):
    """Create new user endpoint.

    Delegates to service layer for business logic.
    """
    try:
        user = await user_service.register_user(
            cpf=request.cpf,
            name=request.name,
            email=request.email,
        )
        return UserResponse.from_entity(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidCPFError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{cpf}", response_model=UserResponse)
@inject
async def get_user(
    cpf: str,
    user_service: IUserService = Depends(Provide[Container.user_service]),
):
    """Get user by CPF."""
    user = await user_service.get_user_profile(cpf)
    return UserResponse.from_entity(user)
```

### 8. Pydantic DTOs (Request/Response)

```python
# src/api/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from src.domain.modules.user.entity import User

class UserCreateRequest(BaseModel):
    """Request DTO for user creation."""
    cpf: str = Field(..., min_length=11, max_length=14)
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr

class UserResponse(BaseModel):
    """Response DTO for user data."""
    id: int
    cpf: str
    name: str
    email: str
    created_at: datetime
    is_active: bool

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        """Convert domain entity to DTO."""
        return cls(
            id=user.id,
            cpf=user.cpf,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            is_active=user.is_active,
        )
```

## Testing Strategy

### Unit Tests (Domain Layer)

```python
# tests/domain/modules/user/test_entity.py
import pytest
from src.domain.modules.user.entity import User
from src.domain.modules.user.exceptions import UserAlreadyInactiveError

def test_user_deactivation():
    """Test user deactivation business rule."""
    user = User(
        id=1,
        cpf="12345678901",
        name="Test User",
        email="test@example.com",
        created_at=datetime.now(),
        is_active=True,
    )

    user.deactivate()
    assert user.is_active is False

def test_user_already_inactive_raises_error():
    """Test deactivating already inactive user raises error."""
    user = User(
        id=1,
        cpf="12345678901",
        name="Test User",
        email="test@example.com",
        created_at=datetime.now(),
        is_active=False,
    )

    with pytest.raises(UserAlreadyInactiveError):
        user.deactivate()

def test_cpf_validation():
    """Test CPF validation logic."""
    user = User(
        id=1,
        cpf="12345678901",
        name="Test User",
        email="test@example.com",
        created_at=datetime.now(),
    )

    assert user.validate_cpf() is True

    user.cpf = "11111111111"  # All same digits
    assert user.validate_cpf() is False
```

### Service Tests (Infrastructure Layer)

```python
# tests/infra/services/test_user_service.py
import pytest
from unittest.mock import AsyncMock

from src.infra.services.user_service import UserService
from src.domain.modules.user.entity import User
from src.domain.modules.user.exceptions import UserAlreadyExistsError

@pytest.fixture
def mock_repository():
    """Mock user repository."""
    return AsyncMock()

@pytest.fixture
def user_service(mock_repository):
    """User service with mocked repository."""
    return UserService(user_repository=mock_repository)

@pytest.mark.asyncio
async def test_register_user_success(user_service, mock_repository):
    """Test successful user registration."""
    mock_repository.get_by_cpf.return_value = None
    mock_repository.create.return_value = User(
        id=1,
        cpf="12345678901",
        name="Test User",
        email="test@example.com",
        created_at=datetime.now(),
        is_active=True,
    )

    user = await user_service.register_user(
        cpf="12345678901",
        name="Test User",
        email="test@example.com",
    )

    assert user.id == 1
    assert user.cpf == "12345678901"
    mock_repository.create.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_already_exists(user_service, mock_repository):
    """Test registering existing user raises error."""
    mock_repository.get_by_cpf.return_value = User(
        id=1,
        cpf="12345678901",
        name="Existing User",
        email="existing@example.com",
        created_at=datetime.now(),
        is_active=True,
    )

    with pytest.raises(UserAlreadyExistsError):
        await user_service.register_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
        )
```

### Integration Tests (API Layer)

```python
# tests/api/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_endpoint(client: AsyncClient):
    """Test user creation endpoint."""
    response = await client.post(
        "/v1/users/",
        json={
            "cpf": "12345678901",
            "name": "Test User",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["cpf"] == "12345678901"
    assert data["name"] == "Test User"

@pytest.mark.asyncio
async def test_create_duplicate_user_returns_409(client: AsyncClient):
    """Test creating duplicate user returns conflict."""
    user_data = {
        "cpf": "12345678901",
        "name": "Test User",
        "email": "test@example.com",
    }

    # Create first user
    await client.post("/v1/users/", json=user_data)

    # Try to create duplicate
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == 409
```

## Database Session Management

```python
# src/infra/database/alchemist/session.py
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.config.settings import app_settings

# Engine configuration
engine = create_async_engine(
    app_settings.DATABASE_URL,
    echo=app_settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Get database session with automatic cleanup.

    Usage with dependency injection:
        session = Depends(get_session)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Configuration Management

```python
# src/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """Application configuration from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "FastAPI Clean Architecture"
    DEBUG: bool = False
    API_VERSION: str = "v1"

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True

app_settings = AppSettings()
```

## Main Application Setup

```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import app_settings
from src.config.dependency import Container
from src.api.path import users, auth

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    # Initialize DI container
    container = Container()

    # Create app
    app = FastAPI(
        title=app_settings.APP_NAME,
        version=app_settings.API_VERSION,
        debug=app_settings.DEBUG,
    )

    # Wire container
    app.container = container

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.CORS_ORIGINS,
        allow_credentials=app_settings.CORS_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(users.router)
    app.include_router(auth.router)

    return app

app = create_app()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

## Best Practices Checklist

### Architecture
- ✅ Domain layer has NO dependencies on API or Infrastructure
- ✅ All database logic encapsulated in repositories
- ✅ Business logic lives in domain entities and services
- ✅ Infrastructure implements domain interfaces
- ✅ API layer only handles HTTP concerns

### Dependency Injection
- ✅ Use `dependency-injector` for IoC container
- ✅ Wire all dependencies through container
- ✅ Inject interfaces, not concrete implementations
- ✅ Use `@inject` decorator on endpoints
- ✅ Configure wiring for all API modules

### Database
- ✅ Use SQLAlchemy 2.0 async patterns
- ✅ Separate ORM models from domain entities
- ✅ Implement mapper methods (`_to_entity`)
- ✅ Use connection pooling
- ✅ Handle transactions properly (commit/rollback)

### Testing
- ✅ 100% coverage for domain layer (pure logic)
- ✅ Mock repositories in service tests
- ✅ Use AsyncMock for async methods
- ✅ Integration tests for endpoints
- ✅ Separate test database for integration tests

### Naming Conventions
- ✅ Entities: PascalCase (`User`, `Order`)
- ✅ Services: `I{Name}Service` (interface), `{Name}Service` (implementation)
- ✅ Repositories: `I{Name}Repository` (interface), `{Name}Repository` (implementation)
- ✅ DTOs: `{Name}Request`, `{Name}Response`
- ✅ Use ptBR names for database columns if applicable

### Error Handling
- ✅ Domain exceptions for business rule violations
- ✅ HTTP exceptions at API layer only
- ✅ Proper status codes (400, 404, 409, 500)
- ✅ Meaningful error messages
- ✅ Global exception handler

## Common Pitfalls to Avoid

1. **Importing Infrastructure in Domain**
   - ❌ Never import SQLAlchemy models in domain layer
   - ✅ Use mapper functions to convert between layers

2. **Business Logic in API Layer**
   - ❌ Never put validation or business rules in endpoints
   - ✅ Move all logic to services or entities

3. **Tight Coupling**
   - ❌ Don't instantiate dependencies directly
   - ✅ Use dependency injection everywhere

4. **Anemic Entities**
   - ❌ Don't use entities as plain data containers
   - ✅ Put behavior and validation in entities

5. **Repository Leakage**
   - ❌ Don't expose SQLAlchemy queries outside repositories
   - ✅ Return domain entities only

6. **Improper Transaction Management**
   - ❌ Don't commit/rollback in repositories
   - ✅ Manage transactions at service or endpoint level

## Migration Guide (Legacy → Clean Architecture)

### Step 1: Create Domain Layer
1. Extract business entities from database models
2. Define repository interfaces
3. Define service interfaces
4. Move business logic to entities/services

### Step 2: Create Infrastructure Layer
1. Implement repositories with SQLAlchemy
2. Create service implementations
3. Keep database models separate from entities

### Step 3: Refactor API Layer
1. Create request/response DTOs
2. Update endpoints to use services
3. Remove direct database access
4. Add dependency injection

### Step 4: Testing
1. Write unit tests for domain layer
2. Add service tests with mocked repositories
3. Create integration tests for endpoints
4. Ensure 100% coverage

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic](https://docs.pydantic.dev/)

## Production Examples

This skill is based on patterns from:
- **GEFIN Backend**: Financial management system with 595+ tests
- **Clean Architecture**: Domain-driven design principles
- **Enterprise Best Practices**: Scalability, maintainability, testability
