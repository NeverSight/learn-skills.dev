---
name: ohos-test-arkruntime-interop-testing
description: >
  Guide for adding and maintaining ArkTS <-> JS/TS interoperability tests in ArkCompiler.
  触发场景：在 plugins/ets/tests/interop_js/tests/ 目录下创建新的 ArkTS 与 JS/TS 互操作（Interop）测试用例、调试/维护已有 Interop 测试、编写 C++ 运行器（GTest runner）或声明文件（.d.ets）时。
metadata:
  author: openharmony
  scope: domain
  stage: testing
  domain: arkruntime
  capability: interop-testing
  version: 1.0.0
  status: production
  tags:
    - arkruntime
    - interop
    - testing
    - test-cases
---

# ETS Interop Testing

This skill provides a structured workflow and templates for creating comprehensive interop tests between ArkTS (ETS) and JavaScript/TypeScript.

## Core Concepts

Interop tests typically involve three layers:
1. **C++ Runner**: GTest-based entry point that manages the VM lifecycle.
2. **ArkTS (ETS) Logic**: The main test code written in ArkTS.
3. **JS/TS Module**: The JavaScript or TypeScript code being called or calling into ArkTS.

## Directory Structure

A typical test case directory (e.g., `plugins/ets/tests/interop_js/tests/my_test/`) should contain:
- `CMakeLists.txt`: Build configuration.
- `arktsconfig.in.json`: ArkTS compiler configuration with dependencies.
- `my_test.cpp`: C++ GTest runner.
- `my_test.ets`: ArkTS test logic.
- `my_test.ts` or `my_test.js`: JS/TS side of interop.
- `my_test.d.ets`: (Optional) Declaration file for JS/TS exports.

## Workflow: Adding a New Test Case

### 1. Initialize Directory
Create a new unique directory in `plugins/ets/tests/interop_js/tests/`.

### 2. Define JS/TS Interface
Write your JS/TS code in a `.ts` or `.js` file.
Use `assets/interop_js.ts.template` as a starting point.

### 3. Create ArkTS Declarations
If your JS/TS code exports functions/classes, create a `.d.ets` file to declare them for ArkTS.
Template: `assets/interop_decl.d.ets.template`.

### 4. Implement ArkTS Test Logic
Write the test logic in ArkTS. This logic should return `true` on success.
Template: `assets/interop_test.ets.template`.

### 5. Configure Build and Compiler
- **arktsconfig.in.json**: Map the JS/TS module to its `.d.ets` declaration.
  Template: `assets/arktsconfig.in.json.template`.
- **CMakeLists.txt**: Use the `panda_ets_interop_js_gtest` macro.
  Template: `assets/CMakeLists.txt.template`.

### 6. Create C++ Runner
Inherit from `EtsInteropTest` and use `CallEtsFunction` to trigger your test.
Template: `assets/test_runner.cpp.template`.

## Verification and Best Practices

- **Unique Naming**: Ensure your target name in `CMakeLists.txt` and directory name are unique to avoid collisions.
- **Isolation**: Each test should be self-contained in its directory.
- **Error Handling**: Prefer returning `boolean` from ETS or throwing exceptions that C++ can catch.
- **Formatting**: Always run `bash code-format.sh format-changed` after adding new files.

## References
- See `ohos-dev-arkruntime-interop-development` for architectural details.
- Root `CMakeLists.txt` in `interop_js/tests/` automatically includes subdirectories via `SUBDIRLIST`.
