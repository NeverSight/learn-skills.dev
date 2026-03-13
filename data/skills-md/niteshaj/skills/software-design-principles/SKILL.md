---
name: software-design-principles
description: Guidelines that help developers design maintainable, scalable, reusable, and loosely coupled software systems. Use when the user asks about design principles, clean code, refactoring, code structure, SOLID, DRY, dependencies, or maintaining software systems.
metadata:
  author: https://github.com/niteshaj
  version: "1.0.0"
  domain: language
  triggers:  Java, Spring Boot, microservices, design patterns, code review, refactoring, clean code, SOLID, DRY, KISS, LoD, composition over inheritance, separation of concerns, high cohesion, low coupling, fail fast, immutability
  role: software architect
  scope: implementation
  output-format: code
---

# Software Design Principles

This skill helps the agent guide a user through software design principles—guidelines for creating software systems that are maintainable, scalable, reusable, and loosely coupled. Apply the principles below when discussing design, reviewing code, or suggesting improvements.

## Instructions

When this skill is invoked:

1. **For design discussions or questions** — Use the principles in this document (SOLID, DRY, KISS, etc.) to explain concepts, compare bad vs better examples, and suggest improvements.
2. **For design/code review output** — Use **Template A** when there are findings (critical issues or suggestions); use **Template B** when there are no issues. Follow the exact structure and section headings defined in the templates.
3. **When suggesting refactors** — Reference the relevant principle by name and point to the "What it achieves" and examples in this skill.

## When to Use

- Design principles
- Clean code
- Refactoring a software system
- Suggesting improvements
- Structuring your code
- Managing class dependencies
- Maintaining a software system
- Reviewing code

---

## SOLID Principles

**SOLID** is the most widely known object-oriented design principle set.

### What SOLID Achieves (Overall)

- **Maintainability** — Changes are localized; fewer side effects.
- **Low coupling** — Modules depend on abstractions, not concrete implementations.
- **High cohesion** — Each class has a focused, single purpose.
- **Testability** — Dependencies can be mocked or stubbed.
- **Extensibility** — New behavior added via new code, not by modifying existing code.

---

### S – Single Responsibility Principle (SRP)

**Definition:** A class should have **only one reason to change**.

**What it achieves (agent context):**

- **Maintainability** — When reviewing code, if a class handles persistence, validation, and notification, suggest splitting so each has one responsibility.
- **Clear responsibilities** — Name classes by their single concern (e.g. `UserPersistenceService`, `EmailNotificationService`).
- **Easier testing** — One responsibility per class means focused unit tests and simpler mocks.
- **Inference:** If you see multiple unrelated methods (e.g. save + send email + log), recommend extracting separate classes.

**Example**

Bad design (one class, multiple reasons to change):

```java
class UserService {
    void saveUser(User user) { /* DB */ }
    void sendEmail(User user) { /* SMTP */ }
    void validateUser(User user) { /* rules */ }
}
```

Better design (one responsibility per class):

```java
class UserRepository {
    void saveUser(User user) { /* DB only */ }
}

class EmailService {
    void sendEmail(User user) { /* SMTP only */ }
}

class UserValidator {
    boolean isValid(User user) { /* validation only */ }
}
```

---

### O – Open/Closed Principle (OCP)

**Definition:** Software entities should be **open for extension but closed for modification**.

**What it achieves (agent context):**

- **Prevents regression** — Adding new behavior does not require changing existing, tested code.
- **Extension without modification** — Prefer interfaces/abstract classes and new implementations over editing existing conditionals.
- **Inference:** When you see `if (type == "X")` or long `switch` on types, suggest polymorphism (e.g. strategy, factory) so new types are added as new classes.

**Example**

Bad (modification required for every new type):

```java
class ReportExporter {
    void export(String type, Data data) {
        if (type.equals("PDF")) { /* PDF */ }
        else if (type.equals("DOC")) { /* DOC */ }
        else if (type.equals("CSV")) { /* CSV */ }
    }
}
```

Better (extend by adding new classes; no change to existing logic):

```java
interface ReportGenerator {
    void generate(Data data);
}

class PdfReportGenerator implements ReportGenerator {
    @Override public void generate(Data data) { /* PDF */ }
}

class CsvReportGenerator implements ReportGenerator {
    @Override public void generate(Data data) { /* CSV */ }
}
```

---

### L – Liskov Substitution Principle (LSP)

**Definition:** Subtypes must be **replaceable for their base types without breaking behavior**.

**What it achieves (agent context):**

- **Correct inheritance** — Subclasses must honor the contract of the base (preconditions, postconditions, invariants).
- **Reliable polymorphism** — Callers can use the base type without knowing the concrete subtype; no surprises (e.g. throwing in a case that base does not).
- **Inference:** If a subclass weakens preconditions, strengthens postconditions, or throws new exceptions, it likely violates LSP. Prefer composition or more specific interfaces (e.g. `FlyingBird` vs `Bird`) when not all subtypes support the same operations.

**Example**

Bad (subtype cannot fulfill base contract — penguin cannot fly):

```java
class Bird {
    void fly() { /* assume all birds fly */ }
}

class Penguin extends Bird {
    @Override void fly() { throw new UnsupportedOperationException("Penguins can't fly"); }
}
```

Better (separate interface for flying; only flying birds implement it):

```java
interface Bird { }

interface FlyingBird extends Bird {
    void fly();
}

class Sparrow implements FlyingBird {
    @Override public void fly() { /* fly */ }
}

class Penguin implements Bird { /* no fly() */ }
```

---

### I – Interface Segregation Principle (ISP)

**Definition:** Clients should **not be forced to depend on interfaces they do not use**.

**What it achieves (agent context):**

- **Smaller, focused interfaces** — Clients depend only on the methods they need.
- **Flexibility** — Implementations can provide only relevant behavior; no dummy/empty methods.
- **Reduced complexity** — Easier to mock and test; changes to one capability do not force changes in unrelated clients.
- **Inference:** When you see a "fat" interface with many methods and implementations that leave some no-op or throwing, suggest splitting into role interfaces (e.g. `Workable`, `Eatable`).

**Example**

Bad (worker must implement `eat()` even if not needed; robot cannot eat):

```java
interface Worker {
    void work();
    void eat();
}

class Human implements Worker {
    public void work() { /* work */ }
    public void eat() { /* eat */ }
}

class Robot implements Worker {
    public void work() { /* work */ }
    public void eat() { } // no-op or throw — forced dependency
}
```

Better (clients depend only on what they use):

```java
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

class Human implements Workable, Eatable {
    public void work() { /* work */ }
    public void eat() { /* eat */ }
}

class Robot implements Workable {
    public void work() { /* work */ }
}
```

---

### D – Dependency Inversion Principle (DIP)

**Definition:** High-level modules should **not depend on low-level modules**; both should depend on **abstractions**.

**What it achieves (agent context):**

- **Loose coupling** — High-level logic does not depend on concrete payment gateways, repositories, or APIs.
- **Testability** — Abstractions (interfaces) can be mocked in tests.
- **Enables Dependency Injection** — Frameworks (e.g. Spring) inject implementations; swapping implementations does not require changing high-level code.
- **Inference:** When you see `new ConcreteService()` inside a high-level class, suggest depending on an interface and injecting the implementation (constructor or setter).

**Example**

Bad (high-level depends on concrete low-level):

```java
class OrderService {
    private PaymentService payment = new PaymentService(); // tight coupling
    void placeOrder(Order order) {
        payment.charge(order.getTotal());
    }
}
```

Better (depend on abstraction; inject implementation):

```java
interface PaymentProcessor {
    void charge(BigDecimal amount);
}

class OrderService {
    private final PaymentProcessor payment;

    OrderService(PaymentProcessor payment) {
        this.payment = payment;
    }

    void placeOrder(Order order) {
        payment.charge(order.getTotal());
    }
}
```

Used heavily in **Spring Dependency Injection** (constructor injection preferred).

---

## DRY Principle

**Definition:** Every piece of knowledge should have **a single source of truth**.

**What it achieves (agent context):**

- **Less duplication** — Logic, constants, and validation live in one place; changes propagate automatically.
- **Easier maintenance** — Fix or evolve behavior in one place instead of hunting duplicates.
- **Consistent behavior** — Same rule (e.g. "adult = age > 18") applied everywhere.
- **Inference:** When you see the same condition, formula, or block of code in multiple places, suggest extracting a method, constant, or shared utility.

**Example**

Bad (same rule repeated):

```java
if (user.getAge() > 18) { /* allow */ }
// ...
if (employee.getAge() > 18) { /* allow */ }
```

Better (single source of truth):

```java
boolean isAdult(int age) {
    return age > 18;
}
// use: if (isAdult(user.getAge())) { ... }
```

---

## KISS Principle

**Definition:** Design should be **as simple as possible** (Keep It Simple, Stupid).

**What it achieves (agent context):**

- **Readable code** — Others can understand and change it without deep mental load.
- **Faster debugging** — Fewer moving parts and fewer abstractions to trace.
- **Lower complexity** — Avoid over-engineering; prefer straightforward conditionals or small methods when they suffice.
- **Inference:** When code uses heavy abstraction or functional chains where a simple null check or loop would do, suggest the simpler version unless there is a clear benefit (e.g. large streams, reuse).

**Example**

Overly complex for a simple null check:

```java
Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");
```

Simpler and clearer when only one level is needed:

```java
String city = (user != null && user.getAddress() != null)
    ? user.getAddress().getCity()
    : "Unknown";
```

---

## Law of Demeter (LoD) / Principle of Least Knowledge

**Definition:** A class should only interact with **its immediate dependencies** (friends), not with their friends.

**What it achieves (agent context):**

- **Reduced coupling** — Caller does not depend on the internal structure of nested objects (e.g. `order.getCustomer().getAddress().getZipCode()`).
- **Better encapsulation** — Details of how zip is obtained stay inside the domain (e.g. `Order` or a service).
- **Easier refactoring** — If `Customer` or `Address` structure changes, only one place (the API that returns zip) needs to change.
- **Inference:** When you see chained getters (e.g. `a.getB().getC().getD()`), suggest a single method on the root object or a facade (e.g. `order.getCustomerZipCode()`).

**Example**

Bad (chained calls; depends on full path):

```java
String zip = order.getCustomer().getAddress().getZipCode();
```

Better (single method on the object you already have):

```java
// On Order (or a service that has Order)
String zip = order.getCustomerZipCode();
// implementation: return customer != null && customer.getAddress() != null
//     ? customer.getAddress().getZipCode() : null;
```

---

## Composition Over Inheritance

**Definition:** Prefer **object composition** (has-a) over **inheritance** (is-a) for reusing behavior.

**What it achieves (agent context):**

- **Flexibility** — Behavior can be swapped at runtime; no rigid hierarchy.
- **Avoids deep inheritance trees** — Fewer fragile base classes and override chains.
- **Easier testing** — Composed dependencies can be mocked.
- **Inference:** When you see "X extends Y" only to reuse Y's code (and "X is-a Y" is not a true subtype), suggest holding Y as a field and delegating (composition).

**Example**

Bad (inheritance for reuse; "Car is-a Engine" is wrong):

```java
class Car extends Engine {
    void drive() { start(); /* ... */ }
}
```

Better (composition; car has an engine):

```java
class Car {
    private final Engine engine;

    Car(Engine engine) {
        this.engine = engine;
    }

    void drive() {
        engine.start();
        // ...
    }
}
```

---

## Separation of Concerns (SoC)

**Definition:** Divide the system so that **each part handles a specific concern** (e.g. API, business logic, data access).

**What it achieves (agent context):**

- **Clear architecture** — Controllers handle HTTP, services handle rules, repositories handle persistence.
- **Easier testing** — Each layer can be tested in isolation with mocks.
- **Independent evolution** — Change API contract or database without rewriting business logic.
- **Inference:** When business logic appears in controllers or SQL in services, recommend moving it to the appropriate layer (e.g. service for rules, repository for queries).

**Example**

Typical layering in **Spring Boot**:

```
Controller  → HTTP, validation, DTO mapping
Service     → Business logic, transactions
Repository  → Data access, queries
```

Code-level example:

```java
// Controller — only HTTP and delegation
@RestController
class UserController {
    private final UserService userService;
    UserDto createUser(@RequestBody UserDto dto) {
        return userService.createUser(dto);
    }
}

// Service — business rules only
@Service
class UserService {
    private final UserRepository userRepository;
    UserDto createUser(UserDto dto) {
        if (userRepository.existsByEmail(dto.getEmail()))
            throw new ConflictException("Email already exists");
        return map(userRepository.save(toEntity(dto)));
    }
}

// Repository — data access only
interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByEmail(String email);
}
```

---

## High Cohesion & Low Coupling

### High Cohesion

**Definition:** A class (or module) should contain **closely related responsibilities** that work toward one purpose.

**What it achieves (agent context):** Changes to one feature stay in one place; the class is easier to name, test, and reuse as a unit.

### Low Coupling

**Definition:** Classes (or modules) should **depend minimally on each other**, preferably on abstractions.

**What it achieves (agent context):** Changing one module has fewer ripple effects; systems are easier to refactor and deploy in parts.

**Combined inference:** When reviewing, prefer modules that do one thing well (high cohesion) and depend on few, stable abstractions (low coupling). Suggest splitting classes that mix unrelated concerns or that depend on many concrete types.

**Example**

Bad (low cohesion, high coupling — one class does persistence, HTTP, and formatting):

```java
class UserHandler {
    public String handle(HttpRequest req) {
        User u = new User(req.getParam("name"), Integer.parseInt(req.getParam("age")));
        try (Connection c = DriverManager.getConnection("jdbc:...")) {
            c.createStatement().executeUpdate("INSERT INTO users ...");
        }
        return "<html><body>Added " + u.getName() + "</body></html>";
    }
}
```

Better (separate concerns; each class has one reason to change):

```java
class UserController {
    private final UserService userService;
    ResponseEntity<String> createUser(@RequestBody UserDto dto) {
        return ResponseEntity.ok(userService.createUser(dto).getId());
    }
}

class UserService {
    private final UserRepository userRepository;
    User createUser(UserDto dto) {
        return userRepository.save(User.from(dto));
    }
}

interface UserRepository {
    User save(User user);
}
```

---

## Fail Fast Principle

**Definition:** Systems should **fail immediately when an error or invalid state is detected**, rather than continuing and failing later in a harder-to-debug way.

**What it achieves (agent context):**

- **Easier debugging** — Failure happens at the point of the bug (e.g. null, invalid argument).
- **Prevents hidden bugs** — Invalid data is not propagated; no silent wrong results.
- **Inference:** Recommend validating inputs at boundaries (e.g. controller, public API) and using assertions or `requireNonNull` for invariants; avoid swallowing exceptions or returning sentinel values when a clear failure is more appropriate.

**Example**

Validate early; fail fast:

```java
public User createUser(String name, int age) {
    Objects.requireNonNull(name, "name must not be null");
    if (age < 0 || age > 150)
        throw new IllegalArgumentException("Invalid age: " + age);
    return new User(name, age);
}
```

---

## Immutability Principle

**Definition:** Objects should **not change state after creation**; all state is set in the constructor and never modified.

**What it achieves (agent context):**

- **Thread safety** — Immutable objects can be shared without synchronization.
- **Predictable behavior** — No hidden changes; same reference always represents same value.
- **Easier concurrency and caching** — Safe to cache and pass across threads.
- **Inference:** When you see setters or mutable fields on value-like objects (e.g. DTOs, domain values), suggest immutable alternatives (records, final fields, copy-on-write if needed).

**Example**

Immutable value with Java record:

```java
public record User(String name, int age) {
    // Compact constructor for validation
    public User {
        Objects.requireNonNull(name);
        if (age < 0) throw new IllegalArgumentException("age must be non-negative");
    }
}
```

Traditional immutable class:

```java
public final class User {
    private final String name;
    private final int age;

    public User(String name, int age) {
        this.name = Objects.requireNonNull(name);
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    // No setters
}
```

---

## Required Output Format

When this skill is invoked for a **design or code review**, the response must exactly follow one of the two templates below:

### Template A (any findings)

```markdown
# Design Review Summary

Found <X> critical issues need to be fixed:

## 🔴 Critical (Must Fix)

### 1. <brief description of the issue>

FilePath: <path> line <line>
<relevant code snippet or pointer>

#### Explanation

<detailed explanation and references of the issue>

#### Suggested Fix

1. <brief description of suggested fix>
2. <code example> (optional, omit if not applicable)

---
... (repeat for each critical issue) ...

Found <Y> suggestions for improvement:

## 🟡 Suggestions (Should Consider)

### 1. <brief description of the suggestion>

FilePath: <path> line <line>
<relevant code snippet or pointer>

#### Explanation

<detailed explanation and references of the suggestion>

#### Suggested Fix

1. <brief description of suggested fix>
2. <code example> (optional, omit if not applicable)

---
... (repeat for each suggestion) ...

## ✅ What's Good

- <Positive feedback on good patterns>
```

- If there are no critical issues or suggestions or good points, just omit that section.
- If the issue number is more than 10, summarize as "Found 10+ critical issues/suggestions" and only output the first 10 items.

### Template B (no issues)

```markdown
## Design Review Summary
✅ No issues found.
```

---

## Knowledge Reference

Java 17, Spring Boot 3.x, JUnit 5, Mockito, Maven/Gradle
