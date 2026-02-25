---
name: test-implement-constructor-validation
description: |
  Auto-generate constructor validation tests from service class signatures.
  Use when creating tests for new services, validating fail-fast principle,
  ensuring constructor validation, or testing required parameters. Analyzes
  service __init__ methods and generates pytest.raises(ValueError) tests
  for each required parameter. Works with Python service classes following
  dependency injection pattern. High automation opportunity (100+ test classes
  use this pattern).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
---

# Implement Constructor Validation Tests

## Purpose

Automatically generate comprehensive constructor validation tests for service classes that follow the fail-fast principle. This skill ensures every required parameter has a corresponding test that validates the service raises `ValueError` when that parameter is `None`.

## When to Use

Use this skill when:
- **Creating tests for new services** - Generating constructor validation tests automatically
- **Validating fail-fast principle** - Ensuring services validate required parameters
- **Testing constructor validation** - Verifying services raise ValueError for None parameters
- **Testing required parameters** - Validating each required parameter has proper validation
- **Following TDD workflow** - Creating tests before or alongside service implementation
- **Automating test generation** - Reducing manual boilerplate for repetitive test patterns

**Trigger phrases:**
- "Generate constructor validation tests"
- "Test service constructor"
- "Validate fail-fast principle"
- "Test required parameters"
- "Create constructor tests"

## Quick Start

Simplest usage - generate tests for a new service:

```bash
# 1. Identify the service class you need tests for
# 2. Locate or create the test file
# 3. Invoke this skill with the service file path and test file path
```

The skill will:
- Extract constructor signature from service class
- Identify all required parameters
- Generate one test method per required parameter
- Include proper fixtures, type ignores, and error message assertions

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Automated constructor validation test generation
- [Instructions](#instructions) - Step-by-step test generation process
  - [Step 1: Analyze Service Constructor](#step-1-analyze-service-constructor) - Extract parameters and validation logic
  - [Step 2: Identify Required Test Fixtures](#step-2-identify-required-test-fixtures) - Mock fixture patterns
  - [Step 3: Generate Test Class Structure](#step-3-generate-test-class-structure) - Test class template
  - [Step 4: Handle Type Ignore Comments](#step-4-handle-type-ignore-comments) - Suppress pyright errors
  - [Step 5: Validate Error Messages](#step-5-validate-error-messages) - Assert specific error messages
  - [Step 6: Organize Test Methods](#step-6-organize-test-methods) - Method ordering and fixture exclusion
- [Examples](#examples) - Working implementations
  - [Example 1: Simple Service (2 Parameters)](#example-1-simple-service-2-parameters) - ChunkingService pattern
  - [Example 2: Complex Service (5 Parameters)](#example-2-complex-service-5-parameters) - IndexingOrchestrator pattern

### Supporting Resources
- [templates/test-template.py](./templates/test-template.py) - Copy-paste ready template
- [references/reference.md](./references/reference.md) - Pattern analysis and edge cases

### Utility Scripts
- [Find Missing Validation Tests](./scripts/find_missing_validation.py) - Identify services lacking constructor validation tests
- [Generate Constructor Tests](./scripts/generate_constructor_tests.py) - Auto-generate pytest test classes from service signatures
- [Validate Test Coverage](./scripts/validate_constructor_tests.py) - Verify all constructor parameters have corresponding tests

### Advanced Topics
- [Requirements](#requirements) - Python 3.11+, pytest, fail-fast validation pattern
- [Automation Strategy](#automation-strategy) - Future script for full automation
- [See Also](#see-also) - Related documentation

## Instructions

### Step 1: Analyze Service Constructor

Read the service class to extract:
- Class name (for test naming)
- Constructor parameters and their types
- Validation error messages (from `if not X: raise ValueError("...")` blocks)
- Dependencies that need mocking

**Example Pattern to Look For:**
```python
def __init__(
    self,
    settings: Settings,
    indexing_module: IndexingModule,
    extractor_registry: ExtractorRegistry,
):
    if not settings:
        raise ValueError("Settings is required for IndexingOrchestrator")
    if not indexing_module:
        raise ValueError("IndexingModule is required for IndexingOrchestrator")
    # ... more validations
```

### Step 2: Identify Required Test Fixtures

For each constructor parameter:
- Determine if it needs a mock fixture (services, repositories)
- Identify the spec type for mocking
- Check if the service has async methods (use AsyncMock)

**Fixture Naming Pattern:** `mock_{parameter_name}`

### Step 3: Generate Test Class Structure

Create a dedicated test class for constructor validation:

```python
class Test{ServiceName}Constructor:
    """Test {ServiceName} constructor and initialization."""

    # Fixtures for each dependency
    @pytest.fixture
    def mock_settings(self):
        """Create mock Settings."""
        return MagicMock(spec=Settings)

    # ... more fixtures

    # Success case test
    def test_constructor_initializes_with_valid_dependencies(self, ...):
        """Test that constructor properly initializes with all valid dependencies."""
        # Arrange + Act
        instance = ServiceName(...)

        # Assert
        assert instance.settings is mock_settings
        # ... assert all dependencies

    # Validation tests (one per parameter)
    def test_constructor_fails_when_{param}_is_none(self, ...):
        """Test that constructor raises ValueError when {Param} is None."""
        with pytest.raises(ValueError) as exc_info:
            ServiceName(
                param=None,  # type: ignore
                # ... other valid params
            )

        assert "{Param} is required for {ServiceName}" in str(exc_info.value)
```

### Step 4: Handle Type Ignore Comments

For each `None` parameter in validation tests:
- Add `# type: ignore` comment on same line
- This suppresses pyright errors for intentionally wrong types
- Required because we're testing failure cases

**Pattern:**
```python
ServiceName(
    settings=None,  # type: ignore
    other_param=mock_other_param,
)
```

### Step 5: Validate Error Messages

Each validation test must assert the specific error message:

```python
assert "{ParamType} is required for {ServiceName}" in str(exc_info.value)
```

**Error Message Pattern from Constructor:**
```python
if not settings:
    raise ValueError("Settings is required for IndexingOrchestrator")
```

### Step 6: Organize Test Methods

**Method Ordering:**
1. Success case (all valid parameters)
2. Validation failures (one per parameter, in parameter order)

**Fixture Exclusion Pattern:**
Each validation test excludes the fixture for the parameter being tested:

```python
def test_constructor_fails_when_settings_is_none(
    self,
    # mock_settings EXCLUDED - this is what we're testing
    mock_indexing_module,
    mock_extractor_registry,
):
```

## Examples

### Example 1: Simple Service (2 Parameters)

**Service Constructor:**
```python
class ChunkingService:
    def __init__(self, settings: Settings, tokenizer: Tokenizer):
        if not settings:
            raise ValueError("Settings is required for ChunkingService")
        if not tokenizer:
            raise ValueError("Tokenizer is required for ChunkingService")

        self.settings = settings
        self.tokenizer = tokenizer
```

**Generated Tests:**
```python
class TestChunkingServiceConstructor:
    """Test ChunkingService constructor and initialization."""

    @pytest.fixture
    def mock_settings(self):
        """Create mock Settings."""
        return MagicMock(spec=Settings)

    @pytest.fixture
    def mock_tokenizer(self):
        """Create mock Tokenizer."""
        return MagicMock(spec=Tokenizer)

    def test_constructor_initializes_with_valid_dependencies(
        self, mock_settings, mock_tokenizer
    ):
        """Test that constructor properly initializes with all valid dependencies."""
        service = ChunkingService(
            settings=mock_settings,
            tokenizer=mock_tokenizer,
        )

        assert service.settings is mock_settings
        assert service.tokenizer is mock_tokenizer

    def test_constructor_fails_when_settings_is_none(self, mock_tokenizer):
        """Test that constructor raises ValueError when Settings is None."""
        with pytest.raises(ValueError) as exc_info:
            ChunkingService(
                settings=None,  # type: ignore
                tokenizer=mock_tokenizer,
            )

        assert "Settings is required for ChunkingService" in str(exc_info.value)

    def test_constructor_fails_when_tokenizer_is_none(self, mock_settings):
        """Test that constructor raises ValueError when Tokenizer is None."""
        with pytest.raises(ValueError) as exc_info:
            ChunkingService(
                settings=mock_settings,
                tokenizer=None,  # type: ignore
            )

        assert "Tokenizer is required for ChunkingService" in str(exc_info.value)
```

### Example 2: Complex Service (5 Parameters)

For a complex service with 5 parameters, follow the same pattern as Example 1 above. Create a test class with fixtures for each parameter, a success case test, and one validation failure test for each required parameter. See [references/reference.md](./references/reference.md) for detailed pattern analysis and edge cases.

## Requirements

- Python 3.11+
- pytest installed: `uv pip install pytest`
- unittest.mock (standard library)
- Service class must follow fail-fast validation pattern
- Service must have `if not param: raise ValueError(...)` blocks

## Automation Strategy

This skill is a **prime candidate for full automation** because:

1. **Highly Repetitive Pattern** - 100+ test classes use identical structure
2. **Deterministic Generation** - Output is fully determined by input (constructor signature)
3. **Clear Rules** - No subjective decisions required
4. **Type Safety** - Can validate against service class signature
5. **Error Message Consistency** - Standard format: `"{Type} is required for {Service}"`

**Future Enhancement:** Create a script that:
- Accepts service file path as input
- Parses AST to extract constructor signature
- Generates complete test class with all fixtures and validation tests
- Runs pyright to validate generated tests
- Writes to appropriate test file location

## See Also

- [templates/test-template.py](./templates/test-template.py) - Copy-paste template
- [references/reference.md](./references/reference.md) - Pattern analysis and edge cases
- [CLAUDE.md](../../../../CLAUDE.md) - Fail-fast principle documentation
