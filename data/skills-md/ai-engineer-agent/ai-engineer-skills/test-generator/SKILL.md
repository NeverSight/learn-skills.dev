---
name: test-generator
description: Generate comprehensive tests for a module or function. Covers happy paths, edge cases, and error scenarios.
disable-model-invocation: true
argument-hint: [file-path]
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Test Generator

Generate comprehensive tests for $ARGUMENTS:

## Process

1. **Read the source file** to understand the API surface
2. **Detect the language and testing framework** from the project setup
3. **Identify existing tests** to avoid duplication
4. **Generate tests** covering:

### Test Categories

**Happy Path Tests**
- Normal inputs produce expected outputs
- All public methods/functions are exercised
- Common use cases are covered

**Edge Cases**
- Empty inputs (empty strings, arrays, objects)
- Boundary values (0, -1, MAX_INT, empty collections)
- Single-element collections
- Unicode and special characters

**Error Cases**
- Invalid inputs (wrong types, out-of-range values)
- Missing required fields
- Network/I/O failures (when applicable)
- Permission errors

**Integration Tests** (when appropriate)
- Component interactions
- Database operations
- API endpoint responses

## Style Rules
- Follow the existing test style in the project
- Use descriptive test names that read as documentation
- Use arrange-act-assert (given-when-then) structure
- One assertion concept per test
- Mock external dependencies, test internal logic directly
- Use factories/builders for test data, not inline object literals

## Output
Create the test file at the conventional location for the project's language and framework. If tests already exist, add missing test cases.
