---
name: java-best-practices-code-review
description: |
  Analyzes Java code against industry best practices and evaluates design principles
  including SOLID, exception handling, thread safety, and resource management. Reviews
  naming conventions, Stream API usage, Optional patterns, and general code quality.
  Use when reviewing Java files, checking code quality, evaluating exception handling,
  or auditing resource management.
allowed-tools:
  - Read
  - Glob
  - Grep
---

Works with .java files, Spring components, and Java projects of any size.
# Java Code Review

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Review Checklist](#review-checklist)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Performs comprehensive code reviews of Java code against industry best practices, SOLID principles, and modern Java idioms. Provides actionable feedback to improve code quality, maintainability, and security.

## When to Use

Use this skill when you need to:
- Review Java files for code quality issues
- Analyze SOLID principle compliance
- Evaluate exception handling patterns
- Assess thread safety in concurrent code
- Audit resource management (try-with-resources usage)
- Check naming conventions and coding standards
- Review Stream API and Optional usage
- Verify modern Java features adoption (Java 8+ idioms)
- Conduct PR reviews for Java projects
- Identify refactoring opportunities

## Quick Start
Point to any Java file or directory and receive immediate feedback on code quality issues:

```bash
# Review a single file
Review src/main/java/com/example/UserService.java

# Review all Java files in a package
Review all Java files in src/main/java/com/example/service/
```

## Instructions

### Step 1: Identify Target Scope
Determine what needs to be reviewed:
- Single Java class file
- Package directory (all .java files)
- Specific component type (controllers, services, repositories)
- Entire src tree

Use Glob to find Java files if not explicitly specified:
```bash
**/*.java                    # All Java files
src/main/java/**/*Service.java  # All service classes
```

### Step 2: Read and Analyze Code
For each Java file, perform multi-dimensional analysis:

**SOLID Principles Assessment:**
- Single Responsibility: Does class have one clear purpose?
- Open/Closed: Is class extensible without modification?
- Liskov Substitution: Are inheritance hierarchies sound?
- Interface Segregation: Are interfaces focused and minimal?
- Dependency Inversion: Does code depend on abstractions?

**Code Quality Checks:**
- Naming conventions (camelCase, PascalCase, UPPER_SNAKE_CASE)
- Method length (flag methods over 50 lines)
- Class cohesion (related methods grouped together)
- Magic numbers and strings (should be constants)
- Code duplication (DRY principle violations)

**Exception Handling:**
- Proper exception types (checked vs unchecked)
- No empty catch blocks
- No catching generic Exception unless necessary
- Meaningful error messages
- Proper exception chaining (throw new CustomException(e))

**Resource Management:**
- try-with-resources for AutoCloseable resources
- Proper Stream/File/Connection closing
- No resource leaks

**Modern Java Patterns:**
- Stream API usage (prefer streams over loops where appropriate)
- Optional instead of null returns
- Records for data classes (Java 14+)
- Switch expressions (Java 14+)
- Text blocks for multi-line strings (Java 15+)

**Thread Safety:**
- Proper synchronization if needed
- Immutability where possible
- Thread-safe collection usage
- Avoid shared mutable state

**Security Concerns:**
- No hardcoded credentials
- Proper input validation
- SQL injection prevention (use PreparedStatement)
- Path traversal vulnerabilities
- Sensitive data logging

### Step 3: Generate Structured Review Report
Organize findings by severity:

**CRITICAL** - Must fix immediately:
- Security vulnerabilities
- Resource leaks
- Thread safety violations in concurrent code

**HIGH** - Should fix soon:
- SOLID principle violations
- Poor error handling
- Significant code smells

**MEDIUM** - Improve when possible:
- Code duplication
- Naming convention issues
- Missing modern Java features

**LOW** - Nice to have:
- Code style inconsistencies
- Minor optimizations
- Documentation improvements

### Step 4: Provide Actionable Recommendations
For each issue identified:
1. Specify exact location (file, line number)
2. Explain the problem clearly
3. Show code example of the issue
4. Provide corrected code example
5. Explain why the change improves code quality

## Examples

### Example 1: Review Single Service Class

**Input:**
```java
public class UserService {
    private UserRepository userRepository = new UserRepository();

    public User getUser(String id) {
        User user = userRepository.findById(id);
        if (user == null) {
            return null;
        }
        return user;
    }
}
```

**Review Output:**
```
CRITICAL Issues:
- Line 2: Dependency Inversion violation - direct instantiation of UserRepository
  Fix: Inject UserRepository via constructor

HIGH Issues:
- Line 7: Returns null instead of Optional<User>
  Fix: Return Optional.ofNullable(user)

MEDIUM Issues:
- Class lacks @Service annotation (assuming Spring)
- No logging for diagnostic purposes

Recommended Refactoring:
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    public Optional<User> getUser(String id) {
        log.debug("Fetching user with id: {}", id);
        return Optional.ofNullable(userRepository.findById(id));
    }
}
```
```

### Example 2: Review Controller with Multiple Issues

**Input:**
```java
public class UserController {
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable String id) {
        try {
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db", "root", "password");
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM users WHERE id = " + id);
            if (rs.next()) {
                return new User(rs.getString("name"), rs.getString("email"));
            }
        } catch (Exception e) {
            // ignore
        }
        return null;
    }
}
```

**Review Output:**
```
CRITICAL Issues:
1. Line 7: SQL Injection vulnerability - concatenating user input into query
   Fix: Use PreparedStatement with parameters

2. Line 5: Hardcoded database credentials in code
   Fix: Externalize to application.properties and use Spring's DataSource

3. Lines 5-10: Resource leak - Connection, Statement, ResultSet not closed
   Fix: Use try-with-resources or Spring JdbcTemplate

4. Line 11-13: Empty catch block silently swallows exceptions
   Fix: Log exception and throw appropriate response exception

HIGH Issues:
5. Architecture violation: Controller directly accessing database
   Fix: Use Service layer and Repository pattern

6. Line 14: Returns null instead of proper HTTP 404
   Fix: Throw ResponseStatusException or return ResponseEntity

MEDIUM Issues:
7. Missing @RestController annotation
8. No input validation on id parameter
9. No API documentation (@Operation, @ApiResponse)

Recommended Architecture:
```java
@RestController
@RequiredArgsConstructor
@Validated
public class UserController {
    private final UserService userService;

    @GetMapping("/users/{id}")
    @Operation(summary = "Get user by ID")
    public ResponseEntity<User> getUser(
            @PathVariable @NotBlank String id) {
        return userService.getUser(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public Optional<User> getUser(String id) {
        return userRepository.findById(id);
    }
}

@Repository
public interface UserRepository extends JpaRepository<User, String> {
}
```
```

### Example 3: Review Stream API Usage

**Input:**
```java
List<String> activeUserNames = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        activeUserNames.add(user.getName());
    }
}
Collections.sort(activeUserNames);
```

**Review Output:**
```
MEDIUM Issues:
- Lines 1-6: Imperative loop should use Stream API for clarity
- Line 7: Mutating list instead of using sorted stream

Recommended Refactoring:
```java
List<String> activeUserNames = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .sorted()
    .toList();
```

Benefits:
- More declarative and readable
- Immutable result (.toList() returns unmodifiable list)
- Potential for parallel processing if needed
- Method reference usage (User::isActive)
```

## Requirements

- Java 8+ knowledge for Stream API, Optional, lambda expressions
- Java 11+ awareness for var, String methods, Collection.toArray()
- Java 14+ familiarity with records, switch expressions, text blocks
- Java 17+ understanding of sealed classes, pattern matching
- Understanding of SOLID principles and design patterns
- Familiarity with Spring Framework conventions (if reviewing Spring code)
- Knowledge of common security vulnerabilities (OWASP Top 10)

## Review Checklist

Use this checklist to ensure comprehensive coverage:

**Design & Architecture:**
- [ ] SOLID principles followed
- [ ] Proper layer separation (Controller/Service/Repository)
- [ ] Dependency injection used correctly
- [ ] Interfaces used for abstraction
- [ ] Design patterns applied appropriately

**Code Quality:**
- [ ] Methods are focused and under 50 lines
- [ ] No code duplication (DRY)
- [ ] Clear, descriptive naming
- [ ] No magic numbers or strings
- [ ] Proper visibility modifiers (private, protected, public)

**Error Handling:**
- [ ] Appropriate exception types used
- [ ] No empty catch blocks
- [ ] Meaningful error messages
- [ ] Exception chaining preserved
- [ ] Resources cleaned up in finally or try-with-resources

**Modern Java:**
- [ ] Stream API used where appropriate
- [ ] Optional used instead of null returns
- [ ] Records used for DTOs (Java 14+)
- [ ] Switch expressions used (Java 14+)
- [ ] Text blocks for multi-line strings (Java 15+)

**Thread Safety:**
- [ ] Shared mutable state identified
- [ ] Proper synchronization if needed
- [ ] Immutable objects preferred
- [ ] Thread-safe collections used

**Security:**
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] SQL injection prevention (PreparedStatement)
- [ ] No path traversal vulnerabilities
- [ ] Sensitive data not logged

**Performance:**
- [ ] No premature optimization
- [ ] Efficient algorithms used
- [ ] Proper use of collections
- [ ] Stream operations optimized
- [ ] Database N+1 queries avoided

## Output Format

Always structure review output as:

```markdown
# Java Code Review: [ClassName or Package]

## Summary
- Files reviewed: X
- Critical issues: X
- High priority issues: X
- Medium priority issues: X
- Low priority issues: X

## Critical Issues (Fix Immediately)
[List with file:line, description, fix]

## High Priority Issues (Fix Soon)
[List with file:line, description, fix]

## Medium Priority Issues (Improve When Possible)
[List with file:line, description, fix]

## Low Priority Issues (Nice to Have)
[List with file:line, description, fix]

## Positive Findings
[Call out well-written code and good practices]

## Overall Assessment
[Summary paragraph with key recommendations]
```

## Error Handling

If review cannot be completed:

1. **File Not Found:** Verify path and use Glob to search for Java files
2. **Cannot Parse Code:** Note syntax errors preventing analysis
3. **Incomplete Context:** Request additional files for proper review (e.g., parent classes, interfaces)
4. **Ambiguous Requirements:** Ask for specific focus areas (security, performance, etc.)

Always fail-fast with clear error messages rather than providing incomplete reviews.
