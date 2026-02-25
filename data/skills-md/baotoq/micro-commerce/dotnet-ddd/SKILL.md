---
name: dotnet-ddd
description: Implement Domain-Driven Design tactical patterns in C#/.NET. Use when building Entities, Value Objects, Aggregates, Domain Events, Repositories, or structuring a DDD solution. Framework-agnostic — covers pure domain modeling with modern C#.
license: MIT
metadata:
  version: "1.0.0"
  domain: architecture
  triggers: DDD, domain driven design, aggregate, value object, entity, domain event, repository pattern, bounded context, aggregate root, domain model, domain layer, rich domain model
  role: architect
  scope: implementation
  output-format: code
  related-skills: domain-analysis, architecture-patterns, csharp-developer, dotnet-core-expert
---

# Domain-Driven Design in .NET

Tactical DDD implementation patterns in modern C# — building rich domain models with Entities, Value Objects, Aggregates, Domain Events, and Repositories.

**Scope:** This skill covers **tactical DDD** (the building blocks). For strategic DDD (Bounded Contexts, Context Mapping, subdomain analysis), use the `domain-analysis` skill.

## When to Use

- Modeling a domain with complex business rules
- Implementing Entities, Value Objects, or Aggregates
- Raising and handling Domain Events
- Designing Repository interfaces
- Structuring a .NET solution with DDD layers
- Applying the Result pattern, Strongly-typed IDs, or Specification pattern

**Not for:** Simple CRUD apps, anemic domain models, or when business logic lives entirely in services.

## Key Concepts

| Concept | What It Is | C# Implementation |
|---|---|---|
| **Entity** | Object with identity that persists across state changes | Class with `Id`, equality by identity |
| **Value Object** | Immutable object defined by its attributes, no identity | `record` or `sealed class` with structural equality |
| **Aggregate** | Cluster of Entities/VOs with a single root, consistency boundary | Root entity that guards all invariants |
| **Aggregate Root** | Entry point to an Aggregate — the only externally-referenced entity | Public API, owns child entities |
| **Domain Event** | Something that happened in the domain that other parts care about | `record` implementing `IDomainEvent` |
| **Repository** | Abstraction for persisting/retrieving Aggregates | Interface in Domain, implementation in Infrastructure |
| **Domain Service** | Stateless operation that doesn't belong to a single Entity/VO | Static method or injected service |
| **Specification** | Encapsulated query/business rule | Class with `IsSatisfiedBy(T)` |

## Entity Base Class

```csharp
public abstract class Entity<TId> : IEquatable<Entity<TId>>
    where TId : notnull
{
    public TId Id { get; protected init; }

    private readonly List<IDomainEvent> _domainEvents = [];
    public IReadOnlyList<IDomainEvent> DomainEvents => _domainEvents;

    protected Entity(TId id) => Id = id;

    public void RaiseDomainEvent(IDomainEvent domainEvent) =>
        _domainEvents.Add(domainEvent);

    public void ClearDomainEvents() => _domainEvents.Clear();

    public bool Equals(Entity<TId>? other) =>
        other is not null && Id.Equals(other.Id);

    public override bool Equals(object? obj) =>
        obj is Entity<TId> other && Equals(other);

    public override int GetHashCode() => Id.GetHashCode();

    public static bool operator ==(Entity<TId>? left, Entity<TId>? right) =>
        Equals(left, right);

    public static bool operator !=(Entity<TId>? left, Entity<TId>? right) =>
        !Equals(left, right);

    // Protected parameterless constructor for ORM
    protected Entity() => Id = default!;
}
```

## Value Object with `record`

```csharp
public record Money(decimal Amount, string Currency)
{
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException($"Cannot add {Currency} to {other.Currency}");
        return this with { Amount = Amount + other.Amount };
    }

    public static Money Zero(string currency) => new(0, currency);
}

public record Address(string Street, string City, string State, string ZipCode, string Country);

public record DateRange
{
    public DateOnly Start { get; init; }
    public DateOnly End { get; init; }

    public DateRange(DateOnly start, DateOnly end)
    {
        if (end < start)
            throw new ArgumentException("End date must be after start date");
        Start = start;
        End = end;
    }

    public bool Overlaps(DateRange other) =>
        Start <= other.End && other.Start <= End;
}
```

## Aggregate Example

```csharp
public sealed class Order : Entity<OrderId>
{
    private readonly List<OrderLine> _lines = [];
    public IReadOnlyList<OrderLine> Lines => _lines;
    public CustomerId CustomerId { get; private init; }
    public OrderStatus Status { get; private set; }
    public Money Total => _lines.Aggregate(Money.Zero("USD"), (sum, line) => sum.Add(line.SubTotal));

    private Order() { } // ORM

    public static Order Create(CustomerId customerId)
    {
        var order = new Order(OrderId.New())
        {
            CustomerId = customerId,
            Status = OrderStatus.Draft
        };
        order.RaiseDomainEvent(new OrderCreatedEvent(order.Id));
        return order;
    }

    public void AddLine(ProductId productId, int quantity, Money unitPrice)
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException("Can only add lines to draft orders");
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");

        var line = new OrderLine(OrderLineId.New(), productId, quantity, unitPrice);
        _lines.Add(line);
    }

    public void Submit()
    {
        if (_lines.Count == 0)
            throw new DomainException("Cannot submit an empty order");
        Status = OrderStatus.Submitted;
        RaiseDomainEvent(new OrderSubmittedEvent(Id, Total));
    }
}
```

**Aggregate rules:**
1. Reference other Aggregates by ID only, never by direct object reference
2. All state changes go through the Aggregate Root
3. One transaction = one Aggregate (eventual consistency between Aggregates)
4. Keep Aggregates small — only include what must be immediately consistent

## Strongly-Typed IDs

```csharp
public readonly record struct OrderId(Guid Value)
{
    public static OrderId New() => new(Guid.NewGuid());
    public override string ToString() => Value.ToString();
}

public readonly record struct CustomerId(Guid Value)
{
    public static CustomerId New() => new(Guid.NewGuid());
}
```

## Domain Events

```csharp
public interface IDomainEvent
{
    DateTime OccurredOn { get; }
}

public abstract record DomainEvent : IDomainEvent
{
    public DateTime OccurredOn { get; init; } = DateTime.UtcNow;
}

public record OrderCreatedEvent(OrderId OrderId) : DomainEvent;
public record OrderSubmittedEvent(OrderId OrderId, Money Total) : DomainEvent;
```

## Repository Interface

```csharp
// Define in Domain layer — implement in Infrastructure
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(OrderId id, CancellationToken ct = default);
    Task AddAsync(Order order, CancellationToken ct = default);
    Task UpdateAsync(Order order, CancellationToken ct = default);
}

// Optional: generic base interface
public interface IRepository<T, TId>
    where T : Entity<TId>
    where TId : notnull
{
    Task<T?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task AddAsync(T entity, CancellationToken ct = default);
}
```

## Result Pattern (No Exceptions for Expected Failures)

```csharp
public sealed class Result<T>
{
    public T? Value { get; }
    public Error? Error { get; }
    public bool IsSuccess => Error is null;

    private Result(T value) => Value = value;
    private Result(Error error) => Error = error;

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(Error error) => new(error);

    public TOut Match<TOut>(Func<T, TOut> onSuccess, Func<Error, TOut> onFailure) =>
        IsSuccess ? onSuccess(Value!) : onFailure(Error!);
}

public record Error(string Code, string Message);
```

Usage in aggregate:
```csharp
public Result<Order> Submit()
{
    if (_lines.Count == 0)
        return Result<Order>.Failure(OrderErrors.EmptyOrder);
    Status = OrderStatus.Submitted;
    RaiseDomainEvent(new OrderSubmittedEvent(Id, Total));
    return Result<Order>.Success(this);
}
```

## Constraints

### MUST DO
- Keep domain layer free of infrastructure dependencies (no EF, no HTTP, no logging)
- Use Value Objects for concepts with no identity (Money, Address, Email)
- Enforce invariants inside the Aggregate — never outside
- Reference other Aggregates by ID only
- Use factory methods (`Create`, `From`) instead of public constructors for Aggregates
- Raise Domain Events for side effects that cross Aggregate boundaries
- Use `CancellationToken` on all async Repository methods

### MUST NOT DO
- Expose setters on Aggregate state (use behavior methods instead)
- Let Aggregates depend on repositories or services
- Create "God Aggregates" that contain everything
- Use Domain Events for intra-Aggregate communication
- Put business logic in Application Services — it belongs in the domain
- Use anemic domain models (entities as data bags with logic in services)

## Additional References

Load based on your task — **do not load all at once**:

- [references/building-blocks.md](references/building-blocks.md) — deep dive into Entity, Value Object, Aggregate patterns with edge cases
- [references/domain-events.md](references/domain-events.md) — event dispatching strategies, outbox pattern, integration events
- [references/patterns.md](references/patterns.md) — Result pattern, Specification, Strongly-typed IDs, Guard clauses
- [references/project-structure.md](references/project-structure.md) — solution layout, layer dependencies, project references

## Resources

- [Domain-Driven Design Reference (Eric Evans)](https://www.domainlanguage.com/ddd/reference/)
- [Implementing Domain-Driven Design (Vaughn Vernon)](https://kalele.io/books/)
- [Microsoft DDD Guidance](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/)
