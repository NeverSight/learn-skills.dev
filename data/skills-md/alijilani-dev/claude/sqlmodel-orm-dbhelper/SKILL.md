---
name: sqlmodel-orm-dbhelper
description: |
  Design and implement production-grade database layers using SQLModel with SQLAlchemy 2.0 patterns.
  This skill should be used when users need to create database models, configure engines/sessions,
  design schemas, implement relationships, or optimize database performance in Python FastAPI projects.
---

# SQLModel ORM Database Helper

A comprehensive skill for designing robust, high-performance database management layers using SQLModel.

## What This Skill Does

- Designs optimal database schemas based on project context
- Creates production-ready SQLModel models with proper types and constraints
- Configures engine with connection pooling (QueuePool, NullPool)
- Implements session management for FastAPI dependency injection
- Defines relationships (One-to-One, One-to-Many, Many-to-Many)
- Implements automatic timestamps (created_at, updated_at)
- Optimizes for performance (indexing, lazy/eager loading, N+1 prevention)
- Follows SQLAlchemy 2.0 and modern Python type hints (Annotated, Optional)

## What This Skill Does NOT Do

- Database migrations (use Alembic separately)
- Database administration or server configuration
- Raw SQL query optimization (focuses on ORM patterns)
- NoSQL database design
- Database backup/restore operations

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, database.py, project structure, FastAPI app setup |
| **Conversation** | Project domain, entities, relationships, performance requirements |
| **Skill References** | SQLModel patterns from `references/` (models, relationships, engine config) |
| **User Guidelines** | Naming conventions, project standards, database choice (SQLite/PostgreSQL/MySQL) |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER's context before designing:

1. **Project Domain**: "What is your project about? (e.g., e-commerce, inventory, blog)"
2. **Key Entities**: "What are the main entities/tables you need?"
3. **Database**: "Which database? (SQLite for dev, PostgreSQL/MySQL for production)"
4. **Performance Priority**: "Any specific performance concerns? (high read, high write, real-time)"

---

## Workflow

```
1. Understand Domain → 2. Design Schema → 3. Create Models → 4. Configure Engine → 5. Implement Session → 6. Add Relationships → 7. Optimize
```

### Step 1: Understand Domain
- Identify entities and their attributes
- Map relationships between entities
- Determine data types and constraints

### Step 2: Design Schema
- Normalize to 3NF (balance with query performance)
- Define primary keys, foreign keys, unique constraints
- Plan indexes for query patterns

### Step 3: Create Models
- Use SQLModel with proper type annotations
- Implement mixins for common fields (timestamps)
- Add field constraints and validators

### Step 4: Configure Engine
- Set up connection pooling based on use case
- Configure echo for debugging (dev only)
- Set appropriate pool size and overflow

### Step 5: Implement Session
- Create session generator for FastAPI Depends
- Use context managers for proper cleanup
- Implement transaction boundaries

### Step 6: Add Relationships
- Define relationship fields with back_populates
- Configure cascade behaviors
- Set lazy/eager loading strategies

### Step 7: Optimize
- Add indexes for frequent queries
- Configure eager loading for N+1 prevention
- Review and tune connection pool settings

---

## Schema Design Principles

### Normalization Guidelines

| Normal Form | When to Use |
|-------------|-------------|
| **1NF** | Always - atomic values, no repeating groups |
| **2NF** | Always - remove partial dependencies |
| **3NF** | Default - remove transitive dependencies |
| **Denormalize** | Only for proven performance needs |

### Data Type Selection

| Data Type | SQLModel Type | Use Case |
|-----------|---------------|----------|
| Primary Key | `int | None = Field(default=None, primary_key=True)` | Auto-increment ID |
| UUID PK | `uuid.UUID = Field(default_factory=uuid4, primary_key=True)` | Distributed systems |
| String | `str = Field(max_length=255)` | Text with limit |
| Text | `str = Field(sa_type=Text)` | Unlimited text |
| DateTime | `datetime = Field(default_factory=datetime.utcnow)` | Timestamps |
| DateTime TZ | `datetime = Field(sa_type=DateTime(timezone=True))` | Timezone-aware |
| Decimal | `Decimal = Field(max_digits=10, decimal_places=2)` | Financial data |
| JSON | `dict = Field(sa_type=JSON)` | Flexible schemas |
| JSONB | `dict = Field(sa_type=JSONB)` | PostgreSQL queryable JSON |

---

## Model Patterns

### Base Model with Timestamps

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False
    )

class BaseModel(TimestampMixin):
    id: Optional[int] = Field(default=None, primary_key=True)
```

### Model with Relationships

See `references/relationships.md` for complete relationship patterns.

---

## Engine & Session Configuration

### Production Engine Setup

```python
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool

DATABASE_URL = "postgresql://user:pass@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,           # Persistent connections
    max_overflow=10,       # Additional connections under load
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections every 30 min
    pool_pre_ping=True,    # Verify connection health
    echo=False,            # Disable SQL logging in production
)
```

### Session Generator for FastAPI

```python
from typing import Generator
from fastapi import Depends
from sqlmodel import Session

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Usage in FastAPI endpoint
@app.get("/items")
def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()
```

See `references/engine-config.md` for database-specific configurations.

---

## Performance Optimization

### Indexing Strategy

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)  # Unique + indexed
    username: str = Field(index=True)            # Frequently queried
    status: str = Field(index=True)              # Filter field
```

### Preventing N+1 Queries

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload

# Eager load related objects
statement = select(User).options(selectinload(User.orders))
users = session.exec(statement).all()

# Use joinedload for single related object
statement = select(Order).options(joinedload(Order.user))
```

### Lazy vs Eager Loading

| Strategy | Use When |
|----------|----------|
| `lazy="select"` (default) | Related data rarely needed |
| `lazy="selectin"` | Loading multiple parents with children |
| `lazy="joined"` | Always need related data, single object |
| `lazy="subquery"` | Complex queries with collections |

See `references/performance.md` for advanced optimization patterns.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Session per operation | Connection overhead | One session per request |
| Missing indexes | Slow queries | Index frequently filtered columns |
| N+1 queries | Performance killer | Use eager loading |
| No connection pooling | Resource exhaustion | Use QueuePool |
| Committing in loops | Transaction overhead | Batch operations |
| No pool_pre_ping | Stale connections | Enable pre-ping |
| Hardcoded credentials | Security risk | Use environment variables |

---

## Output Specification

When implementing, deliver:

1. **Schema Design Document**: Logical explanation of tables and relationships
2. **models.py**: Clean SQLModel implementations with:
   - Type-annotated fields
   - Proper constraints (PK, FK, unique, indexes)
   - Relationship definitions
   - Timestamp mixins
3. **database.py**: Production-ready setup with:
   - Engine configuration with pooling
   - Session generator for FastAPI
   - Database initialization function
4. **Performance Notes**: Brief optimization explanations

---

## Output Checklist

Before delivering, verify:

- [ ] All entities from requirements are modeled
- [ ] Primary keys defined for all tables
- [ ] Foreign keys maintain referential integrity
- [ ] Indexes added for frequently queried columns
- [ ] Relationships use back_populates correctly
- [ ] Engine uses connection pooling
- [ ] Session generator uses context manager
- [ ] Timestamps (created_at/updated_at) implemented
- [ ] No hardcoded credentials
- [ ] Type hints use modern Python (Annotated, Optional)
- [ ] Code follows SQLAlchemy 2.0 patterns

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/relationships.md` | Implementing One-to-One, One-to-Many, Many-to-Many |
| `references/engine-config.md` | Database-specific engine configuration |
| `references/performance.md` | Advanced optimization, query tuning |
| `references/field-types.md` | Complete field type reference |
| `references/migrations.md` | Alembic migration guidance |
