---
name: automotive-embedded-skills
description: C/C++/CAPL best practices for automotive embedded systems. This skill should be used when writing, reviewing, or refactoring embedded C/C++ code or CAPL scripts targeting automotive ECUs, following MISRA, AUTOSAR, ISO 26262, and ISO 21434 guidelines. Triggers on tasks involving embedded firmware, CAN/CAN FD/LIN/Ethernet communication, TCP/UDP/DoIP/SOME-IP protocols, RTOS programming, safety-critical code, cybersecurity, diagnostics (UDS), CAPL test automation, or calibration toolchain integration.
license: MIT
metadata:
  author: automotive-embedded-engineering
  version: "2.0.0"
---

# Automotive Embedded C/C++/CAPL Best Practices

Comprehensive coding guidelines for automotive embedded software development in C, C++, and CAPL. Contains 180+ rules across 23 categories, prioritized by safety impact and industry compliance requirements (MISRA C:2012, MISRA C++:2023, AUTOSAR C++14 Classic & Adaptive, ISO 26262, ISO 21434). Covers full automotive communication stack (CAN/LIN/Ethernet/IP/TSN), cybersecurity, diagnostics, CAPL simulation/testing/fault injection, AUTOSAR BSW modules, boot/NVM/power management, compiler toolchains, static analysis tools, and CI/CD integration.

## When to Apply

Reference these guidelines when:
- Writing new embedded C/C++ modules for automotive ECUs
- Implementing or reviewing CAN/LIN/Ethernet communication stacks
- Writing CAPL scripts for CANoe/CANalyzer simulation and testing
- Refactoring code for MISRA C/C++ or AUTOSAR C++14 compliance
- Designing safety-critical software (ASIL A-D per ISO 26262)
- Implementing RTOS task management and inter-task communication
- Reviewing code for memory safety, timing, and determinism
- Working with diagnostic protocols (UDS, OBD-II, DoIP)
- Implementing Automotive Ethernet (TCP, UDP, SOME/IP, DoIP, VLAN)
- Addressing cybersecurity requirements (ISO 21434, secure boot, TLS)
- Integrating with calibration/diagnostic tools (A2L, ODX, XCP)
- Optimizing for resource-constrained microcontrollers (RAM, Flash, CPU)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Memory Safety & Management | CRITICAL | `memory-` |
| 2 | MISRA C/C++ Compliance | CRITICAL | `misra-` |
| 3 | AUTOSAR C++14 Guidelines (Classic & Adaptive) | CRITICAL | `autosar-` |
| 4 | Safety & Functional Safety (ISO 26262) | HIGH | `safety-` |
| 5 | Real-Time & Timing Constraints | HIGH | `realtime-` |
| 6 | Communication Protocols (CAN/LIN/Ethernet/IP/UDS) | HIGH | `comm-` |
| 7 | Concurrency & RTOS Patterns | MEDIUM-HIGH | `rtos-` |
| 8 | CAPL Scripting — CANoe | MEDIUM-HIGH | `capl-canoe-` |
| 9 | CAPL Scripting — vTESTstudio | MEDIUM-HIGH | `capl-vtest-` |
| 10 | Code Organization & Architecture | MEDIUM | `arch-` |
| 11 | Performance Optimization | MEDIUM | `perf-` |
| 12 | Build, Compilation & Static Analysis | MEDIUM | `build-` |
| 13 | Security & Cybersecurity (ISO 21434) | HIGH | `security-` |
| 14 | Testing & Verification | MEDIUM | `test-` |
| 15 | Tool Integration (A2L/ODX/FIBEX) | MEDIUM | `integration-` |

## Quick Reference

### 1. Memory Safety & Management (CRITICAL)

- `memory-stack-over-heap` - Prefer stack allocation over heap in embedded context
- `memory-static-allocation` - Use static allocation for deterministic memory usage
- `memory-buffer-bounds` - Always validate buffer boundaries before access
- `memory-pool-pattern` - Use memory pool patterns for dynamic-like allocation
- `memory-no-malloc-in-rt` - Never use malloc/free in real-time critical paths
- `memory-raii-cpp` - Use RAII for resource management in C++ embedded code
- `memory-volatile-correctness` - Use volatile correctly for hardware registers and shared data
- `memory-alignment` - Ensure proper data structure alignment for target architecture
- `memory-zero-init` - Always initialize variables, especially in safety-critical code

### 2. MISRA C/C++ Compliance (CRITICAL)

- `misra-no-implicit-conversions` - Avoid implicit type conversions
- `misra-single-exit-point` - Prefer single function exit point for critical functions
- `misra-no-dynamic-memory` - Avoid dynamic memory allocation (Rule 21.3)
- `misra-no-recursion` - Avoid recursion in embedded context (Rule 17.2)
- `misra-switch-default` - Always include default case in switch statements
- `misra-no-goto` - Avoid goto except for error cleanup patterns in C
- `misra-boolean-expressions` - Use explicit boolean comparisons
- `misra-pointer-arithmetic` - Restrict pointer arithmetic to array indexing
- `misra-side-effects` - Avoid side effects in conditional expressions

### 3. AUTOSAR C++14 Guidelines (CRITICAL)

- `autosar-smart-pointers` - Use smart pointers instead of raw pointers for ownership
- `autosar-no-exceptions-rt` - Avoid exceptions in real-time contexts, use Result types
- `autosar-const-correctness` - Apply const-correctness throughout interfaces
- `autosar-override-final` - Always use override/final for virtual function overrides
- `autosar-enum-class` - Use enum class instead of plain enum
- `autosar-no-unions` - Avoid unions, use std::variant when needed
- `autosar-braces-init` - Prefer braced initialization to prevent narrowing
- `autosar-nodiscard` - Use [[nodiscard]] for functions with important return values

### 4. Safety & Functional Safety - ISO 26262 (HIGH)

- `safety-defensive-programming` - Apply defensive programming at module boundaries
- `safety-error-detection` - Implement error detection and plausibility checks
- `safety-redundant-checks` - Use redundant checks for critical control paths
- `safety-watchdog-pattern` - Implement watchdog monitoring patterns
- `safety-state-machine-integrity` - Protect state machine transitions from corruption
- `safety-crc-validation` - Validate data integrity with CRC for critical data
- `safety-safe-state` - Always define and reach safe state on failure
- `safety-asil-decomposition` - Follow ASIL decomposition patterns correctly

### 5. Real-Time & Timing Constraints (HIGH)

- `realtime-deterministic-execution` - Ensure deterministic execution time in cyclic tasks
- `realtime-wcet-awareness` - Design with WCET (Worst-Case Execution Time) in mind
- `realtime-no-blocking-isr` - Never block in interrupt service routines
- `realtime-priority-inversion` - Prevent priority inversion with proper locking
- `realtime-cyclic-scheduling` - Follow cyclic scheduling patterns correctly
- `realtime-interrupt-latency` - Minimize interrupt latency and ISR execution time
- `realtime-deadline-monitoring` - Implement deadline monitoring for critical tasks

### 6. Communication Protocols (HIGH)

**CAN / LIN Bus:**
- `comm-can-message-layout` - Follow proper CAN/CAN FD message layout and DBC conventions
- `comm-can-error-handling` - Handle CAN bus-off recovery and error frames
- `comm-can-fd-handling` - Handle CAN FD extended data length and bit rate switching
- `comm-lin-schedule-table` - Implement LIN schedule tables and response handling
- `comm-signal-timeout` - Implement signal timeout monitoring with default values
- `comm-network-management` - Follow NM (Network Management) state machine correctly

**Automotive Ethernet / IP Stack:**
- `comm-tcp-socket-lifecycle` - Manage TCP socket lifecycle (connect, keepalive, graceful shutdown)
- `comm-udp-datagram-handling` - Handle UDP datagrams for service discovery and streaming
- `comm-doip-implementation` - Implement Diagnostics over IP (ISO 13400) activation and routing
- `comm-arp-table-management` - Manage ARP tables and static ARP entries for deterministic networks
- `comm-icmp-handling` - Handle ICMP for network diagnostics and reachability detection
- `comm-vlan-qos-priority` - Configure VLAN tagging and QoS priority mapping (IEEE 802.1Q)
- `comm-dhcp-autoip` - Implement IP address assignment (DHCP client, AutoIP fallback)
- `comm-someip-serialization` - Use correct SOME/IP serialization for service-oriented communication
- `comm-someip-sd` - Implement SOME/IP Service Discovery (offer, find, subscribe)

**Diagnostics & Routing:**
- `comm-uds-service-handler` - Implement UDS diagnostic services with proper NRC handling
- `comm-gateway-routing` - Implement proper message routing in gateway ECUs

### 7. Concurrency & RTOS Patterns (MEDIUM-HIGH)

- `rtos-task-design` - Design tasks with single responsibility and proper priority
- `rtos-critical-section` - Minimize critical section duration
- `rtos-mutex-pattern` - Use mutexes correctly, avoid nested locking
- `rtos-message-queue` - Prefer message queues over shared memory for inter-task communication
- `rtos-no-priority-inversion` - Use priority inheritance or ceiling protocols
- `rtos-isr-to-task` - Defer ISR processing to task context via flags/queues
- `rtos-stack-sizing` - Size task stacks correctly with safety margin

### 8. CAPL Scripting — CANoe (MEDIUM-HIGH)

- `capl-canoe-message-handler` - Structure message handlers for readability and performance
- `capl-canoe-timer-pattern` - Use timer patterns correctly for cyclic and one-shot operations
- `capl-canoe-test-structure` - Structure test cases with proper setup/teardown/verification
- `capl-canoe-signal-access` - Access signals via database symbols, not raw byte manipulation
- `capl-canoe-error-frame-handling` - Handle error frames and bus-off conditions in simulation
- `capl-canoe-environment-variables` - Use environment variables for panel interaction correctly
- `capl-canoe-diagnostic-testing` - Implement diagnostic request/response testing patterns
- `capl-canoe-node-simulation` - Design node simulation with proper state machines
- `capl-canoe-multi-channel` - Multi-channel bus simulation (CAN+CAN, CAN+LIN, CAN+ETH)
- `capl-canoe-rbs-cyclic` - Cyclic Rest Bus Simulation with counter/CRC generation
- `capl-canoe-rbs-reactive` - Reactive RBS with Interaction Layer and state-dependent responses
- `capl-canoe-gateway-routing` - Gateway simulation with signal/PDU/cross-protocol routing

### 8b. CAPL — Shared Patterns (MEDIUM-HIGH)

- `capl-signal-manipulation` - Reusable signal manipulation library (ramp, sine, noise, step, sequence)

### 8c. CAPL — Fault Injection (HIGH)

- `capl-fault-can` - CAN/CAN FD fault injection (error frames, bus-off, signal stuck, timing)
- `capl-fault-lin` - LIN fault injection (checksum, no-response, header, timing)
- `capl-fault-eth` - Ethernet fault injection (link down, packet loss, latency, corruption)

### 8d. CAPL — External Integration (MEDIUM)

- `capl-ext-dll-integration` - CAPL DLL API, data exchange, thread safety, 32/64-bit
- `capl-ext-com-python` - CANoe COM automation via Python
- `capl-ext-com-csharp` - CANoe COM automation via C#
- `capl-ext-ci-cd` - CI/CD integration (Jenkins, GitLab CI, headless execution)

### 9. Code Organization & Architecture (MEDIUM)

- `arch-hal-abstraction` - Use Hardware Abstraction Layer for portability
- `arch-module-interface` - Design clean module interfaces with information hiding
- `arch-state-machine` - Implement state machines with table-driven or state-pattern approach
- `arch-callback-pattern` - Use callback patterns for decoupling layers
- `arch-config-separation` - Separate configuration from logic (calibration parameters)
- `arch-layered-architecture` - Follow layered architecture (MCAL, ECU-AL, BSW, SWC)

### 10. Performance Optimization (MEDIUM)

- `perf-loop-optimization` - Optimize loop constructs for embedded targets
- `perf-lookup-table` - Use lookup tables instead of runtime computation
- `perf-bitwise-operations` - Use bitwise operations for flag and register manipulation
- `perf-cache-friendly` - Organize data for CPU cache efficiency
- `perf-inline-critical` - Inline small, critical functions
- `perf-fixed-point` - Use fixed-point arithmetic instead of floating-point when possible
- `perf-dma-usage` - Use DMA for bulk data transfers

### 11. Build, Compilation & Static Analysis (MEDIUM)

- `build-warnings-as-errors` - Treat all compiler warnings as errors
- `build-static-analysis` - Integrate static analysis (PC-lint, Polyspace, Coverity)
- `build-compiler-flags` - Use appropriate compiler flags for safety and optimization
- `build-link-time-optimization` - Use LTO for cross-module optimization
- `build-reproducible-builds` - Ensure reproducible builds for traceability

### 12. Testing & Verification (MEDIUM)

- `test-unit-test-pattern` - Structure unit tests for embedded C/C++ (Unity, Google Test)
- `test-mock-hardware` - Mock hardware dependencies for testability
- `test-boundary-values` - Test boundary values and edge cases systematically
- `test-coverage-targets` - Meet code coverage targets per ASIL level
- `test-integration-testing` - Design integration tests for inter-module communication
- `test-hil-sil-pattern` - Structure HIL/SIL test patterns for verification

### 13. Security & Cybersecurity — ISO 21434 (HIGH)

- `security-secure-boot` - Implement secure boot chain verification
- `security-secure-communication` - Use TLS/DTLS for in-vehicle Ethernet communication
- `security-key-management` - Handle cryptographic keys with proper storage and rotation
- `security-secure-diagnostics` - Implement secure UDS authentication (0x29 service)
- `security-input-sanitization` - Sanitize all external inputs (CAN, Ethernet, diagnostic)
- `security-secure-update` - Implement secure OTA/reflash with signature verification
- `security-access-control` - Enforce access control between security domains
- `security-crypto-usage` - Use cryptographic primitives correctly (AES, HMAC, CMAC)

### 14. MISRA Grouped Topics (CRITICAL)

- `misra-type-system` - Essential type model, implicit conversions, type casting (Rules 10-11)
- `misra-control-flow` - Switch, goto, unreachable code, single exit (Rules 15-16)
- `misra-pointer-safety` - Pointer arithmetic, null checks, conversions (Rules 18, 11)
- `misra-declarations` - Variable scope, linkage, storage class (Rules 8)
- `misra-expressions` - Side effects, precedence, boolean, sizeof (Rules 12-14)
- `misra-functions` - Prototypes, parameters, return values, recursion ban (Rules 17)
- `misra-preprocessor` - Macro safety, include guards, conditional compilation (Rules 20)
- `misra-standard-library` - Banned functions, restricted headers (Rules 21-22)
- `misra-initialization` - Variable/array/struct initialization (Rules 9)
- `misra-memory-model` - Volatile, atomic access, memory barriers (Rules 19)
- `misra-concurrency` - Thread safety, shared data access (Amendment 4)
- `misra-deviation-process` - Deviation documentation, approval, common patterns

### 15. AUTOSAR Classic BSW Modules (HIGH)

- `autosar-classic-ecum` - EcuM startup/shutdown, sleep/wakeup
- `autosar-classic-bswm` - BswM mode arbitration, action lists
- `autosar-classic-com` - COM signal packing, transmission modes
- `autosar-classic-pdu-router` - PDU Router routing paths, gateway
- `autosar-classic-dcm-dem` - Dcm/Dem diagnostics, DTC management
- `autosar-classic-nvm` - NvM block configuration, CRC, read/write
- `autosar-classic-os` - AUTOSAR OS tasks, ISRs, resources, alarms
- `autosar-classic-canif-cantp` - CanIf/CanTp callbacks, flow control

### 16. AUTOSAR Adaptive ara:: APIs (HIGH)

- `autosar-adaptive-ara-com` - ara::com proxy/skeleton, service discovery
- `autosar-adaptive-ara-core` - ara::core Result<T,E>, ErrorCode, Future
- `autosar-adaptive-ara-exec` - ara::exec process lifecycle, function groups
- `autosar-adaptive-ara-diag` - ara::diag diagnostic services
- `autosar-adaptive-ara-log` - ara::log logging patterns
- `autosar-adaptive-ara-phm` - ara::phm health management, supervision
- `autosar-adaptive-ara-per` - ara::per persistency, key-value storage

### 17. ECU Boot Sequence (HIGH)

- `boot-baremetal-startup` - Bare-metal boot: startup → C runtime → main
- `boot-autosar-classic-startup` - Classic AUTOSAR EcuM/BswM boot
- `boot-autosar-adaptive-startup` - Adaptive Execution Manager boot
- `boot-bootloader-reprogramming` - UDS flash download sequence
- `boot-secure-boot-chain` - Secure boot with HSM verification

### 18. NVM Management (HIGH)

- `nvm-autosar-block-config` - AUTOSAR NvM blocks, CRC, redundancy
- `nvm-fee-ea-abstraction` - Fee/Ea Flash EEPROM Emulation
- `nvm-baremetal-flash` - Bare-metal Flash/EEPROM patterns
- `nvm-wear-leveling` - Wear leveling strategies for automotive lifetime

### 19. Power Management (MEDIUM)

- `power-ecum-sleep-wakeup` - EcuM sleep/wakeup state machine
- `power-partial-networking` - Partial networking, selective transceiver wakeup
- `power-bswm-shutdown` - BswM ordered shutdown action lists
- `power-clock-peripheral` - Clock gating and peripheral power-down
- `power-low-power-modes` - MCU low-power modes (SLEEP, STANDBY, STOP)

### 20. Automotive Ethernet Deep-Dive (HIGH)

- `eth-tsn-time-sync` - TSN time synchronization (IEEE 802.1AS / gPTP)
- `eth-tsn-traffic-shaping` - TSN traffic shaping (IEEE 802.1Qbv)
- `eth-tsn-stream-filtering` - TSN stream filtering (IEEE 802.1Qci)
- `eth-switch-configuration` - Automotive Ethernet switch configuration
- `eth-avb-streaming` - AVB Audio/Video streaming

### 21. Compiler & Static Analysis (HIGH)

- `build-gcc-warnings` - GCC warning flags for automotive
- `build-clang-analysis` - Clang-Tidy and Clang Static Analyzer
- `build-greenhills-safety` - GreenHills safety-qualified compiler
- `analysis-pclint-config` - PC-lint MISRA configuration
- `analysis-polyspace` - Polyspace Bug Finder / Code Prover
- `analysis-coverity` - Coverity embedded checkers
- `analysis-cppcheck` - cppcheck with MISRA addon
- `analysis-parasoft` - Parasoft C/C++test
- `analysis-ldra` - LDRA traceability and coverage

### 22. vTESTstudio CAPL (MEDIUM-HIGH)

- `capl-vtest-test-unit` - Test unit/group/fixture structure
- `capl-vtest-data-driven` - Data-driven testing with parameters
- `capl-vtest-xml-module` - XML test module integration
- `capl-vtest-verdict-reporting` - Verdict and reporting patterns
- `capl-vtest-stimulus-response` - Stimulus/response timing validation

### 23. Tool Integration (MEDIUM)

- `integration-a2l-calibration` - Generate and maintain A2L/ASAP2 calibration descriptions
- `integration-odx-diagnostic` - Structure ODX/PDX diagnostic descriptions correctly
- `integration-fibex-network` - Maintain FIBEX network description files
- `integration-dbc-arxml-sync` - Keep DBC/ARXML and code signal definitions synchronized
- `integration-xcp-calibration` - Implement XCP (Universal Measurement and Calibration Protocol)
- `integration-autosar-arxml` - Generate and parse AUTOSAR ARXML configuration correctly

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/memory-stack-over-heap.md
rules/misra-no-recursion.md
rules/capl-message-handler.md
```

Each rule file contains:
- Brief explanation of why it matters in automotive embedded context
- Incorrect code example with explanation
- Correct code example with explanation
- Relevant standard references (MISRA, AUTOSAR, ISO 26262)
- Additional context and impact on safety/performance

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
