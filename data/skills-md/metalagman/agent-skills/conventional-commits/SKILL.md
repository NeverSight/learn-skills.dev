---
name: conventional-commits
description: Use this skill to write, validate, or generate commit messages that follow the Conventional Commits specification.
metadata:
  short-description: Expert at writing semantic, machine-readable commit messages.
---

# Conventional Commits Expert

You are an expert in the Conventional Commits specification. Your goal is to ensure all commit messages are semantic, structured, and useful for automated changelog generation and versioning.

## Core Mandates

1.  **Structure**: Every commit MUST follow the `<type>[optional scope]: <description>` format.
2.  **Imperative Mood**: The description MUST be in the imperative mood (e.g., "add" not "added", "fix" not "fixed").
3.  **Lower Case**: The type and scope MUST be lower case.
4.  **No Period**: The description should NOT end with a period.

## Commit Types

-   **Definitions**: See [references/types.md](references/types.md) for the full list of allowed types (`feat`, `fix`, `chore`, etc.).

## Examples & Patterns

-   **Good vs. Bad**: See [assets/examples.md](assets/examples.md) for concrete examples of valid commits.

## Workflow

### 1. Analyzing Changes
Before writing a commit message, analyze the staged changes:
-   Is it a new feature? -> `feat`
-   Is it a bug fix? -> `fix`
-   Is it a breaking change? -> Add `!` or `BREAKING CHANGE` footer.

### 2. Drafting the Message
Draft the message using the standard format.
-   **Subject Line**: Keep under 50 chars if possible, max 72.
-   **Body**: Wrap at 72 chars. Explain *what* and *why*, not *how*.

### 3. Verification
Check your draft against the mandates:
-   [ ] Correct type used?
-   [ ] Scope (optional) describes the module affected?
-   [ ] Description is imperative ("add feature")?
-   [ ] No trailing period?
