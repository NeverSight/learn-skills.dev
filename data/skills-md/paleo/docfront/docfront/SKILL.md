---
name: docfront
description: "Conventions for writing, organizing, and browsing documentation in a docs/ directory using docfront. Use when creating documents, restructuring documentation, or unsure about frontmatter format and file naming conventions."
license: CC0 1.0
metadata:
  author: Paleo
  version: "0.2.4"
  repository: https://github.com/paleo/docfront
---

# Authoring Documentation

All project documentation lives in the `docs/` directory. The `docfront` CLI lets both humans and AI agents discover and read documents without leaving the terminal.

## Browsing with CLI

> Run commands via the project's package manager (e.g. `npm run docfront --`, `pnpm docfront`).

```bash
docfront                                          # list root docs
docfront --dir topic-a --dir topic-b/sub-topic-c  # list subdirectories
docfront --recursive                              # list everything
docfront --read doc-1.md topic-a/doc-2.md         # read documents (frontmatter stripped)
docfront --check                                  # validate all files
```

## Workflow

1. **Understand the Subject** — clarify what needs to be documented. Ask the user if unclear.
2. **Determine Placement** — scan existing docs (`docfront --recursive`). Decide: new file, existing file, which subdirectory. Discuss with the user if unclear.
3. **Write** — follow the conventions below.

## Writing Guidelines

- **Target audience:** an experienced newcomer — someone technically capable but unfamiliar with this specific project.
- Be brief and specific — no obvious information, no generic best practices.
- Typical document: 40–80 lines.
- Prefer referencing source files over large code blocks.
- If the title makes the purpose obvious, omit the `summary`.

## File and Directory Naming

- Use **lowercase-with-dashes** (kebab-case) for new files and directories.
- Uppercase is allowed by the CLI (e.g. `RELEASING.md`).
- Names must be **shell-safe**: no spaces, no quotes, no special characters. The CLI validates this for both files and directories. Use `docfront --check` to verify.
- Use `.md` (Markdown) for all documents.
- Use short, descriptive names.
- Group related documents into subdirectories. Subdirectories can be nested.

## YAML Frontmatter

Every `.md` file **must** start with a YAML frontmatter block with these fields:

| Field | Required | Description |
| --- | --- | --- |
| `title` | Yes | A human-readable display name shown in listings. |
| `summary` | Recommended | One concise sentence. If the title already makes the purpose obvious, omit the summary to avoid redundancy. |
| `read_when` | Recommended | A YAML list of short, action-oriented hints. Each hint completes: *"Read this document when you are…"* |

## Document Body

After the closing `---` of the frontmatter, write standard Markdown. There are no constraints on the body format — use headings, code blocks, tables, and lists as needed.

```markdown
---
title: Your Title Here
summary: A one-sentence description of what this document covers.
read_when:
  - first situation when this document is useful
  - second situation
---

# Your Title Here

Start your content here…
```

## References

- [Installing Docfront CLI](references/installation.md) — how to add docfront CLI to a project.
- [Bootstrapping a docs/ Directory](references/bootstrapping-docs.md) — instructions for creating a `docs/` directory from scratch by exploring the project structure.
- [Migrate Existing Documents](references/migrate-existing-docs) — guide for bringing an existing folder of Markdown documents into docfront conventions (naming, frontmatter).
- [Migrate Skills to Docfront Documentation](references/migrate-skills-to-docfront) — guide for moving internal project documentation from agent skills into `docs/`.
