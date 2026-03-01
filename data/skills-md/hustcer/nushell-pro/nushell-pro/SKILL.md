---
name: nushell-pro
description: |
  Comprehensive Nushell scripting best practices, idioms, security, and code review. Use when writing, reviewing, auditing, or refactoring Nushell (.nu) scripts to ensure they follow idiomatic patterns, naming conventions, proper type annotations, functional style, security best practices, and Nushell's unique design principles. Triggers on tasks involving Nushell scripts, modules, custom commands, pipelines, or any .nu file editing. Also helps convert Bash/POSIX scripts to idiomatic Nushell. Covers the type system, data manipulation, performance optimization, security hardening, script review, and common gotchas.
---

# Nushell Pro — Best Practices & Security Skill

Write idiomatic, performant, secure, and maintainable Nushell scripts. This skill enforces Nushell conventions, catches security issues, and helps avoid common pitfalls.

## Core Principles

1. **Think in pipelines** — Data flows through pipelines; prefer functional transformations over imperative loops
2. **Immutability first** — Use `let` by default; only use `mut` when functional alternatives don't apply
3. **Structured data** — Nushell works with tables, records, and lists natively; leverage structured data over string parsing
4. **Static parsing** — All code is parsed before execution; `source`/`use` require parse-time constants
5. **Implicit return** — The last expression's value is the return value; no need for `echo` or `return`
6. **Scoped environment** — Environment changes are local to their block; use `def --env` when caller-side changes are needed
7. **Type safety** — Annotate parameter types and input/output signatures for better error detection and documentation
8. **Parallel ready** — Immutable code enables easy `par-each` parallelization

## Critical: Pipeline Input vs Parameters

**Pipeline input (`$in`) is NOT interchangeable with function parameters!**

```nu
# WRONG — treats pipeline data as first parameter
def my-func [items: list, value: any] {
    $items | append $value
}

# CORRECT — declares pipeline signature
def my-func [value: any]: list -> list {
    $in | append $value
}

# Usage
[1 2 3] | my-func 4  # Works correctly
```

**Why this matters:**

- Pipeline input can be **lazily evaluated** (streaming)
- Parameters are **eagerly evaluated** (loaded into memory)
- Different calling conventions entirely — `$list | func arg` vs `func $list arg`

### Type signature forms

```nu
def func [x: int] { ... }                    # params only
def func []: string -> int { ... }           # pipeline only
def func [x: int]: string -> int { ... }     # both pipeline and params
def func []: [list -> list, string -> list] { ... }  # multiple I/O types
```

## Naming Conventions

| Entity           | Convention             | Example                              |
| ---------------- | ---------------------- | ------------------------------------ |
| Commands         | `kebab-case`           | `fetch-user`, `build-all`            |
| Subcommands      | `kebab-case`           | `"str my-cmd"`, `date list-timezone` |
| Flags            | `kebab-case`           | `--all-caps`, `--output-dir`         |
| Variables/Params | `snake_case`           | `$user_id`, `$file_path`             |
| Environment vars | `SCREAMING_SNAKE_CASE` | `$env.APP_VERSION`                   |
| Constants        | `snake_case`           | `const max_retries = 3`              |

- Prefer full words over abbreviations unless widely known (`url` ok, `usr` not ok)
- Flag variable access replaces dashes with underscores: `--all-caps` -> `$all_caps`

## Formatting Rules

### One-line format (default for short expressions)

```nu
[1 2 3] | each {|x| $x * 2 }
{name: 'Alice', age: 30}
```

### Multi-line format (scripts, >80 chars, nested structures)

```nu
[1 2 3 4] | each {|x|
    $x * 2
}

[
    {name: 'Alice', age: 30}
    {name: 'Bob', age: 25}
]
```

### Spacing rules

- One space before and after `|`
- No space before `|params|` in closures: `{|x| ...}` not `{ |x| ...}`
- One space after `:` in records: `{x: 1}` not `{x:1}`
- Omit commas in lists: `[1 2 3]` not `[1, 2, 3]`
- No trailing spaces
- One space after `,` when used (closure params, etc.)

## Custom Commands Best Practices

### Type annotations and I/O signatures

```nu
# Fully typed with I/O signature
def add-prefix [text: string, --prefix (-p): string = 'INFO']: nothing -> string {
    $'($prefix): ($text)'
}

# Multiple I/O signatures
def to-list []: [
    list -> list
    string -> list
] {
    # implementation
}
```

### Documentation with comments and attributes

```nu
# Fetch user data from the API
#
# Retrieves user information by ID and returns
# a structured record with all available fields.
@example 'Fetch user by ID' { fetch-user 42 }
@category 'network'
def fetch-user [
    id: int           # The user's unique identifier
    --verbose (-v)    # Show detailed request info
]: nothing -> record {
    # implementation
}
```

### Parameter guidelines

- Maximum 2 positional parameters; use flags for the rest
- Provide both long and short flag names: `--output (-o): string`
- Use default values: `def greet [name: string = 'World']`
- Use `?` for optional positional params: `def greet [name?: string]`
- Use rest params for variadic input: `def multi-greet [...names: string]`
- Use `def --wrapped` to wrap external commands and forward unknown flags

### Environment-modifying commands

```nu
def --env setup-project [] {
    cd project-dir
    $env.PROJECT_ROOT = (pwd)
}
```

## Data Manipulation Patterns

### Working with records

```nu
{name: 'Alice', age: 30}          # Create record
$rec1 | merge $rec2                # Merge (right-biased)
[$r1 $r2 $r3] | into record       # Merge many records
$rec | update name {|r| $'Dr. ($r.name)' }  # Update field
$rec | insert active true          # Insert field
$rec | upsert count {|r| ($r.count? | default 0) + 1 }  # Update or insert
$rec | reject password secret_key  # Remove fields
$rec | select name age email       # Keep only these fields
$rec | items {|k, v| $'($k): ($v)' }  # Iterate key-value pairs
$rec | transpose key val           # Convert to table
```

### Working with tables

```nu
$table | where age > 25                          # Filter rows
$table | insert retired {|row| $row.age > 65 }   # Add column
$table | rename -c {age: years}                   # Rename column
$table | group-by status --to-table               # Group by field
$table | transpose name data                      # Transpose rows/columns
$table | join $other_table user_id                 # Inner join
$table | join --left $other user_id                # Left join
```

### Working with lists

```nu
$list | enumerate | where {|e| $e.index > 5 }     # Filter with index
$list | reduce --fold 0 {|it, acc| $acc + $it }   # Accumulate
$list | window 3                                   # Sliding window
$list | chunks 100                                 # Process in batches
$list | flatten                                    # Flatten nested lists
```

### Null safety

```nu
$record.field?                    # Returns null if missing (no error)
$record.field? | default 'N/A'   # Provide fallback
if ($record.field? != null) { }   # Check existence
$list | default -e $fallback      # Default for empty collections
```

## Pipeline & Functional Patterns

### Prefer functional over imperative

```nu
# Bad — imperative with mutable variable
mut total = 0
for item in $items { $total += $item.price }

# Good — functional pipeline
$items | get price | math sum

# Bad — mutable counter
mut i = 0
for file in (ls) { print $'($i): ($file.name)'; $i += 1 }

# Good — enumerate
ls | enumerate | each {|it| $'($it.index): ($it.item.name)' }
```

### Iteration patterns

```nu
# each: transform each element
$list | each {|item| $item * 2 }

# each --flatten: stream outputs (turns list<list<T>> into list<T>)
ls *.txt | each --flatten {|f| open $f.name | lines } | find 'TODO'

# each --keep-empty: preserve null results
[1 2 3] | each --keep-empty {|e| if $e == 2 { 'found' } }

# par-each: parallel processing (I/O or CPU-bound)
$urls | par-each {|url| http get $url }
$urls | par-each --threads 4 {|url| http get $url }

# reduce: accumulate (first element is initial acc if no --fold)
[1 2 3 4] | reduce {|it, acc| $acc + $it }

# generate: create values from arbitrary sources without mut
generate {|state| { out: ($state * 2), next: ($state + 1) } } 1 | first 5
```

### Row conditions vs closures

```nu
# Row conditions — short-hand syntax, auto-expands $it
ls | where type == file              # Simple and readable
$table | where size > 100            # Expands to: $it.size > 100

# Closures — full flexibility, can be stored and reused
let big_files = {|row| $row.size > 1mb }
ls | where $big_files
$list | where {$in > 10}             # Use $in or parameter
```

**Use row conditions** for simple field comparisons; **use closures** for complex logic or reusable conditions.

### Pipeline input with $in

```nu
def double-all []: list<int> -> list<int> {
    $in | each {|x| $x * 2 }
}

# Capture $in early when needed later (it's consumed on first use)
def process []: table -> table {
    let input = $in
    let count = $input | length
    $input | first ($count // 2)
}
```

## Variable Best Practices

### Prefer immutability

```nu
let config = (open config.toml)
let names = $config.users | get name

# Acceptable — mut when no functional alternative
mut retries = 0
loop {
    if (try-connect) { break }
    $retries += 1
    if $retries >= 3 { error make {msg: 'Connection failed'} }
    sleep 1sec
}
```

### Constants for parse-time values

```nu
const lib_path = 'src/lib.nu'
source $lib_path                  # Works: const is resolved at parse time

let lib_path = 'src/lib.nu'
source $lib_path                  # Error: let is runtime only
```

### Closures cannot capture mut

```nu
mut count = 0
ls | each {|f| $count += 1 }     # Error! Closures can't capture mut

# Solutions:
ls | length                       # Use built-in commands
[1 2 3] | reduce {|x, acc| $acc + $x }  # Use reduce
for f in (ls) { $count += 1 }    # Use a loop if mutation truly needed
```

## String Conventions

Refer to [String Formats Reference](references/string-formats.md) for the full priority and rules.

**Quick summary (high to low priority):**

1. Bare words in arrays: `[foo bar baz]`
2. Raw strings for regex: `r#'(?:pattern)'#`
3. Single quotes: `'simple string'`
4. Single-quoted interpolation: `$'Hello, ($name)!'`
5. Double quotes only for escapes: `"line1\nline2"`
6. Double-quoted interpolation: `$"tab:\t($value)\n"` (only with escapes)

## Modules & Scripts

### Module structure

```
my-module/
├── mod.nu              # Module entry point
├── utils.nu            # Submodule
└── tests/
    └── mod.nu          # Test module
```

### Export rules

- Only `export` definitions are public; non-exported are private
- Use `export def main` when command name matches module name
- Use `export use submodule.nu *` to re-export submodule commands
- Use `export-env` for environment setup blocks

### Script with main command and subcommands

```nu
#!/usr/bin/env nu

# Build the project
def "main build" [--release (-r)] {
    print 'Building...'
}

# Run tests
def "main test" [--verbose (-v)] {
    print 'Testing...'
}

def main [] {
    print 'Usage: script.nu <build|test>'
}
```

For stdin access in shebang scripts: `#!/usr/bin/env -S nu --stdin`

## Error Handling

### Custom errors with span info

```nu
def validate-age [age: int] {
    if $age < 0 or $age > 150 {
        error make {
            msg: 'Invalid age value'
            label: {
                text: $'Age must be between 0 and 150, got ($age)'
                span: (metadata $age).span
            }
        }
    }
    $age
}
```

### try/catch and graceful degradation

```nu
let result = try {
    http get $url
} catch {|err|
    print -e $'Request failed: ($err.msg)'
    null
}

# Use complete for detailed external command error info
let result = (^some-external-cmd | complete)
if $result.exit_code != 0 {
    print -e $'Error: ($result.stderr)'
}
```

### Suppress errors with `do -i`

`do -i` (ignore errors) runs a closure and suppresses any errors, returning null on failure. `do -c` (capture errors) catches errors and returns them as values.

```nu
# Ignore errors — returns null if the closure fails
do -i { rm non_existent_file }

# Use as a concise fallback
let val = (do -i { open config.toml | get setting } | default 'fallback')

# Capture errors as values (instead of aborting the pipeline)
let result = (do -c { ^some-cmd })
```

**When to use each approach:**
- `do -i` — Fire-and-forget, or when you only need a default on failure
- `do -c` — Catch errors as values to abort downstream pipeline on failure
- `try/catch` — When you need to inspect or log the error
- `complete` — When you need exit code + stdout + stderr from external commands

## Testing

### Using std assert

```nu
use std/assert

for t in [[input expected]; [0 0] [1 1] [2 1] [5 5]] {
    assert equal (fib $t.input) $t.expected
}
```

### Custom assertions

```nu
def "assert even" [number: int] {
    assert ($number mod 2 == 0) --error-label {
        text: $'($number) is not an even number'
        span: (metadata $number).span
    }
}
```

## Debugging Techniques

```nu
$value | describe                 # Inspect type
$data | each {|x| print $x; $x } # Print intermediate values (pass-through)
timeit { expensive-command }      # Measure execution time
metadata $value                   # Inspect span and other metadata
```

## Security Best Practices

Refer to [Security Reference](references/security.md) for the full guide.

Nushell is safer than Bash by design (no `eval`, arguments passed as arrays not through shell), but security risks remain.

### Never execute untrusted input as code

```nu
# DANGEROUS — arbitrary code execution
^nu -c $user_input
source $user_provided_file

# DANGEROUS — shell interprets the string
^sh -c $'echo ($user_input)'
^bash -c $user_input
```

### Separate commands from arguments (prevent injection)

```nu
# Bad — constructing command strings
let cmd = $'ls ($user_path)'
^sh -c $cmd

# Good — pass arguments directly (no shell interpretation)
^ls $user_path
run-external 'ls' $user_path
```

### Validate and sanitize paths

```nu
# Bad — path traversal possible
def read-file [name: string] { open $name }

# Good — validate against traversal
def read-file [name: string, --base-dir: string = '.'] {
    let full = ($base_dir | path join $name | path expand)
    let base = ($base_dir | path expand)
    if not ($full | str starts-with $base) {
        error make {msg: $'Path traversal detected: ($name)'}
    }
    open $full
}
```

### Protect credentials

```nu
# Bad — credential visible to all child processes and in env
$env.API_KEY = 'secret-key-123'
^curl -H $'Authorization: Bearer ($env.API_KEY)' $url

# Good — scope credentials, use with-env
with-env {API_KEY: (open ~/.secrets/api_key | str trim)} {
    ^curl -H $'Authorization: Bearer ($env.API_KEY)' $url
}
```

### Safe file operations

```nu
# Bad — predictable temp file, race condition
let tmp = '/tmp/my-script-tmp'
'data' | save $tmp

# Good — use mktemp for unique temp files
let tmp = (^mktemp | str trim)
'data' | save $tmp
# ... use $tmp ...
rm $tmp
```

### Handle external command errors

```nu
let result = (^cargo build o+e>| complete)
if $result.exit_code != 0 {
    error make {msg: $'Build failed: ($result.stderr)'}
}
```

### Safe rm operations

```nu
# Bad — glob from variable, could match unintended files
^rm $'($user_dir)/*'

# Good — validate then use trash or explicit paths
if ($user_dir | path type) == 'dir' {
    rm -r $user_dir
}
```

## Script Review Checklist

Refer to [Script Review Reference](references/script-review.md) for the full checklist.

When reviewing a Nushell script, check these categories in order:

### 1. Security review (highest priority)

- [ ] No `nu -c` / `source` / `^sh -c` with untrusted input
- [ ] No credential hardcoding or env leaking
- [ ] Paths from user input are validated (no traversal)
- [ ] External commands use argument separation (not string concatenation)
- [ ] Temp files use `mktemp`, not predictable paths
- [ ] `rm` operations are guarded and intentional

### 2. Correctness review

- [ ] Type annotations on all exported commands
- [ ] I/O pipeline signatures match actual behavior
- [ ] Error handling with `try/catch` for fallible operations
- [ ] External commands checked with `complete` when error handling matters
- [ ] Optional fields accessed with `?` operator
- [ ] No `for` as final expression (use `each` instead)
- [ ] `mut` not captured in closures

### 3. Style review

- [ ] Naming: kebab-case commands, snake_case variables
- [ ] String format priority followed
- [ ] Formatting: spacing, line length, multi-line rules
- [ ] Documentation comments on exported commands
- [ ] `^` prefix on external commands
- [ ] Functional style preferred over imperative

### 4. Performance review

- [ ] `par-each` for I/O or CPU-bound parallel work
- [ ] `each --flatten` for streaming when appropriate
- [ ] Expensive computations cached in `let` bindings
- [ ] Large files streamed (lazy), not loaded entirely

## Common Pitfalls

Refer to [Anti-Patterns Reference](references/anti-patterns.md) for detailed explanations.

| Anti-Pattern                          | Fix                                              |
| ------------------------------------- | ------------------------------------------------ |
| `echo $value`                         | Just `$value` (implicit return)                  |
| `$"simple text"`                      | `'simple text'` (no interpolation needed)        |
| `for` as final expression             | Use `each` (for doesn't return a value)          |
| `mut` for accumulation                | Use `reduce` or `math sum`                       |
| `let path = ...; source $path`        | `const path = ...; source $path`                 |
| `"hello" > file.txt`                  | `'hello' \| save file.txt`                       |
| `grep pattern`                        | `where $it =~ pattern` or built-in `find`        |
| Parsing string output                 | Use structured commands (`ls`, `ps`, `http get`) |
| `$env.FOO = bar` inside `def`         | Use `def --env`                                  |
| `{ \| x \| ... }` (space before pipe) | `{\|x\| ...}` (no space before params)           |
| `$record.missing` (error)             | `$record.missing?` (returns null)                |
| `each` on single record               | Use `items` or `transpose` instead               |
| External cmd without `^`              | Use `^grep` to be explicit about externals       |

## Best Practices Summary

1. **Use type signatures** — Catch errors early, improve documentation
2. **Prefer pipelines** — More idiomatic, composable, and streamable
3. **Document with comments** — `#` above `def` for help integration
4. **Export selectively** — Don't pollute namespace
5. **Use `default`** — Handle null/missing gracefully
6. **Validate inputs** — Check types/ranges at function start
7. **Return consistent types** — Don't mix null and values unexpectedly
8. **Use modules** — Organize related functions
9. **Prefix external commands with `^`** — `^grep` not `grep`; Nushell builtins take precedence (e.g., `find` is Nushell's, not Unix `find`)
10. **Use external tools when faster** — `^rg` for large file search, `^jq` for giant JSON

## Workflow

When writing or reviewing Nushell code:

1. **Read existing code** to understand the context
2. **Security audit** — Check for injection, path traversal, credential leaks (see [Security](references/security.md))
3. **Check naming** — kebab-case commands, snake_case variables
4. **Check types** — Add/verify type annotations and I/O signatures
5. **Check strings** — Follow the string format priority
6. **Check patterns** — Prefer functional pipelines over imperative loops
7. **Check formatting** — Spacing, line length, multi-line rules
8. **Check documentation** — Comments for exported commands, parameter descriptions
9. **Check error handling** — try/catch, complete for externals, validate inputs
10. **Run validation** if possible — `nu -c 'source file.nu'` or `nu file.nu`
11. **Summarize changes** made with security findings highlighted

## References

- [Security](references/security.md) — Security hardening, threat model, safe patterns
- [Script Review](references/script-review.md) — Comprehensive review checklist
- [String Formats](references/string-formats.md) — String type priority and conversion rules
- [Anti-Patterns](references/anti-patterns.md) — Common mistakes with detailed fixes
- [Data & Type System](references/data-and-types.md) — Type hierarchy, collections, conversions, type guards
- [Advanced Patterns](references/advanced-patterns.md) — Performance, streaming, closures, memory efficiency
- [Modules & Scripts](references/modules-and-scripts.md) — Module system, testing, attributes
- [Bash to Nushell](references/bash-to-nushell.md) — Conversion guide from Bash/POSIX

## Getting Help

- Use `nu -c 'help <command>'` to check command signatures and examples
- Use Nushell MCP tools for evaluating and testing Nushell code
- Consult the [Nushell Book](https://www.nushell.sh/book/) for in-depth documentation
