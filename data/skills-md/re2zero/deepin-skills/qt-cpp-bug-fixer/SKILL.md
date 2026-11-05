---
name: qt-cpp-bug-fixer
description: Use when encountering compilation errors, runtime crashes, memory leaks, UI issues, or threading problems in Qt C++ projects. Also use when MOC errors, undefined vtable references, missing Q_OBJECT macros, or signal-slot connection failures occur.
---

# Qt C++ Bug Fixer

## Overview

Diagnose and fix Qt C++ bugs with minimal, Qt-style changes. **Iron Rule: Fix ONLY the reported issue.** No extra refactoring, no "while I'm here" improvements.

## When to Use

**Compilation Errors:** `undefined reference to 'vtable'`, missing `Q_OBJECT`, MOC errors, circular includes, CMakeLists.txt/.pro issues

**Runtime Crashes:** Segmentation faults, null pointer dereferences, pure virtual calls

**Memory Issues:** `new` without `delete`, incorrect parent-child relationships, leaks

**UI Problems:** Widgets not displaying, layout failures, signal-slot not working, unresponsive controls

**Threading:** Cross-thread UI crashes, thread affinity, blocking UI thread

**Do NOT use when:** Intentionally refactoring, adding features (use TDD), or performance optimization

## Core Pattern

```cpp
// ❌ WRONG: Refactoring while fixing
void MyWidget::processData()
{
    if (m_processor) {
        auto dataProcessor = m_processor;  // UNNECESSARY rename
        QList<int> items = dataProcessor->getItems();  // UNNECESSARY STL→Qt
        qDebug() << "Processing" << items.size();  // UNNECESSARY logging
    }
}

// ✅ CORRECT: Only the fix
void MyWidget::processData()
{
    if (m_processor) {  // Fix: Added null check
        m_processor->process();
    }
}
```

```cpp
// ❌ WRONG: External smart pointers
#include <memory>
std::unique_ptr<DataProcessor> m_processor;

// ✅ CORRECT: Qt parent-child ownership
DataProcessor *m_processor = new DataProcessor(this);  // Parent handles deletion
```

## Quick Reference

| Bug Type | Root Cause | Minimal Fix |
|----------|------------|-------------|
| `undefined reference to 'vtable'` | Missing `Q_OBJECT` macro | Uncomment/add `Q_OBJECT` in header |
| `moc` file not generated | Header not in CMakeLists.txt/.pro | Add header to build files |
| Segfault on nullptr | No null check before dereferencing | Add `if (ptr)` before use |
| Memory leak | `new` without parent ownership | Add parent to `new` or use `deleteLater()` |
| Signal not firing | Connection broken or wrong signature | Check `connect()` syntax and lifetime |
| Cross-thread UI crash | Direct UI manipulation from worker | Use `QMetaObject::invokeMethod` or signal-slot |

## Implementation

### 1. Diagnostic Phase

**Read error carefully:** Compiler error → find line number; Runtime crash → read backtrace; UI issue → note specific behavior

**Locate problematic code:** Use `@file:line` notation, read context (class definition, includes, parent), check related files

**Check Qt context:** Does class inherit `QObject`? Is `Q_OBJECT` present? Are parent-child relationships correct? Are signals/slots connected?

### 2. Hypothesis and Verification

**Generate 1-2 root causes:** Focus on error type (MOC/config, memory/null, signals/layout, thread affinity)

**Verify hypothesis:** Check code - don't assume. MOC errors always involve `Q_OBJECT` and meta-object system

### 3. Generate Minimal Fix

**Fix ONLY the identified issue:** ONE problem = ONE fix. No variable renames, no style cleanup, no optimizations

**Explain WHY:** Root cause, not symptom. Qt-specific mechanics (MOC, parent-child, signal-slot)

**Explain HOW:** Principle behind change. Why it solves root cause

**Regression testing:** Compile (`cmake --build .` or `make`), suggest specific verification steps, run tests if applicable

### 4. Configuration File Fixes

**CMakeLists.txt:**
```cmake
qt_add_executable(MyApp
    main.cpp
    mywidget.h  # MUST include header with Q_OBJECT
    mywidget.cpp
)
```

**.pro file:**
```qmake
HEADERS += mywidget.h  # Headers with Q_OBJECT must be listed
SOURCES += mywidget.cpp
```

## Common Mistakes

| Mistake | Why Wrong | Correct |
|---------|-----------|---------|
| Renaming variables while fixing | Violates minimal change principle | Keep existing names |
| "Upgrading" SIGNAL/SLOT to lambda | Unnecessary change, breaks code | Fix only broken connection |
| Converting STL to Qt containers | Unrelated to bug | Fix only what causes crash |
| Adding logging "for debugging" | Extra code not needed | Fix root cause directly |
| Adding null checks everywhere | Masks real problem | Add only where crash occurs |
| Refactoring while fixing | Scope creep, introduces bugs | ONE fix per bug report |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "This variable name is confusing, I'll rename it" | Variable names don't cause crashes. Fix the crash. |
| "While I'm here, let me upgrade to modern Qt syntax" | Technical debt is not a bug. Fix the bug. |
| "This cleanup makes the code clearer" | Clarity improvements are refactoring, not bug fixing. |
| "The old SIGNAL/SLOT macros are deprecated" | Deprecated ≠ broken. Fix only what's broken. |
| "I'm adding a safeguard, it's defensive programming" | Safeguards without justification are extra code. Fix root cause. |
| "This refactoring is minimal and obvious" | Any change beyond the fix is NOT minimal. |
| "I'll improve the design while fixing it" | Design improvements are separate tasks. Fix the bug. |
| "It's about quality, not just functionality" | Quality bug fixes focus on minimal, surgical changes. |

## Red Flags - STOP and Start Over

**STOP immediately** if you think or say ANY of these:

- "While I'm fixing this, I'll also..."
- "This is a good opportunity to clean up..."
- "The old style should be modernized..."
- "I'll add a safeguard/precaution..."
- "This variable name is confusing, better rename it..."
- "Let me upgrade to the latest Qt API..."
- "This design could be improved..."
- "I'll make it more robust/defensive..."
- "This code is messy, let me organize it..."

**ALL mean:** You're doing MORE than fixing the bug. Stop. Delete extra changes. Fix ONLY the reported issue.

## Qt-Specific Anti-Patterns

**Avoid External Smart Pointers:**
```cpp
// ❌ std::unique_ptr
std::unique_ptr<QWidget> m_widget;
// ✅ Qt parent-child
QWidget *m_widget = new QWidget(this);
```

**Thread-Aware Connections:**
```cpp
// ❌ Wrong affinity assumption
workerThread->start();
worker->doWork();  // Might crash
// ✅ Qt 5 explicit type
connect(worker, &Worker::finished, this, [this]() {}, Qt::QueuedConnection);
```

**Qt Blocking Helpers:**
```cpp
// ❌ Manual locks
QMutexLocker locker(&m_mutex);
// ✅ Qt's QSignalBlocker
QSignalBlocker blocker(this);  // Auto-unblocks on scope exit
```

**Memory Management:**
```cpp
// ❌ Manual delete
MyWidget *w = new MyWidget();
delete w;
// ✅ Parent-child system
MyWidget *w = new MyWidget(this);  // Parent deletes on destruction
```

## Backward Compatibility

**CRITICAL:** Verify fix doesn't break existing connections:
1. Check all `connect()` calls to/from modified object
2. Verify object lifetime doesn't break parents/children
3. Don't change signal/slot signatures unless that's the bug
4. Don't remove connections unless causing the issue

## The Iron Law

**Fixing bugs is NOT an excuse for refactoring.**

Every change beyond the minimal fix introduces new risk, wastes user's time, violates the contract of "bug fix."

**When in doubt:** Ask yourself "Would this change be justified if I only said I was fixing the bug, not 'cleaning up'?"

If NO → Delete the change. Fix ONLY the bug.

**No exceptions:**
- Not for "obvious" improvements
- Not for "technical debt" reduction
- Not for "best practices" alignment
- Not for "making it clearer"
- Not for "while I'm here"
- Minimal fix means MINIMAL
