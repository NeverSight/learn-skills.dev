---
name: electronics
description: >-
  Design, review, prototype, measure, and troubleshoot electronic circuits using component evidence, worst-case calculations, interface contracts, and staged bench verification. Use for component selection, analog or digital building blocks, power and protection, sensor conditioning, schematic-to-wiring review, instrumented diagnosis, and I2C electrical integration. Do not use as a substitute for exact device documentation, ESP32 firmware operations, FPGA RTL development, named CAD-tool operation, or regulated design certification.
license: MIT
---

# Electronics

Turn a desired physical behavior into a justified circuit and an observable verification result. Treat the schematic, components, layout, power source, load, measurement setup, and environment as one system. A plausible schematic or successful simulation is an intermediate artifact, not proof of a working assembly.

## Working contract

1. Identify the requested decision: explain, calculate, select, review, diagnose, build, or verify. Produce the artifact needed for that decision; do not demand a full design dossier for a bounded calculation.
2. Record exact component and board identities when device-specific claims matter. Use the manufacturer datasheet revision, package and operating conditions. Separate recommended operation, absolute maximum, typical performance, guaranteed bounds and measured behavior.
3. Model the relevant signal, power, timing and thermal paths. State units, sign conventions, assumptions and corners. Compute a useful conditional result from supplied hypothetical inputs; do not invent missing measurements or guaranteed ratings.
4. Define acceptance before experimentation. Each measurement needs a predicted value/range, instrument configuration, validity limits and a decision it will resolve.
5. Change one explanatory variable at a time when feasible. Preserve the initial symptom and distinguish observation from hypothesis and inference.
6. Before changing wiring, applying power, driving signals or operating connected equipment, confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation. Obtain the measurement and recovery plan appropriate to the actual energy and fault paths.
7. Stop if the next action exceeds verified device, instrument or isolation limits. Missing high-risk facts require a bounded evidence request, not a guessed command or connection.

## Route the work

Load only the references needed for the current decision. Each reference contains assumptions, worked reasoning, failure patterns and acceptance guidance; templates turn that reasoning into reviewable artifacts.

| Task | Reference | Artifact |
|---|---|---|
| Choose or replace a component | [Component selection](references/component-selection.md) | [Component contract](templates/component-contract.md) |
| Bound a ratio, threshold, accuracy or loading error | [Tolerance and error budgets](references/tolerances-and-error-budgets.md) | [Calculation record](templates/design-calculation-record.md) |
| Review a supply, switch, driver, clamp or heat problem | [Power, thermal and protection](references/power-thermal-and-protection.md) | Component contract and calculation record |
| Review amplification, thresholds, logic and interface behavior | [Analog and digital building blocks](references/analog-and-digital-building-blocks.md) | Component contract |
| Integrate or calibrate a sensor | [Sensors and conditioning](references/sensors-and-conditioning.md) | [Calibration plan](templates/sensor-calibration-plan.md) |
| Translate a schematic into physical connections | [Schematic to bench](references/schematic-to-bench.md) | [Schematic review](templates/schematic-review.md) |
| Choose or interpret a measurement | [Measurement and instrumentation](references/measurement-and-instrumentation.md) | [Measurement plan](templates/measurement-plan.md) |
| Review I2C electrical behavior and transaction evidence | [I2C integration](references/i2c-integration.md) | [Bus electrical budget](templates/bus-electrical-budget.md) |
| Localize a fault | [Fault isolation](references/fault-isolation.md) | [Fault ledger](templates/fault-ledger.md) |
| Accept an assembly and its observed behavior | [Assembly and verification](references/assembly-and-verification.md) | [Assembly acceptance](templates/assembly-acceptance.md) |

## Default engineering sequence

### 1. Establish function and boundaries

Record what the circuit must do and what failure would mean. Identify supplies, loads, signal ranges, timing or bandwidth, duty cycle, environment, allowable error and operating modes. Distinguish a component, a module with additional circuitry, and a complete board. A photograph can suggest identity but cannot establish pinout, rating, isolation or health.

Request only missing inputs that affect the decision. Label each as blocking, useful for confidence, or unnecessary for the current calculation. If specifications conflict, surface the conflict and present feasible changes rather than selecting a nominal compromise silently.

### 2. Build the model and compare corners

Use the actual topology. Include parallel paths, source/load impedance, bias/leakage, power-up states and temperature dependencies where material. State whether an error budget is a guaranteed bound or a statistical estimate and why the combination method is valid. Do not combine correlated systematic errors as independent noise.

Evaluate component and instrument limitations together. A meter or probe changes the circuit it observes. A low DC error does not establish settling, stability, bandwidth or noise performance. A protection device must survive the relevant fault waveform and leave the protected device inside its own limits.

Record the controlling corner and margin, then identify assumptions whose uncertainty could reverse the decision. Prefer a simple independently checked model over an elaborate simulation with undocumented component models.

### 3. Review physical implementation

Trace current loops, return paths, polarity, reference nodes, connectors and power sequencing. Check schematic connectivity against the real breadboard or assembly. Identify paths that can back-power an unpowered device. Separate board logic pins from load power paths; driver and protection choices depend on the actual load and fault conditions.

Do not treat generic layout advice as a verified PCB design. Trace the relevant coupling or current-return mechanism, consult the actual component's guidance, and specify how the proposed arrangement will be tested.

### 4. Plan and perform bounded verification

Start with appropriate unpowered inspection and continuity/resistance checks, then controlled power and progressively enabled functions. Meter mode, lead jack, probe rating, reference connection and energy source must be correct for the measurement. A current limit is not a substitute for understanding stored energy or the instrument grounding path.

For connected hardware, retain target identity, instrument configuration, initial state, expected result, observation and restoration steps. A bus scan is an active transaction and may change a device; an ACK is not an identity or functional test.

### 5. Decide and retain evidence

Conclude with one of: accepted for the stated conditions; rejected with the controlling failure; conditionally acceptable under named assumptions; or inconclusive with the smallest decisive next test. Separate modeled, simulated and physically measured evidence. Record design/firmware revision when software affects the circuit.

For a measurement diagnosis, include a compact evidence row even in a short
answer: quantity/test point, stated instrument configuration, model prediction,
reported observation, interpretation and next check. Mark supplied readings as
user-reported and unperformed measurements as planned; do not turn a prediction
into a claimed observation. Use the measurement template for larger tasks.

For troubleshooting, stop after three non-converging passes and summarize the evidence, eliminated hypotheses, remaining uncertainty and next specialist or artifact needed. Do not keep swapping components or repeating scans without a new hypothesis.

## When not to use

- For ESP32 board identification, pin restrictions, firmware frameworks, flashing, boot/recovery or OTA, use the repository's `esp32-development` skill. This skill still owns the electrical model and measurement reasoning for the attached circuit; do not duplicate framework instructions here.
- For programmable-logic architecture, RTL, simulation, synthesis or timing closure, use the repository's `fpga-development` skill. Electrical compatibility remains part of this skill's scope.
- For a named CAD, simulator, programmer or instrument automation system, consult its exact tool documentation or existing operational skill. Do not invent nonexistent catalog routes.
- Mains, high energy, RF/high-speed layout, functional safety, medical or other regulated acceptance requires the appropriate specialist evidence and review. This skill can organize requirements and evidence; it cannot confer certification or replace those disciplines.

## Completion criteria

The requested decision has a concrete artifact; assumptions and unknowns are visible; calculations and units are reproducible; chosen operating conditions are justified; relevant measurements or outstanding tests are recorded; and the conclusion matches the strength and scope of the evidence. An analysis task can finish with a sound conditional result. A hardware verification task cannot finish on calculation or simulation alone.
