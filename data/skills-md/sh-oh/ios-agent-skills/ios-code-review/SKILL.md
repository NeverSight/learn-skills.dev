---
name: ios-code-review
description: Swift/iOS code review guide for quality, security, memory management, concurrency safety, and Swift best practices. Includes comprehensive checklists and review workflows.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# iOS Code Review

Comprehensive security and quality review guide for Swift/iOS code changes. Covers memory leaks, concurrency issues, iOS security vulnerabilities, and Swift best practices.

## When to Apply

- Reviewing pull requests or code changes in Swift/iOS projects
- Running pre-merge quality gates on Swift codebases
- Performing security audits on iOS applications
- Validating concurrency safety for Swift 6 migration
- Checking memory management in ViewModels, closures, and Combine pipelines
- Ensuring compliance with App Store review guidelines

## Quick Reference

### Review Checklist Summary

| Area | Priority | Key Checks |
|------|----------|------------|
| Security | CRITICAL | No hardcoded secrets, Keychain for sensitive data, ATS compliance |
| Memory Management | CRITICAL | No retain cycles, weak delegates, cancellable cleanup |
| Code Quality | HIGH | No force unwraps, proper error handling, size limits |
| Concurrency | HIGH | @MainActor for UI, Sendable compliance, Task cancellation |
| Best Practices | MEDIUM | Swift API Guidelines, accessibility, localization |

### Approval Criteria

| Verdict | Condition | Action |
|---------|-----------|--------|
| **Approve** | No CRITICAL or HIGH issues | Safe to merge |
| **Warning** | Only MEDIUM issues present | Can merge with caution |
| **Block** | CRITICAL or HIGH issues found | Must fix before merge |

## Workflow

### How to Conduct a Review

1. **Get changed files**

```bash
# See all changed files
git diff --name-only HEAD

# See full diff for review
git diff HEAD
```

2. **Focus on Swift files** -- Filter to `.swift` files and prioritize by change size.

3. **Categorize each finding** by severity:
   - CRITICAL: Security vulnerabilities, memory leaks, data races
   - HIGH: Force unwraps, missing error handling, concurrency violations
   - MEDIUM: Style issues, missing accessibility, optimization opportunities

4. **Generate report** using the output format below.

5. **Determine verdict** based on approval criteria.

## Key Review Areas

### Security (CRITICAL)

> Full checklist: `references/security-checks.md`

- [ ] No sensitive data stored in UserDefaults (use Keychain instead)
- [ ] No hardcoded API keys, secrets, or credentials in source code
- [ ] App Transport Security (ATS) exceptions justified and documented
- [ ] Debug code guarded with `#if DEBUG` and excluded from release builds
- [ ] Privacy manifest (PrivacyInfo.xcprivacy) present and Required Reason APIs declared

### Memory Management (CRITICAL)

> Full checklist: `references/concurrency-checks.md`

- [ ] Closures use `[weak self]` to prevent retain cycles in escaping contexts
- [ ] Delegates declared as `weak` to avoid ownership cycles
- [ ] NotificationCenter observers removed on deinit
- [ ] Timers invalidated on deinit
- [ ] Combine `AnyCancellable` stored properly in `Set<AnyCancellable>`

### Code Quality (HIGH)

- [ ] No force unwrapping (`!`) without guard/if-let safety
- [ ] Functions stay under 40 lines; files under 500 lines
- [ ] Nesting depth does not exceed 4 levels
- [ ] Empty catch blocks are not used; errors are handled or propagated
- [ ] Access control applied (default to `private`; expose only what is needed)

### Concurrency (HIGH)

> Full checklist: `references/concurrency-checks.md`

- [ ] UI updates happen on `@MainActor` or main thread
- [ ] Non-Sendable types do not cross actor boundaries
- [ ] Tasks are cancelled when the owning scope is deallocated
- [ ] No blocking synchronous operations on the main thread
- [ ] Actor isolation is correct and `nonisolated` is not overused

### Best Practices (MEDIUM)

- [ ] Naming follows Swift API Design Guidelines (UpperCamelCase for types, lowerCamelCase for members)
- [ ] Boolean properties read as assertions (`isEmpty`, `isEnabled`, `hasCompleted`)
- [ ] Accessibility labels and hints provided for interactive elements
- [ ] User-facing strings are localized (no hardcoded display text)
- [ ] Public APIs have documentation comments

## Review Output Format

For each issue found, use this structure:

```
[SEVERITY] Brief Issue Title
File: path/to/file.swift:lineNumber
Issue: Description of the problem and its impact.
Fix: How to resolve it.

// Current (problematic)
<code showing the problem>

// Suggested (fixed)
<code showing the fix>
```

### Example: Critical Issue

```
[CRITICAL] Sensitive data in UserDefaults
File: Sources/Services/AuthService.swift:42
Issue: API token stored in UserDefaults, accessible without encryption.
Fix: Move to Keychain with appropriate protection class.

// Current
UserDefaults.standard.set(token, forKey: "authToken")

// Suggested
try KeychainService.shared.save(token, forKey: "authToken",
                                 accessibility: .whenUnlockedThisDeviceOnly)
```

### Example: High Issue

```
[HIGH] Retain cycle in closure
File: Sources/ViewModels/HomeViewModel.swift:78
Issue: Strong reference to self in async closure may cause memory leak.
Fix: Depends on actor isolation context.

// Case 1: @MainActor class - Task inherits actor context, weak self optional
@MainActor
final class HomeViewModel: ObservableObject {
    func load() {
        Task {
            items = await fetchItems()  // OK - inherits MainActor
        }
    }
}

// Case 2: Non-isolated class - weak self required
final class DataManager {
    func load() {
        Task { [weak self] in
            guard let self else { return }
            await self.process()
        }
    }
}

// Case 3: Escaping closures - always weak self
repository.fetch { [weak self] result in
    self?.handleResult(result)
}
```

## Summary Template

Use this template for the final review report:

```markdown
## Code Review Summary

### Files Reviewed
- `path/to/file.swift` (Modified)
- `path/to/other.swift` (Added)

### CRITICAL Issues (X)
| Issue | Location | Fix |
|-------|----------|-----|
| Brief description | file:line | How to fix |

### HIGH Issues (X)
| Issue | Location | Fix |
|-------|----------|-----|
| Brief description | file:line | How to fix |

### MEDIUM Suggestions (X)
| Issue | Location | Fix |
|-------|----------|-----|
| Brief description | file:line | How to fix |

### Good Practices Found
- [What was done well]

### Verdict: Approve / Warning / Block
```

## Quick Check Commands

Run these before committing to catch common issues early:

```bash
# Check for print statements in production code
grep -rn "print(" --include="*.swift" Sources/

# Check for force unwraps
grep -rn "!" --include="*.swift" Sources/ | grep -v "//"

# Check for TODO/FIXME without ticket references
grep -rn "TODO\|FIXME" --include="*.swift" Sources/

# Check for hardcoded secrets (basic scan)
grep -rn "api_key\|apiKey\|secret\|password" --include="*.swift" Sources/
```

## References

- `references/security-checks.md` -- Full security review checklist (data storage, network, authentication, App Store compliance)
- `references/concurrency-checks.md` -- Swift 6 concurrency, Combine memory, and performance checks
- `references/cascading-verification.md` -- Cascading verification scenarios, code quality, best practices, accessibility, and test quality

## Common Mistakes

### 1. Approving code with unguarded force unwraps

Force unwraps (`!`) crash at runtime when the value is nil. Always require guard/if-let unless the value is provably non-nil (e.g., `IBOutlet` after `viewDidLoad`).

### 2. Missing retain cycle detection in nested closures

A closure inside another closure can capture `self` strongly even if the outer closure uses `[weak self]`. Check the full closure chain, especially in Combine `sink` and `map` pipelines.

### 3. Overlooking @MainActor requirements for UI updates

ViewModels that update `@Published` properties driving SwiftUI views must be annotated with `@MainActor` or explicitly dispatch to the main actor. Missing this causes runtime warnings or undefined UI behavior.

### 4. Ignoring Sendable compliance warnings

Swift 6 strict concurrency requires types crossing actor boundaries to conform to `Sendable`. Treating these warnings as noise leads to data races in production. Review each warning and either conform or restructure.

### 5. Not verifying cascading impacts of API changes

Changing an enum case, protocol requirement, or function signature can break callers throughout the codebase. Always search for all usage sites before approving such changes. See `references/cascading-verification.md`.
