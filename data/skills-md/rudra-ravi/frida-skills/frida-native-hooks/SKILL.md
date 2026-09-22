---
name: frida-native-hooks
description: Build Frida native hooks for C/C++/Objective-C functions, exports, imports, symbols, memory, Interceptor, NativeFunction, Stalker, and CModule.
---

# Frida Native Hooks

Use this skill when the target is a native function or memory behavior.

## Discovery First

1. Identify process architecture and module:
   ```js
   console.log(Process.arch, Process.platform, Process.pointerSize);
   for (const m of Process.enumerateModules()) console.log(m.name, m.base, m.size);
   ```
2. Resolve addresses through Frida APIs when possible:
   ```js
   const mod = Process.getModuleByName("libtarget.so");
   const fn = mod.getExportByName("target_function");
   ```
3. If names are stripped, search imports/exports first, then symbols, strings, and byte patterns.
4. On ARM/Thumb, prefer addresses returned by Frida APIs so instruction-set details are handled correctly.

## Hook Pattern

```js
const target = Process.getModuleByName("libc.so").getExportByName("open");

Interceptor.attach(target, {
  onEnter(args) {
    this.path = args[0].readUtf8String();
    console.log("[open] path=", this.path);
  },
  onLeave(retval) {
    console.log("[open] fd=", retval.toInt32());
  }
});
```

## Replacement Rules

- Use `Interceptor.attach()` for tracing and light argument/return mutation.
- Use `Interceptor.replace()` when fully replacing behavior.
- Use `Interceptor.replaceFast()` only for hot functions where lower overhead is required; call the original through the returned pointer.
- Wrap original functions with `NativeFunction` using the correct ABI, return type, and argument types.
- Call `Interceptor.flush()` only when a just-installed hook must be invoked immediately from the same script.

## Practitioner Patterns

- Hook boundaries before internals: exported API, imported libc/crypto/TLS calls, file/network/syscall wrappers, then app-specific stripped functions.
- When names are stripped, combine static strings, imports, cross-references from a disassembler, runtime module load logs, and Stalker/caller summaries.
- Use `Thread.backtrace()` early to find who called a generic boundary such as `open`, `connect`, `SSL_write`, `CCCrypt`, `strcmp`, or `memcmp`.
- Use Stalker for bounded questions only: a specific thread, during a specific function call, with call/block summaries before instruction-level tracing.
- Treat anti-Frida checks as native work when they involve `/proc`, `ptrace`, loaded module scans, thread names, ports, or symbol/string scans.

## Memory Safety

- Do not write a longer string into an existing buffer unless the buffer size is proven.
- Prefer allocating a new string and replacing the pointer argument.
- Keep allocated replacement strings reachable for the required lifetime:
  ```js
  const keepalive = [];
  Interceptor.attach(target, {
    onEnter(args) {
      const s = Memory.allocUtf8String("replacement");
      keepalive.push(s);
      args[0] = s;
    }
  });
  ```
- Copy `retval`/argument data inside callbacks if it is needed later.

## Native Investigation Checklist

- Module loaded before resolving address.
- Function signature verified from headers, decompiler, debug symbols, or observed calling convention.
- Pointer reads guarded for null and readability.
- Logs include enough context to prove the right call path.
- Mutation has a rollback path: detach, revert, restart, or remove Gadget config.

## References

Read `references/native-patterns.md` for templates covering exports, imports, pattern scans, backtraces, replacements, and performance notes.
