---
name: dbg
description: >
  Debug applications using the dbg CLI debugger.
  Supports Node.js (V8/CDP), Bun (WebKit/JSC), and native code via LLDB (DAP).
  Use when: (1) investigating runtime bugs by stepping through code, (2) inspecting
  variable values at specific execution points, (3) setting breakpoints and conditional
  breakpoints, (4) evaluating expressions in a paused context, (5) hot-patching code
  without restarting (JS/TS), (6) debugging test failures by attaching to a running process,
  (7) debugging C/C++/Rust/Swift with LLDB, (8) any task where understanding runtime
  behavior requires a debugger.
  Triggers: "debug this", "set a breakpoint", "step through", "inspect variables",
  "why is this value wrong", "trace execution", "attach debugger", "runtime error",
  "segfault", "core dump".
---

# dbg Debugger

`dbg` is a CLI debugger that supports **Node.js** (V8/CDP), **Bun** (WebKit/JSC), and **native code** (C/C++/Rust/Swift via LLDB/DAP). It uses short `@refs` for all entities -- use them instead of long IDs.

## Supported Runtimes

| Runtime | Language | Launch example |
|---------|----------|----------------|
| Node.js | JavaScript | `dbg launch --brk node app.js` |
| tsx / ts-node | TypeScript | `dbg launch --brk tsx src/app.ts` |
| Bun | JavaScript / TypeScript | `dbg launch --brk bun app.ts` |
| LLDB | C / C++ / Rust / Swift | `dbg launch --brk --runtime lldb ./program` |

The runtime is auto-detected from the launch command for JS runtimes. For native code, use `--runtime lldb`.

## Core Debug Loop

```bash
# 1. Launch with breakpoint at first line
dbg launch --brk node app.js
# Or: dbg launch --brk bun app.ts
# Or: dbg launch --brk --runtime lldb ./my_program
# Or attach to a running process with the --inspect flag
dbg attach 9229

# 2. Set breakpoints at suspicious locations
dbg break src/handler.ts:42
dbg break src/utils.ts:15 --condition "count > 10"

# 3. Run to breakpoint
dbg continue

# 4. Inspect state (shows location, source, locals, stack)
dbg state

# 5. Drill into values
dbg props @v1              # expand object
dbg props @v1 --depth 3   # expand nested 3 levels
dbg eval "x + 1"

# 6. Fix and verify (JS/TS only)
dbg set count 0            # change variable
dbg hotpatch src/utils.js  # live-edit (reads file from disk)
dbg continue               # verify fix
```

## Debugging Strategies

### Bug investigation -- narrow down with breakpoints
```bash
dbg launch --brk node app.js
dbg break src/api.ts:50                    # suspect line
dbg break src/api.ts:60 --condition "!user" # conditional
dbg continue
dbg vars                                    # check locals
dbg eval "JSON.stringify(req.body)"         # inspect deeply
dbg step over                               # advance one line
dbg state                                   # see new state
```

### Native code debugging (C/C++/Rust)
```bash
dbg launch --brk --runtime lldb ./my_program
dbg break main.c:42
dbg break-fn main                          # function breakpoint (DAP only)
dbg continue
dbg vars                                    # inspect locals
dbg eval "array[i]"                         # evaluate expression
dbg step into                               # step into function
```

### Attach to running/test process
```bash
# Start with inspector enabled
node --inspect app.js
# Or: bun --inspect app.ts
# Then attach
dbg attach 9229
dbg state
```

### Trace execution flow with logpoints (no pause)
```bash
dbg logpoint src/auth.ts:20 "login attempt: ${username}"
dbg logpoint src/auth.ts:45 "auth result: ${result}"
dbg continue
dbg console    # see logged output
```

### Exception debugging
```bash
dbg catch uncaught          # pause on uncaught exceptions
dbg continue                # runs until exception
dbg state                   # see where it threw
dbg eval "err.message"      # inspect the error
dbg stack                   # full call stack
```

### TypeScript source map support
dbg automatically resolves `.ts` paths via source maps. Set breakpoints using `.ts` paths, see `.ts` source in output. Use `--generated` to see compiled `.js` if needed.

## Ref System

Every output assigns short refs. Use them everywhere:
- `@v1..@vN` -- variables: `dbg props @v1`, `dbg set @v2 true`
- `@f0..@fN` -- stack frames: `dbg eval --frame @f1 "this"`
- `BP#1..N` -- breakpoints: `dbg break-rm BP#1`, `dbg break-toggle BP#1`
- `LP#1..N` -- logpoints: `dbg break-rm LP#1`

Refs `@v`/`@f` reset on each pause. `BP#`/`LP#` persist until removed.

## Key Flags

- `--json` -- machine-readable JSON output on any command
- `--session NAME` -- target a specific session (default: "default")
- `--runtime NAME` -- select debug adapter (e.g. `lldb` for native code)
- `--generated` -- bypass source maps, show compiled JS (on state/source/stack)

## Command Reference

See [references/commands.md](references/commands.md) for full command details and options.

## Tips

- `dbg state` after stepping always shows location + source + locals -- usually enough context
- `dbg state -c` for source only, `-v` for vars only, `-s` for stack only -- save tokens
- `dbg eval` supports `await` -- useful for async inspection (JS/TS)
- `dbg blackbox "node_modules/**"` -- skip stepping into dependencies
- `dbg hotpatch file` reads the file from disk -- edit the file first, then hotpatch (JS/TS only)
- `dbg break-fn funcName` -- function breakpoints work with DAP runtimes (LLDB)
- Execution commands (`continue`, `step`, `pause`, `run-to`) auto-return status
- `dbg stop` kills the debugged process and daemon
