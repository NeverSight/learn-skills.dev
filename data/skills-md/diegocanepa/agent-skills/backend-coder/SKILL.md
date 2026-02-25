---
name: backend-coder
description: Expert backend development following SOLID principles, design patterns, type-safety, and test-driven workflows.
---

# Backend Coder Skill

## Core Principles
1. **Language Documentation**: Always use the **context MCP** tool (`context7`) to fetch updated documentation, best practices, and idiomatic patterns for the language/framework being used.
2. **Type Safety**: Prioritize strong typing and compile-time validation. Avoid `any` or dynamic types.
3. **SOLID Principles**: Focused on SRP, OCP, LSP, ISP, and DIP.
4. **Clean Architecture**: Separation of domain, application, and infrastructure.

## Workflow
1. **Analysis**: Understand dependencies and fetch language documentation via MCP.
2. **TDD (Testing Strategy)**: Write unit tests for business logic and integration tests for external dependencies. Use mocks/stubs for I/O.
3. **Implementation**: Atomic functions, dependency injection, and clear patterns.
4. **Verification**: Run local tests and fix autonomously.

## Best Practices
- **English Only**: Code, comments, and docs.
- **Atomic**: One responsibility per function/class.
- **Logging & Traceability**: Implement structured logging (JSON preferred) with unique trace IDs to track requests across the system. This is CRITICAL for production debugging.
- **Error Handling**: Specific exceptions, clear messages, no bare `except`.

## Performance Considerations
- **Efficiency**: Use caching strategically for expensive operations.
- **I/O Optimization**: Use async/await for I/O-bound operations and optimize DB queries.
- **Pagination**: Implement for any list-returning endpoint to handle large datasets.

## Security Best Practices
- **Input Validation**: Sanitize and validate all external input.
- **SQL Injection**: Use parameterized queries or ORMs correctly.
- **Secrets Management**: Never hard-code credentials; use environment variables or secret managers.
- **Principle of Least Privilege**: Access only the data/services necessary for the task.

## Anti-Patterns
- **God Objects**: Classes that handle too many responsibilities.
- **Tight Coupling**: Direct dependencies between high-level and low-level modules.
- **Mixing Concerns**: Business logic contaminated with infrastructure/database details.