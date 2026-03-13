---
name: go-api-documentation
description: Automates API documentation creation for Go projects using godoc conventions and best practices. Use when creating, modifying, or reviewing documentation comments, or when the user mentions godoc, documentation, or API docs.
metadata:
  version: "1.1.1"
  activation:
    implicit: true
    priority: 2
    triggers:
      - "godoc"
      - "documentation"
      - "API docs"
      - "API documentation"
      - "package doc"
      - "document function"
      - "package documentation"
    match:
      languages: ["go", "golang"]
      paths: ["pkg/**/*.go", "internal/**/*.go"]
      prompt_regex: "(?i)(godoc|documentation|API docs|API documentation|doc comments|package documentation)"
  usage:
    load_on_prompt: true
    autodispatch: true
---

# API Documentation

Instructions for AI coding agents on adding godoc-compatible documentation comments to Go source files.

> [!NOTE]
> This skill is for documenting Go packages, types, functions, and methods following Go documentation conventions.

- [1. Benefits](#1-benefits)
- [2. Principles](#2-principles)
- [3. Patterns](#3-patterns)
  - [3.1. Package Documentation](#31-package-documentation)
  - [3.2. Function Documentation](#32-function-documentation)
  - [3.3. Type Documentation](#33-type-documentation)
  - [3.4. Method Documentation](#34-method-documentation)
  - [3.5. Constant and Variable Documentation](#35-constant-and-variable-documentation)
  - [3.6. Examples](#36-examples)
  - [3.7. Formula Documentation](#37-formula-documentation)
- [4. Workflow](#4-workflow)
- [5. Commands](#5-commands)
- [6. Style Guide](#6-style-guide)
- [7. Templates](#7-templates)
  - [7.1. Package Template](#71-package-template)
  - [7.2. Type Template](#72-type-template)
  - [7.3. Function Template](#73-function-template)
  - [7.4. Method Template](#74-method-template)
  - [7.5. Constant/Variable Template](#75-constantvariable-template)
  - [7.6. Example Template](#76-example-template)
  - [7.7. Formula Template](#77-formula-template)
- [8. References](#8-references)

## 1. Benefits

- Discoverability
  > Well-documented APIs enable developers to quickly understand and use packages without reading implementation details.

- Maintainability
  > Documentation embedded in source code stays synchronized with implementation, reducing drift between code and documentation.

- Tooling Integration
  > Documentation comments are automatically extracted by `go doc` and displayed in IDEs, editors, and pkg.go.dev.

- Standards Compliance
  > Following Go documentation conventions ensures consistency across the Go ecosystem.

## 2. Principles

Effective API documentation follows these core principles aligned with Go conventions.

- Complete
  > Document all exported identifiers (packages, types, functions, methods, constants, and variables). Unexported identifiers may have documentation for internal clarity.

- Contextual
  > Documentation provides context about usage patterns, performance characteristics, and concurrency safety.

- Consistent
  > Use a uniform style and format throughout following Go documentation conventions defined in this skill.

- Concise
  > Use clear, brief descriptions. The first sentence should be a complete sentence that starts with the name being documented.

- Concrete
  > Provide specific details about behavior, edge cases, and error conditions rather than vague statements.

- Accurate
  > Documentation must match the actual behavior. Update documentation whenever the implementation changes.

- Actionable
  > Include usage examples, preconditions, postconditions, and error handling to help developers use the API correctly.

## 3. Patterns

### 3.1. Package Documentation

Package documentation appears in a comment immediately before the package clause or in a separate `doc.go` file.

- Format
  > Package documentation starts with `Package <name>` followed by a description.

- Content
  > Describes the package's purpose, main concepts, and typical usage patterns.

- Location
  > Can be in any file in the package (typically the main file) or in a dedicated `doc.go` file.

### 3.2. Function Documentation

Function documentation describes what the function does and its contract.

- Format
  > Starts with the function name followed by a description.

- Parameters
  > Parameters are described in the main description when needed, not as separate annotations.

- Return Values
  > Return values are described in the main description, including error conditions.

- Errors
  > Document what errors can be returned and under what conditions.

- Panics
  > Document any conditions that cause the function to panic.

### 3.3. Type Documentation

Type documentation describes the purpose and usage of a type (structs, interfaces, aliases).

- Format
  > Starts with the type name followed by a description.

- Content
  > Explains what the type represents, its responsibilities, and any invariants.

- Related Types
  > May reference related types and their relationships.

### 3.4. Method Documentation

Method documentation is similar to function documentation.

- Format
  > Starts with the method name followed by a description.

- Receiver
  > The receiver type is mentioned when relevant to understanding the method.

- Context
  > Describes how the method relates to the type's overall functionality.

### 3.5. Constant and Variable Documentation

Constants and variables are documented with their purpose and usage.

- Format
  > Starts with the identifier name followed by a description.

- Grouped Declarations
  > Groups of related constants/variables can share a single comment before the group.

### 3.6. Examples

Examples demonstrate typical usage patterns.

- Format
  > Example functions follow the naming convention `Example`, `Example_suffix`, or `ExampleType_Method`.

- Output
  > Examples can include `// Output:` comments to specify expected output for testing.

- Documentation
  > Examples appear in godoc as executable code samples.

- Completeness
  > Examples should be self-contained and runnable.

### 3.7. Formula Documentation

Mathematical formulas and equations for algorithms and technical documentation.

> [!NOTE]
> Go's godoc does not natively support LaTeX or MathML rendering. Use text-based representations, Unicode symbols, and preformatted blocks for mathematical expressions.

- Text Descriptions
  > Describe formulas using clear mathematical language (e.g., "the square root of the sum of squares").

- Unicode Symbols
  > Use Unicode mathematical symbols for common operations (×, ÷, ≤, ≥, √, ∑, π, Δ, etc.).

- ASCII Representations
  > Use ASCII art for simple formulas (e.g., `(a + b) / c`, `sqrt(x^2 + y^2)`).

- Preformatted Blocks
  > Use indented text for multi-line formulas and equations to preserve formatting.

- Variable Notation
  > Clearly define variables and their meanings before presenting formulas.

- Examples
  > Include concrete numerical examples to illustrate formula application.

- External References
  > Link to external resources (Wikipedia, MathWorld) for complex mathematical concepts.

## 4. Workflow

1. Identify

    Identify exported functions, types, constants, and variables in `pkg/` or `internal/` that need documentation.

2. Review Existing

    Check if documentation exists and if it needs updating or improvement.

3. Add Documentation

    Add or update documentation comments following the templates and style guide.

4. Verify Format

    Ensure comments follow Go conventions:
    - Start with the identifier name
    - Form complete sentences
    - Use proper punctuation
    - Are placed immediately before the declaration

5. Validate

    Run `go doc <package>` or `go doc <package>.<identifier>` to verify documentation renders correctly.

6. Apply Templates

    Structure all documentation using the [template](#7-templates) patterns.

## 5. Commands

| Command                        | Description                                    |
| ------------------------------ | ---------------------------------------------- |
| `go doc ./pkg/percent`         | View package documentation                     |
| `go doc ./pkg/percent.Percent` | View function documentation                    |
| `go doc -all ./pkg/percent`    | View all documentation including unexported    |
| `godoc -http=:6060`            | Start local documentation server               |
| `pkgsite -http=:8080`          | Start pkgsite server for pkg.go.dev style docs |

## 6. Style Guide

- License Header
  > All source files must include `// SPDX-License-Identifier: Apache-2.0` at the top.

- Comment Style
  > Use `//` comment style, not `/* */` for documentation comments.

- First Sentence
  > The first sentence should be a complete, standalone summary that starts with the name being documented.

- Capitalization
  > Start with the identifier name (capitalized as it appears in code), then continue with normal sentence capitalization.

- Punctuation
  > Use proper punctuation. End sentences with periods.

- Present Tense
  > Use present tense to describe what the code does (e.g., `Percent calculates` not `Percent will calculate`).

- Blank Lines
  > No blank lines within a documentation comment block.

- Positioning
  > Place the comment immediately before the declaration with no blank line in between.

- Code References
  > Reference other identifiers without special markup (godoc will automatically link them).

- Links
  > Use URLs directly in documentation; godoc will render them as links.

- Formatting
  > Indented text is displayed as preformatted (code blocks).

- Paragraphs
  > Separate paragraphs with blank comment lines (lines containing only `//`).

- Lists
  > Use simple text lists; no special markup is needed.

- No Redundancy
  > Avoid repeating the function signature in the documentation.

## 7. Templates

Use these templates for documenting Go code. Replace placeholders with actual values.

### 7.1. Package Template

Use this template for package documentation. Place in the main package file or in `doc.go`.

```go
// SPDX-License-Identifier: Apache-2.0

// Package <name> provides <brief description of package purpose>.
//
// <Extended description of what the package does, main concepts,
// and typical usage patterns.>
//
// Example usage:
//
// <code example showing typical usage>
//
// <Additional notes about concurrency, performance, or other important
// considerations.>
package <name>
```

### 7.2. Type Template

Use this template for documenting types (structs, interfaces, type aliases).

```go
// <TypeName> <describes what the type represents and its purpose>.
//
// <Extended description of responsibilities, invariants, and usage patterns.
// Include information about thread safety, lifecycle, or other important
// characteristics.>
//
// Example:
//
// <code example showing typical usage of the type>
type <TypeName> struct {
 // <FieldName> <describes the field's purpose>
 <FieldName> <type>
}
```

### 7.3. Function Template

Use this template for documenting functions.

```go
// <FunctionName> <describes what the function does>.
//
// <Extended description including parameter meanings, return value
// descriptions, and any error conditions.>
//
// The function <describes behavior, preconditions, postconditions>.
//
// Returns <description of return value(s)>. If an error occurs,
// it returns <description of error conditions>.
//
// Example:
//
// <code example showing typical usage>
func <FunctionName>(<params>) (<returns>) {
 // implementation
}
```

### 7.4. Method Template

Use this template for documenting methods.

```go
// <MethodName> <describes what the method does>.
//
// <Extended description including how it relates to the receiver type,
// parameter meanings, return value descriptions, and any error conditions.>
//
// The method <describes behavior, preconditions, postconditions>.
//
// Returns <description of return value(s)>. If an error occurs,
// it returns <description of error conditions>.
func (r <ReceiverType>) <MethodName>(<params>) (<returns>) {
 // implementation
}
```

### 7.5. Constant/Variable Template

Use this template for documenting constants and variables.

```go
// <IdentifierName> <describes the constant/variable and its purpose>.
const <IdentifierName> = <value>

// <GroupDescription> describes this group of related constants.
const (
 // <ConstName1> <describes this specific constant>
 <ConstName1> = <value1>

 // <ConstName2> <describes this specific constant>
 <ConstName2> = <value2>
)
```

### 7.6. Example Template

Use this template for creating example functions.

```go
// Example demonstrates basic usage of <name>.
func Example() {
 // Setup
 <setup code>
 
 // Usage
 <example usage code>
 
 // Output:
 // <expected output>
}

// Example<Type>_<method> demonstrates usage of <Type>.<method>.
func Example<Type>_<method>() {
 // Example implementation
 <example code>
 
 // Output:
 // <expected output>
}
```

### 7.7. Formula Template

Use this template for documenting functions with mathematical formulas.

```go
// <FunctionName> <describes what the function calculates>.
//
// The calculation follows the formula:
//
//	<formula in ASCII or indented text>
//
// Where:
//   - <var1> is <description>
//   - <var2> is <description>
//   - <result> is <description>
//
// For example, with <var1> = <value1> and <var2> = <value2>:
//
//	<result> = <calculated_example>
//
// The function returns <description of return value>.
// If an error occurs, it returns <description of error conditions>.
func <FunctionName>(<params>) (<returns>) {
 // implementation
}
```

**Example with percentage calculation:**

```go
// Percent calculates the percentage of a value.
//
// The calculation follows the formula:
//
//	result = value × (percent / 100)
//
// Where:
//   - value is the base amount
//   - percent is the percentage in range [0, 100]
//   - result is the calculated percentage of the value
//
// For example, 25% of 200:
//
//	result = 200 × (25 / 100) = 50
//
// The function returns the calculated result as float64.
// Returns an error if percent is outside the range [0, 100].
func Percent[T constraints.Integer | constraints.Float](percent, value T) (float64, error) {
 // implementation
}
```

**Example with Unicode symbols:**

```go
// Distance calculates the Euclidean distance between two points.
//
// The calculation follows the formula:
//
//	d = √((x₂ - x₁)² + (y₂ - y₁)²)
//
// Where:
//   - (x₁, y₁) is the first point
//   - (x₂, y₂) is the second point
//   - d is the distance (d ≥ 0)
//
// For example, distance between (0, 0) and (3, 4):
//
//	d = √((3 - 0)² + (4 - 0)²) = √(9 + 16) = √25 = 5
//
// The function returns the distance as a non-negative float64.
func Distance(x1, y1, x2, y2 float64) float64 {
 // implementation
}
```

**Example with preformatted multi-line formula:**

```go
// Change calculates the percentage change between two values.
//
// The calculation follows the formula:
//
//	         (newValue - oldValue)
//	change = ───────────────────── × 100
//	              |oldValue|
//
// Where:
//   - oldValue is the original value
//   - newValue is the new value
//   - change is the percentage change (positive for increase, negative for decrease)
//
// For example, change from 50 to 75:
//
//	change = (75 - 50) / |50| × 100 = 50%
//
// The function returns the percentage change as float64.
// Returns an error if oldValue is zero (division by zero).
func Change[T constraints.Integer | constraints.Float](oldValue, newValue T) (float64, error) {
 // implementation
}
```

## 8. References

- Go [Documentation Comments](https://go.dev/doc/comment) specification.
- Go [Effective Go - Commentary](https://go.dev/doc/effective_go#commentary) guide.
- Go [Godoc](https://go.dev/blog/godoc) documentation.
- Go [Godoc](https://pkg.go.dev/golang.org/x/tools/cmd/godoc) tool documentation.
- Go [Go Code Review](https://github.com/golang/go/wiki/CodeReviewComments#doc-comments) comments.
