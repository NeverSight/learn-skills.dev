---
name: golang-base-practices
description: Go language best practices guide covering frameworks (Gin/Go-Kratos), ORM (GORM), database migrations (Goose), DDD project structure, error handling, concurrency patterns, testing (99% coverage target), and Lint tools. This skill should be used when writing, reviewing, or refactoring Go code to ensure best practices are followed. Triggers on Go project development, code review, performance optimization, or architecture design.
---

# Golang Base Practices

Comprehensive Go development best practices guide, organized by priority for code generation, review, and refactoring. Contains 53 rules referenced from Effective Go, Google Go Style Guide, Uber Go Style Guide, and Go Code Review Comments.

## When to Apply

Reference these guidelines when:
- Creating new Go projects or microservices
- Building API interfaces (REST/gRPC)
- Performing database operations and migrations
- Conducting code reviews and refactoring
- Optimizing performance and concurrency
- Improving test coverage

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Framework Selection | CRITICAL | `framework-` |
| 2 | Database & ORM | CRITICAL | `db-` |
| 3 | DDD Project Structure | HIGH | `ddd-` |
| 4 | Error Handling | HIGH | `error-` |
| 5 | Concurrency Patterns | HIGH | `concurrency-` |
| 6 | Idiomatic Go | MEDIUM | `idiomatic-` |
| 7 | Testing Practices | CRITICAL | `testing-` |
| 8 | Performance Optimization | MEDIUM | `performance-` |
| 9 | Lint & Toolchain | MEDIUM | `lint-` |

## Quick Reference

### 1. Framework Selection (CRITICAL)

- `framework-gin-simple` - Use Gin for simple projects
- `framework-kratos-complex` - Use Go-Kratos for complex microservices
- `framework-middleware` - Middleware design patterns
- `framework-graceful-shutdown` - Graceful server shutdown

### 2. Database & ORM (CRITICAL)

- `db-gorm-setup` - GORM initialization and configuration
- `db-gorm-hooks` - GORM Hook usage guidelines
- `db-gorm-transactions` - Transaction handling patterns
- `db-goose-migrations` - Database migrations with Goose
- `db-connection-pool` - Connection pool configuration

### 3. DDD Project Structure (HIGH)

- `ddd-project-layout` - Standard project directory structure
- `ddd-domain-layer` - Domain layer design
- `ddd-application-layer` - Application layer design
- `ddd-infrastructure-layer` - Infrastructure layer design
- `ddd-interface-layer` - Interface layer design
- `ddd-dependency-injection` - Dependency injection patterns

### 4. Error Handling (HIGH)

- `error-wrap-context` - Error wrapping with context
- `error-sentinel` - Sentinel error definitions
- `error-custom-types` - Custom error types
- `error-handling-check` - Always check error returns
- `error-api-response` - API error response standards
- `error-panic-recover` - Panic and recover usage guidelines

### 5. Concurrency Patterns (HIGH)

- `concurrency-goroutine-lifecycle` - Goroutine lifecycle management
- `concurrency-channel-patterns` - Channel usage patterns
- `concurrency-channel-size` - Channel buffer size selection
- `concurrency-context-cancel` - Context cancellation propagation
- `concurrency-errgroup` - errgroup concurrency control
- `concurrency-sync-primitives` - sync package primitives usage
- `concurrency-race-detection` - Race condition detection

### 6. Idiomatic Go (MEDIUM)

- `idiomatic-naming` - Naming conventions
- `idiomatic-comment` - Doc Comments guidelines
- `idiomatic-interface` - Interface design (prefer small interfaces)
- `idiomatic-receiver` - Receiver naming and selection
- `idiomatic-struct-init` - Struct initialization
- `idiomatic-functional-options` - Functional options pattern
- `idiomatic-defer` - defer usage guidelines
- `idiomatic-slice-map` - Slice and Map operations
- `idiomatic-zero-value` - Zero value utilization
- `idiomatic-embedding` - Type embedding
- `idiomatic-blank-identifier` - Blank identifier usage

### 7. Testing Practices (CRITICAL)

- `testing-coverage-99` - 99% test coverage target
- `testing-table-driven` - Table-driven tests
- `testing-mock` - Mocking and interface abstraction
- `testing-helper` - Test helper function guidelines
- `testing-benchmark` - Benchmark testing
- `testing-integration` - Integration testing standards
- `testing-testify` - testify assertion library usage

### 8. Performance Optimization (MEDIUM)

- `performance-strconv` - Use strconv instead of fmt
- `performance-prealloc` - Container preallocation

### 9. Lint & Toolchain (MEDIUM)

- `lint-golangci` - golangci-lint configuration
- `lint-gofmt` - Code formatting
- `lint-govet` - Static analysis
- `lint-staticcheck` - Advanced static checking
- `lint-revive` - Customizable linter

## How to Use

Consult specific rule files in the `rules/` directory for detailed explanations and code examples:

```
rules/framework-gin-simple.md
rules/db-gorm-setup.md
rules/testing-table-driven.md
```

Each rule file contains:
- Rule explanation and importance
- Incorrect example with analysis
- Correct example with explanation
- Additional context and references

## Core Principles

1. **KISS** - Keep it simple, avoid over-engineering
2. **YAGNI** - Only implement what is currently needed
3. **Explicit over Implicit** - Code intent should be clear
4. **Handle All Errors** - Never ignore error returns
5. **99% Test Coverage** - Foundation for high-quality code
