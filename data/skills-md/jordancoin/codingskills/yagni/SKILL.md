---
name: yagni
description: When writing or reviewing code to prevent over-engineering and speculative features. Use when the user says "is this over-engineered," "do we need this," "should I add," "future-proof," or "just in case." For simplicity concerns, see kiss. For abstraction design, see solid.
metadata:
  version: 1.0.0
---

# YAGNI — You Aren't Gonna Need It

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Do not build for hypothetical future requirements. Build what is needed now, and refactor when actual requirements emerge.

## Why This Matters in Production

Speculative code is the #1 source of accidental complexity. Every abstraction, configuration option, or extension point you add "just in case" has a real cost: it must be understood, tested, maintained, and debugged. Unused code paths are the most dangerous — they rot silently, give false confidence in test coverage, and create surface area for bugs.

Premature generalization is worse than duplication. Duplication is obvious and easy to fix later. A wrong abstraction is painful to undo because other code grows to depend on it.

## Rules

1. **Solve the problem in front of you.** If you have one use case, write code for one use case. Not two. Not "what if later."
2. **Three strikes, then abstract.** The first time you write something, just write it. The second time, note the duplication. The third time, extract the pattern — now you have enough data to design the right abstraction.
3. **Delete speculative code paths.** If a feature flag has never been toggled, a configuration option has never been changed, or a parameter has never been passed anything other than the default — remove it.
4. **Don't build plugin systems for one plugin.** Interfaces, registries, and extension points are justified only when you have multiple concrete implementations today.
5. **Prototype when uncertain.** If you aren't sure whether something will be needed, spike it in a branch. Don't merge speculative infrastructure into main.

## Anti-Patterns

- Adding parameters "for flexibility" that only ever receive one value
- Building an event system when you have two components that could just call each other
- Creating abstract base classes with a single concrete implementation
- Writing configuration files for values that never change
- Adding database columns "we might need later"
- Implementing caching before measuring whether there's a performance problem
- Building a microservice when a function call would suffice

## Examples

```
-- YAGNI violation: generic "processor" for one operation
class DataProcessor:
    def __init__(self, strategy, validator, transformer, output_format):
        self.strategy = strategy
        ...

-- Actually needed: one function
def process_csv_upload(file):
    rows = parse_csv(file)
    validate_rows(rows)
    save_to_db(rows)
```

```
-- YAGNI violation: premature abstraction
interface INotificationService
class EmailNotificationService implements INotificationService
class SMSNotificationService implements INotificationService  // "we might need this"
class PushNotificationService implements INotificationService  // "just in case"

-- Actually needed: you only send emails today
def send_welcome_email(user):
    mailer.send(to=user.email, template="welcome")
```

## Boundaries

- **YAGNI does not mean ignore architecture.** Good structure (separation of concerns, clear module boundaries) is not speculative — it makes future changes cheaper. YAGNI targets unused features, not good design.
- **YAGNI does not mean skip error handling.** Handling known failure modes (network errors, invalid input, disk full) is not speculative — those things will happen in production.
- **YAGNI does not mean avoid extensibility at zero cost.** If making code extensible costs nothing (e.g., using a map instead of a switch statement), do it. YAGNI targets costly abstractions.
- **Tension with DRY:** Sometimes YAGNI wins — it's better to have two similar-but-not-identical functions than to prematurely unify them behind the wrong abstraction.

## Code Review Checklist

- [ ] Does this change introduce any code paths that aren't exercised by current requirements?
- [ ] Are there parameters, configs, or options that only have one possible value today?
- [ ] Could this abstraction be replaced by a direct implementation without loss of functionality?
- [ ] Is this interface/trait/protocol justified by multiple concrete implementations?
- [ ] Would a simpler approach work for the current scope?

## Related Skills

- **kiss**: When the issue is complexity rather than speculation
- **solid**: When designing abstractions that are justified
- **dry**: When deciding whether to extract a pattern (YAGNI says wait for 3 occurrences)
