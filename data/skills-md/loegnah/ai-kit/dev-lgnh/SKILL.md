---
name: dev-lgnh
description: "Developer workflow runner (code implementation, simplification, refactoring, code review)."
disable-model-invocation: true
---

# DEV-LGNH Skill Runner

Execute developer workflows (implementation, refactoring, code review, simplification) when invoked with `/dev-lgnh <keyword>` or matching workflow intent.

## Rules

- NEVER run `glob`, `grep`, or directory listings to explore or verify catalog files.
- Read the exact relative file path (`catalog/<filename>.md`) directly.

## Workflow Dispatcher

Match the user's keyword or intent against the workflows below:

| Keywords / Intent                                          | Target Workflow              | Catalog File                     |
| :--------------------------------------------------------- | :--------------------------- | :------------------------------- |
| `implement`, `subagent-impl`, `parallel-impl`              | Subagent Implementation      | `catalog/implement.md`           |
| `simplify`                                                 | Simplify Code                | `catalog/simplify/SKILL.md`      |
| `simplify-fast`, `fast-simplify`                           | Fast Code Simplify           | `catalog/simplify/SKILL-fast.md` |
| `superpowers`                                              | Superpowers Catalog Workflow | `catalog/superpowers/INDEX.md`   |
| `mattpocock`, `matt`                                       | Matt Pocock Catalog Workflow | `catalog/mattpocock/INDEX.md`    |
| `pstack`                                                   | Pstack Catalog Workflow      | `catalog/pstack/INDEX.md`        |
| `grill`, `grill-me`, `grilling`                            | Relentless Interview         | `catalog/mattpocock/INDEX.md`    |
| `code-review`, `review-diff`, `review`                     | Two-Axis Code Review         | `catalog/mattpocock/INDEX.md`    |
| `handoff`                                                  | Session Handoff Document     | `catalog/mattpocock/INDEX.md`    |
| `refactor`, `ts-refactor`, `refactor-ts`, `style-refactor` | Style Refactor               | `catalog/refactor/SKILL.md`      |
| `no-edit`, `edit-no`                                       | No-Edit Mode                 | `catalog/no-edit.md`             |

## Execution Procedure

1. **Match Workflow**: Identify the catalog file from the table above.
2. **Read Catalog Directly**: Read `catalog/<filename>.md` directly using relative path.
3. **Execute Steps**: Follow the instructions in the catalog file sequentially.

## Fallback / No-Keyword Behavior

If invoked without a keyword (`/dev-lgnh` only) or if no workflow matches:

- Print the table above to guide available commands and ask the user to choose.
- Do not read any catalog files or inspect directories.
