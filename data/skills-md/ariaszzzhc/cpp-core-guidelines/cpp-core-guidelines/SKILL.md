---
name: cpp-core-guidelines
description: C++ Core Guidelines by Stroustrup and Sutter for writing modern, safe, and efficient C++ code. Use when writing, reviewing, or refactoring C++ code to ensure type safety, resource safety, and performance. Triggers on C++ code tasks including interface design, resource management (memory, handles, locks), class design, error handling, concurrency, templates, and general code review. Use for questions like "review this C++ code", "how should I manage resources in C++", "best practices for C++ interfaces", or when writing any C++ code that should follow modern standards (C++11/14/17/20).
---

# C++ Core Guidelines

## Overview

These guidelines help write C++ code that is:
- **Type-safe**: No implicit violations of the type system
- **Resource-safe**: No leaks (memory, handles, locks, etc.)
- **Performant**: Efficient without sacrificing correctness
- **Correct**: Catches more logic errors at compile time

## Load Reference by Scenario

Choose the reference file based on what you're doing:

| Scenario | Reference File | Rules |
|----------|----------------|-------|
| Checking memory leaks, RAII, pointers | [memory-safety.md](references/memory-safety.md) | R.*, ES.*, Con.* |
| Designing function signatures, APIs | [api-design.md](references/api-design.md) | I.*, F.* |
| Designing or reviewing classes | [class-design.md](references/class-design.md) | C.* |
| Thread safety, data races, locks | [concurrency.md](references/concurrency.md) | CP.* |
| Exceptions, error codes, error handling | [error-handling.md](references/error-handling.md) | E.* |
| Templates, STL, generic code | [templates.md](references/templates.md) | T.*, SL.*, Enum.* |
| Coding style, naming, philosophy | [modern-style.md](references/modern-style.md) | P.*, NL.*, SF.* |
| Performance optimization, C compatibility | [performance.md](references/performance.md) | Per.*, CPL.*, A.* |

## Quick Reference

### Memory Safety
```cpp
// Bad: manual management
X* p = new X;
delete p;

// Good: RAII
auto p = make_unique<X>();
```

### API Design
```cpp
// Bad: unclear ownership
void process(int* data, int n);

// Good: explicit ownership and size
void process(span<const int> data);
```

### Class Design
```cpp
// Rule of zero - let compiler generate
class Widget {
    unique_ptr<Impl> pImpl;  // No explicit dtor/copy/move needed
};
```

### Concurrency
```cpp
// Bad: manual lock
mutex mtx;
mtx.lock();
// ...
mtx.unlock();

// Good: RAII lock
lock_guard<mutex> lock(mtx);
```

## Code Review Checklist

When reviewing C++ code, load the appropriate reference and check:

**Memory Safety** → [memory-safety.md](references/memory-safety.md)
- [ ] No raw `new`/`delete`
- [ ] RAII for all resources
- [ ] No dangling pointers
- [ ] Proper const usage

**API Design** → [api-design.md](references/api-design.md)
- [ ] Interfaces are explicit
- [ ] Parameters express ownership
- [ ] Return values over output params

**Class Design** → [class-design.md](references/class-design.md)
- [ ] Class has clear invariant
- [ ] Rule of zero/five followed
- [ ] Virtual destructor for base classes

**Thread Safety** → [concurrency.md](references/concurrency.md)
- [ ] No data races
- [ ] lock_guard/scoped_lock used
- [ ] No deadlocks
