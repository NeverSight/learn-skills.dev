---
name: technical-writing
description: Guide for creating effective internal technical documentation (READMEs, ADRs, Contribution Guides). Use this skill when the user asks to write, refactor, or improve internal project documentation.
---

# Technical Writing for Developers

This skill provides best practices and templates for writing clear, maintainable internal documentation.

## Core Principles

1.  **Audience Awareness**: Write for your teammates (and your future self). Assume they know *how* to code, but not *why* this specific code exists.
2.  **Active Voice**: Use active voice for instructions.
    *   *Bad*: "The server should be started by running..."
    *   *Good*: "Run `npm start` to start the server."
3.  **Single Source of Truth**: Don't duplicate code logic in comments. Explain *why*, not *what*.
4.  **Front-Load Context**: Put the most important information (what is this? how do I run it?) at the top.

## Common Artifacts & Templates

### 1. README.md (Root or Component)

Every significant directory should have a README.

```markdown
# [Project/Component Name]

[One-sentence description of what this is].

## Prerequisite

*   Node.js >= 20
*   [Other dependency]

## Quick Start

```bash
npm install
npm run dev
```

## Architecture

[Brief explanation of how it works. Diagrams are great.]

## Key Concepts

*   **Concept A**: Definition...
*   **Concept B**: Definition...
```

### 2. Architecture Decision Record (ADR)

Use for significant technical decisions.

```markdown
# [Short Title]

*   **Status**: [Proposed | Accepted | Deprecated]
*   **Date**: YYYY-MM-DD
*   **Deciders**: [List names]

## Context

[Describe the problem and constraints.]

## Decision

[Describe what we are doing.]

## Consequences

*   [Positive consequence]
*   [Negative consequence / Trade-off]
```

## Style Guide

*   **Headers**: Use Sentence case for headers (e.g., "Getting started" not "Getting Started").
*   **Code Blocks**: Always specify the language for syntax highlighting (e.g., \`\`\`typescript).
*   **Lists**: Use bullet points for options, numbered lists for steps.
*   **Links**: Use relative links `[Link](./path/to/file)` so they work in the repo browser.

## Review Checklist

Before committing documentation:

- [ ] **Completeness**: did I cover "how to run" and "how to test"?
- [ ] **Freshness**: Did I actually run the commands in a fresh terminal?
- [ ] **Links**: Do all internal links work?
- [ ] **Grammar**: Is it readable? (Use a spell checker).
