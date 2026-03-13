---
name: java
description: Use when writing, modifying, or reviewing Java code - applies SOLID principles, clean code practices, minimal documentation, and pragmatic abstraction to create maintainable Java applications
---

# Java Development

## Overview

Write clean, maintainable Java code following SOLID principles and pragmatic practices. **No Javadoc on private methods.** Favor self-documenting code over comments.

## Core Principles

### Object-Oriented Design

- Apply SOLID principles appropriately
- Use encapsulation to hide implementation details
- Design clear class responsibilities
- **Favor composition over inheritance** for code reuse

### Pragmatic Abstraction

- Only introduce abstractions when they provide clear value
- Avoid premature generalization
- **Don't create interfaces or abstract classes unless multiple implementations exist or polymorphism is needed**
- Keep it simple until complexity is justified

## Clean Code Practices

### Documentation Rules

**NEVER add Javadoc to private methods or constructors**

Private methods are implementation details. If they need documentation, refactor for clarity instead.

**Javadoc on public APIs only when:**

- Complex algorithm or business logic
- Non-obvious behavior or side effects
- Important constraints or assumptions

**Don't document obvious methods:**

```java
// ❌ BAD
/**
 * Gets the customer count
 */
public int getCustomerCount() { return customers.size(); }

// ✅ GOOD - self-documenting, no comment needed
public int getCustomerCount() { return customers.size(); }
```

### Constants and Magic Values

- **Only extract constants if used in multiple places**
- Don't create constants for single-use values - inline them with clear context
- Use meaningful names that explain purpose, not just value

### Method Design

**Provide clean overloads for optional parameters:**

```java
// ✅ GOOD
public void process(Data data) {
    process(data, ProcessingOptions.DEFAULT);
}

public void process(Data data, ProcessingOptions options) {
    // implementation
}

// ❌ BAD - forcing clients to pass null
public void process(Data data, ProcessingOptions options) {
    if (options == null) options = ProcessingOptions.DEFAULT;
}
```

### Utility Methods vs Constants

**Don't create utility methods that always return the same value:**

```java
// ❌ BAD
private static String getDefaultFormat() {
    return "yyyy-MM-dd";
}

// ✅ GOOD
private static final String DEFAULT_FORMAT = "yyyy-MM-dd";
```

### Naming and Clarity

- Prefer clear, descriptive names over comments
- Variables and methods should be self-documenting
- Avoid cryptic abbreviations
- Write code that reads like prose

### Comments

Keep comments minimal. Use them only for:

- Complex algorithms or business logic
- Non-obvious decisions or workarounds
- Important constraints or assumptions

**Don't comment what code obviously does.**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Javadoc on private methods | Remove it. Refactor for clarity. |
| Documenting obvious getters/setters | Remove Javadoc. Code is self-documenting. |
| Forcing null parameters | Provide overloads with defaults. |
| Utility method returning constant | Use a constant field instead. |
| Inheritance for code reuse | Use composition instead. |
| Creating interfaces prematurely | Wait until multiple implementations exist. |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This private method is complex so I should document it" | If it's complex, refactor it into smaller, clearer methods. Don't document complexity. |
| "This helps IDE tooltips" | IDE tooltips are for public APIs. Private methods are implementation details. |
| "Just brief Javadoc won't hurt" | Any Javadoc on private methods violates clean code. No exceptions. |
| "This algorithm needs explanation" | Use self-documenting method names and clear variable names instead. |
| "Future maintainers will thank me" | Future maintainers want clear code, not documented unclear code. |
| "This getter has side effects so it needs docs" | If a getter has side effects, it shouldn't be named 'get'. Rename it. |

## Red Flags - Review Your Code If You

- Added Javadoc comment to any private method
- Documented a simple getter/setter
- Wrote comment explaining what code does (vs why)
- Created interface with only one implementation
- Used inheritance when composition would work
- Made clients pass null for optional parameters

## Code Review Checklist

Before finalizing Java code:

- [ ] No Javadoc on private methods/constructors
- [ ] Public method Javadoc adds real value (not obvious)
- [ ] Classes have single, clear responsibilities
- [ ] Composition used instead of inheritance where appropriate
- [ ] No unnecessary abstractions or premature generalizations
- [ ] Constants only extracted when used multiple times
- [ ] Public methods have clean interfaces with appropriate overloads
- [ ] Code is self-documenting with clear names
- [ ] Comments are minimal and add real value

## Examples

### Composition Over Inheritance

```java
// ✅ GOOD
public class EmailNotifier {
    private final MessageFormatter formatter;
    private final EmailSender sender;

    public EmailNotifier(MessageFormatter formatter, EmailSender sender) {
        this.formatter = formatter;
        this.sender = sender;
    }

    public void notify(User user, String message) {
        String formatted = formatter.format(message);
        sender.send(user.getEmail(), formatted);
    }
}
```

### Self-Documenting Code

```java
// ✅ GOOD - clear without comments
public boolean isEligibleForDiscount(Customer customer) {
    return customer.getOrderCount() >= 10
        && customer.getAccountAge().isAfter(oneYearAgo());
}

// ❌ BAD - needs comment to explain
public boolean check(Customer c) {
    // Check if customer has 10 orders and account older than 1 year
    return c.getOrderCount() >= 10 && c.getAccountAge().isAfter(oneYearAgo());
}
```
