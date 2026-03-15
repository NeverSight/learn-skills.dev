---
name: golang-expert-skill
description: Comprehensive documentation and language specification for the Go Programming Language. Use this skill when asked to write or debug Go code, explain Go syntax or data structures, understand concurrency patterns (goroutines, channels), modules, and workspace setups. It contains exhaustive reference on everything related to Go.
---

# Go Expert Skill

This skill provides comprehensive and official documentation for the Go programming language to assist in developing, debugging, understanding, and architecting Go applications.

The skill comes with the following key references that should be consulted as needed:

## References

1. **[The Go Programming Language Specification](references/go_spec.md)**  
   *Use when:* You need authoritative answers about language syntax, lexical elements, types (structs, interfaces, arrays, slices, maps, channels), specific behaviors of operators, expressions, variable declarations, memory representations, or any nuance regarding how the compiler evaluates code. It contains the exact grammar and rules (v1.26).

2. **[Go Language Documentation and Tutorials](references/go_docs.md)**  
   *Use when:* You need idiomatic go best practices (Effective Go), explanations of the Go garbage collector, modules (`go.mod`, dependency management, semantic versioning), workspaces, testing suites, REST API development with standard library or Gin, profiling, fuzzing, concurrency patterns, or database access methodologies using `database/sql`.

## Best Practices
- **Idiomatic Go**: Go code should be simple, clean, and concise. Consult the references to ensure adherence to standard library patterns instead of porting conventions from other languages.
- **Concurrency**: Rely on "Don't communicate by sharing memory, share memory by communicating" when using goroutines and channels.
- **Dependencies**: For handling packages and dependencies, refer to the module's documentation sections. Go modules are the standard dependency management system.

Whenever a user request demands deep Go-specific knowledge, always look up the relevant section in `references/go_spec.md` or `references/go_docs.md` before proceeding.
