---
name: python:fastapi
description: Building REST APIs with FastAPI, Pydantic validation, and OpenAPI. Use when creating routes, handling requests, designing endpoints, implementing validation, error responses, pagination, or generating API documentation.
user-invocable: false
---

# FastAPI - Modern Python Web APIs

FastAPI is a modern, fast web framework for building APIs with Python, using standard Python type hints. FastAPI automatically validates requests, generates OpenAPI documentation, and provides excellent developer experience.

## Quick Start

### Basic Application

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for my application",
    version="1.0.0",
)

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items", response_model=Item)
def create_item(item: Item):
    return item
```

**Run with:**
```bash
uvicorn main:app --reload
```

## Core Concepts

### Request & Response Models

Use Pydantic models for automatic validation and serialization:

```python
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    model_config = {"from_attributes": True}  # Enable ORM mode

@app.post("/users", response_model=UserResponse)
def create_user(user: CreateUserRequest):
    """Request validated, response serialized automatically"""
    return user
```

See `references/validation.md` for detailed validation patterns including custom validators and field constraints.

### Routers for Organization

Split routes across routers for clean organization:

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    ...

@router.post("/")
def create_user(user: CreateUserRequest):
    ...

# main.py
app.include_router(users.router)
```

### Dependency Injection

FastAPI's core feature for managing dependencies like database sessions and authentication:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db() -> Session:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    """db automatically injected"""
    return db.query(User).all()
```

See `references/dependencies.md` for advanced patterns including auth services, scoped dependencies, and dependency classes.

## Error Handling

### HTTP Exceptions

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessError(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )
```

## Project Structure

```
my-api/
├── main.py                   # FastAPI app
├── routers/                  # Route handlers
│   ├── users.py
│   └── products.py
├── schemas/                  # Pydantic models
│   ├── users.py
│   └── products.py
├── services/                 # Business logic
│   └── users.py
├── repositories/             # Data access
│   └── users.py
└── dependencies.py           # Dependency injection
```

## Reference Materials

Detailed patterns for common scenarios:

- **Validation**: `references/validation.md` - Field constraints, custom validators, model validation
- **Dependencies**: `references/dependencies.md` - Auth services, scoped dependencies, advanced injection patterns
- **Middleware**: `references/middleware.md` - CORS, custom middleware, request/response processing
- **API Design**: `references/api-design.md` - REST naming, pagination, OpenAPI customization, status codes

## Best Practices

1. **Use response_model** - Always define explicit response schemas
2. **Validate inputs** - Use Pydantic models with constraints
3. **Dependency injection** - Manage sessions, auth, and cross-cutting concerns
4. **Router organization** - Split routes by resource/domain
5. **Error handling** - Use HTTP exceptions and custom handlers appropriately
6. **Type hints** - FastAPI uses them for both validation and documentation
