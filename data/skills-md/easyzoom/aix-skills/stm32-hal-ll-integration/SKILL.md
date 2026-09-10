---
name: stm32-hal-ll-integration
description: Use when integrating, configuring, or debugging STM32 HAL, LL, CubeMX generated code, clocks, GPIO, DMA, NVIC, peripheral handles, or Cube firmware examples
---

# STM32 HAL LL Integration

## Overview

Use this skill to debug STM32 projects by separating Cube-generated
configuration, clock tree, pin mux, HAL handle state, DMA, and interrupt
routing. STM32 bugs often come from generated configuration drift.

## When To Use

Use this skill when:

- The user is working with STM32CubeMX, STM32CubeIDE, HAL, LL, or Cube firmware
  examples.
- The issue involves clock configuration, GPIO alternate functions, DMA,
  interrupts, peripheral init, callbacks, low power, or generated code regions.
- A peripheral works in polling but fails with DMA/interrupts, or works until
  Cube regenerates files.

Do not use this skill for non-STM32 MCUs or pure protocol logic. Use the
matching protocol or peripheral skill instead.

## First Questions

Ask for:

- STM32 part number, board, Cube package version, IDE/toolchain, and HAL version.
- `.ioc` settings, clock tree, pin mux, DMA streams/channels, and NVIC priorities.
- Peripheral instance, HAL/LL mode, generated init code, callbacks, and logs.
- Whether user code is inside preserved `USER CODE` regions.
- Current symptom, return code, error flags, and register snapshot if available.

## Debug Workflow

1. Freeze Cube configuration.
   Inspect `.ioc`, generated init functions, clock tree, pin mux, DMA, and NVIC.

1. Prove clocks and pins.
   Confirm peripheral clock enable, GPIO alternate function, speed, pull, and
   external signal presence.

1. Check HAL handle state.
   Inspect handle init, state, error code, MSP init, callbacks, and return codes.

1. Add interrupt or DMA carefully.
   Verify IRQ handler names, priorities, DMA request mapping, cache policy, and
   callback completion.

1. Compare HAL and LL boundaries.
   Do not mix direct register/LL changes with HAL state machines unless the
   ownership is explicit.

1. Protect generated code.
   Keep edits in user regions or separate files so Cube regeneration is safe.

## Common Failures

- Peripheral clock or GPIO alternate function is missing.
- DMA request/channel mapping is valid on another STM32 family, not this one.
- IRQ handler is not linked or has the wrong name.
- HAL callback never fires because interrupt enable is missing.
- Direct register writes break HAL's state machine assumptions.
- User edits outside preserved regions are lost after Cube regeneration.

## Verification

Before claiming STM32 integration works:

- State part number, Cube package, HAL version, and relevant `.ioc` settings.
- Confirm clock, pin, DMA, and NVIC configuration.
- Confirm HAL return codes, callbacks, and error flags.
- Confirm behavior survives a Cube regeneration if generated code was touched.

## Example

User:

```text
STM32 UART DMA 收不到回调。
```

Agent:

1. Checks `.ioc`, DMA request, NVIC enable, IRQ handler, and MSP init.
1. Verifies HAL state and error code after starting reception.
1. Fixes interrupt/DMA routing before changing UART protocol code.
