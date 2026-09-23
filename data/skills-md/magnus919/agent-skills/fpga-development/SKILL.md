---
name: fpga-development
description: >-
  Design, review, simulate, and verify FPGA logic using explicit RTL contracts, clock and reset models, CDC analysis, timing constraints, and reproducible implementation evidence. Use for synthesizable HDL, fixed-point arithmetic, handshakes, testbenches, resource tradeoffs, timing closure, and FPGA release or bring-up planning. Do not use for ordinary MCU firmware, generic circuit design, a substitute vendor-tool manual, or unsupported claims of hardware or timing signoff.
license: MIT
---

# FPGA Development

Treat HDL as a description of concurrent hardware with explicit temporal and electrical interfaces. A correct design requires consistent functional intent, language semantics, clock/reset behavior, implementation constraints and verification evidence. Compilation, simulation, synthesis, timing and physical observation establish different facts.

## Operating contract

1. Identify the requested decision and design boundary: new RTL, review, simulation failure, resource problem, CDC/timing analysis, implementation or hardware release. Use the smallest complete evidence set for that decision.
2. Record device/package, board revision, clocks, reset, I/O voltage and pin constraints before making target-specific claims. Pure RTL reasoning can proceed from a stated abstract interface without inventing a board.
3. State transaction semantics, latency, throughput, backpressure, loss/duplication policy, initialization and arithmetic behavior before implementation. A waveform picture is not an interface contract.
4. Keep synthesizable design and verification-only constructs separate. Match the HDL subset and vendor primitive model to the actual simulator and synthesizer versions.
5. Review constraint coverage and exception intent before interpreting slack. A green summary with missing clocks or unconstrained endpoints is incomplete evidence.
6. Before programming, resetting, erasing or otherwise changing connected hardware, confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation. Bitstreams and programming paths must match the exact target.
7. Retain artifacts tied to one source/constraint/tool/device configuration. Do not combine yesterday's tests with today's unverified bitstream into a release claim.

## Task routing

Read only the relevant depth references; use their templates to retain reviewable decisions.

| Task | Reference | Template |
|---|---|---|
| Establish device and external interface requirements | [Target and interface contracts](references/01-target-and-interface-contracts.md) | [Target contract](templates/target-contract.md) |
| Review RTL semantics, inference and arithmetic | [RTL and arithmetic](references/02-rtl-synthesizability-and-arithmetic.md) | [RTL contract](templates/rtl-contract.md) |
| Build a self-checking verification strategy | [Simulation and verification](references/03-simulation-and-verification.md) | [Simulation plan](templates/simulation-plan.md) |
| Review clocks, reset and domain crossings | [Clocks, reset and CDC](references/04-clocks-reset-and-cdc.md) | [CDC review](templates/cdc-review.md) |
| Diagnose timing or review constraints | [Timing and constraints](references/05-timing-and-constraints.md) | [Timing review](templates/timing-review.md) |
| Decide pipelining, memory, DSP and implementation tradeoffs | [Implementation and resources](references/06-implementation-and-resource-tradeoffs.md) | RTL contract and timing review |
| Release an implementation or plan physical bring-up | [Release and hardware verification](references/07-release-and-hardware-verification.md) | [Implementation release](templates/implementation-release.md) |

## Default design and verification loop

### Specify observable behavior

Name the top-level ports, widths, signedness, units, clock domains and reset semantics. For each transaction define when acceptance occurs and when outputs become valid. Specify stalled behavior, maximum sustained rate, permitted bursts and buffering policy. Check producer and consumer rates before proposing a FIFO: finite storage cannot solve an unbounded service-rate deficit.

For numeric operations, derive intermediate widths from operand ranges and operations. Track the binary point through multiplication, accumulation, rescaling and conversion. State rounding, saturation, overflow and invalid-input policies. Test negative extrema and boundary values rather than relying on nominal positive examples.

### Implement and inspect inferred hardware

Translate the contract into synthesizable combinational and sequential structures. Review assignment completeness, reset coverage, register enables, multiple drivers, accidental latches and width/signedness conversions. Check inference reports for expected memory, DSP, carry and register structures. A behavioral implementation that simulates correctly can infer unsuitable hardware or unsupported initialization.

Avoid expanding one methodology skill into vendor runbooks. Use the exact installed tool's documentation for commands, supported language, libraries and device primitives; retain that version with the result. Device-independent examples are teaching and regression artifacts, not pin-ready projects.

### Verify temporal behavior

Build a self-checking testbench with a reference model or scoreboard, explicit timeout and diagnostic failures. Cover reset, stalls, simultaneous transfers, boundaries and parameter variants relevant to the design. Keep stimulus and checking free of sampling races. Record deterministic seeds when random stimulus is used.

Check that verification can fail: introduce a controlled local mutation that violates the contract and confirm the test rejects it. Remove the mutation from the deliverable. Passing a simulation with no effective checker provides little evidence; coverage counts show exercise, not correctness or exhaustive proof.

Formal analysis can supplement simulation when properties, assumptions, clock/reset abstraction and proof bounds are explicit. A bounded pass is not an unbounded proof; a vacuous property is not successful verification. Keep solver/tool/version and counterexample evidence with the result.

### Model clocks, resets and crossings

Inventory primary and generated clocks and their actual relationships. For each crossing distinguish single-bit level, pulse/event, coherent word, pointer or stream. Select synchronization or transfer architecture according to its semantics. Independently synchronizing each bit does not guarantee coherent words. A narrow pulse can disappear; a pulse toggle can lose events if it changes too quickly.

Make reset assertion and release behavior explicit in every domain, including one-sided reset and clock absence. Device-specific synchronizer attributes and implementation constraints need the appropriate vendor guidance. Functional simulation does not model analog metastability reliability.

### Close timing against the real interface

Validate clock and I/O constraints, generated clocks, corners, modes, ignored commands and unconstrained endpoints. Then inspect setup and hold paths, clock relationships, uncertainty, logic depth, routing contribution and exceptions. Tie any false or multicycle path to an architectural argument and verified scope; typical traffic inactivity is insufficient.

When changing pipelines, widths, memories, retiming or clocks, revisit latency and protocol behavior as well as timing. Correcting the constraint model and improving the circuit are distinct actions. Record which action changed the result and why.

### Retain release evidence

Keep source and constraint hashes, top-level and parameters, exact tool/build versions, device/package, reports, warnings, tests and output artifact hashes together. State explicitly which stages were executed: elaboration, functional simulation, synthesis, placement/routing, static timing, CDC analysis, formal analysis, programming and physical verification.

For hardware work, verify image identity, board and programming transport, documented clock/pin/I/O conditions, initial state and recovery path. Observe the specified function and relevant reset/power-cycle behavior. A successful programmer exit alone does not establish the design's behavior.

## Executable verification example

The original [ready/valid buffer](assets/rv_buffer.sv) and [self-checking testbench](assets/tb_rv_buffer.sv) demonstrate a one-entry, single-clock transfer contract with synchronous reset flushing. Run the offline [fixture checker](scripts/fpga_fixture.py) with Python 3, Icarus Verilog and Yosys:

```sh
python3 scripts/fpga_fixture.py --json --output /path/to/new-fixture-results
```

Run from the skill directory, or invoke the script by its full path. The output directory must be empty or new. Read `--help` before changing widths or seed. It records versions, source hashes and per-stage results; inspect its result JSON and retained logs. Missing tools produce an incomplete result, not successful verification. This fixture has no pin constraints, place-and-route, timing signoff, CDC or physical-hardware proof. Do not program it as an assumed board project.

The checker tests are in `scripts/test_fixture.py`. Run `python3 -m pytest scripts/test_fixture.py --no-cov -q`; integration tests require the named tools and skip explicitly when unavailable. A deliberate local mutation must fail the testbench; never retain the mutated RTL as the deliverable.

## When not to use

- ESP32 firmware, pin restrictions, framework APIs, flashing and OTA belong to the repository's `esp32-development` skill.
- Platform-neutral component selection, schematic, load/driver and bench measurement reasoning belong to the repository's `electronics` skill. Do not infer electrical compatibility from an HDL type or constraint name.
- Named vendor tool administration, installation and operational runbooks require that tool's current documentation or dedicated skill. No assumed cross-vendor constraint syntax or primitive equivalence.
- High-speed board channels, RF, EMC, power-integrity design and regulated signoff require the relevant specialist evidence. This skill can identify dependencies and missing evidence; it does not replace those reviews.

## Exit criteria

Complete when the requested artifact and decision are delivered, checks are tied to the correct revision/configuration, known limitations are explicit, and the conclusion does not exceed the executed verification stages. For diagnosis, after three non-converging passes retain the evidence and escalate the smallest unresolved question rather than applying speculative constraints or RTL patches.
