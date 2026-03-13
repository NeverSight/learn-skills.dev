---
name: fastapi
description: This skill MUST be loaded when ANY .py file involving FastAPI is being read, reviewed, edited, or created. Also use when the user asks to "create a FastAPI app", "add an API endpoint", "create a REST API", "implement authentication", "add OAuth2", "create Pydantic models", "add request validation", "implement dependency injection", "create API routers", "add middleware", "handle errors in FastAPI", "create background tasks", "add WebSocket endpoints", "implement CRUD operations", "review a FastAPI route", "read a FastAPI file", or mentions FastAPI, Pydantic with FastAPI, async Python APIs, Starlette, or FastAPI patterns.
---

# FastAPI Development Guide

This skill provides comprehensive guidance for building high-performance Python APIs with FastAPI.

## Core Concepts

### Application Structure

FastAPI applications follow this recommended structure:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Settings and configuration
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── db/                  # Database related
│       ├── __init__.py
│       └── database.py
├── tests/
├── requirements.txt
└── pyproject.toml
```

### Basic Application Setup

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    print("Starting up...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down...")

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Pydantic Models

Use Pydantic for request/response validation:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
```

### Path Operations

```python
from fastapi import FastAPI, Path, Query, Body, HTTPException, status

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., gt=0, description="User ID"),
    include_posts: bool = Query(False, description="Include user posts"),
):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return await create_new_user(user)

@app.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user: UserUpdate = Body(...),
):
    return await update_user_by_id(user_id, user)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    await delete_user_by_id(user_id)
    return None
```

### APIRouter for Organization

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    return await get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router, prefix="/api/v1")
```

### Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from typing import Annotated

# Simple dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency with parameters
def get_query_params(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
):
    return {"skip": skip, "limit": limit}

# Using dependencies
@app.get("/items/")
async def get_items(
    db: Annotated[Session, Depends(get_db)],
    params: Annotated[dict, Depends(get_query_params)],
):
    return db.query(Item).offset(params["skip"]).limit(params["limit"]).all()

# Class-based dependency
class CommonParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit

@app.get("/resources/")
async def get_resources(commons: Annotated[CommonParams, Depends()]):
    return {"skip": commons.skip, "limit": commons.limit}
```

### Authentication with OAuth2

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
```

### Error Handling

```python
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Custom exception
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

# Exception handler
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": f"Item {exc.item_id} not found"},
    )

# Override validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )

# Usage
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await find_item(item_id)
    if not item:
        raise ItemNotFoundError(item_id)
    return item
```

### Middleware

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

async def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification sent in the background"}
```

### Response Models and Status Codes

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, RedirectResponse

@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Item created successfully"},
        400: {"description": "Invalid input"},
        409: {"description": "Item already exists"},
    },
)
async def create_item(item: ItemCreate):
    return await create_new_item(item)

@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="/items/")

@app.get("/custom-response")
async def custom_response():
    return JSONResponse(
        content={"message": "Custom response"},
        headers={"X-Custom-Header": "value"},
    )
```

## Best Practices

1. **Use Pydantic models** for all request/response validation
2. **Organize with routers** - Group related endpoints in separate router files
3. **Use dependency injection** for shared logic (database, auth, etc.)
4. **Handle errors properly** with appropriate status codes and messages
5. **Use async/await** for I/O operations (database, HTTP calls)
6. **Add OpenAPI documentation** via docstrings and response models
7. **Use type hints** everywhere for better IDE support and validation
8. **Separate concerns** - Keep business logic in services, not route handlers
9. **Use environment variables** for configuration via pydantic-settings
10. **Write tests** using TestClient from fastapi.testclient

## Common Patterns

See the `references/` directory for detailed patterns:
- `authentication.md` - OAuth2 and JWT authentication patterns
- `database.md` - SQLAlchemy and async database patterns
- `testing.md` - Testing strategies and patterns

See the `examples/` directory for working code:
- `crud_router.py` - Complete CRUD router example
- `auth_dependencies.py` - Authentication dependency examples
- `middleware_examples.py` - Common middleware patterns
