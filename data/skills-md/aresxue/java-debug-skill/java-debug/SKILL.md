---
name: java-debug
description: >
  Java remote breakpoint debugging. Uses an in-house JDI Client (zero-dependency fat jar, HTTP server mode, no tmux/sleep dependency) to attach to a remote JVM's JDWP port; the AI autonomously sets breakpoints, collects call stacks and local variables, evaluates expressions, and single-steps to locate the root cause.
  Compared with jdb: SUSPEND_EVENT_THREAD freezes only the hit thread instead of the whole JVM, interaction is structured JSON, and a breakpoint hit automatically returns stack + locals.
  Use when: "java远程debug", "远程debug", "远程断点调试", "断点调试", "JDI调试", "jdwp调试", "attach jvm", "设断点", "java remote debug", "remote debug", "breakpoint debug", "remote breakpoint debugging", "JDI debug", "jdwp debug", "set breakpoint".
argument-hint: "<host:port> [--bp <Class.method[:line]>]... [--repo <local-repo-path>] [--max-bp <n>] [--wait-timeout <seconds>] [--manual]"
allowed-tools: [Read, Bash, Glob, Grep]
---

# Java Remote Breakpoint Debugging (JDI Client)

Attach to a remote JVM that has JDWP enabled; the AI sets breakpoints, waits for hits, collects runtime state (call stack / local variables / expression evaluation), single-steps, and uses that to locate the root cause.

The core is `scripts/jdi-client.jar` (a fat jar that uses only the JDK's built-in `com.sun.jdi`, zero external dependencies). The jar is **not shipped with the skill**: on first use `scripts/ensure-jdi-client.sh` builds it locally from the bundled source `jdi-client/` (see Chapter 4). It stays resident in HTTP server mode (**listening on 127.0.0.1 only**), and every operation is a JSON command sent with `curl` (POST MUST carry `Content-Type: application/json`).

**`<SKILL_DIR>`** in the commands below is the absolute path of the directory containing this SKILL.md. It depends on how the skill was installed (global or project scope, and which agent), e.g. `~/.claude/skills/java-debug`, `<project>/.claude/skills/java-debug`, `~/.agents/skills/java-debug`. Take it from where this file was loaded and write it into each command as a literal absolute path; do not keep it in a shell variable, since shell state does not survive between commands.

**Core differences from jdb**:

| Aspect | jdb | This Skill |
|------|-----|----------|
| Suspend scope | `SUSPEND_ALL`, freezes the whole JVM | `SUSPEND_EVENT_THREAD`, freezes only the hit thread (**each hit freezes one thread; without resume they accumulate**, see Chapter 8) |
| Interaction | Text output must be parsed; relies on tmux + sleep to race timing | Structured JSON, no tmux, no sleep races |
| Hit information | Requires `where` / `locals` one by one | Hit response automatically includes stack + locals |
| Determinism | Polling | Event-driven, blocking wait |

---

## 1. Input Parsing

| Parameter | Required | Description |
|------|------|------|
| `<host:port>` | Yes | JDWP address of the target JVM, e.g. `10.0.1.5:5005`, `localhost:5005` |
| `--bp <Class.method[:line]>` | No | Pre-specified breakpoint, repeatable. `com.example.OrderService.query` is a method-entry breakpoint; `com.example.OrderService:123` is a line breakpoint |
| `--repo <path>` | No | Local source repository, used to read code and plan breakpoints. If not given and the cwd is a Java project, use the cwd |
| `--max-bp <n>` | No | Max breakpoints per round, replaces the default "3-4" in Step 3b |
| `--wait-timeout <seconds>` | No | Replaces `"timeout":180` in every `wait-breakpoint` command in this document |
| `--manual` | No | This machine cannot reach the target JDWP: do not start jdi-client locally; only produce the command block for the user to run on the target machine, see Chapter 10 |

After splitting `host` / `port` on `:`, **substitute them into later commands as literals**; do not use `$(...)` command substitution or shell variable expansion.

**When invoked by another skill** (e.g. another diagnosis skill): constraints the caller attaches in args (parameters or prose, e.g. "resume immediately after reading the value on hit → disconnect")
take precedence over this skill's defaults; but they may only tighten, never loosen, the hard rules in Chapter 8 (MUST disconnect, breakpoints MUST be confirmed by the user).

**Scenario branches**:

| Input | Path |
|----------|------|
| Has `--bp` | Skip Chapter 3 (the user-given breakpoints are already a confirmed plan); go straight to Chapter 4 to connect |
| No `--bp`, has `--repo` | Full flow; Chapter 3 reads source to build the breakpoint plan |
| Neither | First ask the user for the repository path or breakpoint locations; do not guess class names out of thin air |
| Has `--manual` | After the breakpoint plan is determined per the three rows above, skip Chapters 4–7 and produce the command block per Chapter 10 |

---

## 2. Enabling JDWP on the Target JVM

The target JVM MUST be started with the JDWP agent; otherwise there is nothing to attach to.

```bash
# JDK 8
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar app.jar

# JDK 9+: address MUST include *:, otherwise it only listens on 127.0.0.1 (under zsh the whole argument MUST be double-quoted, see below)
java "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005" -jar app.jar
```

- `suspend=n`: the JVM starts normally without waiting for a debugger. `suspend=y` blocks at startup waiting for attach
- **Omitting `*:` on JDK 9+ is the most common reason a connection fails**: since JDK 9 the default binds loopback only, so remote attach gets connection refused
- **Conversely, JDK 8 does not support the `*:` syntax** and fails to start if you use it: `transport error 202: gethostbyname: unknown host`
  + `AGENT_ERROR_TRANSPORT_INIT(197)`. On JDK 8, `address=5005` already binds all interfaces
- **Under zsh, `address=*:5005` MUST have the entire `-agentlib:...` argument quoted**; otherwise `*` is treated as a glob,
  and with no match zsh reports `no matches found` and **aborts the whole command** (bash does not have this problem)
- A process that is already running **cannot have JDWP added**; it MUST be restarted with the argument
- **Target classes MUST be compiled with `-g` (including the local variable table); otherwise `locals` only returns
  `{"_error":"No debug info (compiled without -g)"}`**, and the core capability of viewing local variables is lost.
  Maven `maven-compiler-plugin` defaults to `<debug>true</debug>` and Gradle defaults to `debug = true`,
  so regular build artifacts qualify; jars produced with `-g:none` or by some optimization pipelines do not
- Verify the port is listening: `lsof -i :5005`
- If there is a firewall/security group between the target machine and this machine, the JDWP port MUST be opened to this machine

> [!WARNING] [SEC-UNAUTH:WARN]
> **The JDWP port has no authentication at all: anyone who can connect can execute arbitrary code and read/write arbitrary memory.** Enabling JDWP in production MUST satisfy one of the following:
> the port binds only to the internal network with a security-group IP allowlist; or it is not exposed and is accessed through an `ssh -L 5005:127.0.0.1:5005 <host>` tunnel.
> If the user gives a prod address, first ask them to confirm the above preconditions before continuing.

> [!WARNING] [SEC-UNAUTH:WARN]
> **jdi-client's own 15005 command port is likewise unauthenticated, and its threat level equals that of the JDWP port**: behind it is the full JDI control plane;
> a single `eval` can execute any method and read any memory in the target JVM, and a single `set-breakpoint` can freeze business threads.
> Therefore it is **hard-wired to bind `127.0.0.1` only, with no switch to open it up**, and every example in this chapter and the appendix uses `127.0.0.1:15005`.
> If you really need to drive it from another machine, forward it via an SSH tunnel: `ssh -L 15005:127.0.0.1:15005 <machine-running-the-client>`.

---

## 3. Code Analysis & Breakpoint Planning

Skip this chapter when the user has specified breakpoints with `--bp`: a breakpoint list given by the user personally is itself a confirmed plan, so Chapter 8's "breakpoints MUST be confirmed by the user" is already satisfied.
But if you want to **add** breakpoints beyond `--bp`, the added ones MUST still be shown first and confirmed.

### Step 3a. Locate the entry point

Based on the symptom the user describes (API path, exception stack, suspicious field name, error message text), search for the entry method under `--repo`. **Prefer the Grep / Glob tools**: they bypass the shell and have no permission friction:

- Search Controllers by API path: `Grep pattern="/api/order/query" glob="*.java"`
- Search for the throw site by exception class name or error message text
- Search for assignment sites by field name

When you MUST use shell grep, single-quote the glob; zsh's `NOMATCH` would otherwise expand an unquoted `*.java` first and abort the whole command:

```bash
grep -rn --include='*.java' '/api/order/query' /path/to/repo/src
```

After finding the entry point, read down the call chain: Controller → Service → external calls / data processing, and pin down the branches and assignment sites related to the symptom.

### Step 3b. Choose breakpoint locations

| Observation goal | Breakpoint type | Example |
|----------|----------|------|
| Confirm the request arrives | Method entry | `OrderController.query` |
| Observe arguments / return value | Method entry + `step over` | `OrderService.buildResponse` |
| Determine which branch is taken | Line breakpoint (on the `if` line) | `OrderService:87` |
| External call arguments and return | Line breakpoint at the call site | `InventoryClient:45` |
| Where the exception is thrown | Line breakpoint on the first line of the `catch` block | `OrderService:132` |

Selection principles: **the entry point is mandatory** (first confirm the request arrives, otherwise everything after is guesswork); no more than 3-4 breakpoints per round (`--max-bp` takes precedence when given), since more makes the hit order hard to reason about.

Line breakpoints require the target class to be compiled with debug info (`javac -g`, on by default in Maven). Without debug info, locals returns `_error: "No debug info"`.

### Step 3c. Show the plan and wait for user confirmation

```
Breakpoint plan:
1. [Entry] com.example.controller.OrderController.query — confirm the request arrives
2. [Logic] com.example.service.OrderService:123 — observe the assignment of the status field
3. [Call] com.example.client.InventoryClient:45 — external call arguments

After confirmation I will start the JDI Client and connect to the JVM.
```

> **Hard rule (MUST)**: you MUST show the breakpoint plan and obtain the user's explicit confirmation before entering Chapter 4. Do not start connecting and setting breakpoints on your own.

---

## 4. Connecting to the Remote JVM

Before starting, probe first to make sure 15005 has no leftover instance from a previous run:

```bash
curl -s -m 2 http://127.0.0.1:15005
```

There are three cases depending on the response; **do not treat "got a response" as a leftover instance across the board**:

| Response | Meaning | Action |
|------|------|------|
| Empty (connection refused) | Port is free | Start directly |
| JSON containing a `"connected"` field (e.g. `{"status":"ok","connected":true}`) | A leftover jdi-client instance, possibly connected to a different JVM | First wind it down per Chapter 7, then start |
| Anything else (HTML, other JSON, `Empty reply`, etc.) | The port is occupied by **another program**, not jdi-client | Do not "wind it down"; start with `--server-port 15006` instead and change the port in all later commands accordingly |

**Before starting, you MUST ensure the jar exists** (idempotent: returns immediately once the jar is built):

```bash
bash <SKILL_DIR>/scripts/ensure-jdi-client.sh
```

On success stdout is the jar path (`<SKILL_DIR>/scripts/jdi-client.jar`). If `scripts/jdi-client.jar` is missing, the script builds it from the bundled source `jdi-client/`: Maven (`jdi-client/build.sh`) first, falling back to the local JDK's `javac` + `jar` when Maven is absent or fails (e.g. offline). It needs a JDK, not just a JRE (`$JAVA_HOME/bin/javac` first, then `javac` on PATH; on JDK 8 `tools.jar` is added automatically). The jar is compiled to Java 8 bytecode, so it also runs on JDK 8 machines.
On a non-zero exit, relay the stderr to the user verbatim and stop; see Chapter 9.

**Start it with the Bash tool's `run_in_background: true`**, and record the returned shell id; Chapter 7 needs it for cleanup.

The start command **depends on the JDK version of the machine running jdi-client** (unrelated to the version of the target JVM being debugged; JDI can debug a JVM older than itself):

```bash
# JDK 9+: com.sun.jdi is already a built-in module, use -jar directly
java -jar <SKILL_DIR>/scripts/jdi-client.jar --server --server-port 15005 --host 10.0.1.5 --port 5005

# JDK 8: you MUST manually put tools.jar on the classpath and specify the main class explicitly
java -cp $JAVA_HOME/lib/tools.jar:<SKILL_DIR>/scripts/jdi-client.jar cn.ares.jvm.jdi.JdiClient --server --server-port 15005 --host 10.0.1.5 --port 5005
```

> **JDK 8 cannot use `java -jar`**: in JDK 8, `com.sun.jdi.*` lives in `tools.jar`, and `tools.jar` is not on the default classpath;
> it is `system` scope in the pom and is not bundled into the fat jar either. Plain `-jar` fails immediately on startup with
> `NoClassDefFoundError: com/sun/jdi/connect/IllegalConnectorArgumentsException`.
> If unsure of the version, run `java -version` first; on this machine you can also use `/usr/libexec/java_home -V` to pick the absolute path of a JDK 9+ to run it.
>
> **On JDK 9+, start with `java -jar`; do not switch to `-cp ... JdiClient`**: the jar's manifest carries `Add-Opens: jdk.jdi/com.sun.tools.jdi`,
> which the client relies on to pre-populate JDI's internal classloader cache. Otherwise, when eval invokes a method, JDI asks the target itself "who is this class's loader",
> and the target JDWP agent leaks a reference while handling that command, so the invoked class's classloader can never be collected until disconnect (old hot-deployed versions are never unloaded).
> When started with `-cp`, the manifest's Add-Opens does not take effect, and startup prints `warning: cannot open JDI's class loader cache`;
> if you really need `-cp`, add `--add-opens jdk.jdi/com.sun.tools.jdi=ALL-UNNAMED`. A JDK 8 client is not affected.

Startup parameters:

| Parameter | Default | Description |
|------|------|------|
| `--server` | — | Resident HTTP server mode; this skill always uses it |
| `--server-port` | `15005` | Command port. Switch to `15006` if occupied |
| `--host` / `--port` | — | JDWP address of the target JVM |

The command port is hard-wired to bind `127.0.0.1`; see the second security warning in Chapter 2 for why.

If `--server-port` / `--port` is not an integer, the client reports an error and exits immediately (`Invalid value for --server-port: 'abc' is not a port number (1-65535)`), rather than starting with a bad argument.

Fill in `--host` / `--port` with the literals the user gave. For the health check, use curl's built-in retries to wait for startup; do not use `sleep`:


```bash
curl -s --retry-connrefused --retry 5 --retry-delay 1 http://127.0.0.1:15005
```

Expect `{"status":"ok","connected":true}`.

> - `connected:false` → the target JVM does not have JDWP enabled or the port is unreachable; go back to Chapter 2 and check. If it turns `false` mid-debugging, the target has disconnected (see `VmDisconnected` in Chapter 9)
> - The process does not start at all → confirm `java` is on PATH and the jar path exists (read the background shell's output); if the jar is missing, run `ensure-jdi-client.sh` above first
> - **The response is not JSON like the above (e.g. a chunk of HTML)** → the command port is occupied by another program, and you are talking to that program.
>   The background shell output will contain `Failed to start HTTP server: Address already in use`. In this case jdi-client has already exited on its own and released
>   the JDWP connection, so no cleanup is needed; restart directly with `--server-port 15006` and change the port in all later commands accordingly

From then on, every operation is a JSON POST to this port, and the connection stays open:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"set-breakpoint","class":"com.example.Foo","method":"bar"}'
```

---

## 5. Setting Breakpoints

**Method-entry breakpoint**:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"set-breakpoint","class":"com.example.controller.OrderController","method":"query"}'
```

**Line breakpoint**:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"set-breakpoint","class":"com.example.service.OrderService","line":123}'
```

Response `{"status":"ok","bp_id":"bp-1","deferred":false,"installed":1}`:

- `installed` —— the number of JDI breakpoints actually installed. **When a class of the same name is loaded by multiple classloaders, or the method is overloaded, all candidates get one**;
  **a line breakpoint is installed at every executable location of that line** (a lambda on the same line, several methods written on one line, one line mapping to multiple bytecode ranges);
  otherwise execution reaching this line from the other locations would not hit.
  In that case `installed > 1` and the response carries an extra `candidates` array, each item being
  `{"location":"ClassName.methodSignature:line","class_loader_id":123,"class_loader":"java.net.URLClassLoader"}`
  (for a class loaded by bootstrap, `class_loader_id` is `"bootstrap"` and there is no `class_loader`). Hot-deployed copies have exactly the same `location` string;
  **distinguish them by `class_loader_id`**. If `installed` is larger than expected, the target is not unique (overloads / hot-deployed copies / inline lambdas); after a hit, use `location` to check which one you landed on
  (a lambda body shows as `ClassName.lambda$outerMethod$0...:line`).
  `installed` only counts the copies loaded at the moment of setting: **copies loaded later (hot deployment, same-name classes newly created by a plugin classloader) are also installed automatically**,
  until `clear-breakpoint`. HotSwap (IDE redefine) modifies the original class and creates no new copy, so the breakpoint stays effective.
  The client remembers every copy it has seen (for deduplication); with frequent hot deployment and a long session this record only grows: **after dozens to hundreds of consecutive hot deployments,
  `disconnect`, restart the client, and set the breakpoints again**; do not let one session span a whole day of repeated deployments
- `deferred:true` —— the class is not loaded yet; the breakpoint takes effect automatically when the class loads. **This is normal and is not an error**
- `status:"error"` —— the class name/method name/line number is wrong; check and set it again. The class name MUST include the full package name

> **`deferred:true` does not guarantee a hit.** After the class loads, installation fails if the method name is wrong, the line has no bytecode, or the class was not compiled with `-g`.
> Such failures are **not** pushed proactively; they are recorded in diagnostics instead: subsequent `wait-breakpoint` responses (including timeout responses) carry
> a `deferred_failures` array, **one entry per copy that could not be installed**, giving `bp_id` / `class` / `method` / `line` / `class_loader_id` / `class_loader` / `reason`.
> **When `wait-breakpoint` times out, the first thing to check is whether there are `deferred_failures`**; do not jump straight to Chapter 9's "the breakpoint is not on the execution path".
>
> The same applies to hot deployment: the breakpoint is installed on the old copy, but the newly deployed version has no code on that line (code changed, line numbers drifted), so the new copy shows up in
> `deferred_failures`. **The old copy is no longer being called, so this breakpoint is effectively dead**; reset the line number according to the new code.
> Each copy's failure record **is kept until that copy is unloaded**, and a successful install on another copy does not erase it: when multiple webapps / plugins run in parallel,
> the copy that failed to install may still be serving traffic. The cost is that with serial hot deployments, old versions keep being listed as long as they have not been unloaded by GC: compare against the
> `class_loader_id` of the hit frame to tell which copy is serving traffic. At most the latest 10 entries are kept per breakpoint.

> **To see local variables declared inside the method body, use a line breakpoint placed after their assignment statement.** A method-entry breakpoint stops at the first line of the method body
> **before it executes**, so at that point `locals` contains only the arguments; variables in the method body are not in scope yet. Measured: in `hello(String name)` with
> `String msg = ...`, when the method-entry breakpoint hits, `locals` is only `{"name":"\"world\""}`; `msg` appears only after one
> `step`. When a method-entry breakpoint has already hit, you can also use `step` to advance one step instead of resetting the breakpoint: the `step` response carries `locals` itself.

After setting, notify the user:

```
Breakpoints are set. Please trigger the target request once.
```

---

## 6. Waiting for Hits & Collecting State

### Step 6a. Wait for a hit

**Run it with `run_in_background: true`**; it blocks until a hit or timeout:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"wait-breakpoint","timeout":180}'
```

> When `timeout` is short (≤20s, e.g. when you can trigger the request yourself right away) you may also call it synchronously, but the Bash tool's
> `timeout` MUST be set longer than it; otherwise the tool times out first, curl is interrupted, and the hit event is wasted.
> For scenarios where it is uncertain when the hit will come, such as waiting for the user to trigger the request manually, always use `run_in_background`.

> **Both curl's `-m` and the Bash tool timeout MUST be greater than the server-side `timeout`**. When curl is killed early the server does not notice,
> and that wait is still waiting on the server: if a hit happens right then, the event is written to a connection that is already closed, **so this hit is lost while the thread stays frozen**.
> The client has two safety nets for this: ① **only the latest `wait-breakpoint` is live**; as soon as a new wait arrives, the old wait immediately returns
> `Superseded` (the killed curl never receives it, harmless), and later hits go only to the new wait; ② the lost thread appears in the `frozen_threads` of a subsequent
> `wait-breakpoint` **timeout** response (see below). Opening two wait-breakpoints at the same time is pointless;
> the earlier one gets pushed out.

The hit response automatically carries stack + locals, no extra command needed:

```json
{
  "status": "ok",
  "event": "breakpoint-hit",
  "thread_id": 42,
  "thread_name": "http-nio-8080-exec-10",
  "bp_id": "bp-1",
  "location": {"class": "OrderController", "method": "query", "line": 35, "source": "OrderController.java", "class_loader_id": 18},
  "stack": [
    {"class": "OrderController", "method": "query", "line": 35, "source": "OrderController.java", "class_loader_id": 18},
    {"class": "DispatcherServlet", "method": "doDispatch", "line": 1084, "source": "DispatcherServlet.java", "class_loader_id": 18}
  ],
  "locals": {
    "request": "org.apache.catalina.connector.RequestFacade@123",
    "dto": "com.example.OrderQueryDTO{id=456, status=\"CLOSED\", tags=java.util.ArrayList@789}"
  }
}
```

> **Hard rule (MUST)**: `thread_id` MUST be taken from this response, and all subsequent commands use it. Do not guess it, do not hard-code it, and do not reuse the previous round's value: each hit may be on a different thread.

> **Objects in `locals` are field trees, not `toString()`**: the format is `ClassName{field=value, ...}`, expanded to depth 2;
> when depth is exhausted or there are too many fields it degrades to `ClassName@id` / `... (n fields total)`. **The target object's `toString()` is never called**
> (to avoid executing business code on the automatic path); if you want its result, explicitly `eval "dto.toString()"`. See the last part of the "Rebuilding the jar" section for details.

> **`dropped_events` in a response means the scenes retained by the client have reached the 64-entry cap** (including hits queued for pickup + threads already handed to you but not resumed):
> hits beyond the cap no longer have their scene collected (not even `suspend()` is done; they are handed straight to the event loop to be released), so the scenes of those hits are lost.
> The accompanying `dropped_hint` explains this.
> Action: first resume the threads you have finished inspecting, then consider moving the breakpoint to a colder path. It is a correctness hint, not an error:
> the scene you did get is real; you just **cannot** infer from it that "this breakpoint was hit only once".
> `frozen_count` in the response is the number of scenes the client currently retains (including the one returned this time); use it to check how many resumes you owe.
>
> **Note that this 64 only bounds how many scenes the client retains, not how many threads the target suspends at once**: on the target side JDWP means "the thread that produced the event
> is suspended immediately". During a concurrent hit storm all hit threads are suspended together and queue up in the target's EventQueue, and these queued threads are **not** in the client's
> count (the client has not fetched their events yet). Measured: with 160 threads hitting at once, the target's simultaneous suspensions reached 160 while `frozen_count` reported only 64.
> In other words: this cap guarantees that "wait for one, do not resume, wait again" will not drain the thread pool indefinitely, but it **cannot** guarantee that the target's simultaneous suspensions
> stay at or below 64. Setting a hot breakpoint on a highly concurrent target can still suspend a large number of threads instantly; that is exactly what "a hot breakpoint is equivalent to gradually freezing the thread pool" below guards against.

> **`frozen_threads` in a timeout response means some threads were "reported but not released"**: the listed threads were previously handed out by some wait / step,
> are still frozen, and nobody has resumed them. Usually curl was interrupted so that response was lost, or it is a late
> step result after a step timeout. They will not be returned again as new hits. Action: for each `thread_id` in the list, first `stack` / `locals` to view the scene (the scene is real),
> then `resume` them one by one. `frozen_hint` reminds you of this.

### Step 6b. Collect runtime state

**Local variables** (omit `frame` for the current stack frame; `frame:1` is the caller's stack frame):

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"locals","thread_id":42}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"locals","thread_id":42,"frame":1}'
```

> **Collections and Maps are also expanded by field**, so what you see is the implementation class's internal structure, not a list of elements: `ArrayList` shows
> `size` and the `elementData` array (the array itself is expanded; `null` slots are reserved capacity, not data),
> and `HashMap` shows `size` and the `table` array, plus useless fields like `modCount` / `threshold` / `loadFactor`.
> **Judge a collection's size by the `size` field**; do not count the length of `elementData`.
> For a clean element view, explicitly `eval "list.get(0)"` / `eval "map.get(\"key\")"` / `eval "list.toString()"`.

**Expression evaluation** (equivalent to IDEA's Evaluate Expression):

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"dto.getUrl()"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"this.config.getTimeout()"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"request.getHeader(\"x-user-id\")"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"list.get(0)"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"map.get(\"key\")"}'
```

eval supports: local variables `varName`; field access `this.field`, `obj.field`; method calls `obj.method()`, `obj.method("arg")`, `obj.method(1, "str")`; chained calls `request.getHeader("key").toLowerCase()`; literal arguments (string / integer / `true` / `false` / `null`); **static methods and static fields**: write the fully qualified class name (`java.lang.management.ManagementFactory.getRuntimeMXBean().getName()`) or the simple name of a `java.lang.*` class (`Thread.currentThread().getName()`); **the class MUST already be loaded in the target JVM**.

> When the class is not loaded, it reports `IllegalArgumentException: Cannot resolve: <first segment>` (e.g. `Cannot resolve: java`). The wording **does not say "class not loaded"** and is easily mistaken for a syntax error: do not keep rewriting the expression and retrying; switch to a class that is already loaded or fetch the value from the instance side.

> **When a class of the same name has multiple copies (hot deployment, multiple webapps, plugin classloaders), a static call does not just pick one at random**:
> with only one copy it uses that one; with several it takes the one visible to the classloader of the class of the current stack frame; if it still cannot tell, it returns
> `AmbiguousClass` + `candidates` (each item `class` / `class_loader_id` / `class_loader`). In that case specify it explicitly with `class_loader_id`:
>
> ```bash
> curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"Hot.VAL","class_loader_id":95}'
> ```
>
> `class_loader_id` comes from `candidates`, the hit response's `location`, or any frame in `stack` (to target "the copy currently running", use the value from the hit frame);
> for a class loaded by bootstrap write `"bootstrap"`. If the specified loader has no such class it reports `ClassLoaderMismatch` (also with `candidates`).
> It **only affects resolution of the class name at the start of the expression**; expressions starting with a local variable / `this` ignore it.
> Stack-frame visibility only covers classes that classloader has already resolved; a copy the code has never touched is invisible, which also yields `AmbiguousClass`; specify it explicitly as above.

> **Static method calls no longer pin the invoked class's classloader in the target**: on JDK 9+ targets, `Cls.m(...)` goes through a method handle instead
> (only for classes in non-built-in classloaders), and every call the client issues is on bootstrap classes, so it never reaches the reference-leaking
> static invoke command in the target agent (`check_methodClass` in `invoker.c`: it takes a JNI local reference to the declaring class without releasing it, so the invoked class together with its loader
> stays around until `disconnect`). Therefore, with repeated hot deployments and repeatedly created classloaders, old copies can unload normally as long as business code no longer references them,
> and there is no need to restart the client for this.
> The handle comes from `MethodHandles.Lookup.IMPL_LOOKUP` (read as a field, without any access check): its `findStatic(class, methodName,
> methodType)` is the fully trusted lookup the JDK opens for itself; unexported modules, non-public members, and a SecurityManager that denies reflection cannot block it,
> matching the permissions of JDWP's own invoke. The method type is constructed once by the target with `MethodType.fromMethodDescriptorString(methodDescriptor, invokedClassLoader)`,
> and the cost does not depend on how many methods the class declares.
> The return value is captured within the call itself: the handle's return type is widened to `Object`, then `filterReturnValue` attaches an `arrayElementSetter` writing into an `Object[1]` (already
> held via `disableCollection`), so during invoke the target writes the value into memory the client already holds; after the call a single
> command reads it back, and there is no window in which "the return value is unreferenced between two commands and gets collected".
> Argument and return-value semantics match the original path item by item: literals can only go into primitive parameters, strings only into parameter types they are assignable to (`String` / `Object` /
> `CharSequence`, etc.), `null` only into reference-type parameters; on mismatch the error is the same as the original path (and nothing gets pinned); a single `null` argument is
> one `null` parameter; for varargs methods the trailing argument is packed into a one-element array by the original path's rules, and passing `null` as the trailing argument makes the whole array `null`;
> `void` methods return `void`, primitive return values are not boxed, and exceptions thrown by the target method are reported as is.
> Objects temporarily created in the target by the method-handle route (boxed arguments, argument array, method type, method handle, capture array) are all held with `disableCollection`
> until the call returns; if any is still collected meanwhile, the whole thing is retried (at most 3 times).
> Reading static fields (`Cls.FIELD`), instance method calls (`obj.m()`), static calls on bootstrap classes such as `java.lang.*`,
> classes in the two built-in classloaders app / platform (they are never unloaded, so pinning is harmless; the JDK's own caller-sensitive methods also live only in these
> loaders, and going through the original path keeps caller semantics unchanged), and JDK 8 targets all take the original path, with unchanged behavior.
> Only on unexpected failure (no `IMPL_LOOKUP` in the JDK, objects collected 3 times in a row) does it fall back to the original path; the result is unaffected, but that copy stays until
> `disconnect`, and the client log has a line `warning: cannot route the static call to ...`; when investigating a classloader
> leak in the target, check first whether it appeared.

> **Object GC protection is best-effort per path, not a whole-path guarantee**: on the handle route, the return value is written by the target into an array the client already holds within the invoke itself,
> so **there is no window**; but the two paths below use JDWP's native invoke, where the return value has a **cross-command window** between "the method finishes → the client then sends `disableCollection`",
> which the client cannot close and cannot retry either (the target method may have side effects):
> - **Static direct fallback**: static calls on bootstrap classes such as `java.lang.*`, classes in the two built-in classloaders app / platform, JDK 8 targets,
>   and when the "unexpected fallback" above happens;
> - **Instance method calls**: things like `obj.m()` and `list.get(0)`, **all** of which use native invoke.
>
> If the target is running **high-frequency full GC** in the background and the invoked method returns a **new object with no other target-side references**, that object may be collected within this window,
> and that eval reports `EvalError: ObjectCollectedException`. The deciding factor is the target's GC intensity: it does not occur under normal GC (measured: 200/200 passed under mild GC;
> under a full GC every 1ms, the instance chain `a().b().c()` failed about 10%~20%, with each instance method call on the chain introducing its own window). If you hit it, retry the eval once (read operations are replayable), or first confirm the target is not in
> a GC storm caused by a leak/memory alert. **Do not** switch to retrying the target business method: that may repeat side effects.
> Reading static fields and **bulk expansion** of collection/object fields behave the same way: when concurrent writer threads replace fields/elements, an old value already read may lose its reference during formatting.
> The resulting shape depends on which level is lost: either **the whole eval reports `ObjectCollectedException`** (the root object or an array element was lost),
> or **an object at some level degrades from its expanded form to `type@id`** (the parent object's `referenceType()` failed and it degraded to a field-less placeholder).
> **Partial nodes like `<collected>` are currently not returned**: either the whole thing fails, or that level degrades. This is likewise only visible when the target is concurrently rewriting + under high-frequency GC at the same time.

> **Method arguments can only be literals**: `map.get("key")`, `f(1)`, `f(true)`, `f(null)` work;
> something like `map.get(someKeyVar)` with **a variable-name argument errors out directly** (`Cannot parse argument`); it is not silently passed in as the string `"someKeyVar"`.
> To use a variable's value as an argument, first view its actual value via `locals`, then fill that literal into the expression.

> **String literal escapes are parsed by Java rules, and the leading segment of an expression and its arguments use the same rules** (they used to differ: `"a\"b".length()` and
> `len("a\"b")` once gave 4 and 3 respectively). Supported escapes: `\"`, `\\`, `\n`, `\t`, `\r`, `\b`, `\f`. Hence
> **`"\\n"` is the two characters "backslash + n"** (not a newline), `"C:\\temp"` is a Windows path, and `"\\t"` is "backslash + t".
> **Unsupported escapes error out directly** with `Unsupported string escape: \x`, and the backslash is **not** kept as is: silently keeping it would make eval look up
> a value different from what the caller wrote. A single trailing backslash at the end of a literal reports `Trailing backslash in string literal`.
> Note that `\` is an escape character only inside string literals: in JSON it MUST be written as `\\`, e.g. `{"expr":"\"\\\\n\".length()"}`.

> **Overload ambiguity also errors out**: when matching by argument count finds multiple overloads, it returns `EvalError` and lists the candidate signatures; it will not pick one for you.
> In that case use field access instead, or switch to an overload whose argument count is unique.

> **Hard rule (MUST)**: Do not eval methods with side effects: writing to the DB, sending MQ, changing state, clearing caches. Evaluation really executes in the target JVM, and side effects are irreversible. Only read-only getters and pure functions are safe.

> **`obj.foo` is not necessarily a field read**: when field `foo` is not found it automatically falls back to calling `obj.getFoo()`. It looks like a field read but may actually run
> business code (lazy loading that triggers SQL, getters that populate caches). Be especially careful with ORM entities and proxy objects; when unsure, check field names with `locals` first.

> **eval hangs when the invoked method contains a breakpoint**: after the invoked method hits the breakpoint the thread freezes there, and this eval's curl never returns
> (JDI method invocation has no timeout). That hit is reported by `wait-breakpoint`; `resume` that thread once and the eval continues and returns its result;
> afterwards the thread is **back at its original breakpoint and still frozen** (`frozen_threads` lists it); resume it as usual when done. To avoid this, `clear-breakpoint` first and then eval.
> When testing locally, note: sending SIGTERM to the target process while an eval is still stuck in the target may leave HotSpot hung halfway through exiting (measured on Zulu 8), requiring `kill -9`;
> do not let a production target get to this point; resume / `disconnect` first.

> The client has a built-in **hard deny list**: `System.exit`, `Runtime.exit` / `halt` / `exec`, `ProcessBuilder.start`,
> `Thread.stop` / `suspend`; calling them returns `EvalError: Refusing to invoke ...`. It only guards against slips (one eval crashing the target
> JVM or spawning a child process); it is **not a sandbox**: other methods with side effects can still be called, and the hard rule above is still yours to uphold.

**Full call stack**:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"stack","thread_id":42}'
```

### Step 6c. Single-stepping

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"step","thread_id":42,"type":"over"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"step","thread_id":42,"type":"into"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"step","thread_id":42,"type":"out"}'
```

| type | IDEA equivalent | Description |
|------|---------------|------|
| `over` | Step Over | Execute the next line without entering methods |
| `into` | Step Into | Enter the method |
| `out` | Step Out | Finish the current method and return to the caller |

The response automatically carries the stack + locals at the new location, and reports which thread completed the step:

```json
{
  "status": "ok",
  "event": "step-complete",
  "thread_id": 42,
  "thread_name": "http-nio-8080-exec-10",
  "location": {"class": "OrderService", "method": "buildResponse", "line": 124, "source": "OrderService.java"},
  "locals": {"text": "\"HELLO\"", "number": "72"}
}
```

After a step the thread stays frozen; no manual suspend / resume is needed.

> **When a step meets a breakpoint, look at `event` and `bp_id`**:
> - `event:"step-complete"` with `bp_id` —— the step landed exactly on a breakpoint line; both facts are reported only this once and will not be returned again by `wait-breakpoint`
> - `event:"breakpoint-hit"` —— the step ran into a different breakpoint along the way (typically one inside the method that `over` steps across); **this step ends here**,
>   and the thread is frozen at the `bp_id` breakpoint, consistent with IDEA. The original step has been cancelled, so a later resume will not freeze at the next line again

> **Concurrent hits do not cross threads during a step**: if other threads hit breakpoints while waiting for the step result, those events stay in the queue in their original order
> and are later taken by `wait-breakpoint`; step only returns events of **the thread you specified**.
> Even so, **always check that the `thread_id` in the response matches the one you requested**: it is the only evidence that no cross-thread mixup happened.
> Conversely, a `wait-breakpoint` running in the background cannot take the result of a thread that is stepping either.
>
> **Only one step at a time per thread**: sending another step to a thread whose previous step has not returned immediately gets
> `StepFailed: Another step is already in progress on thread: <id>`, and the previous one is unaffected. Wait for it to return before sending the next.
> Different threads can step concurrently.

> **After a `step` timeout the thread state depends on the message; you MUST read it**:
> - `...Step request cancelled, the thread was left running` —— the request was cancelled and the thread kept running; **do not** resume it again
>   (it is no longer at a breakpoint; `resume` would answer `note: Thread was not suspended`)
> - `...the thread is frozen at the next line and still needs an explicit resume; wait-breakpoint will report it`
>   —— the step event arrived right at the timeout and still was not delivered to this step within the 10s grace period. The thread **is frozen at the next line**,
>   and that late step-complete will be returned by the next `wait-breakpoint` (`event:"step-complete"`); you MUST explicitly `resume` it,
>   otherwise this business thread stays hung
>
> If the step event arrives right at the timeout but is delivered within the grace period, it is returned directly as a normal step result, with no timeout reported.
>
> A step times out when the thread is stuck on a remote call / lock / IO; you can pass a larger `timeout` (seconds) to `step`.

### Step 6d. Multi-breakpoint loop

Resume the current thread and continue to the next breakpoint:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"resume","thread_id":42}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"wait-breakpoint","timeout":180}'
```

New breakpoints can be added at any time while running without affecting already frozen threads: the command port uses a thread pool, so while `wait-breakpoint` is blocking,
`set-breakpoint` / `clear-breakpoint` / `threads` / `locals` are still handled concurrently (just run `wait-breakpoint`
in the background).

> **At most 2 `step` / `eval` run at the same time**; a 3rd immediately returns `Busy` (with `in_flight` listing the running commands and threads).
> This keeps a worker thread always available for `resume` / `disconnect`: a stuck eval (hit a breakpoint inside the method, waiting on a lock) cannot drag down the whole command port.
> On `Busy`, first `wait-breakpoint` to see whether an eval hit a breakpoint, resume the thread it reports, then retry.

> A `resume` response may carry `note: "Thread was not suspended, nothing to resume"`. **This is ok, not an error**:
> one resume clears all of the thread's suspend counts, so repeated resumes, or resuming a thread that is already running, are safe idempotent operations.
> The real error is `InvalidThread` (the thread ID does not exist).

> `resume` / `step` **discard the thread's events still in the queue that have not been taken**: once the thread runs, the frozen locations and locals those events describe are stale,
> and keeping them would only get them reported later as new hits. So for multiple hits accumulated on the same thread, after resume only the new event from its next real arrival at a breakpoint remains.

### Step 6e. Iterative debugging

After a round of collection, if the information is not enough to locate the root cause:

1. Analyze based on the state obtained so far and decide what to observe in the next round
2. Clear the breakpoints no longer needed: `curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"clear-breakpoint","bp_id":"bp-1"}'`
3. Set new breakpoints (back to Chapter 5)
4. `resume` the current thread
5. Notify the user to trigger the request again
6. `wait-breakpoint` (back to Step 6a)

Termination conditions (stop when any is met):

- The root cause has been located (abnormal variable value, deviated execution path, clear exception throw site)
- 3 consecutive rounds without new information —— the breakpoints are aimed in the wrong direction; stop and re-analyze instead of adding more breakpoints
- The user terminates actively

> Every iteration MUST explain two things to the user: why the current information is insufficient, and what the new breakpoints will observe.

---

## 7. Ending Debugging & Reporting Conclusions

### Step 7a. Disconnect

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"disconnect"}'
```

After disconnect, all frozen threads in the remote JVM resume automatically. Then stop the background process started in Chapter 4: **use the TaskStop tool to stop the recorded shell id**.

> Do not write `kill %1`: each Bash call is an independent shell, and the job table does not persist across calls, so `%1` does not exist in a new shell.
> If you lost the shell id, first get the pid with `pgrep -f jdi-client.jar`, then `kill <pid>` (`pkill` is often blocked by permission policies).

> **Hard rule (MUST)**: whether it ends normally, fails midway, or is interrupted by the user, you MUST send disconnect first. Skipping it leaves the target JVM's business threads frozen on breakpoints indefinitely; in production that means piled-up request timeouts.

### Step 7b. Report conclusions

```markdown
## Debugging Conclusion

### Execution Path
1. OrderController.query() — request arrived normally
2. OrderService.buildResponse():123 — status field value is "CLOSED"
3. InventoryClient.getStock() — not called (short-circuited)

### Variable Snapshot
| Breakpoint location | Variable | Actual value | Note |
|---------|------|--------|------|
| OrderService:123 | order.status | "CLOSED" | Order status causes an early return |
| OrderService:125 | shouldCallInventory | false | Inventory query skipped because status=CLOSED |

### Root Cause
The status check at OrderService:120-126 skips the inventory query and returns directly when status="CLOSED",
so the response is missing the stock field.

### Recommendation
(Fix or workaround mapped to specific code locations)
```

Conclusions MUST be based on variable values actually collected. Write "not observed" for any step that was not observed; do not fill it in with speculation.

---

## 8. Constraints & Safety

- **prod environment**: before connecting to a production JVM, explicitly tell the user that the business thread hitting a breakpoint will be frozen. The impact of a single `SUSPEND_EVENT_THREAD` hit
  is indeed far smaller than jdb's `SUSPEND_ALL`, but **this "smaller" only holds for "a single hit + a timely resume"**; the two items below amplify it
- **Impact spreads when a frozen thread holds a lock**: if the frozen thread holds a `synchronized` monitor, a database connection, or a slot in a connection pool,
  every thread contending for the same resource blocks along with it. The impact grows from "one request hangs" to the whole service being unavailable,
  and **you cannot tell** from the frozen thread's stack who is waiting on it. In prod, place breakpoints at lock-free locations (entry points, pure computation sections) whenever possible,
  and keep freeze time as short as possible
- **A hot breakpoint is equivalent to gradually freezing the thread pool**: each hit of the breakpoint freezes one thread, and without resume they accumulate. When set on a hot path
  (loop bodies, utility methods every request passes through), the target service's worker threads are drained step by step, showing up as piled-up request timeouts.
  The client has a 64-entry **scene retention** cap as protection; the count includes **hits queued for pickup + threads already handed to you but not yet resumed**,
  so "wait for one, do not resume, wait again" hits the cap as well; beyond the cap, new hits no longer have their scene collected and the response reports `dropped_events`,
  but **dropping events is a protective action, not a normal state**; when you see it, first resume the threads you are done with, then consider moving the breakpoint.
  This cap **does not bound the target's simultaneous suspensions**: on the target side JDWP suspends the event-producing thread immediately, and with concurrent hits all hit threads are
  suspended together and queued in the target's EventQueue, outside the client's count (measured: 160 threads hitting at once → 160 suspended at once on the target, while the client reported only 64).
  In other words, it stops "slowly draining without resume" but not the instant shock of "a burst of concurrent hits"; the latter can only be prevented by placing breakpoints on cold paths.
  `frozen_count` in the `wait-breakpoint` response is the number of scenes the client currently retains (including the one returned this time); if it keeps rising, some thread was forgotten and not released.
  In prod, start with cold-path breakpoints with clear conditions
- **An explicit resume is still REQUIRED after a timeout**: a `wait-breakpoint` / `step` timeout **only means the command returned; it does not automatically resume any thread**.
  After a timeout, first look at `frozen_threads` in the response, then use `threads` to check for threads with `suspended:true`, and `resume` them one by one (idempotent, extra sends are harmless),
  or simply `disconnect` as a fallback
- **The JDWP port has no authentication**: see the security warning in Chapter 2; prod MUST have an IP allowlist or an SSH tunnel
- **The 15005 command port is likewise unauthenticated**: it is hard-wired to bind loopback; use an SSH tunnel across machines (see the second warning in Chapter 2)
- **MUST disconnect**: when debugging ends (including error paths) you MUST disconnect; otherwise threads stay frozen
- **Breakpoints MUST be confirmed by the user**: before setting breakpoints, show the plan and wait for confirmation
- **Do not change runtime state**: do not eval methods with side effects. `locals` auto-expansion only reads fields and **does not call `toString()`**,
  so a breakpoint hit by itself does not execute business code
- **Do not leak sensitive data**: `locals` / `eval` results from authentication, payment, or user-privacy-related stack frames may contain tokens, ID card numbers,
  bank card numbers, or plaintext passwords; **do not paste them verbatim into the conversation, conclusion documents, or logs**; reference only the fields needed for diagnosis, and mask them
- **Timeout protection**: `wait-breakpoint` defaults to 180s and `step` to 30s; on timeout they return an error instead of hanging forever

---

## 9. Error Handling

| Error | Meaning | Action |
|------|------|------|
| `ensure-jdi-client.sh` reports `javac not found` / `tools.jar not found` / `build failed` | The jar could not be built locally: only a JRE is installed, JDK 8 lacks `tools.jar`, or compilation failed (the Maven/javac output is in stderr) | Install a JDK or point `JAVA_HOME` at one, then rerun the script. Do not start jdi-client until the script exits 0 |
| `NoClassDefFoundError: com/sun/jdi/...` | jdi-client was started with `java -jar` on JDK 8 | See Chapter 4: JDK 8 MUST use `-cp $JAVA_HOME/lib/tools.jar:...` and specify the main class |
| `ConnectFailed` | Cannot connect to the remote JVM. Connection setup and the JDWP handshake each have a 10s limit; distinguish by message: `Connection refused` means the port is not listening; `attach timed out` means the network is unreachable / packets are dropped by a firewall; `handshake timed out` means the port is reachable but the peer is not JDWP or the target JVM is stuck; `connection closed by the target` / `not a JDWP agent` means the port is occupied by another service | Check the JDWP arguments (especially JDK 9+'s `address=*:`), the port, and network connectivity |
| `Timeout` | Breakpoint not hit | ① First check the response for `deferred_failures` (the breakpoint was never actually installed) and `frozen_threads` (threads reported but not released; resume them one by one); ② confirm the request was triggered; ③ the breakpoint is not on the actual execution path; move it. For `step` timeouts see Step 6c; judge from the message whether the thread is still frozen |
| `Superseded` | A newer `wait-breakpoint` took over | Normal: only the latest wait receives hits at any moment. Do not open multiple waits concurrently |
| `VmDisconnected` | The remote JVM disconnected or exited unexpectedly | Message `Remote JVM exited` means the target exited normally (`System.exit`, SIGTERM, end of main); `Remote JVM disconnected` means the connection broke (kill -9, network). It may have been restarted/killed. At this point the health-check GET shows `connected:false`; once the target is back up, just send `connect` to reconnect (the old connection and event loop are cleaned up first), and breakpoints MUST be set again. When the peer disappears silently (no FIN/RST), the disconnect only shows after the next command fails |
| `Busy` | 2 `step` / `eval` are already running | See Step 6d: `in_flight` lists the occupants; first `wait-breakpoint` + resume the stuck thread, then retry |
| `AlreadyConnected` | `connect` was sent while the connection is still alive | It does not silently reconnect (old connection leak + two event loops competing for events). To switch targets, `disconnect` first; this error is not reported when the target has already disconnected |
| `ShutdownPending` | On reconnect, the previous connection's event loop did not exit within 3s | Very rare. Resend `connect` after a few seconds; if it keeps happening, `disconnect` and restart the client |
| `AmbiguousClass` | The static class name in eval maps to multiple loaded copies, and the current stack frame cannot tell which to use | Pick a `class_loader_id` from `candidates`, add it to the eval request, and resend; see Step 6b |
| `ClassLoaderMismatch` | The `class_loader_id` specified in eval has no such class | Switch to a value listed in `candidates` |
| `InvalidThread` | The thread ID does not exist | Use the `thread_id` from the hit response; do not use old values. Note that `resume` on an already running thread returns `ok` + `note`, not this error |
| `InvalidArgs` | Missing argument or wrong type | Integer arguments always reject decimals instead of truncating (`thread_id:42.9`, `line:3.9` both error); `max_frames` limited to 1~500; `timeout` limited to 1~3600; `line` ≥ 1; `port` limited to 1~65535; `frame` ≥ 0 |
| `ParseError` | The request is not valid JSON | Check quote escaping in `-d`. Numbers out of double range like `1e309`, extra content after the JSON, nesting deeper than 64 levels, illegal escapes like `\e`, `\u` not followed by 4 hex digits, and unescaped control characters inside strings (including raw newlines / Tabs) are all rejected |
| `UnsupportedMediaType` (HTTP 415) | POST without a JSON Content-Type | Add `-H 'Content-Type: application/json'` to curl |
| `ForbiddenHost` / `ForbiddenOrigin` (HTTP 403) | Host is not 127.0.0.1 / localhost, or the request carried an Origin | Connect directly via `http://127.0.0.1:<port>` (including the local end of an ssh -L tunnel); do not access it through a browser or with a custom Host |
| `BodyTooLarge` (HTTP 413) | Request body exceeds 1 MB | Command JSON should never be this large; check whether file content was spliced into `-d` |
| curl gets an empty response / connection closed | The request was not fully sent within 30s | The command port has a 30s deadline for "receiving the request" (to prevent slow connections from exhausting worker threads); it does not affect `wait-breakpoint` long polling. Normal curl usage never triggers it; to relax it, add `-Dsun.net.httpserver.maxReqTime=<seconds>` at startup |
| `EvalError` | Expression execution failed | Check syntax, whether the variable is in the current scope, and whether the method signature matches. Arguments can only be literals; overload ambiguity lists the candidates |
| `EvalError` + `Unsupported string escape: \x` | An unsupported escape was used in a string literal | Only `\"` `\\` `\n` `\t` `\r` `\b` `\f` are supported. For a literal backslash write `\\`; a lone trailing `\` reports `Trailing backslash in string literal` |
| `EvalError` + `ObjectCollectedException` | Under high-frequency full GC on the target, a return value/field value was collected in the cross-command window | See the GC protection notes in Step 6b: retry the eval once (read operations are replayable); **do not** retry a target method that has side effects |
| `BreakpointFailed` | Breakpoint setup failed | Check the fully qualified class name, method name, and line number |
| locals shows `_error: "No debug info"` | Compiled without `-g` | Variable names were erased or code was inlined; use field/expression evaluation instead, or have the target recompiled with `-g` |

---

## 10. No Direct Connection: Producing a Command Block for Manual Execution on the Target (`--manual`)

When this machine cannot reach the target JDWP (JDWP is open only to the target machine or a jump host, or the production network is isolated), jdi-client is instead run **by the user on the target machine (or a jump host that can reach the target)**.
This skill executes no commands; it only fills in the template below according to the confirmed breakpoint plan and hands it to the user (or to the caller to embed in its observation request).

- Replace `<JAR>` with the actual path on the target machine; use `--wait-timeout` for `<timeout>`, or 180 if not given
- Write one `set-breakpoint` per breakpoint in the plan, with no more than `--max-bp` entries
- For the start command in step 2, pick one of the two according to the **target machine's** JDK version, using the same rules as Chapter 4

````
# 0. Build jdi-client if missing, then copy it to the target machine (run on this machine)
bash <SKILL_DIR>/scripts/ensure-jdi-client.sh
scp <SKILL_DIR>/scripts/jdi-client.jar <user>@<host>:/tmp/jdi-client.jar
# 1. Confirm JDWP is listening (if not enabled, the JVM MUST be restarted with -agentlib, see Chapter 2)
#    JDK 9+: write address=*:<port> (under zsh the whole -agentlib argument MUST be double-quoted, otherwise * is eaten by glob)
#    JDK 8: write address=<port>; JDK 8 does not support the *: syntax and would report gethostbyname: unknown host
lsof -i :<jdwp_port>
# 2. Start jdi-client (on JDK 8 use -cp $JAVA_HOME/lib/tools.jar:<JAR> cn.ares.jvm.jdi.JdiClient instead; java -jar does not work)
java -jar <JAR> --server --server-port 15005 --host 127.0.0.1 --port <jdwp_port>
#    Health check in another terminal, expect {"status":"ok","connected":true}; on connected:false go back to step 1 and check JDWP
curl -s --retry-connrefused --retry 5 --retry-delay 1 http://127.0.0.1:15005
# 3. Set breakpoints; POST MUST carry Content-Type, otherwise HTTP 415
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"set-breakpoint","class":"<fully-qualified-class-name>","line":<line>}'
# 4. Wait for a hit after triggering the request; the hit response carries stack + locals, paste the whole thing back
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"wait-breakpoint","timeout":<timeout>}'
# 5. Release and disconnect immediately (thread_id is the value from the previous step's response); disconnect MUST be run regardless of success or failure
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"resume","thread_id":<id>}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"disconnect"}'
````

After the user pastes the output back, interpret the responses per Chapter 6 and report conclusions per Step 7b; if the hit response's `locals` is `_error: "No debug info"`, see Chapter 9.

---

## Appendix: JDI Client Command Reference

> All commands: `curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '<JSON>'`. GET `/` is the health check.
> POST MUST carry `-H 'Content-Type: application/json'` (otherwise HTTP 415 `UnsupportedMediaType`); `Host` only accepts 127.0.0.1 / localhost, and any request carrying an `Origin` header gets 403. This blocks browser pages (cross-site POST, DNS rebinding); normal curl usage is unaffected.

### Connection management

| Command | Purpose |
|------|------|
| `{"cmd":"connect","host":"...","port":5005}` | Connect to the remote JVM (reports `AlreadyConnected` if already connected) |
| `{"cmd":"disconnect"}` | Disconnect and exit (all frozen threads resume automatically) |

### Breakpoint management

| Command | Purpose |
|------|------|
| `{"cmd":"set-breakpoint","class":"...","method":"..."}` | Method-entry breakpoint |
| `{"cmd":"set-breakpoint","class":"...","line":123}` | Line breakpoint |
| `{"cmd":"clear-breakpoint","bp_id":"bp-1"}` | Delete the specified breakpoint |
| `{"cmd":"wait-breakpoint","timeout":180}` | Wait for a hit (blocking, default 180s, 1~3600) |

> `wait-breakpoint` responses (both success and timeout) may carry two diagnostic fields: `deferred_failures` (why the breakpoint could not be installed on some loaded copies, one entry per copy) and
> `dropped_events` + `dropped_hint` (the scenes retained by the client exceeded the 64-entry cap, and the extra hits were released without collecting their scene). Check both; see Chapter 5 and Step 6a.
> When threads are frozen it also carries `frozen_count` (the number of scenes the client currently retains, **not the number of threads suspended at once on the target**).
> Timeout responses may also carry `frozen_threads` + `frozen_hint` (threads reported but still frozen and not resumed by anyone); see Step 6a.
> Only the latest wait is live at any moment; the old wait returns `Superseded`.

### State reading

| Command | Purpose |
|------|------|
| `{"cmd":"locals","thread_id":42}` | Local variables of the current stack frame |
| `{"cmd":"locals","thread_id":42,"frame":1}` | Local variables of the specified stack frame |
| `{"cmd":"stack","thread_id":42}` | Full call stack |
| `{"cmd":"stack","thread_id":42,"max_frames":10}` | Limit stack depth (1~500) |
| `{"cmd":"threads"}` | List all threads |
| `{"cmd":"eval","thread_id":42,"expr":"..."}` | Expression evaluation |
| `{"cmd":"eval","thread_id":42,"expr":"Cls.STATIC","class_loader_id":95}` | Specify the classloader when a same-name class has multiple copies (integer or `"bootstrap"`) |

### Execution control

| Command | Purpose | IDEA equivalent |
|------|------|---------------|
| `{"cmd":"step","thread_id":42,"type":"over"}` | Execute the next line | Step Over |
| `{"cmd":"step","thread_id":42,"type":"into"}` | Enter the method | Step Into |
| `{"cmd":"step","thread_id":42,"type":"out"}` | Return to the caller | Step Out |
| `{"cmd":"step","thread_id":42,"type":"over","timeout":60}` | Same as above, with wait seconds specified (default 30) | — |
| `{"cmd":"resume","thread_id":42}` | Resume thread execution (idempotent) | Resume |

### Collection strategy examples

**Entry breakpoint** —— confirm the request parameters:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"request.getRequestURI()"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"request.getHeader(\"x-user-id\")"}'
```

**Logic breakpoint** —— look at field values and branch conditions, then step once to see the assignment result:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"targetField"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"condition"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"step","thread_id":42,"type":"over"}'
```

**External call breakpoint** —— look at the arguments, step over the call, then look at the return value:

```bash
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"requestParam"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"step","thread_id":42,"type":"over"}'
curl -s http://127.0.0.1:15005 -H 'Content-Type: application/json' -d '{"cmd":"eval","thread_id":42,"expr":"returnValue.getCode()"}'
```

---

## Rebuilding the jar

The source ships with the skill under `jdi-client/` (a Maven project; the jar itself is never shipped). `ensure-jdi-client.sh` only checks whether the jar exists, not whether it is older than the source, so after changing the Java code (or upgrading the skill), delete the old jar and rerun the script:

```bash
rm <SKILL_DIR>/scripts/jdi-client.jar
bash <SKILL_DIR>/scripts/ensure-jdi-client.sh
```

The script tries `jdi-client/build.sh` (Maven) first and falls back to `javac` + `jar`; on JDK 8 it depends on `tools.jar`, on JDK 9+ `com.sun.jdi` is built in.

Source layout (packages under `cn.ares.jvm.jdi` are split by domain, with one-way top-down dependencies):
- Root package: `JdiClient` (main + assembly + transport selection), `ClientOptions` (CLI arguments)
- `transport/`: `StdioTransport` (JSON Lines), `HttpTransport` + `JdiHttpHandler` (HTTP server), `JsonProtocol` (zero-dependency JSON)
- `command/`: `CommandDispatcher` (command-name routing + exception → error code), `ConnectedCommand` (not-connected check template), `BlockingCommand` (step/eval concurrency permits), `Responses` / `EventResponses` / `CommandArgs` (response and argument helpers), `ClientLifecycle` (shutdown flag); under `handler/`, one class per command
- `connection/`: `ConnectionManager` (current connection + lifecycle lock), `ConnectionContext` (per-connection component assembly), `CommandSlots` (blocking-command permits + in-flight records)
- `session/`: `JvmSession` (VM handle), `JdwpConnection` (JDWP attach), `ThreadRegistry` (thread lookup cache), `ClassLoaderResolver` (classloader queries + JDI cache collection protection)
- `breakpoint/`: `BreakpointManager` (breakpoints / deferred handling) and its `BreakpointSpec`, `BreakpointResult`
- `execution/`: `ExecutionController` (freeze / wait / resume / step state machine), `EventLoop` (JDI event loop), `DebugEvent`
- `inspect/`: `StackInspector` (stack + locals), `ThreadLister` (threads), `ValueFormatter` (value formatting)
- `eval/`: `ExpressionEvaluator` (expression evaluation), `ExpressionTokenizer`, `LiteralParser`, `ClassResolver`, `MethodSelector`, `InvocationGuard` (dangerous-method interception), `StaticInvoker` (MethodHandle route for static calls + collection protection for the invoked class's classloader), `EvaluationScope` (lifetime holding of ObjectReferences during eval)

**Value formatting for breakpoint hits and steps shares `ValueFormatter.format`**, so `locals` and `eval` return the same string for the same value. Formatting rules:

| Value type | Format | Example |
|--------|------|-----|
| String | Quoted, truncated beyond 500 characters | `"CLOSED"`, `"aaa...(truncated, total 1200)"` |
| Primitive / null | As is | `72`, `true`, `null` |
| Array | Expanded recursively, at most 10 elements | `[1, 2, 3, ... (50 total)]` |
| Object | **Field tree**, `ClassName{field=value, ...}`, expanded recursively to depth 2 | `com.example.Dto{id=456, status="CLOSED"}` |
| Depth exhausted / no instance fields / read failure | Degrades to `ClassName@id` | `java.util.ArrayList@789` |
| More than 20 fields | Truncated with the total marked | `{..., ... (37 fields total)}` |

**Expansion reads fields (bulk reads via `ObjectReference.getValues`), not `toString()`**: the target object's `toString()`
**is never called automatically**. This is deliberate: `toString()` is real business code in the target JVM and may have side effects (Hibernate lazy loading triggering SQL),
may take locks or make remote calls that hang the event thread (JDI `invokeMethod` has no timeout parameter), and would contradict the hard rule
"do not eval methods with side effects". When you need the result of `toString()`, explicitly `eval "obj.toString()"`, and the side effects are on whoever initiates it.

The cost is that collections show the implementation class's internal structure (`ArrayList`'s `size` + `elementData`, `HashMap`'s `table` + `modCount`
+ `loadFactor`) rather than a list of elements. **This is a known and accepted trade-off**: for a clean view, use `eval`.







