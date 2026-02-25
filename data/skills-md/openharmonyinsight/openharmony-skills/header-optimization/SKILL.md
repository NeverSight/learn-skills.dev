---
name: header-optimization
description: This skill should be used when the user asks to "optimize header files", "reduce header dependencies", "优化头文件", "减少头文件依赖", "analyze compilation efficiency", "分析编译效率", or mentions test_header.cpp analysis. This skill optimizes C++ header file compilation efficiency through systematic refactoring.
version: 1.0.0
---

# Header File Optimization for ACE Engine

Optimize C++ header file compilation efficiency in ace_engine through systematic dependency reduction and implementation restructuring. This skill focuses on reducing compilation time and memory footprint by minimizing header dependencies and moving implementations out of headers.

## When to Use This Skill

Invoke this skill when:
- Optimizing specific header files for compilation efficiency
- Working with test_header.cpp to analyze header dependencies
- Reducing header file dependencies in ace_engine
- Analyzing compilation performance of specific headers
- User specifies "只分析不进行修改" (analysis only, no modifications)

## Key Rules

Follow these critical constraints during optimization:

1. **Preserve business logic** - Only modify structure, not functionality
2. **Minimize file creation** - Edit current header/cpp directly, only create new files for header splitting scenarios
3. **Limit scope** - Only perform work defined in key steps, do not expand modification scope
4. **Standalone compilation** - Use compile-analysis skill for individual file compilation verification, never full build
5. **test_header.cpp is read-only** - Never modify test_header.cpp; it only serves for dependency statistics

## Optimization Workflow

### Step 1: Analyze Input and Mode

Determine the optimization target and mode:
- If input is a header file (`.h`): Optimize that header directly
- If input is `test_header.cpp`: Extract the header file from its content and optimize that header
- Check if user specified "只分析不进行修改" (analysis only mode)

In analysis-only mode:
- Perform all analysis steps
- Generate optimization recommendations
- Do NOT modify any files
- Present findings and suggested changes for user approval

### Step 2: Move Inline Implementations to CPP

**Objective**: Move all method implementations longer than 3 lines from header to cpp file.

**Procedure**:
1. Read the target header file
2. Identify all methods (including static methods) with implementations exceeding 3 lines
3. If corresponding cpp file does not exist, create it
4. Move method implementations to cpp file
5. Keep only declarations in header file
6. For template methods, see Step 6

**What counts as 3 lines**:
```cpp
// Less than 3 lines - Keep in header
int GetValue() const { return value_; }

// 3 lines or more - Move to cpp
void ProcessData() {
    auto result = Calculate();
    Validate(result);
    cache_.Store(result);
}
```

**Exception**: Simple getters/setters that are one-liners typically remain in headers for performance.

### Step 3: Remove Unnecessary Header Includes

**Objective**: Eliminate unused header dependencies.

**Procedure**:
1. List all `#include` directives in the header file
2. For each included header, verify if it's actually used:
   - Search for types from that header in the file
   - Check if member variables, function parameters, or return types use those types
   - Verify base class inheritance
3. Remove includes that have no actual usage
4. Document removal reasons in analysis report

**Example**:
```cpp
// Before
#include "base/memory/ace_type.h"
#include "core/components/common/layout.h"
#include "core/pipeline/base/element.h"  // Not used - REMOVE

// After
#include "base/memory/ace_type.h"
#include "core/components/common/layout.h"
```

### Step 4: Convert Includes to Forward Declarations

**Objective**: Replace full header includes with forward declarations wherever possible.

**Procedure**:
1. For each remaining header include, analyze what's needed from it:
   - Type names only (pointers, references, function parameters)
   - Type definitions (complete class definition needed)
   - Static constants or enums
2. Convert to forward declaration when only type name is needed:
   ```cpp
   // Before
   #include "core/components_ng/base/frame_node.h"

   // After
   namespace OHOS::Ace::NG {
   class FrameNode;
   }  // namespace OHOS::Ace::NG
   ```
3. Keep full include only when:
   - Inheriting from the class
   - Class has member variables of that type
   - Template instantiation requires complete definition
   - Accessing static constants or inline methods

**Forward Declaration Template**:
```cpp
namespace OHOS::Ace {
namespace NG {
class FrameNode;
class UINode;
}  // namespace NG
}  // namespace OHOS
```

### Step 4.1: Advanced Forward Declaration Scenarios

**IMPORTANT**: This section contains advanced forward declaration patterns based on real optimization cases in ace_engine.

#### Scenario 1: Smart Pointer Template Parameters (RefPtr/WeakPtr)

**When to use forward declaration**:
- Type is only used as template parameter for `RefPtr<T>` or `WeakPtr<T>`
- Type is used as member variable with smart pointer
- Type is used as function parameter/return value with smart pointer

**Rule**: Smart pointer templates (RefPtr, WeakPtr, std::unique_ptr, std::shared_ptr) do NOT require complete type definition in header files.

**Example - Before Optimization**:
```cpp
// click_event.h (BEFORE)
#include "core/components_ng/gestures/recognizers/click_recognizer.h"  // ❌ Full include

class ClickEventActuator {
private:
    RefPtr<ClickRecognizer> clickRecognizer_;  // Only needs forward declaration

    const RefPtr<ClickRecognizer>& GetClickRecognizer();  // Also OK with forward decl
};
```

**Example - After Optimization**:
```cpp
// click_event.h (AFTER)
// Removed: #include "click_recognizer.h"
namespace OHOS::Ace::NG {
class ClickRecognizer;  // ✅ Forward declaration only
}

class ClickEventActuator {
private:
    RefPtr<ClickRecognizer> clickRecognizer_;  // Works with forward decl
};

// click_event.cpp
#include "core/components_ng/gestures/recognizers/click_recognizer.h"  // Full include here

const RefPtr<ClickRecognizer>& ClickEventActuator::GetClickRecognizer() {
    if (!clickRecognizer_) {
        clickRecognizer_ = MakeRefPtr<ClickRecognizer>();  // Needs full definition
    }
    return clickRecognizer_;
}
```

**Key Insights**:
- ✅ Member variables with `RefPtr<T>` work with forward declaration
- ✅ Return types `const RefPtr<T>&` work with forward declaration
- ❌ Actual instantiation `MakeRefPtr<T>()` requires full definition in .cpp

**Verification**: Compile both header and cpp to ensure no undefined type errors.

---

#### Scenario 2: Cross-Namespace Forward Declarations

**When to use**: When a type from one namespace is needed in another namespace's header file.

**Pattern**: Add forward declarations in appropriate namespace scope.

**Example - gesture_event_hub.h needs ClickInfo**:
```cpp
// click_event.h
#include "base/memory/ace_type.h"
#include "core/components_ng/event/gesture_event_actuator.h"
#include "ui/gestures/gesture_event.h"         // Provides GestureEvent, GestureEventFunc
#include "core/components_ng/event/target_component.h"  // Provides GestureJudgeFunc

// Cross-namespace forward declaration for gesture_event_hub.h
namespace OHOS::Ace {
class ClickInfo;  // Type defined in OHOS::Ace, needed by gesture_event_hub.h
}

namespace OHOS::Ace::NG {
class GestureEventHub;   // Forward declaration in target namespace
class ClickRecognizer;   // Forward declaration in target namespace
}

class ClickEventActuator : public GestureEventActuator {
    // ... implementation
};
```

**Why this works**:
- When gesture_event_hub.h is included through frame_node.h → click_event.h chain
- ClickInfo forward declaration is already available
- Avoids circular dependencies
- Reduces coupling between namespaces

---

#### Scenario 3: Replacing Indirect Dependencies with Precise Includes

**Problem**: Removing a heavy include (like click_recognizer.h) breaks compilation because other types were indirectly included.

**Solution**: Identify and directly include only the necessary type definition headers.

**Example - Removing click_recognizer.h**:
```cpp
// BEFORE: Heavy indirect dependencies
#include "core/components_ng/gestures/recognizers/click_recognizer.h"
// This indirectly brought in:
// - tap_gesture.h (GestureEventFunc)
// - gesture_recognizer.h
// - multi_fingers_recognizer.h
// - And many more...

// AFTER: Precise includes
#include "ui/gestures/gesture_event.h"         // Provides GestureEvent, GestureEventFunc
#include "core/components_ng/event/target_component.h"  // Provides GestureJudgeFunc

// Forward declarations
namespace OHOS::Ace::NG {
class ClickRecognizer;  // Only name needed for RefPtr<ClickRecognizer>
}
```

**Analysis Process**:
1. Search for type usages in the header (e.g., `GestureEventFunc`, `GestureJudgeFunc`)
2. Find their definition locations using grep/search tools
3. Include the header that defines the type directly
4. Replace heavy include with forward declaration for RefPtr/WeakPtr types

---

#### Scenario 4: Complete Decision Matrix for Forward Declarations

| Usage Pattern | Can Use Forward Decl? | Requires Full Include? |
|---------------|----------------------|----------------------|
| `T*` member variable | ✅ Yes | ❌ No |
| `T&` parameter/return | ✅ Yes | ❌ No |
| `RefPtr<T>` member | ✅ Yes | ❌ No |
| `RefPtr<T>&` return | ✅ Yes | ❌ No |
| `WeakPtr<T>` member | ✅ Yes | ❌ No |
| `std::unique_ptr<T>` | ✅ Yes | ❌ No |
| `std::shared_ptr<T>` | ✅ Yes | ❌ No |
| `std::vector<T>` | ❌ No* | ✅ Yes |
| `std::vector<T*>` | ✅ Yes | ❌ No |
| Class inheritance | ❌ No | ✅ Yes |
| `T` member variable | ❌ No | ✅ Yes |
| `T` value parameter | ❌ No* | ✅ Yes |
| Template instantiation | ❌ No | ✅ Yes |
| Access static members | ❌ No | ✅ Yes |
| Access inline methods | ❌ No | ✅ Yes |

\* Exceptions exist with extern templates

---

#### Common Pitfalls and Solutions

**Pitfall 1: Removing include breaks dependent headers**

**Symptom**:
```
error: unknown type name 'ClickInfo' in gesture_event_hub.h
```

**Root Cause**: gesture_event_hub.h was indirectly getting ClickInfo from click_recognizer.h

**Solution**: Add forward declaration in appropriate namespace
```cpp
namespace OHOS::Ace {
class ClickInfo;  // Forward declaration for gesture_event_hub.h
}
```

---

**Pitfall 2: Missing type definitions after removing include**

**Symptom**:
```
error: unknown type name 'GestureEventFunc'
error: unknown type name 'GestureJudgeFunc'
```

**Root Cause**: These types were indirectly included through click_recognizer.h

**Solution**: Directly include headers that define these types
```cpp
#include "ui/gestures/gesture_event.h"         // GestureEvent, GestureEventFunc
#include "core/components_ng/event/target_component.h"  // GestureJudgeFunc
```

---

**Pitfall 3: Namespace mismatch in forward declarations**

**Symptom**:
```
error: no type named 'ClickInfo' in namespace 'OHOS::Ace::NG'
```

**Root Cause**: ClickInfo is in `OHOS::Ace`, not `OHOS::Ace::NG`

**Solution**: Use correct namespace for forward declaration
```cpp
namespace OHOS::Ace {        // Correct namespace
class ClickInfo;
}

namespace OHOS::Ace::NG {    // Different namespace
class ClickRecognizer;
}
```

---

#### Real Case Study: click_event.h Optimization

**Before Optimization**:
```cpp
// 214 lines, 6 includes
#include <list>
#include "base/memory/ace_type.h"
#include "base/memory/referenced.h"              // Redundant
#include "base/utils/noncopyable.h"
#include "core/components_ng/event/gesture_event_actuator.h"
#include "core/components_ng/gestures/recognizers/click_recognizer.h"  // Heavy include

namespace OHOS::Ace::NG {
class GestureEventHub;  // Only 1 forward declaration
}

// 15 inline method implementations
```

**After Optimization**:
```cpp
// 139 lines (-35%), 5 includes (-16.7%)
#include <list>
#include "base/memory/ace_type.h"
#include "base/utils/noncopyable.h"
#include "core/components_ng/event/gesture_event_actuator.h"
#include "ui/gestures/gesture_event.h"         // Precise include
#include "core/components_ng/event/target_component.h"  // Precise include

namespace OHOS::Ace {
class ClickInfo;  // Cross-namespace forward declaration
}

namespace OHOS::Ace::NG {
class GestureEventHub;    // Existing forward declaration
class ClickRecognizer;    // ✨ New forward declaration (RefPtr<T> optimization)
}

// 5 inline method implementations (moved 12 to cpp)
```

**Results**:
- ✅ Header reduced from 214 to 139 lines (-35.0%)
- ✅ Includes reduced from 6 to 5 (-16.7%)
- ✅ Forward declarations increased from 1 to 3 (+200%)
- ✅ Inline implementations reduced from 15 to 5 (-66.7%)
- ✅ Compilation verified successfully
- ✅ test_header.cpp indirect dependency verified

**Key Techniques Applied**:
1. Replaced `#include "click_recognizer.h"` with forward declaration
2. Added precise includes for type definitions (`GestureEventFunc`, `GestureJudgeFunc`)
3. Added cross-namespace forward declaration for `ClickInfo`
4. Moved 12 inline implementations to cpp file

---

### Step 5: Split Headers for Constants and Enums

**Objective**: Extract frequently-used constants or enums into separate headers to reduce coupling.

**When to Apply**:
- Original header is only included for a few constants or enum values
- Multiple files depend on these constants but not the full header
- Splitting provides measurable compilation benefit

**Procedure**:
1. Identify constants or enums that are dependencies for other files
2. Create new header file (e.g., `original_types.h`, `original_constants.h`)
3. Move extracted definitions to new header
4. Update original header to include the split header
5. Update dependent files to include only the smaller header

**Example**:
```cpp
// original.h (before)
#pragma once
namespace Constants {
    constexpr int MAX_VALUE = 100;
    enum class Type { A, B, C };
}

class BigImplementation {
    // ... hundreds of lines
};

// original_types.h (after split)
#pragma once
namespace Constants {
    constexpr int MAX_VALUE = 100;
    enum class Type { A, B, C };
}

// original.h (after split)
#pragma once
#include "original_types.h"
class BigImplementation {
    // ... implementation
};
```

**Verification**: Only split if it provides clear compilation benefit. Measure before/after with compile-analysis skill.

### Step 6: Apply PIMPL Pattern (When Applicable)

**Objective**: Hide implementation details to reduce compilation dependencies.

**When to Apply**:
- Header has many heavy dependencies from private members
- Public API is stable but implementation changes frequently
- Reducing header dependencies would significantly improve compile time

**Procedure**:
1. Create an Impl class (forward declared in header)
2. Move private members and heavy dependencies to Impl class in cpp
3. Replace private members with std::unique_ptr<Impl>
4. Update constructor/destructor to manage Impl lifecycle

**PIMPL Template**:
```cpp
// header.h
#pragma once
#include <memory>
namespace OHOS::Ace {
class MyClass {
public:
    MyClass();
    ~MyClass();

    // Public interface
    void PublicMethod();

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

// cpp.cpp
#include "header.h"
#include "heavy_dependency.h"

class MyClass::Impl {
public:
    HeavyDependency dep_;
    // Private implementation details
};

MyClass::MyClass() : impl_(std::make_unique<Impl>()) {}
MyClass::~MyClass() = default;

void MyClass::PublicMethod() {
    impl_->dep_.DoSomething();
}
```

**Caution**: PIMPL adds runtime overhead (extra allocation, indirection). Only use when compilation benefit justifies cost.

### Step 7: Optimize Template Methods

**Objective**: Reduce template compilation overhead through explicit instantiation.

**Procedure**:
1. Identify template methods in header
2. Check if templates can be converted to regular methods with explicit instantiation
3. Move template implementations to cpp file
4. Add explicit instantiation declarations for commonly used types

**Example**:
```cpp
// header.h (before)
template<typename T>
void Process(T value) {
    // Implementation
}

// header.h (after)
template<typename T>
void Process(T value);

extern template void Process<int>(int);
extern template void Process<float>(float);

// cpp.cpp (after)
template<typename T>
void Process(T value) {
    // Implementation
}

template void Process<int>(int);
template void Process<float>(float);
```

**Limitation**: Only works when template parameter types are known and limited.

### Step 8: Verify Standalone Compilation

**Objective**: Ensure optimized code compiles correctly.

**Procedure**:
1. Use compile-analysis skill to extract compilation command for the cpp file
2. Verify standalone compilation of the cpp file
3. For test_header.cpp analysis, verify it compiles with optimized header
4. Do NOT run full build - only standalone compilation verification

**Error Handling**:
- If compilation fails, analyze errors
- Fix missing includes or forward declarations
- Re-verify until compilation succeeds
- Document all fixes applied

### Step 9: Measure Optimization Results

**Objective**: Quantify the impact of optimizations.

**Metrics to Collect**:

1. **Header dependency count**:
   - Count includes before optimization
   - Count includes after optimization
   - Calculate reduction percentage

2. **Compilation time**:
   - Use compile-analysis skill to measure before/after
   - Report time savings

3. **Memory footprint**:
   - Measure header file size before/after
   - Report reduction percentage

4. **Lines of code**:
   - Header file LOC reduction
   - New LOC added to cpp file

**Result Template**:
```
## Optimization Results

### Header: frameworks/path/to/header.h

**Before Optimization:**
- Includes: 15
- Header size: 45.2 KB
- Estimated compile impact: High

**After Optimization:**
- Includes: 6
- Header size: 12.8 KB
- Reduction: 60% includes, 72% size

**Changes Made:**
- Moved 12 method implementations to cpp
- Converted 8 includes to forward declarations
- Removed 3 unused includes
- Split constants into separate header
- Applied PIMPL pattern (if applicable)

**Compilation Status:** ✅ Verified standalone compilation
```

### Step 10: Stage Changes with Git

**Objective**: Preserve optimized files in git.

**Procedure**:
1. Use `git add` to stage modified files:
   - Optimized header file
   - Modified or created cpp file
   - Any newly created split headers
2. Do NOT stage test_header.cpp (it's reference only)
3. Present staged changes to user

---

## Generalized Optimization Strategies

This section provides **generalized guidance** derived from real optimization cases in ace_engine. Use these strategies to select the right optimization approach for your situation.

### Strategy Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│               What type of dependency problem?              │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   Heavy include        Value type        Cross-namespace
   within same        member from        include with
   namespace          heavy include    only enum usage
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  RefPtr<T>    │  │ unique_ptr<T> │  │ Light Include │
│  Forward Decl │  │  + Forward    │  │  Replacement │
│  (Scenario 1) │  │  Declaration  │  │  (Scenario 3) │
└───────────────┘  └───────────────┘  └───────────────┘
```

### Scenario 1: RefPtr<T> Forward Declaration (Lightest)

**When to use**:
- Member is already `RefPtr<T>` or `WeakPtr<T>`
- Only type name needed in header
- No value semantics required

**Pattern**:
```cpp
// Header
namespace OHOS::Ace::NG {
class ClickRecognizer;  // Forward declaration
}

class ClickEventActuator {
private:
    RefPtr<ClickRecognizer> clickRecognizer_;  // ✅ Works with forward decl
};

// CPP
#include "core/components_ng/gestures/recognizers/click_recognizer.h"

const RefPtr<ClickRecognizer>& ClickEventActuator::GetClickRecognizer() {
    if (!clickRecognizer_) {
        clickRecognizer_ = MakeRefPtr<ClickRecognizer>();  // Full definition needed here
    }
    return clickRecognizer_;
}
```

**⚠️ CRITICAL: RefPtr<T> Members CAN Use Forward Declarations**

**Common misconception**: "RefPtr<T> members require complete type definition"

**✅ Correct understanding**: RefPtr<T> members work perfectly with forward declarations, **provided that**:

1. **All inline methods that use the RefPtr<T> member are moved to .cpp**
   - Any method that calls `member_->Method()` must be in .cpp
   - Any method that calls `MakeRefPtr<T>()` must be in .cpp
   - Any method with `RefPtr<T>` parameter or return type should be in .cpp

2. **Only declarations remain in header**
   - `RefPtr<T> member_;` ✅ Works with forward declaration
   - `RefPtr<T> GetMember();` ✅ Declaration only
   - `void SetMember(const RefPtr<T>& member);` ✅ Declaration only

3. **No inline instantiation in header**
   - ❌ `MakeRefPtr<T>()` calls in header
   - ❌ `member_->Method()` calls in header
   - ✅ Both must be in .cpp implementation

**Example from gesture_recognizer.h optimization**:
```cpp
// gesture_recognizer.h - BEFORE (inline implementations)
class NGGestureRecognizer {
    bool IsSystemGesture() const {  // ❌ Inline - needs full GestureInfo definition
        if (!gestureInfo_) return false;
        return gestureInfo_->IsSystemGesture();
    }

    RefPtr<GestureInfo> GetGestureInfo() {  // ❌ Inline - returns RefPtr<GestureInfo>
        return gestureInfo_;
    }

private:
    RefPtr<GestureInfo> gestureInfo_;  // ❌ Requires full definition due to inline methods
};

// gesture_recognizer.h - AFTER (forward declaration + declarations)
namespace OHOS::Ace::NG {
class GestureInfo;  // ✅ Forward declaration only
}

class NGGestureRecognizer {
    bool IsSystemGesture() const;  // ✅ Declaration only

    RefPtr<GestureInfo> GetGestureInfo();  // ✅ Declaration only

private:
    RefPtr<GestureInfo> gestureInfo_;  // ✅ Works with forward declaration!
};

// gesture_recognizer.cpp - Full implementations
#include "core/components_ng/event/gesture_info.h"  // ✅ Full include here

bool NGGestureRecognizer::IsSystemGesture() const {
    if (!gestureInfo_) return false;
    return gestureInfo_->IsSystemGesture();  // ✅ Full definition available
}

RefPtr<GestureInfo> NGGestureRecognizer::GetGestureInfo() {
    return gestureInfo_;  // ✅ Can return RefPtr with full definition
}
```

**Key principle**: RefPtr<T> members **do NOT** require complete type definition in the header. The requirement comes from **inline methods** that use the member, not from the member itself.

**Benefits**:
- ✅ No destructor separation needed (RefPtr manages lifecycle)
- ✅ Minimal code changes
- ✅ Zero runtime overhead
- ✅ Existing pattern in ace_engine

**Real case**: `case-click_event-forward-declaration.md`

**Complexity**: Easy

---

### Scenario 2: Value Type → unique_ptr<T> Conversion

**When to use**:
- Value type member from heavy include
- Member only used in implementation (.cpp)
- Want to remove heavy include dependency
- Can accept small runtime overhead (heap allocation)

**Pattern**:
```cpp
// Before
#include "core/components_ng/gestures/gesture_info.h"  // Heavy include

class DragDropRelatedConfigurations {
private:
    DragPreviewOption previewOption_;  // ❌ Value type - needs full definition
};

// After
namespace OHOS::Ace::NG {
struct DragPreviewOption;  // Forward declaration
}

class DragDropRelatedConfigurations {
public:
    ~DragDropRelatedConfigurations() override;  // ✅ Declaration only

    ACE_FORCE_EXPORT const DragPreviewOption& GetOrCreateDragPreviewOption();  // ✅ Return const&

private:
    std::unique_ptr<DragPreviewOption> previewOption_;  // ✅ Smart pointer
};

// CPP
#include "core/components_ng/gestures/gesture_info.h"  // Full include

DragDropRelatedConfigurations::~DragDropRelatedConfigurations() = default;

const DragPreviewOption& DragDropRelatedConfigurations::GetOrCreateDragPreviewOption()
{
    if (!previewOption_) {
        previewOption_ = std::make_unique<DragPreviewOption>();
    }
    if (!previewOption_) {
        static DragPreviewOption defaultInstance;  // ✅ Non-const fallback
        return defaultInstance;
    }
    return *previewOption_;  // ✅ Zero-copy return
}
```

**Required Changes**:
1. ✅ Add forward declaration
2. ✅ Convert member to `std::unique_ptr<T>`
3. ✅ Move destructor to cpp (required for unique_ptr<T> with forward decl)
4. ✅ Change return value to `const T&` (zero-copy optimization)
5. ✅ Update cpp to dereference smart pointer

**Benefits**:
- ✅ Removes heavy include dependency
- ✅ Zero-copy return value optimization
- ✅ Maintains const correctness
- ✅ Cleaner encapsulation

**Costs**:
- ⚠️ Heap allocation overhead (usually negligible)
- ⚠️ Need to manage destructor in cpp

**Real case**: `case-drag-drop-forward-declaration.md`

**Complexity**: Medium

---

### Scenario 3: Include Replacement (Light Include Strategy)

**When to use**:
- Heavy cross-namespace include
- Only enums/constants needed from that header
- Can create new light header file
- Most types can be forward declared

**Pattern**:
```cpp
// Before - Heavy include
#include "core/gestures/drag_event.h"  // ~200 lines, full implementations

class DragEventActuator {
private:
    OptionsAfterApplied optionsAfterApplied_;  // Value type
};

// After - Light include + forward declarations
#include "core/gestures/drag_constants.h"  // ✅ Only enums (~15 lines)

namespace OHOS::Ace {
class DragEvent;  // Forward declaration
}

namespace OHOS::Ace::NG {
struct OptionsAfterApplied;  // Forward declaration
}

class DragEventActuator {
public:
    const OptionsAfterApplied& GetOptionsAfterApplied();  // Declaration only

private:
    std::unique_ptr<OptionsAfterApplied> optionsAfterApplied_;  // ✅ Smart pointer
};

// Create light header: drag_constants.h
namespace OHOS::Ace {
enum class PreDragStatus : int32_t {
    READY = 0,
    PROCESSING = 1,
    FAILED = 2,
};
}
```

**Required Changes**:
1. ✅ Create new light header (*_constants.h)
2. ✅ Extract enums/constants to light header
3. ✅ Replace heavy include with light include
4. ✅ Add forward declarations for complex types
5. ✅ Convert value members to smart pointers (if applicable)
6. ✅ Move implementations to cpp

**Benefits**:
- ✅ Massive dependency reduction (90%+)
- ✅ Cleaner namespace boundaries
- ✅ Better code organization
- ✅ Reusable light header for other files

**Costs**:
- ⚠️ Creates new file (light header)
- ⚠️ More changes than Scenario 1

**Real case**: `case-drag-event-include-reduction.md`

**Complexity**: Medium

---

### Strategy Comparison Table

| Aspect | Scenario 1: RefPtr<T> | Scenario 2: unique_ptr<T> | Scenario 3: Light Include |
|--------|----------------------|--------------------------|-------------------------|
| **Primary use case** | Already using smart pointers | Value type members | Cross-namespace heavy includes |
| **Creates new files?** | No | No | Yes (light headers) |
| **Destructor separation** | Not needed | Required | Required |
| **Return type change** | May need `RefPtr<T>&` | Value → `const T&` | May or may not need |
| **Runtime overhead** | Zero | Small (heap alloc) | Small (heap alloc) |
| **Dependency reduction** | High | High | Very High (90%+) |
| **Code complexity** | Low | Medium | Medium |
| **Best for** | RefPtr/WeakPtr members | Value type members | Cross-namespace dependencies |

---

### Common Implementation Patterns

#### Pattern 1: Destructor Separation

**When**: Using forward declarations with smart pointer members

**Why**: Smart pointer destructor needs complete type definition

**Template**:
```cpp
// Header
class MyClass {
public:
    ~MyClass();  // ✅ Declaration only

private:
    std::unique_ptr<ForwardDeclaredType> member_;
};

// CPP
MyClass::~MyClass() = default;  // ✅ Implementation here
```

---

#### Pattern 2: Zero-Copy Return

**When**: Returning smart pointer managed objects

**Why**: Avoid unnecessary object copying

**Template**:
```cpp
// ❌ Before - Returns by value (creates copy)
DragPreviewOption GetOption() {
    return *previewOption_;
}

// ✅ After - Returns const reference (zero copy)
const DragPreviewOption& GetOption() {
    if (!previewOption_) {
        static DragPreviewOption defaultInstance;
        return defaultInstance;
    }
    return *previewOption_;
}
```

---

#### Pattern 3: Static Fallback Instance

**When**: Smart pointer may be null, need safe default

**Template**:
```cpp
const OptionsAfterApplied& GetOptionsAfterApplied()
{
    if (!optionsAfterApplied_) {
        static OptionsAfterApplied defaultInstance;  // ✅ Non-const
        return defaultInstance;
    }
    return *optionsAfterApplied_;
}
```

**Why non-const**: Const static initialization may fail for complex types with constructors.

---

#### Pattern 4: Conditional Dereference

**When**: Passing smart pointer value to function expecting value type

**Template**:
```cpp
// When calling: void SetOptionsAfterApplied(const OptionsAfterApplied& options)

// ❌ Wrong - Compile error
frameNode->SetOptionsAfterApplied(optionsAfterApplied_);

// ✅ Correct - Conditional dereference
frameNode->SetOptionsAfterApplied(
    optionsAfterApplied_ ? *optionsAfterApplied_ : OptionsAfterApplied()
);
```

---

### Generalized Decision Checklist

Use this checklist to decide which optimization strategy to apply:

#### Step 1: Analyze the Dependency

- [ ] Identify the heavy include causing the issue
- [ ] Search for all usages of types from that include in the header
- [ ] Categorize usages:
  - Member variables (value type vs smart pointer)
  - Function parameters/returns
  - Base class inheritance
  - Template instantiations

#### Step 2: Choose Strategy

**If already using RefPtr/WeakPtr → Scenario 1**
- ✅ Just add forward declaration
- ✅ No other changes needed

**If value type member from same namespace → Scenario 2**
- ✅ Convert to unique_ptr<T>
- ✅ Move destructor to cpp
- ✅ Return const& instead of by value

**If cross-namespace include with only enum usage → Scenario 3**
- ✅ Create light header (*_constants.h)
- ✅ Replace heavy include with light include
- ✅ Add forward declarations for complex types
- ✅ Convert value members to smart pointers (if applicable)

**If none of the above → Consider PIMPL**
- See `references/pimp-guide.md` for detailed guidance

#### Step 3: Implement Changes

- [ ] Add forward declarations
- [ ] Convert members to smart pointers (if applicable)
- [ ] Move destructor to cpp (if using unique_ptr)
- [ ] Move inline implementations to cpp
- [ ] Update return types to const&
- [ ] Update cpp to dereference smart pointers
- [ ] Add full includes to cpp
- [ ] Verify standalone compilation

#### Step 4: Verify Results

- [ ] Check that header compiles independently
- [ ] Verify cpp compiles with full includes
- [ ] Confirm no compilation errors in dependent files
- [ ] Measure dependency reduction

---

### Common Pitfalls

#### Pitfall 1: Forgetting Destructor Separation

**Symptom**:
```
error: invalid application of 'sizeof' to an incomplete type
```

**Cause**: unique_ptr<T> with forward declaration needs destructor in cpp

**Solution**: Move destructor implementation to cpp file

---

#### Pitfall 2: Returning by Value After unique_ptr Conversion

**Symptom**: Unnecessary object copies, potential performance degradation

**Cause**: Changed member to unique_ptr but still returning by value

**Solution**: Change return type to `const T&`

---

#### Pitfall 3: Missing Dereference

**Symptom**: Compile error when passing smart pointer to function

**Cause**: Forgetting to dereference unique_ptr when value type expected

**Solution**: Use conditional dereference pattern:
```cpp
function(ptr ? *ptr : Type());
```

---

#### Pitfall 4: Const Static Initialization Failure

**Symptom**: Static initialization fails for complex types

**Cause**: Using `static const T` with complex constructor

**Solution**: Use `static T` (non-const) as fallback

---

## Additional Resources

### Reference Files

For detailed techniques and examples:
- **`references/patterns.md`** - Common refactoring patterns for header optimization
- **`references/pimp-guide.md`** - PIMPL pattern detailed guide with ace_engine examples
- **`references/forward-declaration.md`** - Forward declaration best practices
- **`references/case-split-enums.md`** - Real case study: Splitting enums from `drag_event.h` to `drag_constants.h` (90%+ dependency reduction)
- **`references/case-click_event-forward-declaration.md`** - Real case study: RefPtr<T> forward declaration optimization for `click_event.h` (35% size reduction, smart pointer optimization patterns)
- **`references/case-drag-drop-forward-declaration.md`** - ✨ NEW: Real case study: unique_ptr<T> conversion for value type members in `drag_drop_related_configuration.h`
- **`references/case-drag-event-include-reduction.md`** - ✨ NEW: Real case study: Light include replacement strategy for cross-namespace dependencies in `drag_event.h`

### Examples

Working examples in `examples/`:
- **`before-after/`** - Side-by-side comparisons of optimizations
- **`pimpl-example/`** - Complete PIMPL implementation example
- **`split-header/`** - Header splitting example

### Scripts

Utility scripts in `scripts/`:
- **`analyze-includes.sh`** - Analyze header include dependencies
- **`extract-includes.py`** - Extract include statistics from headers

## Common Pitfalls

**DO NOT:**
- Modify test_header.cpp for any reason
- Run full builds during optimization
- Modify business logic or change behavior
- Create unnecessary additional files (beyond splitting scenarios)
- Expand optimization scope beyond defined steps
- Forget to verify standalone compilation

**ALWAYS:**
- Verify each optimization with standalone compilation
- Document changes and their rationale
- Use compile-analysis skill for compilation command extraction
- Focus on reducing header dependencies
- Maintain functional equivalence
- Stage changes with git add after successful optimization

## Analysis-Only Mode

When user specifies "只分析不进行修改":

1. Perform all analysis steps (1-9)
2. Generate detailed report with:
   - Current header dependency analysis
   - Recommended optimizations with rationale
   - Expected improvements
   - Specific code changes proposed
3. Present report to user
4. Request approval before making modifications
5. Do NOT modify any files until user approves

## Integration with compile-analysis Skill

This skill integrates with compile-analysis skill for compilation efficiency measurement:

1. Use compile-analysis to extract compilation commands
2. Measure compilation time before optimization
3. Apply optimizations
4. Measure compilation time after optimization
5. Compare and report results

When compilation command extraction is needed, invoke:
```
Use compile-analysis skill to extract compilation command for [file.cpp]
```
