---
name: dotnet-best-practices
description: Comprehensive .NET development best practices from industry experts. Use when writing, reviewing, or architecting .NET applications. Triggers on Clean Architecture, CQRS, Entity Framework Core optimization, performance tuning, API design, async patterns, or production deployment. Provides contextual guidance based on project size—from simple APIs to enterprise systems.
---

# .NET Best Practices
Production-grade .NET development guidance from top thought leaders

## When to Apply
Reference these guidelines when:
- Architecting new .NET projects (choosing between Simple/Clean/Modular patterns)
- Writing or reviewing C# code for performance
- Implementing CQRS or mediator patterns
- Optimizing Entity Framework Core queries
- Designing RESTful APIs
- Debugging production performance issues
- Upgrading to .NET 8/9 features

## Architecture Decision Matrix
Choose architecture based on **project complexity** and **team size**:

| Project Type | Team Size | Recommended Architecture | Reference |
|--------------|-----------|-------------------------|-----------|
| Simple API/MVP | 1-2 devs | Simple Layered | [arch-simple.md](references/arch-simple.md) |
| Rapid development | 1-4 devs | Vertical Slice | [arch-vertical-slice.md](references/arch-vertical-slice.md) |
| Medium complexity | 2-5 devs | Clean Architecture | [arch-clean.md](references/arch-clean.md) |
| Large/Enterprise | 5+ devs | Modular Monolith | [arch-modular-monolith.md](references/arch-modular-monolith.md) |
| Scaling required | 10+ devs | Microservices (migrate later) | Start with Modular Monolith |

> [!IMPORTANT]
> **Start simple, evolve when pain points emerge.** Over-engineering kills velocity. A well-structured simple API can handle most business needs.

## Rule Categories by Priority
| Priority | Category | Impact | Prefix | Reference |
|----------|----------|--------|--------|-----------|
| 1 | Architecture Selection | CRITICAL | `arch-` | [Project Sizing](references/arch-project-sizing.md) |
| 2 | Performance & Memory | CRITICAL | `perf-` | [Memory](references/perf-memory.md), [Async](references/perf-async.md) |
| 3 | Distributed Systems | CRITICAL | `dist-` | [Distributed Systems](references/distributed-systems.md) |
| 4 | Database & EF Core | HIGH | `ef-` | [EF Core](references/ef-core-performance.md) |
| 5 | CQRS & Mediator | HIGH | `cqrs-` | [CQRS Patterns](references/cqrs-patterns.md) |
| 6 | API Design | MEDIUM-HIGH | `api-` | [API Design](references/api-design.md) |
| 7 | Error & Logging | MEDIUM | `error-` | [Pitfalls](references/production-pitfalls.md) |
| 8 | Testing | MEDIUM | `test-` | [Testing](references/testing-strategies.md) |
| 9 | Modern .NET | MEDIUM | `dotnet-` | [.NET 8/9](references/dotnet-8-9-features.md) |

---

## Quick Reference
### 1. Architecture Selection (CRITICAL)

**Simple API Pattern** – For MVPs, internal tools, small teams:
```csharp
// ✅ Simple: Controllers → Services → DbContext
public class ProductsController : ControllerBase
{
    private readonly ProductService _service;
    public ProductsController(ProductService service) => _service = service;
    
    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> Get(int id) 
        => Ok(await _service.GetByIdAsync(id));
}
```

**Clean Architecture** – For complex domain logic, medium teams:
```
Domain → Application → Infrastructure → Presentation
         (no dependencies on outer layers)
```

**Modular Monolith** – For enterprise, large teams preparing for microservices:
```
Each module = independent bounded context with own:
- Domain layer
- Application layer  
- Infrastructure (can share DB initially)
- Public API (contracts for inter-module communication)
```

### 2. Performance & Memory (CRITICAL)
| Rule | Impact | Quick Fix |
|------|--------|-----------|
| `perf-span` | CRITICAL | Use `Span<T>` for slicing without allocation |
| `perf-arraypool` | HIGH | Use `ArrayPool<T>.Shared` for temp buffers |
| `perf-valuetask` | HIGH | Use `ValueTask` in hot paths when result often cached |
| `perf-struct` | MEDIUM | Use readonly struct for small, short-lived data |
| `perf-stringbuilder` | MEDIUM | Use StringBuilder for 4+ concatenations |

```csharp
// ❌ BAD: Allocates new array for each slice
var subset = array.Skip(10).Take(20).ToArray();

// ✅ GOOD: Zero-allocation slice
ReadOnlySpan<int> subset = array.AsSpan(10, 20);
```

```csharp
// ❌ BAD: New array allocation each call
public byte[] GetBuffer() => new byte[4096];

// ✅ GOOD: Rent from pool, return when done
public byte[] GetBuffer() => ArrayPool<byte>.Shared.Rent(4096);
// Remember: ArrayPool<byte>.Shared.Return(buffer);
```

### 3. Entity Framework Core (HIGH)
| Rule | Impact | Quick Fix |
|------|--------|-----------|
| `ef-notracking` | CRITICAL | Use `.AsNoTracking()` for read-only queries |
| `ef-projection` | CRITICAL | Use `.Select()` to fetch only needed columns |
| `ef-n+1` | CRITICAL | Use `.Include()` or projection to prevent N+1 |
| `ef-batch` | HIGH | Use `AddRange()`, call `SaveChanges()` once |
| `ef-compiled` | MEDIUM | Use compiled queries for hot paths |

```csharp
// ❌ BAD: Tracks entities + fetches all columns + N+1
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
    Console.WriteLine(order.Customer.Name); // N+1!

// ✅ GOOD: No tracking, projection, eager load
var orders = await _context.Orders
    .AsNoTracking()
    .Include(o => o.Customer)
    .Select(o => new OrderDto(o.Id, o.Customer.Name, o.Total))
    .ToListAsync();
```

### 4. CQRS & Mediator (HIGH)
| Rule | Impact | Description |
|------|--------|-------------|
| `cqrs-separate` | HIGH | Commands mutate state, Queries read data |
| `cqrs-dapper-query` | HIGH | Use Dapper for complex read queries |
| `cqrs-ef-command` | MEDIUM | Use EF Core for commands (change tracking) |
| `cqrs-no-mediatr` | LOW | Consider custom interfaces over MediatR for simplicity |

```csharp
// Command: Uses EF Core for rich domain model
public class CreateOrderHandler : ICommandHandler<CreateOrderCommand, Guid>
{
    private readonly AppDbContext _context;
    
    public async Task<Guid> Handle(CreateOrderCommand cmd, CancellationToken ct)
    {
        var order = Order.Create(cmd.CustomerId, cmd.Items); // Domain logic
        _context.Orders.Add(order);
        await _context.SaveChangesAsync(ct);
        return order.Id;
    }
}

// Query: Uses Dapper for performance
public class GetOrdersHandler : IQueryHandler<GetOrdersQuery, IEnumerable<OrderDto>>
{
    private readonly ISqlConnectionFactory _sql;
    
    public async Task<IEnumerable<OrderDto>> Handle(GetOrdersQuery query, CancellationToken ct)
    {
        using var conn = _sql.Create();
        return await conn.QueryAsync<OrderDto>(
            "SELECT Id, CustomerName, Total FROM Orders WHERE CustomerId = @Id",
            new { query.CustomerId });
    }
}
```

### 5. API Design (MEDIUM-HIGH)
| Rule | Impact | Quick Fix |
|------|--------|-----------|
| `api-versioning` | HIGH | Use URL versioning: `/api/v1/products` |
| `api-pagination` | HIGH | Always paginate list endpoints |
| `api-problem-details` | MEDIUM | Return RFC 7807 ProblemDetails for errors |
| `api-async` | MEDIUM | All I/O endpoints must be async |

```csharp
// ✅ GOOD: Versioned, paginated, proper response types
[ApiController]
[Route("api/v1/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    [ProducesResponseType<PagedResult<ProductDto>>(200)]
    public async Task<ActionResult<PagedResult<ProductDto>>> GetAll(
        [FromQuery] int page = 1, 
        [FromQuery] int pageSize = 20)
    {
        var result = await _service.GetPagedAsync(page, pageSize);
        return Ok(result);
    }
    
    [HttpGet("{id:guid}")]
    [ProducesResponseType<ProductDto>(200)]
    [ProducesResponseType<ProblemDetails>(404)]
    public async Task<ActionResult<ProductDto>> GetById(Guid id)
    {
        var product = await _service.GetByIdAsync(id);
        return product is null ? NotFound() : Ok(product);
    }
}
```

### 6. Async/Await Patterns (MEDIUM)
| Rule | Impact | Quick Fix |
|------|--------|-----------|
| `async-all-way` | CRITICAL | Never mix sync and async (causes deadlocks) |
| `async-no-result` | CRITICAL | Never use `.Result` or `.Wait()` |
| `async-configureawait` | MEDIUM | Use `ConfigureAwait(false)` in libraries |
| `async-cancellation` | MEDIUM | Always accept and use `CancellationToken` |

```csharp
// ❌ BAD: Deadlock risk in ASP.NET
public string GetData()
{
    return GetDataAsync().Result; // DEADLOCK!
}

// ✅ GOOD: Async all the way
public async Task<string> GetDataAsync(CancellationToken ct = default)
{
    var data = await _httpClient.GetStringAsync(url, ct);
    return data;
}
```

### 7. Common Production Pitfalls
| Pitfall | Impact | Solution |
|---------|--------|----------|
| HttpClient per-request | CRITICAL | Use `IHttpClientFactory` |
| Catching `Exception` | HIGH | Catch specific exceptions |
| Logging sensitive data | HIGH | Use structured logging, sanitize |
| DateTime.Now | MEDIUM | Use `DateTime.UtcNow` or `TimeProvider` |
| String concatenation in loops | MEDIUM | Use `StringBuilder` |

```csharp
// ❌ BAD: Port exhaustion
public class MyService
{
    public async Task CallApi()
    {
        using var client = new HttpClient(); // DON'T!
        await client.GetAsync("...");
    }
}

// ✅ GOOD: Factory-managed lifecycle
public class MyService
{
    private readonly IHttpClientFactory _factory;
    
    public async Task CallApi()
    {
        var client = _factory.CreateClient();
        await client.GetAsync("...");
    }
}
```

---

## Searching References
```bash
# Find patterns by keyword
grep -l "ef core" references/
grep -l "async" references/
grep -l "memory" references/
grep -l "cqrs" references/
```

## Problem → Reference Mapping

| Problem | Start With |
|---------|------------|
| Choosing architecture | [arch-project-sizing.md](references/arch-project-sizing.md) |
| Simple API needed | [arch-simple.md](references/arch-simple.md) |
| Rapid dev / feature-focused | [arch-vertical-slice.md](references/arch-vertical-slice.md) |
| Complex domain logic | [arch-clean.md](references/arch-clean.md) |
| Large team, scaling | [arch-modular-monolith.md](references/arch-modular-monolith.md) |
| Slow queries | [ef-core-performance.md](references/ef-core-performance.md) |
| Memory issues | [perf-memory.md](references/perf-memory.md) |
| Deadlocks/async bugs | [perf-async.md](references/perf-async.md) |
| API design questions | [api-design.md](references/api-design.md) |
| Implementing CQRS | [cqrs-patterns.md](references/cqrs-patterns.md) |
| Implementing CQRS | [cqrs-patterns.md](references/cqrs-patterns.md) |
| Event Sourcing | [event-sourcing-wolverine.md](references/event-sourcing-wolverine.md) |
| Distributed failures | [distributed-systems.md](references/distributed-systems.md) |
| .NET 8/9 migration | [dotnet-8-9-features.md](references/dotnet-8-9-features.md) |
| Test strategy | [testing-strategies.md](references/testing-strategies.md) |
| Production bugs | [production-pitfalls.md](references/production-pitfalls.md) |
| Security issues | [production-pitfalls-security.md](references/production-pitfalls-security.md) |
| Middleware/DI issues | [aspnet-core-internals.md](references/aspnet-core-internals.md) |

## Attribution

Based on teachings from **Original Thinkers**:
- **David Fowler** - Async/Await, Concurrency, ASP.NET Core (Microsoft)
- **Jeremy D. Miller** - Wolverine, Marten, Vertical Slice, Event Sourcing
- **Julie Lerman** - Entity Framework Core, DDD
- **Nick Chapsas** - C# Performance, Span<T>, Benchmarking
- **Andrew Lock** - ASP.NET Core Internals, Middleware, DI
- **Milan Jovanovic** - Clean Architecture, CQRS, Functional Core
- **Julio Casal** - Modular Monoliths, Microservices Transition
- **Gui Ferreira** - Memory Management, Struct Layout
- **Mukesh Murugan** - API Design, Idempotency, Global Errors
- **Dr. Milan Milanovic** - Distributed Systems, Resilience Patterns
