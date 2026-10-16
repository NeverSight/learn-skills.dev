---
name: threenix-benchmark-webgpu
description: Measure Three.js WebGPU render or compute workloads with deterministic GPU timestamp fixtures. Use for standalone performance baselines or before/after comparisons, including TSL work.
---

# Benchmark Three.js WebGPU work

Measure a representative render or compute workload without changing production code. Read [the benchmark guide](BENCHMARK.md) for the runner command, fixture contract, and interpretation limits.

1. Inspect the target project, its Three.js version, the real code path, and any existing fixture. Choose fixed inputs that represent the requested workload. The bundled runner needs a hardware WebGPU adapter with timestamp queries and a Node-compatible fixture; browser-only behavior needs a browser measurement instead.
2. Build or adapt a fixture around the actual target code. Declare edited source dependencies and fixed workload inputs. Do not substitute the guide's synthetic example for a component measurement. If a faithful fixture cannot run, report the limitation without inventing timings.
3. Run the bundled `scripts/benchmark.mjs` into a new output directory. Repeat the unchanged workload to establish timing noise. For an edit comparison, capture the baseline **before** the edit and use `--baseline` with the same fixture and settings afterward. Keep the original artifacts intact.
4. Inspect GPU timing samples, workload and environment compatibility, shader snapshots, and output bytes. Investigate output differences. Repeat A/B runs under comparable conditions before claiming an improvement.
5. Report the fixture, hardware, settings, artifact paths, medians and p05–p95 ranges, output comparison, and uncertainty. Pass timing does not identify the limiting shader stage or predict application FPS. A standalone baseline is a measurement, not a speedup claim.
