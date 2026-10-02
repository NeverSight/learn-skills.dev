---
name: zephyr-shell-commands
description: "Comprehensive Zephyr Shell subsystem expertise for creating and managing CLI commands. Use this skill when you need to: (1) Create or register new shell commands with SHELL_CMD_REGISTER or SHELL_CMD_ARG_REGISTER, (2) Define static or dynamic subcommands, (3) Implement command handlers with shell_print/shell_error/shell_warn output, (4) Create dictionary commands for string-to-value mappings, (5) Configure shell backends (UART, RTT, USB, Telnet, BLE NUS), (6) Enable shell Kconfig options (CONFIG_SHELL_*), (7) Parse command arguments or use getopt, (8) Debug shell command issues or understand shell architecture."
---

# Zephyr Shell Commands

Expert guidance on Zephyr's Shell subsystem for creating custom CLI commands, managing subcommands, and interacting with users via console interfaces.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Common Workflows](#common-workflows)
3. [Command Structure](#command-structure)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

---

## Core Concepts

### Command Registration vs. Handler Implementation

| Step | What | Where |
|------|------|-------|
| **Define Handler** | Implement `shell_cmd_handler` function | Your C file |
| **Register Command** | Use `SHELL_CMD_REGISTER` or `SHELL_CMD_ARG_REGISTER` | Your C file (global scope) |
| **Enable Shell** | Set `CONFIG_SHELL=y` | prj.conf |

### Handler Prototype

```c
typedef int (*shell_cmd_handler)(const struct shell *sh, size_t argc, char **argv);
```

- `sh`: Shell instance pointer (use for all output)
- `argc`: Argument count (includes command name)
- `argv`: Argument vector. `argv[0]` is the command name
- Return: `0` success, `-EINVAL` invalid args, `-ENOEXEC` execution failed

### Key Rules

- **Use shell output functions**: Always use `shell_print()`, `shell_error()`, etc. Never use `printk()` in handlers
- **Return codes matter**: Return `0` on success, negative errno on failure
- **Argument counting**: `mandatory` count includes the command name itself

---

## Common Workflows

### 1. Creating a Simple Root Command

```c
static int cmd_hello(const struct shell *sh, size_t argc, char **argv)
{
    ARG_UNUSED(argc);
    ARG_UNUSED(argv);
    shell_print(sh, "Hello, World!");
    return 0;
}

SHELL_CMD_REGISTER(hello, NULL, "Print hello message", cmd_hello);
```

### 2. Creating Commands with Subcommands

- **Macro syntax and registration**: See [macros.md](references/macros.md)
- **Complete examples**: See [examples.md](references/examples.md)

**Quick Example:**
```c
static int cmd_demo_ping(const struct shell *sh, size_t argc, char **argv)
{
    shell_print(sh, "pong");
    return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(sub_demo,
    SHELL_CMD(ping, NULL, "Ping command", cmd_demo_ping),
    SHELL_SUBCMD_SET_END
);

SHELL_CMD_REGISTER(demo, &sub_demo, "Demo commands", NULL);
```

### 3. Commands with Argument Validation

Use `SHELL_CMD_ARG_REGISTER` to automatically validate argument counts.

```c
/* Command requires exactly 2 args: command + one parameter */
SHELL_CMD_ARG_REGISTER(greet, NULL, "Greet <name>", cmd_greet, 2, 0);
```

- **Argument parsing techniques**: See [advanced.md](references/advanced.md)

### 4. Dynamic Commands

Create commands whose subcommands are determined at runtime.

- **Dynamic command creation**: See [advanced.md](references/advanced.md#dynamic-commands)

### 5. Dictionary Commands

Map string subcommands to data values (perfect for enums, settings).

- **Dictionary command patterns**: See [advanced.md](references/advanced.md#dictionary-commands)

---

## Command Structure

### Hierarchy

```
Root Commands (Level 0)
├── Registered with SHELL_CMD_REGISTER or SHELL_CMD_ARG_REGISTER
├── Stored in dedicated memory section, alphabetically sorted
│
└── Subcommands (Level 1+)
    ├── Static: SHELL_STATIC_SUBCMD_SET_CREATE
    ├── Dynamic: SHELL_DYNAMIC_CMD_CREATE
    └── Dictionary: SHELL_SUBCMD_DICT_SET_CREATE
```

### Macro Reference

| Macro | Purpose |
|-------|---------|
| `SHELL_CMD_REGISTER` | Register root command |
| `SHELL_CMD_ARG_REGISTER` | Register root command with arg validation |
| `SHELL_STATIC_SUBCMD_SET_CREATE` | Define static subcommand array |
| `SHELL_DYNAMIC_CMD_CREATE` | Define dynamic subcommand generator |
| `SHELL_SUBCMD_DICT_SET_CREATE` | Define dictionary subcommands |
| `SHELL_CMD` | Define a subcommand entry |
| `SHELL_CMD_ARG` | Define subcommand with arg validation |
| `SHELL_COND_CMD` | Conditional subcommand (Kconfig-based) |

- **Complete macro documentation**: See [macros.md](references/macros.md)

---

## Configuration

### Essential Kconfig Options

```kconfig
CONFIG_SHELL=y                    # Enable shell subsystem
CONFIG_SHELL_BACKEND_SERIAL=y     # UART backend (most common)
CONFIG_SHELL_LOG_BACKEND=y        # Shell as logging backend
```

### Backend Selection

| Backend | Kconfig | Use Case |
|---------|---------|----------|
| UART | `CONFIG_SHELL_BACKEND_SERIAL` | Default, most common |
| USB CDC ACM | Snippet `cdc-acm-console` | USB serial |
| RTT | `CONFIG_SHELL_BACKEND_RTT` | Segger J-Link debugging |
| Telnet | `CONFIG_SHELL_BACKEND_TELNET` | Network access |
| BLE NUS | Snippet `nus-console` | Bluetooth LE |

- **Kconfig options reference**: See [kconfig.md](references/kconfig.md)
- **Backend configuration guide**: See [backends.md](references/backends.md)

---

## Troubleshooting

For common errors and debugging techniques:
- See [debugging.md](references/debugging.md)

### Quick Reference

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| Command not appearing | Not registered or shell disabled | Check `SHELL_CMD_REGISTER`, enable `CONFIG_SHELL` |
| Output not visible | Using `printk()` instead of `shell_print()` | Use shell output functions |
| "Wrong parameter count" | Mandatory arg count wrong | Adjust `mandatory` (includes command name) |
| Handler not called | Arg validation failing | Check mandatory/optional counts |
| Subcommands not showing | Missing `SHELL_SUBCMD_SET_END` | Add terminator to subcommand array |

---

## References

- [macros.md](references/macros.md) — Command registration macros, subcommand creation
- [api.md](references/api.md) — Output functions, helper functions, handler prototypes
- [advanced.md](references/advanced.md) — Dynamic commands, dictionary commands, getopt, argument parsing
- [kconfig.md](references/kconfig.md) — Shell Kconfig options reference
- [backends.md](references/backends.md) — Backend configuration (UART, RTT, USB, Telnet, BLE)
- [examples.md](references/examples.md) — Complete working examples
- [debugging.md](references/debugging.md) — Error resolution and debugging techniques
