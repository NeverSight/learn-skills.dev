---
name: law-of-demeter
description: When reviewing code for excessive coupling and deep object chains. Use when the user says "too coupled," "train wreck," "chained calls," "feature envy," "mocking is painful," or "this reaches too deep." For broader structural coupling, see solid.
metadata:
  version: 1.0.0
---

# LoD — Law of Demeter (Principle of Least Knowledge)

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

A component should only talk to its immediate collaborators. Don't reach through an object to access its internals, its children's internals, or anything deeper.

More precisely: a method should only call methods on (1) itself, (2) its own fields, (3) its parameters, (4) objects it creates, and (5) global/singleton services.

## Why This Matters in Production

Every chain of access (`order.customer.address.city`) is a chain of coupling. If any link in that chain changes — the customer model gets restructured, address becomes optional, city moves to a sub-object — every caller breaks.

LoD violations create **fragile systems** where a seemingly small refactor triggers cascading failures across unrelated code. They also make testing painful: to test a function that reaches through 4 layers, you must mock all 4 layers.

In production, LoD violations are a leading cause of `NullPointerException` and `undefined is not an object` errors. Each `.` in a chain is a potential null/undefined dereference point.

## Rules

1. **Don't chain through objects.** If you need data from deep inside a structure, ask the immediate owner to provide it. `order.shipping_city()` not `order.customer.address.city`.
2. **Tell, don't ask.** Instead of reaching into an object to get data and make a decision, tell the object what you need done. Let it use its own internals.
3. **Wrap external APIs at the boundary.** Third-party SDKs and API responses often expose deep structures. Create a thin wrapper that exposes only what your code needs, in the shape your code needs.
4. **Flatten data for consumers.** When passing data across boundaries (to templates, to frontends, to other services), flatten the nested structure into a purpose-built shape rather than exposing your internal model.
5. **Limit parameter knowledge.** A function that receives an object should only use the fields it directly needs. If it only needs the user's email, accept the email — not the entire user object.

## Anti-Patterns

- **Train wrecks:** `app.config.database.connection.pool.max_size` — any change to the config structure breaks this
- **Feature envy:** A function that uses more data from another object than from its own — it probably belongs on that other object
- **Transparent wrappers:** Objects that expose their internals via getters, making every consumer dependent on the internal structure
- **Deep mocking in tests:** If you need to mock `order.customer.address` just to test order processing, the code is reaching too deep

## Examples

```
-- LoD violation: reaching through the chain
def get_shipping_label(order):
    name = order.customer.name
    street = order.customer.address.street
    city = order.customer.address.city
    zip = order.customer.address.zip_code
    return format_label(name, street, city, zip)

-- LoD-compliant: ask the order for what you need
def get_shipping_label(order):
    info = order.shipping_info()  # order knows how to assemble this
    return format_label(info)
```

```
-- LoD violation: reaching into config internals
timeout = app.config.services.payment.timeout_ms

-- LoD-compliant: config provides what you need
timeout = config.payment_timeout()
```

## Boundaries

- **LoD does not apply to pure data structures.** Accessing fields of a DTO, dictionary, or value object is fine — these exist specifically to carry data. LoD applies to objects with behavior.
- **LoD does not mean wrap everything.** Don't create a wrapper method for every single access pattern. Apply it at meaningful boundaries where the internal structure is likely to change.
- **Fluent/builder APIs are an exception.** Chaining like `query.select("name").where(active=true).limit(10)` is not a LoD violation because each method returns `self` — you're talking to the same object.
- **Tension with KISS:** Sometimes a direct chain is clearer than an intermediary method. Apply LoD where the coupling risk is real (across module boundaries, through unstable structures), not within tightly-coupled internals.

## Code Review Checklist

- [ ] Are there chains of 3+ property/method accesses reaching through object boundaries?
- [ ] Does any function access more internals of another object than its own? (Feature envy)
- [ ] Are external API responses wrapped at the boundary rather than leaked into business logic?
- [ ] Can the internal structure of passed objects change without breaking this code?
- [ ] Are tests forced to build deep object graphs just to exercise simple logic?

## Related Skills

- **solid**: For dependency inversion and interface segregation (structural decoupling)
- **separation-of-concerns**: For keeping layers independent
- **kiss**: When wrapping becomes more complex than the chain
