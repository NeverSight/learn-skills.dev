---
name: translate-kit
description: "translate-kit i18n pipeline. Ensures agents run the translation pipeline after modifying user-facing strings. Use when: translate-kit, i18n, internationalization, translatable strings, adding UI text."
---

# translate-kit

Detect projects using translate-kit by checking for `translate-kit.config.ts` in the project root.

## After modifying translatable strings

When you add, modify, or delete user-facing strings in JSX/TSX files, run:

```bash
npx translate-kit run
```

This executes the full pipeline: **scan → codegen → translate**.

| Step | What it does |
|------|-------------|
| `scan` | Parses TSX/JSX, extracts translatable strings, generates semantic keys |
| `codegen` | Replaces raw strings with `t()` calls or `<T>` wrappers in source code |
| `translate` | Sends only new/modified keys to AI, merges with cached translations |

## Do NOT manually edit

These files are generated and managed by translate-kit:

- `.translate-map.json` — text-to-key mapping
- `.translate-lock.json` — translation cache hashes
- `.translate-context.json` — extracted context metadata
- Locale JSON files in the configured messages directory

## Useful commands

```bash
npx translate-kit run               # Full pipeline
npx translate-kit run --dry-run     # Preview without writing
npx translate-kit run --force       # Ignore cache, re-translate everything
npx translate-kit run --locale es   # Only translate a specific locale
npx translate-kit scan              # Scan only
npx translate-kit translate         # Translate only (incremental)
```
