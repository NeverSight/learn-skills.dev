---
name: justfile
description: >
  Create or migrate to a justfile (casey/just command runner) for any project.
  Use this skill when the user asks to add a justfile, replace a Makefile with
  just, set up project commands, create task runners, or mentions "just" in the
  context of build/dev workflows. Do not trigger only because a project has a
  Makefile or is new; the request must ask to create or migrate project commands.
  Covers Rust, Python, TypeScript/JavaScript, Go, and Ruby ecosystems.
  Do NOT use for CI pipeline configuration, Dockerfiles, or actual build system setup (cargo, webpack, etc.).
license: MIT
---

# justfile

Generate idiomatic justfiles for any project. Replace Makefiles and ad-hoc
shell scripts with a clean, discoverable command runner.

## Why just over Make

- No `.PHONY` hacks — all recipes are commands, not file targets
- No tab-indentation gotchas — any whitespace works
- First-class parameters, dotenv loading, OS detection, and modules
- `just --list` gives instant discoverability with doc comments
- Shebang recipes let you write Python/Ruby/Node inline

For the official feature rationale — the most-used features, the special use
cases that make justfiles truly worth it, and a deep-linked chapter index — see
[`references/manual.md`](references/manual.md), grounded in the
[Just Programmer's Manual](https://just.systems/man/en/introduction.html).

## The default: one canonical command

Every justfile this skill generates exposes **one** command an agent runs after
every change — `just build` — and its no-autofix CI twin `just ci`. `build` is
the default recipe. Both run the full gate (format/lint → typecheck → test →
coverage) and compact their output: `✓ <step>` per passing step, full tool
output with file:line only on failure.

This is the default posture for *every* generated justfile, not an opt-in —
unless the user explicitly asks for a different layout. The rationale (agents
converge faster with one consistent command, deterministic pass/fail, and
compact error-only output — with citations) and the full recipe template,
`_gate` helper, and the mandatory `AGENTS.md` / CI updates all live in
`references/agent-build.md`. **Read it before writing any justfile.**

`build` = the gate (autofix on). `ci` = the gate (autofix off). The recipe that
compiles or packages an artifact is named `dist` (or `release`) — never `build`,
which is reserved for the gate.

## Protocol

### 1. Detect the project

Scan the project root for ecosystem markers:

| File | Ecosystem | Reference |
|------|-----------|-----------|
| `Cargo.toml` | Rust | `references/rust.md` |
| `pyproject.toml`, `setup.py`, `uv.lock` | Python | `references/python.md` |
| `package.json` | TypeScript/JS | `references/typescript.md` |
| `go.mod` | Go | `references/go.md` |
| `Gemfile` | Ruby | `references/ruby.md` |

Read the relevant reference file for language-specific recipes.

If multiple markers exist (e.g., a Rust backend + TypeScript frontend), combine
patterns. Use modules (`mod frontend`, `mod backend`) for true monorepos — the
root `build` gate then aggregates each module's gate so `just build` still means
"verify everything." For the full module/import composition pattern (and when to
pick `import` over `mod`), see [`references/composition.md`](references/composition.md).

**Multi-ecosystem naming:** When a project has multiple languages (e.g., Tauri
with Rust + TypeScript), use ecosystem suffixes to disambiguate overlapping
concerns:

- `test-rust`, `test-ts` (not generic `test` that hides what runs)
- `fmt-rust`, `fmt-ts` (each ecosystem's formatter)
- `lint-rust` (clippy), `lint-ts` (eslint/biome)
- Aggregate recipes combine them: `test: test-rust test-ts`, `fmt: fmt-rust fmt-ts`
- Shared recipes that span both ecosystems keep plain names: `dev`, `build`, `clean`

### 2. Check for existing build files

Look for `Makefile`, `Taskfile.yml`, `Rakefile`, `package.json` scripts, or
shell scripts in `scripts/` or `bin/`. If found:

- **Migrate**: Translate existing targets to just recipes (see migration table below)
- **Preserve**: Keep any complex logic that just can't replace (e.g., Make's
  file-target dependency tracking for actual build artifacts)
- **Remove**: Delete the old file only after confirming with the user

Also check for an existing `justfile`. If one exists, show the user a diff
of the proposed changes and wait for explicit authorization before you
overwrite it.

### 3. Write the justfile

Place `justfile` in the project root. Follow these conventions:

**Structure order:**

1. Settings (`set dotenv-load`, `set shell`)
2. Variables (version, binary name, etc.)
3. Default recipe — `default: build` (the canonical gate). Use `@just --list`
   only when the user explicitly wants no default gate.
4. The gate: `build` (autofix) + `ci` (no autofix) + the `_gate` helper — see
   `references/agent-build.md`
5. Granular recipes the gate composes: test, lint, fmt, typecheck, coverage
6. Other recipes by concern: run/dev, dist/release, docs
7. Utility recipes (clean, etc.)
8. Private helpers (`_prefixed` or `[private]`)

**Recipe naming:**

- Use kebab-case: `test-coverage`, `build-release`
- Use verbs: `build`, `test`, `lint`, `deploy` (not `builder`, `tests`)
- Group with prefixes for large files: `db-migrate`, `db-seed`, `db-reset`
- Default recipe should be the most common action or `--list`

**Doc comments:**
Every public recipe gets a comment on the line above it — this is what
`just --list` displays:

```just
# Run the full test suite
test *args:
    cargo test {{args}}
```

**Parameters:**

- Use defaults for optional args: `test filter=""`
- Use variadic for passthrough: `run *args`
- Use `+args` (1+ required) sparingly
- For ergonomic CLI flags (`just dist --target x86_64`), use the
  `[arg()]` attribute (v1.46+ — see "Recipe argument flags" below)

**Aliases:** Add a one-letter alias for any recipe a developer will
type more than a few times a day. Define it on the line below the
recipe so `just --list` shows the canonical name first:

```just
# Run tests
test *args:
    cargo test {{args}}
alias t := test
```

Don't manufacture aliases for every recipe — only the hot path.

**Settings to always include:**

```just
set dotenv-load
set shell := ["bash", "-euo", "pipefail", "-c"]
```

`-euo pipefail` makes shell recipes fail loudly on any error, unset
variable, or broken pipe — the same posture as a well-written bash
script. If a recipe needs softer behavior, use `-` line prefix to
ignore errors on a single command, not weaker shell flags. Skip the
`set shell` line for Windows targets or projects without a bash
dependency — the default `/bin/sh` is fine for most recipes.

`set unstable` is no longer needed for the common features: modules (stable
since just 1.31), the `[script]` attribute (1.44), and `[arg()]` flags (1.46)
all work on a current just without it. Add `set unstable` only to support a just
older than the relevant stabilization.

**dotenv hardening:** `set dotenv-load` silently does nothing when `.env` is
absent. When a project genuinely *requires* its `.env` (DB URLs, API keys),
make that failure loud — fail fast rather than running with empty vars:

```just
set dotenv-load
set dotenv-required          # error if no dotenv file is found

# Pick ONE of the following (omit both to load ./.env):
set dotenv-path := ".env.local"     # explicit path (relative to justfile), OR…
# set dotenv-filename := ".env.dev" # …a filename to search for up the tree
```

`dotenv-required` turns a missing env file into a hard error instead of a silent
no-op — the "fail fast and loud" posture. Use `dotenv-path` to point at one
exact file, or `dotenv-filename` to change which name just walks the tree
looking for. See
[Settings § dotenv](https://just.systems/man/en/settings.html#dotenv-settings).

### Tool dependencies — `require()`

When a recipe depends on a tool that isn't a standard system command,
declare it at the top of the justfile so `just --evaluate` fails fast
when it's missing:

```just
# https://github.com/jqlang/jq
jq := require("jq")

# https://github.com/casey/just (yes, just itself)
just := require("just")
```

Use `{{ jq }}` to invoke through the resolved path, or call `jq`
normally — `require()` has already confirmed it exists at evaluate
time, so either form works. The URL comment doubles as the install
hint. Skip `require()` for ubiquitous tools like `git`, `curl`, or
the language toolchain — declare only what a fresh machine might be
missing.

### 4. Token-optimized output (default, not opt-in)

`build` and `ci` run through the `_gate` helper from
`references/agent-build.md`, which is already compacted: `✓ <step>` per passing
step, full tool output (with file:line) only on failure. Coverage runs inside
the gate — its table is swallowed on success and shown in full when the
threshold fails. (This supersedes the old "skip coverage to save tokens"
advice: keep coverage in the gate; let compaction, not omission, handle the
token cost.)

For the granular recipes the gate composes, use the `@` prefix to silence
recipe echo, and pass `--silent --no-audit --no-fund` to npm to drop
banner/audit/fund noise.

### 5. Update project docs (mandatory)

Generating the recipes is only half the job — the value of one canonical command
is lost if nothing tells agents to use it. After creating the justfile, **always**
do both updates. Full snippets live in `references/agent-build.md`.

**Agent context file** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, or whatever the
harness uses; create `AGENTS.md` if none exists) — add/replace a build section
that tells the agent to ALWAYS run the one command and treat failure as a hard
stop:

```markdown
## Build & verification

This project has ONE canonical verification command. ALWAYS run it after
changing code, and treat a non-zero exit as a hard stop.

- `just build` — autofix, then lint, typecheck, test, and coverage. Run after
  every change.
- `just ci` — the same gate with no autofixes; exactly what CI runs.

Output is compacted: `✓ <step>` on success, full output (file:line) only on
failure. Don't invent ad-hoc test/lint commands — run `just build`.
```

**CI workflow** — point the existing verify step at `just ci` so local and CI
run the identical gate. This skill doesn't design pipelines; it only redirects
the verify step (e.g. replace separate lint/test/coverage steps with a single
`run: just ci`). See `references/agent-build.md` for the Actions snippet.

**README.md** — Add a "Development" or "Getting Started" section:

```markdown
## Development

### Prerequisites
- [just](https://github.com/casey/just) — `brew install just` / `cargo install just`

### Quick Start
```bash
just install   # Install dependencies
just test      # Run tests
just           # See all available commands
```

```

Don't duplicate the full recipe list — `just --list` is self-documenting.

## Makefile Migration Table

| Makefile | justfile |
|----------|----------|
| `.PHONY: target` | (not needed) |
| `$(VAR)` | `{{var}}` |
| `$(shell cmd)` | `` `cmd` `` |
| `-include .env` | `set dotenv-load` |
| `ifeq ($(OS),Darwin)` | `if os() == "macos" { ... }` |
| `ifndef VAR` / `$(or ...)` | `env_var_or_default("VAR", "default")` |
| `make -C subdir` | `mod subdir` |
| `$(MAKE) target` | `just target` |
| `.DEFAULT_GOAL := help` | First recipe is default |
| `@cmd` (suppress echo) | `@cmd` (same) |
| Tab indentation | Any whitespace |
| `%:` pattern rules | Not applicable — just has no file targets |

## Key Syntax Reference

**Variables:**
```just
VERSION := "1.0.0"
GIT_HASH := `git rev-parse --short HEAD`
DB_URL := env_var_or_default("DATABASE_URL", "postgres://localhost/dev")
OPEN := if os() == "macos" { "open" } else { "xdg-open" }
```

**Recipe attributes:**

```just
[confirm("Deploy to production?")]
deploy: build test

[macos]
open-docs:
    open target/doc/index.html

[linux]
open-docs:
    xdg-open target/doc/index.html

[private]
_setup:
    mkdir -p tmp/

# Group recipes in `just --list` output
[group("checks")]
lint:
    cargo clippy

[group("checks")]
fmt:
    cargo fmt

# Multiple attributes — same line (comma-separated) or stacked
[group("dev"), no-cd]
status:
    git status
```

**Recipe argument flags (v1.46+):** Use `[arg()]` to expose a
parameter as a CLI option instead of a positional arg. Best for
recipes a human runs at the prompt:

```just
[arg("target", long, help="Build target architecture")]
[arg("release", long, value="true", help="Build in release mode")]
dist target release="false":
    cargo build --target {{target}} {{ if release == "true" { "--release" } else { "" } }}
```

Usage: `just dist --target x86_64 --release`. Run `just --usage dist`
to see the generated help.

**Script blocks (`[script]`):** Cleaner than shebang recipes and
preferred when the body has shell control flow you don't want
re-evaluated line-by-line (stable since just 1.44 — no `set unstable` needed):

```just
[script("bash")]
deploy env:
    set -e
    case {{env}} in
        prod) URL="https://prod.example.com" ;;
        stage) URL="https://stage.example.com" ;;
        *) echo "unknown env: {{env}}"; exit 1 ;;
    esac
    curl -X POST "$URL/deploy"

[script("python3")]
analyze:
    import json
    print(json.load(open("results.json"))["total"])
```

`[script()]` is preferred over `#!/usr/bin/env` shebangs for
cross-platform portability and so the whole body runs as one block.

**Built-in color constants:** Available globally without definition —
`RED`, `GREEN`, `YELLOW`, `BLUE`, `CYAN`, `MAGENTA`, plus `BOLD`,
`UNDERLINE`, and `NORMAL` to reset. Useful for status output in
multi-step recipes:

```just
@check:
    cargo check
    echo -e '{{ GREEN }}✓ check passed{{ NORMAL }}'

@fail-loudly:
    echo -e '{{ BOLD + RED }}deploy aborted{{ NORMAL }}'
```

Don't sprinkle color through every recipe — reserve it for status
lines that summarize an aggregate step.

**Watch / dev loop:** just has no built-in watch flag — the manual's pattern is
to let [`watchexec`](https://github.com/watchexec/watchexec) re-run a recipe
whenever a watched file changes: `watchexec just <recipe>`. This is the
inner-loop counterpart to the gate. Wrap the common case in a `dev` recipe and
declare the dependency:

```just
# https://github.com/watchexec/watchexec
watchexec := require("watchexec")

# Re-run the fast checks on every save (Ctrl-C to stop).
dev:
    watchexec just test
```

`watchexec just test` is the day-to-day inner loop; the canonical `build` gate
stays the after-each-change verification. See
[Re-running recipes when files change](https://just.systems/man/en/re-running-recipes-when-files-change.html).

**Modules (monorepo):** See
[`references/composition.md`](references/composition.md) for the full pattern —
aggregating module gates into one root `build`, and `mod` vs `import`.

```just
mod api        # looks for api/justfile or api.just
mod web
mod? local     # optional — no error if missing

# Usage: just api::test, just web::build
```

**Shebang recipes (multi-line scripts, no `set unstable` needed):**

```just
analyze:
    #!/usr/bin/env python3
    import json
    data = json.load(open("results.json"))
    print(f"Total: {len(data)}")
```

Prefer `[script("python3")]` over shebangs on just ≥ 1.44 (stable, no
`set unstable` needed) — it runs the body as one block and avoids
shebang-portability quirks.

## Anti-patterns

- Don't recreate Make's file-target system — just is a command runner, not a build system
- Don't use `set positional-arguments` unless you have a strong reason — `{{arg}}` is clearer
- Don't put secrets in justfiles — use dotenv or env vars
- Don't write 200-line justfiles — use modules (`mod`) to split by concern
- Don't duplicate CI pipeline steps 1:1 — collapse them into the `build`/`ci` gate
- Don't name the artifact/compile recipe `build` — that name is the gate; use `dist` or `release`

## What You Don't Do

- Design CI pipelines or GitHub Actions workflows from scratch — but **do**
  redirect the existing CI verify step at `just ci` (see step 5)
- Create Dockerfiles or container configs
- Replace actual build systems (cargo, webpack, go build) — just wraps them
- Remove existing Makefiles without user confirmation

## Gotchas

- `just` binary may not be on PATH — check with `which just` before generating recipes
- Shebang recipes need explicit `#!/usr/bin/env` for portability across systems
- `dotenv-load` exposes all env vars to all recipes — avoid for secrets-heavy projects
- Module paths are relative to the justfile location, not the working directory
- `set positional-arguments` changes how `$1` works inside recipes — document when used
- `require("tool")` validates at evaluate time — use `{{ jq }}` to
  invoke via resolved path, or call `jq` directly; both work once
  `require` has confirmed the tool exists
- `[script()]` is stable since just 1.44, modules since 1.31, `[arg()]` since
  1.46 — none need `set unstable` on a current just. Add `set unstable` only for
  an older just, and pin the relevant minimum in your README if you rely on them
