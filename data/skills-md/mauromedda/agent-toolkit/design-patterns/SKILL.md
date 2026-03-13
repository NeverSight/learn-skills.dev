---
name: design-patterns
description: >-
  Cross-language architectural patterns for Go, Python, Bash, and Terraform.
  Covers dependency injection, error handling, configuration, logging, testing
  heuristics, and common anti-patterns. Use for architectural guidance and
  consistent patterns across languages. Triggers on "dependency injection",
  "DI pattern", "error handling pattern", "cross-language", "architectural pattern",
  "anti-pattern", "naming convention", "design pattern", "testing heuristic",
  "config pattern", "logging pattern".
allowed-tools: Read
---

# ABOUTME: Cross-language architectural patterns skill for consistent design
# ABOUTME: Orchestrates pattern selection and delegates to language-specific skills

# Design Patterns

Architectural patterns implemented consistently across Go, Python, Bash, and Terraform.

## Quick Reference

| Pattern | Go | Python | Bash | Terraform |
|---------|----|----|------|-----------|
| DI | Interfaces | Protocols | Functions | Variables/Modules |
| Errors | `error` return | Exceptions | Exit codes | Validation blocks |
| Config | Env + struct | Pydantic Settings | Env vars | `tfvars` files |
| Logging | `log/slog` | `logging` | stderr functions | N/A |
| Testing | `go test` | `pytest` | `bats` | `terraform validate` |

## Pattern Selection

What are you working on?

- **Dependency Injection** → See `references/cross-language.md` Section 1
- **Error Handling** → See `references/cross-language.md` Section 2
- **Configuration** → See `references/cross-language.md` Section 3
- **Logging** → See `references/cross-language.md` Section 4
- **Testing Heuristics** → See `references/cross-language.md` Section 5
- **Background Jobs** → See `references/cross-language.md` Section 6
- **Anti-Patterns** → See `references/cross-language.md` Section 7
- **Naming Conventions** → See `references/cross-language.md` Section 8

## Workflow

1. **Identify the pattern** needed from the selection above
2. **Read the reference** for cross-language examples
3. **Invoke language skill** for implementation:
   - Go code → `/golang`
   - Python code → `/python`
   - Bash script → `/bash`
   - Terraform → `/terraform`

## When to Use This Skill

- Discussing architectural decisions across multiple languages
- Ensuring consistency in error handling, DI, or config patterns
- Reviewing code for anti-patterns
- Establishing naming conventions for a polyglot project
- Teaching or documenting cross-language standards

## Language-Specific Implementation

After reviewing the pattern, invoke the appropriate language skill:

| Language | Skill | When |
|----------|-------|------|
| Go | `/golang` | Writing `.go` files |
| Python | `/python` | Writing `.py` files |
| Bash | `/bash` | Writing `.sh` files |
| Terraform | `/terraform` | Writing `.tf` files |

## Resources

- `references/cross-language.md` - Detailed patterns with code examples
