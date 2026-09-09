---
name: translate-site
description: >-
  Translate a Rosey-ready site with AI. Covers Rosey locale JSON files
  (untranslated + stale entries) and split-by-directory content collection files
  (MDX/MD with frontmatter). Use when the user wants to translate locale files,
  fill in missing translations, update stale translations, bulk-translate a
  locale, or translate per-locale content directories (blog_fr/, blog_de/).
---

# Translate a Rosey Site with AI

Two translation systems can run on the same site, and this skill covers both:

| Part                                                    | What it holds                                                                                                                                   | Section    |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **Rosey locale JSON** (`rosey/locales/{code}.json`)     | Shared UI and any page text tagged with `data-rosey` — nav, footer, headings, buttons, breadcrumbs, and (for non-split pages) whole page bodies | **Part 1** |
| **Content collection files** (`blog_fr/`, `blog_de/` …) | Split-by-directory body content + per-post frontmatter (title, description, alt text) that the SSG renders natively per locale                  | **Part 2** |

**Most sites only need Part 1.** Only reach for Part 2 if the project actually has per-locale content directories (split-by-directory, set up in the [`make-site-multilingual`](../make-site-multilingual/SKILL.md) skill, Phase 8). A split-by-directory _page_ needs both: its body comes from a content collection file (Part 2), its shared UI from the locale JSON (Part 1).

This skill is written for AI coding agents, but the process works with any AI tool that reads and writes JSON.

## When to use

- Locale files have untranslated entries (`value` still equals `original`)
- A source string changed and its translations are now stale
- A new locale needs bulk-translating from scratch
- Per-locale content directories (`blog_fr/`, `blog_de/`) need their bodies and frontmatter translated

## When not to use

- **The site is not Rosey-ready yet** — no `rosey/base.json`, no `data-rosey` tags. Set it up with [`make-site-multilingual`](../make-site-multilingual/SKILL.md) first; there is nothing here to translate until then.
- **Adding a new locale to the build** — that is a pipeline and config change, also [`make-site-multilingual`](../make-site-multilingual/SKILL.md)
- **Translations come from a human team or an external service** — this skill only covers filling the files with AI

## Contents

| File                                             | Covers                                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **SKILL.md** (this file)                         | Which part applies, and why the file format suits AI translation                    |
| [locale-files.md](locale-files.md)               | **Part 1, most sites need only this** — `rosey/locales/{code}.json`                 |
| [content-directories.md](content-directories.md) | **Part 2** — per-locale content directories, only if the site is split-by-directory |
| [scripts/README.md](scripts/README.md)           | The prepare/merge scripts both parts drive                                          |

## Why Rosey files are ideal for AI

Rosey locale files are flat JSON with a predictable three-field structure per entry. That gives an agent three properties that make translation efficient and safe:

1. **Incremental** — new entries from `write-locales` have `value` set to the source original. Comparing `value` to `original` instantly identifies what's untranslated; already-translated entries are left untouched. No diffing, no external state, no tracking database.
2. **Deterministic / idempotent** — running the same pass twice produces the same output. No re-translation of existing work, reviewable `git diff`.
3. **Context-rich** — keys encode where text appears (`nav:about`, `index:hero:title`, `blog:recent-posts`), which disambiguates short strings ("More", "Back", "Home") without a screenshot.

The data format _is_ the state management: read a JSON file, find entries where `value === original`, translate them, write the file.

## Learnings and Gotchas

> This section is a living document. When you discover new patterns, issues, or improvements while translating, **ask the user** before appending them here. See the repo README's **Key conventions → Living documents**.
