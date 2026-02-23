---
name: yaml-validator
description: Validates YAML syntax and structure for all .yml and .yaml files in the project. Identifies common issues like invalid syntax, indentation errors, missing keys, type mismatches, and provides fixes. Use when editing, creating, or debugging YAML configuration files.
---

# YAML Validator

Validate and fix YAML syntax and structure for all YAML files in the project.

## Purpose

Ensures YAML files follow proper syntax, have valid structure, and comply with schema requirements where applicable.

## When to Use

- Creating new YAML configuration files
- Editing existing .yml/.yaml files
- Debugging YAML syntax errors
- Validating GitHub Actions workflows
- Checking docker-compose files
- Validating Kubernetes manifests
- Pre-commit YAML quality checks
- CI/CD configuration validation

## YAML Syntax Rules

### Basic Structure

```yaml
# Comments start with #
key: value                    # Simple key-value
list:                         # Lists use dash prefix
  - item1
  - item2
nested:                       # Nested objects
  key1: value1
  key2: value2
multiline: |                  # Literal block scalar
  Line 1
  Line 2
flow: >                       # Folded block scalar
  This is a long
  sentence that folds
```

### Data Types

```yaml
string: "value"               # Quoted string
unquoted: value               # Unquoted string
number: 42                    # Integer
float: 3.14                   # Float
boolean: true                 # Boolean (true/false, yes/no, on/off)
null_value: null              # Null
empty: ~                      # Also null
multiline_string: |
  This preserves
  newlines
```

### Indentation Rules

- Use **2 spaces** per indentation level (not tabs)
- Consistent indentation throughout file
- Keys at same level must align
- Lists use 2 additional spaces after dash

```yaml
# Correct
parent:
  child: value
  list:
    - item1
    - item2

# Incorrect - mixed tabs/spaces
parent:
	child: value  # Tab character!

# Incorrect - wrong indentation
parent:
 child: value   # Only 1 space
```

## Common Issues and Fixes

### Issue 1: Invalid Indentation
**Problem:** Mixed spaces and tabs or wrong indentation level
**Fix:** Convert all to 2-space indentation
```yaml
# Wrong
parent:
	child: value

# Correct
parent:
  child: value
```

### Issue 2: Missing Colon
**Problem:** Key without colon separator
**Fix:** Add colon and space after key
```yaml
# Wrong
key value

# Correct
key: value
```

### Issue 3: Special Characters in Strings
**Problem:** Characters like `:`, `{`, `}`, `[`, `]` in unquoted strings
**Fix:** Quote strings containing special characters
```yaml
# Wrong
message: Error: something went wrong

# Correct
message: "Error: something went wrong"
```

### Issue 4: Duplicate Keys
**Problem:** Same key defined multiple times
**Fix:** Remove duplicate or merge values
```yaml
# Wrong
config:
  key: value1
  key: value2

# Correct
config:
  key: value1
  other_key: value2
```

### Issue 5: Unquoted Strings That Look Like Types
**Problem:** `yes`, `no`, `on`, `off`, `true`, `false`, numbers
**Fix:** Quote strings that should be literal text
```yaml
# Wrong - parsed as boolean true
country: YES

# Correct
country: "YES"
```

### Issue 6: Trailing Spaces
**Problem:** Spaces at end of lines
**Fix:** Remove trailing whitespace

### Issue 7: Missing Document Start
**Problem:** File doesn't start with `---`
**Fix:** Optional but recommended for clarity
```yaml
---
# Your content here
```

## File-Specific Validation

### GitHub Actions Workflows (`.github/workflows/*.yml`)

Required structure:
```yaml
name: Workflow Name
on: [push, pull_request]        # Event triggers
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Step name
        run: echo "Hello"
```

Common issues:
- Missing `on:` trigger
- Invalid `runs-on` value
- Missing `steps:`
- Old action versions (v1/v2)

### Docker Compose (`docker-compose.yml`)

```yaml
version: "3.8"
services:
  app:
    image: node:18
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

Common issues:
- Missing version declaration
- Port binding format
- Volume mount syntax

### Kubernetes Manifests (`*.yaml`)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: container-name
      image: nginx:latest
```

Common issues:
- Wrong apiVersion
- Missing required fields (apiVersion, kind, metadata, spec)
- List indentation under containers

## Workflow

### 1. Parse YAML File

```bash
# Basic syntax check
python3 -c "import yaml; yaml.safe_load(open('file.yml'))"

# With better error messages
python3 -c "
import yaml
try:
    with open('file.yml') as f:
        yaml.safe_load(f)
    print('✓ Valid YAML')
except yaml.YAMLError as e:
    print(f'✗ Error: {e}')
"
```

### 2. Validate Structure

Check for:
- [ ] Valid YAML syntax
- [ ] Consistent indentation (2 spaces)
- [ ] No trailing spaces
- [ ] No tabs (spaces only)
- [ ] Proper key-value formatting
- [ ] Valid data types
- [ ] No duplicate keys

### 3. File-Specific Checks

Based on file location and purpose:
- [ ] GitHub Actions: Valid triggers, job structure
- [ ] Docker Compose: Version, service definitions
- [ ] K8s manifests: apiVersion, required fields
- [ ] Config files: Expected schema

### 4. Report Issues

For each violation:
- Line number and column
- Issue type: Error / Warning / Info
- Description of the problem
- Suggested fix with code example

## Validation Commands

```bash
# Install yamllint (recommended)
pip install yamllint

# Validate single file
yamllint file.yml

# Validate with config
yamllint -c .yamllint file.yml

# Check all YAML files
find . -name "*.yml" -o -name "*.yaml" | xargs yamllint

# Using Python (if yamllint not available)
python3 -c "
import yaml
import sys
errors = []
for file in sys.argv[1:]:
    try:
        with open(file) as f:
            yaml.safe_load(f)
        print(f'✓ {file}')
    except Exception as e:
        errors.append(f'✗ {file}: {e}')
        print(f'✗ {file}: {e}')
sys.exit(1 if errors else 0)
" file1.yml file2.yml
```

## yamllint Configuration

Create `.yamllint` in project root:

```yaml
---
yaml-files:
  - '*.yml'
  - '*.yaml'

rules:
  braces:
    min-spaces-inside: 0
    max-spaces-inside: 0
  brackets:
    min-spaces-inside: 0
    max-spaces-inside: 0
  colons:
    max-spaces-after: 1
    max-spaces-before: 0
  commas:
    max-spaces-after: 1
    max-spaces-before: 0
  comments:
    min-spaces-from-content: 1
    require-starting-space: true
  comments-indentation: disable
  document-end: disable
  document-start: disable
  empty-lines:
    max: 2
  empty-values: disable
  indentation:
    spaces: 2
    indent-sequences: true
    check-multi-line-strings: false
  key-duplicates: enable
  key-ordering: disable
  line-length:
    max: 120
  new-line-at-end-of-file: enable
  new-lines:
    type: unix
  octal-values: disable
  quoted-strings: disable
  trailing-spaces: enable
  truthy: disable
```

## Output Format

```
## YAML Validation Report

### Summary
- Files Checked: 5
- Errors: 2
- Warnings: 3
- Status: FAIL

### file1.yml
✓ Valid YAML syntax
⚠ Warning (Line 15): Line too long (145 > 120)

### file2.yml
✗ Error (Line 8, Col 5): Invalid indentation
   Current: 4 spaces
   Expected: 2 spaces
✗ Error (Line 12): Duplicate key "name"

### file3.yml
✓ Valid YAML syntax
⚠ Warning (Line 20): Trailing spaces
```

## Best Practices

### DO
✓ Use 2 spaces for indentation
✓ Quote strings with special characters (:, {, }, [, ])
✓ Use consistent formatting throughout
✓ Validate before committing
✓ Add comments for complex sections
✓ Keep lines under 120 characters
✓ End files with newline
✓ Use `---` document start marker for clarity

### DON'T
✗ Use tabs for indentation
✗ Leave trailing spaces
✗ Mix quoted/unquoted styles inconsistently
✗ Use duplicate keys
✗ Forget to quote strings that look like booleans/numbers
✗ Mix YAML 1.1 and 1.2 features

## Examples

### Valid GitHub Actions

```yaml
---
name: Rust CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: cargo test --all
```

### Valid Docker Compose

```yaml
---
version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Valid Kubernetes

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:alpine
          ports:
            - containerPort: 80
```

## Integration

Use with:
- **github-workflows**: Validate workflow files
- **code-quality**: Pre-commit YAML checks
- **debug-troubleshoot**: Debug parsing errors
- **feature-implement**: Create new config files

## Quick Fixes

```bash
# Fix trailing spaces
sed -i 's/[[:space:]]*$//' file.yml

# Convert tabs to spaces
sed -i 's/\t/  /g' file.yml

# Ensure newline at end
sed -i -e '$a\' file.yml
```
