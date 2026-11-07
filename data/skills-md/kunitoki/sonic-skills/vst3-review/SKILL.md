---
name: vst3-review
description: >
  Reviews VST3 plugin implementations for spec compliance, host compatibility, and correctness.
  Use when the user asks to review a VST3 plugin, check bus arrangements, audit parameter
  handling, or verify their process() callback is safe. Trigger on phrases like "review my
  VST3 plugin", "check VST3 bus arrangement", "is my VST3 process safe", "audit my
  IAudioProcessor", or when you see IComponent, IAudioProcessor, IEditController,
  ProcessData, or Vst:: namespaced types in the code.
---

# VST3 Plugin Review

VST3's split controller/processor model and bus negotiation are the most common sources of host incompatibility. Issues are rarely compile-time errors — they surface as broken recall, silence, or crashes in specific DAWs.

## Step 0 — Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds VST3-specific spec compliance and host compatibility checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 — Identify plugin structure

Locate the three core interfaces and their ownership:

| Interface | Thread | Responsibilities |
|-----------|--------|-----------------|
| `IComponent` | Main thread | Bus layout, activation, state save/load, unit info |
| `IAudioProcessor` | Audio thread in `process()`; main thread otherwise | Bus arrangement negotiation, latency, processing setup |
| `IEditController` | Main thread | Parameter definitions, UI, MIDI mapping, `setComponentState` |
| `IConnectionPoint` | Main thread | Processor↔controller messaging via `notify()` |

## Step 2 — Scan for VST3-specific violations

| Violation | Where | Risk |
|-----------|-------|------|
| `process()` allocating memory or acquiring a lock | `IAudioProcessor::process` | Realtime violation — causes xruns and glitches |
| Latency not reported via `getLatencySamples()` | `IAudioProcessor` | Host delay compensation broken — early mixdown or timing drift |
| Bus arrangement not matching what was negotiated in `setBusArrangements` | `setBusArrangements` / `process` | Channel count mismatch — buffer overread or silent output |
| `ParamID` not stable across save/load and plugin versions | `IEditController` | Parameter recall broken — automation and presets silently map to wrong params |
| Calling `IHostApplication` or `IComponentHandler` from audio thread | `process()` | Not thread-safe — host component handler is main-thread only |
| `IParamValueQueue` not fully consumed each `process()` callback | `process()` | Parameter updates lost — automation steps skipped |
| Bypass parameter not passing audio through cleanly | `IAudioProcessor` / controller parameter setup | Incorrect bypassed output — artifacts or silence when host automates bypass |
| `kOfflineProcessing` mode not handled separately from realtime | `setProcessing` / `process` | Offline rendering broken — wrong timing, denormal handling, or lookahead |
| `setComponentState` not applied by controller on load | `IEditController::setComponentState` | Controller shows stale values after preset load |
| `setState` / `getState` on IComponent and IEditController not symmetric | Both | Preset corruption — one side saves data the other ignores |

## Step 3 — Write the review

```
## VST3 Plugin Review: `[file / processor class]`

### Verdict
[Spec-compliant | Has critical violations | Warnings only] — [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [one sentence on spec / thread safety / host compat risk]
Fix: [concrete VST3-idiomatic suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns — clean bus negotiation, stable ParamIDs, latency reported, etc.]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Fix |
|-----------|-----|
| Allocation in `process()` | Move to `setupProcessing()` or constructor; use pre-sized buffers |
| Missing latency report | Override `getLatencySamples()` and return a stable value; call `restartComponent(kLatencyChanged)` if it changes |
| Bus mismatch | Store the accepted arrangement from `setBusArrangements`; validate `numInputs`/`numOutputs` against it in `process()` |
| Unstable `ParamID` | Use a fixed enum or stable CRC of the param name string; never use a container index |
| Params not consumed | Iterate `inputParameterChanges` fully each block; apply at sample-accurate offsets |
| Unsafe bypass | Mark the bypass parameter with `ParameterInfo::kIsBypass`; when bypassed, copy inputs to outputs with no modification and keep consuming parameter changes |

For deep detail on bus negotiation, parameter ID stability, latency reporting, controller↔processor communication, and per-DAW compatibility quirks see `references/vst3-pitfalls.md`.
