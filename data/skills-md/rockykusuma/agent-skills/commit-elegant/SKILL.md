---
name: commit-elegant
description: Creates elegant git commits using emoji conventional commit format. Handles pre-commit verification, auto-staging, analyzes diffs for logical grouping, suggests splitting large changes into focused commits, and writes clear imperative commit messages. Use this skill when the user wants to commit changes, stage files, or craft a commit message. Supports --no-verify to skip pre-commit checks.
---

# Commit Elegant

A structured workflow for crafting clean, expressive git commits using emoji conventional commit format.

## Workflow

1. **Pre-commit checks** (skip if `--no-verify` is passed):
   - Detect the project's lint/typecheck/docs commands (check `package.json` scripts, `Makefile`, etc.).
   - Run them. If any fail, show the errors and ask the user: fix first or proceed anyway?
2. **Check staged files** — run `git status`.
   - If files are already staged, only commit those — do not auto-add.
   - If 0 files are staged, run `git add -A` to add all modified and new files.
3. **Diff** — run `git diff --staged` to understand what is being committed.
4. **Analyze** — determine if the diff contains multiple distinct logical concerns (different types, different domains, unrelated files).
5. **Split or single** — if multiple distinct concerns exist, present the proposed split to the user before executing. Otherwise, proceed with one commit.
6. **Commit** — for each commit, write a message in the format below and run `git commit -m "<message>"`.
7. **Verify** — review the committed diff to confirm the message accurately represents the change.

## Commit Message Format

### Subject line (required)
```
<emoji> <type>[(<scope>)][!]: <short imperative description>
```
- `(<scope>)` is optional — use when the change is clearly scoped to a module, package, or domain. Scope must be a noun (e.g., `auth`, `parser`, `ui`).
- `!` is optional — append immediately before `:` to flag a breaking change (e.g., `feat(api)!: remove v1 endpoints`).
- First line ≤ 72 characters.
- Use present-tense, imperative mood: "add feature", not "added feature".
- Do NOT include a `Co-Authored-By` line.

### Body (optional)
Add a body when the "why" is not obvious from the subject alone:
```
<emoji> <type>: <subject>

<body explaining why, not what>

[optional footer(s)]
```
- Separate subject from body with a blank line.
- Wrap body lines at 72 characters.
- Use body for motivation, context, or trade-off reasoning — not restating the diff.

### Footers (optional)
Footers go after the body, separated by a blank line. Common footers:
- `BREAKING CHANGE: <explanation>` — signals a breaking API change (correlates with SemVer MAJOR).
- `Refs: #<issue>` — links to an issue or ticket.
- `Reviewed-by: <name>` — credits a reviewer.
- Footer tokens use `-` instead of spaces (e.g., `Acked-by`), except `BREAKING CHANGE`.
- If `!` is used in the subject, `BREAKING CHANGE:` footer may be omitted.

### SemVer Correlation
- `fix` → PATCH release
- `feat` → MINOR release
- `BREAKING CHANGE` (any type) → MAJOR release

## Emoji + Type Reference

| Emoji | Type | Use for |
|-------|------|---------|
| ✨ | feat | New feature |
| 🐛 | fix | Bug fix |
| 🚑️ | fix | Critical hotfix |
| 🔒️ | fix | Security fix |
| 🚨 | fix | Fix compiler/linter warnings |
| 🩹 | fix | Simple non-critical fix |
| ✏️ | fix | Fix typos |
| 🔇 | fix | Remove logs |
| 🔥 | fix | Remove code or files |
| 📝 | docs | Documentation changes |
| 💡 | docs | Add or update source comments |
| 💄 | style | Formatting/style (no logic change) |
| 🎨 | style | Improve code structure/format |
| ♻️ | refactor | Refactor (no feature, no fix) |
| 🚚 | refactor | Move or rename resources |
| ⚰️ | refactor | Remove dead code |
| ⚡️ | perf | Performance improvement |
| ✅ | test | Add or update tests |
| 🧪 | test | Add a failing test |
| 📸 | test | Add or update snapshots |
| 🔧 | chore | Tooling, configuration |
| 🙈 | chore | Add or update .gitignore |
| 📦️ | chore | Add or update compiled files/packages |
| ➕ | chore | Add a dependency |
| ➖ | chore | Remove a dependency |
| 🔖 | chore | Release/version tag |
| 📌 | chore | Pin dependencies to specific versions |
| 👥 | chore | Add or update contributors |
| 🔀 | chore | Merge branches |
| 👷 | ci | Add or update CI build system |
| 🚀 | ci | CI/CD improvements |
| 💚 | fix | Fix CI build |
| ⏪️ | revert | Revert changes |
| 🗑️ | revert | Remove (deprecated/dead things) |
| 💥 | feat | Introduce breaking changes |
| 🏷️ | feat | Add or update types |
| 🦺 | feat | Add or update validation logic |
| 👔 | feat | Add or update business logic |
| 🌐 | feat | Internationalization/localization |
| 📱 | feat | Responsive design |
| 🚸 | feat | Improve UX/usability |
| ♿️ | feat | Improve accessibility |
| 🔊 | feat | Add or update logs |
| 📈 | feat | Add or update analytics/tracking |
| 🧵 | feat | Multithreading/concurrency |
| 🚩 | feat | Feature flags |
| 🔍️ | feat | Improve SEO |
| 💬 | feat | Add or update text and literals |
| 🥅 | fix | Catch errors |
| 👽️ | fix | Update code due to external API changes |
| 🗃️ | db | Perform database related changes |
| 🏗️ | refactor | Architectural changes |
| 🧑‍💻 | chore | Improve developer experience |
| 🌱 | chore | Add or update seed files |
| 🎉 | chore | Begin a project |
| 📄 | chore | Add or update license |
| 🤡 | test | Mock things |
| ⚗️ | experiment | Perform experiments |
| 🚧 | wip | Work in progress |
| 💫 | ui | Animations and transitions |
| 🍱 | assets | Add or update assets |
| 🥚 | feat | Add or update easter egg |
| ✈️ | feat | Improve offline support |

## When to Split Commits

Split when changes span:
1. **Different concerns** — unrelated parts of the codebase
2. **Different types** — e.g., mixing a feature with a refactor or a test
3. **Different file domains** — e.g., source code vs. CI config vs. documentation
4. **Logical independence** — changes that are easier to understand or review separately
5. **Size** — very large diffs that would be clearer if broken down

When splitting, present the proposed list of commits to the user before executing them.

### How to split mechanically
1. Unstage everything: `git reset HEAD`
2. For each proposed commit, selectively stage the relevant files:
   - `git add <file1> <file2>` for whole files
   - `git add -p <file>` for partial hunks within a file
3. Commit, then repeat for the next group.

## Edge Cases

- **Amend**: If the user says "amend", use `git commit --amend` and rewrite the message to reflect the combined change.
- **Empty commit**: Never create an empty commit unless explicitly requested (`git commit --allow-empty`).
- **Merge commits**: Do not rewrite merge commit messages — leave them as generated by git.
- **Fixup**: If a change is a direct fix to the previous commit, suggest `git commit --fixup=HEAD` for later interactive rebase, or amend if the user prefers.
- **Wrong type**: If a commit was made with the wrong type, suggest `git rebase -i` to reword it before pushing. After push, note that cleanup depends on the team's workflow.
- **Multi-type change**: If a single change conforms to more than one type, always split into multiple commits.

## Examples

Good single commit messages:
```
✨ feat: add user authentication system
🐛 fix: resolve memory leak in rendering process
📝 docs: update API documentation with new endpoints
♻️ refactor: simplify error handling logic in parser
🚨 fix: resolve linter warnings in component files
🧑‍💻 chore: improve developer tooling setup process
👔 feat: implement business logic for transaction validation
🩹 fix: address minor styling inconsistency in header
🚑️ fix: patch critical security vulnerability in auth flow
🎨 style: reorganize component structure for better readability
🔥 fix: remove deprecated legacy code
🦺 feat: add input validation for user registration form
💚 fix: resolve failing CI pipeline tests
📈 feat: implement analytics tracking for user engagement
🔒️ fix: strengthen authentication password requirements
♿️ feat: improve form accessibility for screen readers
```

Good with scope:
```
✨ feat(auth): add JWT-based user authentication
🐛 fix(api): resolve null pointer in user endpoint
♻️ refactor(db): simplify query builder interface
```

Good with `!` breaking change:
```
💥 feat(api)!: remove deprecated v1 endpoints
🔧 chore!: drop support for Node 14
```

Good with body and footer:
```
⚡️ perf: lazy-load dashboard widgets

Reduces initial bundle size by 40%. Widgets now load on scroll
into viewport instead of all at mount time.

Refs: #452
```

Good with breaking change footer:
```
✨ feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used
for extending other config files.
```

Good split sequence:
```
✨ feat: add new solc version type definitions
📝 docs: update documentation for new solc versions
🔧 chore: update package.json dependencies
🏷️ feat: add type definitions for new API endpoints
🧵 feat: improve concurrency handling in worker threads
🚨 fix: resolve linting issues in new code
✅ test: add unit tests for new solc version features
🔒️ fix: update dependencies with security vulnerabilities
```

## Anti-Patterns

Avoid these:
```
# Too vague
🔧 chore: update stuff
🐛 fix: fix bug
✨ feat: changes

# Past tense
🐛 fix: fixed the login issue

# Too long
✨ feat: add user authentication system with JWT tokens and refresh token rotation and session management

# Mixing concerns in one commit
✨ feat: add auth system and fix header styling and update docs

# Meaningless scope
🐛 fix(code): resolve bug
```
