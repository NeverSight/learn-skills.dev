---
name: commit
description: Create a git commit with a well-crafted conventional commit message. Use when the user asks to commit, create a commit, or says something like "commit this".
model: haiku
allowed-tools: Bash(git:*), Bash(fmt:*), Read
---

# Commit

Create conventional commit messages that explain the **why**, not the what.

The commit message helps:
- The **PR reviewer** understand the context quickly
- The **devs in 6 months** who will `git blame` this code

## Workflow

### 1. Get the staged diff

```bash
git diff --cached
```

If nothing is staged, stop and tell the user to stage changes first.

### 2. Get existing scopes

Extract scopes already used in the project to stay consistent:

```bash
git log --oneline --no-merges | sed -n 's/^[^ ]* [a-z]*(\([^)]*\)).*/\1/p' | sort | uniq -c | sort -rn
```

Use one of these scopes if it fits. Only invent a new scope if none matches.

### 3. Analyze the diff

Identify:
- Which files are touched
- Which functions/classes/components are modified
- The pattern of the change (addition, deletion, refactoring, fix...)

If needed, use `Read` to explore touched files for better architectural understanding.

### 4. Decide: ask or skip

**Skip questions if the why is obvious:**
- Bug fix with explicit error message
- Typo / formatting
- Adding tests for existing code
- Rename with clear reason in the code
- The conversation already provides full context (e.g. you just helped implement the change)

**Ask 1-2 questions if you need to clarify:**
- Refactoring without a visible problem
- New feature without business context
- Non-obvious technical choice
- Behavior change without an apparent bug

Questions must be **specific to the diff** — mention what you see and ask why:
- "You're migrating from bash to Node.js — was it for performance, maintainability, something else?"
- "You're adding retry with backoff on API X — what was the issue in prod?"
- "You're replacing moment.js with date-fns — bundle size problem?"

Never ask vague questions like "Why this change?" or "What was the problem?".

### 5. Generate the commit message

#### Format

```
type(scope): short description

One or two paragraphs explaining the context and motivation.
Each paragraph is between 125 and 250 characters.
```

#### Rules

- Title < 72 characters, english, lowercase
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`
- Body: 1-2 paragraphs, 125-250 chars each

#### The body explains the WHY

Answer: What problem? Why now? Why this approach?

**Forbidden patterns** (the diff already shows the what):
- "This change/commit introduces/adds/creates..."
- "This refactors/updates/modifies..."
- Any form of "add X, create X, update X, remove X, rename X, refactor X"

### 6. Wrap the body

Do not rely on the LLM to respect line length. Wrap the body (not the title) at 80 characters using `fmt`:

```bash
echo "<body>" | fmt -w 80
```

### 7. Commit

Always use a HEREDOC to avoid escaping issues:

```bash
git commit -F - << 'EOF'
type(scope): description

Wrapped body paragraph.
EOF
```
