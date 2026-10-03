---
name: aim-common-rules
description: UNNC AIM team's repository and code standards. Covers repository naming (competition / aim- academic-year / reusable), branch and Conventional Commits rules, AI-agent git behavior (never commit / push unless the user explicitly asks in the current task; never call the gh CLI without explicit permission; never add an AI Co-Authored-By trailer; suggest a commit message at the end of a code-changing task), and formatting standards for Python (autopep8 / PEP 8), C++ (clang-format / clang-tidy), TypeScript (Prettier + ESLint, pnpm), Go (gofmt), CMake, and Markdown / YAML / JSON, with ready-to-copy canonical rule files. Use when creating or naming a repository, validating a ROS2 package.xml name, creating a branch, writing a git commit message, on any task that could involve committing, pushing, or calling gh, composing a competition workspace (git submodules under src/), or setting up Python, C++ (.clang-format / setup.cfg / .clang-tidy), TypeScript (Prettier / ESLint / pnpm) or Go (gofmt) tooling, styling a CMakeLists.txt or Markdown / YAML / JSON files, or applying the team's recommended git configuration.
---

# UNNC AIM Team — Repository & Code Standards

This skill is the **single entry point** for the team's standards. It consolidates and operationalizes the written rules that live in the org repo [`unnc-aim/.github`](https://github.com/unnc-aim/.github) under `profile/`:

- Repository naming / branch / commit rules ← [`profile/README.md`](https://github.com/unnc-aim/.github/blob/main/profile/README.md)
- C++ standard ← [`profile/standard.cpp.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.cpp.md)
- Python standard ← [`profile/standard.py.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.py.md)
- TypeScript / Go / CMake standards ← [`profile/standard.ts.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.ts.md) / [`standard.go.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.go.md) / [`standard.cmake.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.cmake.md)
- Docs style (Markdown / YAML / JSON) ← [`profile/standard.docs.md`](https://github.com/unnc-aim/.github/blob/main/profile/standard.docs.md)

Those written docs remain the source of truth; this skill (which lives in [`unnc-aim/aim-common-agentic-skills`](https://github.com/unnc-aim/aim-common-agentic-skills)) turns them into actionable checklists plus ready-to-copy rule files (`assets/`).

> **Language rule for generated artifacts:** documentation prose is language-agnostic, but **all code, code comments, and commit messages must be in American English** (e.g. `color`, `behavior`, `optimize` — not *colour*, *behaviour*, *optimise*).

## Where to look

| Task | Read | Copy this file |
| --- | --- | --- |
| Create / name a repo, validate a ROS2 package name | [references/repo-naming.md](references/repo-naming.md) | — |
| Clone & organize a competition **workspace** (git submodules) | [references/workspace-organization.md](references/workspace-organization.md) | — |
| Create a branch, write a commit message, follow the agent git-safety rules, set up recommended git config | [references/git-workflow.md](references/git-workflow.md) | [assets/.gitattributes](assets/.gitattributes) |
| Format / configure **Python** | [references/python-formatting.md](references/python-formatting.md) | [assets/setup.cfg](assets/setup.cfg) |
| Format / configure **C++** | [references/cpp-formatting.md](references/cpp-formatting.md) | [assets/.clang-format](assets/.clang-format) + [assets/.clang-tidy](assets/.clang-tidy) |
| Format / configure **TypeScript** (Prettier, ESLint, pnpm) | [references/ts-formatting.md](references/ts-formatting.md) | [assets/.prettierrc](assets/.prettierrc) + [assets/eslint.config.js](assets/eslint.config.js) |
| Format **Go** | [references/go-formatting.md](references/go-formatting.md) | — |
| Style a **CMakeLists.txt** | [references/cmake-style.md](references/cmake-style.md) | — |
| Markdown / YAML / JSON style (`.editorconfig`) | [references/docs-style.md](references/docs-style.md) | [assets/.editorconfig](assets/.editorconfig) |
| Set up **VS Code** (extensions, Pylance, format-on-save, spelling) | [references/python-formatting.md](references/python-formatting.md) §3, §5, §6 + `profile/README.md` §1.6 | [assets/.vscode/extensions.json](assets/.vscode/extensions.json) + [assets/.vscode/settings.json](assets/.vscode/settings.json) |

## Naming quick reference (most-used — read this first)

| Repo type | Pattern | Separator | Example |
| --- | --- | --- | --- |
| **Competition** (one year / one match / one robot) | `[2-digit year][match abbr]_[robot (optional)]_[package]` | underscore `_` | `26RC_R2_controller`, `26RC_interfaces`, `26UL_Sentry_ws` |
| **Internal / academic-year** (non-competition) | `aim-[4-digit year]-[package]` (long-term libs may drop the year) | hyphen `-` | `aim-2526-py-coursework`, `aim-rookie-courses` |
| **External / reusable / lib** | `BrandingRepo` or `package_name` | free | `RoboMark`, `ros2_hik_camera` |

- Year/match tokens: `26RC` = 2026 Robocon; `25RM` = 2025 RoboMaster; `2526` = academic year 2025-2026 (only in `aim-*`).
- **Segment casing:** 2-digit year (`26`); match abbreviation ALL CAPS (`RC` / `UC` / `UL`); robot name, when present, run-together PascalCase (`Sentry`, `NormalHero`, `R1`); package segment lowercase `snake_case`.
- **ROS2 package-name consistency:** if the repo is a single ROS package, the `<name>` in `package.xml` must match the repo's "package" segment; prefixes like `ros2_` are usually **dropped** in `<name>` (e.g. `ros2_hik_camera` → `<name>hik_camera</name>`).
- Default branch is always `main` (**never** `master`); competition / stable repos must not push directly to `main` — use a Pull Request.

> Full rules, decision tree, and known inconsistencies: [references/repo-naming.md](references/repo-naming.md).

## Commit message quick reference (Conventional Commits)

```text
<type>(<scope>): <subject>
<blank line>
<body>           # optional, wrap at <=72 chars
<blank line>
<footer>         # optional: BREAKING CHANGE: ... / Closes #123
```

`type` ∈ `feat | fix | docs | style | refactor | test | chore | perf | ci | build`; `subject` ≤ 50 chars, imperative mood, lowercase first letter, no trailing punctuation. Details: [references/git-workflow.md](references/git-workflow.md).

**Agent rules:** never run `git commit` / `git push` unless the user explicitly asks in the current task, never call the `gh` CLI without explicit permission (any subcommand), never add an AI `Co-Authored-By:` trailer to any commit, and after any code-changing task suggest a commit message — one line, ≤50 chars including the type prefix, American English — instead of committing. Details: [references/git-workflow.md](references/git-workflow.md) §5.

**The committer is you, AI or not:** credit for what your AI gets right and blame for what it gets wrong both land on you, the user — so review the diff and commit yourself, with no AI co-author trailer. Policy: [references/git-workflow.md](references/git-workflow.md) §0.

## How members adopt this skill

This skill lives in [`unnc-aim/aim-common-agentic-skills`](https://github.com/unnc-aim/aim-common-agentic-skills). Install it with the open [skills](https://github.com/vercel-labs/skills) CLI (`npx skills`), which auto-detects every local agent (Claude Code / Cursor / Codex / …) and installs the whole skill directory for all of them:

```bash
npx skills add unnc-aim/aim-common-agentic-skills --skill aim-common-rules -g
```

- `-g` installs globally (every project you open — recommended for individuals); omit `-g` to install into the current project's `.agents/skills/` (recommended for competition / collaborative repos — commit it so the whole team gets it on clone).
- Update later with `npx skills update`.

> Prefer a manual copy? `cp -R` the whole skill directory into `~/.claude/skills/` (global) or `<your-repo>/.claude/skills/` (per repo). The directory — `SKILL.md` + `references/` + `assets/` — must travel together.

**Whether or not you use AI**, copy the canonical formatting rule files into **your repo root** and commit them, so everyone's editors / CI agree:

| Language | Copy as | Source |
| --- | --- | --- |
| C++ | `.clang-format` and `.clang-tidy` | [assets/.clang-format](assets/.clang-format), [assets/.clang-tidy](assets/.clang-tidy) |
| Python | the `[flake8]` / `[autopep8]` / `[isort]` sections of `setup.cfg` (merge in — do not overwrite ROS `[develop]`/`[install]`) | [assets/setup.cfg](assets/setup.cfg) |

> Members not using AI: just read `references/*.md` and copy `assets/` — no Claude Code required.

## Repo setup — proactively offer editor config

When you help create or set up a repo (a new project, or onboarding an existing one), **proactively offer** to add the team's VS Code config under `.vscode/` so everyone who opens the repo gets the same extensions, formatting, and spelling baseline. Templates: [assets/.vscode/extensions.json](assets/.vscode/extensions.json) + [assets/.vscode/settings.json](assets/.vscode/settings.json).

- **Ask first.** Propose it (e.g. *"Want me to add `.vscode/extensions.json` + `.vscode/settings.json` with the team's editor config?"*) and write files only on confirmation — never silently create files in the user's repo.
- **Merge, don't overwrite.** If `.vscode/extensions.json` or `.vscode/settings.json` already exists, merge by hand (add missing extension IDs to `recommendations`; append missing settings / `cSpell.words`) instead of replacing.
- **Or just install locally.** If the user prefers not to commit the files, offer to run `code --install-extension <id>` per extension (after confirming), or point them to the list in `profile/README.md` §1.6.
- **Spelling (Code Spell Checker).** When `cSpell` flags a word, first check whether it is a real typo; if it is a correct term spelled in **American English** (team / domain jargon, acronym, proper noun), add it to the `cSpell.words` array in `.vscode/settings.json`. Do not disable the checker or leave genuine typos in place.

`settings.json` also carries format-on-save + isort + Pylance (see [references/python-formatting.md](references/python-formatting.md) §3 / §5 / §6).

## Key gotchas

- **clang-format only does layout, not naming.** C++ naming rules (functions `snake_case` / variables `camelBack` / classes `PascalCase` / macros & constants `UPPER_CASE` / structs `_t`) are enforced by human review or the provided `.clang-tidy`. See [references/cpp-formatting.md](references/cpp-formatting.md).
- The vendored `ros2_hik_camera/.clang-tidy` uses `lower_case` variables, which **conflicts** with the written `standard.cpp.md` (`camelBack`). New repos follow the written standard; the team should reconcile. Details in cpp-formatting.md.
- Python line length is **79** (matches the `autopep8` default used in `aim-py-2526-courseworks` CI). Changing it to 99/100 would break that repo's CI.
- **autopep8 does not sort imports.** Sort them with **isort** (`line_length = 79`; see [references/python-formatting.md](references/python-formatting.md) §5), and run it **before** autopep8. The `aim-py-2526-courseworks` CI runs only autopep8, so isort is a recommended addition, not yet gated.
- `standard.cpp.md` examples show 4-space indent, but the team's actual `.clang-format` (Google base) uses **2 spaces** — the `.clang-format` wins.
- **Inside a competition workspace** (`*_ws`, e.g. `26RC_R2_ws`): add competition-prefixed repos as git submodules under `src/` with the prefix **stripped** (`26RC_R2_arm_controller` → `src/arm_controller`). The prefix is redundant — the workspace name already carries the year/match/robot. See [references/workspace-organization.md](references/workspace-organization.md).
