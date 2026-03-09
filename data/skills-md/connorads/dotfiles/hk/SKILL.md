---
name: hk
description: Set up and maintain hk git hook manager in any repository. Use when adding pre-commit hooks, configuring linters, setting up code quality automation, working with hk.pkl, or maintaining existing hook configurations. Triggers on tasks involving hk, git hooks, pre-commit checks, commit-msg validation, or linting pipelines.
---

# hk — Git Hook Manager

[hk](https://hk.jdx.dev) by jdx runs linters and formatters as git hooks with **built-in parallelism**, **file locking** (no race conditions), and **staged-file-only** operation (no separate lint-staged needed). Config is in Pkl — Apple's typed configuration language.

## Mental Model

Every hk setup is three steps: **detect** what the project has → **compose** steps from tiers → **wire** the hooks in.

```
detect project type + tools
         ↓
compose hk.pkl (tiered steps)
         ↓
wire: mise.toml + .hk-hooks/ + prepare script
```

## Setup Workflow

### 1. Detect

```bash
hk --version                    # get current version for amends URL
ls package.json go.mod Cargo.toml pyproject.toml flake.nix Makefile
cat mise.toml package.json      # existing tools, package manager, scripts
```

Identify:
- Language(s) and framework
- Package manager (pnpm/bun/npm/yarn for JS, cargo, go, pip, etc.)
- Formatter already configured (prettier, biome, ruff, gofmt…)
- Linter already configured (eslint, golangci-lint, ruff, clippy…)
- Test runner (vitest, jest, go test, cargo test, pytest…)
- Whether it's a team/shared repo (needs no-commit-to-branch)

### 2. Choose steps (tiered)

**Tier 1 — Universal (always add):**

| Step | Builtin |
|------|---------|
| trailing-whitespace | `Builtins.trailing_whitespace` |
| newlines | `Builtins.newlines` |
| check-merge-conflict | `Builtins.check_merge_conflict` |

**Tier 2 — Common tools (add if relevant):**

| Step | Builtin | When |
|------|---------|------|
| typos | `Builtins.typos` | Always (fast spell check) |
| gitleaks | custom | Always (secret detection) |
| rumdl | `Builtins.rumdl` | If `*.md` files exist |

**Tier 3 — Language-specific** (see `references/builtins-by-language.md`):

| Signal file | Steps to add |
|------------|-------------|
| `package.json` + `biome.json`/`biome.jsonc` | biome (or ultracite), eslint |
| `package.json` (no biome) | prettier, eslint |
| `tsconfig.json` | typecheck (tsc/tsgo/astro check/svelte-check) |
| `go.mod` | go_fmt, go_vet, golangci_lint, gomod_tidy |
| `Cargo.toml` | cargo_fmt, cargo_clippy |
| `pyproject.toml`/`requirements.txt` | ruff (format+lint), mypy |
| `flake.nix`/`*.nix` | nix_fmt (nixfmt), deadnix |
| `*.sh`/`*.zsh` | shfmt, shellcheck |

**Tier 4 — Project-specific (detect from config files):**

| Signal | Step |
|--------|------|
| `commitlint.config.*` exists | commit-msg hook with commitlint |
| `.yamllint*` exists | yamllint |
| Team/shared repo | no-commit-to-branch (pre-commit), no-push-to-branch (pre-push) |
| Test runner detected | test step(s) — vitest/jest/go test/cargo test/pytest |

### 3. Wire the hooks

Four files to create/update:

1. `mise.toml` — add hk, pkl, tool binaries
2. `hk.pkl` — configuration
3. `scripts/quiet-on-success.sh` — noise suppressor (copy from `assets/quiet-on-success.sh` in this skill)
4. `.hk-hooks/pre-commit` — tracked hook wrapper

Then:
```bash
chmod +x scripts/quiet-on-success.sh .hk-hooks/*
git config --local core.hooksPath .hk-hooks
```

And add to `package.json` prepare script (JS projects):
```json
"prepare": "[ -n \"$CI\" ] && exit 0 || command -v hk >/dev/null && (hk install 2>/dev/null || git config --local core.hooksPath .hk-hooks) || echo 'Note: hk not found, skipping git hooks. Install mise to enable.'"
```

For non-JS projects, set `core.hooksPath` manually or via a Makefile `setup` target.

### 4. Validate

```bash
hk check --all      # verify all steps pass on existing files
hk validate         # verify hk.pkl is valid Pkl
```

---

## Preferred Patterns

### hk.pkl global settings

Always use these at the top (after the amends/import lines):

```pkl
exclude = List("node_modules", "dist", ".next", ".git")  // add project-specific dirs
display_skip_reasons = List()   // suppress skip noise
terminal_progress = false        // cleaner output
```

Always use these on the pre-commit hook:

```pkl
["pre-commit"] {
    fix = true        // auto-fix and re-stage
    stash = "git"     // isolate staged changes
    steps { ... }
}
```

### Binary file excludes

Always exclude binary/font files from trailing-whitespace, newlines, and typos:

```pkl
local binary_excludes = List(
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.ico",
    "*.woff", "*.woff2", "*.ttf", "*.eot", "*.pdf", "*.zip"
)

["trailing-whitespace"] = (Builtins.trailing_whitespace) {
    exclude = binary_excludes
}
```

### The quiet-on-success wrapper

Wrap noisy commands so output only appears on failure:

```pkl
["typecheck"] {
    check = "scripts/quiet-on-success.sh pnpm exec tsc --noEmit"
}
```

Copy `assets/quiet-on-success.sh` from this skill directory into `scripts/` in the target repo.

### The .hk-hooks/pre-commit wrapper

This is the file git actually executes. It's tracked in git (unlike `.git/hooks/`):

```sh
#!/bin/sh
# hk pre-commit hook — silent on success, minimal on failure
if [ -n "$CI" ]; then
  exec hk run pre-commit "$@"
fi
output=$(hk run pre-commit "$@" 2>&1)
code=$?
[ $code -ne 0 ] && printf '%s\n' "$output"
exit $code
```

For other hooks (commit-msg, pre-push), use simpler wrappers:

```sh
#!/bin/sh
exec hk run commit-msg "$@"
```

```sh
#!/bin/sh
exec hk run pre-push "$@"
```

---

## Pkl Syntax Reference

### Required first lines

```pkl
amends "package://github.com/jdx/hk/releases/download/v1.36.0/hk@1.36.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v1.36.0/hk@1.36.0#/Builtins.pkl"
```

**Always match the version in `amends` and `import` to the installed hk version** (`hk --version`).

### Builtin step (use as-is)

```pkl
["trailing-whitespace"] = Builtins.trailing_whitespace
```

### Builtin step (with overrides)

```pkl
["trailing-whitespace"] = (Builtins.trailing_whitespace) {
    exclude = List("*.png", "*.jpg")
    batch = true
}
```

### Custom step

```pkl
["typecheck"] {
    glob = List("*.ts", "*.tsx")       // optional: only run when these files staged
    check = "scripts/quiet-on-success.sh pnpm exec tsc --noEmit"
    // fix = "command to auto-fix"     // optional
}
```

### Template variables

| Variable | Value |
|----------|-------|
| `{{files}}` | Space-separated list of staged files matching the step's glob |
| `{{commit_msg_file}}` | Path to commit message file (commit-msg hook only) |
| `{{workspace}}` | Directory containing `workspace_indicator` file |
| `{{workspace_files}}` | Files relative to workspace directory |

### Multi-line inline script

```pkl
["no-commit-to-branch"] {
    check = """
      branch=$(git rev-parse --abbrev-ref HEAD)
      if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
        echo "Direct commits to '$branch' are not allowed."
        exit 1
      fi
      """
}
```

### Local variable (share steps across hooks)

```pkl
local fast_steps = new Mapping<String, Step> {
    ["trailing-whitespace"] = Builtins.trailing_whitespace
    ["shfmt"] = (Builtins.shfmt) { batch = true }
}

hooks {
    ["pre-commit"] { fix = true; stash = "git"; steps = fast_steps }
    ["check"] { steps = fast_steps }
    ["fix"] { fix = true; stash = "git"; steps = fast_steps }
}
```

### Sequential ordering with Groups

Steps within a group run in parallel; groups run sequentially:

```pkl
steps {
    ["format"] = new Group {
        steps = new Mapping<String, Step> {
            ["prettier"] { ... }
            ["eslint"] { ... }
        }
    }
    ["validate"] = new Group {   // runs after format completes
        steps = new Mapping<String, Step> {
            ["typecheck"] { ... }
            ["test"] { ... }
        }
    }
}
```

Or use `depends` for fine-grained ordering:

```pkl
["eslint"] {
    depends = List("prettier")   // waits for prettier to finish
    ...
}
```

---

## mise.toml Additions

```toml
[tools]
hk = "latest"
pkl = "latest"        # required for hk.pkl parsing

# Add as needed based on detected steps:
typos = "latest"      # Tier 2: spell check
gitleaks = "latest"   # Tier 2: secret detection
rumdl = "latest"      # Tier 2: markdown lint (if .md files present)
yamllint = "latest"   # Tier 4: YAML lint (if .yamllint* present)
```

---

## Maintenance

### Add a new step

Insert into `hk.pkl` under the appropriate section. Check `hk builtins` for available built-ins, or write a custom step.

### Update hk version

```bash
hk --version   # check current
```

Bump both URLs in `hk.pkl`:
```pkl
amends "package://github.com/jdx/hk/releases/download/v1.37.0/hk@1.37.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v1.37.0/hk@1.37.0#/Builtins.pkl"
```

### Bypass hooks temporarily

```bash
HK=0 git commit -m "wip"             # skip all hk hooks
HK_SKIP_STEPS=vitest git commit      # skip specific step
```

### Debug a failing step

```bash
hk check -v                          # verbose output
hk check -v --step typecheck         # single step only
hk run pre-commit -v                 # simulate hook run
```

### Local developer overrides

Create `hk.local.pkl` (gitignored) to override settings locally:

```pkl
amends "./hk.pkl"
hooks {
    ["pre-commit"] {
        steps {
            ["vitest"] {
                check = "scripts/quiet-on-success.sh pnpm exec vitest run --testPathPattern=fast"
            }
        }
    }
}
```

---

## Gotchas

| Issue | Fix |
|-------|-----|
| `pkl: command not found` | Add `pkl = "latest"` to `mise.toml`, run `mise install` |
| `amends` version mismatch | Match amends/import URL version to `hk --version` output |
| Builtins snake_case vs step names kebab-case | `Builtins.trailing_whitespace` → `["trailing-whitespace"]` |
| Hook runs but matches nothing | Check glob patterns; use `hk check -v` to see file matching |
| Binary files fail spell check | Add binary excludes to typos/trailing-whitespace/newlines steps |
| Git worktrees: `hk install` fails | Automatic since v1.35.0; if using older version use `.hk-hooks/` + `core.hooksPath` |
| Fix auto-stages wrong files | Use explicit `stage` glob on the step, or ensure step `glob` covers fixed files |
| Noisy output on success | Wrap commands in `scripts/quiet-on-success.sh` |
| Hook runs in CI unnecessarily | Add `[ -n "$CI" ] && exit 0` to `prepare` script |
| `hk.local.pkl` uses amends not being honoured | First line must be `amends "./hk.pkl"` |

---

## References

- `references/builtins-by-language.md` — step selection by ecosystem
- `references/complete-examples.md` — full hk.pkl configs for different stacks
- `assets/quiet-on-success.sh` — copy into `scripts/` in target repo
- [hk docs](https://hk.jdx.dev) — official documentation
- `hk builtins` — list all 90+ available built-in linters
