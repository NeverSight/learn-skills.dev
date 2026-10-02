---
name: android-guide
description: Mandatory architecture, folder-structure, naming, and code-quality rules for Android projects. Use this whenever reading, writing, reviewing, or refactoring Kotlin/XML code in an Android app or module.
---

# Android Development Guidelines

You are working on an **Android project**. These guidelines are mandatory — follow them without being reminded.

**First, always detect the project type** (View-based vs. Jetpack Compose, Single-Module vs. Multi-Module) using [rules/1-project-detection.md](rules/1-project-detection.md), then apply the matching rules below.

| File                                                                   | Topic                                                           |
| ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| [rules/1-project-detection.md](rules/1-project-detection.md)           | Detecting View-based vs. Compose and Single vs. Multi-Module    |
| [rules/2-init-general-rule.md](rules/2-init-general-rule.md)           | Agent Bootstrap Guide                                           |
| [rules/3a-view-based-multi-module.md](rules/3a-view-based-multi-module.md)   | View-based Multi-Module Architecture                            |
| [rules/3b-view-based-single-module.md](rules/3b-view-based-single-module.md) | View-based Single-Module Architecture                           |
| [rules/4a-compose-multi-module.md](rules/4a-compose-multi-module.md)   | Jetpack Compose Multi-Module Architecture                       |
| [rules/4b-compose-single-module.md](rules/4b-compose-single-module.md) | Jetpack Compose Single-Module Architecture                      |
| [rules/5-networking.md](rules/5-networking.md)                         | Networking and API layer guidelines                             |
| [rules/6-mapping.md](rules/6-mapping.md)                               | Data mapping guidelines (explicit Kotlin extensions)         |
| [rules/7-local-storage.md](rules/7-local-storage.md)                   | Local storage rules (Room database, SharedPreferences)          |
| [rules/8-code-quality.md](rules/8-code-quality.md)                     | Naming conventions and Kotlin code quality standards            |
| [rules/9-security.md](rules/9-security.md)                             | Security rules (tokens, storage, networking)                    |
| [rules/10-unit-testing.md](rules/10-unit-testing.md)                   | Unit testing rules and patterns (JUnit4 + MockK + Google Truth) |
| [rules/11-code-review.md](rules/11-code-review.md)                     | Code review checklist and reporting rules                       |

## AI Workflow Rules

These rules govern how you operate when assisting in an Android project.

- **Log every AI-made change** to `ai.log` in the project root — one line per change point, format: `[YYYY-MM-DD HH:MM:SS] <brief description>`. Create the file if it does not exist; never overwrite existing entries.
- **Ask the user about any unclear decision** before proceeding. Do not assume ambiguous requirements, architecture choices, or scope. A clarifying question is always cheaper than a wrong implementation.
- **No Force Pushes**: The agent is strictly prohibited from running `git push --force` or `--force-with-lease` automatically. If a push is rejected due to local/remote divergence, the agent MUST pause, explain the conflict, and ask the user for permission to rebase or merge instead of force pushing.
