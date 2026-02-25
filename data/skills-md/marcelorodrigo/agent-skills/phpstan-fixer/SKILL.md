---
name: phpstan-fixer
description: |
  Fix PHPStan static analysis errors by adding type annotations and PHPDocs.
  Use when encountering PHPStan errors, type mismatches, missing type hints,
  or static analysis failures. Never ignores errors without user approval.
license: MIT
compatibility: Requires PHPStan installed in project
metadata:
  version: "1.0.0"
---

# PHPStan Error Fixer
Fix PHPStan static analysis errors through proper type annotations, PHPDocs, and 
code improvements. This skill teaches agents how to resolve errors without 
suppressing them, respecting the project's configured strictness level.

## Core Principles

1. **Never suppress errors as first resort** — Fix the root cause with proper
   types and annotations
2. **Respect user configuration** — Never modify `phpstan.neon` settings
   (level, paths, parameters)
3. **No silent ignoring** — Never add `ignoreErrors` to config without explicit
   user approval
4. **Context-aware fixes** — Understand the project type (Laravel, Symfony,
   vanilla PHP) before proposing solutions
5. **Ask before ignoring** — If a legitimate ignore is needed, explain why and
   get user approval first
6. **Don't fix third-party code** — Never modify files in `vendor/`. Use stub
   files instead to override wrong types

## Workflow

### Step 1: Understand the Project Context

Before fixing errors, identify the project type:

```bash
# Check for Laravel
grep laravel/framework composer.json

# Check for Symfony
grep symfony/symfony composer.json

# Check for PHPStan extensions
grep phpstan composer.json

# Read PHPStan config
cat phpstan.neon

# Check project guidelines
cat AGENTS.md
```

**Key information to extract:**
- PHPStan level (0-10, or max)
- Installed PHPStan extensions (larastan, phpstan-strict-rules, etc.)
- Framework-specific helpers (Laravel IDE Helper, Symfony plugin)
- Project-specific type conventions

### Step 2: Analyze the Error

PHPStan errors have this structure:

```text
------ ----------------------------------------------
Line   /path/to/File.php
------ ----------------------------------------------
42     Parameter $user of method foo() has invalid
       type App\User.
       💡 Identifier: parameter.type
------ ----------------------------------------------
```

**Extract:**
1. **Error identifier** (e.g., `parameter.type`, `missingType.return`)
2. **Error location** (file, line number)
3. **Context** (what's the code trying to do?)

### Step 3: Apply the Right Fix

Use the error identifier to determine the fix strategy:

### Step 4: Verify the Fix

After applying fixes, run PHPStan again to confirm:

```bash
vendor/bin/phpstan analyse
```

**Important:**
- If new errors appear, the fix may have been incorrect. Re-analyze the error and try a different approach.
- If the same error persists, the fix wasn't applied correctly. Double-check the code.
- If errors are resolved, mark the fix as successful and move to the next error.

---

## Common Error Fixes

### Type-Related Errors

#### `missingType.parameter` — Missing parameter type

**Error:**
```text
Parameter $name has no type specified.
```

**Fix — Add native type:**
```php
// Before
function greet($name) {
    return "Hello, $name";
}

// After
function greet(string $name): string {
    return "Hello, $name";
}
```

**Fix — Use PHPDoc for complex types:**
```php
// Before
function processUsers($users) { ... }

// After
/**
 * @param array<int, User> $users
 */
function processUsers(array $users): void { ... }
```

---

#### `missingType.return` — Missing return type

**Error:**
```text
Method foo() has no return type specified.
```

**Fix — Add native return type:**
```php
// Before
public function getUser() {
    return $this->user;
}

// After
public function getUser(): User {
    return $this->user;
}
```

**Fix — Use PHPDoc for union/intersection types:**
```php
// Before
public function findUser($id) { ... }

// After
/**
 * @return User|null
 */
public function findUser(int $id): ?User { ... }
```

---

#### `argument.type` — Wrong argument type

**Error:**
```text
Parameter #1 $id of method find() expects int, string given.
```

**Fix — Cast the argument:**
```php
// Before
$user = $repository->find($request->input('id'));

// After
$user = $repository->find((int) $request->input('id'));
```

**Fix — Narrow the type earlier:**
```php
// Better approach
$id = $request->integer('id'); // Laravel helper
$user = $repository->find($id);
```

---

#### `return.type` — Wrong return type

**Error:**
```text
Method foo() should return User but returns User|null.
```

**Fix — Adjust return type:**
```php
// Before
public function getUser(): User {
    return $this->user ?? null;
}

// After
public function getUser(): ?User {
    return $this->user ?? null;
}
```

**Fix — Ensure non-null with assertion:**
```php
public function getUser(): User {
    assert($this->user !== null);
    return $this->user;
}
```

---

### Property Errors

#### `property.notFound` — Undefined property access

**Error:**
```text
Access to an undefined property User::$name.
```

**Fix — Add property declaration:**
```php
class User {
    private string $name;
    
    public function __construct(string $name) {
        $this->name = $name;
    }
}
```

**Fix — Document magic property:**
```php
/**
 * @property string $name
 */
class User {
    public function __get($key) { ... }
}
```

**Fix (Laravel) — Use IDE Helper:**
```bash
# Generate PHPDocs for Eloquent models
php artisan ide-helper:models
```

---

#### `property.onlyWritten` — Property written but never read

**Error:**
```text
Property User::$name is never read, only written.
```

**Fix — Remove unused property or add getter:**
```php
// If truly unused, remove it
// If needed, add usage:
public function getName(): string {
    return $this->name;
}
```

---

### Method Errors

#### `method.notFound` — Undefined method call

**Error:**
```text
Call to an undefined method App\User::getFullName().
```

**Fix — Add method:**
```php
class User {
    public function getFullName(): string {
        return $this->first_name . ' ' . $this->last_name;
    }
}
```

**Fix — Document magic method:**
```php
/**
 * @method string getFullName()
 */
class User {
    public function __call($method, $args) { ... }
}
```

**Fix (Laravel) — Add to `@mixin` for query builders:**
```php
/**
 * @mixin \Illuminate\Database\Eloquent\Builder
 */
class User extends Model { ... }
```

---

### Array/Offset Errors

#### `offsetAccess.notFound` — Undefined array offset

**Error:**
```text
Offset 'email' does not exist on array.
```

**Fix — Use array shape PHPDoc:**
```php
/**
 * @param array{email: string, name: string} $data
 */
function createUser(array $data): void {
    echo $data['email']; // PHPStan knows this exists
}
```

**Fix — Add existence check:**
```php
if (isset($data['email'])) {
    echo $data['email'];
}
```

**Fix — Use null coalescing:**
```php
$email = $data['email'] ?? 'default@example.com';
```

---

### Generics Errors

#### `missingType.generics` — Missing generic type

**Error:**
```text
Class Collection has @template T but does not specify it.
```

**Fix — Specify generic type in PHPDoc:**
```php
// Before
/** @var Collection $users */
$users = User::all();

// After
/** @var Collection<int, User> $users */
$users = User::all();
```

**Fix (Laravel) — Use IDE Helper stubs for collections.**

---

### Dead Code Errors

#### `deadCode.unreachable` — Unreachable code

**Error:**
```text
Unreachable statement - code above always terminates.
```

**Fix — Remove dead code:**
```php
// Before
function foo() {
    return true;
    echo "This never runs"; // Error
}

// After
function foo() {
    return true;
}
```

---

#### `identical.alwaysTrue` / `identical.alwaysFalse` — Condition is always true/false

**Error:**
```text
Strict comparison using === between int and string will always evaluate to false.
```

**Fix — Remove useless condition or fix type:**
```php
// Before
if ($id === '123') { ... } // $id is int

// After
if ($id === 123) { ... }
```

---

## Framework-Specific Fixes

### Laravel

**Install Larastan for Laravel-aware analysis:**
```bash
composer require --dev larastan/larastan
```

**Check `phpstan.neon` includes Larastan** (ask user to add if missing):
```yaml
includes:
    - vendor/larastan/larastan/extension.neon
```

**Common Laravel fixes:**

```php
// Eloquent relationships - use @property PHPDoc
/**
 * @property-read \Illuminate\Database\Eloquent\Collection<int, Post> $posts
 */
class User extends Model {
    public function posts() {
        return $this->hasMany(Post::class);
    }
}

// Collections - specify generic types
/** @var \Illuminate\Support\Collection<int, User> $users */
$users = User::all();

// Request input - use typed helpers
$id = $request->integer('id'); // Not $request->input('id')
$email = $request->string('email')->toString();
```

### Symfony

**Install Symfony PHPStan extension:**
```bash
composer require --dev phpstan/phpstan-symfony
```

**Check `phpstan.neon` includes Symfony extension** (ask user to add if missing):
```yaml
includes:
    - vendor/phpstan/phpstan-symfony/extension.neon
parameters:
    symfony:
        containerXmlPath: var/cache/dev/App_KernelDevDebugContainer.xml
```

**Common Symfony fixes:**

```php
// Service container - use proper type hints
public function __construct(
    private UserRepository $userRepository, // Not mixed
) {}

// Forms - type the data
/** @var array{email: string, password: string} $data */
$data = $form->getData();
```

---

## When Ignoring is Acceptable (Last Resort)

Sometimes a legitimate ignore is needed. **Always ask the user first using the Question tool**:

**Step 1: Explain the situation**
```text
I found a PHPStan error that cannot be easily fixed:

Error: [describe error]
Location: [file:line]
Reason: [explain why it can't be fixed]
```

**Step 2: Use Question tool to get user choice**
```text
Use the Question tool with these options:
- Header: "PHPStan Error Resolution"
- Question: "How would you like to handle this error?"
- Options:
  1. "Use @phpstan-ignore with comment" - description: "Add inline ignore with explanation (recommended for third-party type issues)"
  2. "Add to baseline" - description: "Generate baseline file (recommended for legacy code migration)"
  3. "Refactor code" - description: "Modify code to satisfy PHPStan (most robust but may require significant changes)"
  4. "Skip for now" - description: "Leave unfixed and continue with other errors"
```

**Example Question tool usage:**
```json
{
  "questions": [{
    "header": "PHPStan Error Resolution",
    "question": "File src/Service.php:42 has argument type mismatch with third-party API. How should I handle this?",
    "options": [
      {
        "label": "Use @phpstan-ignore (Recommended)",
        "description": "Add inline ignore with explanation"
      },
      {
        "label": "Add to baseline",
        "description": "Include in baseline file for tracking"
      },
      {
        "label": "Refactor code",
        "description": "Modify to satisfy PHPStan"
      },
      {
        "label": "Skip for now",
        "description": "Continue with other errors"
      }
    ]
  }]
}
```

**Valid reasons for ignoring:**
- Third-party library with wrong types (and no stub file available)
- Reflection-based code that's correct but PHPStan can't understand
- Complex business logic that's type-safe at runtime but not provably so statically
- Temporary during large refactoring (use baseline)

**How to ignore (if approved):**

```php
// Inline ignore with explanation
/** @phpstan-ignore argument.type (API returns string|int, we handle both) */
$result = $api->getValue();

// Baseline for legacy code
vendor/bin/phpstan analyse --generate-baseline
```

**Never do this without approval:**
```yaml
# Don't add this to phpstan.neon without user consent
parameters:
    ignoreErrors:
        - '#.*#' # NEVER
```

---

## Debugging Types

Use `\PHPStan\dumpType()` to see what PHPStan thinks:

```php
$user = User::find($id);
\PHPStan\dumpType($user); // Reports: App\User|null

// Remove before committing!
```

---

## Troubleshooting

### PHPStan doesn't recognize a valid type

**Check:**
1. Is the class autoloadable? (`composer dump-autoload`)
2. Does PHPStan scan the file? (Check `paths` in `phpstan.neon`)
3. Is there a typo in the namespace?

### Type inference doesn't work

**Check:**
1. Are you using inline `@var` too much? (Fix at source instead)
2. Is the function/method return type specified?
3. Are you using dynamic features PHPStan can't analyze?

### Laravel magic methods not recognized

**Install and run:**
```bash
composer require --dev barryvdh/laravel-ide-helper
php artisan ide-helper:generate
php artisan ide-helper:models --write
php artisan ide-helper:meta
```

---

## Error Identifier Reference

Full list: https://phpstan.org/error-identifiers

**Most common categories:**
- `argument.*` — Function/method argument issues
- `return.*` — Return type mismatches
- `missingType.*` — Missing type declarations
- `property.*` — Property access/declaration issues
- `method.*` — Method call issues
- `offsetAccess.*` — Array/ArrayAccess issues
- `class.*` — Class inheritance/usage issues
- `deadCode.*` — Unreachable code
- `identical.*` / `equal.*` — Comparison issues

---

## Resources

- [PHPStan User Guide](https://phpstan.org/user-guide/getting-started)
- [PHPDoc Types](https://phpstan.org/writing-php-code/phpdoc-types)
- [Error Identifiers](https://phpstan.org/error-identifiers)
- [Troubleshooting Types](https://phpstan.org/user-guide/troubleshooting-types)
- [Larastan (Laravel)](https://github.com/larastan/larastan)
- [PHPStan Symfony Extension](https://github.com/phpstan/phpstan-symfony)