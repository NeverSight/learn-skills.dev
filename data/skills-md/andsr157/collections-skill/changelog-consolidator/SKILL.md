---
name: changelog-consolidator
description: >-
  Use when the user has changelog documents from multiple frontend modules
  in this VitePress documentation site (each under docs/en/<module>-front/changelog.md,
  git-commit-style logs with hash/author/file/reason/impact) and wants them
  merged into ONE consolidated, high-level changelog grouped by date with a
  breakdown per module. Only consolidates frontend modules — directories
  ending in the "-front" suffix (e.g. fund-front, activity-front) — skipping
  backend, mobile, or other non-front modules even if their changelogs are
  present. Triggers: "gabungkan changelog semua module front", "buat log
  version gabungan module -front", "summarize semua module frontend jadi satu
  changelog per tanggal", or any request to merge multiple per-module
  changelogs into one condensed doc. Key trait: condensation, not
  reformatting — drop file paths, commit hashes, authors, Reason/Impact prose;
  keep only a one-line gist per change, tagged Added/Changed/Fixed/Removed/Other,
  grouped by date then module.
---

# Module Changelog Consolidator

## Purpose

Take changelog documents from every `-front` module in this VitePress
documentation site and merge them into a single Markdown document rendered as a
**three-column table** with one row per date. All modules that shipped changes
on that date appear together inside the `detail` cell, each module getting its
own block of bullets so it stays clear which module each change belongs to:

```
| date       | version | detail |
|------------|---------|--------|
| 2026-06-23 | 1.1     | fund-front<br>Added: short gist of the change<br>Changed: another change<br>activity-front<br>Fixed: short gist of a change in another module |
| 2026-03-13 | 1.2     | fund-front<br>Added: short gist of the change (V1.2) |
```

The `version` column holds a per-date release identifier assigned by the user.
Individual bullets may also carry a module-level version in parentheses at the
end (e.g. `(V1.2)`) when the source module actually has one — most modules log
by git commit and will not include a per-bullet version.

This is a **summarization** task, not a reformatting task. The point is to give
someone a bird's-eye view of "what happened across all modules, on which date,"
without making them read every module's full changelog. Never copy
implementation detail (file names, commit hashes, GitLab/GitHub links, author
names, "Reason:"/"Impact:" paragraphs) into the output — those belong in the
source documents, not in the consolidated view.

## Summarization Principles

This skill generates release notes, not commit logs.

Prioritize information density over completeness.

Summarize changes from the perspective of released capabilities rather than implementation work.

The goal is to answer:

> What changed in this release?

—not—

> What changed in every commit?

Merge related commits whenever they contribute to the same feature, subsystem, architectural improvement, or user-visible capability.

Prefer feature-oriented summaries over commit-oriented summaries.

Do NOT generate one output bullet for every source bullet.

Avoid mentioning implementation artifacts unless they are the primary purpose of the change.

Avoid summarizing around:

- filenames
- directories
- classes
- interfaces
- hooks
- configuration files
- individual Vue components

Instead, summarize the capability or improvement they collectively provide.

## Project Structure

This is a VitePress documentation site with locale-based routing:

```
docs/
├── en/                         ← primary locale (read from here)
│   ├── fund-front/             ← module directory (has -front suffix)
│   │   └── changelog.md        ← the changelog
│   ├── activity-front/
│   │   └── changelog.md
│   ├── credit/                 ← NOT a -front module, skip even if changelog exists
│   │   └── changelog.md
│   └── ...
├── id/                         ← Indonesian locale (skip unless no /en file exists)
│   ├── fund-front/
│   │   └── changelog.md
│   └── ...
└── .vitepress/
```

Only modules whose directory name ends with `-front` are in scope. Currently
the module directories may not yet carry the `-front` suffix; the skill is
designed for when they do. Until then, no modules will match and the
consolidation will produce an empty result — which is expected.

## Workflow

### 1. Identify the source files and their module names

This project hosts changelogs inside locale-namespaced module directories under
`docs/`. **Only ever consolidate modules whose directory name ends with
`-front`** (e.g. `fund-front`, `activity-front`). Any module directory without
the `-front` suffix (e.g. `auth`, `risk`, `lender`) is out of scope and must be
skipped, even if it has a `changelog.md` file.

Use this command to discover candidate modules from the project root:

```bash
find docs/en/ -maxdepth 1 -type d -iname '*-front' -exec test -f '{}/changelog.md' \; -print
```

Only process changelog files from the directories that command returns. The
module name is the directory name as-is (e.g. `fund-front`).

**VitePress i18n locale priority.** Every module has changelogs under both
`docs/en/<module>-front/changelog.md` and `docs/id/<module>-front/changelog.md`
(Indonesian translation). When both exist:

- Read the changelog from `docs/en/<module>-front/changelog.md` only.
- Fall back to `docs/id/<module>-front/changelog.md` for a given module ONLY if
  that module has no `/en` changelog file at all.
- Never read both locales for the same module — `/en` and `/id` are
  translations of each other, so reading both just duplicates every entry.

If a discovered path does not unambiguously belong to a `-front` module, ask
the user — do not guess silently for something that will appear in every
section header.

### 2. Read each file with the right tool

All changelog files in this project are `.md`. Read each one in full. The
structure is consistent across modules:

- `## [<commit-hash>] - YYYY-MM-DD` — dated commit block header
- `### Added` / `### Changed` / `### Fixed` / `### Removed` — category sections
- Each bullet under a category describes a single change with `(Title)`,
  `File:`, `Changes:`, `Reason:`, `Impact:` sub-fields
- A trailing block with `Author:`, `Source:`, `GitLab Commit:` link

### 3. Extract raw entries

For every commit block in a source file, pull out:

- the **date** as written (from the `## [hash] - YYYY-MM-DD` header)
- the **category** (`Added`, `Changed`, `Fixed`, `Removed`)
- the **substance of the change** — primarily from the title in parentheses and the `Changes:` section, extracting only the information necessary to produce a high-level release summary.

Ignore everything that is purely bookkeeping: commit hashes, author emails,
GitLab commit links, `File:` paths, `Reason:` paragraphs, `Impact:` paragraphs,
and the metadata footer block.

### 4. Normalize every date to `YYYY-MM-DD`

The project already uses `YYYY-MM-DD` dates in commit headers, so minimal
normalization is needed. Watch for:

- Indonesian month names in free-form text (`Januari`, `Februari`, `Maret`,
  `April`, `Mei`, `Juni`, `Juli`, `Agustus`, `September`, `Oktober`, `November`,
  `Desember`)
- Two-digit years (`-23` → `2023`, `-24` → `2024`)
- Entries with no real date — use your best judgment to place them near
  neighboring dated entries; never invent a fake precise date.

### 5. Consolidate Related Entries into High-Level Summaries

This is a release note generation task, not a commit extraction task.

Multiple related commits should normally become one summary.

Group changes by their functional purpose rather than where they happened in the codebase.

Prefer grouping by:

- feature
- subsystem
- user-visible capability
- architectural improvement
- infrastructure
- development tooling

Only create separate summaries when the changes are clearly unrelated.

Each summary should answer:

"What capability was added, changed, fixed, or removed?"

instead of

"What files were modified?"

Keep summaries concise while preserving the overall scope of the work.

### Grouping Guidelines

When several entries contribute to the same feature or release objective, summarize them as a single capability instead of listing implementation pieces.

Examples:

routing + menu + navigation

→ Updated application navigation.

API + Axios + service layer

→ Added networking layer.

Jenkins + build + deployment + environment

→ Updated build and deployment infrastructure.

components + hooks + utilities

→ Added reusable frontend components and utilities.

TypeScript + models + interfaces

→ Added frontend data models.

translations + i18n + locale

→ Updated localization support.

CRUD API + validation + models + routes

→ Added <Feature Name> support.

If a feature spans multiple categories (for example API, routing, models, UI, validation, localization), summarize it as a single feature whenever those changes were made to deliver the same capability.

Do not group unrelated features together simply to reduce the number of bullets.

Accuracy is more important than aggressive compression.

### High-Level Summary Examples

Bad

Added:

- Utility functions
- State management
- Router
- Axios
- Layout

Good

Added:

- Implemented the core application architecture, including routing, state management, networking, and layouts.

---

Bad

Added:

- API service
- Model
- Route

Good

Added:

- Added AutoSQLConfig feature, including API services, data models, validation, and routing.

---

Bad

Changed:

- Jenkinsfile
- build.sh
- pom.xml

Good

Changed:

- Updated build and deployment infrastructure.

---

Bad

Changed:

- Translation files
- Menu labels
- Notification text

Good

Changed:

- Updated localization resources and UI labels.

---

Bad

Added:

- Prize page
- Rule page
- Award page
- Dictionary page

Good

Added:

- Added core application pages and business features.

### 6. Build a Structured Entries List

After grouping related changes, build a structured list of consolidated summaries.

Each entry should represent one meaningful release note rather than one source commit whenever possible.

Group changes by:

- feature
- subsystem
- technical area
- infrastructure
- user-visible capability

before creating the final summary.

Example:

```json
[
  {
    "date": "2026-06-23",
    "version": "1.1",
    "module": "activity-front",
    "category": "Changed",
    "description": "Updated build and deployment infrastructure."
  },
  {
    "date": "2026-06-23",
    "version": "1.1",
    "module": "fund-front",
    "category": "Added",
    "description": "Implemented the core application architecture."
  }
]
```

The entries list should contain consolidated release summaries, not individual commit summaries.

### Summary Granularity

Generate as many summaries as necessary to accurately describe the release.

Prefer one summary for an entire feature rather than multiple summaries for its implementation pieces.

Good examples:

Added:

- Added AutoSQLConfig feature, including API services, models, routing, and UI integration.

Changed:

- Updated production deployment pipeline.

Added:

- Implemented the core application architecture.

Avoid summaries such as:

Added:

- Added API service.
- Added router.
- Added model.
- Added validator.
- Added Vue component.

unless those changes belong to completely different features.

### Summary Writing Style

Summaries should describe outcomes rather than implementation.

Prefer:

- Added payment management feature.

instead of

- Added payment page.
- Added payment API.
- Added payment model.

Prefer:

- Updated deployment pipeline.

instead of

- Updated Jenkinsfile.
- Updated pom.xml.
- Updated build.sh.

Write summaries as if they were release notes shown to product managers, QA engineers, or stakeholders rather than developers reviewing commits.

Avoid using implementation-specific terminology unless it is widely recognized or represents the primary feature being delivered.

Prefer describing business capabilities, platform capabilities, or architectural outcomes over internal technical details.

### Category Selection

Choose the category based on the primary outcome of the consolidated summary, not the wording of the original commits.

Use the following guidelines:

- **Added** — Introduces a new feature, capability, integration, page, component, or infrastructure.
- **Changed** — Modifies or improves existing behavior, architecture, configuration, UI, performance, or development workflow.
- **Fixed** — Corrects bugs, broken behavior, regressions, or incorrect functionality.
- **Removed** — Removes or deprecates features, components, routes, or obsolete code.
- **Other** — Use only when none of the above categories accurately describe the change.

When multiple commits are merged into one summary, select the category that best represents the overall outcome of the grouped changes rather than the individual commit actions.

### 7. Render the final document

Group entries by date (newest first). Each date becomes one table row with
three columns: `date`, `version`, and `detail`.

Inside the `detail` cell, group entries by module. Each module gets its name
on its own line, followed by its bullets on subsequent lines. Use `<br>` tags
for line breaks inside the table cell so the Markdown renders correctly:

```

| date | version | detail |
| ---- | ------- | ------ |

```

Write the output to `consolidated-changelog.md` at the project root:

```markdown
# Consolidated Changelog

| date       | version | detail                                                                                                                                                                                                                                                                                                      |
| ---------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-23 | 1.1     | fund-front<br>Added: Added payment channel management feature.<br>Changed: Updated build and deployment infrastructure.<br>activity-front<br>Added: Added AutoSQLConfig feature, including API services, frontend models, validation, and routing.<br>Fixed: Improved localization resources and UI labels. |
| 2026-03-13 | 1.2     | fund-front<br>Added: Improved development environment configuration and build consistency.<br>Changed: Enhanced header language switching experience.                                                                                                                                                       |
```

Rules for the `detail` cell:

- Each module block starts with the module name on its own line (no prefix, no
  bold).
- The module name is followed by its bullets, one per line, each starting with
  `- ` removed and using the `Category: description` pattern.
- Different modules inside the same `detail` cell are separated by a line break
  (the next module name appears directly after the previous module's last
  bullet — no blank line between modules inside the table cell).
- Use `<br>` for every line break within the cell so the raw Markdown table
  stays parseable.

If the user wants oldest-first ordering, reverse the row order so the earliest
date appears first.

### 8. Deliver the result

Present the consolidated output to the user and briefly mention how many source
files and modules were merged and the date range covered. If a module's
changelog used a format the workflow above did not anticipate, say so
explicitly rather than silently dropping entries. If the user asks for `.docx`
or `.pdf`, convert the Markdown output using the **docx** or **pdf** skill
rather than hand-rolling a new format.

## Notes

- If the user adds new modules later, re-run from step 1 with just the new
  files plus the previous `entries.json` (append, do not redo everything).
- If two or more modules changed on the exact same date, each appears as its
  own name-line + bullet block inside the same `detail` cell — never merge
  different modules' bullets into one undifferentiated list.
- Keep each summary concise, typically one sentence, while preserving the overall capability delivered by the grouped changes.
- When the module directories do not yet have the `-front` suffix, the
  consolidation will return zero modules. That is correct and expected behavior
  — the skill is designed to activate once the suffix convention is applied.
- When uncertain whether multiple commits should be merged, prefer grouping them into one high-level release summary if they describe the same capability or feature.
- Prefer fewer high-quality summaries over many low-level summaries when both accurately represent the same release.
