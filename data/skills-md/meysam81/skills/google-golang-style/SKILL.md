---
name: google-golang-style
description: >
  Enforces Google's official Go style guide when writing or editing Go (.go) files.
  Use this skill BEFORE creating, modifying, or reviewing any Go code. Covers naming
  (packages, receivers, variables, repetition avoidance), error handling (structure,
  wrapping, strings, sentinel errors), imports (grouping, renaming, blank imports),
  code organization (package size, file structure), and documentation (doc comments,
  godoc conventions). Trigger on any Go code task — new files, refactors, code reviews,
  or architecture decisions involving Go packages.
---

# Google Go Style Guide for Claude Code

This skill distills Google's official Go style guide into actionable rules.
The guide prioritizes these attributes in order: **Clarity > Simplicity > Concision > Maintainability > Consistency**.

Clarity means the reader understands what the code does and why. Simplicity means accomplishing goals without unnecessary abstraction. These two trump all other concerns.

## Formatting

All Go source files must conform to `gofmt` output. Never manually adjust formatting that `gofmt` handles.

Use `MixedCaps` or `mixedCaps` for all multi-word names. Never use `snake_case` or `SCREAMING_SNAKE_CASE`, even for constants.

```go
// Correct.
const MaxPacketSize = 512
var userCount int

// Wrong.
const MAX_PACKET_SIZE = 512
var user_count int
```

## Line Length

There is no fixed line length. If a line feels too long, prefer refactoring (extracting a variable, helper function) over splitting it. If the line is already as short as practical, let it remain long.

Do not split a line before an indentation change (function declaration, conditional). Do not split long strings (like URLs) across multiple lines.

When wrapping function parameters, group by semantic meaning, not column width:

```go
// Group by meaning.
canvas.RenderHeptagon(
    fillColor,
    x0, y0, vertexColor0,
    x1, y1, vertexColor1,
    // ...
)
```

## Naming

Names should not feel repetitive when used, should account for context, and should not repeat concepts that are already clear.

### Package Names

- Lowercase only, no underscores, no mixedCaps: `tabwriter` not `tabWriter`.
- Name describes what it provides, not what it contains.
- Avoid `util`, `helper`, `common`, `model` — these are uninformative at call sites.
- Avoid names likely shadowed by local variables: `usercount` over `count`.

```go
// Good: clear at the call site.
db := spannertest.NewDatabaseFromFile(...)
b := elliptic.Marshal(curve, x, y)

// Bad: uninformative.
db := test.NewDatabaseFromFile(...)
b := helper.Marshal(curve, x, y)
```

### Receiver Names

Short (1-2 letters), abbreviation of the type, consistent across all methods:

```go
func (t Tray) Size() int          // not (tray Tray) or (this Tray)
func (ri *ResearchInfo) Update()  // not (info *ResearchInfo)
func (s *Scanner) Next() Token    // not (self *Scanner)
```

### Variable Names

Length proportional to scope, inversely proportional to usage frequency:

- Small scope (1-7 lines): single letter or short word (`i`, `c`, `r`).
- Medium scope (8-15 lines): single descriptive word (`count`, `users`).
- Large scope (15-25 lines): multi-word (`userCount`, `projectName`).
- Very large scope (25+ lines): fully descriptive names.

Familiar abbreviations for common types: `r` for `io.Reader`/`*http.Request`, `w` for `io.Writer`/`http.ResponseWriter`, `ctx` for `context.Context`.

Omit the type from the name:

```go
var users int        // not numUsers, usersInt
var name string      // not nameString
var primary *Project // not primaryProject
```

### Avoid Repetition

This is the most impactful naming rule. Repetition makes code noisy and harder to read.

**Package vs. exported name** — don't repeat the package name in the symbol:

```go
// Good.
widget.New()           // not widget.NewWidget()
db.Load()              // not db.LoadFromDatabase()

// If the package exports only one type named after itself,
// the constructor is just New.
```

**Method vs. receiver** — don't repeat the receiver type:

```go
func (c *Config) WriteTo(w io.Writer)   // not WriteConfigTo
func (p *Project) Name() string         // not ProjectName()
```

**Context vs. local name** — strip information already provided by context:

```go
// In package "sqldb":
type Connection struct{} // not DBConnection

// In a method of *DB:
func (db *DB) UserCount() (int, error) {
    var count int64 // not userCountInt64
    if err := db.Load("count(distinct users)", &count); err != nil {
        return 0, fmt.Errorf("load user count: %s", err)
    }
    return int(count), nil
}
```

### Initialisms

Initialisms keep consistent case: `URL` or `url`, never `Url`. `ID` not `Id`. `HTTP` not `Http`.

| Scope      | Correct                      | Incorrect                    |
| ---------- | ---------------------------- | ---------------------------- |
| Exported   | `XMLAPI`, `ID`, `DB`, `GRPC` | `XmlApi`, `Id`, `Db`, `Grpc` |
| Unexported | `xmlAPI`, `id`, `db`, `gRPC` | `xmlapi`, `iD`, `dB`, `grpc` |

### Getters

No `Get` prefix. Use the noun directly:

```go
func (c *Config) Name() string   // not GetName()
func (u *User) Counts() int      // not GetCounts()
```

Use `Compute` or `Fetch` when the operation is expensive or involves I/O, to signal that the call may block.

### Constants

MixedCaps only. Name by role, not by value:

```go
const MaxPacketSize = 512     // not MAX_PACKET_SIZE, not kMaxPacketSize
const ExecuteBit = 1 << iota  // not Twelve = 12
```

## Error Handling

### Returning Errors

`error` is always the last return value. Return `nil` for success. Always return `error` (the interface), never a concrete error type from exported functions.

```go
// Good.
func Lookup() (*Result, error)

// Bad: concrete error type can cause nil-pointer-in-interface bugs.
func Bad() *os.PathError
```

### Error Strings

Not capitalized (unless starting with an exported name or proper noun). No trailing punctuation.

```go
err := fmt.Errorf("something bad happened")     // Good.
err := fmt.Errorf("Something bad happened.")     // Bad.
```

Full display messages (logs, test failures, UI) should be capitalized:

```go
log.Errorf("Operation aborted: %v", err)
t.Errorf("Op(%q) failed unexpectedly; err=%v", args, err)
```

### Wrapping Errors

Use `%w` when callers need to inspect the underlying error with `errors.Is`/`errors.As`. Use `%v` when you want to add context but hide the chain (especially at system boundaries like RPCs).

Add context that the underlying error doesn't already provide. Don't duplicate information:

```go
// Good: adds meaningful context.
if err := os.Open("settings.txt"); err != nil {
    return fmt.Errorf("launch codes unavailable: %w", err)
}

// Bad: duplicates the filename already in os.Open's error.
if err := os.Open("settings.txt"); err != nil {
    return fmt.Errorf("could not open settings.txt: %w", err)
}

// Bad: annotation adds no information.
return fmt.Errorf("failed: %w", err) // just return err
```

### Sentinel Errors

Define package-level sentinel errors for expected conditions callers need to distinguish. Use `errors.Is()` to check (handles wrapped errors).

```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Caller checks with errors.Is, not ==.
if errors.Is(err, ErrNotFound) {
    // handle missing resource
}
```

### Handle Every Error

Never discard errors with `_` unless the function is documented to never fail. When discarding, comment why:

```go
n, _ := b.Write(p) // never returns a non-nil error
```

Otherwise, handle it, return it, or in exceptional cases call `log.Fatal`. Do not `panic`.

### Avoid In-Band Errors

Don't return -1, "", or nil to signal errors. Use multiple return values:

```go
// Good.
func Lookup(key string) (value string, ok bool)

// Bad: caller can't distinguish "not found" from empty string.
func Lookup(key string) string
```

## Imports

### Grouping

Four groups, separated by blank lines, in this order:

1. Standard library
2. Third-party / project packages
3. Protocol buffer imports (with `pb` suffix)
4. Side-effect imports (`_ "package"`)

```go
import (
    "fmt"
    "os"

    "github.com/user/project/internal/config"
    "golang.org/x/text/encoding"

    foopb "myproj/foo/proto/proto"

    _ "myproj/rpc/protocols/dial"
)
```

### Renaming

Avoid renaming imports unless necessary. Valid reasons:

- Name collision with another import.
- Generated proto packages (must rename to remove underscores, add `pb` suffix).
- Uninformative names like `v1` — rename to something descriptive: `core "k8s.io/api/core/v1"`.
- Collision with common local variable — add `pkg` suffix: `urlpkg`.

### Blank and Dot Imports

Blank imports (`_ "package"`) only in `main` packages or tests. Never in library code.

Never use dot imports (`import . "package"`). They obscure where symbols come from.

## Documentation

### Doc Comments

All exported names must have doc comments. Start with the name of the thing being described. Use full sentences.

```go
// A Request represents a request to run a command.
type Request struct { ... }

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) { ... }
```

Unexported types with non-obvious behavior should also have doc comments.

### Comment Style

Doc comments: full sentences, capitalized, punctuated.
End-of-line comments for struct fields: can be fragments.

```go
type Server struct {
    // BaseDir points to the base directory for data storage.
    BaseDir string

    WelcomeMessage  string // displayed when user logs in
    ProtocolVersion string // checked against incoming requests
    PageLength      int    // optional; default: 20
}
```

Comment line length: aim for readability on 80-column terminals, but no hard limit.

### Package Comments

Immediately above the `package` clause, no blank line between them:

```go
// Package math provides basic constants and mathematical functions.
package math
```

One package comment per package. For `main` packages, describe the command.

## Code Organization

### Simplicity First

Use the least mechanism needed. Prefer core language constructs (channels, slices, maps, loops, structs) over libraries. Look in stdlib before adding dependencies. A `map[string]bool` is fine for set membership — don't import a set library for that.

### Package Size

- Group types whose implementations are tightly coupled.
- If a user must import two packages to use either meaningfully, combine them.
- Don't put everything in one package — conceptually distinct things get their own package.
- No "one type, one file" rule. Files should be focused enough that a maintainer can tell which file has what.

### Test Doubles

Place test doubles in a separate `<package>test` package (e.g., `creditcardtest`). Name stubs by behavior when there are multiple:

```go
package creditcardtest

// AlwaysCharges stubs creditcard.Service and simulates success.
type AlwaysCharges struct{}

func (AlwaysCharges) Charge(*creditcard.Card, money.Money) error { return nil }

// AlwaysDeclines stubs creditcard.Service and simulates declined charges.
type AlwaysDeclines struct{}

func (AlwaysDeclines) Charge(*creditcard.Card, money.Money) error {
    return creditcard.ErrDeclined
}
```

### Happy Path

Structure code so the success path flows straight down. Handle errors immediately, then continue with main logic. Avoid nesting the success case inside conditions.

```go
// Good: happy path flows down.
func Process(id string) (*User, error) {
    user, err := db.GetUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }

    if err := user.Validate(); err != nil {
        return nil, fmt.Errorf("validate user %s: %w", id, err)
    }

    return user, nil
}
```

### Shadowing

Be careful with `:=` in new scopes — it creates a new variable that shadows the outer one. This is a common source of bugs with `ctx` and `err`:

```go
// Bug: ctx inside the if is a new variable; outer ctx unchanged.
if *shortenDeadlines {
    ctx, cancel := context.WithTimeout(ctx, 3*time.Second) // shadows!
    defer cancel()
}
// ctx here is still the original, unbounded context.

// Fix: declare cancel separately, use = not :=.
if *shortenDeadlines {
    var cancel func()
    ctx, cancel = context.WithTimeout(ctx, 3*time.Second)
    defer cancel()
}
```

## Quick Reference: Common Mistakes

| Mistake                            | Fix                                       |
| ---------------------------------- | ----------------------------------------- |
| `MAX_PACKET_SIZE`                  | `MaxPacketSize`                           |
| `widget.NewWidget()`               | `widget.New()`                            |
| `func (c *Config) GetName()`       | `func (c *Config) Name()`                 |
| `var numUsers int`                 | `var users int`                           |
| `return err` (bare, no context)    | `return fmt.Errorf("operation: %w", err)` |
| `err := fmt.Errorf("Failed.")`     | `err := fmt.Errorf("failed")`             |
| `func Bad() *os.PathError`         | `func Bad() error`                        |
| Splitting lines at 80/100/120 cols | Refactor if too long; otherwise let it be |
| `import . "foo"`                   | `import "foo"` and qualify: `foo.Bar()`   |
| `package util`                     | Name by what it provides                  |
