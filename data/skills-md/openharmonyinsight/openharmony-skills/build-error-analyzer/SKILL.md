---
name: build-error-analyzer
description: This skill should be used when the user asks to "分析构建错误", "analyze build errors", "查看编译错误", "检查构建日志", "诊断链接错误", "fix build errors", "resolve compilation errors", "分析 last_error.log", "extract build error", "分析SDK的编译错误", "分析 SDK 编译错误", "analyze SDK build errors", "check SDK errors", "诊断 sdk 编译错误", or mentions analyzing build failures, compilation errors, linker errors, undefined symbols, SDK compilation errors, or needs to fix build issues. Focuses on reading last_error.log from out/<product>/ directory (or out/sdk/ for SDK builds) and providing specific fix recommendations based on error patterns and historical cases.
version: 0.9.0
---

# Build Error Analyzer Skill

This skill specializes in analyzing OpenHarmony build errors from `last_error.log` and providing **fix recommendations only** (no automatic code modifications) based on error patterns and historical case studies.

**IMPORTANT**: This skill provides analysis and recommendations ONLY. It does NOT automatically modify code files.

## ⚠️ CRITICAL WORKFLOW (MUST FOLLOW)

**YOU MUST ALWAYS FOLLOW THIS EXACT SEQUENCE**:

1. **FIRST**: Extract errors from `out/<product>/build.log` → generates `out/<product>/last_error.log`
2. **THEN**: Read and analyze ONLY from `out/<product>/last_error.log`
3. **NEVER**: Read directly from `out/<product>/build.log` or any other log files (error.log, build_output*.log, etc.)
4. **SUCCESS CASE**: If `last_error.log` contains "build success" or "no error", STOP and report success

**Why?**:
- `build.log` contains the entire build history (thousands of lines)
- `last_error.log` contains ONLY the most recent error block (extracted by script)
- Reading `build.log` directly will give you STALE or IRRELEVANT errors
- The extraction script ensures you always analyze the LATEST errors
- Other log files (error.log, build_output*.log) may contain outdated errors from previous builds

**Before reading ANY errors, ALWAYS run**:
```bash
# ⚠️ CRITICAL: First cd to OpenHarmony root directory, then run the script
cd <openharmony_root>
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/<product>/build.log
```

**⚠️ CRITICAL - CHECK FOR SUCCESS FIRST**:
After reading `last_error.log`, if you see:
- `build success, no error`
- `no error`
- Or similar success messages

**IMMEDIATELY STOP and report**:
```
## ✅ 构建成功

最新的构建已经成功完成，没有发现任何错误。

**构建状态**: 成功
**错误信息**: 无

建议: 您可以继续进行开发或测试工作。
```

**DO NOT**:
- ❌ Continue searching for errors in other log files
- ❌ Read error.log
- ❌ Read build_output*.log files
- ❌ Look for historical errors

## Important Path Information

**Always use these paths**:
- **Extraction Script**: `foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh` (relative to OpenHarmony root)
- **Source Build Log**: `out/<product>/build.log` (e.g., `out/rk3568/build.log`) - **DO NOT READ DIRECTLY**
- **Target Error Log**: `out/<product>/last_error.log` (auto-generated in same directory as build.log) - **READ ONLY THIS FILE**

**⚠️ SPECIAL CASE - SDK Build Paths**:
- **SDK Build Log**: `out/sdk/build.log` (NOT `out/ohos-sdk/build.log`)
- **SDK Error Log**: `out/sdk/last_error.log` (NOT `out/ohos-sdk/last_error.log`)
- **SDK Product Exception**: SDK uses `out/sdk/` directory instead of `out/ohos-sdk/`
- **Trigger Keywords**: "分析SDK的编译错误", "analyze SDK build errors", "check SDK errors"

**Workflow**:
1. ✅ Extract errors from `out/<product>/build.log` using the script → creates `out/<product>/last_error.log`
2. ✅ For SDK: Extract from `out/sdk/build.log` → creates `out/sdk/last_error.log`
3. ✅ Analyze errors from the extracted `last_error.log` ONLY
4. ✅ **Provide fix recommendations ONLY - do NOT modify code**

**Common Mistakes to Avoid**:
- ❌ Reading `build.log` directly (will get stale/wrong errors)
- ❌ Reading `error.log` (contains outdated errors from previous builds)
- ❌ Reading other log files (build_output*.log, error.*.log, etc.)
- ❌ Continuing to search for errors when `last_error.log` shows "build success"
- ❌ Analyzing errors without extraction step
- ❌ Running extraction script from wrong directory (MUST be from OpenHarmony root)
- ✅ ALWAYS cd to `<openharmony_root>` first
- ✅ ALWAYS extract → then read `last_error.log` ONLY
- ✅ If `last_error.log` shows success → STOP and report success

## Behavior Guidelines

**This skill provides ANALYSIS and RECOMMENDATIONS ONLY:**

✅ **DO**:
- Extract errors from build logs
- Analyze and categorize errors
- Match errors against known patterns
- Provide detailed fix recommendations with file paths and line numbers
- Show before/after code examples
- Explain root causes
- Suggest verification steps

❌ **DO NOT**:
- Use Edit tool to modify code files
- Use Write tool to create or modify files
- Run build commands automatically
- Apply fixes without user confirmation
- Make any changes to the codebase
- Read from log files other than `last_error.log` (error.log, build_output*.log, error.*.log, etc.)
- Continue searching for errors when build is successful

⚠️ **CRITICAL - NEVER SUGGEST CLEARING LTO CACHE**:
- ❌ **NEVER** suggest clearing `thinlto-cache` directory
- ❌ **NEVER** suggest clearing `llvmcache-*` directories
- ❌ **NEVER** suggest deleting `out/obj` directory
- ❌ **NEVER** suggest deleting entire `out/` directory
- ❌ **NEVER** blame LTO cache for build errors
- ❌ **NEVER** suggest "clean build" as first solution

**Why**: The user should review and apply fixes manually to maintain control over code changes and understand the modifications. LTO cache issues are extremely rare and clearing caches as first resort masks real problems, wastes rebuild time, and disrupts incremental compilation benefits.

## Prerequisites

1. **⚠️ CRITICAL**: ALWAYS extract from `out/<product>/build.log` FIRST before reading
2. **Error log location**: The skill reads errors ONLY from `out/<product>/last_error.log` (same directory as build.log)
3. **Error extraction**: ALWAYS use the extraction script from `foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh` (from OpenHarmony root) to generate/update `last_error.log` before reading
4. **Source build.log**: Errors are extracted ONLY from `out/<product>/build.log` in the OpenHarmony output directory
5. **Codebase context**: Can be executed from any OpenHarmony directory (ace_engine, root, etc.)
6. **⚠️ SUCCESS CHECK**: If `last_error.log` contains "build success" or "no error", STOP and report success - DO NOT read other log files like `error.log`, `build_output*.log`, etc.
7. **EXCLUSIVE LOG SOURCE**: ONLY read from `last_error.log` - NEVER from `error.log`, `build_output*.log`, `error.*.log`, or any other log files

## Analysis Workflow

### Step 1: Extract Latest Error (REQUIRED - ALWAYS DO THIS FIRST)

**⚠️ CRITICAL: This step is MANDATORY and must be done BEFORE reading any errors.**

**Why this is required:**
- `build.log` contains the full build output (old and new errors mixed together)
- Reading it directly will analyze STALE or IRRELEVANT errors
- The extraction script isolates ONLY the most recent error block
- `last_error.log` is generated in the same directory as `build.log`

**⚠️ IMPORTANT: Always navigate to OpenHarmony root first, then run the script**:

```bash
# Step 1: Navigate to OpenHarmony root directory
cd <openharmony_root>

# Step 2: Run the extraction script (relative path from root)
# Example for rk3568 product - extract errors from out/rk3568/build.log
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

# Example for SDK product - extract errors from out/sdk/build.log (⚠️ SPECIAL CASE: out/sdk/ NOT out/ohos-sdk/)
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/sdk/build.log

# Example for other products:
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3588/build.log
```

**The script will:**
- Extract ONLY the latest error block from `out/<product>/build.log`
- Output to `out/<product>/last_error.log` (same directory)
- Show error block size and summary
- Overwrite previous `last_error.log` if it exists

**⚠️ DO NOT SKIP THIS STEP**
- Even if `last_error.log` exists, RE-EXTRACT to get the latest errors
- DO NOT read `build.log` directly
- DO NOT read other log files (build_output*.log, error.log, error.*.log, etc.)
- ONLY analyze `last_error.log` after extraction

### Step 2: Read and Categorize Errors

**⚠️ CRITICAL**: Only read `last_error.log` from `out/<product>/` directory in the OpenHarmony output tree.

**After extraction, the error log is located at**:
- `out/<product>/last_error.log` (same directory as build.log)

**Read the extracted error log**:
```bash
# Check for last_error.log in common product directories
cat out/rk3568/last_error.log
# or for SDK (⚠️ SPECIAL CASE: out/sdk/ NOT out/ohos-sdk/)
cat out/sdk/last_error.log
# or for other products
cat out/rk3588/last_error.log
```

**⚠️ CRITICAL - CHECK FOR SUCCESS FIRST**:

**Before any analysis, CHECK if the build succeeded**:

If `last_error.log` contains:
- `build success, no error`
- `no error`
- Or similar success messages

**IMMEDIATELY STOP and report**:
```markdown
## ✅ 构建成功

最新的构建已经成功完成，没有发现任何错误。

**构建状态**: 成功
**错误信息**: 无

建议: 您可以继续进行开发或测试工作。
```

**DO NOT continue to**:
- ❌ Search for errors in error.log
- ❌ Search for errors in build_output*.log
- ❌ Search for errors in error.*.log files
- ❌ Look for historical errors
- ✅ **STOP and report success**

**Only if there are actual errors**, proceed to categorize them:

**Error Categories:**
1. **Compilation errors** (CXX tasks) - Syntax, missing headers, incomplete types
2. **Linker errors** (SOLINK/LINK tasks) - Undefined symbols, missing libraries
3. **Build system errors** - GN/Ninja configuration issues

### Step 3: Match Against Known Cases

Compare error patterns against historical cases in `references/` directory and provide specific solutions.

**Case matching priority**:
1. Match by error signature (e.g., "undefined symbol" + "referred by")
2. Match by error context (e.g., "timepicker module" usage)
3. Match by file pattern (e.g., BUILD.gn issues)
4. Provide general guidance if no specific case matches

### Step 4: Provide Fix Recommendations (NO Automatic Modifications)

**CRITICAL**: This step provides recommendations ONLY. Do NOT use Edit/Write tools to modify code.

Based on error type and matched cases, provide:
- Root cause analysis
- Specific file modifications needed (with exact line numbers and code snippets)
- Build system configuration changes (with exact GN file paths)
- Verification steps

**Recommended Output Format**:

```markdown
## 构建错误分析

### 错误类型
[编译错误/链接错误/构建系统错误]

### 错误位置
[文件路径:行号]

### 错误信息
[完整的错误消息]

### 根本原因
[详细解释为什么会出现这个错误]

### 修复建议

**文件**: [完整文件路径:行号]

**当前代码**:
```cpp
[错误代码片段]
```

**应修改为**:
```cpp
[正确代码片段]
```

**修改说明**: [解释为什么要这样修改]

### 验证步骤
1. [第一步验证操作]
2. [第二步验证操作]
3. [如何确认修复成功]

### 参考
[相关的历史案例或文档链接]
```

**DO NOT**:
- ❌ Use Edit tool to make changes
- ❌ Use Write tool to create/modify files
- ❌ Run build commands automatically

**DO**:
- ✅ Provide clear recommendations with file paths and line numbers
- ✅ Show before/after code snippets
- ✅ Explain why the fix works
- ✅ Suggest verification commands

## Error Patterns and Solutions

### Pattern 1: Undefined Symbol Errors

**Error signature:**
```
ld.lld: error: undefined symbol: <symbol_name>
>>> referenced by <file>:<line>
```

**⚠️ CRITICAL ANALYSIS WORKFLOW (MUST FOLLOW IN ORDER):**

When encountering `ld.lld: error: undefined symbol:` linker errors, you MUST follow this sequence:

#### Step 1: Identify Which Library is Failing to Link

Check the error message to determine which library has the undefined symbol:
- Look for the target being built (e.g., `libace.z.so`, `libace_compatible.z.so`, `libarkoala_native_ani.so`, `libace_ndk.z.so`)
- Check which library is referencing the symbol (`>>> referenced by`)

#### Step 2: Apply the Correct Scenario Based on Library Type

**Scenario 1: libace/libace_compatible Main Library Cannot Find Symbol**

**Symptoms:**
- Error occurs when linking `libace.z.so` or `libace_compatible.z.so`
- Symbol is undefined in the main library itself

**Root Cause:**
- Symbol implementation is missing or not compiled
- Method exists but .cpp file not in BUILD.gn

**Solution:**
1. **Check if implementation exists:**
   ```bash
   grep -r "SymbolName" --include="*.cpp" frameworks/
   ```

2. **If implementation exists, check BUILD.gn:**
   ```bash
   grep -r "implementation_file.cpp" frameworks/*/BUILD.gn
   ```

3. **Add .cpp to BUILD.gn:**
   - Find where other files in same directory are added
   - Add the missing .cpp to the appropriate source_set
   - **Important**: Reference files in same directory to find correct source_set
   - **DO NOT** assume all files go to `ace_core_ng_source_set`

4. **Verify with other files:**
   ```bash
   # Find where similar files in same directory are compiled
   find frameworks/core/components_ng/pattern/<pattern_name>/ -name "*.cpp"
   grep "similar_file.cpp" frameworks/core/BUILD.gn
   ```

**Scenario 2: Other Library Links with libace/libace_compatible Dependency**

**Symptoms:**
- Error occurs when linking a library that depends on `libace` or `libace_compatible`
- GN file shows `deps` includes libace/libace_compatible
- Symbol should come from main library

**Root Cause:**
- Symbol exists in main library but not exported
- Missing ACE_FORCE_EXPORT macro
- Symbol not in libace.map whitelist

**⚠️ CRITICAL: Distinguish Non-Template vs Template FIRST**

Before applying any solution, determine the type:

```
undefined symbol error
    ↓
Is it a non-template class method?
    → YES: Use Non-Template Solution (Step 1A)
    → NO: Use Template Solution (Step 1B, see Scenario 3)
```

**Solution (Step-by-Step):**

**Step 1A: For NON-TEMPLATE class methods** ⭐

**⚠️ CHECK 1: Does the class have ACE_FORCE_EXPORT?**

```cpp
// Case A: Class WITHOUT ACE_FORCE_EXPORT
class PaddingPropertyF {
    float Width() const;
};

// Case B: Class WITH ACE_FORCE_EXPORT
class ACE_FORCE_EXPORT PaddingPropertyF {
    float Width() const;
};
```

**For Case A (Class WITHOUT export) - PREFERRED METHOD**:
- ✅ **Add `ACE_FORCE_EXPORT` to method declaration in header (.h file)**
- ❌ **DO NOT** add to method definition in .cpp file
- Reason: Fine-grained export control, clear API boundaries

**Example (PaddingPropertyF case)**:
```cpp
// In header file (.h) - Add ACE_FORCE_EXPORT to method declarations
class PaddingPropertyF {
    ACE_FORCE_EXPORT float Width() const;   // ← Add here
    ACE_FORCE_EXPORT float Height() const;  // ← Add here
};

// In implementation file (.cpp) - NO ACE_FORCE_EXPORT here
float PaddingPropertyF::Width() const
{
    return left.value_or(0.0f) + right.value_or(0.0f);
}

float PaddingPropertyF::Height() const
{
    return top.value_or(0.0f) + bottom.value_or(0.0f);
}
```

**For Case B (Class WITH export)**:
- ✅ **NO additional export needed** - class export covers all methods
- ❌ **DO NOT** add `ACE_FORCE_EXPORT` to individual methods
- Reason: Entire class already exported

**Example**:
```cpp
// In header file (.h) - Class already exported
class ACE_FORCE_EXPORT PaddingPropertyF {  // ← Entire class exported
    float Width() const;   // Automatically exported
    float Height() const;  // Automatically exported
};

// In implementation file (.cpp) - No individual exports needed
float PaddingPropertyF::Width() const { /* implementation */ }
```

**Step 1B: For TEMPLATE class methods/functions** (see Scenario 3)

Template-specific rules apply - refer to Scenario 3 for detailed steps.

**Step 2: Add to libace.map with fine-grained symbol names** ⭐

After adding exports, add the symbol to `build/libace.map`:

```bash
# Check if symbol already in libace.map
grep "ClassName" build/libace.map
```

**Required changes:**
- ⭐ **ALWAYS prefer fine-grained symbol patterns** - Export specific methods over entire class
- Add symbol pattern to `build/libace.map` whitelist
- Use method-level granularity when possible

**Example - Regular Methods**:
```
# In build/libace.map
{
  global:
    # ✅ FINE-GRAINED - Export specific methods (PREFERRED for non-template)
    OHOS::Ace::PaddingPropertyF::Width*;
    OHOS::Ace::PaddingPropertyF::Height*;

    # ⚠️ ACCEPTABLE - Export entire class (if class has ACE_FORCE_EXPORT)
    OHOS::Ace::PaddingPropertyF::*;

    # ⚠️ DIFFERENT - Template patterns (use wildcards)
    void?OHOS::Ace::StringUtils::StringSplitter*;  # Template function
    OHOS::Ace::NG::LayoutConstraintT*;             # Template class
  };
}
```

**Why fine-grained for non-templates?**
- ⭐ **Minimizes exported symbol surface** - Only export what's needed
- ⭐ **Clearer API boundaries** - Explicit about which symbols are public
- ⭐ **Reduces symbol conflicts** - Smaller export surface = fewer conflicts
- ⭐ **Better dependency tracking** - Easy to see what's used by other modules
- ⭐ **Security** - Limits attack surface of exported symbols

**Common Mistakes (DO NOT do):**
- ❌ Using `ClassName::*;` when only specific methods are needed
- ❌ Exporting private methods that aren't used externally
- ❌ Forgetting that constructor wildcards match all overloads

**Step 3: Verify symbol export:**
```bash
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName
```

- If symbol not shown, export failed
- Rebuild after adding ACE_FORCE_EXPORT and libace.map entry

**Common mistakes (DO NOT do):**
- ❌ DO NOT use `ClassName::*;` when only specific methods are needed (⚠️ COMMON MISTAKE)
- ❌ DO NOT export all class members when only constructors are undefined
- ❌ DO NOT mix non-template and template rules
- ❌ DO NOT add export to .cpp for non-template methods
- ❌ DO NOT add individual method exports if class already has `ACE_FORCE_EXPORT`
- ❌ DO NOT use `__attribute__((visibility("default")))` directly

**⚠️ Example of Common Mistake - Over-Exporting**:

```cpp
// ❌ WRONG - Exports entire class when only constructors needed
OHOS::Ace::VelocityTracker::*;  // Exports ALL members unnecessarily

// ✅ CORRECT - Fine-grained constructor export
OHOS::Ace::VelocityTracker::VelocityTracker*;  // Only constructors
```

**When to use each pattern**:
- Use `ClassName::MethodName*;` for specific methods
- Use `ClassName::ClassName*;` for all constructor overloads
- Use `ClassName::*;` ONLY when most/all members are exported (rare)

**Scenario 3: Template Function Instantiation Issues**

**Symptoms:**
- Undefined symbol is a template function
- Template uses forward declaration + explicit instantiation in .cpp
- Error shows missing specific template specialization (e.g., `StringSplitter<Color>`, `TransformStrCase<std::string>`)

**Root Cause:**
- New specialization not explicitly instantiated
- Template declaration or implementation missing export macro
- libace.map missing pattern for template instantiation

**Solution (3 steps required):**

**Step 1: Add extern template declaration in header (.h)**

Add explicit template declaration for new specialization:
```cpp
// In header file (.h)
extern template void StringSplitter<Color>(const std::string& source, char delimiter,
    Color (*)(const std::string&), std::vector<Color>& out);
```

**Step 2: Add ACE_FORCE_EXPORT to template function declaration**

```cpp
// In header file (.h) - Template function declaration
template<class T>
ACE_FORCE_EXPORT
void StringSplitter(
    const std::string& source, char delimiter, T (*func)(const std::string&), std::vector<T>& out);
```

**Step 3: Add explicit instantiation in .cpp**

```cpp
// In implementation file (.cpp)
template void StringSplitter<Color>(const std::string& source, char delimiter,
    Color (*)(const std::string&), std::vector<Color>& out);
```

**Step 4: Add ACE_FORCE_EXPORT to template implementation**

```cpp
// In implementation file (.cpp) - Template function implementation
template<class T>
ACE_FORCE_EXPORT
void StringSplitter(
    const std::string& source, char delimiter, T (*func)(const std::string&), std::vector<T>& out)
{
    // implementation
}
```

**Step 5: Add to libace.map whitelist**

```
# In build/libace.map
{
  global:
    OHOS::Ace::StringUtils::*;
    void?OHOS::Ace::StringUtils::StringSplitter*;  # Match template instantiations
    void?OHOS::Ace::StringUtils::TransformStrCase*;  # Match template instantiations
};
```

**⚠️ Template Special Notes:**
- Templates require **BOTH** declaration and implementation to have export macros
- Explicit instantiation must be in .cpp file
- libace.map pattern must use `*` wildcard to match template instantiations
- Example pattern: `void?OHOS::Ace::StringUtils::StringSplitter*;`

**Scenario 4: Special Libraries (Rare Cases)**

**Symptoms:**
- Library does NOT depend on libace/libace_compatible
- But uses utility functions from main library (previously inline, now in .cpp)
- Only applies to these specific libraries:
  - `libarkoala_native_ani.so`
  - `libace_ndk.z.so`

**Root Cause:**
- Utility functions changed from inline to .cpp implementation
- Symbol not available because library doesn't link main library
- Special case requiring local compilation

**Solution:**
- Add the utility .cpp file directly to the library's BUILD.gn sources

**Example for libarkoala_native_ani:**
```gn
# In: frameworks/bridge/arkts_frontend/koala_projects/arkoala-arkts/arkui-ohos/src/ani/native/BUILD.gn
ohos_shared_library("arkoala_native_ani") {
  sources = [
    "//foundation/arkui/ace_engine/frameworks/base/utils/string_utils.cpp",
    "UINode/uinode_module_methods.cpp",
    # ... other sources
  ]
}
```

**Example for ace_ndk:**
```gn
# In: interfaces/native/BUILD.gn
ohos_shared_library("ace_ndk") {
  sources = [
    "//foundation/arkui/ace_engine/frameworks/base/utils/string_utils.cpp",
    "//foundation/arkui/ace_engine/frameworks/core/accessibility/native_interface_accessibility_impl.cpp",
    # ... other sources
  ]
}
```

**⚠️ IMPORTANT:**
- This solution is ONLY for `libarkoala_native_ani` and `ace_ndk`
- DO NOT use this pattern for other libraries
- These libraries use utility functions but don't link main library

**Scenario 5: Template Class Method Export Issues**

**Symptoms:**
- Error occurs when linking a library that depends on `libace` or `libace_compatible`
- Undefined symbol is a template class method with explicit instantiation
- Error shows: `undefined symbol: ClassName<T>::MethodName(params)`
- Template class has `ACE_FORCE_EXPORT` on struct declaration but methods still not exported

**Example Error:**
```
ld.lld: error: undefined symbol: OHOS::Ace::NG::LayoutConstraintT<float>::UpdateSelfMarginSizeWithCheck(OHOS::Ace::NG::OptionalSize<float> const&)
>>> referenced by slider_layout_algorithm.cpp:212
```

**Root Cause:**
- Template class struct declaration has `ACE_FORCE_EXPORT` (e.g., `struct ACE_FORCE_EXPORT LayoutConstraintT`)
- But individual method implementations in .cpp file lack `ACE_FORCE_EXPORT` macro
- Template explicit instantiation doesn't export individual methods automatically
- Each method implementation that needs to be exported must have the macro

**Solution:**

**Step 1: Add ACE_FORCE_EXPORT to method implementation in .cpp**

Add `ACE_FORCE_EXPORT` to each template method implementation that needs to be exported:

```cpp
// In implementation file (.cpp)
template<typename T>
ACE_FORCE_EXPORT  // ← Add this macro before return type
bool LayoutConstraintT<T>::UpdateSelfMarginSizeWithCheck(const OptionalSize<T>& size)
{
    if (selfIdealSize == size) {
        return false;
    }
    return selfIdealSize.UpdateSizeWithCheck(size);
}

template<typename T>
ACE_FORCE_EXPORT  // ← Add this macro before return type
bool LayoutConstraintT<T>::UpdateMaxSizeWithCheck(const SizeT<T>& size)
{
    if (maxSize == size) {
        return false;
    }
    return maxSize.UpdateSizeWhenSmaller(size);
}
```

**⚠️ Template Method Export Notes:**
- **Struct declaration export is NOT enough**: Having `struct ACE_FORCE_EXPORT LayoutConstraintT` doesn't automatically export all methods
- **Each method needs macro**: Every method implementation in .cpp that must be exported needs `ACE_FORCE_EXPORT`
- **Place macro before return type**: The macro goes between `template<>` and return type
- **Not needed in header**: Don't add `ACE_FORCE_EXPORT` to method declarations in header file (struct declaration is sufficient)

**Step 2: Verify libace.map has wildcard pattern**

Check that libace.map includes the template class with wildcard:

```bash
# Check libace.map for template class pattern
grep "LayoutConstraintT" build/libace.map
```

Expected output:
```
OHOS::Ace::NG::LayoutConstraintT*;
```

**⚠️ libace.map Wildcard Rules:**
- Use unquoted patterns with wildcards: `OHOS::Ace::ClassName::*;`
- **DO NOT** use quoted patterns with wildcards: `"OHOS::Ace::ClassName<T>::*;"` (wildcards won't work)
- Unquoted wildcards match all template instantiations automatically
- Use `*` at end to match all methods: `OHOS::Ace::NG::LayoutConstraintT*;`

**Step 3: Verify symbol export**

```bash
# Check if symbol is exported in shared library
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep LayoutConstraintT
```

Expected output (should show exported symbols):
```
0000000000000000 T _ZN2OHOS3Ace2NG14LayoutConstraintTIfE25UpdateSelfMarginSizeWithCheckERKNS0_11OptionalSizeIfEE
```

**⚠️ Common Mistakes:**
- ❌ Relying only on `struct ACE_FORCE_EXPORT ClassName` - NOT sufficient for methods
- ❌ Forgetting to add macro to each method implementation in .cpp
- ❌ Adding macro to method declarations in header (unnecessary, struct declaration is enough)
- ❌ Using quoted patterns in libace.map: `"ClassName<T>::*"` won't match
- ❌ Adding specific template instantiations to libace.map: use wildcards instead

**✅ Correct Approach:**
- ✅ Add `ACE_FORCE_EXPORT` to each template method implementation in .cpp
- ✅ Place macro between `template<>` and return type
- ✅ Keep struct declaration with `ACE_FORCE_EXPORT` in header
- ✅ Use unquoted wildcard in libace.map: `OHOS::Ace::NG::ClassName*;`

#### Step 3: Verify the Fix

After applying the appropriate solution:

```bash
# 1. Navigate to OpenHarmony root and rebuild
cd <openharmony_root>
./build.sh --product-name rk3568 --build-target ace_engine

# 2. Check if symbol is now exported (for scenarios 2-3)
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName

# 3. Extract new errors
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

# 4. Check result
cat out/rk3568/last_error.log

# For SDK builds (⚠️ use out/sdk/ directory):
# 1. Build SDK: ./build.sh --product-name ohos-sdk --ccache
# 2. Extract errors: foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/sdk/build.log
# 3. Check result: cat out/sdk/last_error.log
```

**Common mistakes (DO NOT do):**

⚠️ **CRITICAL - CACHE CLEARING IS FORBIDDEN**:
- ❌ **NEVER** suggest clearing thinlto-cache (99.9% of the time it's NOT the issue)
- ❌ **NEVER** suggest clearing llvmcache-* directories
- ❌ **NEVER** suggest deleting out/obj directory
- ❌ **NEVER** suggest deleting entire out directory
- ❌ **NEVER** suggest "clean build" as first solution
- ❌ Cache clearing masks real problems and wastes massive rebuild time
- ✅ **ALWAYS** analyze the actual error and fix the root cause

**Other common mistakes**:
- ❌ DO NOT skip scenario analysis
- ❌ DO NOT use `__attribute__((visibility("default")))` instead of ACE_FORCE_EXPORT
- ❌ DO NOT forget both declaration AND implementation export for templates
- ❌ DO NOT use Scenario 4 (local compilation) except for the two specified libraries
- ❌ DO NOT rely only on `struct ACE_FORCE_EXPORT ClassName` for template class methods (Scenario 5)
- ❌ DO NOT use quoted patterns with wildcards in libace.map: `"ClassName<T>::*"` doesn't work (Scenario 5)

**✅ ALWAYS do:**
- ✅ Identify which library is failing
- ✅ Check if implementation exists and is compiled
- ✅ Verify ACE_FORCE_EXPORT on header declarations
- ✅ Check libace.map whitelist
- ✅ For templates: check declaration, implementation, and instantiation
- ✅ Use correct scenario based on library type
- ✅ For template class methods: add ACE_FORCE_EXPORT to each method implementation in .cpp (Scenario 5)
- ✅ Use unquoted wildcard patterns in libace.map: `OHOS::Ace::NG::ClassName*;` (Scenario 5)

### Pattern 2: Incomplete Type Errors

**Error signature:**
```
error: member access into incomplete type 'const ClassName'
error: invalid use of incomplete type 'class ClassName'
error: member access into incomplete type 'OHOS::Ace::Animator'
    rawPtr_->IncRefCount();
```

**Common causes:**
1. Missing header include
2. Forward declaration without full definition
3. **RefPtr<T> as class member without proper implementation separation**
4. Header file optimization issues

**⚠️ SPECIAL CASE: RefPtr<T> as Class Member**

When encountering incomplete type errors with `RefPtr<T>` or `WeakPtr<T>` as class members:

**DO NOT** simply add the full include to the header file. Instead:
- Keep forward declaration in header: `class Animator;`
- Declare special member functions in header (without `= default`):
  ```cpp
  AnimatableColor();  // Declaration only
  ~AnimatableColor();  // Declaration only
  AnimatableColor(const AnimatableColor& color);  // Declaration only
  ```
- Implement them in .cpp file with `= default`:
  ```cpp
  // animatable_color.cpp
  #include "core/animation/animator.h"  // Full definition here
  AnimatableColor::AnimatableColor() = default;
  AnimatableColor::~AnimatableColor() = default;
  AnimatableColor::AnimatableColor(const AnimatableColor& color) = default;
  ```

**See**: `references/forward-declaration-refptr-member.md` for detailed solution

### Pattern 3: Redefinition Errors

**Error signature:**
```
error: redefinition of 'symbol_name'
```

**Common causes:**
1. Multiple definitions across translation units
2. Missing inline/constexpr for header-only definitions
3. ODR violations

## Historical Cases

All cases are organized by problem type in `references/` directory.

### Case 1: Undefined Symbol - Missing .cpp Files

**Location**: `references/undefined-symbol-missing-cpp.md`

**Error signature**:
```
ld.lld: error: undefined symbol: OHOS::Ace::TextTheme::Builder::Build
ld.lld: error: undefined symbol: OHOS::Ace::AdvancedTextStyle::GetGradient
```

**Common causes**:
- New .cpp files created but not added to BUILD.gn
- Files added to component BUILD.gn but not to source_set
- libace.z.so only links ace_core_ng libraries

**Solution**: Add .cpp to both component BUILD.gn AND frameworks/core/BUILD.gn xx_ng_source_set

### Case 2: Symbol Export - ACE_FORCE_EXPORT Missing

**Location**: `references/symbol-export-ace-force-export.md`

**Error signature**:
```
ld.lld: error: undefined symbol: OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin
>>> referenced by dialog_button.cpp (timepicker module)
```

**Common causes**:
- Symbol used by other modules but not marked for export
- ACE_FORCE_EXPORT missing from header declaration

**Solution**: Add ACE_FORCE_EXPORT to header declaration and add to build/libace.map

### Case 3: Symbol Export - libace.map Whitelist

**Location**: `references/symbol-export-libace-map.md`

**Error signature**:
```
ld.lld: error: undefined symbol: OHOS::Ace::NG::ClassName::MethodName
```

**Context**: Symbol has ACE_FORCE_EXPORT but still not exported

**Common causes**:
- Symbol not in build/libace.map whitelist
- Incorrect symbol format in version script

**Solution**: Add symbol to build/libace.map with correct format: `OHOS::Ace::NG::ClassName::MethodName*;`

### Case 4: Redefinition - inline constexpr

**Location**: `references/redefinition-error-constexpr.md`

**Error signature**:
```
error: redefinition of 'DRAG_BACKGROUND_OPACITY'
error: redefinition of 'URL_DISA_OPACITY'
```

**Common causes**:
- Constant defined in both header (inline constexpr) and .cpp
- ODR (One Definition Rule) violation

**Solution**: Remove duplicate definition from .cpp, keep only `inline constexpr` in header

### Case 5: Build System - ace_core_ng_source_set

**Location**: `references/build-system-ace-core-ng-source-set.md`

**Error signature**:
```
ld.lld: error: undefined symbol
```

**Context**: File exists in component BUILD.gn but symbol still undefined

**Common causes**:
- File not in frameworks/core/BUILD.gn ace_core_ng_source_set
- libace.z.so only links ace_core_ng libraries

**Solution**: Add file to ace_core_ng_source_set template in frameworks/core/BUILD.gn

### Case 6: RefPtr<T> Member - Forward Declaration Optimization

**Location**: `references/forward-declaration-refptr-member.md`

**Error signature**:
```
error: member access into incomplete type 'OHOS::Ace::Animator'
    rawPtr_->IncRefCount();
note: in instantiation of member function 'OHOS::Ace::RefPtr<OHOS::Ace::Animator>::RefPtr'
```

**Context**: `RefPtr<Animator>` or `WeakPtr<T>` used as class member variable

**Common causes**:
- Special member functions (constructor/destructor/copy constructor) defined with `= default` in header
- Compiler instantiates these functions in header, requiring complete type definition
- Common mistake: reverting forward declaration and adding full include

**Correct Solution**: DO NOT revert forward declaration! Use implementation separation:
1. Keep forward declaration in header: `class Animator;`
2. Declare special member functions in header (without `= default`)
3. Implement them in .cpp file with `= default`
4. Include full definition in .cpp file

**Benefits**: Reduced header dependencies, faster compilation (57% improvement in example)

### Case 7: Test Linking - Missing Source Files

**Location**: `references/test-missing-source-files.md`

**Error signature**:
```
ld.lld: error: undefined symbol: OHOS::Ace::ClassName::MethodName(...)
>>> referenced by test_file.cpp:123
```

**Context**: Linking test executable (e.g., `xxx_unittest`)

**Common causes**:
- Test BUILD.gn missing required .cpp files in sources
- Header optimization moved implementations to .cpp (e.g., StringUtils, LogWrapper)
- New implementation files not added to build system

**Common missing files**:
- `log_wrapper.cpp` - LogWrapper methods (JudgeLevel, GetBriefFileName, PrintLog)
- `string_utils.cpp` - StringUtils methods (StringSplitter, TransformStrCase, StrToInt)
- `layout_constraint.cpp` - LayoutConstraintT template methods
- `measure_property.cpp` - PaddingPropertyF, MeasureProperty methods

**Solution**: Add missing .cpp files to appropriate sources based on test template type:
- **ohos_unittest without ace_base**: Add to test's sources
- **ohos_unittest with ace_base**: Add to ace_base source_set
- **ace_unittest**: Add to ace_base source_set (default dependency)

**⚠️ Critical**: Only add source files, do NOT modify cflags/configs/defines

### Case 8: Struct RefPtr Member - Helper Method Pattern

**Location**: `references/forward-declaration-struct-helper-method.md`

**Error signature**:
```
error: member access into incomplete type 'OHOS::Ace::PixelMap'
    shadowInfo.pixelMap->GetPixelMapSharedPtr()
                         ^
note: forward declaration of 'OHOS::Ace::PixelMap'
class PixelMap;
```

**Context**: Pure data structure (POD struct) contains `RefPtr<T>` member and needs `->` access

**Common causes**:
- Struct contains `RefPtr<T>` member variable
- Code needs to call `->` operator on the smart pointer
- Direct call to `pixelMap->Method()` triggers incomplete type error
- Cannot use Case 6 approach because struct has no its own .cpp file

**Root Cause**:
- `RefPtr<T>::operator->()` returns `LifeCycleCheckable::PtrHolder<T>`
- `PtrHolder` constructor/destructor needs complete type definition to access `usingCount_`
- Pure data structures don't have their own implementation file

**Solution**: Add helper method to encapsulate type access:
1. Declare helper method in struct: `std::shared_ptr<::OHOS::Media::PixelMap> GetPixelMapSharedPtr() const;`
2. Create new implementation file (e.g., `interaction_data.cpp`)
3. Implement helper method in .cpp with full include: `#include "base/image/pixel_map.h"`
4. Update usage to call helper method instead of direct `->` access
5. Add new .cpp to BUILD.gn source set

**Advanced Scenario** (when helper method is not enough):
- Struct has its own .cpp file and is used by `std::vector`
- `std::vector::operator=` triggers copy, needs complete type
- Solution: Upgrade to full forward declaration optimization (similar to Case 6)
- See `forward-declaration-struct-helper-method.md` - "Advanced Scenario" section

**Key Points**:
- Use fully-qualified name `::OHOS::Media::PixelMap` to avoid namespace confusion
- Keep forward declaration in header, full definition only in .cpp

### Case 9: Namespace Type Resolution - Missing Qualifier

**Location**: `references/namespace-ambiguous-type-resolution.md`

**Error signature**:
```
error: no member named 'DragEvent' in namespace 'OHOS::Ace'
using OnDragStartFunc = std::function<DragDropBaseInfo(const RefPtr<OHOS::Ace::DragEvent>&, const std::string&)>;
                                      ~~~~~~~~~~~~~^
```

**Context**: Type defined in parent namespace, used in child namespace

**Common causes**:
- Type `DragEvent` defined in `OHOS::Ace` namespace
- Using code in `OHOS::Ace::NG` child namespace
- git diff shows **deletion** of namespace prefix (e.g., `- OHOS::Ace::DragEvent`)
- Someone removed the fully-qualified namespace prefix

**Root Cause**:
- Type is defined in parent namespace (e.g., `OHOS::Ace::DragEvent`)
- Used in child namespace (e.g., `OHOS::Ace::NG`)
- Deleting the namespace prefix causes compiler to search in wrong namespace
- Forward declaration in wrong namespace doesn't help

**Correct Solutions** (in priority order):

1. **Preserve full namespace qualifier** (RECOMMENDED):
   ```cpp
   // In OHOS::Ace::NG namespace
   using OnDragStartFunc = std::function<DragDropBaseInfo(
       const RefPtr<OHOS::Ace::DragEvent>&,  // ✅ Keep full namespace
       const std::string&)>;
   ```

2. **Add forward declaration in correct namespace**:
   ```cpp
   // In header, before OHOS::Ace::NG namespace
   namespace OHOS::Ace {
       class DragEvent;  // ✅ Forward declare in correct namespace
   }

   // In OHOS::Ace::NG namespace
   using OnDragStartFunc = std::function<DragDropBaseInfo(
       const RefPtr<OHOS::Ace::DragEvent>&,  // Still need full namespace
       const std::string&)>;
   ```

3. **Add header dependency** (when complete type needed):
   ```cpp
   #include "core/components_ng/event/drag_event.h"

   // In OHOS::Ace::NG namespace
   using OnDragStartFunc = std::function<DragDropBaseInfo(
       const RefPtr<OHOS::Ace::DragEvent>&,  // Still use full namespace
       const std::string&)>;
   ```

**⚠️ Critical**:
- NEVER delete namespace prefixes
- Forward declarations MUST be in the same namespace as type definition
- If type is in `OHOS::Ace`, forward declaration must also be in `OHOS::Ace`
- Using code can be in child namespace, but must reference parent namespace

**Key Points**:
- Find complete type definition (not just forward declarations)
- Match forward declaration namespace to type definition namespace
- Prefer keeping fully-qualified names over adding includes
- Helper method encapsulates complete type access
- Reduces header dependencies while maintaining clean API

**When to use**:
- ✅ Pure data structures (POD struct) with smart pointer members
- ✅ Need to dereference smart pointer with `->` or `*`
- ✅ Cannot add .cpp to existing struct
- ❌ Classes with their own .cpp file (use Case 6 instead)
- ❌ Only need constructor/destructor (use Case 6 instead)

### Case 9: LTO Virtual Thunk - libace.map Export

**Location**: `references/lto-virtual-thunk-libace-map-export.md`

**Error signature**:
```
ld.lld: error: undefined symbol: virtual thunk to OHOS::Ace::TouchEventTarget::~TouchEventTarget()
>>> referenced by ld-temp.o
>>>               lto.tmp:(construction vtable for OHOS::Ace::TouchEventTarget-in-OHOS::Ace::V2::ListScrollBarController)
>>> referenced by ld-temp.o
>>>               lto.tmp:(construction vtable for OHOS::Ace::TouchEventTarget-in-OHOS::Ace::VerticalDragRecognizer)
```

**Context**: Class with virtual functions used as base class, destructor declared in header and implemented in .cpp (forward declaration optimization), LTO (Link Time Optimization) enabled

**Common causes**:
- Class has virtual functions and is used as base class
- Forward declaration optimization: destructor in .cpp file (not inline)
- LTO creates virtual thunks for derived classes
- Virtual thunk symbols not exported from library

**Root Cause**:
- LTO optimizes virtual function tables during linking
- Creates **virtual thunk** symbols to adjust this pointer for derived classes
- These virtual thunk symbols must be available at link time
- If destructor not inline, LTO-generated virtual thunk may not be exported
- Common mistake: reverting to inline destructor (`= default` in header)

**Solution**: Keep forward declaration optimization, add libace.map exports:
1. **Keep destructor in .cpp file**: `~TouchEventTarget() override;` in header, implementation in .cpp
2. **Add to libace.map**:
   - `OHOS::Ace::TouchEventTarget::*;` - Export all class symbols
   - `virtual?thunk?to?OHOS::Ace::TouchEventTarget::*;` - Export LTO virtual thunks
3. **DO NOT revert** to inline definition in header

**Key Points**:
- Two export patterns required: `ClassName::*;` AND `virtual?thunk?to::ClassName::*;`
- Wildcard `*` matches all methods including virtual thunks
- Maintains forward declaration optimization
- No need to sacrifice header optimization for LTO

**Why This Works**:
1. **Compilation phase**: Header uses forward declaration, .cpp has implementation
2. **LTO link phase**: LTO optimizes vtables, creates virtual thunks
3. **Symbol export**: libace.maps patterns match virtual thunks, export to dynamic symbol table
4. **Runtime**: Derived class vtables can reference virtual thunks correctly

**When to use**:
- ✅ Classes with virtual functions used as base classes
- ✅ Using forward declaration optimization (destructor not inline)
- ✅ Linker errors: "undefined symbol: virtual thunk to ClassName::~ClassName()"
- ✅ Using LTO (Link Time Optimization)
- ❌ Classes not used as base classes (won't have virtual thunks)
- ❌ Destructor already inline in header (no optimization to maintain)
- ❌ Not using LTO (traditional compilation doesn't create virtual thunks)

**Common Mistakes**:
- ❌ Reverting to inline destructor (loses forward declaration optimization)
- ❌ Only exporting `ClassName::*;` without virtual thunk pattern
- ❌ Forgetting to add libace.map entry at all

### Case 10: MinGW - dllexport Declaration Mismatch

**Location**: `references/mingw-dllexport-declaration-mismatch.md`

**Error signature**:
```
error: redeclaration of 'OHOS::Ace::NG::PaddingPropertyT::SetEdges' cannot add 'dllexport' attribute
void PaddingPropertyT<T>::SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue)
                          ^
note: previous declaration is here
    void SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue);
         ^
```

**Context**: MinGW/Windows platform compilation only

**Key features**:
- Only occurs on MinGW/Windows builds (not Linux/MacOS)
- Error message: "redeclaration cannot add 'dllexport' attribute"
- Header declaration and .cpp implementation have inconsistent export attributes
- Usually triggered after adding `ACE_FORCE_EXPORT` to template methods

**Common causes**:
- Header file method declaration missing `ACE_FORCE_EXPORT`
- Implementation file has `ACE_FORCE_EXPORT` but header doesn't
- Only some overloaded methods have export attribute (inconsistent)
- MinGW requires strict consistency between declaration and definition

**Root Cause**:
- MinGW DLL export rules require declaration and definition export attributes to match exactly
- If header has no `__declspec(dllexport)` but implementation has it → compilation fails
- Unlike Linux/MacOS which are more lenient with visibility attributes

**Solution**: Add `ACE_FORCE_EXPORT` to ALL overloaded method declarations in header:
```cpp
// Header file - add to ALL declarations
ACE_FORCE_EXPORT void SetEdges(const T& padding);
ACE_FORCE_EXPORT void SetEdges(const T&, const T&, const T&, const T&);  // ✅ Don't forget
ACE_FORCE_EXPORT bool operator==(const PaddingPropertyT& value) const;
ACE_FORCE_EXPORT bool operator!=(const PaddingPropertyT& value) const;  // ✅ Don't forget
```

**Key Points**:
- Add to header file declarations (not just .cpp implementations)
- Ensure ALL overloaded methods are marked (don't miss any)
- Implementation file must also have `ACE_FORCE_EXPORT`
- Test on MinGW platform (Windows build)

**When to use**:
- ✅ MinGW/Windows compilation errors
- ✅ Error: "cannot add 'dllexport' attribute"
- ✅ Template methods with export attributes
- ❌ Linux/MacOS only (different rules)
- ❌ Link errors (this is a compilation error)

**Prevention checklist**:
1. ✅ Confirm need for export (cross-module usage)
2. ✅ Add `ACE_FORCE_EXPORT` to ALL header declarations
3. ✅ Add `ACE_FORCE_EXPORT` to ALL .cpp definitions
4. ✅ Check all overloaded versions (don't miss any)
5. ✅ Test compilation on MinGW platform

### Case 11: std::function<RefPtr<T>> Forward Declaration

**Location**: `references/case-std-function-refptr-forward-declaration.md`

**Error signature**:
```
error: no member named 'DragEvent' in namespace 'OHOS::Ace'
using OnDragStartFunc = std::function<DragDropBaseInfo(const RefPtr<OHOS::Ace::DragEvent>&, const std::string&)>;
                                                                    ~~~~~~~~~~~^
```

**Context**: `std::function` template using `RefPtr<T>` as parameter type

**Key features**:
- `RefPtr<T>` is a pointer wrapper with fixed size
- `using` alias does NOT immediately instantiate template
- Forward declaration works because RefPtr<T> size is known
- Actual template instantiation happens in .cpp file

**Common causes**:
- Misconception that `std::function` requires complete type definition
- Not understanding when template instantiation actually occurs
- Confusing type alias declaration with template instantiation

**Root Cause**:
- `RefPtr<T>` has fixed size (pointer size), so forward declaration works
- `using OnDragStartFunc = ...` is just a type alias, not instantiation
- Template instantiation only happens when the type is actually used in .cpp

**Solution**: Use forward declaration in header, full definition in .cpp:
```cpp
// Header file (gesture_event_hub.h)
namespace OHOS::Ace {
class DragEvent;  // ✅ Forward declaration only
}

namespace OHOS::Ace::NG {
// Type alias - NO template instantiation here
using OnDragStartFunc = std::function<DragDropBaseInfo(
    const RefPtr<OHOS::Ace::DragEvent>&,  // ✅ Works with forward decl
    const std::string&)>;
}

// Implementation file (gesture_event_hub.cpp)
#include "core/gestures/drag_event.h"  // ✅ Full definition here

// Actual usage - template instantiation happens here
OnDragStartFunc callback = ...;
```

**Key Principles**:
- RefPtr<T> is just a pointer wrapper (fixed size)
- using alias ≠ template instantiation
- Instantiation happens in .cpp when actually used
- Header: forward declaration sufficient
- Implementation: full definition required

**When to use**:
- ✅ `std::function<RefPtr<T>>` in header (type alias)
- ✅ `std::vector<RefPtr<T>>` in header (no instantiation)
- ✅ Function declarations returning/taking RefPtr<T>
- ❌ Accessing T members in header (needs full definition)
- ❌ Inline methods using T members (needs full definition)

**Comparison with Related Cases**:
- **Case 6**: RefPtr<T> as class member → ✅ Forward declaration works
- **Case 8**: RefPtr<T> in struct with → access → ⚠️ Needs helper method
- **Case 11**: std::function<RefPtr<T>> → ✅ Forward declaration works (this case)

**Benefits**:
- Reduced header dependencies
- Faster compilation
- Cleaner namespace boundaries
- Preserves optimization work

**Real-World Example**: OpenHarmony ACE Engine - `gesture_event_hub.h` optimization successfully uses forward declaration with `std::function<RefPtr<OHOS::Ace::DragEvent>>`

## Analysis Commands

### Check Symbol Existence

```bash
# Search for symbol definition in codebase
grep -r "SymbolName" --include="*.h" --include="*.cpp" frameworks/

# Check if .cpp file exists
find frameworks/ -name "implementation_file.cpp"
```

### Verify Build Configuration

```bash
# Check if file in BUILD.gn
grep -r "implementation_file.cpp" frameworks/*/BUILD.gn

# Check ace_core_ng source set
grep -A 100 "ace_core_ng_source_set" frameworks/core/BUILD.gn | grep "implementation_file.cpp"
```

### Check Symbol Export

```bash
# Check if symbol exported in shared library
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName

# Check libace.map
grep "SymbolName" build/libace.map
```

## Troubleshooting Guide

### For New .cpp Files

1. Create implementation file (.cpp)
2. Add to component's BUILD.gn
3. Add to frameworks/core/BUILD.gn ace_core_ng_source_set (if used by libace.z.so)
4. If symbol is cross-module used:
   - Add ACE_FORCE_EXPORT to header declaration
   - Add to build/libace.map whitelist

### For Header Optimization Issues

1. Check for forward declarations used incorrectly
2. Ensure complete types available where needed
3. Use inline constexpr for header-only constants
4. Avoid ODR violations

### For Link Errors

1. Identify missing symbol from error message
2. Find symbol definition location
3. Verify implementation is compiled (in BUILD.gn)
4. Check symbol visibility/export if cross-module
5. Verify linking order and dependencies

## Best Practices

### ⚠️ CRITICAL RULE - NEVER Clear LTO Cache or Suggest "Clean Build"

**⚠️ ABSOLUTE PROHIBITION - When encountering ANY build errors:**

**Rule Description**:
**NEVER, UNDER ANY CIRCUMSTANCES, suggest clearing LTO cache, deleting build directories, or performing a "clean build" as the first or primary solution.**

**What is STRICTLY FORBIDDEN**:
- ❌ **NEVER** suggest clearing `thinlto-cache` directory
- ❌ **NEVER** suggest clearing `llvmcache-*` directories
- ❌ **NEVER** suggest deleting `out/obj` directory
- ❌ **NEVER** suggest deleting entire `out/` directory
- ❌ **NEVER** suggest running `rm -rf out/`
- ❌ **NEVER** suggest "clean build" or "rebuild from scratch"
- ❌ **NEVER** blame LTO cache for linker errors
- ❌ **NEVER** say "this might be a cache issue, try clearing it"

**Why this is FORBIDDEN**:
1. **LTO cache issues are EXTREMELY RARE** - 99.9% of build errors are code/configuration issues, not cache problems
2. **Masking real problems** - Clearing cache temporarily hides issues without fixing root causes
3. **Wastes massive time** - Full rebuilds take hours; incremental builds take minutes
4. **Disables incremental compilation benefits** - Future builds become slower
5. **Breaks reproducibility** - Makes debugging harder by destroying build state
6. **Lazy diagnosis** - Suggesting cache clearing indicates insufficient error analysis

**Remember**: Real build errors have real causes. Find them, fix them. Don't blame the cache.

---

### 0. ⭐ HIGH PRIORITY RULE - Header File Missing Error Resolution

**⚠️ CRITICAL RULE - When encountering "file not found" or "no such file or directory" header errors:**

**Rule Description**:
When compilation fails due to missing header files, ALWAYS follow this priority order:

1. **PREFERRED Solution**: Add the missing header to the **.cpp file that has the error** (NOT the optimized header)
2. **LAST RESORT**: Only consider modifying optimized headers after user confirmation

**Why this rule?**:
- Header optimization work intentionally removes dependencies to improve build times
- Blindly adding back deleted dependencies undermines optimization efforts
- .cpp files are the correct place to add necessary includes that were removed from headers
- Maintains separation between interface (headers) and implementation (.cpp)

**How to Detect Optimized Headers**:

Before suggesting any header modifications, CHECK if the header file is in an optimization state:

```bash
# Check 1: Staged changes (暂存状态)
git status --porcelain | grep "^M.*\.h$"

# Check 2: Modified but not staged (修改状态)
git status --porcelain | grep "^ M.*\.h$"

# Check 3: Recent commit (最近一笔提交)
git log -1 --name-only --pretty=format:"" | grep "\.h$"

# Combined check - all three states:
git status --porcelain | grep "\.h$"  # Staged or modified
git diff HEAD~1 --name-only | grep "\.h$"  # Changed in last commit
```

**If the header is in ANY of these states**:
- ✅ **PREFERRED**: Add missing #include to the .cpp file with the error
- ❌ **DO NOT**: Suggest adding back the dependency to the optimized header
- ⚠️ **LAST RESORT**: If modifying the header is absolutely necessary, MUST ask user first

**When to add to .cpp file** (PREFERRED):
```cpp
// ✅ CORRECT - Add to the .cpp file with the compilation error
// frameworks/core/components_ng/pattern/search/search_gesture_event_hub.cpp
#include "core/events/click_event.h"  // Add missing header here

// ❌ WRONG - Do NOT add back to optimized headers
// frameworks/core/components_ng/event/click_event.h
// #include "core/pipeline/base/element.h"  // Don't restore deleted dependencies
```

**User Confirmation Template** (when header modification might be necessary):

```
⚠️ 检测到 [header_name.h] 可能正在被优化（状态：暂存/修改/最近提交）

编译错误：[error_message]
缺失头文件：[missing_header.h]
错误位置：[error_file.cpp:line]

建议方案：
✅ 方案1（推荐）：在 [error_file.cpp] 中添加 #include "[missing_header.h]"
   - 保持头文件优化成果
   - 不增加头文件依赖
   - 符合最佳实践

⚠️ 方案2（需确认）：在 [header_name.h] 中添加回 #include "[missing_header.h]"
   - 可能影响编译性能优化
   - 需要用户确认必要性

请确认是否使用方案1，或说明为何需要方案2？
```

**Examples of optimized headers (do NOT modify without confirmation)**:
- `animation_utils.h` - Animation utility functions
- `click_event.h` - Click event handling
- Any header in staged/modified state or recent commit

**Detection Workflow**:

**Step 1**: When encountering "file not found" error
```bash
# Extract the missing header path from error
# Example: error: 'core/pipeline/base/element.h' file not found
```

**Step 2**: Check if the referencing file is an optimized header
```bash
# Find where this error occurs
grep -r "#include.*element.h" frameworks/core/components_ng/event/click_event.h

# Check if click_event.h is being optimized
git status --porcelain | grep "click_event.h"
git log -1 --name-only | grep "click_event.h"
```

**Step 3**: Apply the appropriate solution
- If header is optimized → Add to .cpp file
- If header is NOT optimized → Can add to header
- If uncertain → Ask user with both options

**Verification steps**:
1. Check git status for staged/modified headers
2. Check last commit for header changes
3. Identify the .cpp file with the compilation error
4. Add the missing #include to that .cpp file (PREFERRED)
5. Verify the fix resolves the error
6. If header modification was necessary, document why

**Key Principles**:
- ✅ Preserve header optimization work
- ✅ Add missing includes to .cpp implementation files
- ✅ Maintain clean header dependencies
- ✅ Check git status before suggesting header modifications
- ❌ DO NOT blindly revert optimization efforts
- ❌ DO NOT suggest adding deleted dependencies back to headers without checking optimization state
- ❌ DO NOT modify headers in staged/modified/recent-commit state without user confirmation

**Related Skills**:
- **header-optimization**: For understanding header optimization patterns
- **compile-analysis**: For analyzing header dependencies
- **Case 6**: RefPtr<T> member forward declaration optimization

**Related Cases**:
- Header optimization work (see: header-optimization skill)
- Forward declaration patterns (Case 6: RefPtr<T> member optimization)
- Compilation error analysis (Pattern 2: Incomplete Type Errors)

### 1. ⭐ HIGH PRIORITY RULE - Type Namespace Confusion (PixelMap, etc.)

**⚠️ CRITICAL RULE - When encountering type mismatch errors with common class names:**

**Rule Description**:
When error messages show type mismatches for common class names (like PixelMap), ALWAYS verify you're using the correct namespace variant for the code location.

**Common Pitfall - PixelMap Namespace Confusion**:

In ACE Engine frameworks (`frameworks/core/components_ng/`, etc.):
- ✅ **CORRECT**: `OHOS::Ace::PixelMap` (wrapper class in `base/image/pixel_map.h`)
- ❌ **WRONG**: `OHOS::Media::PixelMap` (underlying media class)

**Why this happens**:
- `Ace::PixelMap` is a wrapper around `Media::PixelMap`
- Designed specifically for ACE Engine frameworks usage
- Located at: `base/image/pixel_map.h`
- IDE auto-complete might incorrectly suggest `Media::PixelMap`

**Solution Pattern**:

1. **Identify the error location**:
   - Check if file is in `frameworks/` directory
   - Verify it's using framework code patterns

2. **Use correct type**:
   ```cpp
   // ✅ CORRECT for frameworks/
   #include "base/image/pixel_map.h"
   RefPtr<PixelMap> pixelMap_;  // OHOS::Ace::PixelMap

   // ❌ WRONG in frameworks/
   #include "native_image/imageinfo.h"  // Don't include media headers
   RefPtr<Media::PixelMap> pixelMap_;  // Wrong namespace
   ```

3. **Fix all occurrences**:
   ```bash
   # Find wrong usage
   grep -rn "Media::PixelMap" frameworks/core/components_ng/

   # Replace with correct type
   # Media::PixelMap → PixelMap (or OHOS::Ace::PixelMap)
   ```

**When to apply this rule**:
- Error mentions type mismatch with common names (PixelMap, etc.)
- Error shows different namespaces for same type name
- File location is in `frameworks/` (not `interfaces/`)
- Virtual function override errors with return types

**DO NOT**:
- ❌ Assume `Media::PixelMap` is correct just because IDE suggests it
- ❌ Add `using Media::PixelMap;` to fix namespace issues
- ❌ Change base class to match derived class (change derived instead)
- ❌ Suggest using media API types in framework code

**Verification**:
1. Check include: `#include "base/image/pixel_map.h"` present
2. Verify usage: `RefPtr<PixelMap>` or `RefPtr<OHOS::Ace::PixelMap>`
3. No `Media::PixelMap` references in framework code
4. Virtual function return types match base class

**Related Patterns**:
- Similar issues can occur with other wrapper types
- Always check if there's an Ace wrapper before using media types
- Frameworks use Ace wrappers, interfaces might use media types

### 2. Build System Architecture

- **libace.z.so** only links ace_core_ng libraries
- Component-specific libraries are not linked to final产物
- New .cpp files used by libace.z.so must be in ace_core_ng_source_set

### 2. Symbol Export Rules ⭐

**⚠️ CRITICAL - RULES FOR NON-TEMPLATE CLASSES AND NON-TEMPLATE METHODS**:

When encountering "undefined symbol" linker errors for **non-template classes and non-template methods**, follow these rules in order:

**Rule 1: Check if class has ACE_FORCE_EXPORT**

First, check if the class definition has `ACE_FORCE_EXPORT`:

```cpp
// Case A: Class WITHOUT ACE_FORCE_EXPORT
class PaddingPropertyF {  // ← No export on class
    float Width() const;
};

// Case B: Class WITH ACE_FORCE_EXPORT
class ACE_FORCE_EXPORT PaddingPropertyF {  // ← Export on entire class
    float Width() const;
};
```

**Rule 2: Apply export based on class export status**

**Case A - Class WITHOUT ACE_FORCE_EXPORT**:
- ✅ **Add `ACE_FORCE_EXPORT` to method declaration in header** (PREFERRED)
- ❌ **DO NOT** add to method definition in .cpp
- Reason: Keeps export control at declaration level, supports fine-grained export control

```cpp
// ✅ CORRECT - Add to header declaration
// interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h
class PaddingPropertyF {
    ACE_FORCE_EXPORT float Width() const;  // ← Add here
    ACE_FORCE_EXPORT float Height() const; // ← Add here
};

// frameworks/core/components_ng/property/measure_property.cpp
// NO ACE_FORCE_EXPORT here
float PaddingPropertyF::Width() const { /* implementation */ }
```

**Case B - Class WITH ACE_FORCE_EXPORT**:
- ✅ **NO additional export needed** - class export covers all methods
- ❌ **DO NOT** add `ACE_FORCE_EXPORT` to individual methods
- Reason: Entire class is already exported

```cpp
// ✅ CORRECT - No individual method exports needed
class ACE_FORCE_EXPORT PaddingPropertyF {  // ← Entire class exported
    float Width() const;   // Automatically exported
    float Height() const;  // Automatically exported
};
```

**Rule 3: Add to libace.map with fine-grained symbol names** ⭐

**⚠️ CRITICAL: ALWAYS prefer fine-grained symbol export as the FIRST choice**

After applying Rule 1 and Rule 2, add the symbol to `build/libace.map`:

```cpp
// build/libace.map
{
  global:
    // ✅ FINE-GRAINED - Export specific methods (PREFERRED - ALWAYS TRY THIS FIRST)
    OHOS::Ace::PaddingPropertyF::Width*;
    OHOS::Ace::PaddingPropertyF::Height*;

    // ✅ FINE-GRAINED CONSTRUCTORS - Match all constructor overloads
    OHOS::Ace::VelocityTracker::VelocityTracker*;  // Matches both constructors

    // ⚠️ ACCEPTABLE - Export entire class (ONLY if fine-grained not feasible)
    OHOS::Ace::PaddingPropertyF::*;
};
```

**Fine-Grained Export Pattern Priority** (in order of preference):

1. **Method-level** (MOST PREFERRED):
   ```
   OHOS::Ace::ClassName::MethodName*;  # Single method
   ```

2. **Constructor-level** (CONSTRUCTORS):
   ```
   OHOS::Ace::ClassName::ClassName*;  # All constructor overloads
   ```

3. **Class-level** (LAST RESORT):
   ```
   OHOS::Ace::ClassName::*;  # All class members (use sparingly)
   ```

**Why fine-grained export?** ⭐
- ⭐ **Minimizes exported symbol surface** - Only what's needed
- ⭐ **Clearer API boundaries** - Explicit about public interface
- ⭐ **Reduces symbol conflicts** - Smaller surface = fewer conflicts
- ⭐ **Better dependency tracking** - Easy to see cross-module usage
- ⭐ **Improved security** - Limits exported attack surface
- ⭐ **Easier maintenance** - Clear which symbols are part of API contract

**Decision Tree**:

```
Linker Error: undefined symbol ClassName::MethodName
    ↓
Is ClassName a non-template class?
    YES → Is class declaration has ACE_FORCE_EXPORT?
        YES → ✅ Class already exported
              → Add ClassName::* to libace.map
              → DONE (no individual method exports needed)
        NO → ✅ Add ACE_FORCE_EXPORT to method declaration in .h
             → Add ClassName::MethodName* to libace.map
             → DONE
    NO → Use template export rules (see below)
```

**Comparison: Non-Template vs Template**

| Aspect | Non-Template Class/Method | Template Class/Method |
|--------|--------------------------|----------------------|
| **Export location** | Method declaration in .h (Rule 2) | Both declaration in .h AND definition in .cpp |
| **Class export** | Covers all methods if present | Individual methods still need export |
| **libace.map** | Fine-grained: `ClassName::MethodName*;` | Wildcard: `ClassName*;` or `TemplateFunction*;` |
| **Reference** | This section (Rule 2) | Pattern 1, Scenario 3 & 5 |

---

**⚠️ TEMPLATE-ONLY RULES (NOT for non-template)**:

For **template classes and template functions ONLY**, use different rules:

**Template functions** (Pattern 1, Scenario 3):
- Add `ACE_FORCE_EXPORT` to **BOTH** declaration in .h AND implementation in .cpp
- Add explicit instantiation in .cpp
- Use wildcard in libace.map: `void?ClassName::FunctionName*;`

**Template class methods** (Pattern 1, Scenario 5):
- Add `ACE_FORCE_EXPORT` to **EACH** method implementation in .cpp
- Class export alone is NOT sufficient
- Use wildcard in libace.map: `ClassName*;`

**DO NOT mix rules**:
- ❌ Do NOT use template rules for non-template classes
- ❌ Do NOT use non-template rules for template classes

### 3. Header Optimization

- Use `inline constexpr` for header-only constants
- Don't define in both header and .cpp
- Forward declarations reduce dependencies but ensure complete type visible at use

## ⭐ Key Principles - Symbol Export for Cross-Module Usage

**When encountering "undefined symbol" linker errors for methods used by other dynamic libraries**:

### ⚠️ IMPORTANT: Distinguish Between Non-Template and Template

**Before applying any export rules, FIRST determine the type**:

```
Linker Error: undefined symbol
    ↓
Is it a non-template class method?
    → YES: Use Non-Template Rules (below)
    → NO: Use Template Rules (Pattern 1, Scenario 3 & 5)
```

### Non-Template Class Methods: Export at Declaration ⭐

**✅ PREFERRED for Non-Template** - Add `ACE_FORCE_EXPORT` to method declaration in header (.h):

```cpp
// interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h
class PaddingPropertyF {
    ACE_FORCE_EXPORT float Width() const;   // ← Add here (PREFERRED)
    ACE_FORCE_EXPORT float Height() const;  // ← Add here (PREFERRED)
};

// frameworks/core/components_ng/property/measure_property.cpp
// NO ACE_FORCE_EXPORT here for non-template methods
float PaddingPropertyF::Width() const
{
    return left.value_or(0.0f) + right.value_or(0.0f);
}
```

**Why this approach for non-templates?**
1. **Fine-grained export control** - Export only needed methods
2. **Clear API boundaries** - Declaration shows what's exported
3. **Works with libace.map fine-grained rules** - Export specific symbols
4. **Consistent with class export semantics** - If class has export, no need for individual exports

**⚠️ CRITICAL: Check Class Export Status First**

```cpp
// Case A: Class WITHOUT export → Add to individual method declarations
class PaddingPropertyF {
    ACE_FORCE_EXPORT float Width() const;  // ← Required
};

// Case B: Class WITH export → No individual exports needed
class ACE_FORCE_EXPORT PaddingPropertyF {  // ← Entire class exported
    float Width() const;  // Automatically exported, no ACE_FORCE_EXPORT needed
};
```

**❌ DO NOT for Non-Template**:
- ❌ Add `ACE_FORCE_EXPORT` to method definition in .cpp (unless template)
- ❌ Add individual method exports if class already has `ACE_FORCE_EXPORT`
- ❌ Use template export rules for non-template code

### Template-Only: Different Rules Apply ⚠️

**For template classes and template functions, use DIFFERENT rules** (see Pattern 1, Scenarios 3 & 5):

| Rule Type | Non-Template | Template |
|-----------|--------------|----------|
| **Export location** | Method declaration in .h | BOTH declaration in .h AND definition in .cpp |
| **Class export sufficient?** | YES (covers all methods) | NO (individual methods need export) |
| **libace.map pattern** | Fine-grained: `ClassName::MethodName*;` | Wildcard: `ClassName*;` |
| **Reference** | This section | Pattern 1, Scenarios 3 & 5 |

### When to Use Each Approach

| Scenario | Recommended Location | Example |
|----------|---------------------|---------|
| **Non-template class method** | **Method declaration in .h** | `PaddingPropertyF::Width()` |
| **Template class method** | **Both** declaration in .h AND implementation in .cpp | `LayoutConstraintT<T>::UpdateMaxSizeWithCheck()` |
| **Template function** | **Both** declaration in .h AND implementation in .cpp | `StringUtils::StringSplitter<T>` |
| **Free function (non-template)** | **Method declaration in .h** | `StringUtils::TransformStrCase<std::string>` |
| **Class with export already** | **None needed** | All methods auto-exported |

### Real-World Success Cases

1. **Non-Template Methods** (PaddingPropertyF):
   - Added `ACE_FORCE_EXPORT` to method declarations in .h
   - No modifications to .cpp file
   - Fine-grained libace.map entries: `OHOS::Ace::PaddingPropertyF::Width*;`

2. **Template Class Methods** (LayoutConstraintT):
   - Added `ACE_FORCE_EXPORT` to each method implementation in .cpp
   - Class export alone NOT sufficient for templates
   - Wildcard pattern in libace.map: `OHOS::Ace::NG::LayoutConstraintT*;`

3. **Template Functions** (StringUtils):
   - Added `ACE_FORCE_EXPORT` to both declaration in .h AND implementation in .cpp
   - Explicit instantiation in .cpp
   - Wildcard pattern in libace.map: `void?OHOS::Ace::StringUtils::StringSplitter*;`

**Remember**: When fixing linker errors for symbols needed by other modules, **try the .cpp implementation approach first** before modifying headers.

### 4. Template Explicit Instantiation ⭐

**For template classes with explicit instantiation**:

**Issue**: `PaddingPropertyT<CalcLength>` symbols not exported, but `PaddingPropertyT<Dimension>` works

**Root Cause**: When a type is used as **template parameter for explicit instantiation**, the type itself must have export attribute

**Key Principle**:
```
Template Type Visibility (CalcLength)
    ↓
Template Specialization (PaddingPropertyT<CalcLength>)
    ↓
Symbol Export Success/Failure
```

- If `CalcLength` has no export → Template specialization inherits internal visibility
- If `CalcLength` has `ACE_FORCE_EXPORT` → Template specialization can export

**Solution**:
```cpp
// ❌ BEFORE - Type missing export (fails when used as template parameter)
class CalcLength {
    std::string ToString() const { /* inline */ }
};

// ✅ AFTER - Add type-level export (required for template parameters)
class ACE_FORCE_EXPORT CalcLength {  // ← Required when used as template type
    std::string ToString() const { /* inline - keep in header */ }
};
```

**Critical Rules**:
1. **Type used as template parameter MUST have export** (if type has inline methods)
2. **DO NOT move inline methods to .cpp** - keep header optimization
3. Template methods still need `ACE_FORCE_EXPORT` in .cpp
4. Explicit instantiation in .cpp required

**When Type-Level Export is Required**:
- ✅ Type has inline methods (ToString, operator==, etc.)
- ✅ Type is used as template parameter for explicit instantiation
- ✅ Template instantiation symbols need to be exported to other modules

**Reference**: See `references/template-instantiation-type-export.md` for detailed case study

**⚠️ IMPORTANT - Header Optimization**:
- StringUtils refactoring (commit e0fd3724d21) moved ~650 lines from header to .cpp
- This is **strategic work** to improve build times
- **DO NOT revert** by moving inline methods to .cpp
- **Add type-level exports** to solve template parameter export issues

## Verification Steps

**After user applies the recommended fixes**, suggest these verification commands:

```bash
# 1. Navigate to OpenHarmony root directory and rebuild
cd <openharmony_root>
./build.sh --product-name rk3568 --build-target ace_engine --ccache

# 2. Check for link errors in out/<product>/build.log
grep "ld.lld: error:" out/rk3568/build.log | wc -l

# 3. Verify symbol export (if applicable)
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName

# 4. Extract and check new errors from out/<product>/build.log
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

# 5. Read the extracted errors:
cat out/rk3568/last_error.log

# For SDK builds (⚠️ use out/sdk/ directory):
# 1. Build SDK: ./build.sh --product-name ohos-sdk --ccache
# 2. Check errors: grep "error:" out/sdk/build.log | tail -50
# 3. Extract errors: foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/sdk/build.log
# 4. Read errors: cat out/sdk/last_error.log
```

**Note**: These are suggestions for the user to run manually. Do not execute build commands automatically.

## Adding New Cases

When solving new build errors:

1. Document the error in `examples/<case-name>.md`
2. Include:
   - Error signature
   - Root cause
   - Solution steps
   - Files modified
   - Verification commands
3. Update this SKILL.md to reference the new case
4. Add patterns to "Error Patterns and Solutions" section

## Example Usage

### Example 1: Successful Build (NO ERRORS)

```
User: "帮我分析一下构建错误"
Assistant: "I'll analyze the build errors from the OpenHarmony output directory.

⚠️ FIRST, I'll extract the latest errors from build.log:

[STEP 1 - NAVIGATE TO ROOT]
cd <openharmony_root>

[STEP 2 - EXTRACTION - MANDATORY]
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

Output:
Extracted latest error block (24 bytes) from out/rk3568/build.log
→ Saved to out/rk3568/last_error.log

[STEP 3 - READ EXTRACTED ERRORS]
Reading out/rk3568/last_error.log...

Content:
build success, no error

[STEP 4 - CHECK FOR SUCCESS]
✅ Build is successful! No errors found.

## ✅ 构建成功

最新的构建已经成功完成，没有发现任何错误。

**构建状态**: 成功
**错误信息**: 无

建议: 您可以继续进行开发或测试工作。

[STOP - DO NOT read other log files like error.log]"
```

### Example 2: Build with Errors

```
User: "帮我分析一下构建错误"
Assistant: "I'll analyze the build errors from the OpenHarmony output directory.

⚠️ FIRST, I'll extract the latest errors from build.log:

[STEP 1 - NAVIGATE TO ROOT]
cd <openharmony_root>

[STEP 2 - EXTRACTION - MANDATORY]
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

Output:
Extracted latest error block (12345 bytes) from out/rk3568/build.log
→ Saved to out/rk3568/last_error.log

[STEP 3 - READ EXTRACTED ERRORS]
Reading out/rk3568/last_error.log...

[STEP 4 - CATEGORIZE]
Identified as: compilation error - undeclared identifier

[STEP 5 - MATCH PATTERNS]
Checking references/ directory for similar patterns...
Found match: references/undefined-symbol-missing-cpp.md

[STEP 6 - PROVIDE RECOMMENDATIONS]
Providing detailed fix recommendations (NOT modifying files)

## 构建错误分析

### 错误类型
编译错误 - 未声明的标识符

### 错误位置
frameworks/core/event/touch_event.cpp:25

### 根本原因
函数被删除但调用点未移除：TouchPoint::CovertId() 已删除，但头文件中仍有声明且多处调用

### 修复建议

**选项1: 恢复函数实现** (推荐)

在 frameworks/core/event/touch_event.cpp 中恢复函数：

**当前代码**: (函数已删除)

**应添加**:
```cpp
void TouchPoint::CovertId()
{
    if (sourceTool == SourceTool::PEN) {
        originalId = TOUCH_TOOL_BASE_ID + static_cast<int32_t>(sourceTool);
        id = id + originalId;
    }
}
```

**选项2: 完全移除函数**

需要修改以下文件：
1. 删除头文件声明: interfaces/inner_api/ace_kit/include/ui/event/touch_event.h:59
2. 移除调用点: adapter/ohos/entrance/mmi_event_convertor.cpp:240
3. 移除测试用例: test/unittest/core/event/touch_event_test_ng.cpp:668

### 验证步骤
1. 重新编译: ./build.sh --product-name rk3568 --build-target ace_engine
2. 重新提取错误: foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log
3. 检查结果: cat out/rk3568/last_error.log

[NOTE: Only providing recommendations, NOT modifying files]"
```

**Key Points**:
- ⚠️ **ALWAYS navigate to root first** → `cd <openharmony_root>` before running extraction script
- ⚠️ **ALWAYS extract first** → use script on `out/<product>/build.log` with correct relative path from root
- ✅ **THEN read** → analyze only from `out/<product>/last_error.log`
- ❌ **NEVER read** → `build.log` directly or other log files
- ✅ **Check for success** → if `last_error.log` shows "build success", STOP and report
- ❌ **NEVER read other logs** → DO NOT read `error.log`, `build_output*.log`, `error.*.log`, etc.
- ✅ **Use correct script path** → `foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/` (from OpenHarmony root)
- ✅ **Provide recommendations ONLY** → do NOT automatically modify code

## Version History

- **0.14.0** (2026-02-10): Non-Template Symbol Export Rules
  - ⚠️ **重要修改**：区分非模板类和模板类的符号导出规则
  - 📋 **非模板类规则**：优先在方法声明处（.h 文件）增加 ACE_FORCE_EXPORT
  - 🔍 **类导出检查**：如果 class 已有 ACE_FORCE_EXPORT，则无需额外导出方法
  - 🎯 **精细化导出**：libace.map 中优先使用细粒度符号名（ClassName::MethodName*）
  - 📊 **决策树**：添加非模板 vs 模板的决策流程图
  - 🔧 **对比表格**：非模板与模板导出规则的清晰对比
  - ✅ **更新位置**：
    - Best Practices 部分："### 2. Symbol Export Rules ⭐"
    - Key Principles 部分："## ⭐ Key Principles - Symbol Export for Cross-Module Usage"
    - Pattern 1 Scenario 2：更新为基于类导出状态的决策流程
  - 🚫 **禁止事项**：非模板方法不要在 .cpp 中添加 ACE_FORCE_EXPORT
  - 💡 **核心理念**：非模板支持精细化导出控制，模板需要宽泛通配符

- **0.13.0** (2026-02-10): CRITICAL RULE - Never Clear LTO Cache
  - ⚠️ **关键修改**：绝对禁止建议清理 LTO cache 或删除构建目录
  - 📋 在 Behavior Guidelines 部分添加 "CRITICAL - NEVER SUGGEST CLEARING LTO CACHE" 子部分
  - 🚨 在 Best Practices 部分添加全新的 "CRITICAL RULE - NEVER Clear LTO Cache" 高优先级规则
  - 💡 强调 LTO cache 问题极其罕见（99.9% 的情况都不是缓存问题）
  - ⏱️ 说明清理缓存会浪费大量时间（完整重建需要数小时，增量编译只需数分钟）
  - 🎯 明确要求必须分析真实错误并修复根本原因，而不是怪罪缓存
  - 📝 加强 Pattern 1 Common mistakes 部分的相关说明
  - ⛔ 仅在极端罕见情况下（用户明确修改了编译器标志等）才考虑缓存问题
  - ✅ 即使在那些情况下，也必须先询问用户并记录具体原因

- **0.12.0** (2026-02-10): Case 11 - std::function<RefPtr<T>> Forward Declaration
  - ✨ 新增 Case 11：std::function<RefPtr<T>> 前向声明成功案例
  - 📝 新增案例分析文档：`case-std-function-refptr-forward-declaration.md`
  - 🎯 核心观点：using 别名不立即实例化模板，RefPtr<T> 大小固定
  - 💡 关键发现：模板实例化延迟到 .cpp 实际使用时
  - 📊 对比表格：Case 6/8/11 的 RefPtr<T> 前向声明使用场景
  - 🔧 纠正错误理解：std::function 不需要完整类型定义
  - ✅ 实战案例：OpenHarmony gesture_event_hub.h 优化成功应用
  - 🛡️ 验证原则：RefPtr<> 本质是指针包装器，前向声明可行

- **0.11.0** (2026-02-09): High Priority Rule - Header Optimization Protection
  - ⭐ 新增高优先级规则：处理头文件缺失错误时的优先级顺序
  - 🔍 新增优化检测方法：通过 git status 检测暂存/修改/最近提交状态
  - ✅ 优先方案：在出错的 .cpp 文件中添加缺失头文件（推荐）
  - ⚠️ 最后手段：仅在用户确认后才修改已优化的头文件
  - 📝 新增用户确认模板：清晰展示两个方案供用户选择
  - 🔧 新增检测工作流：三步检测并应用正确的解决方案
  - 🛡️ 保护头文件优化成果：避免盲目回退已删除的依赖
  - 🔗 关联 header-optimization 和 compile-analysis skills

- **0.10.0** (2026-02-06): Case 8 Advanced Scenario - Struct with Own .cpp File
  - ✨ 新增 Case 8 进阶场景：当辅助方法模式不够时的完整解决方案
  - 📝 在 `forward-declaration-struct-helper-method.md` 中添加 Advanced Scenario
  - 🎯 应用场景：结构体有 .cpp 文件，被 std::vector 使用，需要保持聚合初始化
  - 💡 关键技术：升级为完整的前向声明优化（类似 Case 6），同时保留辅助方法
  - 🔧 决策树：指导何时使用标准方案 vs 完整方案
  - 📊 对比表格：标准方案（无 .cpp）vs Advanced Scenario（有 .cpp）
  - ⚠️ 渐进式升级：从辅助方法模式开始，遇到 vector 拷贝问题时升级
  - 🔗 关联 Case 6 和 Case 7：完整的 RefPtr 成员优化知识体系

- **0.9.0** (2026-02-04): LTO Virtual Thunk Export Solution
  - ✨ 新增 LTO Virtual Thunk 导出案例分析：`lto-virtual-thunk-libace-map-export.md`
  - 📝 新增 Case 9：基类虚函数 + LTO 的 libace.map 导出解决方案
  - 🎯 核心观点：保持前向声明优化，不要回退到 inline 定义
  - 💡 关键技术：在 libace.map 中同时导出 `ClassName::*;` 和 `virtual?thunk?to::ClassName::*;`
  - 🔧 LTO 工作原理：链接时创建 virtual thunk 调整 this 指针
  - 📊 符号导出模式：通配符 `*` 匹配所有方法和 virtual thunk
  - ⚠️ 常见错误：只导出类符号而忘记导出 virtual thunk

- **0.8.0** (2026-02-04): Struct RefPtr Member Optimization
  - ✨ 新增结构体智能指针成员优化案例分析：`forward-declaration-struct-helper-method.md`
  - 📝 新增 Case 8：纯数据结构中 RefPtr 成员的辅助方法模式
  - 🎯 与 Case 6 的区别：Case 6 适用于有自己 .cpp 的类，Case 8 适用于纯数据结构
  - 💡 关键技术：使用辅助方法封装完整类型访问，保持头文件前向声明优化
  - 🔧 完全限定名 `::OHOS::Media::PixelMap` 避免命名空间混淆
  - 📊 编译性能优化：减少头文件依赖，降低重编译范围

- **0.7.0** (2026-02-02): Test Linking Error Support
  - ✨ 新增测试链接错误案例分析：`test-missing-source-files.md`
  - 📝 新增 Case 7：测试中缺失源文件的通用解决方案
  - 🎯 泛化案例场景，不仅限于 LogWrapper，涵盖所有缺失源文件情况
  - 📋 列出常见缺失源文件：log_wrapper.cpp、string_utils.cpp、layout_constraint.cpp 等
  - ⚠️ 强调只添加源文件，不修改 cflags/configs/defines
  - 🌳 添加决策树帮助判断正确的解决方案

- **0.6.0** (2025-02-02): 新增 SDK 编译错误分析支持
  - ✨ 添加 SDK 错误触发关键词："分析SDK的编译错误"、"analyze SDK build errors"、"check SDK errors"
  - ⚠️ 特别说明：SDK 日志路径为 `out/sdk/build.log` 和 `out/sdk/last_error.log`（特殊目录）
  - 📝 更新所有路径示例，标注 SDK 的特殊目录结构
  - 🔧 优化错误提取命令，支持 SDK 路径

- **0.5.0** (2026-01-27): 模板类方法导出支持
- **0.4.0** (2026-01-27): 模板实例化类型导出支持
- **0.3.0** (2026-01-27): 符号导出最佳实践
- **0.2.0** (2026-01-27): 添加重定义错误案例
- **0.1.0** (2026-01-27): 初始版本，包含未定义符号案例研究

## Related Skills

- **openharmony-build**: For building OpenHarmony codebase
- **compile-analysis**: For analyzing compilation performance and dependencies
