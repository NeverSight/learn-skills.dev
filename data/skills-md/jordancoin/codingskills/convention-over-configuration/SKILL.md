---
name: convention-over-configuration
description: When organizing project structure, establishing patterns, or reducing configuration overhead. Use when the user says "how should I organize this," "what's the convention," "too much config," "project structure," "naming pattern," or "standardize this." For code-level structure, see separation-of-concerns.
metadata:
  version: 1.0.0
---

# Convention over Configuration

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Adopt sensible defaults and consistent patterns so that decisions are made once and applied everywhere. Reserve explicit configuration for the cases that genuinely need to differ from the default.

## Why This Matters in Production

Every configuration option is a decision that someone must make, document, understand, and maintain. Misconfigured systems are a top cause of production incidents — wrong environment variables, typos in YAML, conflicting settings between services.

Convention-driven systems are predictable. A new team member can look at one module and know how every other module works. There's no "well, this service does it differently because someone configured it that way 18 months ago."

Configuration should be the exception, not the default. When everything is configurable, nothing is standardized.

## Rules

1. **Establish project conventions early and document them.** File structure, naming patterns, error handling style, test organization — decide once and follow everywhere. Put these in a living document (like a CLAUDE.md or CONTRIBUTING.md).
2. **Use framework conventions as-is.** If your framework puts routes in `routes/`, models in `models/`, and tests in `tests/` — follow that. Don't invent a custom layout unless the framework's conventions genuinely don't fit.
3. **Name things predictably.** If the users table has a handler called `users.rs`, the tests should be in `users_test.rs`, the migration should reference `users`, and the API endpoint should be `/users`. Predictable naming is a convention that eliminates searching.
4. **Default to the common case.** Configuration options should have sane defaults that work for 90% of use cases. Only require explicit configuration for the 10% that genuinely varies.
5. **Minimize environment-specific config.** The gap between dev, staging, and production should be as small as possible. Environment-specific configuration is a leading source of "works on my machine" bugs.
6. **Treat configuration as code.** Config files should be version-controlled, reviewed, and tested like code. If changing a config value could cause an outage, it deserves the same scrutiny as a code change.

## Anti-Patterns

- **Config-driven architecture:** Systems where behavior is determined by hundreds of knobs in YAML files that no one fully understands
- **Inconsistent project structure:** Each module organized differently because "the developer preferred it that way"
- **Reinventing the wheel:** Custom build scripts, custom test runners, custom deployment tools when standard ones exist and are sufficient
- **Feature flags for everything:** Wrapping every decision in a feature flag "so we can change it later" when the decision is already made
- **Undocumented conventions:** Patterns that exist in the codebase but aren't written down, so new team members violate them unknowingly

## Examples

```
-- Over-configured: every handler specifies its own middleware stack
app.route("/users", handler=users, middleware=[auth, logging, rate_limit, cors])
app.route("/orders", handler=orders, middleware=[auth, logging, rate_limit, cors])
app.route("/products", handler=products, middleware=[logging, cors])  # oops, forgot auth

-- Convention: default middleware applied globally, exceptions are explicit
app.use([auth, logging, rate_limit, cors])   # convention: all routes get this
app.route("/users", handler=users)
app.route("/orders", handler=orders)
app.route("/health", handler=health, skip=[auth])  # explicit exception
```

```
-- Over-configured: every test specifies database setup
def test_create_user():
    db = connect("postgres://localhost:5432/test")
    db.migrate()
    db.seed("users.sql")
    ...

-- Convention: test framework handles setup, tests just test
def test_create_user(db):   # db fixture provided by convention
    user = create_user(db, name="Alice")
    assert user.name == "Alice"
```

## Boundaries

- **Convention does not mean rigidity.** Conventions should evolve as the team and project grow. Review and update them periodically.
- **Some things must be configured.** Database URLs, API keys, feature flags for gradual rollouts, and environment-specific settings legitimately need configuration. The principle is about minimizing unnecessary configuration, not eliminating all of it.
- **Conventions must be discoverable.** A convention that exists only in one developer's head is not a convention — it's a trap. Write them down.
- **Tension with flexibility:** In libraries and frameworks meant for diverse use cases, more configuration is appropriate. In application code, less is better.

## Code Review Checklist

- [ ] Does this change follow the project's established patterns and conventions?
- [ ] If it introduces a new pattern, is that pattern documented and justified?
- [ ] Are there configuration options that could be replaced by sensible defaults?
- [ ] Is the file/module structure consistent with the rest of the project?
- [ ] Could a new team member predict this code's location and structure based on the project's conventions?

## Related Skills

- **boy-scout-rule**: For maintaining conventions incrementally
- **separation-of-concerns**: For the structural conventions themselves
- **kiss**: When conventions should default to the simpler option
