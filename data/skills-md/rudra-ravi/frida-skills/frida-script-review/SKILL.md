---
name: frida-script-review
description: Review, harden, and simplify Frida scripts before running CodeShare snippets, universal bypasses, broad hooks, native pointer code, Java hooks, or ObjC hooks.
---

# Frida Script Review

Use this skill before running public, generated, or mutation-heavy Frida scripts.

## Review Pass

1. Identify platform assumptions: Android, iOS, native, desktop, Gadget.
2. Identify mutation points: return replacement, argument rewrite, file writes, process control, network changes.
3. Check timing: spawn vs attach, module load, class loader, ObjC availability.
4. Check safety: null pointers, overloads, string lifetimes, `retval` copies, recursion, noisy hooks.
5. Reduce broad bundles to the hooks relevant to the target behavior.

## Red Flags

- Blind universal bypass without proof of which hook fired.
- Native pointer reads without null or length checks.
- String replacement into fixed buffers without proving buffer size.
- Java method hook without explicit overload where overloads exist.
- ObjC selector assumed without checking `ObjC.available` and class/method presence.
- `retval` or argument wrappers stored for later use instead of copied.
- Logs that print secrets unnecessarily.

## Hardening Pattern

Before mutation:

```js
console.log("hook fired", targetName);
console.log(Thread.backtrace(this.context, Backtracer.ACCURATE)
  .map(DebugSymbol.fromAddress).join("\n"));
```

After proof:

```js
if (shouldPatchThisCall()) {
  retval.replace(1);
}
```

## Output

Return:

- Risk summary.
- Exact lines or hook blocks to keep, remove, or change.
- Safer reviewed script or patch.
- Verification command and expected proof.

## References

- Frida JavaScript API: https://frida.re/docs/javascript-api/
- Frida troubleshooting: https://frida.re/docs/troubleshooting/
- Frida CodeShare: https://codeshare.frida.re/
