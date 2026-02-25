---
name: golang-ddd
description: "This skill should be used when implementing DDD tactical design patterns in Go, including Entities, Value Objects, Aggregates, Repositories, Domain Services, Domain Events, Factories, and Specifications."
license: MIT
metadata:
  version: "1.0.0"
  domain: architecture
  triggers: ddd golang, domain driven design go, aggregate go, entity go, value object go, repository pattern go, domain events go, ddd tactical
  role: specialist
  scope: implementation
  output-format: code
---

# DDD Tactical Design Patterns in Go

## Purpose

To guide implementation of Domain-Driven Design tactical patterns in idiomatic Go. This skill covers Entities, Value Objects, Aggregates, Repositories, Domain Services, Domain Events, Factories, and Specifications using Go-native idioms (composition over inheritance, interfaces, unexported fields, functional options).

## When to Use This Skill

- Implementing domain models with rich business logic in Go
- Designing aggregate boundaries and consistency rules
- Creating repository interfaces and infrastructure implementations
- Building event-driven domain models
- Structuring a Go project following DDD layered architecture
- Reviewing domain code for DDD pattern adherence

## Core Principles

1. **Go idioms first** - No Java-style OOP. Use composition, interfaces, and package boundaries
2. **Unexported fields** - All entity/aggregate fields lowercase; expose through getters and behavior methods
3. **Pointer receivers for entities** - Mutable domain objects use `*T` receivers
4. **Value receivers for value objects** - Immutable types use `T` receivers
5. **Factory functions** - Use `NewX()` constructors to enforce invariants at creation
6. **Interface in domain, implementation in infrastructure** - Repository interfaces live with aggregates
7. **One package per aggregate** - Each aggregate root gets its own package under `internal/domain/`
8. **Context propagation** - Pass `context.Context` as first parameter in repository and service methods

## Project Structure

```
internal/
├── domain/                     # Domain layer (no external deps)
│   ├── customer/               # One package per aggregate
│   │   ├── customer.go         # Aggregate root entity
│   │   ├── repository.go       # Repository interface
│   │   ├── email.go            # Value objects
│   │   ├── events.go           # Domain events
│   │   └── errors.go           # Domain errors
│   ├── order/
│   │   ├── order.go
│   │   ├── repository.go
│   │   ├── item.go             # Child entity
│   │   └── money.go            # Value object
│   └── shared/                 # Shared kernel
│       ├── events.go           # Event interface
│       └── specification.go    # Generic specification
│
├── application/                # Application services (orchestration)
│   ├── command/
│   │   └── place_order.go
│   └── query/
│       └── get_customer.go
│
└── infrastructure/             # Technical implementations
    ├── postgres/
    │   ├── customer_repo.go
    │   └── order_repo.go
    └── eventbus/
        └── in_memory.go
```

**Dependency rule:** Domain has zero imports from application or infrastructure. Dependencies point inward.

## Pattern Quick Reference

| Pattern | Go Idiom | Receiver | Identity |
|---------|----------|----------|----------|
| Entity | Struct + pointer receiver | `*T` | By ID |
| Value Object | Type alias or struct + value receiver | `T` | By value |
| Aggregate Root | Entity + unexported children | `*T` | By ID |
| Repository | Interface in domain package | N/A | N/A |
| Domain Service | Stateless struct with deps | `*T` or func | N/A |
| Domain Event | Immutable struct | `T` (value) | By name+time |
| Factory | `NewX()` function | N/A | N/A |
| Specification | Generic interface `IsSatisfiedBy(T) bool` | `T` or `*T` | N/A |

## Implementation Workflow

When implementing a new aggregate or domain concept:

1. **Define value objects** - Create self-validating types for domain primitives (`Email`, `Money`, `Address`)
2. **Define entities** - Create types with identity, unexported fields, and behavior methods
3. **Define aggregate root** - Designate one entity as root; enforce all invariants through its methods
4. **Define repository interface** - Place interface in same package as aggregate root
5. **Define domain events** - Create immutable event structs for significant state changes
6. **Implement infrastructure** - Create repository implementations in `infrastructure/` package
7. **Wire application layer** - Create command/query handlers that orchestrate domain operations

## Pattern Details

For detailed implementation guides with full code examples, see:
- `references/entities-and-value-objects.md` - Entities, Value Objects, and Factories
- `references/aggregates-and-repositories.md` - Aggregates, Repositories, and Domain Services
- `references/events-and-specifications.md` - Domain Events and Specifications
- `references/anti-patterns.md` - Common mistakes and how to avoid them

### Entities

Entities have unique identity and mutable state. Use unexported fields, pointer receivers, and factory functions.

```go
type Order struct {
    id        uuid.UUID
    status    Status
    items     []Item
    createdAt time.Time
}

func NewOrder(customerID uuid.UUID) (*Order, error) {
    return &Order{
        id:        uuid.New(),
        status:    StatusDraft,
        items:     make([]Item, 0),
        createdAt: time.Now(),
    }, nil
}

func (o *Order) AddItem(product ProductID, qty int, price Money) error {
    if o.status != StatusDraft {
        return ErrOrderNotDraft
    }
    o.items = append(o.items, NewItem(product, qty, price))
    return nil
}
```

### Value Objects

Immutable types validated at creation. Use value receivers. Return new instances for operations.

```go
type Money struct {
    amount   int64
    currency string
}

func NewMoney(amount int64, currency string) (Money, error) {
    if currency == "" {
        return Money{}, ErrInvalidCurrency
    }
    return Money{amount: amount, currency: currency}, nil
}

func (m Money) Add(other Money) (Money, error) {
    if m.currency != other.currency {
        return Money{}, ErrCurrencyMismatch
    }
    return Money{amount: m.amount + other.amount, currency: m.currency}, nil
}
```

### Aggregates

Aggregate roots enforce invariants across child entities. All mutations go through the root.

```go
func (o *Order) Place() error {
    if len(o.items) == 0 {
        return ErrEmptyOrder
    }
    if o.status != StatusDraft {
        return ErrOrderNotDraft
    }
    o.status = StatusPlaced
    o.events = append(o.events, NewOrderPlacedEvent(o.id, o.Total()))
    return nil
}
```

### Repositories

Interface in domain, implementation in infrastructure. One repository per aggregate root.

```go
// domain/order/repository.go
type Repository interface {
    Find(ctx context.Context, id uuid.UUID) (*Order, error)
    Save(ctx context.Context, order *Order) error
    Update(ctx context.Context, id uuid.UUID, fn func(*Order) error) error
}
```

### Domain Events

Immutable structs collected by aggregates, published by application layer.

```go
type OrderPlaced struct {
    orderID    uuid.UUID
    total      Money
    occurredAt time.Time
}

func (o *Order) PullEvents() []Event {
    events := o.events
    o.events = nil
    return events
}
```

### Domain Services

Stateless operations spanning multiple aggregates. Domain logic only, no orchestration.

```go
type TransferService struct {
    accountRepo account.Repository
}

func (s *TransferService) Transfer(ctx context.Context, from, to uuid.UUID, amount Money) error {
    // Load aggregates, validate domain rules, coordinate changes
}
```

### Specifications

Composable business rules using Go generics.

```go
type Specification[T any] interface {
    IsSatisfiedBy(T) bool
}

func And[T any](specs ...Specification[T]) Specification[T] { /* ... */ }
func Or[T any](specs ...Specification[T]) Specification[T]  { /* ... */ }
func Not[T any](spec Specification[T]) Specification[T]     { /* ... */ }
```

## Key Rules

- **Never expose aggregate internals** - No public fields, no getters that return mutable child collections
- **No setters** - Replace `SetStatus()` with domain methods like `Place()`, `Cancel()`, `Ship()`
- **Reference other aggregates by ID** - Never hold direct pointers to other aggregate roots
- **Reconstitution factories** - Create separate `Reconstruct()` functions for loading from DB (bypass validation)
- **Domain errors** - Define sentinel errors (`var ErrNotFound = errors.New(...)`) per aggregate package
- **Accept interfaces, return structs** - Repository parameters use interfaces; factories return concrete types

## References

Detailed guides with full code examples are in the `references/` directory.
