---
name: test-effort-estimator
description: This skill should be used when users need to estimate test effort based on product requirements. It analyzes requirements, breaks down tasks, estimates test effort (case design, first run, retest, regression), and exports results to Excel.
---

# Test Effort Estimator

## Purpose

This skill provides a systematic approach to estimate test effort based on product requirements. It analyzes requirements, breaks them down into testable items, estimates effort for each phase (case design, first run, retest, regression), and generates an Excel report.

## When to Use

Use this skill when users provide product requirements and need:
- Test effort estimation for new features
- Resource planning for testing phases
- Detailed breakdown of testing activities
- Excel export of effort estimates

## How to Use

### Step 1: Analyze Requirements

Read and understand the provided product requirements. Identify:
- Functional modules and features
- User stories and test scenarios
- Complexity levels of different features

### Step 2: Break Down Test Items

For each requirement, identify test items:
- Test entry points and navigation
- Data display and validation
- User interactions and workflows
- System operations and state changes

### Step 3: Estimate Effort

Apply complexity-based estimation standards:

**Simple Features** (0.20-0.30 person-days for design):
- Single function, clear logic
- Few operation steps, simple data preparation
- Examples: list display, simple navigation

**Medium Features** (0.35-0.40 person-days for design):
- Multiple sub-functions, moderate complexity
- Requires test data preparation
- Examples: data filtering, user management

**Complex Features** (0.50 person-days for design):
- Complex business logic, multiple interaction paths
- Requires diverse test data, strong dependencies
- Examples: online/offline binding, batch operations

**Time Calculation Formulas:**

- **Case Design**: Simple 0.20-0.30, Medium 0.35-0.40, Complex 0.50
- **First Run**: Simple 0.15-0.20, Medium 0.25-0.30, Complex 0.30-0.40
- **Retest**: 33%-67% of first run, round to 0.10 minimum
- **Regression**: 48%-67% of first run, round to two decimals

### Step 4: Generate Excel Report

Use the bundled script `scripts/generate_excel.py` to create the Excel report with:
- Requirement title
- Requirement story/description
- Case design time
- First run time
- Retest time
- Regression time
- Estimation rationale

## Constraints

- All time values must be >= 0.10 person-days
- All time values must be rounded to two decimals
- Total estimation error should be within 0.5 person-days of actual values
- Minimum unit is 0.01 person-days

## Bundled Resources

### Scripts

- `scripts/generate_excel.py`: Python script to generate Excel report from estimation data

### References

- `references/complexity-standards.md`: Detailed complexity classification criteria and examples
- `references/estimation-formulas.md`: Complete formula documentation and calculation examples

## Workflow

1. Load complexity standards from `references/complexity-standards.md`
2. Analyze requirements and identify test items
3. Apply estimation formulas based on complexity
4. Execute `scripts/generate_excel.py` to generate Excel report
5. Review and validate total estimates against constraints
