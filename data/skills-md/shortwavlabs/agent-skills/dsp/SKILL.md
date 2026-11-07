---
name: dsp
description: Digital signal processing algorithms and techniques for real-time audio. Covers filter design (biquad, Moog ladder, SVF, FIR, Linkwitz-Riley), audio effects (delay, reverb, dynamics, modulation, distortion, stereo processing), sound synthesis (oscillators, bandlimited waveforms, FM/PM, noise generation, envelopes), spectral analysis (FFT, envelope detection, beat detection), and DSP utilities (fast math, interpolation, denormal prevention, dithering). Use this skill whenever implementing audio DSP in C/C++, building synthesizers or effects, writing filter code, generating waveforms, or any task involving digital audio processing — even if the user doesn't explicitly mention "DSP."
---

# DSP — Digital Signal Processing for Audio

A comprehensive reference for implementing real-time audio DSP algorithms in C/C++. Derived from the musicdsp.org community archive covering two decades of practitioner knowledge.

## When to Use This Skill

- Implementing audio filters, effects, synthesizers, or analyzers in C/C++
- Writing `processBlock()`, `process()`, or sample-by-sample DSP loops
- Designing biquad coefficients, Moog ladder filters, or state variable filters
- Building delay lines, reverbs, compressors, waveshapers, or stereo processors
- Generating bandlimited waveforms, noise, or envelopes
- Optimizing audio code with fast math approximations or denormal prevention

For circuit-accurate emulation of a specific analog circuit (matching a schematic or SPICE reference), load `circuit-to-dsp` as well: it decides structure, solver, integrator and rate from measured error; this skill supplies the building blocks.

## Architecture

The skill is organized into domain-specific references. Read the relevant file(s) for the task at hand:

| Reference | Coverage | When to read |
|-----------|----------|-------------|
| `references/filters.md` | Biquad/RBJ, Moog ladder, SVF, FIR, DC block, formant, parameter smoothing, crossover | Any filter implementation |
| `references/effects.md` | Delay, reverb, compressor/limiter, phaser/wah, waveshaper/distortion, lo-fi, stereo, convolution | Any audio effect |
| `references/synthesis.md` | Oscillators, bandlimited waveforms, FM/PM, DSF, noise, envelopes, Chebyshev waveshaping, LFOs | Any sound generation |
| `references/analysis.md` | FFT, DFT, Goertzel, Walsh-Hadamard, envelope following, beat detection, LPC, limiting | Spectral analysis, detection |
| `references/utilities.md` | Fast math (exp, log, sin, sqrt), interpolation, clipping, denormals, dithering, MIDI conversion, parameter mapping, benchmarking, lock-free FIFO | Performance optimization, conversion, audio safety |

## Implementation Principles

These principles apply across all domains:

### Sample Rate Independence
Always derive coefficients from the sample rate. Never hard-code values that assume 44.1 kHz.

```cpp
// Coefficient from frequency and sample rate
float w0 = 2.0f * M_PI * cutoffHz / sampleRate;
```

### Denormal Prevention
Floating-point denormals (subnormal numbers near zero) cause massive CPU stalls on x86. Add a tiny offset to state variables:

```cpp
static constexpr float kDenormal = 1e-24f;
// In process loop:
state += kDenormal;
```

Alternatively, flush-to-zero compiler flags (`-ffast-math` on GCC/Clang) handle this at the CPU level.

### Parameter Smoothing
Never change filter coefficients or gain values instantaneously — this causes clicks. Smooth parameters with a one-pole lowpass:

```cpp
// Time-based smoothing coefficient
float a = expf(-2.0f * M_PI / (smoothTimeMs * 0.001f * sampleRate));
// Per sample:
smoothedValue = a * smoothedValue + (1.0f - a) * targetValue;
```

### Audio Thread Safety
The process callback must never allocate memory, take locks, or call blocking OS functions. Pre-allocate all buffers, use lock-free communication for parameter updates, and avoid virtual dispatch in hot loops.

### Bilinear Transform / Prewarping
Most digital filters are derived from analog prototypes via the bilinear transform. The key mapping:

```
w0 = 2 * pi * fc / Fs
```

For higher accuracy at high frequencies, apply frequency prewarping:

```
wa = 2 * Fs * tan(w0 / 2)
```

## Code Conventions

All code examples in this skill use C/C++ with these conventions:

- `float` for audio samples (32-bit), `double` for coefficient calculation
- `sampleRate` or `sr` for sample rate in Hz
- `M_PI` for pi (define as `#ifndef M_PI ... #endif` for portability)
- Processing functions take input sample and return output sample
- State variables are class members (not globals)
- All frequencies in Hz unless explicitly noted otherwise
