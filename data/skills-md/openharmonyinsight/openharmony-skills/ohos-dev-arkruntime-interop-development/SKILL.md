---
name: ohos-dev-arkruntime-interop-development
description: >
  Expert assistant for ArkTS-JS Interoperability in ArkCompiler (ArkTS runtime).
  触发场景：修改/调试 ArkCompiler 互操作层代码（static_core/plugins/ets/runtime/interop_js/）、实现 ArkTS 与 JS 跨语言调用、处理 ETS 和 JS 之间的值转换（js_convert/JSRefConvert）、分析 Interop 内存泄漏与 GC 安全点、以及进行相关代码规范审查。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkruntime
  capability: interop-development
  version: 1.0.0
  status: production
  tags:
    - arkruntime
    - interop
    - arkts
    - cpp
---

# ArkRuntime Interop Development

## Overview

This skill specializes in the **ArkTS <-> JavaScript Interoperability** layer located in `runtime_core/static_core/plugins/ets/runtime/interop_js/`. It bridges the ArkTS runtime (ETS) with the JavaScript engine via NAPI.

## Core Capabilities

### 1. Navigating the Interop Layer
The directory structure is segmented by function:
- **`ets_proxy/`**: ETS objects in JS.
- **`js_proxy/`**: JS objects in ETS.
- **`intrinsics/`**: Direct interop access from ArkTS.
- **`napi_impl/`**: Implementation of NAPI interfaces.
- **Reference**: [architecture.md](references/architecture.md)

### 2. Underlying Runtimes
Interop depends on both the JS runtime and the NAPI framework:
- **JS Runtime**: Core VM, interpreter, and compiler context. See [ets-runtime.md](references/ets-runtime.md).
- **NAPI Framework**: The abstraction layer for JS engines. See [napi-framework.md](references/napi-framework.md).

### 3. Value Conversion
Handled by `js_convert` and `JSRefConvert` classes.
- **Key Files**: `js_convert.h`, `js_refconvert_*.h`.

## Common Workflows

### Debugging Interop Issues
- **Crashes**: Check `napi_env` usage and scope mismatches.
- **Leaks**: Monitor `GlobalObjectStorage` and proxy reference counting.
- **Exceptions**: Use `InteropCtx::ThrowJSError` or `ThrowETSError`.

### Performance & Memory
- Use `napi_create_async_work` for heavy tasks.
- Respect GC safepoints and handle allocation through `EcmaVM`.
- Use `napi_handle_scope` to prevent memory leaks.

### Coding Standards
- **Formatting**: Always run `bash code-format.sh format-changed` before committing.
- **Validation**: Ensure `check <path>` passes and `tidy` reports no new warnings.

## Key Headers
- `interop_context.h`: Main context.
- `js_convert.h`: Value conversion.
- `ets_proxy/ets_class_wrapper.h`: ETS classes in JS.
- `js_proxy/js_proxy.h`: JS objects in ETS.