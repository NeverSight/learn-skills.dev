---
name: testing-guide
description: VST3 plugin testing patterns and practices — the broad, general-purpose testing skill. Use when writing tests, debugging test failures, adding new test cases, when tests don't appear after changes, running the test suites, or wiring integration tests. Covers build-before-test discipline, Catch2 patterns and test doubles, integration testing (processor-level wiring, parameter application, host environment), VST3 validation, and anti-patterns. For deep DSP-verification (FFT aliasing measurement, THD/SNR, click/artifact detection, spectral golden references) use the companion testing-dsp-analysis skill.
allowed-tools: Read, Grep, Glob, Bash
---

# Testing Guide for VST Plugin Development

This skill provides comprehensive guidelines for writing effective tests for this VST3 plugin project.

---

## CRITICAL: How to Run Tests (READ THIS FIRST)

**All tests are C++ executables. There is NO Python involved in testing.**

### Test Executables

| Executable | Purpose | Location |
|------------|---------|----------|
| `dsp_<layer>_tests.exe` | DSP tests, one exe per layer: core/primitives/processors/systems/effects (no single `dsp_tests` anymore) | `build/bin/Release/dsp_<layer>_tests.exe` |
| `plugin_tests.exe` | Plugin tests | `build/bin/Release/plugin_tests.exe` |
| `approval_tests.exe` | Golden master tests | `build/bin/Release/approval_tests.exe` |

### Build and Run Tests

```bash
# 1. BUILD FIRST (always!) — build only the layer you touched (no single dsp_tests anymore)
cmake --build build --config Release --target dsp_primitives_tests

# 2. Run that layer's tests — ALWAYS SHARDED (user ruling 2026-10-26; one serial exe = one core of 32)
node tools/run-gate.js --filter '~[performance]~[perf]~[benchmark]~[!benchmark]' dsp_primitives_tests

# 3. Run tests by tag — same runner, the tag goes in the filter
node tools/run-gate.js --filter '[wavefold_math]~[performance]~[perf]~[benchmark]~[!benchmark]' dsp_primitives_tests

# Timing tests (CPU budgets, benchmarks) are the one exception: alone, never sharded
node tools/run-cpu-tests.js dsp_primitives_tests

# 4. Run ONE test case by name pattern (the only direct exe run)
"F:/projects/iterum/build/windows-x64-release/bin/Release/dsp_processors_tests.exe" "*lambert*"

# 5. List all tags
"F:/projects/iterum/build/windows-x64-release/bin/Release/dsp_core_tests.exe" --list-tags
```

### DO NOT DO THIS

- **DO NOT run a whole executable, a tag, or a list of executables as serial processes** (`$t.exe | tail`, <!-- lint-serial-ok: names the anti-pattern -->
  `for t in ...`). Use `node tools/run-gate.js` — Catch2 `--shard-count`/`--shard-index` over a worker pool. A
  Profundum gate went from ~14 min serial to 2 min 15 s. This applies to gates, lanes, fixer loops, workflow
  scripts, new plugins and every new workflow. Several concurrent gates: `--share <N>` each.
- **DO NOT run Python scripts** - This is a C++ project. Tests are C++ executables.
- **DO NOT use pytest, unittest, or any Python test framework**
- **DO NOT try to "generate reference values" with Python** - Use mathematical constants or Wolfram Alpha
- **DO NOT skip the build step** - Code must compile before tests can run
- **DO NOT guess binary locations** - Binaries are in `build/bin/{Config}/`

For complete commands and examples, see [QUICK-START.md](QUICK-START.md).

---

## Quick Reference

- **Build commands**: See [QUICK-START.md](QUICK-START.md)
- **Integration testing**: See [INTEGRATION-TESTING.md](INTEGRATION-TESTING.md) **(READ THIS for any processor-level feature)**
- **VST3-specific testing**: See [VST3-TESTING.md](VST3-TESTING.md)
- **Catch2 patterns & test doubles**: See [PATTERNS.md](PATTERNS.md)
- **Anti-patterns to avoid**: See [ANTI-PATTERNS.md](ANTI-PATTERNS.md)
- **Deep DSP verification** (FFT aliasing, THD, artifact detection, spectral goldens): use the
  **testing-dsp-analysis** skill (`DSP-TESTING.md`, `SPECTRAL-ANALYSIS.md`, `ARTIFACT-DETECTION.md`)

---

## CRITICAL: Build-Before-Test Discipline

**Tests cannot run if the code doesn't compile. Period.**

### The Mandatory Workflow

After ANY code changes:

1. **Build the test target**:
   ```bash
   cmake --build build --config Debug --target dsp_tests
   ```

2. **Check for compilation errors** - Look for `error` in build output

3. **Fix errors BEFORE running tests**

4. **Only then run tests**

### When Tests Don't Appear

> **STOP. DID YOU CHECK THE BUILD OUTPUT?**
>
> If you just added new tests and they don't appear:
> 1. Your code probably doesn't compile
> 2. Run: `cmake --build build --config Debug --target dsp_tests 2>&1`
> 3. Look for `error` in the output
> 4. **FIX THE COMPILATION ERRORS FIRST**
>
> Do NOT:
> - Try different test filters
> - Blame CMake cache
> - Run `--list-tests` repeatedly

**The build output tells you EXACTLY what's wrong. Read it.**

---

## Test Suite Architecture

The project has **two separate test executables**:

| Executable | Purpose | SDK Dependencies |
|------------|---------|------------------|
| `dsp_tests` | Pure DSP algorithm tests | None (Catch2 only) |
| `vst_tests` | VST3-specific functionality tests | VST3 SDK |

### Why Two Suites?

1. **Build speed**: `dsp_tests` compiles faster without VST3 SDK headers
2. **Isolation**: DSP algorithms remain testable without VST3 infrastructure
3. **Layered architecture**: Enforces that Layer 0-4 DSP code has no VST3 dependencies

### Test Locations

```
tests/
├── unit/
│   ├── core/           # Layer 0 tests (→ dsp_tests)
│   ├── primitives/     # Layer 1 tests (→ dsp_tests)
│   ├── processors/     # Layer 2 tests (→ dsp_tests)
│   ├── systems/        # Layer 3 tests (→ dsp_tests)
│   ├── features/       # Layer 4 tests (→ dsp_tests)
│   └── vst/            # VST3 SDK tests (→ vst_tests)
├── integration/        # Integration tests
└── regression/         # Golden master tests
```

### Test Helpers

Determine which of the following helpers make sense for the code under test. The types of potential problems they help identify are vital, so consider carefully.

- **Signal generators**: `tests/test_helpers/test_signals.h`
- **Buffer comparison**: `tests/test_helpers/buffer_comparison.h`
- **Allocation detector**: `tests/test_helpers/allocation_detector.h`
- **Spectral analysis**: `tests/test_helpers/spectral_analysis.h` - FFT-based aliasing measurement
- **Statistical utilities**: `tests/test_helpers/statistical_utils.h` - Mean, stddev, median, MAD
- **Signal metrics**: `tests/test_helpers/signal_metrics.h` - SNR, THD, crest factor, kurtosis, ZCR
- **Artifact detection**: `tests/test_helpers/artifact_detection.h` - ClickDetector, LPCDetector, SpectralAnomalyDetector
- **Golden reference**: `tests/test_helpers/golden_reference.h` - Reference comparison, A/B testing
- **Parameter sweep**: `tests/test_helpers/parameter_sweep.h` - Automated parameter range testing

---

## Core Testing Philosophy

### Test Behavior, Not Implementation

The most critical principle: **tests should verify what the code does, not how it does it**.

```cpp
// BAD: Tests implementation details
TEST_CASE("DelayLine uses circular buffer internally", "[bad]") {
    DelayLine delay(1000);
    REQUIRE(delay.getWriteIndex() == 0);  // Fragile!
}

// GOOD: Tests behavior
TEST_CASE("DelayLine returns samples at specified delay", "[delay]") {
    DelayLine delay(1000);
    delay.write(0.5f);
    for (int i = 0; i < 10; ++i) delay.write(0.0f);
    REQUIRE(delay.read(10) == Approx(0.5f));
}
```

### Benefits

| Aspect | Implementation Tests | Behavioral Tests |
|--------|---------------------|------------------|
| **Refactoring** | Break frequently | Survive changes |
| **Readability** | Obscure intent | Document behavior |
| **Maintenance** | High burden | Low burden |

---

## Test Categories

### Unit Tests
Test individual DSP functions and primitives in isolation.
**Scope:** Layer 0 (Core) and Layer 1 (Primitives)

```cpp
TEST_CASE("dBToLinear converts correctly", "[dsp][unit]") {
    REQUIRE(dBToLinear(0.0f) == Approx(1.0f));
    REQUIRE(dBToLinear(-6.0206f) == Approx(0.5f).margin(0.001f));
}
```

### Component Tests
Test composed DSP processors with their dependencies.
**Scope:** Layer 2 (Processors) and Layer 3 (Systems)

### Integration Tests
Test that components work correctly **when wired together** in the processor. This is where
the most costly bugs hide — sub-components that work perfectly in isolation but fail when
integrated due to wiring bugs, per-block configuration resets, or host environment assumptions.

**Scope:** Processor-level wiring, parameter application, host environment, multi-block behavior.
**See:** [INTEGRATION-TESTING.md](INTEGRATION-TESTING.md) for complete patterns, anti-patterns, and checklist.

**Critical rule:** Integration tests must verify **behavioral correctness**, not just presence
of output. "Audio exists" is necessary but grossly insufficient — verify the output is
**correct** (right notes, right timing, right values).

### Regression Tests
Capture known-good outputs for comparison (golden masters).

---

## Essential Best Practices

### 1. Use Arrange-Act-Assert Pattern

```cpp
TEST_CASE("Filter attenuates above cutoff", "[dsp][filter]") {
    // ARRANGE
    BiquadFilter filter;
    filter.setLowpass(1000.0f, 44100.0f, 0.707f);
    std::array<float, 1024> buffer;
    generateSineWave(buffer.data(), 1024, 5000.0f, 44100.0f);

    // ACT
    filter.process(buffer.data(), 1024);

    // ASSERT
    float outputPeak = findPeak(buffer.data(), 1024);
    REQUIRE(outputPeak < 0.5f);  // At least -6dB attenuation
}
```

### 2. Use Descriptive Test Names

```cpp
// GOOD
TEST_CASE("OnePoleSmoother reaches target within 5 time constants", "[dsp][smoother]")
TEST_CASE("DelayLine handles zero-length buffer without crash", "[dsp][delay][edge]")

// BAD
TEST_CASE("testSmoother", "[dsp]")
TEST_CASE("test1", "[dsp]")
```

### 3. Test Edge Cases

```cpp
TEST_CASE("DelayLine handles edge cases", "[dsp][delay][edge]") {
    DelayLine delay(100);

    SECTION("zero delay returns current sample") {
        delay.write(0.5f);
        REQUIRE(delay.read(0) == Approx(0.5f));
    }

    SECTION("maximum delay returns oldest sample") {
        for (int i = 0; i < 100; ++i) delay.write(static_cast<float>(i));
        REQUIRE(delay.read(99) == Approx(0.0f));
    }
}
```

### 4. Test Failure Modes

```cpp
TEST_CASE("calculateRMS handles invalid input gracefully", "[dsp][analysis]") {
    SECTION("null pointer returns zero") {
        REQUIRE(calculateRMS(nullptr, 100) == 0.0f);
    }

    SECTION("zero length returns zero") {
        float buffer[4] = {1.0f, 1.0f, 1.0f, 1.0f};
        REQUIRE(calculateRMS(buffer, 0) == 0.0f);
    }
}
```

---

## Test Tags

Use consistent tags for filtering:

```cpp
// Layer tags
[core]       // Layer 0
[primitives] // Layer 1
[processors] // Layer 2
[systems]    // Layer 3
[features]   // Layer 4

// Category tags
[dsp]        // DSP algorithm
[vst3]       // VST3 specific
[state]      // State save/restore
[edge]       // Edge case
[regression] // Regression test

// Speed tags
[fast]       // < 100ms
[slow]       // > 1s
```

Run specific tests:
```bash
./dsp_tests "[dsp][fast]"    # Fast DSP tests
./dsp_tests "~[slow]"        # Exclude slow tests
./dsp_tests "[filter]"       # Filter tests only
```

---

## Floating-Point Comparison

| Situation | Strategy | Example |
|-----------|----------|---------|
| Known exact value | Direct | `REQUIRE(x == 0.0f)` |
| Approximate | Margin | `Approx(expected).margin(1e-5f)` |
| Relative precision | Epsilon | `Approx(expected).epsilon(0.01f)` |
| Near zero | Margin only | `Approx(0.0f).margin(1e-7f)` |

```cpp
// Default epsilon (scale-dependent)
REQUIRE(value == Approx(expected));

// Custom margin (absolute tolerance)
REQUIRE(value == Approx(expected).margin(0.001f));

// For near-zero values, use margin
REQUIRE(nearZeroValue == Approx(0.0f).margin(1e-6f));
```

---

## Platform-Dependent Behaviour (Windows-green ≠ CI-green)

A test can encode an assumption that is true on Windows and false on Linux/macOS. It passes
locally every time and fails only in CI, ~40 min later.

**Known divergences that have already broken CI:**

| Behaviour | Windows | Linux / glibc |
|-----------|---------|---------------|
| MXCSR (FTZ/DAZ) in a **newly created** thread | fresh default | **inherits the creator's** |
| `-ffast-math` (macOS CI) folding `quiet_NaN()`/`infinity()` | n/a | non-finite becomes finite garbage |

Real example (PR #262): a test set FTZ on the main thread, spawned a worker, and asserted the
worker did *not* flush denormals. True on Windows; on glibc `clone()` copies the FPU state, so
the worker inherited FTZ and the assertion failed. The test was also modelling the wrong thing —
a host's audio thread already exists when `setupProcessing()` runs. **Fix the model, not the
assertion**: start the worker first, then change the state.

**Verify on real Linux before pushing** — Ubuntu WSL with g++ 13 is installed:

```bash
# Compile the behaviour under test as a standalone TU; no CMake, runs in seconds.
wsl -e bash -lc 'g++ -std=c++20 -O2 -fno-fast-math \
  -I /mnt/f/projects/iterum/dsp/include /tmp/probe.cpp -o /tmp/probe -pthread && /tmp/probe'
```

Do this whenever a test depends on **threads, FP environment, locale, filesystem
case-sensitivity, `long double`, or struct padding**. Write the probe so it exercises BOTH the
old and new shape — that proves the diagnosis, not just that the new code passes.

---

## Guard Rail Tests

Ensure DSP code doesn't produce invalid output. **Important:** Never put `REQUIRE`/`INFO` inside sample-processing loops — collect metrics in the loop and assert once after. See [ANTI-PATTERNS.md #13](ANTI-PATTERNS.md#13-the-loop-assertion-catch2-performance-killer).

```cpp
TEST_CASE("DSP output contains no NaN or Inf", "[dsp][safety]") {
    Saturator sat;
    sat.prepare(44100.0, 512);
    sat.setDrive(10.0f);  // Extreme setting

    std::array<float, 512> buffer;

    SECTION("normal input") {
        generateSine(buffer.data(), 512, 440.0f, 44100.0f);
        sat.process(buffer.data(), 512);

        bool hasNaN = false, hasInf = false;
        for (float sample : buffer) {
            if (detail::isNaN(sample)) hasNaN = true;
            if (detail::isInf(sample)) hasInf = true;
        }
        REQUIRE_FALSE(hasNaN);
        REQUIRE_FALSE(hasInf);
    }

    SECTION("extreme input") {
        std::fill(buffer.begin(), buffer.end(), 1000.0f);
        sat.process(buffer.data(), 512);

        bool hasNaN = false;
        float maxAbs = 0.0f;
        for (float sample : buffer) {
            if (detail::isNaN(sample)) hasNaN = true;
            maxAbs = std::max(maxAbs, std::abs(sample));
        }
        REQUIRE_FALSE(hasNaN);
        REQUIRE(maxAbs <= 2.0f);
    }
}
```

---

## Pre-Commit Checklist

Before committing code:
1. All unit tests pass
2. No new compiler warnings
3. `vstvalidator` passes on built plugin (if plugin code changed)
4. Code coverage hasn't decreased

---

## Additional Resources

For detailed information, see the supporting files:

- [QUICK-START.md](QUICK-START.md) - Build commands, run commands, troubleshooting
- [INTEGRATION-TESTING.md](INTEGRATION-TESTING.md) - Processor-level wiring, parameter application, host environment
- [VST3-TESTING.md](VST3-TESTING.md) - Validator, state tests, processor/controller separation
- [PATTERNS.md](PATTERNS.md) - Catch2 patterns, test doubles, UI testing with mocks
- [ANTI-PATTERNS.md](ANTI-PATTERNS.md) - Common mistakes and how to avoid them

Deep DSP verification lives in the **testing-dsp-analysis** skill:
- `DSP-TESTING.md` - Test signals, THD measurement, frequency estimation, deterministic RNG
- `SPECTRAL-ANALYSIS.md` - FFT-based aliasing measurement for waveshaper and ADAA tests
- `ARTIFACT-DETECTION.md` - Click detection, LPC analysis, spectral flatness, signal quality metrics, parameter sweep testing
