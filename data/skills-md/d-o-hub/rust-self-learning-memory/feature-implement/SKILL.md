---
name: feature-implement
description: Systematic approach to implementing new features in the Rust memory system following project conventions. Use when adding new functionality with proper testing and documentation, maintaining code quality and test coverage.
---

# Feature Implementation

Systematic approach to implementing new features in the Rust memory system.

## Quick Reference

- **[Process](process.md)** - Implementation phases (planning, design, implementation, testing)
- **[Structure](structure.md)** - Module structure and file organization
- **[Patterns](patterns.md)** - Code patterns and conventions
- **[Quality](quality.md)** - Quality standards and checklists

## When to Use

- Adding new functionality to the codebase
- Following project conventions for feature development
- Maintaining code quality and test coverage

## Core Process

1. **Planning** - Understand requirements and constraints
2. **Design** - Architecture and module structure
3. **Implementation** - Write code following patterns
4. **Testing** - Add tests with >90% coverage
5. **Documentation** - Update docs and examples

See **[process.md](process.md)** for detailed phases and **[patterns.md](patterns.md)** for Rust code patterns.

## Project Standards

- File size: ≤ 500 LOC per file
- Async/Tokio patterns for I/O
- Error handling: `anyhow::Result`
- Storage: Turso (durable) + redb (cache)
- Serialization: postcard
