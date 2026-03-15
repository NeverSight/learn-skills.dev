---
name: xcode-build-resolver
description: Xcode build and Swift compilation error resolution guide. Covers common compilation errors, linking issues, signing problems, and dependency resolution with minimal-diff fix strategies.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# Xcode Build Error Resolver

Expert build error resolution focused on fixing Swift compilation, Xcode build, and iOS project errors quickly and efficiently. The goal is to get builds passing with minimal changes -- no architectural modifications.

## When to Apply

**USE when:**
- `xcodebuild` fails with compilation errors
- Swift type errors, inference failures, or generic constraint issues
- Import/module resolution errors (`No such module`)
- Code signing or provisioning profile errors
- Linker errors (missing frameworks, duplicate symbols)
- SPM/CocoaPods dependency resolution failures
- Architecture mismatch errors (simulator vs device)
- CI/CD build pipeline failures (Xcode Cloud, GitHub Actions, Fastlane)

**DO NOT USE when:**
- Code needs refactoring (use swift-refactor-cleaner)
- Architectural changes needed (use ios-architect)
- New features required (use ios-planner)
- Tests failing with logic errors (use swift-tdd-guide)
- Security issues found (use ios-security-reviewer)

## Quick Reference: Diagnostic Strategy

**Quick First, Full Later** -- start with fast single-file diagnostics, escalate to full build only when needed.

### Step 1: Quick Diagnostics (single file, under 2 seconds)

```bash
# Single file type-check -- catches type errors, API typos, missing imports, syntax errors
swiftc -typecheck -sdk $(xcrun --show-sdk-path --sdk iphonesimulator) path/to/File.swift

# Multiple files
swiftc -typecheck -sdk $(xcrun --show-sdk-path --sdk iphonesimulator) path/to/*.swift
```

### Step 2: Full Build (only when quick diagnostics cannot resolve)

```bash
# Full project build
xcodebuild -scheme MyApp -configuration Debug build 2>&1

# For CocoaPods projects (requires -workspace)
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -configuration Debug build 2>&1
```

**Full Build catches what Quick cannot:** linker errors, code signing errors, resource/asset errors, cross-module dependency errors, macro expansion errors.

### Common Build Commands

```bash
# Build for simulator
xcodebuild -scheme MyApp -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 15' build

# Build for device
xcodebuild -scheme MyApp -sdk iphoneos -destination 'generic/platform=iOS' build

# Archive
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -archivePath MyApp.xcarchive archive

# Clean build folder
xcodebuild clean -scheme MyApp

# Clear derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# List available schemes
xcodebuild -list

# Show build settings
xcodebuild -scheme MyApp -showBuildSettings

# Check code signing identities
security find-identity -v -p codesigning

# SPM resolve / CocoaPods install
swift package resolve
pod install --repo-update
```

## Workflow: Error Resolution

### 1. Collect All Errors

```
a) Run build (Quick Diagnostics first, then Full Build if needed)
   - Capture ALL errors, not just the first one

b) Categorize errors:
   - Swift compilation errors (type, inference, generics)
   - Concurrency errors (Sendable, @MainActor, Swift 6)
   - Linker errors (missing framework, duplicate symbols)
   - Code signing errors (certificate, provisioning profile)
   - Dependency errors (SPM, CocoaPods)
   - Resource/asset errors

c) Prioritize by impact:
   - Build-blocking errors: fix first
   - Compilation errors: fix in dependency order
   - Warnings: fix if time permits
```

### 2. Fix Each Error

```
For each error:

1. Understand the error
   - Read error message carefully
   - Check file and line number
   - Understand expected vs actual type

2. Find minimal fix
   - Add missing type annotation
   - Fix import statement
   - Add nil check (guard/if let)
   - Use type casting (as last resort)

3. Verify fix does not break other code
   - Rebuild after each fix
   - Check related files
   - Ensure no new errors introduced

4. Iterate until build passes
   - Fix one error at a time
   - Track progress (X/Y errors fixed)
```

### 3. Verify

```
1. Quick Diagnostics pass on changed files
2. Full Build exits with code 0
3. No new errors or warnings introduced
4. Minimal lines changed (under 5% of affected file)
```

## Key Patterns

### Type Inference Failure

```swift
// ERROR: Cannot convert value of type 'Int' to expected argument type 'String'
func display(text: String) { print(text) }
display(text: 42)

// FIX: Convert type explicitly
display(text: String(42))
```

### Optional Unwrapping

```swift
// ERROR: Value of optional type 'String?' must be unwrapped
let name: String? = user.name
let uppercased = name.uppercased() // ERROR

// FIX 1: Optional chaining
let uppercased = name?.uppercased()

// FIX 2: Guard statement
guard let name = name else { return }
let uppercased = name.uppercased()

// FIX 3: Nil coalescing
let uppercased = (name ?? "").uppercased()
```

### Missing Protocol Conformance

```swift
// ERROR: Type 'User' does not conform to protocol 'Codable'
struct User: Codable {
    let id: UUID
    let name: String
    let avatar: UIImage // UIImage is not Codable
}

// FIX: Exclude non-Codable property via CodingKeys
struct User: Codable {
    let id: UUID
    let name: String
    var avatar: UIImage?

    enum CodingKeys: String, CodingKey {
        case id, name // avatar excluded
    }
}
```

### SwiftUI Property Wrapper Errors

```swift
// ERROR: Cannot use mutating member on immutable value: 'self' is immutable
struct ContentView: View {
    var count = 0
    var body: some View {
        Button("Tap") { count += 1 } // ERROR
    }
}

// FIX: Use @State
struct ContentView: View {
    @State private var count = 0
    var body: some View {
        Button("Tap") { count += 1 }
    }
}
```

## Minimal Diff Strategy

**CRITICAL: Make the smallest possible change to fix each error.**

### DO

- Add type annotations where missing
- Add nil checks where needed (guard/if let)
- Fix import statements
- Add missing dependencies
- Update availability checks
- Fix configuration files
- Add protocol conformance

### DO NOT

- Refactor unrelated code
- Change architecture
- Rename variables/functions (unless causing the error)
- Add new features
- Change logic flow (unless fixing the error)
- Optimize performance
- Improve code style

**Example:**

```swift
// File has 200 lines, error on line 45

// WRONG: Refactor entire file, rename variables, extract functions -> 50 lines changed
// CORRECT: Add type annotation on line 45 -> 1 line changed

// Before (line 45) -- ERROR: Cannot infer type
let data = fetchData()

// MINIMAL FIX:
let data: [User] = fetchData()
```

## Build Error Priority Levels

### CRITICAL (Fix Immediately)
- Build completely broken, cannot run on simulator/device
- Archive/distribution blocked
- Multiple files failing

### HIGH (Fix Soon)
- Single file failing
- Type errors in new code
- Import errors, non-critical linking issues

### MEDIUM (Fix When Possible)
- SwiftLint warnings
- Deprecated API usage
- iOS version availability warnings
- Minor configuration warnings

## References

- [Compilation Errors](references/compilation-errors.md) - Type inference, optionals, protocol conformance, imports, generics, SwiftUI property wrappers
- [Concurrency Errors](references/concurrency-errors.md) - @MainActor, Sendable, Swift 6, SwiftData, Observable, Privacy Manifest, macros
- [Signing & Linking Errors](references/signing-errors.md) - Code signing, linker errors, architecture, SPM/CocoaPods, CI/CD builds

## Common Mistakes (Build Anti-Patterns)

### 1. Fixing Errors Without Reading the Full Message

Always read the complete error message including the expected type, actual type, and suggestion. The compiler often tells you exactly what to do.

### 2. Cleaning Build Folder as First Resort

`rm -rf DerivedData` is slow and usually unnecessary. Use Quick Diagnostics first. Only clean when you suspect stale caches (after Xcode updates, branch switches, or dependency changes).

### 3. Force Unwrapping to Silence Errors

```swift
// BAD: Crashes at runtime
let url = URL(string: userInput)!

// GOOD: Handle nil properly
guard let url = URL(string: userInput) else { return }
```

### 4. Suppressing Concurrency Warnings Globally

```swift
// BAD: Hides real data race issues
// Build Settings: SWIFT_STRICT_CONCURRENCY = minimal

// GOOD: Fix individual issues with proper isolation
@MainActor class ViewModel { /* ... */ }
```

### 5. Changing Architecture to Fix a Type Error

If a type mismatch error leads you to redesign a module, you are overreacting. Add a type annotation, a conversion, or a protocol conformance -- not a new abstraction layer.

## Build Error Report Format

```markdown
# Build Error Resolution Report

**Build Target:** Debug / Release / Archive
**Scheme:** MyApp
**Initial Errors:** X
**Errors Fixed:** Y
**Build Status:** PASSING / FAILING

## Errors Fixed

### 1. [Error Category]
**Location:** `Sources/Features/Home/HomeView.swift:45`
**Error:** Value of optional type 'String?' must be unwrapped
**Root Cause:** Missing optional unwrapping
**Fix:**
- let title = user.name
+ let title = user.name ?? "Unknown"
**Lines Changed:** 1

## Verification
1. Debug build passes
2. No new errors introduced
3. Simulator run works
```

**Remember**: The goal is to fix errors quickly with minimal changes. Do not refactor, do not optimize, do not redesign. Fix the error, verify the build passes, move on. Speed and precision over perfection.
