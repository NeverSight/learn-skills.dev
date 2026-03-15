---
name: cpp-embedded
description: >
  Expert guidance for writing C (C99/C11) and C++ (C++17) code for embedded systems and microcontrollers.
  Use this skill whenever the user is working with: STM32, ESP32, Arduino, PIC, AVR, nRF52, or any other MCU;
  FreeRTOS, Zephyr, ThreadX, or any RTOS; bare-metal firmware; hardware registers, DMA, interrupts, or
  memory-mapped I/O; memory pools, allocators, or fixed-size buffers; MISRA C or MISRA C++ compliance;
  smart pointers or RAII in embedded contexts; stack vs heap decisions; placement new; volatile correctness;
  alignment and struct packing; C99/C11 patterns; C and C++ interoperability; debugging firmware crashes,
  HardFaults, stack overflows, or heap corruption; firmware architecture decisions (superloop vs RTOS vs
  event-driven); low-power modes (WFI/WFE/sleep); CubeMX project setup; HAL vs LL driver selection;
  CI/CD for firmware; embedded code review; MPU configuration; watchdog strategies; safety-critical
  design (IEC 61508, SIL); peripheral protocol selection (UART/I2C/SPI/CAN); linker script memory
  placement; or C/C++ callback patterns. Also trigger on implicit cues like "my MCU keeps crashing",
  "writing firmware", "ISR safe", "embedded allocator", "no dynamic memory", "power consumption",
  "CubeMX regenerated my code", "which RTOS pattern should I use", "MPU fault", "watchdog keeps
  resetting", "which protocol should I use for my sensor", "ESP32 deep sleep", "PSRAM vs DRAM",
  "ESP32 heap keeps shrinking", "ESP.getFreeHeap()", "task stack overflow on ESP32", or
  "WiFi reconnect after deep sleep is slow".
---

# Embedded C and C++ Skill

> **Quick navigation**
> - Memory patterns, ESP32 heap fragmentation, ETL containers → `references/memory-patterns.md`
> - C99/C11 patterns, UART read-to-clear, _Static_assert → `references/c-patterns.md`
> - Debugging workflows (stack overflow, heap corruption, HardFault) → `references/debugging.md`
> - Coding style and conventions → `references/coding-style.md`
> - Firmware architecture, RTOS IPC, low-power, ESP32 deep sleep, CI/CD → `references/architecture.md`
> - STM32 pitfalls, CubeMX, hard-to-debug issues, code review → `references/stm32-pitfalls.md`
> - Design patterns, SOLID for embedded, HAL design, C/C++ callbacks → `references/design-patterns.md`
> - MPU protection, watchdog hierarchy, safety-critical, protocols, linker scripts → `references/safety-hardware.md`

---

## Embedded Memory Mindset

Embedded systems have no OS safety net. A bad pointer dereference doesn't produce a polite segfault — it
silently corrupts memory, triggers a HardFault hours later, or hangs in an ISR. The stakes of every
allocation decision are higher than in hosted environments.

Three principles govern embedded memory:

**Determinism over convenience.** Dynamic allocation (malloc/new) is non-deterministic in both time and
failure mode. MISRA C Rule 21.3 and MISRA C++ Rule 21.6.1 ban dynamic memory after initialization.
Even outside MISRA, avoid heap allocation in production paths.

**Size is known at compile time.** Embedded software has a fixed maximum number of each object type.
Design around this. If you need 8 UART message buffers, declare 8 at compile time. Don't discover the
maximum at runtime.

**ISRs are sacred ground.** Never allocate, never block, never call non-reentrant functions from an ISR.
Keep ISRs minimal — set a flag or write to a ring buffer, then do the real work in a task.

---

## Allocation Decision Table

| Need | Solution | Notes |
|------|----------|-------|
| Short-lived local data | Stack | Keep < 256 bytes per frame; profile with `-fstack-usage` |
| Fixed singleton objects | `static` at file or function scope | Zero-initialized before `main()` |
| Fixed array of objects | Object pool (`ObjectPool<T, N>`) | O(1) alloc/free, no fragmentation |
| Temporary scratch space | Arena / bump allocator | Reset whole arena at end of operation |
| Variable-size messages | Ring buffer of fixed-size slots | Simplest ISR-safe comms pattern |
| Custom lifetime control | Placement new + static storage | Full control, no heap involvement |
| **Never in ISR** | Any of the above except stack | Allocator calls are not ISR-safe |
| **Avoid entirely** | `malloc`/`new` / `std::vector` | Non-deterministic; fragmentation risk |

---

## Critical Patterns

### RAII Resource Guard

Acquire on construction, release on destruction. Guarantees release even through early returns or exceptions
(if using exceptions — rare in embedded, but possible in C++ environments that allow them).

```cpp
class SpiGuard {
public:
    explicit SpiGuard(SPI_HandleTypeDef* spi) : spi_(spi) {
        HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_RESET);
    }
    ~SpiGuard() {
        HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET);
    }
    // Non-copyable, non-movable — guard is tied to this scope
    SpiGuard(const SpiGuard&) = delete;
    SpiGuard& operator=(const SpiGuard&) = delete;
private:
    SPI_HandleTypeDef* spi_;
};

// Usage: CS deasserts automatically at end of scope
void read_sensor() {
    SpiGuard guard(&hspi1);
    // ... transfer bytes ...
}  // CS deasserts here
```

### ISR-to-Task Communication: Ring Buffer vs Ping-Pong DMA

For passing data from an ISR/DMA to a task, two main patterns exist:
- **SPSC ring buffer** (power-of-2 capacity with bitmask indexing) — best for variable-rate streams. See `references/memory-patterns.md` §3 for the full implementation. Always use `_Static_assert` or `static_assert` to validate the capacity is a power of 2.
- **Ping-pong (double) buffering** — best for fixed-burst DMA transfers. ISR fills one buffer while task processes the other.

When asked for ISR-to-task communication, include a ring buffer with power-of-2 bitmask indexing as the primary pattern, even if ping-pong is also mentioned as an alternative for specific DMA scenarios.

### Static Object Pool

Pre-allocates N objects of type T with O(1) alloc/free and no heap involvement.
Read `references/memory-patterns.md` §1 for the full arena allocator and §2 for CRTP patterns.

```cpp
template<typename T, size_t N>
class ObjectPool {
public:
    template<typename... Args>
    T* allocate(Args&&... args) {
        for (auto& slot : slots_) {
            if (!slot.used) {
                slot.used = true;
                return new (&slot.storage) T(std::forward<Args>(args)...);
            }
        }
        return nullptr;  // Pool exhausted — handle at call site
    }

    void free(T* obj) {
        obj->~T();
        for (auto& slot : slots_) {
            if (reinterpret_cast<T*>(&slot.storage) == obj) {
                slot.used = false;
                return;
            }
        }
    }

private:
    struct Slot {
        alignas(T) std::byte storage[sizeof(T)];
        bool used = false;
    };
    Slot slots_[N]{};
};
```

### Volatile Hardware Register Access

`volatile` tells the compiler the value can change outside its knowledge (hardware can write it).
Without `volatile`, the compiler may cache the read in a register and never see the hardware update.

```cpp
// Define register layout matching the hardware manual
struct UartRegisters {
    volatile uint32_t SR;   // Status register
    volatile uint32_t DR;   // Data register
    volatile uint32_t BRR;  // Baud rate register
    volatile uint32_t CR1;  // Control register 1
};

// Map to the hardware base address
auto* uart = reinterpret_cast<UartRegisters*>(0x40011000U);

// Read status — volatile ensures each read hits the hardware
if (uart->SR & (1U << 5)) {   // RXNE bit
    uint8_t byte = static_cast<uint8_t>(uart->DR);
}
```

### Interrupt-Safe Access

Sharing data between an ISR and a task requires either a critical section or `std::atomic`.
Use atomics when the type fits in a single load/store (usually ≤ pointer size). Use critical sections
for larger structures.

```cpp
#include <atomic>

// Atomic: ISR and task can access without disabling interrupts
std::atomic<uint32_t> adc_value{0};

// In ISR:
void ADC_IRQHandler() {
    adc_value.store(ADC1->DR, std::memory_order_relaxed);
}

// In task:
uint32_t val = adc_value.load(std::memory_order_relaxed);

// Critical section for larger structures (ARM Cortex-M):
struct SensorFrame { uint32_t timestamp; int16_t x, y, z; };
volatile SensorFrame latest_frame{};

void update_frame_from_isr(const SensorFrame& f) {
    __disable_irq();
    latest_frame = f;
    __enable_irq();
}
```

---

## Smart Pointer Policy

| Pointer type | Use in embedded? | Guidance |
|---|---|---|
| Raw pointer (observing) | Yes | For non-owning references; make ownership explicit in naming |
| Raw pointer (owning) | Carefully | Only into static/pool storage where lifetime is obvious |
| `std::unique_ptr` | Yes, with care | Zero overhead; use with custom deleters for pool objects |
| `std::unique_ptr` + custom deleter | Yes | Returns pool objects to their pool on destruction |
| `std::shared_ptr` | Avoid | Reference counting uses heap and is non-deterministic |
| `std::weak_ptr` | Avoid | Tied to `shared_ptr`; same concerns |

```cpp
// unique_ptr with pool deleter — zero heap, automatic return to pool
ObjectPool<SensorData, 8> sensor_pool;

auto deleter = [](SensorData* p) { sensor_pool.free(p); };
using PooledSensor = std::unique_ptr<SensorData, decltype(deleter)>;

PooledSensor acquire_sensor() {
    return PooledSensor(sensor_pool.allocate(), deleter);
}
```

---

## Compile-Time Preferences

Prefer compile-time computation and verification over runtime checks:

```cpp
// constexpr: computed at compile time, no runtime cost
constexpr uint32_t BAUD_DIVISOR = PCLK_FREQ / (16U * TARGET_BAUD);
static_assert(BAUD_DIVISOR > 0 && BAUD_DIVISOR < 65536, "Baud divisor out of range");

// std::array: bounds info preserved, unlike raw arrays
std::array<uint8_t, 64> tx_buffer{};

// std::span: non-owning view, no allocation, C++20 but often available via ETL
// std::string_view: for string literals and buffers, no heap

// CRTP replaces virtual dispatch — zero runtime overhead
// See references/memory-patterns.md §2 for full example
```

**C++ features to avoid in embedded:**

| Avoid | Reason | Alternative |
|---|---|---|
| `-fexceptions` | Code size (10-30% increase), non-deterministic stack unwind | `std::optional`, `std::expected` (C++23/polyfill), error codes |
| `-frtti` / `typeid` / `dynamic_cast` | Runtime type tables increase ROM | CRTP, explicit type tags |
| `std::vector`, `std::string`, `std::map` | Heap allocation | `std::array`, ETL containers |
| `std::thread` | Requires OS primitives | RTOS tasks |
| `std::function` | Heap allocation for captures | Function pointers, templates |
| Virtual destructors in deep hierarchies | vtable size, indirect dispatch, blocks inlining | CRTP or flat hierarchies (≤2 levels); virtual OK for non-critical paths |

Compile with `-fno-exceptions -fno-rtti` for ARM targets. Use the [Embedded Template Library (ETL)](https://www.etlcpp.com)
for fixed-size `etl::vector`, `etl::map`, `etl::string` alternatives.

---

## Common Anti-Patterns

These patterns cause real bugs in production firmware. Knowing them saves hours of debugging.

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `std::function` with captures | Heap-allocates when captures exceed small-buffer threshold (~16-32 bytes, implementation-dependent) | Function pointer + `void* context`, template callable, or lambda passed directly to template parameter |
| Arduino `String` in loops | Every concatenation/conversion heap-allocates; 10Hz × 4 sensors = 3.4M alloc/day → fragmentation | Fixed `char[]` with `snprintf`; for complex strings use `etl::string<N>` |
| `new`/`delete` in periodic tasks | Same fragmentation; violates MISRA C++ Rule 21.6.1 | Object pool, static array, or ETL fixed-capacity container |
| `std::shared_ptr` anywhere | Atomic ref-counting overhead, control block on heap | `std::unique_ptr` with pool deleter, or raw pointer with clear ownership |
| Deep virtual hierarchies | vtable per class (ROM), indirect dispatch, blocks inlining | CRTP or flat hierarchy (≤2 levels) |
| Hidden `std::string`/`std::vector` | Dynamic allocation on every operation — often hidden in library APIs | ETL containers (`etl::string<N>`, `etl::vector<T,N>`) |
| `volatile` for thread sync | `volatile` only prevents the compiler from caching or eliminating reads/writes — it does NOT prevent reordering between threads or provide atomicity. Data races on `volatile` variables are still undefined behavior | `std::atomic` with explicit memory ordering (`memory_order_relaxed` suffices for ISR-to-task on single-core Cortex-M) |
| ISR handler name mismatch | Misspelled ISR name silently falls through to `Default_Handler` — system hangs or resets | Verify names against startup `.s` vector table; use `-Wl,--undefined=USART1_IRQHandler` to catch missing symbols at link time |
| `printf`/`sprintf` in ISR | Heap allocation, locking, non-reentrant — crashes or deadlocks | `snprintf` to pre-allocated buffer outside ISR, or ITM/SWO trace output |
| Unbounded recursion | Stack overflow on MCU with 1–8KB stack; MISRA C Rule 17.2 bans recursion | Convert to iterative with explicit stack |

**Hidden allocation checklist:** Before using any STL type, check whether it allocates. Common
surprises: `std::string::operator+=`, `std::vector::push_back` (reallocation), `std::function`
(type-erased captures), `std::any`, `std::regex`.

---

## Common Memory Bug Diagnosis

| Symptom | Likely cause | First action |
|---|---|---|
| Crash after N hours of uptime | Heap fragmentation | Switch to pools/ETL containers; cite MISRA C Rule 21.3; see `references/memory-patterns.md` §9 for ESP32-specific guidance |
| HardFault with BFAR/MMFAR valid | Null/wild pointer dereference or bus fault | Read CFSR sub-registers; check MMARVALID/BFARVALID before using address registers; see `references/debugging.md` §4 |
| Stack pointer in wrong region | Stack overflow | Check `.su` files; add MPU guard region; see `references/debugging.md` §1 |
| ISR data looks stale | Missing `volatile` | Add `volatile` to shared variables; audit ISR data paths |
| Random corruption near ISR | Data race | Apply atomics or critical section; see `references/debugging.md` §3 |
| Use-after-free | Object returned to pool while still referenced | Verify no aliasing; use unique_ptr with pool deleter |
| MPU fault in task | Task overflowed its stack into neighboring region | Increase stack size or reduce frame depth |
| Uninitialized read | Local variable used before assignment | Enable `-Wuninitialized`; initialize all locals |
| HardFault on first `float` operation | FPU not enabled in CPACR | `SCB->CPACR |= 0xF << 20;` before any float code; CFSR shows NOCP |
| ISR does nothing / default handler runs | ISR function name misspelled | Verify name against startup `.s` vector table |

---

## Debugging Tools Decision Tree

```
Is the bug reproducible on a host (PC)?
├── YES → Use AddressSanitizer (ASan) + Valgrind
│         Compile embedded logic for PC with -fsanitize=address
│         See references/debugging.md §5
└── NO  → Is it a memory layout/access issue?
          ├── YES → Enable MPU; add stack canaries; read CFSR on fault
          │         See references/debugging.md §1, §4
          └── NO  → Is it a data-race between ISR and task?
                    ├── YES → Audit shared state; apply atomics/critical section
                    │         See references/debugging.md §3
                    └── NO  → Use GDB watchpoint on the corrupted address
                              See references/debugging.md §6
```

Static analysis: run `clang-tidy` with `clang-analyzer-*` and `cppcoreguidelines-*` checks.
Run `cppcheck --enable=all` for C code. Both catch many issues before target hardware.

---

## Error Handling Philosophy

Four layers, each for a distinct failure category:

**Recoverable errors (with context)** — use `std::expected` (C++23, or `tl::expected`/`etl::expected`
as header-only polyfills for C++17) when you need to communicate *why* something failed. Zero heap
allocation, zero exceptions, type-safe error propagation:
```cpp
enum class SensorError : uint8_t { not_ready, crc_fail, timeout };

[[nodiscard]] std::expected<SensorReading, SensorError> read_sensor() {
    if (!sensor_ready()) return std::unexpected(SensorError::not_ready);
    auto raw = read_raw();
    if (!verify_crc(raw)) return std::unexpected(SensorError::crc_fail);
    return SensorReading{.temp = convert(raw)};
}
```

**Recoverable errors (simple)** — use `std::optional` when the only failure is "no value":
```cpp
[[nodiscard]] std::optional<SensorReading> read_sensor() {
    if (!sensor_ready()) return std::nullopt;
    return SensorReading{.temp = read_temp(), .humidity = read_humidity()};
}
```

**`[[nodiscard]]` enforcement:** Mark every function returning an error code, status, or
allocated pointer with `[[nodiscard]]`. The compiler then warns if the caller silently ignores
the return value — this catches the #1 error handling bug in firmware (discarded error codes).
In C, use `[[nodiscard]]` (C23) or `__attribute__((warn_unused_result))`.

**Programming errors** — use `assert` or a trap that halts with debug info:
```cpp
void write_to_pool(uint8_t* buf, size_t len) {
    assert(buf != nullptr);
    assert(len <= MAX_PACKET_SIZE);  // Trips in debug, removed in release with NDEBUG
    // ...
}
```

**Unrecoverable runtime errors** — log fault reason + registers to non-volatile memory
(flash/EEPROM), then let the watchdog reset the system. Without pre-reset logging, field
failures leave no post-mortem data. Write CFSR + stacked PC + LR to a dedicated flash sector,
then call `NVIC_SystemReset()` or spin and let the watchdog fire.

---

## Testability Architecture

Write firmware that can be tested on a PC without target hardware. The key: separate business
logic from hardware I/O at a clear HAL boundary.

**Compile-time dependency injection** — the hardware is known at compile time, so use templates
instead of virtual dispatch. Zero runtime overhead, full testability:

```cpp
// HAL interface as a concept (or just template parameter)
template<typename Hal>
class SensorController {
public:
    explicit SensorController(Hal& hal) : hal_(hal) {}
    std::optional<float> read_temperature() {
        auto raw = hal_.i2c_read(SENSOR_ADDR, TEMP_REG, 2);
        if (!raw) return std::nullopt;
        return convert_raw_to_celsius(*raw);
    }
private:
    Hal& hal_;
};

// Production: uses real hardware
SensorController<StmHal> controller(real_hal);

// Test: uses mock — same code, no vtable, no overhead in production
SensorController<MockHal> test_controller(mock_hal);
```

**Testing pyramid for firmware:**
- **Unit tests (host PC):** Business logic with mock HAL — runs with ASan/UBSan, fast CI
- **Integration tests (QEMU):** Full firmware on emulated Cortex-M — catches linker/startup issues
- **Hardware-in-the-loop (HIL):** On real target — catches timing, peripheral, and electrical issues

---

## Firmware Architecture Selection

Choose the simplest architecture that meets your requirements:

| Architecture | Complexity | Best for |
|---|---|---|
| **Superloop** (bare-metal polling) | Lowest | < 5 tasks, loose timing, fully deterministic |
| **Cooperative scheduler** (time-triggered) | Low | Hard real-time, safety-critical (IEC 61508 SIL 1–2), analyzable |
| **RTOS preemptive** (FreeRTOS/Zephyr) | Medium | Complex multi-task, priority-based scheduling |
| **Active Object** (QP framework) | Highest | Event-heavy, hierarchical state machines, protocol handling |

For FreeRTOS IPC selection (task notifications vs queues vs stream buffers), low-power
patterns, CI/CD pipeline setup, and binary size budgeting → see `references/architecture.md`.

For STM32 CubeMX pitfalls, HAL vs LL driver selection, hard-to-debug embedded issues,
and code review checklists → see `references/stm32-pitfalls.md`.

---

## ESP32 Platform Guidance

When responding to any ESP32/ESP32-S2/S3/C3 question, always consider these platform-specific concerns:

**Memory architecture — always address in ESP32 responses:** ESP32 has multiple non-contiguous
memory regions. In every ESP32 response, explicitly discuss where buffers should be placed:

- **DRAM** (~320KB, fast): Ring buffers, DMA buffers, ISR data, FreeRTOS stacks. All real-time
  and latency-sensitive data goes here.
- **PSRAM** (4-8MB, ~10× slower, optional on -WROVER/S3): Large non-realtime data like SD card
  write buffers, CSV formatting buffers, web server buffers, display framebuffers. Allocate with
  `heap_caps_malloc(size, MALLOC_CAP_SPIRAM)` or `ps_malloc()`. Never use PSRAM in ISRs or
  tight control loops — access latency is ~100ns vs ~10ns for DRAM.
- **If the ESP32 variant has PSRAM**, recommend moving large format/write buffers there to free
  DRAM for real-time use. If PSRAM is not available, note the DRAM pressure and size budgets.
  Always mention both regions so the user understands the tradeoff.

**ETL on ESP32:** When replacing `std::vector`, `std::string`, or `std::map` on ESP32, always
recommend the [Embedded Template Library (ETL)](https://www.etlcpp.com) by name with specific
types: `etl::vector<T, N>`, `etl::string<N>`, `etl::map<K, V, N>`, `etl::queue_spsc_atomic<T, N>`.
ETL works on ESP32 with both Arduino (`lib_deps = ETLCPP/Embedded Template Library`) and ESP-IDF
(add as component). Even when providing a custom implementation (like a ring buffer), mention ETL
as a production-ready alternative the user should consider.

**Deep sleep and fast wake:** For battery-powered ESP32 sensor nodes, see
`references/architecture.md` for RTC memory WiFi caching, static IP, and sensor forced mode patterns.

**Task stack sizing on ESP32:** WiFi tasks need 4096-8192 bytes, BLE 4096-8192, TLS/SSL 8192-16384.
Monitor with `uxTaskGetStackHighWaterMark()`. See `references/memory-patterns.md` §9 for details.

For full ESP32 heap fragmentation diagnosis, monitoring, and ETL integration →
see `references/memory-patterns.md` §9.

---

## Coding Conventions Summary

See `references/coding-style.md` for the full guide. Key rules:

- **Variables and functions**: `snake_case`
- **Classes and structs**: `PascalCase`
- **Constants**: `kConstantName` (Google style) or `ALL_CAPS` for macros
- **Member variables**: `trailing_underscore_`
- **Include guards**: `#pragma once` (prefer) or `#ifndef HEADER_H_` guard
- **const correctness**: const every non-mutating method, const every parameter that isn't modified
- **`[[nodiscard]]`**: on any function whose return value must not be silently dropped (error codes, pool allocate)

---

## Reference File Index

| File | Read when |
|---|---|
| `references/memory-patterns.md` | Implementing arena, ring buffer, DMA buffers, lock-free SPSC, singletons, linker sections, ESP32 heap fragmentation, ETL containers |
| `references/c-patterns.md` | Writing C99/C11 firmware, C memory pools, C error handling, C/C++ interop, MISRA C rules, UART read-to-clear mechanism, `_Static_assert` for buffer validation |
| `references/debugging.md` | Diagnosing stack overflow, heap corruption, HardFault, data races, NVIC priority issues, or running ASan/GDB |
| `references/coding-style.md` | Naming conventions, feature usage table, struct packing, attributes, include guards |
| `references/architecture.md` | Choosing firmware architecture, FreeRTOS IPC patterns, low-power modes, ESP32 deep sleep + fast wake, CI/CD pipeline setup, binary size budgets |
| `references/stm32-pitfalls.md` | CubeMX code generation issues, HAL vs LL selection, hard-to-debug issues (cache, priority inversion, flash stall), code review checklist |
| `references/design-patterns.md` | HAL design patterns (CRTP/template/virtual/opaque), dependency injection strategies, SOLID for embedded, callback + trampoline patterns |
| `references/safety-hardware.md` | MPU protection patterns, watchdog hierarchy, IEC 61508 fault recovery, peripheral protocol selection (UART/I2C/SPI/CAN), linker script memory placement |
