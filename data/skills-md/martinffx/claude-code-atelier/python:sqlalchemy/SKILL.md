---
name: python:sqlalchemy
description: SQLAlchemy ORM patterns for Python database access. Use when defining models, writing queries, implementing upserts, working with JSON columns, or managing database sessions.
user-invocable: false
---

# SQLAlchemy ORM Patterns

Modern SQLAlchemy 2.0+ patterns for database access in Python applications.

## Model Definition

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from uuid import UUID
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal]
    in_stock: Mapped[bool] = mapped_column(default=True)
```

## Session Management

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Query Patterns

```python
# Select
stmt = select(ProductModel).where(ProductModel.price > 100)
products = session.execute(stmt).scalars().all()

# Filter
products = session.query(ProductModel).filter(ProductModel.in_stock == True).all()

# Get by ID
product = session.get(ProductModel, product_id)

# Count
count = session.query(ProductModel).count()
```

## Upsert

```python
from sqlalchemy.dialects.postgresql import insert

stmt = insert(ProductModel).values(
    id=product_id,
    name="Widget",
    price=9.99,
)

# On conflict, update
stmt = stmt.on_conflict_do_update(
    index_elements=["id"],
    set_={"name": stmt.excluded.name, "price": stmt.excluded.price},
)

session.execute(stmt)
session.commit()
```

## Relationships

```python
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="user")

class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="orders")
```

## JSON Columns

```python
from sqlalchemy import JSON

class ConfigModel(Base):
    __tablename__ = "configs"
    id: Mapped[int] = mapped_column(primary_key=True)
    settings: Mapped[dict] = mapped_column(JSON)

# Query JSON field
configs = session.query(ConfigModel).filter(
    ConfigModel.settings["theme"] == "dark"
).all()
```

See references/ for model patterns, query optimization, and async SQLAlchemy.
