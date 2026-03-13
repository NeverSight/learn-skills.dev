---
name: go-benchmark-testing
description: Automates benchmark test creation for Go projects using the standard testing package with consistent software testing patterns. Use when creating performance benchmarks, profiling tests, or when the user mentions benchmarking, performance testing, or optimization.
metadata:
  version: "1.0.0"
  activation:
    implicit: true
    priority: 2
    triggers:
      - "benchmark"
      - "benchmarking"
      - "performance test"
      - "profiling"
      - "microbenchmark"
      - "optimization"
      - "performance"
    match:
      languages: ["go", "golang"]
      paths: ["pkg/**/*_test.go", "internal/**/*_test.go"]
      prompt_regex: "(?i)(benchmark|benchmarking|performance test|profiling|microbenchmark|optimization|performance)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# Benchmark Testing

Instructions for AI coding agents on automating benchmark test creation using consistent software testing patterns in this Go project.

- [1. Benefits](#1-benefits)
- [2. Patterns](#2-patterns)
  - [2.1. Microbenchmarking](#21-microbenchmarking)
  - [2.2. Comparative Benchmarking](#22-comparative-benchmarking)
  - [2.3. Memory Profiling](#23-memory-profiling)
  - [2.4. Statistical Benchmarking](#24-statistical-benchmarking)
  - [2.5. Sub-benchmarks](#25-sub-benchmarks)
  - [2.6. Table-Driven Testing](#26-table-driven-testing)
- [3. Workflow](#3-workflow)
- [4. Commands](#4-commands)
- [5. Style Guide](#5-style-guide)
- [6. Template](#6-template)
  - [6.1. Multi-Scenario Benchmarks](#61-multi-scenario-benchmarks)
  - [6.2. Simple Benchmarks](#62-simple-benchmarks)
  - [6.3. Benchmarks with Validation](#63-benchmarks-with-validation)
- [7. References](#7-references)

## 1. Benefits

- Performance Measurement
  > Benchmark tests measure the execution time and memory allocation of functions, providing quantifiable metrics for performance analysis.

- Regression Detection
  > Continuous benchmarking helps identify performance regressions early in the development cycle before they reach production.

- Optimization Guidance
  > Benchmark results guide optimization efforts by identifying bottlenecks and quantifying the impact of performance improvements.

- Comparative Analysis
  > Benchmarks enable comparison of different implementations or algorithms to make informed decisions about performance trade-offs.

- Resource Profiling
  > Memory allocation tracking helps identify unnecessary allocations and optimize memory usage patterns.

## 2. Patterns

### 2.1. Microbenchmarking

Microbenchmarking is a software testing technique that measures the performance of small, isolated code units to identify performance characteristics and bottlenecks.

### 2.2. Comparative Benchmarking

Comparative Benchmarking is a testing approach that compares the performance of different implementations or algorithms side-by-side using consistent workloads.

### 2.3. Memory Profiling

Memory Profiling is the process of measuring memory allocations and usage patterns during benchmark execution using `-benchmem` flag.

### 2.4. Statistical Benchmarking

Statistical Benchmarking uses multiple iterations to calculate statistical measures (mean, variance) to ensure reliable and reproducible results.

### 2.5. Sub-benchmarks

Sub-benchmarks organize related benchmark cases using `b.Run()` to group variations of the same function with different input scenarios.

### 2.6. Table-Driven Testing

Table-Driven Testing is a software testing technique in which benchmark cases are organized in a tabular format to systematically cover different input scenarios.

## 3. Workflow

1. Identify

    Identify performance-critical functions in `pkg/` or `internal/` that benefit from performance tracking (e.g., `pkg/<package>/<file>.go`).

2. Add/Create

    Create benchmark tests in the same package (e.g., `pkg/<package>/<file>_test.go`).

3. Benchmark Test Coverage Requirements

    Focus on functions that:
    - Are called frequently in hot paths
    - Perform mathematical operations or calculations
    - Process data structures or collections
    - Have multiple implementation approaches to compare
    - Are candidates for optimization

4. Apply Templates

    Structure all benchmark tests using the [template](#6-template) pattern.

5. Baseline Measurements

    Establish performance baselines by running benchmarks on stable code before making changes.

## 4. Commands

| Command                                                         | Description                                        |
| --------------------------------------------------------------- | -------------------------------------------------- |
| `make go-test-bench`                                            | Execute all benchmarks with memory statistics      |
| `go test -bench=BenchmarkPercent -benchmem ./pkg/percent`       | Execute a specific benchmark function              |
| `go test -bench=. -benchmem -cpuprofile=cpu.prof ./pkg/percent` | Generate CPU profile for performance analysis      |
| `go test -bench=. -benchmem -memprofile=mem.prof ./pkg/percent` | Generate memory profile for allocation analysis    |
| `go test -bench=. -benchtime=10s ./pkg/percent`                 | Run benchmarks for a specific duration             |
| `benchstat old.txt new.txt`                                     | Compare benchmark results before and after changes |

## 5. Style Guide

- Test Framework
  > Use the standard Go `testing` package with `testing.B` for benchmark tests.

- Include Imports
  > Include `testing` and any packages needed for the function under test.

- Benchmark Function Naming
  > Name benchmark functions with the `Benchmark` prefix followed by the function name (e.g., `BenchmarkPercent` for testing `Percent()`).

- Benchmark Loop
  > Use `b.Loop()` to control the number of iterations. The testing framework automatically adjusts the loop iterations to get reliable timing measurements. `b.Loop()` is preferred over `b.N` as it provides better integration with the testing framework and more accurate measurements. Unlike `b.N`-style benchmarks, `b.Loop()` integrates timer management, it automatically handles `b.ResetTimer()` at the loop's start and `b.StopTimer()` at its end, eliminating the need to manually manage the benchmark timer for setup and cleanup code.

- Timer Control
  > When using `b.Loop()`, timer management is automatic and no manual `b.ResetTimer()`, `b.StopTimer()`, or `b.StartTimer()` calls are needed for typical benchmarks. For advanced scenarios not using `b.Loop()`, use `b.ResetTimer()` to exclude setup time from measurements and `b.StopTimer()`/`b.StartTimer()` to exclude specific operations.

- Sub-benchmarks
  > Use `b.Run()` to organize related benchmark cases with different input scenarios. Each sub-benchmark runs independently with its own `b.N` iterations.

- Memory Reporting
  > Use `b.ReportAllocs()` to report memory allocations per operation when not using `-benchmem` flag.

- Result Validation
  > Optionally validate results in benchmarks to prevent compiler optimizations from eliminating dead code.

## 6. Template

Use this template for new benchmark test functions. Replace placeholders with actual values and adjust as needed for the use case.

### 6.1. Multi-Scenario Benchmarks

For benchmarking multiple scenarios or input variations, use sub-benchmarks with table-driven approach.

```go
func Benchmark<FunctionName>(b *testing.B) {
	// Define benchmark cases with different scenarios
	benchmarks := []struct {
		name   string
		param1 <type>
		param2 <type>
		// Add more parameters as needed
	}{
		{
			name:   "scenario description 1",
			param1: <value1>,
			param2: <value2>,
		},
		{
			name:   "scenario description 2",
			param1: <value1>,
			param2: <value2>,
		},
		// Add more benchmark cases
	}

	for _, bm := range benchmarks {
		b.Run(bm.name, func(b *testing.B) {
			// Arrange
			// Setup code here (automatically excluded from timing by b.Loop)

			// Act
			for b.Loop() {
				_, _ = <Function>(bm.param1, bm.param2)
			}
		})
	}
}
```

### 6.2. Simple Benchmarks

For benchmarking a single scenario, use a simple loop without sub-benchmarks.

```go
func Benchmark<FunctionName>(b *testing.B) {
	// Arrange
	// Setup code here (automatically excluded from timing by b.Loop)
	param1 := <value1>
	param2 := <value2>

	// Act
	for b.Loop() {
		_, _ = <Function>(param1, param2)
	}
}
```

### 6.3. Benchmarks with Validation

For benchmarks that need to prevent compiler optimizations, store results in package-level variables.

```go
var (
	benchResult <type>
	benchError  error
)

func Benchmark<FunctionName>(b *testing.B) {
	// Arrange
	// Setup code here (automatically excluded from timing by b.Loop)
	param1 := <value1>
	param2 := <value2>

	// Act
	for b.Loop() {
		benchResult, benchError = <Function>(param1, param2)
	}
}
```

## 7. References

- Go [Benchmarks](https://pkg.go.dev/testing#hdr-Benchmarks) documentation.
- Go [testing.B](https://pkg.go.dev/testing#B) package documentation.
- Go [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat) tool documentation.
