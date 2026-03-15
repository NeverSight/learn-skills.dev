---
name: cpp-benchmark-testing
description: Automates benchmark test creation for C++ projects using Google Benchmark with consistent software testing patterns. Use when creating performance benchmarks, profiling tests, or when the user mentions benchmarking, Google Benchmark, or performance testing.
metadata:
  version: "1.1.0"
  activation:
    implicit: true
    priority: 2
    triggers:
      - "benchmark"
      - "benchmarking"
      - "google benchmark"
      - "performance test"
      - "profiling"
      - "microbenchmark"
    match:
      languages: ["cpp", "c", "c++"]
      paths: ["src/**/*_bench.cpp", "tests/**/*_bench.cpp", "bench/**/*.cpp", "benchmark/**/*.cpp"]
      prompt_regex: "(?i)(benchmark|benchmarking|performance test|profiling|microbenchmark|google benchmark)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# Benchmark Testing

Instructions for AI coding agents on automating benchmark test creation using consistent software testing patterns in this C++ project.

<!-- TODO: Add benchmark testing instructions -->
