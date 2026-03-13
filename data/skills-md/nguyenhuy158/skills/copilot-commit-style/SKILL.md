---
name: copilot-commit-style
description: Use this skill when the user asks to write, generate, draft, or format a git commit message. It enforces the Conventional Commits specification with mandatory emojis and strict formatting rules.
---

# Copilot Commit Style Instructions

This skill provides the mandatory rules for formatting git commit messages according to the project's Conventional Commits specification.

## Commit Message Format

Every commit message **MUST** follow this exact format:

```
<emoji> <type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Constraints:
* **Emoji is REQUIRED**: Every commit must start with a relevant emoji.
* **Scope is REQUIRED**: You must specify a scope in parentheses. Format: `type(scope): description`.
* **Lowercase Types**: `<type>` must be in lowercase.
* **Separation**: A colon and space must follow the scope.
* **Single Line Only**: The commit header must be a single line. No newline characters within the header.
* **Length Limit**: The entire commit header (including emoji and scope) must be **less than 80 characters**.

---

## Allowed Types & Emojis

| Emoji | Type | Meaning | SemVer |
| :--- | :--- | :--- | :--- |
| ✨ | `feat` | New feature | `MINOR` |
| 🐛 | `fix` | Bug fix | `PATCH` |
| 📝 | `docs` | Documentation changes | None |
| 🎨 | `style` | Formatting, missing semi-colons, etc. | None |
| ♻️ | `refactor` | Code change that neither fixes a bug nor adds a feature | None |
| ⚡️ | `perf` | Code change that improves performance | `PATCH` |
| ✅ | `test` | Adding missing tests or correcting existing tests | None |
| 👷 | `build` | Changes that affect the build system or external dependencies | None |
| 💚 | `ci` | Changes to CI configuration files and scripts | None |
| 🔧 | `chore` | Other changes that don't modify src or test files | None |
| ⏪ | `revert` | Reverts a previous commit | None |

**Note:** A **BREAKING CHANGE** (which triggers a `MAJOR` version bump) is signaled by adding a `!` after the type/scope or by including `BREAKING CHANGE:` in the footer.

---

## Examples

✅ **Correct Format:**
- `✨ feat(auth): add OAuth2 login flow`
- `🐛 fix(api): resolve memory leak in worker`
- `📝 docs(readme): update installation guide`
- `⚡️ perf(db)!: optimized query for user lookup`

❌ **Incorrect Format:**
- `feat: add something` (Missing scope and emoji)
- `✨ feat: add something` (Missing scope)
- `feat(ui): add something` (Missing emoji)
- `✨ fix memory leak` (Missing type/scope format)
- `⚡️ fix(stock): very long description that exceeds the character limit of eighty characters per line` (Over 80 chars)
- `🐛 fix(api): first line\nsecond line` (Contains multiple lines in header)

## Links
- [Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification)
