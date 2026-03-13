---
name: write-conventional-commit
description: Create Git commit messages that conform to Conventional Commits 1.0.0, including type/scope/description format, optional body, trailer-style footers, and explicit BREAKING CHANGE signaling. Use when users ask to draft commit messages, commit current changes, rewrite a commit message into conventional format, or enforce conventional commit standards in a repo.
---

# Write Conventional Commit

Generate and apply Conventional Commits that follow the 1.0.0 specification.

## Workflow

### Step 1: Inspect commit scope

Run from repository root:

```bash
git status --short
git diff --staged --name-only
git diff --name-only
```

Use staged changes when available. If nothing is staged and the user asked to commit now, stage intentionally relevant files first and state what was staged.

### Step 2: Classify intent into commit type

Pick the best type from change intent, not from file extension.

Common types:

- `feat`: add a user-facing feature
- `fix`: fix a bug
- `refactor`: code change without new feature or bug fix
- `perf`: improve performance
- `docs`: documentation only
- `test`: add/update tests
- `build`: build/dependency tooling
- `ci`: CI/CD configuration
- `chore`: maintenance that does not fit above
- `revert`: revert a previous commit

If uncertain between `feat` and `fix`, prefer:

- `fix` when correcting broken behavior
- `feat` when adding new behavior

### Step 3: Choose optional scope

Scope is optional and should be short and stable.

Prefer one of:

- top-level package/app (`api`, `billing`, `auth`)
- subsystem (`migrations`, `deps`, `release`)
- user-visible surface (`checkout`, `search`)

Avoid broad scopes like `misc`.

### Step 4: Detect breaking changes

Mark breaking changes when diff indicates incompatible API/contract behavior.

Signals include:

- removed/renamed public endpoints, fields, events, CLI flags
- required inputs changed incompatibly
- output schema changed incompatibly

When breaking:

1. Add `!` after type or type+scope (`feat!:` or `feat(api)!:`)
2. Add footer: `BREAKING CHANGE: <what changed and how to migrate>`

Use both when possible for clarity.

### Step 5: Compose message in spec format

Use this structure exactly:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Formatting rules:

- Header type must be lowercase noun.
- Put a colon and single space after header prefix.
- Keep description concise and specific.
- Put one blank line between header and body.
- Put one blank line between body and footers.
- Footer tokens follow git trailer style (`Token: value`), except references may use `Token #value`.
- Use `BREAKING CHANGE:` as the canonical breaking footer token.

### Step 6: Create commit (when requested)

If user wants the commit executed, run non-interactively:

```bash
git commit -m "<header>" -m "<body>" -m "<footer1>" -m "<footer2>"
```

Only include `-m` blocks that are needed.

For multiline body/footer with precise formatting, use:

```bash
git commit -F /tmp/commit-msg.txt
```

Then report:

- final commit header
- commit hash
- whether breaking change was marked

## Quality checks

Before finalizing, verify:

- Header matches `<type>[scope][!]: description`
- Type reflects intent correctly
- Scope is helpful or omitted
- Breaking changes are explicitly marked when applicable
- Body explains why when context is not obvious
- Footers are valid trailers and references are accurate

## Output behavior

When user asks only for message suggestions, provide 1 recommended message and up to 2 alternatives.

When user asks to commit directly, proceed with staging/commit commands and then return commit result.

## Reference

Read [references/conventional-commits-1.0.0.md](references/conventional-commits-1.0.0.md) for the normative checklist and examples.
