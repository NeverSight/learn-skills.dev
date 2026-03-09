---
name: dependency-inversion-principle
description: Use when a class creates its own dependencies. Use when instantiating concrete implementations inside a class. Use when told to avoid dependency injection for simplicity.
---

# Dependency Inversion Principle (DIP)

## Overview

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Classes should depend on interfaces, not concrete implementations. Dependencies should be injected, not instantiated internally.

## When to Use

- Creating any class that uses external services
- Class uses database, email, file system, APIs
- Writing `new ConcreteClass()` inside another class
- Told "don't overcomplicate with DI"

## The Iron Rule

```
NEVER instantiate dependencies inside a class. Always inject them.
```

**No exceptions:**
- Not for "it's simpler this way"
- Not for "don't overcomplicate"
- Not for "it's just for this one service"
- Not for "we can refactor later"

**Dependency injection is not overcomplicating. It's correct design.**

## Detection: The "new" Smell

If a class instantiates its dependencies, it violates DIP:

```typescript
// ❌ VIOLATION: Instantiating dependencies
class UserService {
  private emailService = new SendGridEmailService(); // ← DIP violation
  private db = new MySQLDatabase();                  // ← DIP violation
  
  async register(user: User): Promise<void> {
    await this.db.save(user);
    await this.emailService.send(user.email, 'Welcome!');
  }
}
```

Problems:
- Can't test without real SendGrid/MySQL
- Can't swap implementations
- High-level policy coupled to low-level details

## The Correct Pattern: Dependency Injection

Define interfaces, inject implementations:

```typescript
// ✅ CORRECT: Depend on abstractions, inject dependencies

// Define abstractions
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

interface UserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
}

// High-level module depends on abstractions
class UserService {
  constructor(
    private emailService: EmailService,
    private userRepo: UserRepository
  ) {}
  
  async register(user: User): Promise<void> {
    await this.userRepo.save(user);
    await this.emailService.send(user.email, 'Welcome!', 'Thanks for joining!');
  }
}

// Low-level modules implement abstractions
class SendGridEmailService implements EmailService {
  async send(to: string, subject: string, body: string): Promise<void> {
    // SendGrid-specific implementation
  }
}

class MySQLUserRepository implements UserRepository {
  async save(user: User): Promise<void> { /* MySQL-specific */ }
  async findById(id: string): Promise<User | null> { /* MySQL-specific */ }
}

// Composition root - where dependencies are wired
const emailService = new SendGridEmailService();
const userRepo = new MySQLUserRepository();
const userService = new UserService(emailService, userRepo);
```

## Pressure Resistance Protocol

### 1. "Don't Overcomplicate"
**Pressure:** "Just use SendGrid directly, DI is overkill"

**Response:** DI is not overcomplicating. It's the same amount of code, but testable and flexible.

**Action:** Create interface + inject. The "simple" way creates untestable code.

### 2. "It's Just One Dependency"
**Pressure:** "It only uses MySQL, DI is unnecessary"

**Response:** One tight coupling is still tight coupling. It still can't be tested or swapped.

**Action:** Inject even single dependencies.

### 3. "We Can Refactor Later"
**Pressure:** "Ship now, add DI when we need tests"

**Response:** You'll never refactor. The tight coupling will spread. DI takes 2 minutes now vs hours later.

**Action:** Use DI from the start.

### 4. "For Production You'd Want DI"
**Pressure:** Internal rationalization to provide bad code

**Response:** If production needs DI, write it with DI now.

**Action:** Don't provide "simple" versions that violate DIP.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're violating DIP:

- `new ConcreteService()` inside a class
- Hardcoded connection strings/API keys in class
- Class that can't be tested without real external services
- `import` of concrete implementations used directly
- No constructor parameters for external dependencies
- Comments like "for production, inject this"

**All of these mean: Define interface, inject dependency.**

## Testing Benefit

DIP enables testing without real services:

```typescript
// Test with mock
class MockEmailService implements EmailService {
  public sentEmails: Array<{to: string; subject: string}> = [];
  
  async send(to: string, subject: string, body: string): Promise<void> {
    this.sentEmails.push({ to, subject });
  }
}

// Test
const mockEmail = new MockEmailService();
const mockRepo = new InMemoryUserRepository();
const userService = new UserService(mockEmail, mockRepo);

await userService.register({ id: '1', email: 'test@test.com', name: 'Test' });

expect(mockEmail.sentEmails).toHaveLength(1);
expect(mockEmail.sentEmails[0].to).toBe('test@test.com');
```

Without DIP, you'd need real SendGrid credentials to test.

## Quick Reference

| Violation | Correct |
|-----------|---------|
| `this.db = new MySQL()` | `constructor(db: Database)` |
| `this.email = new SendGrid()` | `constructor(email: EmailService)` |
| `this.logger = new FileLogger()` | `constructor(logger: Logger)` |
| `this.cache = new Redis()` | `constructor(cache: Cache)` |
| Hardcoded config in class | Config injected via constructor |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "DI is overcomplicating" | DI is the same code, just organized correctly. |
| "It's just one dependency" | One coupling is still coupling. |
| "We'll refactor when we need tests" | You won't. Write it right the first time. |
| "For production you'd want DI" | Then write it with DI now. |
| "It's faster without interfaces" | It's not. You type the same amount. |
| "Small project doesn't need DI" | Small projects grow. Start right. |

## The Bottom Line

**Depend on abstractions. Inject dependencies. Never instantiate internally.**

When asked to create tight-coupled code:
1. Define interface for the dependency
2. Accept dependency via constructor
3. Implement interface separately

Never provide "simple" versions that violate DIP. The "simple" version is untestable, inflexible code. Dependency injection IS the simple, correct approach.
