---
name: godoc
description: |
  How to use `go doc` to look up Go package documentation, types, functions, methods, and source code efficiently.
  Use this skill whenever working with Go code and you need to understand an API — whether it's a standard library package,
  a third-party dependency, or the current project's own packages. Trigger this skill when investigating Go types, interfaces,
  function signatures, method sets, constants, or variables. Prefer `go doc` over reading source files directly when you
  need to understand what a Go API does, because `go doc` gives you exactly the documentation and signatures without noise.
  Also use this skill when the user asks about Go documentation, godoc, or wants to explore a Go package's public API.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/godoc.sh*)
---

# go doc Skill

`go doc` prints documentation comments and signatures for Go packages, symbols (types, funcs, consts, vars), methods, and struct fields. Prefer it over reading source files — it extracts doc comments and type signatures without implementation noise, works across the entire module graph, and groups constructors with types.

## Usage

Use the wrapper script instead of `go doc` directly. It handles `@version` resolution, auto-fallback for packages not in `go.mod`, and multi-target batch lookup:

```bash
# Single target (same as go doc)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh [flags] package.Symbol.Method

# Explicit package/symbol split with : separator
${CLAUDE_SKILL_DIR}/scripts/godoc.sh [flags] package:Symbol.Method

# @version support
${CLAUDE_SKILL_DIR}/scripts/godoc.sh [flags] package@version[/subpkg][:Symbol]

# Multi-target batch lookup (multiple targets in one command)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh [flags] target1 target2 target3

# List subpackages of a module or package
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list package@version
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list package
```

### The `:` separator

`:` explicitly separates the package path from the symbol name. Go import paths and symbol names never contain `:`, so this is always unambiguous.

- **`pkg:Symbol`** — two-arg form: `go doc pkg Symbol`
- **`pkg:`** — package doc (explicit)
- **`pkg@v1.0:Symbol`** — root symbol at specific version
- **`pkg@v1.0/codes:Code`** — subpackage symbol at specific version
- **`pkg@v1.0/codes:`** — subpackage doc (explicit, overrides uppercase heuristic)

Without `:`, the script uses heuristics for `@version` targets (uppercase = symbol, lowercase = subpackage, lowercase.Uppercase = subpackage.Symbol) or passes through to `go doc` directly for non-`@version` targets.

### Examples

```bash
# Standard usage (identical to go doc)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -short encoding/json
${CLAUDE_SKILL_DIR}/scripts/godoc.sh encoding/json.Decoder

# Explicit : separator
${CLAUDE_SKILL_DIR}/scripts/godoc.sh encoding/json:Decoder
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc/codes:Code

# Packages not in go.mod (auto-fallback — no special syntax needed)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh github.com/pelletier/go-toml/v2.Marshal

# Specific version (with heuristic)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0/codes.Code
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0/DialOption
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -short google.golang.org/grpc@latest

# Specific version (with : separator — explicit, no heuristic)
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0:DialOption
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0/codes:Code
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0/codes:

# Multi-target batch lookup
${CLAUDE_SKILL_DIR}/scripts/godoc.sh encoding/json.Decoder encoding/json.Encoder fmt.Printf
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -short google.golang.org/grpc@v1.68.0:DialOption google.golang.org/grpc@v1.68.0:ServerOption

# List subpackages
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list google.golang.org/grpc@v1.68.0
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list net/http
```

## Quick reference

```
go doc                              # package doc for current directory
go doc <pkg>                        # package doc (e.g., encoding/json)
go doc <Sym>                        # symbol in current package (capital = current pkg)
go doc <pkg>.<Sym>                  # symbol in a package
go doc <pkg>.<Sym>.<Method>         # method or field of a symbol
go doc <pkg> <Sym>                  # two-arg form (same as above)
go doc <pkg> <Sym>.<Method>         # two-arg form for method
```

`godoc.sh` additions:

```
godoc.sh <pkg>:<Sym>                # : separator → two-arg form
godoc.sh <pkg>@<ver>[/subpkg]:<Sym> # @version with : separator
godoc.sh target1 target2 ...        # multi-target batch lookup
godoc.sh --list <pkg>[@<ver>]       # list subpackages
```

## Flags

| Flag | Effect | When to use |
|------|--------|-------------|
| `-short` | One-line summary per symbol (no doc comments) | Getting a quick overview of what's in a package — like a table of contents |
| `-all` | Show full documentation for every symbol in the package | When you need comprehensive understanding of an entire package |
| `-src` | Show the full source code of a symbol's declaration and body | When you need to see implementation details, not just the signature |
| `-u` | Include unexported symbols, methods, and fields | When debugging internals or understanding private APIs |
| `-cmd` | Treat `package main` like a regular package (show exported symbols) | Without this flag, `go doc` on a `package main` hides exported symbols |
| `-c` | Case-sensitive symbol matching | By default lowercase in queries matches either case; use `-c` when you need an exact match |
| `-C dir` | Change to `dir` before running the command | When you want to look up symbols in a different module or directory context |

## Common patterns

### Explore an unfamiliar module: `--list` then `-short`

When encountering a module you haven't used before, start by discovering its package structure:

```bash
# What packages does this module have?
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list google.golang.org/grpc@v1.68.0

# Then get an overview of the interesting packages
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -short google.golang.org/grpc@v1.68.0/codes google.golang.org/grpc@v1.68.0/credentials
```

`--list` also works for standard library and packages in go.mod:

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh --list net/http
```

### Explore a package: `-short` then targeted lookups

Do NOT explore a package by calling `go doc <pkg>.<Sym>` repeatedly for each symbol — this is an N+1 anti-pattern. `go doc <pkg>.<Type>` already shows the doc comment, all method signatures, and constructors — do not then call `go doc <pkg>.<Type>.<Method>` for each method.

**Stage 1: `-short` for the table of contents**

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -short <pkg>
```

This gives a one-line-per-symbol overview. For "what API does this package provide?" questions, `-short` output alone is often the complete answer. You may not need Stage 2 at all.

**Stage 2: get full documentation (only if needed)**

Only proceed to Stage 2 when you need details beyond what `-short` shows (doc comments, method signatures, field definitions).

**Option A: `-all` for small/medium packages**

If `-short` shows the package is small or medium-sized (roughly under 500 lines of `-all` output), read `-all` output directly:

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -all <pkg>
```

**Option B: `-all` to file for large packages (recommended for detailed lookups)**

For large packages, save `-all` to a file, then extract what you need:

```bash
# Turn 1: save, check size, and find structure — all in one call
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -all <pkg> > /tmp/pkg-doc.txt
wc -l /tmp/pkg-doc.txt
rg -n '^(type \w+ (interface|struct)|func [A-Z])' /tmp/pkg-doc.txt

# Turn 2: extract multiple sections of interest in one call
# (use line numbers from Turn 1's rg output)
echo "=== Pipeline ===" && sed -n '3441,3520p' /tmp/pkg-doc.txt
echo "=== Tx ===" && sed -n '5870,5950p' /tmp/pkg-doc.txt
echo "=== DialOption functions ===" && rg 'DialOption' /tmp/pkg-doc.txt
```

**Option C: multi-target batch lookup for specific symbols**

When you want full docs for specific symbols identified from `-short`, use multi-target:

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh <pkg>.Client <pkg>.Options <pkg>.Pipeline <pkg>.Tx

# For a specific version:
${CLAUDE_SKILL_DIR}/scripts/godoc.sh google.golang.org/grpc@v1.68.0:ServerOption google.golang.org/grpc@v1.68.0:DialOption google.golang.org/grpc@v1.68.0:CallOption
```

For small packages (like `golang.org/x/sync/errgroup`), `-all` output is short enough to read directly — you can skip the `-short` stage entirely.

Only call `go doc <pkg>.<Type>.<Method>` when the user asks about a **specific** method and you need its doc comment or when the method signature alone is ambiguous.

### Working with `package main`

`go doc` on a command package (package main) hides exported symbols by default — the rationale is that commands expose a CLI, not a Go API. Use `-cmd` to override this:

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -cmd              # show exported symbols in current package main
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -cmd -u           # also include unexported symbols
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -cmd -short       # one-line listing of everything
```

### Investigating unexported internals

When you need to understand private types, methods, or struct fields (for debugging, testing, or code review):

```bash
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -u SomeType               # shows unexported fields and methods too
${CLAUDE_SKILL_DIR}/scripts/godoc.sh -u -src someUnexportedFunc # source code of an unexported function
```

### Finding example code

`go doc` does not show Example functions — they live in `_test.go` files which `go doc` excludes. Use `go test -list` to discover them, then read the source from the module cache or `GOROOT`.

**List available examples:**

```bash
go test -list 'Example' <pkg>                    # in-module packages
go test -list 'Example' encoding/json             # stdlib
```

**Read example source code:**

```bash
# stdlib — source is in GOROOT
grep -A 30 'func ExampleDecoder(' "$(go env GOROOT)/src/encoding/json/example_test.go"

# dependency in go.mod — find via go list
grep -A 30 'func ExampleClient(' \
  "$(go list -m -f '{{.Dir}}' google.golang.org/grpc)/example_test.go"

# package not in go.mod — download to cache, then read
DIR=$(GOFLAGS=-mod=mod go mod download -C /tmp -json github.com/redis/go-redis/v9@latest | jq -r '.Dir')
grep -A 30 'func ExampleClient_Pipelined(' "$DIR/example_test.go"
```

For packages with multiple `*_test.go` files, find the right one first:

```bash
grep -rl 'func Example' "$DIR"/*.go "$DIR"/*_test.go
```

### Alternative: browsing pkg.go.dev

pkg.go.dev can complement `go doc` when you need **example code with expected output** (which `go doc` excludes) or a quick overview without installing a package locally. For version-specific docs, append `@version` to the URL.

**Web fetching tools** (e.g., WebFetch in Claude Code, or equivalent tools in other AI-assisted environments) fetch the HTML and convert it to LLM-readable format, often applying AI-powered extraction or filtering. Output is clean but may be non-deterministically summarized.

**Direct fetch via CLI tools** gives the raw, complete content without AI summarization:

```bash
w3m -dump 'https://pkg.go.dev/golang.org/x/sync/errgroup'                                         # w3m
pandoc -f html -t plain 'https://pkg.go.dev/golang.org/x/sync/errgroup'                            # pandoc
curl -sL 'https://pkg.go.dev/golang.org/x/sync/errgroup' | textutil -convert txt -stdin -stdout    # macOS (textutil requires stdin)
```

**Caveats:** Large packages produce very large HTML (e.g., ~7.5 MB for go-redis) — web fetching tools may heavily summarize, and CLI tools produce very long output. For precise API lookups, `go doc` is more reliable and efficient.

## Decision guide: which flag combination to use

- **"What functions/types does this package have?"** → `godoc.sh -short <pkg>`
- **"What does this function do?"** → `godoc.sh <pkg>.<Func>`
- **"Show me all methods on this type"** → `godoc.sh <pkg>.<Type>` (or `-all` for full docs)
- **"I need to see the implementation"** → `godoc.sh -src <pkg>.<Sym>`
- **"Show me example code"** → `go test -list 'Example' <pkg>` then `grep` the source; or fetch from pkg.go.dev if a web fetching tool is available
- **"Include private stuff too"** → add `-u`
- **"This is a main package"** → add `-cmd`
- **"What's in this whole package?"** → `godoc.sh -all <pkg>`
- **"Docs for a specific version"** → `godoc.sh <pkg>@<version>:Symbol` or `<pkg>@<version>/subpkg:Symbol`
- **"What subpackages does this module have?"** → `godoc.sh --list <pkg>` or `godoc.sh --list <pkg>@<version>`
- **"Multiple symbols at once"** → `godoc.sh target1 target2 target3`
- **"Package not in go.mod"** → just use `godoc.sh` — it auto-fallbacks
