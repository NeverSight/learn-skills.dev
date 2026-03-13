---
name: format-commit-message
description: Generate standardized conventional commit messages with Claude Code attribution. Use when creating automated commits, release commits, or any git commit requiring consistent formatting.
---

# Format Commit Message

Generate conventional commit messages following project standards with proper attribution.

## When to Use

- Release commits
- Automated version updates
- Refactoring commits
- Any commit requiring consistent formatting
- Documentation updates

## Instructions

### Step 1: Gather Commit Information

Collect required information for commit message.

**Expected Input**:
- `type`: String (feat|fix|chore|docs|refactor|test|style|perf)
- `scope`: String (optional, e.g., "auth", "api", "ui")
- `description`: String (brief description)
- `body`: String (optional, detailed explanation)
- `breaking`: Boolean (optional, is this a breaking change?)

### Step 2: Format Message

Apply conventional commit format with project standards.

**Format Structure**:
```
{type}({scope}): {description}

{body}

{footer}
```

**Footer Template**:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Breaking Changes**:
If `breaking: true`, prepend "BREAKING CHANGE: " to body or add as footer.

### Step 3: Validate Message

Ensure message follows guidelines.

**Validation Rules**:
- Type must be valid (feat|fix|chore|docs|refactor|test|style|perf)
- Description must be present and < 72 characters
- Description should be lowercase and no period at end
- Scope should be lowercase if present
- Body should be wrapped at 72 characters if present

### Step 4: Return Formatted Message

Return complete commit message ready for git commit.

**Expected Output**:
```
feat(auth): add OAuth2 authentication support

Implemented OAuth2 flow with token refresh and secure storage.
Supports Google and GitHub providers.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Error Handling

- **Invalid Type**: Return error listing valid types
- **Missing Description**: Return error requesting description
- **Description Too Long**: Return error with character count
- **Invalid Format**: Describe format issue

## Examples

### Example 1: Simple Feature Commit

**Input**:
```json
{
  "type": "feat",
  "description": "add dark mode toggle"
}
```

**Output**:
```
feat: add dark mode toggle

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 2: Scoped Fix with Body

**Input**:
```json
{
  "type": "fix",
  "scope": "api",
  "description": "resolve memory leak in connection pool",
  "body": "Connection pooling was not properly releasing connections after timeout. Implemented automatic cleanup and connection recycling."
}
```

**Output**:
```
fix(api): resolve memory leak in connection pool

Connection pooling was not properly releasing connections after
timeout. Implemented automatic cleanup and connection recycling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 3: Breaking Change

**Input**:
```json
{
  "type": "feat",
  "scope": "api",
  "description": "migrate to v2 authentication API",
  "breaking": true,
  "body": "Updated authentication to use new v2 endpoints with improved security."
}
```

**Output**:
```
feat(api): migrate to v2 authentication API

BREAKING CHANGE: Updated authentication to use new v2 endpoints with
improved security. All clients must update authentication tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 4: Release Commit

**Input**:
```json
{
  "type": "chore",
  "scope": "release",
  "description": "bump version to 0.8.0"
}
```

**Output**:
```
chore(release): bump version to 0.8.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Validation

- [ ] Formats all conventional commit types correctly
- [ ] Handles optional scope properly
- [ ] Wraps long descriptions and bodies
- [ ] Includes Claude Code attribution
- [ ] Formats breaking changes correctly
- [ ] Validates input fields

## Supporting Files

- `template.md`: Commit message template reference (see Supporting Files section)
