---
name: dsp-engineer
description: Think DSP-inspired signal-processing engineering guide for C++ implementations. Use when Codex needs to explain, design, debug, or implement DSP analysis/synthesis workflows involving Signal/Wave/Spectrum models, FFT/DFT/DCT, spectra, spectrograms, harmonics, aliasing, noise, autocorrelation and pitch estimation, convolution, LTI systems, impulse responses, filtering, modulation, sampling, interpolation, or translating Think DSP/Python/NumPy examples into C++.
---

# DSP Engineer

## Overview

Use this skill to reason about digital signal processing the way Think DSP teaches it: start with programmable signals, inspect the time and frequency domains, then turn the idea into clear C++.

This skill complements the `dsp` skill in this repository. Use `dsp` for production-ready audio algorithms and cookbook implementations; use `dsp-engineer` for concept-first analysis, derivations, experiment scaffolding, and translating Think DSP-style Python/NumPy examples into C++.

## Source

This skill is based on a review of Think DSP by Allen B. Downey, Green Tea Press, copyright 2014, distributed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0. Treat the references here as transformed engineering notes, not as a replacement for the book. Attribute Think DSP when using its explanations, exercises, or example structure.

## Workflow

1. Classify the task as synthesis, analysis, transformation, comparison, resampling, or system modeling.
2. Establish units first: sample rate in Hz, duration in seconds, frame count, bin spacing, Nyquist/folding frequency, amplitude convention, and whether the signal is real or complex.
3. Choose the representation:
   - `Signal`: a mathematical signal that can be evaluated at times.
   - `Wave`: sampled values plus sample rate and start time.
   - `Spectrum`: complex frequency bins plus bin frequencies.
   - `Spectrogram`: a time-indexed set of short-time spectra.
4. Build the smallest C++ experiment that proves the idea. Prefer `std::vector<double>` and `std::complex<double>` for analysis code; use `float` and library FFTs only after the behavior is correct.
5. Validate with round trips and invariants: DFT then IDFT, DCT then inverse DCT, convolution direct versus frequency-domain multiplication, known harmonic peaks, expected alias folds, or known autocorrelation lag.
6. Only then optimize for real-time constraints: preallocate, avoid locks and allocations in audio callbacks, smooth parameters, and replace direct DFT examples with an FFT library.

## Reference Map

Read only the files needed for the current task:

| Reference | Read when |
| --- | --- |
| `references/thinkdsp-concepts.md` | Need the Think DSP chapter map, concept summaries, equations, or task routing. |
| `references/cpp-patterns.md` | Need C++ translations of the book's Python/NumPy examples. |
| `references/engineering-checks.md` | Need implementation checks, scaling conventions, test cases, common DSP failure modes, or coherent-tone/sub-sample-phase error measurement. |
| `assets/thinkdsp.hpp` | Need a compact educational C++ header to copy into a prototype or use as a reference implementation. |

## C++ Defaults

- Use `double` for offline analysis and examples; move to `float` in real-time paths when tests pass.
- Use `std::complex<double>` for DFT, DCT derivations, transfer functions, modulation, and phase-aware work.
- Name sample rate `sampleRate`, frame count `n`, time samples `ts`, amplitudes `ys`, complex bins `hs`, and bin frequencies `fs`.
- Define DFT as `X[k] = sum_n x[n] * exp(-i * 2*pi*k*n/N)` and inverse DFT as `x[n] = (1/N) * sum_k X[k] * exp(i * 2*pi*k*n/N)`.
- For a real sinusoid exactly on bin `k`, estimate amplitude as `2 * abs(X[k]) / N`, except DC and the Nyquist bin.
- Use a proven FFT for production: FFTW, KissFFT, pffft, JUCE `dsp::FFT`, vDSP, IPP, or the host framework's FFT. The direct DFT examples in this skill are for clarity and small tests.

## Engineering Rules

- Check Nyquist before synthesis, analysis, downsampling, or modulation. A component above `sampleRate / 2` aliases unless removed before sampling.
- Window finite segments before spectral analysis unless the segment is exactly periodic. Hamming is a good default; choose other windows deliberately.
- Distinguish circular convolution from linear convolution. Zero-pad before FFT convolution when the signal should not wrap.
- Treat bin 0 as DC/bias. Differentiation destroys it, and integration cannot recover it without a constant of integration.
- Treat frequency-domain filters as complex operations. Magnitude changes amplitude; angle changes phase.
- Use spectrogram segment length as a resolution tradeoff: time resolution is `N / sampleRate`; frequency resolution is `sampleRate / N`.
- Validate noise by distribution, serial correlation, and log-log power slope. White is slope near 0, pink is near `-beta`, Brownian/red is near -2.
