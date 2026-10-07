---
name: coding-standards
description: Enforce language-specific coding standards (Python/TS/JS/Go/Rust/C/C++) + PR/commit conventions.
license: Apache-2.0
---

# Coding Standards

You enforce coding standards by detecting the project language and applying the correct style guide.

## Step 1 — Detect the language

Look at the file extensions, project config files, and context of the user's request to determine the primary language.

## Step 2 — Fetch the right guide

Based on the detected language, fetch and read the corresponding style guide using `WebFetch`:

| Language | Guide | URL |
|----------|-------|-----|
| Python | Google Python Style Guide | `https://raw.githubusercontent.com/google/styleguide/refs/heads/gh-pages/pyguide.md` |
| TypeScript | Anthony Fu's ESLint Config | `https://eslint-config.antfu.me/rules` |
| Go | Uber Go Style Guide | `https://raw.githubusercontent.com/uber-go/guide/refs/heads/master/style.md` |
| Rust | Rust API Guidelines | `https://rust-lang.github.io/api-guidelines/print.html` |
| C / C++ | LLVM Coding Standards | `https://llvm.org/docs/CodingStandards.html` |
| JavaScript | Airbnb JavaScript Style Guide | `https://raw.githubusercontent.com/airbnb/javascript/refs/heads/master/README.md` |

## Step 3 — Satisfy the user's request

Use the fetched guide as your reference to do what the user asked — whether that's reviewing code, fixing style issues, refactoring, or writing new code that follows the standard.

Always cite the specific rule or section from the guide when making suggestions.

## Commit messages

When writing commit messages, follow Conventional Commits:

Commit messages must be:

- **Single line** — header only, no body unless absolutely necessary
- **Short** — 72 character max (`header-max-length`)
- **Minimal** — state what changed, nothing more
- **Conventional** — `type(scope): subject` format (e.g. `fix(api): handle null response`)

Good: `feat(auth): add jwt refresh` | Bad: `Added a new feature that refreshes the JWT token when it expires`
