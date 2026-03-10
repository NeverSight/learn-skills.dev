---
name: create-adr
description: >-
  Create a new Architecture Decision Record in doc/adr/.
  TRIGGER when: user asks to create or record an architectural decision, or mentions ADR.
  Examples: "create an ADR for...", "record the decision to use PostgreSQL", "add an ADR".
  DO NOT TRIGGER when: user wants to read/review existing ADRs or write general documentation.
allowed-tools: Bash, Read, Write, Glob, AskUserQuestion
---

Create a new Architecture Decision Record (ADR) in `doc/adr/` using the Nygard format.

## Steps

1. If the user did not provide a decision title as an argument, ask them for one
2. Convert the title to kebab-case for the filename
3. Use today's date (YYYY-MM-DD) as prefix: `doc/adr/YYYY-MM-DD-kebab-case-title.md`
4. Create the file with this template:

```markdown
# [Title]

**Status:** proposed

## Context

[What is the issue? What forces are at play? What is the background?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

[What becomes easier or more difficult to do because of this change?
Include positive, negative, and neutral consequences.]
```

6. Tell the user the file was created and its path
7. Remind them: "ADRs are immutable once accepted — to change a decision, supersede it with a new ADR."
