---
name: go-dev
description: Opinionated Go setup with golangci-lint v2, gofumpt, gotestsum, golang-migrate, and just. Use when starting a Go project, configuring lint, format, test, coverage or CI, writing a Justfile, wiring migrations, or leaving a Makefile workflow.
metadata:
  version: "0.7.0"
  categories: "development"
  topics: "go, golangci-lint, gofumpt, testing, just"
  upstream: "go@1.27.3, golangci-lint@v2.15.0, gofumpt@v0.12.0, gotestsum@v1.13.0, golang-migrate@v4.20.1, just@1.59.0, lefthook@v2.2.2"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/go-dev
    emoji: "🐹"
    envVars:
      - name: DATABASE_URL
        required: false
        description: Connection string used by the Justfile migration recipes (golang-migrate)
---

# Go Development Stack

Opinionated, modern Go development setup. One tool per concern, zero overlap.

## When to Use

- Starting a new Go project from scratch
- Adding linting, formatting, or testing infrastructure
- Setting up CI/CD for a Go service or library
- Creating a Justfile to replace a Makefile
- Adding database migration tooling
- Migrating from scattered gofmt/govet/staticcheck invocations to a unified setup

Not for a fork that regularly merges from upstream: replacing its Makefile and reformatting the tree with gofumpt conflicts on every merge and buries real changes in a reformat diff. Keep upstream's gofmt and build tooling there, and only add checks.

## The Stack

| Tool | Version | Role | Replaces |
|------|---------|------|----------|
| **Go** | 1.27+ | Language, toolchain, `go mod`, `go fix` | - |
| **golangci-lint** | v2.15+ | Meta-linter (100+ linters + formatters + `fmt` command) | gofmt, govet, staticcheck, errcheck run separately |
| **gofumpt** | v0.12+ | Strict formatter (superset of gofmt, 19 default rules) | gofmt |
| **gotestsum** | v1.13+ | Test runner with readable output, watch mode, JUnit XML | Raw `go test` |
| **just** | 1.59+ | Task runner | Makefile |
| **golang-migrate** | v4.20+ | DB migrations (CLI + library + `embed.FS`) | Manual SQL scripts |
| **lefthook** | v2.2+ | Git hooks (single binary, parallel) | pre-commit (Python) |

**Version floors are load-bearing.** golangci-lint "supports Go versions lower or equal to the Go version used to compile it" - a pin older than your Go toolchain fails outright. Go 1.27 support landed in golangci-lint v2.13.0, but a patch release can move the floor: v2.13.2 loads packages built by go1.27.1 and go1.27.2, yet fails on go1.27.3 with `export data version 5 is greater than maximum supported version 4` reported as a `typecheck` issue on every stdlib import. v2.14.0 and v2.15.0 pass on all three, so `v2.14` is the floor for a current Go 1.27 toolchain; this skill pins v2.15.0. Two more floors moved recently: gofumpt v0.12.0 "is based on Go 1.27's gofmt, and requires Go 1.26 or later", and lefthook v2.2's `go install` path needs Go 1.27 - "The minimum Go version required is 1.27" - and tracking it with `go get -tool` raises your own module's `go` line to `1.27.0`.

## Quick Start: New Project

```bash
# 1. Create module
mkdir myapp && cd myapp
go mod init github.com/yourorg/myapp

# 2. Scaffold directories
mkdir -p cmd/myapp internal migrations

# 3. Install golangci-lint as a binary, not as a module tool (see note below)
curl -sSfL https://golangci-lint.run/install.sh | sh -s -- -b $(go env GOPATH)/bin v2.15.0

# 4. Track the rest in go.mod (Go 1.24+ tool directive). Pin versions - never @latest,
#    which recompiles the tool on every CI run and drifts between machines.
go get -tool mvdan.cc/gofumpt@v0.12.0
go get -tool gotest.tools/gotestsum@v1.13.0

# golang-migrate needs a build tag, so install it directly
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@v4.20.1

# 5. Create config files (templates below)
# 6. Run: just check
```

**Do not install golangci-lint through the tools pattern.** Upstream is explicit: "Using `go install`/`go get`, \"tools pattern\", and `tool` command/directives installations aren't guaranteed to work. We recommend using binary installation." The reason that matters in a shared repo is dependency bleed - "the dependencies of a tool can modify the dependencies of another tool or your project". If you must have it in `go.mod`, isolate it behind its own `-modfile` - see the [golangci-lint Reference](references/golangci-lint-reference.md). The bleed is not specific to golangci-lint: "Tools are built using the same module graph as the module itself", so every `go get -tool` (gofumpt, gotestsum, lefthook, a secret scanner) can upgrade your project's dependencies or fail on a conflict with them. Keep the tool set small, and give a heavy tool its own `-modfile`.

**`go get -tool` tracks; `go tool` runs.** The tool directive records the dependency in `go.mod` but puts nothing on your PATH. Either invoke through the toolchain - `go tool gofumpt -l .`, `go tool gotestsum --format testname` - or `go install tool` once to populate `$(go env GOPATH)/bin`. The Justfile below calls the bare binaries, so it assumes the `go install tool` route (or a system install via Homebrew - but "Homebrew can use an unexpected version of Go to build the binary" for golangci-lint, and it cannot pin a version). Note that `go tool` resolves against the module in the current directory - "additional tools may be defined in the go.mod of the current module" - so in a monorepo of independent modules it fails with `go: no such tool "..."` unless the recipe sets `[working-directory(...)]`. A `go.work` workspace lifts this - "In workspace mode, you can use `go tool` to run a tool declared in any workspace module" - see the [Go Toolchain Reference](references/go-toolchain-reference.md).

Two Go-command behaviours worth knowing before the first commit:

- `go mod init` under a 1.N toolchain writes `go 1.(N-1).0`, not `1.N` - "Running `go mod init` using a toolchain of version `1.N.X` will create a `go.mod` file specifying the Go version `go 1.(N-1).0`." Bump the directive deliberately if you want 1.N language features.
- Set a `toolchain go1.27.3` line in `go.mod`, but know it is a floor, not a pin: under the default `GOTOOLCHAIN=auto` the `go` command switches only "if ... `<tname>` is newer than the default Go toolchain", so a newer local `go` wins. For an exact toolchain set `GOTOOLCHAIN=go1.27.3` (CI or `go env -w`); `GODEBUG=toolchaintrace=1 go version` shows which one was picked. Keep the line at the current patch, not the `.0`: it selects the `go` that `govulncheck` scans stdlib advisories against on any machine whose own `go` is older, so a stale patch red-lights CI on its own - see Footguns below. Live example: go1.27.2 and go1.27.3 fixed 16 stdlib and toolchain advisories, so a module still on `toolchain go1.27.1` that imports `crypto/x509` or `net/http` gets nine findings from govulncheck v1.9.0 (first: `GO-2026-6809`, "Fixed in: crypto/x509@go1.27.3") and exit 3.
- Bumping the `go` directive also flips GODEBUG defaults, not only the removed settings listed below. Each setting carries the release that changed its default (`{Name: "urlstrictcolons", Package: "net/url", Changed: 26, Old: "0"}` means that once the module says `go 1.26`, "`Parse` now rejects malformed URLs containing colons in the host subcomponent", which breaks multi-host DSNs such as `postgres://h1:5432,h2:5432/db`). List what a bump to 1.N flips with `rg 'Changed: N,' $(go env GOROOT)/src/internal/godebugs/table.go`, and pin an old value with a `godebug` line while you migrate.

## .golangci.yml

```yaml
version: "2"

run:
  timeout: 5m
  build-tags:
    - integration   # otherwise files behind the Justfile's integration tag are never linted

linters:
  default: standard
  enable:
    - bodyclose
    - copyloopvar
    - dupl
    - durationcheck
    - err113
    - errname
    - errorlint
    - exhaustive
    - exptostd
    - fatcontext
    - goconst
    - gocritic
    - gosec
    - intrange
    - misspell
    - modernize
    - musttag
    - nakedret
    - nestif
    - nilerr
    - noctx
    - nolintlint
    - nonamedreturns
    - perfsprint
    - prealloc
    - revive
    - sqlclosecheck
    - testifylint
    - thelper
    - unconvert
    - unparam
    - usestdlibvars
    - usetesting
    - wastedassign
    - whitespace
    - wrapcheck
  settings:
    govet:
      enable:
        - shadow
    gocritic:
      enabled-checks:
        - nestingReduce
    revive:
      enable-all-rules: true
      rules:
        # Wants same-typed results named, which nonamedreturns forbids - keep one.
        - name: confusing-results
          disabled: true
    nolintlint:
      require-explanation: true   # both default to false
      require-specific: true
    errcheck:
      check-type-assertions: true
  exclusions:
    generated: strict
    presets:
      - comments
      - std-error-handling
      - common-false-positives
    rules:
      - path: _test\.go
        linters:
          - errcheck
          - dupl
          - gosec
          - wrapcheck

formatters:
  enable:
    - gofumpt
    - goimports
  settings:
    gofumpt:
      # Select rules individually. `extra-rules: true` is deprecated, and it also
      # switches on `balance_calls`, which gofumpt itself demoted as controversial.
      extra:
        group-params: true
        clothe-returns: true
        balance-calls: false
  exclusions:
    generated: strict
    paths:
      - vendor/

output:
  formats:
    text:
      path: stdout
      print-linter-name: true
      colors: true
  sort-order:
    - linter
    - file
  show-stats: true
```

Two template choices are deliberate. revive's `unhandled-error` needs no override: standalone revive flags `fmt.Println` with it, but golangci-lint loads revive in syntax mode (`goanalysis.LoadModeSyntax`), and on v2.14.0 and v2.15.0 the rule reported nothing - not even an unchecked call to a same-package function - although the v2.15.0 changelog lists it among rules now "working (less randomly)". errcheck is what catches unchecked errors here. `confusing-results` is off because it flags `func f() (string, string)` while `nonamedreturns` flags `func f() (a, b string)` - with both on, a same-typed pair of results has no passing form.

## Justfile

```just
set shell := ["bash", "-euo", "pipefail", "-c"]
set dotenv-load

binary := "myapp"

[private]
default:
    @just --list --unsorted

# ── Code Quality ──────────────────────────────────────────

# Format all Go code
[group('quality')]
fmt:
    golangci-lint fmt ./...

# Check formatting without modifying (CI-safe)
[group('quality')]
fmt-check:
    golangci-lint fmt --diff ./...

# Run linter
[group('quality')]
lint:
    golangci-lint run ./...

# Run linter with auto-fix
[group('quality')]
lint-fix:
    golangci-lint run --fix ./...

# Run vulnerability check
[group('quality')]
vuln:
    govulncheck -test -tags=integration ./...

# ── Testing ───────────────────────────────────────────────

# Run all tests with race detection
[group('test')]
test *args="./...":
    gotestsum --format testname -- -race {{ args }}

# Run tests with coverage
[group('test')]
test-cov:
    gotestsum --format testname -- -race -coverprofile=coverage.out -covermode=atomic ./...
    go tool cover -func=coverage.out

# Open coverage report in browser
[group('test')]
coverage: test-cov
    go tool cover -html=coverage.out

# Run integration tests
[group('test')]
test-integration:
    gotestsum --format testname -- -race -tags=integration ./...

# Watch tests during development
[group('test')]
test-watch:
    gotestsum --watch --watch-clear --format testname

# Run benchmarks
[group('test')]
bench:
    go test -bench=. -benchmem ./...

# ── Build ─────────────────────────────────────────────────

# Build the binary
[group('build')]
build:
    go build -o {{ binary }} ./cmd/{{ binary }}

# Build optimized release binary
[group('build')]
build-release:
    CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o {{ binary }} ./cmd/{{ binary }}

# ── Dependencies ──────────────────────────────────────────

# Tidy and verify modules
[group('deps')]
tidy:
    go mod tidy
    go mod verify

# Fail if go.mod/go.sum are untidy, without touching them (CI-safe)
[group('deps')]
tidy-check:
    go mod tidy -diff

# Run code generators
[group('deps')]
generate:
    go generate ./...

# ── Database ──────────────────────────────────────────────

# Apply all pending migrations
[group('db')]
migrate-up:
    migrate -path migrations -database "$DATABASE_URL" up

# Revert last migration
[group('db')]
migrate-down:
    migrate -path migrations -database "$DATABASE_URL" down 1

# Create a new migration
[group('db')]
migrate-create name:
    migrate create -ext sql -dir migrations -seq {{ name }}

# ── CI ────────────────────────────────────────────────────

# Full CI gate (format check + lint + test)
[group('ci')]
check: fmt-check lint test
    @echo "All checks passed"

# Clean build artifacts
[group('ci')]
clean:
    go clean
    rm -f {{ binary }} coverage.out
```

`check` deliberately leaves out `vuln`: govulncheck calls the network, and a vulnerability-database update can turn the gate red on a change that touched nothing. Run it as its own CI job instead. The `-test -tags=integration` flags matter: govulncheck documents `-test` as "analyze test files (only valid for source mode, default false)", and like `go build` it skips files behind an unset build tag, so a bare `govulncheck ./...` never scans the test-only dependencies or the integration suite the linter covers. `golangci-lint run` also runs the enabled formatters and reports their issues, so `fmt-check` duplicates that check - keep it anyway for the readable diff.

## Lefthook Config

Lefthook is preferred over pre-commit for Go projects - it is a single Go binary, runs hooks in parallel, and needs no Python.

```bash
go install github.com/evilmartians/lefthook/v2@v2.2.2   # needs Go 1.27+
lefthook install
```

```yaml
# lefthook.yml
# yaml-language-server: $schema=https://lefthook.dev/schema.json
assert_lefthook_installed: true   # fail loudly instead of skipping every rule

pre-commit:
  piped: true   # fail fast - stop at the first failing job
  commands:
    fmt:
      glob: "*.go"
      run: golangci-lint fmt {staged_files}
      stage_fixed: true
    lint:
      glob: "*.go"
      # Never pass a bare file list to `golangci-lint run`: a list spanning two
      # directories is rejected outright, and one file of a multi-file package
      # reports phantom `undefined:` typecheck errors. Lint the packages instead,
      # line- and NUL-delimited so a file name with a space survives.
      run: printf '%s\n' {staged_files} | xargs -I{} dirname {} | sort -u | tr '\n' '\0' | xargs -0 golangci-lint run --fix
      stage_fixed: true
    mod-tidy:
      glob: "*.{go,mod,sum}"
      run: go mod tidy

pre-push:
  commands:
    test:
      run: go test -race ./...
```

`piped: true` is fail-fast, not ordering - lefthook "runs commands and scripts **sequentially** by default", and `piped` adds "Stop running commands and scripts if one of them fail." It cannot be combined with `parallel: true`.

`jobs:` (added in lefthook 1.10.0) is the newer primitive alongside the `commands:`/`scripts:` split - "Jobs provide a flexible way to define tasks, supporting both commands and scripts. Jobs can be grouped for advanced flow control." `commands:` is not deprecated and stays fully documented; reach for `jobs:` when you need grouping, nested control flow, or a mix of inline commands and scripts in one hook.

Four more worth wiring:

- `assert_lefthook_installed: true`, above, is the antidote to the dormancy footgun below: "fail (with exit status 1) if `lefthook` executable can't be found in $PATH".
- `lefthook validate` in CI catches a malformed `lefthook.yml` before it silently disables hooks; `lefthook dump` prints the merged effective config when a hook does not behave as written.
- A gitignored `lefthook-local.yml` lets a developer add or skip jobs without imposing it on teammates - "This is useful when you want to use lefthook locally without imposing it on your teammates."
- In a monorepo of independent modules, give each job a `root:` pointing at its module directory; without it `go mod tidy` and `go tool` run against the repo root and fail. Under a `go.work` workspace, one root job that lints `$(go list -m -f '{{.Dir}}/...')` replaces the per-module jobs - see the [Go Toolchain Reference](references/go-toolchain-reference.md).
- `skip: [merge, rebase]` on the `mod-tidy` and lint jobs keeps them out of commits made while a merge or rebase is in progress, so resolving conflicts does not also restage a tidy rewrite or `--fix` edits.

The `pre-push` race suite repeats what CI already runs. Once it takes minutes, drop it or scope it to changed packages - otherwise developers learn to push with `LEFTHOOK=0`. Tests run from a hook also inherit git's hook environment (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`), so a test helper that runs `git init` or `git commit` in `t.TempDir()` acts on the real repository - clear those variables in `cmd.Env`.

A conflict-free `git merge` never runs `pre-commit`: git invokes `pre-merge-commit` instead, and runs `pre-commit` only when you finish a conflicted merge with `git commit`. Mirror the checks under a `pre-merge-commit:` key, or merges land unlinted.

Hook commands resolve tools from the caller's PATH, so a missing binary fails the commit with a bare `exit 127`. Running them as `go tool <name>` (tool directive) makes the hook as reproducible as the build.

Beta, but worth knowing: `ai:` declares LLM agent hooks in the same file - "During `lefthook install`, lefthook generates the provider-specific settings file so that the agent calls `lefthook run <hook>` when the event fires", for `claude`, `codex`, `cursor`, and `copilot`. Since v2.2.0 the generated files call the `lefthook:` config value, or else a bare `lefthook`, so the binary must be on the agent's PATH. See the [Lefthook Reference](references/lefthook-reference.md) for the wider config surface.

## Project Structure

```
myapp/
  cmd/
    myapp/
      main.go              # Wire deps, call Run(), nothing else
  internal/
    user/                  # Domain logic, one package per domain
      user.go
      user_test.go
      repository.go
    transport/             # HTTP/gRPC handlers
    storage/               # Database layer
  migrations/
    000001_create_users.up.sql
    000001_create_users.down.sql
  testdata/                # Test fixtures (ignored by go toolchain)
  .golangci.yml
  lefthook.yml
  Justfile
  go.mod
  go.sum
  Dockerfile
```

**Guidelines:**
- `cmd/` - one directory per binary, keep `main.go` thin (~50 lines max). A second binary is a second `cmd/<name>/`, not a second `go.mod`: a nested module is invisible to every `./...` gate aimed at the first one, and it releases only from path-prefixed tags (`sub/dir/vX.Y.Z`)
- `internal/` - all business logic goes here. The rule is by import path, not by module: a package under `.../a/b/c/internal/` "can be imported only by code in the directory tree rooted at `.../a/b/c`", so a separate module nested under that tree can still import it
- `pkg/` - only add when another repo actually imports it today, not "maybe someday"
- `testdata/` - test fixtures, golden files, fuzz corpus
- `migrations/` - SQL migration files (timestamp or sequential versioned)

## Daily Workflow

```bash
just fmt          # Format code
just lint         # Run linter
just test         # Run tests with race detection
just check        # Full CI gate (fmt-check + lint + test)
just test-watch   # Watch mode during development
just generate     # Run go generate
just tidy         # go mod tidy + verify
```

`go fix` is the toolchain-native complement to the `modernize` linter: Go 1.26 rebuilt it as a codebase modernizer - "The venerable `go fix` command has been completely revamped and is now the home of Go's *modernizers*. It provides a dependable, push-button way to update Go code bases to the latest idioms and core library APIs." Run `go fix ./...` after a toolchain bump, before the linter has to complain. Go 1.27 added four more modernizers - "The go fix command contains several new modernizers (atomictypes, embedlit, slicesbackward, and unsafefuncs)" - and removed `fmtappendf`, so a 1.27 bump is a good moment to run it. It also renamed one: "The existing `waitgroup` analyzer was renamed to `waitgroupgo`", which matters if you disable it by name. For your own API migrations, annotate a deprecated function with a `//go:fix inline` directive and `go fix` (and golangci-lint's `govet` `inline` analyzer) rewrites its callers.

Both `go fix` and `go vet` take `-diff`: "instead of applying each fix, print the patch as a unified diff; exit with a non-zero status if the diff is not empty". `go fix -diff ./...` in CI fails a PR that still has modernizer rewrites pending, without touching the tree.

Other Go 1.27 changes that touch this stack directly:

- **Generic methods.** "Go 1.27 now supports generic methods: a method declaration may declare its own type parameters."
- **`encoding/json/v2`.** "The encoding/json package is now backed by the v2 implementation" - "Marshaling and unmarshaling behavior is preserved, but the exact text of error messages may differ", so tests that assert on JSON error strings break. The escape hatch is `GOEXPERIMENT=nojsonv2` at build time.
- **`go test -json` gained an `OutputType` field**, annotating `"Action":"output"` lines. gotestsum v1.13.0 does not use it yet ([gotestsum#571](https://github.com/gotestyourself/gotestsum/issues/571)).
- **`go mod tidy` reshapes `go.mod`** to "at most two require blocks". The first tidy after the bump rewrites the file, and the lefthook `mod-tidy` job stages that rewrite into whatever you commit next.
- **Removed GODEBUG settings fail the build.** The `go` command now recognizes removed settings (`asynctimerchan`, `gotypesalias`, `tls10server`, `tlsrsakex`, `tls3des`, `tlsunsafeekm`, `x509keypairleaf`) in `go.mod` `godebug` lines and `//go:debug` comments - "If they are set to an old value, the go command will fail." Delete them before bumping.
- **gofmt alignment changed.** Go 1.27 warns that "running gofmt from Go 1.27 on previously formatted code may produce minor whitespace changes", and gofumpt v0.12.0 inherits it - expect a one-time formatting diff alongside the toolchain bump.

## Footguns

Eight failure modes that cost real debugging time, none of which produce an obvious error message.

**Config placement is load-bearing.** `.golangci.yml` must sit at the repo root: golangci-lint "searches for config files in all directories from the directory of the first analyzed path up to the root" (`.yml`, `.yaml`, `.toml` and `.json` all count), and editor Go plugins auto-detect only a root `.golangci.*`, so filing it under `.github/` costs in-IDE linting even if you pass `--config`. lefthook auto-discovers only the repo root or `.config/` - move `lefthook.yml` anywhere else and commits silently stop running hooks, because git invokes the hook directly and no task-runner recipe can intercept that.

**lefthook is dormant until installed.** The binary being absent from PATH, or `lefthook install` never having run, both present as "hooks just don't fire" with no warning. Set `assert_lefthook_installed: true` so this fails loudly, pin lefthook as a repo tool, and make `lefthook install` part of onboarding. A leftover `core.hooksPath` (husky, pre-commit) is a third cause: `lefthook install` stops when it is set, until you run `lefthook install --reset-hooks-path`.

**A stale lint cache invents issues.** golangci-lint can report failures in files that no longer exist on disk - typically after a branch switch or a deleted worktree. The costlier variant is nolintlint reporting a load-bearing `//nolint` directive as unused, which tempts you to delete a real suppression. Its main root cause was lost analyzer facts after an interrupted run, a changed linter set, or a partly cleaned cache ([#6807](https://github.com/golangci/golangci-lint/issues/6807)), fixed in v2.14.0 - so upgrade before debugging. The same bug can also *hide* real issues that CI then catches. Prove which side is lying with `GL_DEBUG=nolint_filter` before touching the code. If a phantom persists, move that suppression into `linters.exclusions.rules` rather than running `golangci-lint cache clean` before every gate, which turns a warm run of seconds into a cold one ten times longer. `cache clean` empties whatever `GOLANGCI_LINT_CACHE` resolves to in *that* shell, so running it outside a recipe that sets the variable cleans the wrong directory. When several worktrees share a checkout, give each its own cache with `GOLANGCI_LINT_CACHE=<worktree>/.golangci-cache` ("the path must be absolute") - and note the cache does not reliably invalidate on config, tool, or dependency changes, so fold those into the cache key if a phantom keeps returning.

**Concurrent golangci-lint runs fail rather than queue.** The lock is a single file in the system temp dir, *not* per-`GOLANGCI_LINT_CACHE`, so per-worktree cache isolation does not prevent it. A second run waits five seconds, then exits with `parallel golangci-lint is running`. This bites hardest in a `just` recipe with `[parallel]` that runs `fmt` and `run` together, on green code. Set `run.allow-serial-runners: true` to wait indefinitely instead of failing, or `run.allow-parallel-runners: true` to drop the lock entirely.

**Don't run two formatters against one gate.** Standalone `gofumpt -w` and `golangci-lint fmt` do not always agree on the same file, so a repo that fixes with one and gates with the other fails CI on code it just formatted. It recurs whenever gofumpt releases ahead of golangci-lint: v2.13.2 bundled gofumpt v0.11.0 against a standalone v0.12.0 (which changed how imports carrying comments and blank lines are laid out), and only v2.14.0 caught up. gofumpt master already carries a batch of unreleased output-changing fixes, so expect the next gap. Pick one as both fixer and gate - the Justfile and the hook above both use `golangci-lint fmt`.

**A pinned linter older than your Go toolchain fails outright.** This is the same trap as the version floor above, and it usually surfaces first as a config-schema rejection: a config authored against a newer golangci-lint hits `additional properties ... not allowed` under the pinned CI version. Bump the CI pin and the local install together. The rejection also runs the other way: v2.15.0 bumped `exhaustive` to 0.15.0, which renamed its options (`explicit-exhaustive-switch`/`-map` -> `explicit-exhaustive`, `ignore-enum-members` -> `ignore-constants`, `ignore-enum-types` -> `ignore-types`), and the old names now fail `config verify` with exit 3 - which golangci-lint-action runs before every lint. The other shape is a `typecheck` issue on every stdlib import, `export data version N is greater than maximum supported version M`: the linter is too old for the toolchain's export format, even within one Go minor (see the version floor above).

**Sandboxed and agent runs fail in the build cache, not in your code.** An agent sandbox or a read-only `HOME` cannot write the default `GOCACHE`, and the run fails as `FAIL <pkg> [setup failed]` with `open .../go-build/...: operation not permitted` - or a generator emits nothing and a later diff fails. Point `GOCACHE` (and `GOLANGCI_LINT_CACHE`) at one persistent, absolute, writable directory rather than a fresh temp dir per run: "The cache is safe for concurrent invocations of the go command", while a new dir is a full cold rebuild every time (`-race` included). `httptest` failing with `bind: operation not permitted` is the same sandbox, not a test bug. And settings exported only inside the Justfile (`GOFLAGS=-trimpath`, cache paths) do not reach an ad-hoc `go test` or `golangci-lint run` from a shell, which then builds a second cache - and can share and poison the lint cache the recipe uses.

**`govulncheck` fails on stdlib advisories, not just your code.** It scans against "the Go version specified by the `go` command found on the PATH". Locally, under `GOTOOLCHAIN=auto`, that is the newer of your installed `go` and the `toolchain` line in `go.mod`. In CI, setup-go exports `GOTOOLCHAIN=local`, so it is whatever `go-version` installed unless you use `go-version-file: go.mod`. Either way, a lagging toolchain red-lights CI on commits that touch zero Go code - and a failed test-and-lint job typically skips the release job downstream. When `govulncheck` reports vulnerabilities "in the Go standard library" all marked fixed in a patch you don't have, the fix is bumping the toolchain, not editing code. The scanner binary has a floor too: a govulncheck built with Go 1.26 fails on Go 1.27 code with "Loading packages failed, possibly due to a mismatch between the Go version used to build govulncheck and the Go version on PATH" (`file requires newer Go version go1.27 (application built with go1.26)`). Reinstall it with the current toolchain after every Go minor bump.

## CI/CD Pipeline (GitHub Actions)

```yaml
name: Go CI
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-go@v7
        with:
          go-version-file: go.mod   # honours the `toolchain` line
      - uses: golangci/golangci-lint-action@v9
        with:
          version: v2.15

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        go-version: [stable, oldstable]
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-go@v7
        with:
          go-version: ${{ matrix.go-version }}
      - run: go install gotest.tools/gotestsum@v1.13.0
      - name: Test
        run: gotestsum --format github-actions --junitfile unit-tests.xml -- -race -coverprofile=coverage.out -covermode=atomic ./...
      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: test-results-${{ matrix.go-version }}
          path: unit-tests.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-go@v7
        with:
          go-version-file: go.mod
      - run: go install golang.org/x/vuln/cmd/govulncheck@v1.9.0
      - run: govulncheck -test -tags=integration ./...
```

Three `setup-go` behaviours decide whether this workflow is fast or pathologically slow:

- **It hashes a repo-root `go.mod`.** Caching is on by default, but a module in a subdirectory never matches, so every run logs a restore failure and cold-compiles the whole dependency tree. Point `cache-dependency-path` at the real file.
- **It restores only the exact key, and that key hashes `go.mod`.** "By default, the cache key for Go modules is based on `go.mod`. To use `go.sum`, configure the `cache-dependency-path` input." There is no `restore-keys` prefix fallback, so every change to the hashed file is a fully cold run. If that hurts, set `cache: false` and use one `actions/cache` step with a `restore-keys` prefix, keyed per job so parallel jobs do not race on save - and end the key with something unique such as `-${{ github.sha }}`: cache entries are immutable, so a key built only from `go.sum` is saved once and every later save fails with `Unable to reserve cache`. In a vendored repo the module cache buys nothing; cache `~/.cache/go-build` instead.
- **The cache is saved in a post step declared `post-if: success()`.** A job that fails saves nothing, so a cold run that times out stays cold forever and raising the timeout never breaks the loop. Split lint and test into separate jobs so one slow gate cannot starve the other's cache. The template's `run.timeout: 5m` is tight for a cold lint on a private repo's 2-vCPU `ubuntu-latest`.

setup-go also exports `GOTOOLCHAIN=local`, so the `go.mod` `toolchain` line is ignored unless you use `go-version-file`. Even then it reads the `toolchain` line only while `GOTOOLCHAIN` is not already `local` (`src/installer.ts`: "use version from go directive if 'GOTOOLCHAIN' has been explicitly set"), so a workflow-level `env: GOTOOLCHAIN: local`, or a second setup-go step in the same job, silently falls back to the `go` directive's older version. A `go.work` workspace takes `go-version-file: go.work`. The same rule breaks the `oldstable` matrix leg once you bump the `go` directive past it: the older `go` fails with `go.mod requires go >= ...` instead of downloading a newer toolchain. Drop `oldstable` at that point, or keep the directive one minor behind.

The action runs `golangci-lint config verify` itself before linting whenever a config file exists (input `verify`, default `true`), so a config the pinned binary rejects fails fast without an extra step. For incremental adoption with `only-new-issues: true`, grant `pull-requests: read`. Note that CI never runs your Justfile unless you install just (`extractions/setup-just`) - the template calls the tools directly. Action inputs for monorepos and `go.work` are in the [golangci-lint Reference](references/golangci-lint-reference.md).

## Existing Project Migration

```bash
# 1. Install tools (golangci-lint as a binary - see Quick Start)
curl -sSfL https://golangci-lint.run/install.sh | sh -s -- -b $(go env GOPATH)/bin v2.15.0
go install mvdan.cc/gofumpt@v0.12.0
go install gotest.tools/gotestsum@v1.13.0

# 2. Migrate existing golangci-lint v1 config, then replace the deprecated
#    `gofumpt: extra-rules: true` it carries over with the `extra:` map above
golangci-lint migrate

# 3. Format codebase
gofumpt -w .

# 4. Run linter (fix what you can, nolint the rest)
golangci-lint run --fix ./...

# 5. Replace go test with gotestsum in scripts/CI
# Before: go test -v ./...
# After:  gotestsum --format testname -- -race ./...

# 6. Copy Justfile and lefthook.yml templates above
# 7. Run: just check
```

For incremental adoption on large codebases, use `only-new-issues: true` in the GitHub Action to only lint changed code. Outside the Action, `--new-from-merge-base=main` and `--new-from-rev=<rev>` do the same locally - see the [golangci-lint Reference](references/golangci-lint-reference.md) for the full set.

Expect new findings after a toolchain bump: since Go 1.27, "`go test` now invokes the `stdversion` vet check by default. This reports the use of standard library symbols that are too new for the Go version in force in the referring file". Adjust the `go` directive or the call site rather than suppressing it. A linter bump does the same: on v2.14.0, `revive: enable-all-rules: true` switches on three new rules (`marshal-receiver`, `multiline-if-init`, `use-slices-concat`) and gosec re-enables G407, so budget for new findings on existing code. v2.15.0 repeats it: revive 1.17.1's `add-constant` "now inspects nested call arguments and function literal signatures ... so existing projects may see new findings after upgrading", and `enable-all-rules` turns that rule on.

Triage a linter bump with the caps off. The default `max-same-issues: 3` prints at most three findings per rule, so the first run hides the size of the fallout - rerun with `--max-same-issues=0 --max-issues-per-linter=0` before deciding whether to fix or `disable` a new rule (one new revive rule produced 260 findings in one existing repo). An upgrade can also move the line an issue is reported on, so a working `//nolint` stops matching and nolintlint reports it unused - a different cause from the stale-cache footgun above. Go 1.27's vet adds a second `go test` failure: "The printf analyzer now reports calls such as `fmt.Errorf("...: %w", p)` in which the `%w` operand `p` has type `*E`, where the type `E` itself implements `error`" - wrap the value, or make `*E` the error type.

## Adjacent Tools

Not part of the core stack, but the gaps most projects fill next:

| Need | Tool | Why |
|------|------|-----|
| Structured logging | `log/slog` (stdlib) | The default since Go 1.21; the `sloglint` linter enforces a consistent call style. Install a handler in `main` (`slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stderr, nil)))`), or `slog.Info` writes the old `log` text format that log pipelines can only regex-parse |
| Hot reload for a running service | [air](https://github.com/air-verse/air) or [wgo](https://github.com/bokwoon95/wgo) | `just test-watch` covers tests; neither `go run` nor gotestsum restarts a server on save |
| Release binaries + changelog | [GoReleaser](https://goreleaser.com/) | Cross-compile, checksum, sign, and publish from one config |
| Type-safe SQL from schema | [sqlc](https://sqlc.dev/) | Generates Go from the same SQL your migrations define, so `storage/` stays hand-written-free |

## Reference Docs

- [golangci-lint Reference](references/golangci-lint-reference.md) - v2 config, linter catalog, recommended sets, nolint syntax
- [gofumpt Reference](references/gofumpt-reference.md) - formatting rules, editor integration, golangci-lint integration
- [gotestsum Reference](references/gotestsum-reference.md) - output formats, watch mode, JUnit XML, CI recipes
- [Go Testing Reference](references/go-testing-reference.md) - table-driven tests, mocking, benchmarks, coverage, fuzz testing
- [golang-migrate Reference](references/go-migrate-reference.md) - CLI, library, embed.FS, transactions, pitfalls
- [Justfile Reference](references/justfile-reference.md) - Go-specific recipes, task groups, lefthook integration
- [Lefthook Reference](references/lefthook-reference.md) - job filtering, monorepo roots, remote configs, CLI, env vars
- [Go Toolchain Reference](references/go-toolchain-reference.md) - `go.work` workspaces, build and test caches, version stamping, container builds
- [Go Correctness Reference](references/go-correctness-reference.md) - recurring bugs in reviewed Go code: filesystem confinement, context lifetimes, processes, concurrency, SQLite

## Resources

- [Go Official Docs](https://go.dev/doc/)
- [golangci-lint Docs](https://golangci-lint.run/)
- [gofumpt](https://github.com/mvdan/gofumpt)
- [gotestsum](https://github.com/gotestyourself/gotestsum)
- [golang-migrate](https://github.com/golang-migrate/migrate)
- [Lefthook](https://github.com/evilmartians/lefthook)
- [just](https://github.com/casey/just)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [Go 1.27 Release Notes](https://go.dev/doc/go1.27)
- [Go Release History](https://go.dev/doc/devel/release)
