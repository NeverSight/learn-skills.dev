---
name: effective-go
description: "Apply Go best practices, idioms, and conventions from golang.org/doc/effective_go. Use when writing, reviewing, or refactoring Go code to ensure idiomatic, clean, and efficient implementations."
metadata:
  author: caijiatao
  version: "2026.2.24"
  source: https://go.dev/doc/effective_go
  language: en
  tags: [best-practices, idioms, conventions, formatting, naming, error-handling]
  category: core
---

# Effective Go

Apply best practices and conventions from the official [Effective Go guide](https://go.dev/doc/effective_go) to write clean, idiomatic Go code.

## When to Apply

Use this skill automatically when:
- Writing new Go code
- Reviewing Go code
- Refactoring existing Go implementations

## Core Concepts

| Topic | Description | Reference |
|-------|-------------|-----------|
| **Formatting** | Always use gofmt - this is non-negotiable | [core-formatting](references/core-formatting.md) |
| **Naming** | MixedCaps for exported, mixedCaps for unexported | [core-naming](references/core-naming.md) |
| **Error Handling** | Check errors, return them, don't panic | [core-error-handling](references/core-error-handling.md) |
| **Concurrency** | Share memory by communicating (use channels) | [core-concurrency](references/core-concurrency.md) |
| **Interfaces** | Keep small (1-3 methods ideal); accept interfaces, return concrete types | [core-interfaces](references/core-interfaces.md) |
| **Documentation** | Document all exported symbols | [core-documentation](references/core-documentation.md) |

## Key Reminders

Follow the conventions and patterns documented at https://go.dev/doc/effective_go:

- **Formatting**: Use `gofmt` - this is non-negotiable
- **Naming**: No underscores, use MixedCaps for exported names
- **Error handling**: Always check errors; return them, don't panic
- **Concurrency**: Share memory by communicating
- **Interfaces**: Keep small and accept interfaces, return structs
- **Documentation**: Document all exported symbols

## References

- Official Guide: https://go.dev/doc/effective_go
- Code Review Comments: https://github.com/golang/go/wiki/CodeReviewComments
- Standard Library: Use as reference for idiomatic patterns
