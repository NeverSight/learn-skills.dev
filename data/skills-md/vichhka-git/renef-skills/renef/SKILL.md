---
name: renef
description: >-
  Use when operating renef / renef.io to instrument Android ARM64 apps: hooking native and Java
  functions, scanning/reading/writing/patching process memory, tracing syscalls (renef-strace),
  stack backtraces, value/memory cheats, and writing Lua 5.4 scripts. Reach for this for SSL
  pinning bypass, root/debugger detection bypass, function tracing, crypto key logging, game
  memory editing/cheats, CTF native challenges, or porting Frida JS / GameGuardian (gg.*) scripts
  to renef. Triggers: "renef", "renef.io", ".renef script", "renef-strace", "hook this Android
  function", "bypass SSL pinning with renef", "port this Frida/GameGuardian script to renef".
---

# Operating Renef

You are driving **renef** — a dynamic instrumentation engine for **Android ARM64**. Your job is to
emit renef Lua/CLI that runs correctly the first time. If you've written Frida hooks, GameGuardian
cheats, or game-hacking Lua, the *concepts* already transfer — you only need renef's **syntax and
workflow**, which this skill makes exact. Do not guess API names; use the Syntax Contract below as
ground truth, and run the Self-Lint before presenting any script.

For **authorized** security testing, app-hardening review, CTFs, and reverse-engineering of
software you own or are permitted to analyze.

**Start here for any real target:** run `probe.lua` (bundled with this skill) to ground-truth the
actual API/behavior of *this* renef build, then follow the investigation loop in
`references/methodology.md`. Attempt and measure on-device — don't pre-decide what's possible —
and report status honestly: *not attempted → installed but unverified → verified working*. The
human drives the device/app/proxy and decides the goal; you do the enumeration, scripting,
error-parsing, and verification. Recipes below are **worked examples of the loop**, not a menu to
copy blindly (offsets/signatures are target-specific).

## What you're driving

- **Topology — read this before anything.** `renef` is a **host** client (your macOS/Linux shell)
  that drives `renef_server` running **on the Android device** over an ADB-forwarded socket. You do
  **not** run `renef` on the device, and you do **not** `adb push hook.lua` + `adb shell renef …`.
  That on-device pattern is **only** `--local` mode (Termux/SSH on a rooted phone). Default and
  assumed-here = host client → remote device. Lua scripts stay on the host and are sent over the
  wire by `-l`; device-side paths apply **only** under `--local`.
- Your Lua runs **inside the target process** (injected `libagent.so`, embedded Lua 5.4, memfd
  injection, no ptrace). `Module.*`, `Memory.*`, hook callbacks all execute in the app's address
  space — paths, PIDs, fds are the *target's*.
- You drive it from the **CLI REPL** (`renef>`) or one-shot via `-l script.lua`.
- **Hook/trace output is asynchronous** — you must `watch` (or launch with `-w`) or you see nothing.

## Preflight (Step 0 — a gate, before you write, run, or "test" anything)

Confirm the host→device chain end-to-end. Until you do, you **cannot test** — deliver the script
as explicitly **unverified**, never as "tested/working", and never invent run output.

1. `adb devices` lists exactly one authorized device (more than one → require `-d <id>`; none → stop).
2. The `renef` client exists **on the host**: `command -v renef` (or `renef -h`).
3. `renef_server` is running **on the device**: `adb shell pidof renef_server`. If absent, start it
   (`adb shell su -c '/data/local/tmp/renef_server &'`) or rely on magisk-renef.
4. Root (or gadget mode for non-root), target is ARM64, and the package is installed (`la~<name>`).

A "test" = you saw real hook output via `-w`/`watch` while exercising the app — **not** that the
script reads correctly. If any link above is missing, say which one and stop short of claiming a run.

## The loop (always follow this)

1. **Connect** to the target (table below).
2. **Locate** the target code — resolve an **offset by symbol or byte-pattern**, never hardcode an
   absolute runtime address; guard with `if not base then return end`.
3. **Install the smallest hook that proves the call fires** (`print` in `onEnter`).
4. **Verify** by watching output while you trigger the app (`-w` / `watch`).
5. **Iterate** — add logic only after the minimal hook is confirmed.

For startup-time protections (root/integrity/debugger checks), connect with `--pause` (spawn gate)
so hooks install before the app's `onCreate` runs.

## Connect modes

| Mode | Command | When |
|---|---|---|
| Spawn (root) | `renef -s com.pkg -l hook.lua` | start fresh, hooks before app code |
| Attach (root) | `renef -a <pid> -l hook.lua` | already running (`adb shell pidof com.pkg`) |
| Spawn gate | `renef -s com.pkg -l bypass.lua --pause` | beat startup-time checks |
| Gadget (no root) | `renef -g <pid> -l hook.lua` | non-root, APK patched with `libagent.so` |
| Local (on-device) | `renef --local -s com.pkg -l /data/local/tmp/hook.lua` | Termux/SSH, SELinux-safe |

Every row except the last runs `renef` **on the host** against the device — only `--local` runs the
client on-device. Server must run on device first (`adb shell /data/local/tmp/renef_server`, or the
magisk-renef module auto-starts it). Engine: `trampoline` (default, any address) or `--hook=pltgot` (imported
functions only). Full flag list and REPL commands → `references/cli.md`.

## Syntax Contract (ground truth — do not invent API)

**Language is Lua 5.4.** `local`; `..` concatenation; `string.format("0x%x", n)`; `function(x) end`;
tables `{}`; `nil`; `ipairs`/`#t`; integer hex `0x..`. No `var/let/const`, arrow fns, template
strings, or `===`.

**Native hook** — target is `(library, offset)`, never an absolute address:
```lua
hook("libc.so", 0x12340, {
  onEnter = function(args)   -- args[0..7] = x0..x7 (first arg = args[0]); assign to modify
    args[0] = 0x200
  end,
  onLeave = function(retval) -- return a value to REPLACE x0; `return retval` passes through; nothing = keep
    return retval
  end,
  caller = "libnative.so"    -- optional: restrict to this caller → PLT/GOT mode (imported fns only)
})
```

**Java hook** — class uses `/` (JNI), signature is **mandatory**:
```lua
hook("com/example/Cls", "method", "(Ljava/lang/String;)Z", {
  onEnter = function(args)
    -- args[0]=ArtMethod* (ignore) | args[1]=this (instance) OR first param (static) | args[2..]=params
    local s = Jni.getStringUTF(args[2])   -- string args are raw pointers
    -- args.skip = true                   -- skip the original entirely (bypass primitive)
  end,
  onLeave = function(retval)
    -- retval.raw = raw x0 (int) ; retval.value = decoded string (String-returning methods only)
    return 1                              -- see return table below
  end
})
```
`onEnter.args` also exposes `args.class/method/signature/isStatic`. `onLeave` return options:
`nil`=keep · integer=set x0 (`1` true / `0` false) · boolean=1/0 · `Jni.newStringUTF("x")`=new
String · `{__jni_type="string"|"int"|"boolean", value=...}`=typed · `retval.raw`=pass original.

**Memory:** `Memory.scan(pat[,lib])`/`search` (string or hex, `??` wildcards) → table of
`{library,addr,offset,hex,ascii}`. `read(a,n)` `readU8/16/32/64(a)` `readStr(a[,n])`/`readString`.
`write(a,bytes)` `writeU8/16/32/64(a,v)` `patch(a,bytes)` (auto-mprotect). **There is no
`Memory.writeString`** — write a string as bytes: `Memory.write(addr, "text\0")`.
`hexdump(target[,len])` → string, `print()` it.

**Module:** `find(name)`→base int|nil · `list()`→**string** · `exports(name)`→`{name,offset}`
(`.dynsym`) · `symbols(name)`→`{name,offset}` (`.symtab`, `nil` if stripped).

**Java runtime (no hook):** `Java.use("p/C")` → `:call(m,sig,...)` / `:new(sig,...)`;
instance `:call(m,sig,...)`; `.raw` = ART pointer; `Java.registerClass{implements=,methods=}`;
`Java.array("p/C",{...})`.

**Other globals:** `Jni.newStringUTF/getStringUTF/getStringLength/deleteGlobalRef` ·
`Thread.backtrace()` (auto caller context in hooks) / `Thread.id()` · `File.read/exists/readlink/
fdpath` · `Syscall.trace(...)/stop()/list()` · `OS.getpid/kill/tgkill/listdir` · `print` /
`console.log` / color globals `RED GREEN YELLOW BLUE MAGENTA CYAN WHITE RESET`.
Script directive: `__hook_type__ = "trampoline"|"pltgot"` at top of file.

> There is **no** `Interceptor`, `Java.perform`, `Process.*`, `ptr()`/NativePointer, or `gg.*`
> namespace. Those belong to other tools — translate them (`references/from-other-tools.md`).

### Share state between onEnter and onLeave with a closure-local (NOT `args`)

`args` does not exist in `onLeave`. Capture in a `local` declared just before `hook(...)`:
```lua
for _, e in ipairs(Module.exports("libc.so")) do
  if e.name == "open" then
    local blocked = false                         -- closure-local
    hook("libc.so", e.offset, {
      onEnter = function(args)
        local p = Memory.readString(args[0]); blocked = p and p:find("/su") ~= nil
      end,
      onLeave = function(retval) if blocked then return -1 end; return retval end
    })
    break
  end
end
```

## Self-Lint (run over every script before presenting it)

- [ ] **Preflight passed** (host `renef` + `adb devices` + device `renef_server`) before any claim of
      a test. Script invoked from the **host** (`renef -s/-a/-g …`), not `adb shell renef`/`adb push`
      (that's `--local`-only). If preflight didn't pass, the script is labeled **unverified** — no
      fabricated output.
- [ ] Hook target is `(library, offset)` — **no absolute address** passed to `hook()`.
- [ ] Offset resolved by symbol (`Module.exports/symbols`) or byte-pattern (`Memory.search`), not a
      hardcoded number — and guarded with `if not base then return end`.
- [ ] Java class uses `/` separators; signature is present and exact `(params)ret`.
- [ ] **Static vs instance arg index:** instance method first param = `args[2]`; **static method
      first param = `args[1]`** (verified). Native first arg = `args[0]`. Getting this wrong reads
      the wrong value silently — the #1 logic bug.
- [ ] State shared across callbacks via a closure-`local`, never via `args` in `onLeave`.
- [ ] `onLeave` returns to modify; native pass-through uses `return retval`. Spoof a return in
      `onLeave` — do **not** mutate the input arg in `onEnter` to change a return value.
- [ ] No `Memory.writeString` (doesn't exist) — use `Memory.write(a, "s\0")`. Only documented
      globals (no Frida/GG names, no `Process.*`).
- [ ] **Every hook wrapped in `safe()`/`pcall` that prints the error** — renef reports failures as a
      bare `ERROR: Lua execution failed` and aborts the rest of the script (see `references/debugging.md`).
- [ ] No hot-function hooks (`open`/`read`/`write`/`system`/`popen`/`do_dlopen`) installed while the
      app runs — they race and crash the agent. Put important bypasses first, risky hooks last.
- [ ] Syntax pre-checked with `luac -p` (renef won't give you the line); output seen via `-w`/`watch`.

## Task → playbook

| User wants | Do |
|---|---|
| Override a Java boolean/int check (root, isVip, license) | Java hook, `onLeave` `return 0/1` |
| Bypass a void Java verify that throws (SSL `checkServerTrusted`) | Java hook, `onEnter` `args.skip = true` |
| Replace a Java String return | `onLeave` `return Jni.newStringUTF("...")` |
| Trace/inspect a native function | resolve offset via `Module.exports/symbols`, minimal `onEnter` hook, `watch` |
| Hook a not-yet-loaded lib (Flutter, plugin) | hook `do_dlopen` in `linker64`, install on load |
| Game value cheat (find/edit/freeze a number) | `Memory.scan` → refine → `writeU32`; freeze via a hot hook → `from-other-tools.md` (GameGuardian) |
| Monitor file/network/syscalls | `Syscall.trace{category="file"}` or `renef-strace`, then `watch` |
| Patch/NOP native code | `Memory.search` pattern → `Memory.patch(addr, bytes)` |
| Port a Frida or GameGuardian script | `references/from-other-tools.md` |

## Reference files (read on demand — don't load them all at once)

- `references/methodology.md` — **the investigation loop**: how to solve a NEW bypass/hook yourself
  (classify → locate → probe mechanism → minimal hook → verify → choose primitive), decompose-to-
  smallest-goal, human/AI roles, honest status. Start here for anything not covered by a recipe.
- `probe.lua` — bundled diagnostic. Run it FIRST on a new target/build to measure the real API
  surface, error behavior, arg layout, and the reflection bridge instead of trusting notes.
- `references/debugging.md` — **read this when anything fails.** renef hides errors (`ERROR: Lua
  execution failed` / `(no response)` / `Agent disconnected`); how to recover the real message with
  `pcall`/`load`, the hot-hook crash race, `--pause` caveats, verifying installs, connection
  recovery, and recognizing RASP/shielded apps.
- `references/lua-api.md` — full API: exact signatures, return shapes, JNI signature table,
  per-function notes. **Read before writing a non-trivial script.**
- `references/cli.md` — every CLI command/flag, connect modes, spawn gate, build/deploy, r2renef,
  python binding, magisk-renef.
- `references/from-other-tools.md` — translate **Frida JS** and **GameGuardian (`gg.*`)** /
  game-hacking Lua into renef. Includes a reusable value scan→refine→freeze helper.
- `references/recipes.md` — copy-paste scripts: SSL unpinning (Java/Flutter/native), root/debugger
  bypass, crypto logging, tracing, dlopen watch, memory cheats, syscall auditing, CTF.
- `references/gotchas.md` — pitfalls, doc/runtime discrepancies (`Jni` vs `JNI`, undocumented
  helpers), troubleshooting (injection fails, hook not firing, SELinux), performance.
