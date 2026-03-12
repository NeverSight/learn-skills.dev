---
name: bun-ffi-interop-pattern
description: 'Use when calling native libraries via bun:ffi, loading shared libraries with dlopen, or working with FFI pointers and C struct memory layouts'
---

# Bun FFI Interop Pattern

You are an expert systems programmer bridging JavaScript/TypeScript with Native C/C++ ABI using `bun:ffi`. When writing FFI bindings, you MUST adhere to these strict memory safety and interop rules.

## 1. Library Loading & Lazy Initialization

**CRITICAL RULE:** NEVER call `dlopen` at the module's top level. It can crash the entire Bun process on startup if the library is missing or incompatible. MUST use lazy loading.

```typescript
import { dlopen, suffix, FFIType, ptr, toArrayBuffer, CString } from 'bun:ffi';

let _lib: ReturnType<typeof dlopen> | null = null;

// suffix auto-resolves: linux=so, darwin=dylib, win32=dll
export function loadMyLib(customPath?: string) {
  if (_lib) return _lib;

  const libPath = customPath || `libexample.${suffix}`;

  _lib = dlopen(libPath, {
    add: { args: [FFIType.i32, FFIType.i32], returns: FFIType.i32 },
    get_data: { args: [], returns: FFIType.ptr },
    free_data: { args: [FFIType.ptr], returns: FFIType.void },
  });

  return _lib;
}
```

## 2. Struct Passing Constraints (MUST READ)

**CRITICAL LIMITATION:** Bun FFI does NOT natively support Pass-by-Value for C structs.

If a C function requires a struct by value (e.g., `void process_struct(MyStruct s);`), you MUST use one of these workarounds. Do NOT attempt to pass a JS object directly.

**Workaround A: Pointer Passing (Recommended)**

Modify the C API to accept a pointer if possible.

```c
// C side: void process_struct_ptr(MyStruct *s);
```

```typescript
// TS side:
const process_struct_ptr = { args: [FFIType.ptr], returns: FFIType.void };
```

**Workaround B: Argument Splitting (For tiny structs only)**

If you cannot change the C API, split the struct fields into discrete arguments based strictly on the target architecture's ABI (e.g., System V ABI for x86_64).

```c
// C side: struct Slice { long len; char *ptr; };
// void process_slice(struct Slice s);
```

```typescript
// TS side (x86_64 System V ABI maps this to two registers):
const process_slice = { args: [FFIType.i64, FFIType.ptr], returns: FFIType.void };
```

## 3. Safe Memory Operations & Pointers

Pointers in `bun:ffi` are represented as `number` (32-bit) or `bigint` (64-bit).

```typescript
// 1. Getting a pointer from a TypedArray
const arr = new Uint8Array(64);
const arrPtr = ptr(arr); // Returns number or bigint pointing to the buffer

// 2. Reading Memory — creates an ArrayBuffer copy from a pointer
const dataPtr = lib.symbols.get_data();
const buffer = toArrayBuffer(dataPtr, 64); // MUST specify the exact byte length
const view = new DataView(buffer);

// MUST always use explicit endianness (true = little-endian) for cross-platform stability
const field1 = view.getBigInt64(0, true);  // offset 0
const field2 = view.getUint32(8, true);    // offset 8

// 3. Reading Null-Terminated C Strings
const str = new CString(dataPtr).toString();
```

## 4. Struct Memory Layout & Offsets

**CRITICAL GUARDRAIL:** DO NOT guess or manually calculate struct offsets in TypeScript. C compilers apply complex padding and alignment rules that cannot be reliably predicted.

You MUST instruct the user to generate the offsets using a C program, or assume the user has already provided the exact byte offsets.

```c
// Instruct the user to compile and run this to get accurate offsets:
#include <stdio.h>
#include <stddef.h>
#include "target_lib.h"

int main() {
  printf("const SIZE = %zu;\n", sizeof(MyStruct));
  printf("const OFFSET_FIELD1 = %zu;\n", offsetof(MyStruct, field1));
  printf("const OFFSET_FIELD2 = %zu;\n", offsetof(MyStruct, field2));
  return 0;
}
```

## 5. Resource Management (Preventing Leaks)

Native memory allocated by the C library MUST be explicitly freed. JS garbage collection does NOT manage FFI pointers.

```typescript
const dataPtr = lib.symbols.get_data();
try {
  const buf = toArrayBuffer(dataPtr, 32);
  const view = new DataView(buf);
  const id = view.getUint32(0, true);
  // Do work...
} finally {
  // MUST always free native memory in a finally block
  lib.symbols.free_data(dataPtr);
}
```

## 6. Type-Safe Wrapper Pattern

When consuming parsed struct data, wrap pointer reads into typed functions with known offsets.

```typescript
interface MyData {
  id: number;
  name: string;
}

// Offsets MUST come from the C offset program (Section 4), NOT from manual calculation
const OFFSETS = { id: 0, name: 4 } as const; // example: verified via offsetof()
const STRUCT_SIZE = 32; // example: verified via sizeof()

function parseData(dataPtr: number): MyData {
  const buf = toArrayBuffer(dataPtr, STRUCT_SIZE);
  const view = new DataView(buf);
  return {
    id: view.getUint32(OFFSETS.id, true),
    name: new CString(dataPtr + OFFSETS.name).toString(),
  };
}
```
