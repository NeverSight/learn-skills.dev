---
name: documentation-writer
description: Technical documentation writer. Use when generating or improving documentation — README files, API docs, architecture docs, and code comments.
disable-model-invocation: true
argument-hint: [target]
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Documentation Writer

Generate or improve documentation for $ARGUMENTS:

## Process

1. **Read the codebase** — understand what exists before documenting
2. **Identify the audience** — developers? users? operators?
3. **Follow existing doc style** in the project
4. **Write documentation** following the guidelines below

## README Structure
A good README contains:
1. **Title + one-line description** — what this project does
2. **Quick start** — how to get running in < 5 commands
3. **Installation** — prerequisites, install steps
4. **Usage** — common use cases with code examples
5. **Configuration** — environment variables, config files
6. **API Reference** — link or inline for library projects
7. **Contributing** — how to contribute, dev setup
8. **License**

## Writing Style
- Write in present tense, active voice
- Use second person ("you") for instructions
- Use code blocks with language identifiers
- One sentence per line in source (better diffs)
- Use headings hierarchically (don't skip levels)
- Include copy-pasteable commands (not pseudo-code)
- Show expected output where helpful

## API Documentation
- Document every public function/method/endpoint
- Include parameter types, descriptions, defaults
- Show at least one usage example
- Document error responses/exceptions
- Group by feature area, not alphabetically

## Architecture Documentation
- Start with a high-level overview diagram
- Describe each component's responsibility
- Document data flow between components
- Note key design decisions and trade-offs
- List external dependencies and why they were chosen

## Rules
- Don't document the obvious — focus on "why" and "how to use"
- Keep docs close to code — prefer doc comments over separate files
- Use diagrams (Mermaid, ASCII) for complex flows
- Update docs when changing the code they describe
