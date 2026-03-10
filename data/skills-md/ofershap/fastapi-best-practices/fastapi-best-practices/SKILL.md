---
name: fastapi-best-practices
description:
  FastAPI done right. Async patterns, dependency injection, Pydantic v2 models, middleware, and
  project structure.
metadata:
  tags: fastapi, python, api, best-practices
---

## When to use

Use this skill when working with FastAPI code. It teaches current best practices and prevents common
mistakes that AI agents make with outdated patterns.

## Critical Rules

### 1. Use async def for I/O-bound endpoints, def for CPU-bound

**Wrong (agents do this):**

```python
@app.get("/users")
def get_users():
    users = db.query(User).all()
    return users

@app.get("/data")
async def get_data():
    result = heavy_computation()
    return result
```

**Correct:**

```python
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@app.get("/data")
def get_data():
    return heavy_computation()
```

**Why:** FastAPI runs async endpoints in the event loop; sync endpoints run in a thread pool. Use
async for I/O (DB, HTTP, file) to avoid blocking. Use def for CPU-bound work; making it async would
block the event loop.

### 2. Use Depends() for dependency injection

**Wrong (agents do this):**

```python
db = get_database()

@app.get("/items")
async def get_items():
    return db.query(Item).all()
```

**Correct:**

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def get_items(db: Annotated[Session, Depends(get_db)]):
    return db.query(Item).all()
```

**Why:** Global DB connections leak, are not testable, and bypass FastAPI's dependency system.
Depends() provides proper scoping, cleanup, and test overrides.

### 3. Use Pydantic v2 patterns

**Wrong (agents do this):**

```python
from pydantic import validator

class Item(BaseModel):
    name: str
    price: float

    class Config:
        orm_mode = True

    @validator("price")
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("must be positive")
        return v
```

**Correct:**

```python
from pydantic import BaseModel, field_validator, ConfigDict

class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: float

    @field_validator("price")
    @classmethod
    def price_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("must be positive")
        return v
```

**Why:** Pydantic v1 validator, Config, and orm_mode are deprecated. Use field_validator,
model_validator, ConfigDict, and from_attributes.

### 4. Use lifespan context manager

**Wrong (agents do this):**

```python
@app.on_event("startup")
async def startup():
    app.state.db = await create_pool()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()
```

**Correct:**

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await create_pool()
    yield
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)
```

**Why:** on_event is deprecated. The lifespan context manager gives a single place for startup and
shutdown with proper resource ordering.

### 5. Use BackgroundTasks for fire-and-forget work

**Wrong (agents do this):**

```python
@app.post("/send-email")
async def send_email(email: str):
    asyncio.create_task(send_email_async(email))
    return {"status": "queued"}
```

**Correct:**

```python
@app.post("/send-email")
async def send_email(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_async, email)
    return {"status": "queued"}
```

**Why:** asyncio.create_task can outlive the request and is not awaited on shutdown. BackgroundTasks
runs after the response is sent and is tied to the request lifecycle.

### 6. Use APIRouter for route organization

**Wrong (agents do this):**

```python
# main.py - 500 lines of routes
@app.get("/users")
@app.get("/users/{id}")
@app.post("/items")
@app.get("/items")
```

**Correct:**

```python
# main.py
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

# routers/users.py
router = APIRouter()
@router.get("/")
@router.get("/{id}")
```

**Why:** Single-file apps become unmaintainable. APIRouter enables routers/, models/, services/,
dependencies/ structure.

### 7. Use response_model for output validation

**Wrong (agents do this):**

```python
@app.get("/items/{id}")
async def get_item(id: int):
    item = await db.get(Item, id)
    return {"id": item.id, "name": item.name}
```

**Correct:**

```python
@app.get("/items/{id}", response_model=ItemOut)
async def get_item(id: int, db: Session = Depends(get_db)):
    item = await db.get(Item, id)
    if not item:
        raise HTTPException(status_code=404)
    return item
```

**Why:** Raw dicts bypass validation and OpenAPI. response_model ensures schema consistency,
serialization, and docs.

### 8. Use status codes from fastapi.status

**Wrong (agents do this):**

```python
raise HTTPException(status_code=404, detail="Not found")
raise HTTPException(status_code=401, detail="Unauthorized")
```

**Correct:**

```python
from fastapi import status

raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
```

**Why:** Magic numbers are error-prone. status constants are self-documenting and match HTTP spec.

### 9. Use Annotated for dependencies

**Wrong (agents do this):**

```python
@app.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
```

**Correct:**

```python
@app.get("/me")
async def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

**Why:** Annotated is the recommended FastAPI pattern. It keeps types and dependencies in one place
and supports dependency reuse.

### 10. Use pydantic-settings for configuration

**Wrong (agents do this):**

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
```

**Correct:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///db.sqlite"
    debug: bool = False
    model_config = {"env_file": ".env"}

settings = Settings()
```

**Why:** os.getenv has no validation or typing. BaseSettings provides validation, .env loading, and
type safety.

## Patterns

- Define routers in routers/ with prefix and tags
- Put shared dependencies in dependencies.py
- Use HTTPException with status constants for errors
- Use Path, Query, Body, Header with validation (min_length, ge, le)
- Register custom exception handlers with app.add_exception_handler
- Use middleware sparingly; order matters (first added runs last for requests)

## Anti-Patterns

- Do not use @app.on_event("startup") or @app.on_event("shutdown")
- Do not use asyncio.create_task for request-scoped background work
- Do not use global variables for DB, cache, or config
- Do not use Pydantic v1 @validator or class Config
- Do not return raw dicts without response_model
- Do not use magic numbers for status codes
- Do not put all routes in main.py
