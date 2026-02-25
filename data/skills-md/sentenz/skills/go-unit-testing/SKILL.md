---
name: go-unit-testing
description: Automates unit test creation for Go projects using the standard testing package with consistent software testing patterns including In-Got-Want, Table-Driven Testing, and AAA patterns. Use when creating, modifying, or reviewing unit tests, or when the user mentions unit tests, test coverage, or Go testing.
metadata:
  version: "1.0.0"
  activation:
    implicit: true
    priority: 1
    triggers:
      - "unit test"
      - "go test"
      - "testing"
      - "create test"
      - "add test"
      - "write test"
      - "test coverage"
    match:
      languages: ["go", "golang"]
      paths: ["pkg/**/*_test.go", "internal/**/*_test.go"]
      prompt_regex: "(?i)(unit test|go test|testing|create test|add test|write test|test coverage)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# Unit Testing

Instructions for AI coding agents on automating unit test creation using consistent software testing patterns in this Go project.

- [1. Benefits](#1-benefits)
- [2. Patterns](#2-patterns)
  - [2.1. In-Got-Want](#21-in-got-want)
  - [2.2. Table-Driven Testing](#22-table-driven-testing)
  - [2.3. Data-Driven Testing (DDT)](#23-data-driven-testing-ddt)
  - [2.4. Arrange, Act, Assert (AAA)](#24-arrange-act-assert-aaa)
  - [2.5. Test Fixtures](#25-test-fixtures)
- [3. Workflow](#3-workflow)
- [4. Commands](#4-commands)
- [5. Style Guide](#5-style-guide)
- [6. Template](#6-template)
  - [6.1. File Header Template](#61-file-header-template)
  - [6.2. Table-Driven Test Template](#62-table-driven-test-template)
  - [6.3. Test Fixture Template](#63-test-fixture-template)
  - [6.4. Error Test Template](#64-error-test-template)
  - [6.5. Boundary Value Test Template](#65-boundary-value-test-template)
  - [6.6. Data-Driven Test Template (JSON)](#66-data-driven-test-template-json)
- [7. References](#7-references)

## 1. Benefits

- Readability
  > Ensures high code quality and reliability. Tests are self-documenting, reducing cognitive load for reviewers and maintainers.

- Consistency
  > Uniform structure across tests ensures predictable, familiar code that team members can navigate efficiently.

- Scalability
  > Table-driven and data-driven approaches minimize boilerplate code when adding new test cases, making it simple to expand coverage.

- Debuggability
  > Scoped traces and detailed assertion messages pinpoint failures quickly during continuous integration and local testing.

## 2. Patterns

### 2.1. In-Got-Want

The In-Got-Want pattern structures each test case into three clear sections.

- In
  > Defines the input parameters or conditions for the test.

- Got
  > Captures the actual output or result produced by the code under test.

- Want
  > Specifies the expected output or result that the test is verifying against.

### 2.2. Table-Driven Testing

Table-driven testing organizes test cases in a tabular format, allowing multiple scenarios to be defined concisely.

- Test Case Structure
  > Each row in the table represents a distinct test case with its own set of inputs and expected outputs.

- Iteration
  > The test framework iterates over each row, executing the same test logic with different data.

### 2.3. Data-Driven Testing (DDT)

Data-driven testing separates test data from test logic, enabling the same test logic to be executed with multiple sets of input data.

- External Data Sources
  > Test data can be stored in external files (e.g., JSON, CSV) and loaded at runtime.

- Reusability
  > The same test logic can be reused with different datasets, enhancing maintainability and coverage.

### 2.4. Arrange, Act, Assert (AAA)

The AAA pattern structures each test case into three clear phases.

- Arrange
  > Set up the necessary preconditions and inputs for the test.

- Act
  > Execute the function or method being tested.

- Assert
  > Verify that the actual output matches the expected output.

### 2.5. Test Fixtures

Test fixtures provide a consistent and reusable setup and teardown mechanism for test cases.

- Setup
  > Initialize common objects or state needed for multiple tests.

- Teardown
  > Clean up resources or reset state after each test.

## 3. Workflow

1. Identify

    Identify new functions in `pkg/` or `internal/` (e.g., `pkg/<package>/<file>.go`).

2. Add/Create

    Create new tests in the same package (e.g., `pkg/<package>/<file>_test.go`).

3. Test Coverage Requirements

    Include comprehensive edge cases:
    - Coverage-guided cases
    - Boundary values (min/max limits, edge thresholds)
    - Empty/null inputs
    - Null pointers and invalid references
    - Overflow/underflow scenarios
    - Special cases (negative numbers, zero, special states)

4. Apply Templates

    Structure all tests using the [template](#6-template) pattern.

## 4. Commands

| Command                 | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `make go-test-unit`     | Execute tests with race detection and JUnit report |
| `make go-test-coverage` | Generate coverage reports (HTML and XML)           |

## 5. Style Guide

- Test Framework
  > Use the standard Go `testing` package.

- Include Imports
  > Include `testing` and `github.com/google/go-cmp/cmp` for comparisons.

- Parallelism
  > Use `t.Parallel()` to run tests in parallel.

- Test Organization
  > Consolidate test cases for a single function into **one `TestXxx(t *testing.T)` function** using table-driven testing.

  This approach:
  - Eliminates redundant test function definitions
  - Simplifies maintenance by grouping related scenarios together
  - Reduces code duplication in setup and teardown phases
  - Makes it easier to add or modify test cases

- Assertions
  > Use `cmp.Equal` for value comparisons and `errors.Is` for error checking.

## 6. Template

Use these templates for new unit tests. Replace placeholders with actual values.

### 6.1. File Header Template

```go
// SPDX-License-Identifier: Apache-2.0

package <package>

import (
	"errors"
	"testing"

	"github.com/google/go-cmp/cmp"
)
```

### 6.2. Table-Driven Test Template

```go
func Test<FunctionName>(t *testing.T) {
	t.Parallel()

	// In-Got-Want
	type in struct {
		/* input fields */
	}

	type want struct {
		/* expected output fields */
		err error
	}

	// Table-Driven Testing
	tests := []struct {
		name string
		in   in
		want want
	}{
		{
			name: "case-description-1",
			in: in{
				/* input values */
			},
			want: want{
				/* expected output */
				err: nil,
			},
		},
		{
			name: "case-description-2",
			in: in{
				/* input values */
			},
			want: want{
				/* expected output */
				err: nil, // or specific error
			},
		},
		// add more cases as needed
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange
			// additional setup as needed

			// Act
			got, err := <Function>(tt.in.<input>)

			// Assert
			if !errors.Is(err, tt.want.err) {
				t.Errorf("<Function>() error = %v, want err %v", err, tt.want.err)
			}
			if !cmp.Equal(got, tt.want.<value>) {
				t.Errorf("<Function>(%+v) = %v, want %v", tt.in, got, tt.want.<value>)
			}
		})
	}
}
```

### 6.3. Test Fixture Template

```go
// testFixture holds common test state and provides setup/teardown.
type testFixture struct {
	t      *testing.T
	// Add common fields for test state
	object *<Type>
}

// newTestFixture creates and initializes a test fixture.
func newTestFixture(t *testing.T) *testFixture {
	t.Helper()

	// Setup
	return &testFixture{
		t:      t,
		object: New<Type>(),
	}
}

// teardown cleans up resources after test completion.
func (f *testFixture) teardown() {
	f.t.Helper()

	// Teardown
	if f.object != nil {
		f.object.Close()
	}
}

func Test<FunctionName>WithFixture(t *testing.T) {
	t.Parallel()

	// Arrange
	f := newTestFixture(t)
	defer f.teardown()

	input := <input_value>

	// Act
	got, err := f.object.<Function>(input)

	// Assert
	if err != nil {
		t.Errorf("<Function>() unexpected error: %v", err)
	}
	if !cmp.Equal(got, <expected>) {
		t.Errorf("<Function>() = %v, want %v", got, <expected>)
	}
}
```

### 6.4. Error Test Template

```go
func Test<FunctionName>Error(t *testing.T) {
	t.Parallel()

	// In-Got-Want
	type in struct {
		/* invalid input fields */
	}

	type want struct {
		err error
	}

	// Table-Driven Testing
	tests := []struct {
		name string
		in   in
		want want
	}{
		{
			name: "nil-input-returns-error",
			in: in{
				/* nil or invalid input */
			},
			want: want{
				err: resource.Err<ErrorName>,
			},
		},
		{
			name: "invalid-value-returns-error",
			in: in{
				/* invalid value */
			},
			want: want{
				err: resource.Err<ErrorName>,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange
			// setup if needed

			// Act
			_, err := <Function>(tt.in.<input>)

			// Assert
			if !errors.Is(err, tt.want.err) {
				t.Errorf("<Function>() error = %v, want err %v", err, tt.want.err)
			}
		})
	}
}
```

### 6.5. Boundary Value Test Template

```go
func Test<FunctionName>BoundaryValues(t *testing.T) {
	t.Parallel()

	// In-Got-Want
	type in struct {
		input <input_type>
	}

	type want struct {
		value <output_type>
		err   error
	}

	// Table-Driven Testing
	tests := []struct {
		name string
		in   in
		want want
	}{
		{
			name: "minimum-value",
			in:   in{input: <MIN_VALUE>},
			want: want{value: /* expected */, err: nil},
		},
		{
			name: "maximum-value",
			in:   in{input: <MAX_VALUE>},
			want: want{value: /* expected */, err: nil},
		},
		{
			name: "zero-value",
			in:   in{input: 0},
			want: want{value: /* expected */, err: nil},
		},
		{
			name: "negative-value",
			in:   in{input: -1},
			want: want{value: /* expected */, err: nil},
		},
		{
			name: "overflow-value",
			in:   in{input: math.MaxFloat64},
			want: want{value: 0, err: resource.ErrOverflow},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange
			// setup if needed

			// Act
			got, err := <Function>(tt.in.input)

			// Assert
			if !errors.Is(err, tt.want.err) {
				t.Errorf("<Function>() error = %v, want err %v", err, tt.want.err)
			}
			if !cmp.Equal(got, tt.want.value) {
				t.Errorf("<Function>(%v) = %v, want %v", tt.in.input, got, tt.want.value)
			}
		})
	}
}
```

### 6.6. Data-Driven Test Template (JSON)

```go
import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/google/go-cmp/cmp"
)

// testCase represents a single test case loaded from JSON.
type testCase struct {
	Name string `json:"name"`
	In   struct {
		Input <input_type> `json:"input"`
	} `json:"in"`
	Want struct {
		Expected <output_type> `json:"expected"`
	} `json:"want"`
}

// testData represents the JSON test data structure.
type testData struct {
	Tests []testCase `json:"tests"`
}

func Test<FunctionName>DataDriven(t *testing.T) {
	t.Parallel()

	// Load test data from JSON file
	testdataPath := filepath.Join("testdata", "<function>_test.json")
	data, err := os.ReadFile(testdataPath)
	if err != nil {
		t.Fatalf("failed to read test data: %v", err)
	}

	var td testData
	if err := json.Unmarshal(data, &td); err != nil {
		t.Fatalf("failed to parse test data: %v", err)
	}

	for _, tc := range td.Tests {
		t.Run(tc.Name, func(t *testing.T) {
			// Arrange
			input := tc.In.Input
			expected := tc.Want.Expected

			// Act
			got, err := <Function>(input)

			// Assert
			if err != nil {
				t.Errorf("<Function>() unexpected error: %v", err)
			}
			if !cmp.Equal(got, expected) {
				t.Errorf("<Function>(%v) = %v, want %v", input, got, expected)
			}
		})
	}
}
```

- `tests/data/<function>_test.json`
  > JSON file containing test cases.

  ```json
  {
    "tests": [
      {
        "name": "case-description-1",
        "in": {
          "input": <value>
        },
        "want": {
          "expected": <value>
        }
      },
      {
        "name": "case-description-2",
        "in": {
          "input": <value>
        },
        "want": {
          "expected": <value>
        }
      }
    ]
  }
  ```

## 7. References

- Go [Testing](https://pkg.go.dev/testing) package documentation.
- Google [go-cmp](https://github.com/google/go-cmp) package documentation.
