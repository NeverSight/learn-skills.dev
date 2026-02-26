---
name: skill-testing-framework
description: Provides test cases and validation tools for skills. Use when creating tests for a new skill, adding regression tests after skill updates, running test suites to verify skill functionality, or validating that skill outputs match expected results. Supports unit tests, integration tests, and regression tests with input/output pair validation.
---

# Skill Testing Framework

## Overview

This skill provides a comprehensive framework for testing skills at multiple levels: unit tests for individual components, integration tests for complete workflows, and regression tests to catch breaking changes. It includes scripts for generating test templates, running test suites, and validating outputs against baselines.

## When to Use This Skill

Use this skill when:
- Building a new skill and want to add tests from the start
- Updating an existing skill and need to verify it still works correctly
- Running regression tests to ensure changes don't break existing functionality
- Validating that skill outputs match expected results
- Creating a test suite for a skill

## Quick Start

### 1. Generate a Test Template

Start by generating a test template for your skill:

```bash
scripts/generate_test_template.py /path/to/your-skill --output your-skill-tests.json
```

This analyzes your skill structure and creates a template with unit, integration, and regression test sections.

### 2. Customize the Test Cases

Edit the generated test file to add specific test cases. Use `assets/test_template.json` as a reference for test case structure.

### 3. Run Tests

Execute the test suite:

```bash
scripts/run_tests.py your-skill-tests.json --skill-path /path/to/your-skill
```

Add `--verbose` flag for detailed output.

## Test Types

### Unit Tests

Test individual components in isolation (scripts, functions, modules).

**Example:**
```json
{
  "name": "Test PDF rotation script",
  "type": "script",
  "script": "rotate_pdf.py",
  "args": ["input.pdf", "output.pdf", "90"],
  "expected_exit_code": 0,
  "description": "Verify PDF rotation executes without errors"
}
```

### Integration Tests

Test complete workflows from start to finish.

**Example:**
```json
{
  "name": "Test document creation workflow",
  "type": "workflow",
  "description": "End-to-end test of document generation",
  "input": {
    "user_query": "Create a report with sections and formatting",
    "files": []
  },
  "expected_output": {
    "type": "docx",
    "validation": "Contains title, sections, and proper formatting"
  }
}
```

### Regression Tests

Compare outputs against known baselines to catch unintended changes.

**Example:**
```json
{
  "name": "Regression: Output format consistency",
  "description": "Ensure output format hasn't changed",
  "input": {
    "user_query": "Process sample data",
    "files": ["sample.csv"]
  },
  "baseline_file": "baselines/sample_output_v1.txt",
  "validation_method": "exact_match"
}
```

## Creating Test Cases

### Input/Output Pair Format

Test cases use input/output pairs to define expected behavior:

**Input:**
- User query or prompt that triggers the skill
- Input files or data
- Configuration parameters

**Expected Output:**
- Exit code (for scripts)
- Output content or patterns
- File existence and properties
- Validation criteria

### Validation Methods

Choose the appropriate validation method:

1. **exact_match** - Output must match exactly (for deterministic outputs)
2. **contains** - Output must contain specific content (for error messages)
3. **pattern** - Output must match regex pattern (for formatted data with variable values)
4. **structural_match** - Structure must match (for documents with dynamic content)

## Managing Baselines

### Creating Baselines

For regression tests, create baseline files from known good outputs:

```bash
# Run skill and capture output
./skill-script.py input.txt > output.txt

# Create baseline from output
scripts/validate_test_results.py --create-baseline output.txt baselines/
```

### Validating Against Baselines

Compare current output with baseline:

```bash
scripts/validate_test_results.py actual.txt baseline.txt --mode exact
```

### Updating Baselines

When skill behavior intentionally changes:
1. Review the changes carefully
2. Verify the changes are correct and intended
3. Update the baseline file
4. Document why the baseline changed (update notes in test case)

**Important:** Don't automatically update baselines when tests fail. Investigate first to ensure it's not a regression.

## Test Organization

Organize test files and data using this structure:

```
tests/
├── your-skill-tests.json          # Main test suite
├── fixtures/                      # Test input files
│   ├── sample_input.pdf
│   ├── test_data.csv
│   └── edge_case_data.txt
├── baselines/                     # Expected outputs for regression tests
│   ├── baseline_v1.txt
│   └── baseline_v2.json
└── outputs/                       # Actual test outputs (gitignored)
    └── test_run_*.txt
```

## Workflow Decision Tree

**Am I building a new skill?**
→ Generate test template → Customize tests → Run tests

**Am I updating an existing skill?**
→ Run existing tests → Add new test cases for new functionality → Update baselines if needed

**Am I debugging a failing test?**
→ Run with --verbose → Compare outputs using validate_test_results.py → Fix issue or update test

**Do I want to add regression tests?**
→ Capture current output as baseline → Create regression test case → Document what the baseline represents

## Available Scripts

### generate_test_template.py

Creates test case templates based on skill structure.

```bash
# Basic usage
generate_test_template.py /path/to/skill

# Specify output file
generate_test_template.py /path/to/skill --output my-tests.json

# YAML format
generate_test_template.py /path/to/skill --format yaml
```

### run_tests.py

Executes test suites and reports results.

```bash
# Run all tests
run_tests.py test-suite.json

# Run with skill path
run_tests.py test-suite.json --skill-path /mnt/skills/public/pdf

# Verbose output
run_tests.py test-suite.json --verbose
```

**Output:**
- Passes: ✅ Test name
- Failures: ❌ Test name with diff
- Summary: Total, passed, failed, success rate

### validate_test_results.py

Validates outputs against expected results and manages baselines.

```bash
# Compare two files (exact match)
validate_test_results.py actual.txt expected.txt

# Check if output contains string
validate_test_results.py output.txt expected.txt --mode contains

# Pattern matching
validate_test_results.py output.txt pattern.txt --mode pattern

# Create baseline
validate_test_results.py --create-baseline output.txt baselines/
```

## Best Practices

1. **Start with happy path tests** - Verify basic functionality first
2. **Add edge case tests** - Test boundary conditions and unusual inputs
3. **Test error handling** - Verify graceful failures with clear messages
4. **Use descriptive test names** - Names should explain what's being tested
5. **Document baselines** - Note what each baseline represents and when it was created
6. **Keep tests independent** - Tests shouldn't depend on each other
7. **Make tests maintainable** - Use fixtures and organize test data
8. **Review failures carefully** - Don't blindly update baselines

## Reference Documentation

For detailed guidance, see:

**references/test_patterns.md** - Examples of test cases for different skill types:
- Script-based skills (PDF manipulation, image processing)
- Document creation skills (DOCX, PPTX, XLSX)
- API integration skills
- Workflow-based skills
- Reference documentation skills

**references/writing_tests.md** - Best practices for effective testing:
- Test design principles
- Coverage strategy
- Test data management
- Writing test cases
- Debugging failed tests

## Example Test Suite

See `assets/test_template.json` for a complete example test suite with:
- Unit test examples
- Integration test examples
- Regression test examples
- Validation method examples
- Instructions and documentation
