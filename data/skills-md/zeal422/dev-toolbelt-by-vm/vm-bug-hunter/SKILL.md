---
name: vm-bug-hunter
description: Detects actual programming errors including syntax, runtime, logical, semantic, linker, resource, security, type, and index/attribute errors. Auto-detects language and focuses on legitimate bugs, not hallucinations.
---

# Bug Hunter Skill

Comprehensive bug detection for identifying ACTUAL programming errors across all error categories.

## Execution Flow

### Step 1: User Confirmation

**Use the `question` tool to ask if the user is ready to begin:**

```
question tool parameters:
  questions:
    - question: "Are you ready to start searching for BUGS?"
      header: "Bug Hunt"
      options:
        - label: "Yes, let's hunt! (Recommended)"
          description: "Start scanning the codebase for bugs now"
        - label: "Not yet"
          description: "Pause and wait until you're ready"
```

- **If user selects "Not yet":** Stop immediately and respond:
  > "Understood. Bug hunting paused. Let me know when you're ready!"

- **If user selects "Yes, let's hunt!":** Proceed immediately to Step 2 with:
  > "AWESOME! Let's hunt some bugs! Detecting Language..."

### Step 2: Language Detection

**Detect the programming language(s) in the codebase:**

1. Check file extensions (.py, .js, .ts, .java, .cpp, .go, .rs, etc.)
2. Analyze syntax patterns and keywords
3. Check configuration files (package.json, requirements.txt, Cargo.toml, etc.)
4. Display findings

**Single-language output:**
```
Language Detected: Python 3.x
Framework: Django 4.2
Dependencies: 47 packages

Now scanning for bugs...
```

**Multi-language output:**
```
Languages Detected:
  - JavaScript (React 18.2) - 67 files
  - TypeScript (5.0) - 134 files
  - Python (3.11) - 23 files
  
Analyzing each language with appropriate error detection...
```

### Step 3: Tool Provisioning

**For each detected language, provision the optimal analysis tool.**

#### Available Tools by Language

| Language | Optimal Tool | Source | Zero-Install Command |
|----------|--------------|--------|---------------------|
| Python | Ruff | [PyPI](https://pypi.org/project/ruff/) | `uvx ruff check` or `pipx run ruff check` |
| JavaScript | Oxlint | [npm](https://www.npmjs.com/package/oxlint) | `npx oxlint@latest` |
| JavaScript | Biome | [npm](https://www.npmjs.com/package/@biomejs/biome) | `npx @biomejs/biome check` |
| TypeScript | Oxlint | [npm](https://www.npmjs.com/package/oxlint) | `npx oxlint@latest` |
| TypeScript | tsc | [npm](https://www.npmjs.com/package/typescript) | `npx tsc --noEmit` |
| Go | go vet | Built-in | `go vet ./...` |
| Rust | cargo clippy | Built-in | `cargo clippy` |
| Java | javac | Built-in | `javac -Xlint:all` |
| C/C++ | clang-tidy | [LLVM](https://releases.llvm.org/) | System install required |

#### Tool Provisioning Process

**For each language, follow this process:**

1. **Check if the optimal tool is already installed:**
   - Run the tool's version command (e.g., `ruff --version`, `oxlint --version`)
   - If the command succeeds, the tool is available

2. **If the tool is NOT installed, ask the user for permission:**

   > "Optimal tool not found for {language}. Would you like to install {tool} for faster, more accurate scanning?"
   >
   > Source: {official URL}
   > Size: ~{size}MB (cached temporarily, no permanent install)
   >
   > [Yes, download {tool}]  [No, use built-in tools only]

3. **Execute based on user choice:**
   - **If Yes:** Run the zero-install command (e.g., `uvx ruff check .` or `npx oxlint@latest .`)
   - **If No:** Use the built-in fallback tool

#### Built-in Fallback Tools (No Download Required)

| Language | Built-in Tool | Command |
|----------|---------------|---------|
| Python | py_compile | `python -m py_compile file.py` |
| Python | ast module | Parse files using Python's built-in ast module |
| JavaScript | node --check | `node --check file.js` |
| Go | go vet | `go vet ./...` |
| Go | go build | `go build ./...` |
| Rust | cargo check | `cargo check` |
| Rust | cargo clippy | `cargo clippy` |
| Java | javac | `javac -Xlint:all *.java` |

#### Official Tool Sources (Verified)

**Python Tools:**
- ruff: https://pypi.org/project/ruff/ (Official PyPI)
- mypy: https://pypi.org/project/mypy/ (Official PyPI)
- bandit: https://pypi.org/project/bandit/ (Official PyPI)

**JavaScript/TypeScript Tools:**
- oxlint: https://www.npmjs.com/package/oxlint (Official npm)
- biome: https://www.npmjs.com/package/@biomejs/biome (Official npm)
- typescript: https://www.npmjs.com/package/typescript (Official npm)
- eslint: https://www.npmjs.com/package/eslint (Official npm)

#### Security Verification Before Download

**Before downloading any tool, show verification info to the user:**

```
Security Verification:
Tool: {name}
Source: {official URL}
Publisher: {publisher name}
Downloads: {monthly download count}
GitHub: {github URL}

Official package from official registry
Open source license
```

#### Session Caching

Tools downloaded via zero-install are automatically cached:
- **npx:** Cached in `~/.npm/_npx/`
- **uvx:** Cached in `~/.cache/uv/`
- **pipx:** Stored in `~/.local/share/venvs/`

No permanent system modification with npx/uvx!

### Step 4: Scan Codebase

**Run the provisioned tools on the codebase:**

- Execute the selected tool for each detected language
- Collect all errors, warnings, and findings
- Parse tool output into a structured format

### Step 5: Validate & Rank Findings

- Cross-reference errors with official language documentation
- Assign severity scores (1-10)
- Calculate confidence levels
- Rank bugs: Critical (9-10) → Serious (7-8) → Minor (5-6)

### Step 6: Generate Report

Display findings with:
- Bug count summary by severity and category
- Detailed bug list with file locations and line numbers
- Code examples showing the bug and the fix
- Quick wins vs moderate vs strategic fixes

---

## Error Categories

### 1. Syntax Errors (Severity: 10)

**Definition:** Code violates language grammar rules, preventing compilation/execution.

**Detection Strategy:**
- Parse the code with language-specific parsers
- Use real syntax validation tools
- Report exact line and character position

**Python Examples:**
```python
# Missing colon
def calculate(x, y)  # SYNTAX ERROR: expected ':'
    return x + y

def calculate(x, y):  # CORRECT
    return x + y

# Invalid indentation
def process():
    if True:
        print("A")
   print("B")  # INDENTATION ERROR: unindent doesn't match

def process():
    if True:
        print("A")
    print("B")  # CORRECT

# Missing parentheses
print "Hello"  # SYNTAX ERROR (Python 3)
print("Hello")  # CORRECT
```

**JavaScript Examples:**
```javascript
// Missing brace
function test() {
  return 42;
// SYNTAX ERROR: Unexpected end of input

function test() {
  return 42;
}  // CORRECT

// Invalid assignment
5 = x;  // SYNTAX ERROR: Invalid left-hand side in assignment
x = 5;  // CORRECT
```

**C/C++ Examples:**
```cpp
// Missing semicolon
int x = 5  // ERROR: expected ';'
int y = 10;

int x = 5;  // CORRECT
int y = 10;

// Undeclared variable
result = x + y;  // ERROR: 'result' was not declared
int result = x + y;  // CORRECT
```

### 2. Runtime Errors (Severity: 9)

**Definition:** Errors during execution due to unexpected conditions.

**Detection Strategy:**
- Analyze code paths for potential runtime failures
- Check for null/undefined access
- Verify array bounds
- Validate file operations
- Check network/IO operations

**Division by Zero:**
```python
def divide(a, b):
    return a / b  # RUNTIME ERROR if b=0

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b  # PROTECTED
```

**Null/Undefined Access:**
```javascript
// Null reference
const user = null;
console.log(user.name);  // RUNTIME ERROR: Cannot read property 'name' of null

const user = null;
console.log(user?.name);  // CORRECT - optional chaining

// Undefined function
data.sort();  // RUNTIME ERROR if data is string

if (Array.isArray(data)) {
    data.sort();  // CORRECT - type check first
}
```

**File Operations:**
```python
# File not found
file = open("missing.txt")  # RUNTIME ERROR: FileNotFoundError

# Safe approach
from pathlib import Path
if Path("file.txt").exists():
    with open("file.txt") as f:
        data = f.read()  # CORRECT
```

**Memory Access (C/C++):**
```cpp
// Null pointer dereference
int* ptr = nullptr;
int value = *ptr;  // RUNTIME ERROR: Segmentation fault

int* ptr = nullptr;
if (ptr != nullptr) {
    int value = *ptr;  // CORRECT - check before access
}
```

### 3. Logical Errors (Severity: 8)

**Definition:** Code runs without crashing but produces incorrect results.

**Detection Strategy:**
- Analyze algorithm correctness
- Check loop conditions and boundaries
- Verify mathematical operations
- Test edge cases
- Cross-reference with expected behavior

**Off-by-One Errors:**
```python
# Incorrect loop
for i in range(len(arr) - 1):  # LOGICAL ERROR: Misses last element
    process(arr[i])

for i in range(len(arr)):  # CORRECT
    process(arr[i])

# Array indexing
def get_last(arr):
    return arr[len(arr)]  # LOGICAL ERROR (should be len-1)

def get_last(arr):
    return arr[-1]  # CORRECT
```

**Wrong Operator:**
```javascript
// Assignment instead of comparison
if (x = 5) {  // LOGICAL ERROR: Always true, assigns x=5
    console.log("x is 5");
}

if (x === 5) {  // CORRECT - comparison
    console.log("x is 5");
}
```

**Incorrect Algorithm:**
```python
# Wrong calculation
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers) + 1  # LOGICAL ERROR: Why +1?

def calculate_average(numbers):
    return sum(numbers) / len(numbers)  # CORRECT

# Wrong condition
def is_even(n):
    return n % 2 == 1  # LOGICAL ERROR: This checks if ODD

def is_even(n):
    return n % 2 == 0  # CORRECT
```

**Infinite Loops:**
```javascript
// Never-ending loop
let i = 0;
while (i < 10) {
    console.log(i);
    // LOGICAL ERROR: Forgot to increment i
}

let i = 0;
while (i < 10) {
    console.log(i);
    i++;  // CORRECT - loop will terminate
}
```

### 4. Semantic Errors (Severity: 7)

**Definition:** Syntactically correct but doesn't convey intended meaning.

**Detection Strategy:**
- Check variable usage context
- Verify operator applicability
- Analyze data flow
- Identify misused constructs

**Wrong Variable:**
```python
def calculate_total(price, quantity, tax_rate):
    subtotal = price * quantity
    tax = price * tax_rate  # SEMANTIC ERROR: Should use subtotal
    return subtotal + tax

def calculate_total(price, quantity, tax_rate):
    subtotal = price * quantity
    tax = subtotal * tax_rate  # CORRECT
    return subtotal + tax
```

**Misused Operators:**
```javascript
// String concatenation instead of addition
const a = "5";
const b = "10";
const sum = a + b;  // SEMANTIC ERROR: Results in "510" not 15

const sum = Number(a) + Number(b);  // CORRECT: 15
```

**Wrong Context:**
```python
# Modifying immutable
numbers = (1, 2, 3)
numbers[0] = 5  # SEMANTIC ERROR: tuple doesn't support item assignment

numbers = [1, 2, 3]
numbers[0] = 5  # CORRECT - use list if mutation needed
```

### 5. Linker Errors (Severity: 9)

**Definition:** Missing function definitions or unresolved external references.

**Detection Strategy:**
- Verify all declared functions are defined
- Check import/export consistency
- Validate library linkage
- Ensure all dependencies are available

**Missing Function Definition (C/C++):**
```cpp
// Header file
void process_data(int* data, int size);  // Declaration

// Implementation file
// LINKER ERROR: Missing definition

// Correct:
void process_data(int* data, int size) {
    // Implementation
}  // Definition provided
```

**Unresolved Import (JavaScript/TypeScript):**
```javascript
// LINKER ERROR: Import from non-existent module
import { helper } from './missing-module';

// CORRECT - verify module exists
import { helper } from './utils/helper';
```

**Missing Library (Python):**
```python
# LINKER ERROR: No module named 'missing_package'
import missing_package

# CORRECT - ensure package is installed
import required_package
```

### 6. Resource Errors (Severity: 8)

**Definition:** Memory leaks, handle exhaustion, network timeouts.

**Detection Strategy:**
- Track resource allocation/deallocation
- Check for unclosed handles
- Verify timeout configurations
- Monitor memory usage patterns

**Memory Leaks:**
```python
# Memory leak in loop
def process_large_data():
    all_data = []
    for i in range(1000000):
        data = fetch_data(i)
        all_data.append(data)  # RESOURCE ERROR: Keeps everything in memory
    return all_data

def process_large_data():
    for i in range(1000000):
        data = fetch_data(i)
        process(data)
        # CORRECT - data garbage collected after each iteration
```

**Unclosed File Handles:**
```python
# File handle leak
def read_file(path):
    f = open(path)
    data = f.read()
    return data  # RESOURCE ERROR: File never closed

def read_file(path):
    with open(path) as f:
        data = f.read()
    return data  # CORRECT - automatically closed
```

**Resource Exhaustion (C++):**
```cpp
// Memory leak
void process() {
    int* data = new int[1000];
    // RESOURCE ERROR: Never deleted - memory leak
}

void process() {
    int* data = new int[1000];
    delete[] data;  // CORRECT - memory freed
}

// Better: Use smart pointers
void process() {
    auto data = std::make_unique<int[]>(1000);
    // CORRECT - automatically freed
}
```

**Connection Leaks:**
```javascript
// Database connection leak
async function query() {
    const conn = await db.connect();
    const result = await conn.query("SELECT * FROM users");
    return result;  // RESOURCE ERROR: Connection never closed
}

async function query() {
    const conn = await db.connect();
    try {
        const result = await conn.query("SELECT * FROM users");
        return result;
    } finally {
        await conn.close();  // CORRECT - always closed
    }
}
```

### 7. Security Errors (Severity: 10)

**Definition:** Vulnerabilities like buffer overflows, injection, insecure handling.

**Detection Strategy:**
- Scan for injection vulnerabilities
- Check buffer boundaries
- Verify input validation
- Audit authentication/authorization
- Detect insecure cryptography

**SQL Injection:**
```python
# SQL injection vulnerability
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    # SECURITY ERROR: Vulnerable to injection
    # username = "admin' OR '1'='1" would bypass auth
    return db.execute(query)

def get_user(username):
    query = "SELECT * FROM users WHERE name = ?"
    return db.execute(query, (username,))  # CORRECT - parameterized

# ORM is safer
def get_user(username):
    return User.objects.get(name=username)  # CORRECT - ORM handles escaping
```

**XSS Vulnerability:**
```javascript
// Cross-site scripting
function display_message(msg) {
    document.body.innerHTML = msg;
    // SECURITY ERROR: msg = "<script>alert('XSS')</script>" would execute
}

function display_message(msg) {
    const div = document.createElement('div');
    div.textContent = msg;  // CORRECT - escapes HTML
    document.body.appendChild(div);
}
```

**Buffer Overflow (C):**
```c
// Buffer overflow
void copy_string(char* dest, char* src) {
    strcpy(dest, src);  // SECURITY ERROR: No bounds checking
}

void copy_string(char* dest, char* src, size_t dest_size) {
    strncpy(dest, src, dest_size - 1);  // CORRECT - bounds checked
    dest[dest_size - 1] = '\0';
}
```

**Insecure Randomness:**
```python
# Weak random for security
import random
token = random.randint(1000, 9999)  # SECURITY ERROR: Predictable

import secrets
token = secrets.token_urlsafe(32)  # CORRECT - cryptographically secure
```

### 8. Type Errors (Severity: 8)

**Definition:** Operations on incompatible data types.

**Detection Strategy:**
- Verify type compatibility
- Check function signatures
- Validate operator usage
- Use static type checking when available

**Python Type Errors:**
```python
# Type mismatch
def add(a, b):
    return a + b

result = add("5", 10)  # TYPE ERROR: can only concatenate str to str

def add(a: int, b: int) -> int:
    return a + b

result = add(5, 10)  # CORRECT - both integers
```

**JavaScript Type Coercion Issues:**
```javascript
// Unexpected type coercion
const result = "5" - 2;  // 3 (string coerced to number)
const result2 = "5" + 2;  // "52" (number coerced to string)
// TYPE ERROR: Inconsistent behavior

const a = Number("5");
const b = 2;
const result = a - b;  // CORRECT - explicit conversion
const result2 = a + b;  // CORRECT - consistent behavior
```

**TypeScript Example:**
```typescript
// Type error caught at compile time
function greet(name: string): string {
    return "Hello, " + name;
}

greet(42);  // TYPE ERROR: number not assignable to string
greet("Alice");  // CORRECT
```

### 9. Index & Attribute Errors (Severity: 8)

**Definition:** Invalid list indices or non-existent object attributes.

**Detection Strategy:**
- Validate array/list bounds
- Check object property existence
- Verify collection access patterns

**Index Out of Bounds:**
```python
# Index error
numbers = [1, 2, 3]
value = numbers[5]  # INDEX ERROR: list index out of range

numbers = [1, 2, 3]
if len(numbers) > 5:
    value = numbers[5]  # CORRECT - bounds check

# Or use try/except
try:
    value = numbers[5]
except IndexError:
    value = None  # CORRECT - handled
```

**Attribute Error:**
```python
# Missing attribute
class User:
    def __init__(self, name):
        self.name = name

user = User("Alice")
print(user.email)  # ATTRIBUTE ERROR: 'User' has no attribute 'email'

class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email  # CORRECT - attribute defined

# Or use hasattr
if hasattr(user, 'email'):
    print(user.email)  # CORRECT - check first
```

**JavaScript Property Access:**
```javascript
// Undefined property
const user = { name: "Alice" };
console.log(user.email.toLowerCase());
// INDEX ERROR: Cannot read property 'toLowerCase' of undefined

const user = { name: "Alice" };
console.log(user.email?.toLowerCase());  // CORRECT - optional chaining
```

---

## Validation Strategy

**To ensure we find ACTUAL errors, not hallucinations:**

### Tier 1: Optimal Tools (Fastest, Most Accurate)

**Python - Ruff:**
```
uvx ruff check .                    # Syntax + linting + imports + complexity
uvx ruff check --select=ALL .       # All 800+ rules
```

**JavaScript/TypeScript - Oxlint:**
```
npx oxlint@latest .                 # 520+ rules built-in
npx oxlint@latest --type-aware .    # Type-aware linting
```

**TypeScript - Full type checking:**
```
npx tsc --noEmit                    # Official TypeScript compiler
```

### Tier 2: Built-in Tools (Always Available)

**Python:**
```
python -m py_compile file.py        # Syntax check only
```

**JavaScript:**
```
node --check file.js                # Syntax check only
```

**Go:**
```
go vet ./...                        # Built-in static analysis
go build ./...                      # Compilation check
```

**Rust:**
```
cargo check                         # Fast type/compile check
cargo clippy                        # Comprehensive linting
```

**Java:**
```
javac -Xlint:all File.java          # Compile with all warnings
```

### Tier 3: Specialized Security Scanners

**Python security:**
```
uvx bandit check .                  # Security vulnerability scanner
```

**Secrets detection:**
```
npx secretlint .                    # Detect secrets in code
```

### Pattern Matching (Conservative)

**Only flag as error if:**
- Pattern is definitively wrong in the language
- Would cause compilation/runtime failure
- Matches known error patterns from official sources

**DO NOT flag as error:**
- Stylistic choices
- Alternative valid approaches
- Subjective "best practices"
- Hypothetical edge cases

---

## Language-Specific Detection Rules

### Python

**Tool Commands:**
```
# Zero-install (recommended)
uvx ruff check .                           # All default rules
uvx ruff check --select=ALL .              # All 800+ rules
uvx ruff check --select=S,SEC .            # Security rules only

# Built-in fallback
python -m py_compile file.py               # Syntax only
```

**Detection Focus:**
- Syntax errors via AST parsing
- Undefined variables and imports
- Common runtime issues (division by zero, None access)
- Security vulnerabilities (SQL injection, eval/exec, weak crypto)
- Type annotation errors (with mypy)
- Import organization and unused imports

### JavaScript

**Tool Commands:**
```
# Oxlint (fastest)
npx oxlint@latest .                        # All built-in rules
npx oxlint@latest -D all .                 # All diagnostics

# Biome (lint + format)
npx @biomejs/biome check .                 # Linting + formatting

# Built-in fallback
node --check file.js                       # Syntax only
```

**Detection Focus:**
- Syntax errors and parse failures
- == vs === confusion
- Undefined variables
- Async/await misuse
- Callback hell patterns
- Promise error handling
- Null/undefined access patterns

### TypeScript

**Tool Commands:**
```
# Fast linting
npx oxlint@latest .                        # 50-100x faster

# Full type checking
npx tsc --noEmit                           # Official TypeScript compiler

# Built-in fallback
npx tsc --noEmit                           # Uses project's TypeScript
```

**Detection Focus:**
- All JavaScript checks plus:
- Type mismatches and inference errors
- Missing/nullish types
- Incorrect generic usage
- Module resolution errors
- Strict mode violations

### C/C++

**Tool Commands:**
```
# Syntax check
gcc -fsyntax-only file.c
clang -fsyntax-only file.cpp

# Static analysis
clang-tidy file.cpp -- -std=c++17
```

**Detection Focus:**
- Buffer overflows
- Null pointer dereferences
- Memory leaks
- Array bounds violations
- Resource leaks
- Undefined behavior
- Format string vulnerabilities

### Go

**Tool Commands:**
```
go vet ./...                               # Built-in static analysis
go build ./...                             # Compilation check
staticcheck ./...                          # Additional linting (if installed)
```

**Detection Focus:**
- Ignored errors (common Go pitfall)
- Goroutine leaks
- Race conditions (with -race flag)
- Deadlocks
- Channel misuse
- Defer in loop issues

### Rust

**Tool Commands:**
```
cargo check                                # Fast type/compile check
cargo clippy                               # Comprehensive linting
cargo clippy -- -W clippy::all             # All warnings
```

**Detection Focus:**
- Memory safety issues (borrow checker)
- Unwrap on None/Err
- Integer overflow
- Dead code
- Unused variables/imports
- Concurrency issues

### Java

**Tool Commands:**
```
javac -Xlint:all File.java                 # Compile with all warnings
javac -Xlint:unchecked,deprecation *.java  # Specific warnings
```

**Detection Focus:**
- Null pointer risks
- Resource leaks (unclosed streams)
- Type safety warnings
- Deprecated API usage
- Exception handling issues
- Thread safety concerns

---

## Confidence Levels

**Each bug report includes confidence:**

- **100% Confident** - Syntax errors verified by parser
- **95% Confident** - Type errors verified by compiler
- **85% Confident** - Runtime errors from static analysis
- **70% Confident** - Logical errors from pattern matching
- **50% Confident** - Requires testing to confirm

**Only report bugs with >70% confidence unless specifically requested.**

---

## Report Output Format

### Bug Count Summary
```
BUGS FOUND: 23

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
By Severity:
Critical (9-10):  5 bugs
Serious (7-8):    12 bugs
Minor (5-6):      6 bugs

By Category:
Syntax Errors:       3
Runtime Errors:      8
Logical Errors:      4
Type Errors:         5
Security Errors:     2
Resource Errors:     1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Critical Bug Report Template
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUG #1: SQL Injection Vulnerability
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Security Error (Severity: 10)
File: src/db/queries.py:45
Language: Python
Confidence: 95%

Problem:
  User input directly concatenated into SQL query

Buggy Code:
  query = f"SELECT * FROM users WHERE id = {user_id}"

Fixed Code:
  query = "SELECT * FROM users WHERE id = ?"
  db.execute(query, (user_id,))

Impact: Critical - Allows database manipulation
Risk: Immediate exploitation possible
Priority: FIX IMMEDIATELY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Quick Fixes Summary
```
QUICK WINS (< 10 minutes):
1. Fix 3 syntax errors (instant)
2. Add null checks in 5 locations
3. Close 2 unclosed file handles

MODERATE FIXES (30-60 minutes):
1. Refactor SQL queries to use parameterization
2. Add type hints to 12 functions
3. Fix 4 logical errors in algorithms

STRATEGIC FIXES (2+ hours):
1. Implement comprehensive input validation
2. Add error handling throughout
3. Conduct security audit of all user input
```

---

## False Positive Prevention

**NEVER report as bugs:**
- Valid alternative approaches
- Style preferences
- Opinionated "best practices"
- Language features used correctly
- Framework-specific patterns

**DO report:**
- Actual syntax violations
- Guaranteed runtime failures
- Proven logical flaws
- Real security vulnerabilities
- Verified type mismatches

---

## Final Notes

This skill prioritizes **ACCURACY over QUANTITY**. It's better to find 10 real bugs than 100 false positives.

Every reported bug should be:
1. **Verifiable** - Can be confirmed with tools or testing
2. **Actionable** - Clear fix provided
3. **Impactful** - Actually affects code behavior
4. **Confident** - High certainty it's a real issue

Remember: We're hunting REAL bugs, not imaginary ones!