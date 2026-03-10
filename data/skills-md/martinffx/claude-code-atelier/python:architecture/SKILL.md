---
name: python:architecture
description: Python application architecture with functional core, effectful shell, DDD, and data modeling. Use when designing application layers, separating pure business logic from IO, defining domain models, implementing validation, or structuring bounded contexts.
user-invocable: false
---

# Python Application Architecture

Modern Python application architecture following functional core / imperative shell pattern, Domain-Driven Design, and type-safe data modeling.

## Core Principle: Functional Core / Imperative Shell

Separate pure business logic from side effects:

- **Functional Core**: Pure functions, business logic, no IO
- **Imperative Shell**: Coordinates external dependencies, handles side effects

See [references/functional-core.md](references/functional-core.md) for detailed patterns and examples.

## Layered Architecture

Follow bottom-up dependency flow:

```
Router/Handler → Service → Repository → Entity → Database
```

Each layer depends only on layers below.

**Responsibilities:**
- **Entity**: Domain models, validation, business rules, data transformations (fromRequest, toRecord, toResponse)
- **Repository**: Abstract storage interface, returns domain entities
- **Service**: Business workflows, orchestrates entities and repositories
- **Router/Handler**: HTTP handling, delegates to services

## Domain Models

### Entity Example

```python
from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass
class Order:
    """Entity - has identity and encapsulated behavior"""
    id: UUID
    customer_id: UUID
    total: Decimal
    status: str

    def apply_discount(self, rate: Decimal) -> None:
        """Business rule - encapsulated in entity"""
        if self.status == "pending":
            self.total = self.total * (1 - rate)

    @classmethod
    def from_request(cls, req, customer_id: UUID) -> "Order":
        """Transform API request → entity"""
        return cls(id=uuid4(), customer_id=customer_id, total=Decimal("0"), status="pending")

    def to_response(self):
        """Transform entity → API response"""
        return {"id": self.id, "total": self.total, "status": self.status}
```

### Value Object Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    """Value object - immutable, no identity"""
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

See [references/ddd.md](references/ddd.md) for aggregates, bounded contexts, and domain services.

## Repository Pattern

Abstract storage behind interface:

```python
from abc import ABC, abstractmethod
from typing import Optional

class OrderRepository(ABC):
    """Abstract repository - interface only"""

    @abstractmethod
    def get(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

class PostgresOrderRepository(OrderRepository):
    """Concrete implementation"""

    def get(self, order_id: UUID) -> Optional[Order]:
        record = self.session.get(OrderRecord, order_id)
        return Order.from_record(record) if record else None

    def save(self, order: Order) -> None:
        record = order.to_record()
        self.session.merge(record)
        self.session.commit()
```

## Data Modeling

- **dataclasses**: Domain models and internal logic (lightweight, standard library)
- **Pydantic**: API boundaries (validation, JSON schema, OpenAPI)
- **Entity transformations**: `from_request()`, `to_response()`, `from_record()`, `to_record()`

See [references/data-modeling.md](references/data-modeling.md) for validation patterns, Pydantic features, and transformation examples.

## Best Practices

1. **Pure functions first** - Write business logic without IO dependencies
2. **Entity encapsulation** - Keep business rules inside entities
3. **Repository abstraction** - Hide storage details, work with domain entities
4. **Validate at boundaries** - Use Pydantic at API edges, simple validation in entities
5. **Immutable value objects** - Always use `frozen=True`
6. **Single Responsibility** - Each layer has one reason to change
7. **Dependency direction** - Always depend on abstractions, not implementations

## Anti-Patterns

❌ **Anemic Domain Model** - Entities with only getters/setters, all logic in services
❌ **Transaction Script** - All logic in service layer, entities just data
❌ **Leaky Abstraction** - Repository exposing database details
❌ **God Object** - Entity with too many responsibilities
❌ **Mixed Concerns** - Business logic calling IO directly

For detailed examples, patterns, and decision trees, see the reference materials:
- [references/functional-core.md](references/functional-core.md) - Core vs shell separation
- [references/ddd.md](references/ddd.md) - DDD patterns, aggregates, bounded contexts
- [references/data-modeling.md](references/data-modeling.md) - dataclasses, Pydantic, transformations
