---
name: comprehensive-code-review
description: "Code review for ACE Engine (OpenHarmony ArkUI) covering C++/JS/TS/ArkTS. Analyzes 19+ dimensions: stability, performance, threading, security, memory, Modern C++ practices, SOLID principles, design patterns, robustness, testability, maintainability, observability, API design, technical debt, backward compatibility. Reports severity levels, refactoring suggestions, and ACE Engine checks (Pattern/Model/Property, component lifecycle, RefPtr/WeakPtr, four-layer architecture). Use when: reviewing PRs, analyzing code quality, enforcing standards, identifying technical debt, validating architecture, generating quality reports."
---

# Comprehensive Code Review for ACE Engine

## Quick Start

Perform comprehensive code review analysis directly with AI:

```
"Review the code in frameworks/core/components_ng for memory management issues"

"Analyze this pull request focusing on security vulnerabilities"

"Check path/to/code.cpp for ACE Engine architecture compliance"
```

## Review Workflow

### Phase 1: Code Analysis

AI will analyze code across all relevant dimensions based on:

1. **Reading the code files** - Understanding implementation details
2. **Applying reference standards** - Using criteria from references/ directory
3. **Checking against ACE Engine patterns** - Validating project-specific conventions

### Phase 2: Dimension-Based Review

Review code across 19+ dimensions. See [DIMENSIONS.md](references/DIMENSIONS.md) for complete coverage.

**High-Priority Dimensions:**
- Security (CRITICAL) - Input validation, command injection, buffer overflows
- Memory (CRITICAL) - Smart pointers, leaks, ownership semantics
- Threading (HIGH) - Data races, deadlocks, callback safety
- Stability (HIGH) - Error handling, boundary conditions

**Medium-Priority Dimensions:**
- Performance - Algorithm complexity, optimization opportunities
- SOLID Principles - Single responsibility, Open/Closed, etc.
- Code Smells - Long methods, large classes, duplicate code
- Testability - Dependency injection, decoupling

### Phase 3: Report Generation

AI generates comprehensive review report including:
- **Executive Summary** - Issue counts by severity
- **Critical Issues** (🔴) - Must fix before merge
- **High Priority Issues** (🟠) - Should fix before merge
- **Medium Priority Issues** (🟡) - Fix soon
- **Low Priority Issues** (🟢) - Nice to have
- **Dimension Breakdown** - Issues grouped by category
- **File-by-File Details** - Specific line numbers and code snippets
- **Recommendations** - Prioritized action items with before/after examples
- **Review Checklist** - Pre-merge verification

## Dimension Reference

Quick reference to all dimensions:

| Dimension | Focus | Severity Levels | Reference |
|-----------|-------|-----------------|-----------|
| **Stability** | Error handling, boundaries | 🔴🟠🟡🟢 | [STABILITY.md](references/STABILITY.md) |
| **Performance** | Algorithms, optimization | 🔴🟠🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Threading** | Concurrency, synchronization | 🔴🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Security** | Input validation, vulnerabilities | 🔴🟠🟡 | [SECURITY.md](references/SECURITY.md) |
| **Memory** | Smart pointers, leaks | 🔴🟠🟡 | [MEMORY.md](references/MEMORY.md) |
| **Modern C++** | C++11/14/17/20 features | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Effective C++** | RAII, Rule of Five | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Code Smells** | 22 types of smells | 🟠🟡 | [CODE_SMELLS.md](references/CODE_SMELLS.md) |
| **SOLID** | Design principles | 🟠🟡 | [SOLID.md](references/SOLID.md) |
| **Design Patterns** | Pattern usage | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Robustness** | Fault tolerance | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Testability** | Dependency injection | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Maintainability** | Code complexity | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Observability** | Logging, monitoring | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **API Design** | Interface quality | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Technical Debt** | TODO/FIXME tracking | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Backward Compatibility** | API stability | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Architecture** | ACE Engine compliance | 🔴🟠🟡 | [ACE_ENGINE_SPECIFIC.md](references/ACE_ENGINE_SPECIFIC.md) |

## ACE Engine Specific Checks

### Architecture Validation

**Four-Layer Architecture:**
```
Frontend Bridge Layer
    ↓
Component Framework Layer (Pattern/Model/Property)
    ↓
Layout/Render Layer
    ↓
Platform Adapter Layer (OHOS/Preview)
```

**Check:**
- No violations of layer boundaries
- Proper use of Pattern/Model/Property separation
- No direct platform calls from framework layer

### Component Structure

```
components_ng/pattern/<component>/
├── *_pattern.h/cpp         # Business logic & lifecycle
├── *_model.h/cpp           # Data model interface
├── *_layout_property.h/cpp # Layout properties
├── *_paint_property.h/cpp  # Render properties
└── *_event_hub.h/cpp       # Event handling
```

### RefPtr Usage

```cpp
// ✅ Creation
auto node = AceType::MakeRefPtr<FrameNode>();

// ✅ Type-safe casting
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!pattern) {
    LOGE("Failed to get pattern");
    return false;
}

// ✅ Breaking cycles with WeakPtr
class Child {
    WeakPtr<Parent> parent_;  // Use weak, not strong
};

// ✅ Safe callbacks
auto weak = AceType::WeakClaim(this);
PostTask([weak]() {
    auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
    if (pattern) pattern->Update();
});
```

### Naming Conventions

```cpp
class MenuPattern {           // PascalCase
public:
    void OnModifyDone();      // PascalCase
    int GetWidth() const;     // Get prefix

private:
    int width_;               // snake_case_ with trailing underscore
    std::string component_id_;  // Abbreviations lowercase
};

constexpr int MAX_MENU_ITEMS = 100;  // UPPER_CASE
```

## Severity Levels

**🔴 CRITICAL** - Must fix before merge
- Security vulnerabilities (command injection, buffer overflow)
- Memory leaks in long-running processes
- Use-after-free, double-free
- Data races
- Crashes / undefined behavior
- Architecture violations

**🟠 HIGH** - Should fix before merge
- Performance degradation
- API violations
- SOLID principle violations
- Major code smells (Large Class, Shotgun Surgery)
- Improper RefPtr usage
- Unsafe callback captures

**🟡 MEDIUM** - Fix soon
- Minor performance issues
- Code smells (Long Method, Duplicate Code)
- Style violations
- Missing error handling in non-critical paths

**🟢 LOW** - Nice to have
- Missing comments
- Minor style issues
- Optimization opportunities
- Code documentation improvements

## Common Issue Patterns

| Pattern | Dimension | Severity | Detection |
|---------|-----------|----------|-----------|
| Raw pointer instead of RefPtr | Memory | HIGH | `new T()` without RefPtr |
| Command injection | Security | CRITICAL | `system(user_input)` |
| Buffer overflow | Security | CRITICAL | `strcpy()`, `sprintf()` |
| Unsafe this capture | Threading | HIGH | `[this]` in PostTask |
| Long method (>50 lines) | Code Smell | MEDIUM | Function length |
| Large class (>500 lines) | Code Smell | HIGH | Class size |
| Missing null check | Stability | HIGH | Pointer use without validation |
| static_cast instead of DynamicCast | Memory | MEDIUM | `static_cast<T*>` |

## Usage Examples

### Review a Pull Request

```
"Review the changes in this PR with focus on memory management and threading safety"
```

AI will:
- Analyze all changed files
- Check memory management (RefPtr, WeakPtr, raw pointers)
- Verify threading safety (callback captures, PostTask usage)
- Report issues with line numbers and severity

### Security Audit

```
"Perform a security audit of path/to/code, focusing on input validation and potential vulnerabilities"
```

AI will check for:
- Command injection risks (system() calls)
- Buffer overflow vulnerabilities (strcpy, sprintf)
- Unvalidated user input
- Unsafe type casts

### Memory Leak Detection

```
"Analyze frameworks/core/components for potential memory leaks and improper RefPtr usage"
```

AI will identify:
- Raw new/delete without smart pointers
- Circular references without WeakPtr
- Missing null checks after DynamicCast
- Improper ownership semantics

### Architecture Compliance Check

```
"Verify that components_ng/menu follows the four-layer architecture and Pattern/Model/Property separation"
```

AI will validate:
- Four-layer architecture compliance
- Pattern/Model/Property separation
- No layer boundary violations
- Component lifecycle methods (OnModifyDone, etc.)

## Integration Examples

### Pre-commit Hook

For pre-commit hooks, consider using traditional static analysis tools:

```bash
#!/bin/bash
# .git/hooks/pre-commit

CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|cc|cxx|h|hpp|ts|tsx)$')

if [ -n "$CHANGED_FILES" ]; then
    echo "Running basic static analysis..."
    # Use clang-tidy, cppcheck, eslint, etc.
    for file in $CHANGED_FILES; do
        if [[ $file == *.cpp || $file == *.h ]]; then
            clang-tidy $file --checks='*' || true
        elif [[ $file == *.ts ]]; then
            eslint $file || true
        fi
    done
fi
```

### Manual Review Workflow

For comprehensive AI-powered review:
1. Identify code to review (PR, specific files, directory)
2. Request review with specific focus areas
3. AI analyzes code using reference standards
4. Review results with severity-tagged issues
5. Address critical and high-priority issues
6. Re-request review for verification

## References

Detailed documentation for all dimensions in `references/`:
- [DIMENSIONS.md](references/DIMENSIONS.md) - Quick reference for all 19+ dimensions
- [STABILITY.md](references/STABILITY.md) - Error handling, boundary conditions
- [MEMORY.md](references/MEMORY.md) - Smart pointers, leaks, ownership
- [SECURITY.md](references/SECURITY.md) - Input validation, vulnerabilities
- [CODE_SMELLS.md](references/CODE_SMELLS.md) - 22 types of code smells
- [SOLID.md](references/SOLID.md) - Five design principles
- [ACE_ENGINE_SPECIFIC.md](references/ACE_ENGINE_SPECIFIC.md) - Project-specific rules

## Assets

- [report_template.md](assets/report_template.md) - Customizable report template for AI-generated reviews

## Review Checklist

Before merging code:

**Code Quality:**
- [ ] No CRITICAL issues
- [ ] HIGH priority issues addressed or documented
- [ ] No compiler warnings
- [ ] Static analysis clean

**Architecture:**
- [ ] Four-layer architecture respected
- [ ] Proper Pattern/Model/Property separation
- [ ] No layer boundary violations

**Memory:**
- [ ] No memory leaks
- [ ] RefPtr used correctly
- [ ] WeakPtr used to break cycles
- [ ] Callbacks use WeakClaim

**Security:**
- [ ] All input validated
- [ ] No command injection
- [ ] No buffer overflows
- [ ] Sensitive data protected

**Testing:**
- [ ] Unit tests added
- [ ] Edge cases covered
- [ ] Error scenarios tested
