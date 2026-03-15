---
name: java-code-review
description: >-
  Review Java source code for bugs, security vulnerabilities, performance
  problems, concurrency issues, AI-generated code quality issues, dependency
  licensing risks, and best practice violations. Use when a user asks to review
  Java code, audit Java files, find bugs in Java, check Java code quality,
  detect AI slop, check library licenses, or perform a code review on .java
  files. Accepts code provided directly, as local file paths, as directory
  paths, or as unified diff output.
---

# Java Code Review

Review Java source code systematically for correctness, security, performance,
and maintainability.

## Input Handling

Determine the input type and gather code accordingly:

1. **Direct code** -- Code provided in the conversation. Review as-is.
2. **File path(s)** -- Read the specified `.java` files.
3. **Directory path** -- Find all `.java` files recursively. For large
   codebases (>50 files), ask the user which packages or files to focus on.
4. **Diff/patch content** -- Review only the changed lines plus sufficient
   surrounding context. Focus findings on the changed code.

## Review Process

Execute these phases in order. For each finding, assign a severity.

### Phase 1: Correctness and Bug Detection

Examine code for:

- **Null safety** -- Nullable parameters without checks, Optional misuse,
  potential NullPointerException paths
- **Resource leaks** -- Unclosed streams, connections, or locks. Verify
  try-with-resources usage for all AutoCloseable types
- **Error handling** -- Empty catch blocks, catching overly broad exceptions
  (Exception, Throwable), swallowed exceptions, missing finally blocks
- **Concurrency** -- Race conditions, unsynchronized shared mutable state,
  incorrect use of volatile, double-checked locking without volatile,
  ConcurrentModificationException risks
- **Logic errors** -- Off-by-one, incorrect operator precedence, unreachable
  code, broken equals/hashCode contracts
- **API misuse** -- Incorrect use of Collections, Streams, Date/Time API,
  String comparison with == instead of .equals()

### Phase 2: Security Review

Read [references/security-checklist.md](references/security-checklist.md)
before this phase.

Check for:

- **Injection** -- SQL injection (string concatenation in queries), command
  injection, LDAP injection, XPath injection, log injection
- **Authentication and authorization** -- Hardcoded credentials, missing
  access checks, insecure token handling
- **Data exposure** -- Sensitive data in logs, exceptions, or error messages.
  Unmasked PII
- **Cryptography** -- Weak algorithms (MD5, SHA-1 for security), hardcoded
  keys, insecure random (Math.random for security purposes)
- **Deserialization** -- Untrusted ObjectInputStream usage, missing type
  validation
- **Input validation** -- Missing or insufficient validation of external input,
  path traversal risks

### Phase 3: Performance Analysis

Read [references/performance-patterns.md](references/performance-patterns.md)
before this phase.

Check for:

- **Algorithmic complexity** -- O(n^2) or worse in hot paths, unnecessary
  nested iterations
- **Memory** -- Excessive object creation in loops, large collections held
  longer than needed, missing initial capacity for known-size collections
- **String handling** -- String concatenation in loops (use StringBuilder),
  unnecessary String.format in hot paths
- **I/O** -- Unbuffered streams, N+1 query patterns, missing connection
  pooling, synchronous I/O where async is appropriate
- **Collections** -- Wrong collection type for the access pattern, unnecessary
  copying, missing pre-sizing
- **JVM considerations** -- Excessive autoboxing, finalizer usage, classloader
  leaks

### Phase 4: Code Quality and Maintainability

Check for:

- **Design** -- God classes, excessive coupling, Liskov substitution
  violations, missing encapsulation
- **Naming** -- Unclear variable/method names, naming convention violations
  (Java conventions: camelCase methods, PascalCase classes, UPPER_SNAKE
  constants)
- **Complexity** -- Methods exceeding ~30 lines, cyclomatic complexity >10,
  deeply nested conditionals (>3 levels)
- **Duplication** -- Repeated logic that should be extracted
- **Documentation** -- Missing Javadoc on public API, outdated comments that
  contradict code
- **Testing gaps** -- Untested public methods, missing edge case tests,
  no assertions in test methods, test methods that cannot fail
- **AI-generated code smells** -- Hallucinated or non-existent API calls,
  overly verbose boilerplate that could use standard library methods,
  unnecessary wrapper classes or abstractions that add indirection without
  value, generic variable names (data, result, temp, info) that obscure
  intent, contradictory or parroted comments that restate the code without
  adding insight, TODO/FIXME/placeholder blocks left unimplemented,
  inconsistent patterns within the same file (e.g., mixing builder and
  constructor styles, mixing streams and loops for identical tasks),
  dead code or unreachable branches that suggest generation artifacts

### Phase 5: Dependency and License Review

If build files are available (`pom.xml`, `build.gradle`, `build.gradle.kts`),
or if import statements reference third-party libraries, check for:

- **License compatibility** -- Copyleft licenses (GPL, AGPL, LGPL) in
  proprietary or permissively licensed projects. Flag any dependency whose
  license is incompatible with the project's declared license
- **License presence** -- Dependencies with no discernible license (treat as
  all-rights-reserved). Unlicensed code cannot be safely used
- **Copyleft obligations** -- LGPL dependencies linked statically (must be
  dynamic), GPL dependencies in non-GPL projects, AGPL dependencies in
  network services without source disclosure
- **Transitive risk** -- A permissively licensed library that itself depends
  on a copyleft library. The copyleft obligation propagates
- **Deprecated or unmaintained libraries** -- Dependencies with known
  end-of-life status, no updates in 2+ years, or archived repositories
- **Duplicate functionality** -- Multiple libraries solving the same problem
  (e.g., both Guava and Apache Commons for the same utilities), increasing
  attack surface and license exposure unnecessarily

## Severity Levels

Assign one severity to each finding:

| Severity | Label | Meaning |
|----------|-------|---------|
| S1 | CRITICAL | Will cause data loss, security breach, or production failure. Fix immediately. |
| S2 | HIGH | Likely to cause bugs, performance degradation, or security weakness in production. Fix before merge. |
| S3 | MEDIUM | Code smell, maintainability issue, or minor bug risk. Should be addressed. |
| S4 | LOW | Style issue, naming suggestion, or minor improvement. Address at discretion. |

## Output Format

Structure the review as follows:

### Summary

Provide a 2-3 sentence overview: what the code does, overall quality
assessment, and the most important finding.

### Findings

List each finding with this structure:

**[S{n}] {Category}: {Brief title}**
- **Location**: File and line number (or method name if line unknown)
- **Issue**: What is wrong and why it matters
- **Suggestion**: Concrete fix, with a code snippet when helpful

Order findings by severity (S1 first), then by location within each severity.

### Positive Observations

Note 1-3 things the code does well. Good patterns, clean design, or thorough
error handling deserve acknowledgment.

### Summary Table

End with a count table:

| Severity | Count |
|----------|-------|
| S1 CRITICAL | n |
| S2 HIGH | n |
| S3 MEDIUM | n |
| S4 LOW | n |

## Guidelines

- Be specific. Reference exact line numbers, method names, and variable names.
- Provide concrete fix suggestions, not vague advice.
- When suggesting a fix, show a brief code snippet demonstrating the
  improvement.
- Do not flag style preferences that have no correctness or readability
  impact (e.g., brace placement style) unless the code mixes styles
  inconsistently.
- For diffs, focus review on changed lines. Only flag pre-existing issues
  if they interact with the changes.
- If the code is too large for a single review, divide it into logical
  sections and review each, providing a consolidated summary.
- When uncertain about intent, state the assumption explicitly rather than
  making a silent judgment.
