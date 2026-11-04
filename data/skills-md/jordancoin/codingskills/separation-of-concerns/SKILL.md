---
name: separation-of-concerns
description: When structuring code into layers and modules with clear boundaries. Use when the user says "this function does too much," "fat controller," "mixed concerns," "where should this logic go," or "separate the layers." For interface-level design, see solid. For object-level coupling, see law-of-demeter.
metadata:
  version: 1.0.0
---

# SoC — Separation of Concerns

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Each module, layer, or component in a system should address a single concern. A concern is a distinct aspect of functionality — data access, business rules, presentation, authentication, error handling, logging.

## Why This Matters in Production

When concerns are entangled, changes become dangerous. Modifying the database schema shouldn't break the UI. Changing the logging format shouldn't affect business logic. Adding authentication shouldn't require rewriting every handler.

Separated concerns mean:
- **Isolated failures.** A bug in rendering doesn't corrupt data. A database timeout doesn't crash the UI.
- **Independent testing.** Business rules can be tested without a database. UI can be tested without a backend.
- **Parallel development.** Different team members can work on different layers without merge conflicts.
- **Targeted debugging.** When something breaks, the problem is localized to one layer, not spread across the whole stack.

## Rules

1. **Separate policy from mechanism.** Business rules (what to do) should be independent of infrastructure (how to do it). A pricing function shouldn't know whether it's called from an HTTP handler or a background job.
2. **Separate data access from business logic.** Queries and mutations go in a data layer. Business rules go in a domain layer. Handlers/controllers wire them together.
3. **Separate input parsing from processing.** Validate and parse inputs at the boundary. Internal functions should receive well-typed, validated data — not raw strings from the wire.
4. **Separate orchestration from computation.** A function that coordinates multiple steps should not also contain the implementation of those steps. Keep coordinators thin.
5. **Separate cross-cutting concerns with dedicated mechanisms.** Authentication, logging, rate limiting, and error handling should be handled by middleware, decorators, or interceptors — not sprinkled into every handler.

## Anti-Patterns

- **Fat handlers/controllers:** HTTP handlers that parse input, validate, query the database, apply business logic, format output, and handle errors all in one function
- **Business logic in the database:** Complex conditional logic in SQL queries or stored procedures that should live in application code where it can be tested and versioned
- **Infrastructure in domain code:** Business rule functions that directly import HTTP clients, database drivers, or filesystem modules
- **Presentation in data models:** Database models that contain HTML formatting, JSON serialization preferences, or UI-specific fields
- **Logging in business logic:** Core algorithms littered with log statements that obscure the actual logic

## Examples

```
-- Concerns entangled
def create_order(request):
    # parsing
    data = json.parse(request.body)
    # validation
    if not data.items:
        return http_response(400, "No items")
    # business logic
    total = sum(item.price * item.qty for item in data.items)
    tax = total * 0.08
    # data access
    db.execute("INSERT INTO orders ...")
    # side effects
    email_service.send(user.email, "Order confirmed")
    logger.info("Order created")
    # presentation
    return http_response(201, {"order_id": id, "total": total + tax})

-- Concerns separated
def create_order_handler(request):            # orchestration
    order_input = parse_order_request(request) # parsing + validation
    order = OrderService.create(order_input)   # business logic
    OrderRepo.save(order)                      # data access
    notify_order_created(order)                # side effects
    return format_order_response(order)        # presentation
```

## Boundaries

- **Separation does not mean maximum layers.** Having 7 layers for a CRUD endpoint is worse than having the logic inline. The goal is meaningful separation along natural fault lines, not bureaucratic layering.
- **Some coupling is natural.** The orchestration layer must know about both the domain layer and the data layer — that's its job. The goal is that domain and data don't know about each other.
- **Microservice boundaries are extreme SoC.** They bring network overhead, distributed systems complexity, and operational cost. Only split across services when the organizational or scaling benefits justify it.
- **Tension with KISS:** Over-separating simple logic adds indirection without benefit. A 5-line script doesn't need a 3-layer architecture.

## Code Review Checklist

- [ ] Does each function/module address a single concern?
- [ ] Can the business logic be tested without infrastructure (database, network, filesystem)?
- [ ] Are cross-cutting concerns (auth, logging, error handling) applied uniformly via middleware rather than per-handler?
- [ ] If the database changes, does business logic need to change? (It shouldn't.)
- [ ] If the API format changes, does business logic need to change? (It shouldn't.)

## Related Skills

- **solid**: For interface-level design within separated layers
- **kiss**: When separation is adding more indirection than clarity
- **law-of-demeter**: For keeping communication between layers clean
