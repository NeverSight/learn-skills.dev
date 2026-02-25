---
name: jdb-debugger
description: Debug Java applications in real time using JDB (Java Debugger CLI). Attach to running JVMs or launch new ones under JDB, set breakpoints, step through code, inspect variables, analyze threads, and diagnose exceptions. Use when debugging Java programs, investigating runtime behavior, or diagnosing production issues on JVMs with JDWP enabled.
compatibility: Requires JDK (jdb command), Bash shell, and a running or launchable Java application
allowed-tools: Bash(jdb:*) Bash(java:*) Bash(python3:*) Read
metadata:
  author: brunoborges
  version: "1.0"
---

# Java Debugger (JDB) Skill

Debug Java applications interactively using the JDK's built-in command-line debugger.

## Critical Rules for Agents

1. **NEVER create files in the workspace** (no `bp.txt`, `cmds.txt`, wrapper scripts, etc.).
   Use the inline CLI flags (`--bp`, `--cmd`, `--auto-inspect`) provided by the skill scripts.
2. **ALWAYS use the skill scripts** in `scripts/`. Never write
   custom JDB wrapper scripts, FIFO-based launchers, or shell scripts to drive JDB.
3. **Compile first, then debug.** Ensure classes are compiled before launching JDB.
4. **On Windows, invoke scripts via WSL:** `wsl bash scripts/<script>.sh`

## Platform Support

### Windows (WSL Required)

The scripts in this skill are Bash scripts. On Windows, invoke them via WSL:

```bash
wsl bash scripts/jdb-launch.sh com.example.MyApp --sourcepath src/main/java
```

If your compiled classes are on the Windows filesystem, WSL accesses them via `/mnt/c/`:
```bash
wsl bash scripts/jdb-launch.sh com.example.MyApp --classpath /mnt/c/Users/you/project/out
```

Ensure JDK is installed in WSL:
```bash
# Ubuntu/Debian WSL
sudo apt update && sudo apt install -y default-jdk

# Verify
which jdb && jdb -version
```

### Linux / macOS

Scripts run natively. Ensure JDK is installed and `jdb` is on PATH:
```bash
export PATH=$JAVA_HOME/bin:$PATH
```

## Decision Tree

```
User wants to debug Java app →
  ├─ App is already running with JDWP agent?
  │   ├─ Yes → Attach: scripts/jdb-attach.sh --port <port>
  │   └─ No  → Can you restart with JDWP?
  │       ├─ Yes → Launch with: scripts/jdb-launch.sh <mainclass> [args]
  │       └─ No  → Suggest adding JDWP agent to JVM flags (see below)
  │
  ├─ What does the user need?
  │   ├─ Set breakpoints & step through code → Interactive JDB session
  │   ├─ Collect thread dumps / diagnostics → scripts/jdb-diagnostics.sh
  │   └─ Catch a specific exception → Use `catch` command in JDB
  │
  └─ Done debugging → Detach cleanly with `quit` or Ctrl+C
```

## Quick Start

### Option 1: Launch a new JVM under JDB

```bash
bash scripts/jdb-launch.sh com.example.MyApp --sourcepath src/main/java
```

### Option 2: Attach to a running JVM

First, ensure the target JVM was started with the JDWP agent:
```bash
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -jar myapp.jar
```

Then attach:
```bash
bash scripts/jdb-attach.sh --host localhost --port 5005
```

### Option 3: Quick diagnostics (thread dump + deadlock detection)

```bash
bash scripts/jdb-diagnostics.sh --port 5005
```

## Enabling JDWP on a Running Application

If the target JVM was not started with JDWP, suggest the user restart with:

```bash
# For direct Java launch
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -cp myapp.jar com.example.Main

# For Maven Spring Boot
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# For Gradle
./gradlew bootRun --jvmArgs="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# As environment variable
export JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
```

## Interactive JDB Session Guide

Once inside a JDB session (launched or attached), use these commands interactively:

### Setting Breakpoints

```
stop at com.example.MyClass:42          # Break at line 42
stop in com.example.MyClass.myMethod    # Break at method entry
stop in com.example.MyClass.<init>      # Break at constructor
stop in com.example.MyClass.<clinit>    # Break at static initializer
```

For overloaded methods, specify parameter types:
```
stop in com.example.MyClass.process(int,java.lang.String)
```

### Running and Stepping

```
run                  # Start the application (if launched, not attached)
cont                 # Continue execution after hitting a breakpoint
step                 # Step into the next line (enters method calls)
next                 # Step over to the next line (skips method internals)
step up              # Run until the current method returns
```

### Inspecting State

```
locals               # Show all local variables in the current frame
print myVariable     # Print value of a variable or expression
print myObj.getX()   # Evaluate a method call
dump myObject        # Show all fields of an object
eval 2 + 2           # Evaluate an arbitrary expression
```

### Navigating the Call Stack

```
where                # Show the current thread's call stack
where all            # Show call stacks for all threads
up                   # Move up one frame in the stack
down                 # Move down one frame in the stack
up 3                 # Move up 3 frames
```

### Thread Management

```
threads              # List all threads and their states
thread main          # Switch to the "main" thread
thread 0x1a3         # Switch to thread by ID
suspend 0x1a3        # Suspend a specific thread
resume 0x1a3         # Resume a specific thread
```

### Exception Handling

```
catch java.lang.NullPointerException              # Break on NPE
catch java.lang.Exception                          # Break on any Exception
catch all                                          # Break on all throwables
ignore java.lang.NullPointerException              # Stop catching NPE
```

### Inspecting Classes and Methods

```
classes                         # List all loaded classes
class com.example.MyClass       # Show details of a class
methods com.example.MyClass     # List all methods of a class
fields com.example.MyClass      # List all fields of a class
```

### Managing Breakpoints

```
clear                                    # List all breakpoints
clear com.example.MyClass:42             # Remove breakpoint at line 42
clear com.example.MyClass.myMethod       # Remove method breakpoint
```

### Source Code

```
list                  # List source around current line
list 50               # List source around line 50
use /path/to/sources  # Set source path
sourcepath            # Show current source path
classpath             # Show current classpath
```

### Exiting

```
quit                  # Exit JDB (detaches from JVM)
exit                  # Same as quit
```

## Debugging Workflow Patterns

### Pattern 1: Investigate a NullPointerException (automated batch mode)

Use inline `--bp` flags and `--auto-inspect` — no files needed:
```bash
bash scripts/jdb-breakpoints.sh \
  --mainclass com.example.MyClass \
  --bp "catch java.lang.NullPointerException" \
  --bp "stop at com.example.MyClass:42" \
  --bp "stop in com.example.MyClass.processMessage" \
  --auto-inspect 20
```

The `--auto-inspect 20` flag automatically generates `run` + 20 cycles of
`where`, `locals`, `cont` + `quit`. The output contains the full JDB session
including stack traces, local variables, and exception details — ready for analysis.

For custom commands, use `--cmd` flags instead of `--auto-inspect`:
```bash
bash scripts/jdb-breakpoints.sh \
  --mainclass com.example.MyClass \
  --bp "catch java.lang.NullPointerException" \
  --cmd "run" --cmd "where" --cmd "locals" --cmd "print myVar" --cmd "cont" \
  --cmd "where" --cmd "locals" --cmd "cont" --cmd "quit"
```

### Pattern 2: Watch a method's behavior

```
# 1. Set breakpoint at method entry
stop in com.example.Service.processOrder

# 2. Continue until breakpoint is hit
cont

# 3. Inspect arguments and step through
locals
next
print result
next
print result
```

### Pattern 3: Diagnose a deadlock

```
# 1. List all threads
threads

# 2. Check each blocked thread's stack
where all

# 3. Look for threads in MONITOR state holding different locks
thread <blocked-thread-id>
where
```

### Pattern 4: Inspect values at a specific line

```
# 1. Set breakpoint
stop at com.example.DataProcessor:128

# 2. Continue to breakpoint
cont

# 3. Inspect everything
locals
print config.getTimeout()
dump dataMap
```

## Important Notes

- **NEVER create files in the workspace.** Use inline `--bp`, `--cmd`, and `--auto-inspect`
  flags. The scripts handle all temp files internally in `/tmp/` and clean up after themselves.
- **Compile with `-g` for full debug info.** Without it, `locals` will show
  "Local variable information not available". Always compile with:
  `javac -g -d out src/main/java/com/example/MyClass.java`
- **JDB is line-oriented**: Send one command at a time and read the output before the next command.
- **Source path**: Use `-sourcepath` or `use` command so `list` can show source code.
- **Classpath**: Ensure compiled classes are accessible for expression evaluation.
- **Thread context**: Many commands operate on the "current thread". Use `thread` to switch.
- **Suspend mode**: When attaching with `suspend=y`, the JVM pauses until JDB connects. Use `suspend=n` for non-blocking attachment.
- **Expression evaluation**: `print` and `eval` can call methods on live objects — use with caution in production.
- **Batch timing**: The batch mode uses configurable delays. Override via env vars:
  `JDB_BP_DELAY` (default: 2s), `JDB_RUN_DELAY` (3s), `JDB_CMD_DELAY` (0.5s), `JDB_CONT_DELAY` (1s).

## Reference Files

- [JDB Command Reference](references/jdb-commands.md) - Complete alphabetical command reference
- [JDWP Options Reference](references/jdwp-options.md) - All JDWP agent configuration options
