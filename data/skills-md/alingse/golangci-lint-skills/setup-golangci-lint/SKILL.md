---
name: setup-golangci-lint
description: Quickly set up golangci-lint environment for Go projects. Auto-detect version, create config, integrate CI, generate smart ignore rules, ensure existing code passes safely.
user-invocable: true
disable-model-invocation: false
---

# golangci-lint Environment Setup

Quickly set up a complete golangci-lint environment for Go projects.

> **Core Principle**: Make existing code pass lint by adjusting configuration, **do not modify existing code**. Only affects new code.

## When to Use

- Initializing Go projects and need to add linter
- Adding code quality checks to existing projects
- Integrating lint into CI/CD workflows

## Execution Flow

### 1. Detect Environment

```bash
# Check Go version in go.mod (priority)
cat go.mod | grep "^go "

# Check system Go version (reference)
go version

# Check for existing configuration (supports 4 formats)
ls .golangci.* 2>/dev/null || echo "No config"

# Check CI configuration
ls .gitlab-ci.yml .github/workflows/*.yml .circleci/config.yml 2>/dev/null

# Check for Makefile
ls Makefile 2>/dev/null && echo "Has Makefile" || echo "No Makefile"
```

### 2. Select Version

Select based on Go version in `go.mod`:

| go.mod Version | golangci-lint Version |
|----------------|----------------------|
| < 1.20 | v1.x |
| >= 1.20 | v2.x (recommended) |

### 3. Install

**Method 1: Using install script (cross-platform, recommended)**

```bash
# v2 (recommended)
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin latest

# v1
# curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.59.1

# Verify
$(go env GOPATH)/bin/golangci-lint --version
```

**Method 2: Using go install (requires Go 1.20+)**

```bash
# v2 (recommended for Go >= 1.20)
go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest

# v1 (for Go < 1.20 or legacy projects)
# go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Verify
golangci-lint --version
```

### 3.5. Configuration Migration (when v1 config exists)

If the project already has `.golangci.yml` in v1 format, use the auto-migration tool:

```bash
# Automatically migrate v1 config to v2 format
$(go env GOPATH)/bin/golangci-lint migrate --skip-validation

# Notes:
# --skip-validation: Skip validation, convert directly (recommended)
# migrate command will automatically:
#   - Add version: 2
#   - Convert enable-all/disable-all to linters.default
#   - Change linters-settings to linters.settings
#   - Change issues.exclude-rules to linters.exclusions.rules
```

After migration, manually check the configuration to ensure:
- `linters.default` value meets expectations (standard/all/none/fast)
- Disabled linters still have `# TODO fix later by human` comments
- Complexity thresholds are raised and marked with `# TODO reduce this`

### 4. Create Configuration

Skip this step if `.golangci.yml` already exists.

> **📌 AI Operation Requirements**:
> 1. **Must** first visit official documentation to confirm latest format: https://golangci-lint.run/docs/configuration/file/
> 2. **Core Principle**: **Do not modify existing code**, only make code pass by adjusting configuration (settings/disable/exclusions)
> 3. **Formatters Handling**:
>    - First run `gofmt -l .` and `goimports -l .` to check code format
>    - If both have no output → enable formatters (uncomment)
>    - If has output → keep commented, add `# TODO format code and enable - X files currently non-compliant` above
> 4. **Workflow**: Create minimal config → Run lint → **Categorize and handle** → Add standardized TODO comments
> 5. **Universal Classification Logic** (based on keywords in linter description):
>
>    **Step 1: Get linter description**
>    ```bash
>    $(go env GOPATH)/bin/golangci-lint help <linter-name>
>    ```
>
>    **Step 2: Categorize based on keywords in description**
>
>    | Category | Keywords in Description | Action | Example Linters & Descriptions |
>    |----------|------------------------|--------|-------------------------------|
>    | **a. Configurable** | complexity, long, deeply, count, length, size, max, min, limit | Adjust settings | funlen: "Checks for **long** functions"<br>gocyclo: "Checks cyclomatic **complexity**"<br>nestif: "Reports **deeply** nested if"<br>dogsled: "Checks **too many** blank identifiers" |
>    | **b. Code Style-Manual Confirm** | style, format, naming, whitespace, align, order, declaration | disable + TODO | godot: "Check if comments end in period"<br>tagalign: "Check struct tags well **aligned**"<br>misspell: "Finds commonly **misspelled**"<br>varnamelen: "Checks variable name **length**" |
>    | **c. Critical Bugs-Suggest Fix** | bug, security, error, check, nil, unsafe, detect, inspects | disable + TODO | errcheck: "Checking for **unchecked errors**"<br>gosec: "**Inspects** source code for **security**"<br>staticcheck: "set of rules from staticcheck"<br>nilerr: "returns **nil** even if error is not **nil**" |
>    | **d. Cannot Modify** | (check specific error message, usually involves external constraints) | exclusions | canonicalheader: HTTP header spec (3rd-party APIs)<br>asciicheck: Non-ASCII symbols (Chinese function names) |
>    | **e. Can Fix Small** | (determined by actual issue count, < 5) | exclude-rules | Any linter with few issues |
>    | **f. New Features-Defer** | modern, new, latest, replace, simplification, feature | disable + TODO | modernize: "suggest **simplifications** using **modern** language"<br>exptostd: "replaced by **std** functions"<br>usestdlibvars: "use variables from **standard library**" |
>
>    **Step 3: Complete Decision Tree**
>    ```
>    1. Issue count < 5?
>       ├── Yes → Category e (can fix small): exclude-rules
>       └── No → Continue
>    2. Description has complexity/long/deeply/max/min/limit/length?
>       ├── Yes → Category a (configurable): Prioritize adjusting settings
>       └── No → Continue
>    3. Specific error caused by external constraints (3rd-party APIs/generated code/Chinese naming)?
>       ├── Yes → Category d (cannot modify): exclusions path exclusion
>       └── No → Continue
>    4. Description has modern/new/latest/replace/std/simplification?
>       ├── Yes → Category f (new features-defer): disable + TODO
>       └── No → Continue
>    5. Description has bug/security/error/check/nil/unsafe/detect/inspects?
>       ├── Yes → Category c (critical bugs-suggest fix): disable + TODO
>       └── No → Category b (code style-manual confirm): disable + TODO
>    ```
>
>    **Example Demonstrations**:
>
>    | Linter | Description | Keywords | Category |
>    |--------|-------------|----------|----------|
>    | cyclop | "Checks function **complexity**" | complexity | a |
>    | gocritic | "checks for **bugs**, performance and **style**" | bugs (priority) | c |
>    | revive | "replacement of golint" | (no clear keywords) | b |
>    | bodyclose | "Checks whether response body is **closed successfully**" | error/check | c |
>    | goconst | "Finds repeated strings that could be replaced by a **constant**" | (style) | b |
>    | fatcontext | "Detects **nested contexts**" | nested → complexity | a |
>
> 6. **Configuration Priority**:
>    - **1st Priority**: Adjust `settings` thresholds (e.g., funlen.lines, gocyclo.min-complexity)
>    - **2nd Priority**: Use `linters.exclusions` path exclusion (code that cannot be modified)
>    - **3rd Priority**: Use `issues.exclude-rules` rule-based exclusion (specific few issues)
>    - **Last Resort**: Completely `disable` (many issues and cannot be resolved via config)
> 7. **Avoid Duplicates**: Each linter appears only once, check for duplicates

**v2 Minimal Configuration Template (.golangci.yml)**

```yaml
version: "2"

run:
  concurrency: 4
  timeout: 5m
  skip-dirs: [vendor, third_party, testdata, examples, gen-go]
  tests: true

output:
  format: colored-line-number
  print-linter-name: true

linters:
  default: all

formatters:
  enable:
    # TODO format code and enable - 17 files currently non-compliant with goimports
    # - gofmt
    # - goimports
```

> **Formatters Handling**: First run `gofmt -l .` and `goimports -l .` to check, uncomment to enable if both have no output.

> **Notes**:
> - Start with minimal configuration, no preset disable
> - After running, gradually add `disable` and `exclusions` based on errors
> - Common linters that need adjustment (add as needed):
>   - `mnd` (magic numbers) → style issues, can be permanently ignored
>   - `wsl` (whitespace) → style issues, can be permanently ignored
>   - `lll` (line length) → style issues, can be permanently ignored
>   - `err113` → error handling, temporarily ignore and mark TODO

**v1 Configuration Template (.golangci.yml)**

> **Note**: v1 does not require `version` field. v2 is recommended.

```yaml
run:
  concurrency: 4
  timeout: 5m
  skip-dirs: [vendor, testdata]

linters:
  enable-all: true
```

> After running, add `disable` and `exclude-rules` based on errors.

### 5. Integrate CI

**GitLab CI**

```yaml
lint:
  stage: test
  image: golang:1.23-alpine
  script:
    - curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin latest
    - $(go env GOPATH)/bin/golangci-lint run --timeout=5m ./...
```

**GitHub Actions**

```yaml
- name: golangci-lint
  uses: golangci/golangci-lint-action@v6
  with:
    version: latest
```

### 6. Update Makefile (Optional)

```makefile
lint:  ## Run lint check
	golangci-lint run --timeout=5m ./...

lint-fix:  ## Auto-fix issues
	golangci-lint run --fix --timeout=5m ./...
```

### 7. Run and Adjust as Needed

```bash
# Run lint
$(go env GOPATH)/bin/golangci-lint run --timeout=5m ./...
```

> **Important**: Resolve issues by adjusting configuration, **do not modify existing code**.

**Analyze Based on Error Output**:

1. **Linter Name Errors** (e.g., `unknown linters`):
   ```bash
   # View supported linters
   $(go env GOPATH)/bin/golangci-lint help linters
   ```
   - `gomnd` → `mnd`
   - `goerr113` → `err113`
   - `execinquery` → removed

2. **Configuration Format Errors**:
   - `output.formats` needs map format, not list
   - Use singular form `output.format`

3. **Adjust Configuration Based on Actual Errors**:

   **Configuration Priority** (try in order):

   | Priority | Action | Use Case |
   |----------|--------|----------|
   | **1️⃣ Highest** | Adjust `settings` thresholds | Linters with config options for complexity/length |
   | **2️⃣ Second** | `linters.exclusions` path exclusion | Code that cannot be modified (generated/3rd-party) |
   | **3️⃣ Then** | `issues.exclude-rules` rule exclusion | Specific few issues |
   | **4️⃣ Last** | `disable` completely | Many issues and no config options |

   **Category a: Configurable (Prioritize adjusting settings)**

   ```yaml
   linters:
     settings:
       # Complexity linters: Prioritize adjusting thresholds rather than completely disabling
       funlen:
         lines: 100        # Default 60, raised to accommodate existing code
         statements: 60    # Default 40
       gocyclo:
         min-complexity: 25  # Default 15
       gocognit:
         min-complexity: 30  # Default 15
       nestif:
         min-complexity: 8   # Default 5
       # If still have issues after adjusting thresholds, then consider disable
   ```

   **Category b: Code Style-Manual Confirm**

   ```yaml
   linters:
     disable:
       # TODO code style-confirm whether to disable: Does not affect functionality, requires manual confirmation
       - mnd              # 47 issues: magic numbers, style issues
       - wsl              # 39 issues: whitespace, deprecated, replaced by wsl_v5
       - wsl_v5           # 50 issues: whitespace v5, code style
       - lll              # 46 issues: line length limit, style issues
       - godot            # 3 issues: comment period
       - tagalign         # 12 issues: struct tag alignment
       - tagliatelle      # 50 issues: struct tag naming convention
       - whitespace       # 3 issues: whitespace issues
       - goconst          # 7 issues: constant extraction suggestion
       - prealloc         # 2 issues: pre-allocate slice suggestion
       - nakedret         # 1 issue: naked return
       - nlreturn         # 9 issues: blank line before return
       - inamedparam      # 1 issue: named parameter
       - varnamelen       # 23 issues: variable name length
       - nonamedreturns   # 2 issues: named return values
       - paralleltest     # 47 issues: parallel test suggestion
       - testpackage      # 3 issues: test package naming
       - testifylint      # 3 issues: testify usage convention
       - ireturn          # 4 issues: interface return
       - intrange         # 3 issues: int range loop
       - nilnil           # 3 issues: nil interface
       - nilnesserr       # 3 issues: nil error check
       - noinlineerr      # 3 issues: inline error
       - gosmopolitan     # 3 issues: internationalization
       - usestdlibvars    # 1 issue: standard library constants
       - unparam          # 1 issue: unused parameter
       - perfsprint       # 9 issues: performance print suggestion
   ```

   **Category c: Critical Bugs-Suggest Fix**

   ```yaml
   linters:
     disable:
       # TODO critical bugs-suggest fix: Security and error handling issues, recommend gradual fixes
       - errcheck         # 13 issues: unchecked errors
       - gosec            # 10 issues: security checks
       - staticcheck      # 8 issues: static analysis
       - rowserrcheck     # 3 issues: database rows.Err check
       - errchkjson       # 4 issues: JSON error check
       - errorlint        # 1 issue: error handling convention
       - errname          # 2 issues: error variable naming
       - wrapcheck       # 44 issues: error wrapping
       - noctx            # 3 issues: context parameter check
       - forcetypeassert  # 2 issues: force type assertion
       - contextcheck     # 4 issues: context passing check
       - nilerr           # nil error check
       - govet            # 1 issue: vet check
       - unused           # 16 issues: unused variables/packages
       - err113           # 21 issues: dynamic error definition
       - ineffassign      # 1 issue: ineffective assignment
       - sqlclosecheck    # 3 issues: SQL not closed check
       - wastedassign     # 2 issues: wasted assignment
   ```

   **Category d: Cannot Modify (Path Exclusion)**

   ```yaml
   linters:
     exclusions:
       rules:
         # Generated code (cannot modify)
         - path: \.pb\.go|\.gen\.go|\.gen-\w+\.go|\.mock\.go
           linters: [all]

         # Third-party dependencies (cannot modify)
         - path: vendor/|third_party/
           linters: [all]

         # Example code (optionally modifiable)
         - path: examples/
           linters: [all]

   issues:
     exclude-rules:
       # Third-party APIs (cannot modify)
       - text: "non-canonical header"
         linters: [canonicalheader]

       # Chinese function names (business requirement, cannot modify)
       - text: "ID.*must match"
         linters: [asciicheck]

       # Internal project using internal packages (business requirement)
       - text: "import of package"
         linters: [depguard]
   ```

   **Category e: Can Fix Small (Few Specific Issues)**

   ```yaml
   issues:
     exclude-rules:
       # Specific business scenarios (cannot modify)
       - text: "G101: potential hardcoded credential"
         path: config/.*\.go
         linters: [gosec]

       # Relax for test files
       - path: _test\.go
         linters: [errcheck, gosec, contextcheck]

       # Relax for main function
       - path: cmd/
         linters: [gocyclo, funlen, errcheck]
   ```

   **Category f: New Features-Defer**

   ```yaml
   linters:
     disable:
       # TODO new features-defer: Does not affect current code, can be selectively enabled later
       - modernize        # 12 issues: modern Go syntax suggestions
       - revive           # 48 issues: revive ruleset
       - gocritic         # 10 issues: code style suggestions
       - godoclint        # 3 issues: godoc format
       - gomoddirectives  # module directive check
       - dogsled          # blank identifier count
       - embeddedstructfieldcheck # 2 issues: embedded field blank lines
       - exhaustruct      # 49 issues: struct field completeness
       - forbidigo        # 6 issues: forbid specific functions
       - gochecknoglobals # 15 issues: global variable check
       - gochecknoinits   # 2 issues: init function check
       - godox            # 2 issues: TODO/FIXME markers
       - nolintlint       # 1 issue: nolint comment check
   ```

**Goal**: Existing code passes lint, **do not modify existing code**, new code must follow rules.

### 8. Final Verification

```bash
# Run again to ensure pass
$(go env GOPATH)/bin/golangci-lint run --timeout=5m ./...

# Or use make
make lint
```

## Output Report Template

```markdown
# golangci-lint Configuration Complete

## Environment Information
- Go Version (go.mod): go 1.23
- golangci-lint Version: v2.8.0

## Configuration
- Created: .golangci.yml (version: 2)
- Initial Config: linters.default: all (minimal config)

## Issue Handling

### Handling Priority

| Priority | Method | Linters |
|----------|--------|---------|
| 1️⃣ Adjust settings | Threshold tuning | funlen, gocyclo, gocognit, nestif |
| 2️⃣ exclusions | Path exclusion | Generated code, 3rd-party dependencies, specific APIs |
| 3️⃣ exclude-rules | Rule exclusion | Test files, specific business scenarios |
| 4️⃣ disable | Completely disable | Linters with many issues |

### Linter Category Statistics

| Category | Count | Description |
|----------|-------|-------------|
| a. Configurable | 4 | Prioritize adjusting settings thresholds |
| b. Code Style-Manual Confirm | 26 | Style issues, need confirmation whether to disable |
| c. Critical Bugs-Suggest Fix | 18 | Security/error handling, recommend fixing |
| d. Cannot Modify | - | Path exclusion (external constraints) |
| e. Can Fix Small | - | Issues exclusion (few issues) |
| f. New Features-Defer | 13 | New features, consider later |

### Settings Threshold Adjustments
```yaml
linters:
  settings:
    funlen:
      lines: 100        # Default 60
      statements: 60    # Default 40
    gocyclo:
      min-complexity: 25  # Default 15
    gocognit:
      min-complexity: 30  # Default 15
    nestif:
      min-complexity: 8   # Default 5
```

### Path Exclusions (Cannot Modify)
- Generated code: `.pb.go`, `.gen.go`, `.mock.go`
- Third-party dependencies: `vendor/`, `third_party/`
- Example code: `examples/`

### Issues Exclusions (Specific Scenarios)
- Third-party APIs: `non-canonical header` (canonicalheader)
- Chinese function names: `ID.*must match` (asciicheck)
- Test files: Relax errcheck, gosec, contextcheck

## Next Steps
1. New code must pass lint
2. Prioritize fixing issues in "c. Critical Bugs-Suggest Fix" category
3. After code improvements, gradually reduce complexity thresholds
4. Regularly run `make lint` checks
```

## Notes

1. **Core Principle**: **Do not modify existing code**, only adjust configuration to make code pass lint
2. **v2 Configuration Format**: Must add `version: 2`, use `linters.default` instead of `enable-all`
3. **Do Not Modify Existing Configuration**
4. **Style Issues Can Be Permanently Ignored**: Function length, cyclomatic complexity, etc. do not affect functionality
5. **Critical Issues Need Fix Reminders**: errcheck, gosec, staticcheck, etc. (exclude via config, do not fix directly)
6. **New Code Must Not Bypass Checks**
7. **CI Needs Sufficient Resources**: Recommend at least 2GB memory

## Related Resources

- [Official Documentation](https://golangci-lint.run/)
- [Supported Linters](https://golangci-lint.run/usage/linters/)
