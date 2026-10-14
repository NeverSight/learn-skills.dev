---
license: MIT
name: prek
description: >
  Onboard prek (Rust-powered pre-commit) into any project and suggest hooks
  tailored to the language/framework. Use when the user says "add prek",
  "set up pre-commit hooks", "configure prek", "what hooks should I use",
  or when you notice a project without a prek.toml that would benefit from
  pre-commit checks. Also trigger when the user wants to add new hooks to
  an existing prek.toml, audit their hook config, or migrate from
  pre-commit to prek. Covers Rust, Python, TypeScript/JavaScript, Go,
  Ruby, and Shell projects.
  Do NOT use for husky, lint-staged, or CI pipeline hook configuration — this skill is specifically for prek.
---

# prek

Onboard and configure [prek](https://prek.j178.dev/) — a fast, Rust-powered pre-commit hook manager.

## When to use

- Project has no `prek.toml` and would benefit from pre-commit hooks
- User wants to add/audit/extend hooks in an existing `prek.toml`
- User is migrating from `.pre-commit-config.yaml` to prek's native TOML format

## Protocol

### 1. Detect project type

Scan the repo root for language markers:

| Marker file | Language/Framework |
|---|---|
| `Cargo.toml` | Rust |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `package.json` | TypeScript/JavaScript |
| `go.mod` | Go |
| `Gemfile` | Ruby |
| `*.sh`, `zsh/`, `bin/` | Shell |
| `Dockerfile` | Docker |

Multiple markers = polyglot project. Suggest hooks for all detected languages.

### 2. Check existing config

- If `prek.toml` exists, read it and identify what's already configured
- If `.pre-commit-config.yaml` exists, offer to migrate (prek reads YAML natively, but TOML is the native format with more features like glob patterns)

### 3. Suggest hooks

Present hooks in categories. Show what each hook does before adding. Use this reference:

#### Built-in hooks (repo = "builtin")

Fast, offline, zero-setup. Always suggest these as the foundation:

| Hook ID | What it does |
|---|---|
| `trailing-whitespace` | Trims trailing whitespace. Args: `--markdown-linebreak-ext=md` |
| `end-of-file-fixer` | Ensures files end with a newline |
| `check-yaml` | Validates YAML syntax. Args: `--allow-multiple-documents` |
| `check-toml` | Validates TOML syntax |
| `check-json` | Validates JSON syntax (rejects duplicate keys) |
| `check-json5` | Validates JSON5 syntax |
| `check-xml` | Validates XML syntax |
| `check-merge-conflict` | Detects unresolved merge conflict markers |
| `detect-private-key` | Catches accidentally committed private keys |
| `check-added-large-files` | Blocks large files. Args: `--maxkb=1024` |
| `check-case-conflict` | Detects filenames that differ only by case |
| `check-symlinks` | Validates symlinks point to existing targets |
| `check-executables-have-shebangs` | Ensures executable scripts have shebangs |
| `mixed-line-ending` | Detects mixed line endings (LF vs CRLF) |
| `fix-byte-order-marker` | Removes UTF-8 BOM |
| `no-commit-to-branch` | Blocks direct commits to protected branches |

#### Language-specific hooks (community repos)

**Rust:**

```toml
# Local hooks (no external repo needed)
[[repos]]
repo = "local"

[[repos.hooks]]
id = "cargo-fmt"
name = "cargo fmt"
language = "system"
entry = "cargo fmt --"
files = "\\.rs$"
pass_filenames = true

[[repos.hooks]]
id = "cargo-clippy"
name = "cargo clippy"
language = "system"
entry = "cargo clippy --all-targets --all-features -- -D warnings"
files = "\\.rs$"
pass_filenames = false
always_run = true
```

**Python:**

```toml
# Ruff (linter + formatter)
[[repos]]
repo = "https://github.com/astral-sh/ruff-pre-commit"
rev = "v0.11.6"
hooks = [
  { id = "ruff", args = ["--fix"] },
  { id = "ruff-format" },
]
```

**TypeScript/JavaScript:**

```toml
[[repos]]
repo = "local"

[[repos.hooks]]
id = "eslint"
name = "eslint"
language = "system"
entry = "npx eslint --fix"
files = "\\.(ts|tsx|js|jsx)$"
pass_filenames = true

[[repos.hooks]]
id = "prettier"
name = "prettier"
language = "system"
entry = "npx prettier --write"
files = "\\.(ts|tsx|js|jsx|json|css|md)$"
pass_filenames = true
```

**Go:**

```toml
[[repos]]
repo = "local"

[[repos.hooks]]
id = "go-fmt"
name = "go fmt"
language = "system"
entry = "gofmt -w"
files = "\\.go$"
pass_filenames = true

[[repos.hooks]]
id = "go-vet"
name = "go vet"
language = "system"
entry = "go vet ./..."
pass_filenames = false
always_run = true
```

**Shell:**

```toml
[[repos]]
repo = "https://github.com/shellcheck-py/shellcheck-py"
rev = "a23f6b85d0fdd5bb9d564e2579e678033debbdff"
hooks = [
  { id = "shellcheck" },
]
```

### 4. Fetch latest versions

Before writing config, check the community hook repos for their current recommended versions (ruff-pre-commit, shellcheck-py, etc.) — via the Context7 MCP if your harness has it, your harness's doc-lookup tool, or the repos' GitHub releases pages. Fall back to the versions listed above if no lookup is available.

### 5. Generate or augment prek.toml

**New project**: Generate a complete `prek.toml` with:

1. Built-in hooks (always include: `trailing-whitespace`, `end-of-file-fixer`, `check-merge-conflict`, `detect-private-key`, `check-added-large-files`)
2. Language-specific hooks based on detection
3. Comments explaining each section

**Existing project**: Show a diff of what would be added. Don't duplicate hooks already present.

### 6. Install and verify

Ask the user before running these commands. For an audit or a proposed config change, stop at the proposed diff and do not run either command unless the user authorizes installation or a mutating run:

```bash
prek install
prek run --all-files
```

If `prek` isn't installed, tell the user to install it (`cargo install prek` or `brew install prek`). Keep installation advice scoped to this repository; do not edit personal package manifests or dotfiles.

## Advanced options

### Stage-specific hooks

Slow checks (tests, full builds) belong on `pre-push`, not `pre-commit`:

```toml
[[repos.hooks]]
id = "pytest"
name = "Run tests"
language = "system"
entry = "pytest -x"
pass_filenames = false
always_run = true
stages = ["pre-push"]
priority = 100
```

`stages = ["pre-push"]` alone does not install a pre-push Git shim. Add `default_install_hook_types = ["pre-commit", "pre-push"]` to the top-level config (verify the key name against the prek docs), then ask the user to rerun the authorized `prek install` so Git installs the pre-push shim. `prek run --hook-stage pre-push` runs the stage but does not prove the shim itself is installed.

### Global filters

Exclude vendored/generated code from all hooks:

```toml
exclude = "^(vendor/|generated/|node_modules/)"
```

### Glob patterns (prek-only)

Prek supports glob patterns as an alternative to regex (not compatible with upstream pre-commit):

```toml
files = { glob = "src/**/*.py" }
exclude = { glob = ["vendor/**", "dist/**"] }
```

## Migration from pre-commit

If `.pre-commit-config.yaml` exists:

1. prek reads YAML natively — the existing config works as-is
2. Offer to convert to `prek.toml` for access to prek-only features (glob patterns, `repo: builtin`)
3. Replace `repo: https://github.com/pre-commit/pre-commit-hooks` with `repo: builtin` where hooks are supported

## What You Don't Do

- Configure CI pipelines, GitHub Actions, or other CI hook systems
- Manage husky, lint-staged, or pre-commit (Python) configs
- Remove existing hooks without user confirmation
- Modify `.pre-commit-config.yaml` directly — only generates `prek.toml`

## Gotchas

- Context7 may be unavailable — fall back to training data for hook recommendations
- `prek run --all-files` can fail on first run if auto-fix hooks reformat everything
- Rev pinning in `prek.toml` goes stale — recommend periodic updates
- `prek install` needs write access to `.git/hooks/` — fails in worktrees with shared hooks
