---
name: freertos-kernel-debug
description: Use when debugging FreeRTOS kernel behavior, task scheduling, priorities, stacks, heap schemes, tick interrupts, ISR APIs, queues, semaphores, timers, or deadlocks
---

# FreeRTOS Kernel Debug

## Overview

Use this skill to debug FreeRTOS by proving tick, scheduler state, task stacks,
heap, ISR boundaries, and synchronization ownership. Many FreeRTOS failures are
contract violations around interrupt priority or blocking context.

## When To Use

Use this skill when:

- The user is debugging FreeRTOS tasks, queues, semaphores, mutexes, timers,
  event groups, streams, or task notifications.
- The issue involves hard faults, hangs, missed ticks, watchdog resets, stack
  overflow, heap exhaustion, priority inversion, or ISR API misuse.
- The target uses vendor HAL callbacks, Cortex-M interrupt priorities, trace
  tools, or multiple heap implementations.

Do not use this skill for RTOS-agnostic firmware architecture questions. Use
`rtos-debug` for broader RTOS triage.

## First Questions

Ask for:

- FreeRTOS version, port, MCU, tick rate, heap implementation, and config file.
- Task list with priorities, stack sizes, states, and high-water marks.
- Interrupt priorities, `configMAX_SYSCALL_INTERRUPT_PRIORITY`, and ISR APIs.
- Current symptom, fault dump, watchdog reason, trace, or scheduler snapshot.
- Whether assertions, stack overflow hook, malloc failed hook, and trace are on.

## Debug Workflow

1. Enable kernel evidence.
   Turn on `configASSERT`, stack overflow checks, malloc failed hook, and
   trace-friendly task names where possible.

1. Prove the tick and scheduler.
   Confirm SysTick/timer setup, interrupt priority, scheduler start, and idle
   task execution.

1. Audit task resources.
   Check priority, stack high-water mark, blocking calls, and CPU hogging loops.

1. Audit ISR boundaries.
   Match every ISR call to the `FromISR` API and verify interrupt priority is
   allowed to call the kernel.

1. Inspect synchronization.
   Identify queue ownership, mutex holders, priority inheritance, timeouts, and
   event group semantics.

1. Validate heap and timers.
   Confirm selected heap scheme, fragmentation risk, timer task priority, and
   timer command queue length.

## Common Failures

- An ISR above `configMAX_SYSCALL_INTERRUPT_PRIORITY` calls a FreeRTOS API.
- A normal API is called from an ISR instead of the `FromISR` variant.
- A task stack is sized for the happy path but not logging or TLS.
- A high-priority task spins and starves lower-priority work.
- Timer callbacks block or perform long operations.
- Heap implementation does not match allocation/free patterns.

## Verification

Before claiming FreeRTOS behavior is fixed:

- State kernel version, port, tick source, heap scheme, and key config symbols.
- Confirm assertions/hooks are enabled or explain why they cannot be.
- Show task state, stack margin, heap margin, and interrupt priority evidence.
- Confirm the original hang/fault/deadlock scenario no longer reproduces.

## Example

User:

```text
FreeRTOS 跑一会儿随机卡死。
```

Agent:

1. Enables `configASSERT`, stack overflow, and malloc failed hooks.
1. Captures task states, stacks, heap, and interrupt priorities.
1. Checks ISR API usage and blocking calls before changing task priorities.
