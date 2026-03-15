---
name: agently-agent-extensions
description: Use when the user wants tool use, MCP access, HTTP or streaming API exposure, auto-function helpers, or wait-for-key behavior through Agently-native extension surfaces rather than custom wrappers first.
---

# Agently Agent Extensions

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer built-in extension surfaces before handwritten wrappers
- keep extension choice explicit: tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter`
- combine with `agently-model-response` or `agently-triggerflow` only when the scenario needs those layers

## Anti-Patterns

- do not build a parallel tool dispatcher before checking native tool and MCP support
- do not create a custom waiter or auto-function shim first

## Read Next

- `references/overview.md`
