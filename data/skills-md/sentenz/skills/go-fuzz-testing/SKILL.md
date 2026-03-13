---
name: go-fuzz-testing
description: Automates fuzz test creation for Go projects using Go's native fuzzing engine with consistent software testing patterns. Use when creating fuzz tests, mutation testing, or when the user mentions fuzzing, coverage-guided testing, or property-based testing.
metadata:
  version: "1.0.0"
  activation:
    implicit: true
    priority: 1
    triggers:
      - "fuzz"
      - "fuzzing"
      - "fuzz test"
      - "mutation testing"
      - "coverage-guided"
      - "property-based"
      - "security test"
    match:
      languages: ["go", "golang"]
      paths: ["pkg/**/*_test.go", "internal/**/*_test.go", "testdata/fuzz/**"]
      prompt_regex: "(?i)(fuzz|fuzzing|fuzz test|mutation test|coverage-guided|property-based|fuzz test|security test)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# Fuzz Testing

Instructions for AI coding agents on automating fuzz test creation using consistent software testing patterns in this Go project.

- [1. Benefits](#1-benefits)
- [2. Patterns](#2-patterns)
  - [2.1. Coverage-Guided Fuzzing](#21-coverage-guided-fuzzing)
  - [2.2. Corpus-Driven Fuzzing](#22-corpus-driven-fuzzing)
  - [2.3. Property-Based Testing](#23-property-based-testing)
  - [2.4. Boundary Value Fuzzing](#24-boundary-value-fuzzing)
  - [2.5. Crash Detection](#25-crash-detection)
- [3. Workflow](#3-workflow)
- [4. Commands](#4-commands)
- [5. Style Guide](#5-style-guide)
- [6. Template](#6-template)
  - [6.1. Multi-Parameter Functions](#61-multi-parameter-functions)
  - [6.2. Single-Parameter Functions](#62-single-parameter-functions)
- [7. References](#7-references)

## 1. Benefits

- Coverage-Guided Exploration
  > Go's native fuzzing engine uses code coverage instrumentation to automatically guide input generation toward unexplored code paths, maximizing bug discovery without manual intervention.

- Automated Input Generation
  > Fuzz testing automatically generates random inputs to discover edge cases and unexpected behaviors that manual testing might miss.

- Security Vulnerability Discovery
  > Helps identify security vulnerabilities, crashes, and undefined behaviors by testing with malformed, unexpected, or extreme inputs.

- Continuous Testing
  > Fuzz tests can run continuously to explore the input space over time, discovering new edge cases as the corpus grows.

- Regression Prevention
  > Once a crash or bug is found, the input is saved in the corpus to prevent regression in future test runs.

## 2. Patterns

### 2.1. Coverage-Guided Fuzzing

Coverage-Guided Fuzzing is the primary fuzzing technique used by Go's native fuzzing engine. It automatically instruments code to track coverage and guides input generation toward unexplored code paths, maximizing code exploration and bug discovery.

### 2.2. Corpus-Driven Fuzzing

Corpus-Driven Fuzzing is a software testing technique that uses a collection of seed inputs (corpus) as the starting point for generating new test inputs through mutation.

### 2.3. Property-Based Testing

Property-Based Testing is a testing approach that verifies invariants and properties that should hold true for all inputs, rather than testing specific input-output pairs.

### 2.4. Boundary Value Fuzzing

Boundary Value Fuzzing focuses on testing edge cases and boundary conditions with randomly generated inputs around critical thresholds.

### 2.5. Crash Detection

Crash Detection is the process of identifying inputs that cause panics, runtime errors, or undefined behavior in the code under test.

## 3. Workflow

1. Identify

    Identify functions in `pkg/` or `internal/` that accept external inputs, perform calculations, or have edge cases worth fuzzing (e.g., `pkg/<package>/<file>.go`).

2. Add/Create

    Create fuzz tests in the same package (e.g., `pkg/<package>/<file>_test.go`).

3. Fuzz Test Coverage Requirements

    Focus on functions that:
    - Accept numeric inputs (integers, floats)
    - Perform mathematical operations (division, multiplication)
    - Have boundary conditions (min/max values, zero checks)
    - Return errors for invalid inputs
    - Use generics or type constraints

4. Apply Templates

    Structure all fuzz tests using the [template](#6-template) pattern.

5. Seed Corpus

    Optionally provide seed inputs in `testdata/fuzz/<FuzzTestName>/` directory to guide fuzzing toward interesting inputs.

## 4. Commands

| Command                                | Description                                  |
| -------------------------------------- | -------------------------------------------- |
| `make go-test-fuzz`                    | Execute fuzz tests for a specified duration  |
| `ls -la testdata/fuzz/<FuzzTestName>/` | Inspect the seed corpus and generated inputs |

## 5. Style Guide

- Test Framework
  > Use the standard Go `testing` package with `testing.F` for fuzz tests. Go's fuzzing engine automatically uses coverage-guided fuzzing to explore code paths.

- Coverage-Guided Behavior
  > The fuzzing engine tracks code coverage during execution and prioritizes inputs that explore new code paths. No manual configuration is required - coverage guidance is automatic.

- Include Imports
  > Include `testing` and any packages needed for the function under test.

- Fuzz Function Naming
  > Name fuzz functions with the `Fuzz` prefix followed by the function name (e.g., `FuzzPercent` for testing `Percent()`).

- Seed Corpus
  > Use `f.Add()` to provide seed inputs that cover important edge cases and known valid/invalid inputs. The fuzzer will mutate these seeds while maximizing coverage.

- Fuzz Target
  > The fuzz target function receives `*testing.T` and randomly generated inputs. It should:
  > - Validate inputs before calling the function under test (skip invalid inputs with `t.Skip()` if necessary)
  > - Call the function with fuzzed inputs
  > - Assert invariants and properties that must always hold true
  > - Not crash or panic for any input

- Error Handling
  > Fuzz tests should verify that functions handle errors gracefully without panicking.

- Assertions
  > Use explicit checks with `t.Errorf()` or `t.Fatalf()` to report violations of expected properties.

## 6. Template

Use this template for new fuzz test functions. Replace placeholders with actual values and adjust as needed for the use case.

### 6.1. Multi-Parameter Functions

For functions with multiple parameters, use a struct array to define test cases.

```go
func Fuzz<FunctionName>(f *testing.F) {
	// Seed corpus with edge cases using testcases array
	testcases := []struct {
		param1 <type>
		param2 <type>
		// Add more parameters as needed
	}{
		{<value1>, <value2>}, // description of test case
		{<value1>, <value2>}, // description of test case
		// Add more test cases
	}
	for _, tc := range testcases {
		f.Add(tc.param1, tc.param2) // Use f.Add to provide a seed corpus
	}

	f.Fuzz(func(t *testing.T, param1 <type>, param2 <type>) {
		// Arrange
		// Optional: skip invalid inputs or prepare test conditions
		// Example: if input < 0 { t.Skip("negative inputs not interesting") }

		// Act
		got, err := <Function>(param1, param2)

		// Assert
		// Verify properties that should always hold true
		// Example 1: Function should never panic
		// Example 2: If no error, result should meet certain properties
		// Example 3: If error, result should be in expected error state

		if err != nil {
			// Verify error cases
			// Example: if got != 0 { t.Errorf("expected zero result on error, got %v", got) }
		} else {
			// Verify success cases and invariants
			// Example: if got < 0 { t.Errorf("result should be non-negative, got %v", got) }
		}
	})
}
```

### 6.2. Single-Parameter Functions

For functions with a single parameter, use a slice array to define test cases.

```go
func Fuzz<FunctionName>(f *testing.F) {
	// Seed corpus with edge cases using testcases array
	testcases := []<type>{
		<value1>, // description
		<value2>, // description
		// Add more test cases
	}
	for _, tc := range testcases {
		f.Add(tc) // Use f.Add to provide a seed corpus
	}

	f.Fuzz(func(t *testing.T, param <type>) {
		// Arrange
		// Optional: skip invalid inputs or prepare test conditions

		// Act
		got, err := <Function>(param)

		// Assert
		// Verify properties and invariants
		if err != nil {
			// Verify error cases
		} else {
			// Verify success cases
		}
	})
}
```

## 7. References

- Go [Fuzzing](https://go.dev/security/fuzz/) documentation.
- Go [testing.F](https://pkg.go.dev/testing#F) package documentation.
