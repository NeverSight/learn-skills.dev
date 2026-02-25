---
name: test-implement-factory-fixtures
description: |
  Create factory fixture patterns for customizable test setup with variations.
  Use when building reusable test fixtures with multiple configurations, creating
  parameterizable mocks, or implementing test data builders. Works with pytest
  fixtures, mock objects, and test utilities. Enables DRY test setup while
  maintaining flexibility for edge cases.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# Implement Factory Fixtures

## Purpose

Factory fixtures are pytest fixtures that return callable functions, enabling dynamic test setup with customizable parameters. This pattern eliminates test duplication while maintaining flexibility for edge cases and variations.

## Quick Start

```python
# Create a factory fixture
@pytest.fixture
def mock_service_factory():
    def create_service(dimensions=384, success=True):
        service = AsyncMock()
        service.generate = AsyncMock(return_value=[0.1] * dimensions)
        return service
    return create_service

# Use in tests
def test_with_custom_dimensions(mock_service_factory):
    service = mock_service_factory(dimensions=1536)
    result = service.generate()
    assert len(result) == 1536
```

## Table of Contents

### Core Sections

- [When to Use Factory Fixtures](#step-1-identify-the-need-for-factory-fixtures)
  - Multiple test variations needed
  - Parameterization insufficient
  - Edge cases require customization
  - Real objects with mock dependencies

- [Factory Design Patterns](#step-2-design-the-factory-function)
  - Standard factory fixture structure
  - Outer fixture, inner function, default values
  - Proper documentation and type hints

- [Common Factory Patterns](#step-3-implement-common-factory-patterns)
  - [Pattern A: Mock Service Factory](#pattern-a-mock-service-factory) - Services with success/failure modes, varying return types
  - [Pattern B: Settings Factory](#pattern-b-settings-factory) - Configuration objects with many attributes
  - [Pattern C: Real Instance Factory](#pattern-c-real-instance-factory) - Real objects with mock dependencies
  - [Pattern D: Result/Data Factory](#pattern-d-resultdata-factory) - ServiceResult mocks, query results, response objects

- [Organization and Usage](#step-4-organize-factory-fixtures)
  - File organization patterns
  - Naming conventions
  - Using factories in tests

### Examples

- [Example 1: Embedding Service Factory](#example-1-embedding-service-factory-from-project)
  - Custom dimensions (384, 1536)
  - Success/failure modes
  - Error message handling

- [Example 2: Settings Factory with Kwargs](#example-2-settings-factory-with-kwargs-from-project)
  - Hierarchical settings structure
  - Flexible kwargs overrides
  - Default value management

- [Example 3: Real Instance Factory](#example-3-real-instance-factory-with-mock-dependencies)
  - Real business logic with mocked dependencies
  - Combining multiple factories
  - Custom configuration testing

### Decision Guidance

- [Factory vs Parametrize](#factory-vs-parametrize-when-to-choose)
  - When to use factory fixtures
  - When to use pytest.mark.parametrize
  - Comparison examples

### Common Pitfalls

- [Pitfall 1: Over-Parameterization](#pitfall-1-over-parameterization) - Too many parameters, use kwargs instead
- [Pitfall 2: Missing Defaults](#pitfall-2-missing-defaults) - Force every test to specify everything
- [Pitfall 3: Stateful Factories](#pitfall-3-stateful-factories) - State leaks between tests
- [Pitfall 4: Not Using Type Hints](#pitfall-4-not-using-type-hints) - Unclear return types

### Supporting Resources

- [Requirements](#requirements)
- [See Also](#see-also) - Project examples, related skills, pytest documentation

### Python Examples
- [Convert Fixture to Factory](./scripts/convert_fixture_to_factory.py) - Convert existing pytest fixtures to factory pattern
- [Generate Factory Fixture](./scripts/generate_factory_fixture.py) - Auto-generate factory fixtures from class definitions
- [Validate Fixtures](./scripts/validate_fixtures.py) - Analyze fixtures and suggest factory pattern conversions

## Instructions

### Step 1: Identify the Need for Factory Fixtures

Factory fixtures are ideal when:
- **Multiple test variations needed**: Same mock with different configurations
- **Parameterization insufficient**: pytest.mark.parametrize doesn't capture all variations
- **Edge cases require customization**: Success/failure modes, different data shapes
- **Real objects with mock dependencies**: Creating real instances with injected mocks

**Example Scenarios:**
- Mock service returning different dimension embeddings (384, 1536, etc.)
- Settings objects with various configuration combinations
- Real service instances with mocked dependencies
- Query results with different data structures

### Step 2: Design the Factory Function

Factory fixtures have three components:

1. **Outer fixture**: Declares dependencies and returns factory function
2. **Inner factory function**: Accepts parameters and creates instances
3. **Default values**: Sensible defaults for common cases

**Standard Pattern:**
```python
@pytest.fixture
def mock_thing_factory():
    """Create a factory for custom mock things.

    Returns:
        callable: Function that creates things with custom parameters

    Example:
        def test_something(mock_thing_factory):
            thing = mock_thing_factory(param1=value1, param2=value2)
            # Use thing in test
    """
    def create_thing(param1=default1, param2=default2):
        """Create custom mock thing.

        Args:
            param1: Description (default: default1)
            param2: Description (default: default2)

        Returns:
            Type: Custom thing instance
        """
        # Implementation
        return thing

    return create_thing
```

### Step 3: Implement Common Factory Patterns

#### Pattern A: Mock Service Factory

For mocks with varying behavior:

```python
@pytest.fixture
def mock_embedding_service_factory():
    def create_service(dimensions=384, success=True, error_message=None):
        service = AsyncMock()

        if success:
            service.generate_embeddings = AsyncMock(
                return_value=MagicMock(
                    success=True,
                    data=[[0.1] * dimensions],
                )
            )
        else:
            service.generate_embeddings = AsyncMock(
                return_value=MagicMock(
                    success=False,
                    error=error_message or "Embedding service error"
                )
            )

        return service

    return create_service
```

**Use for**: Services with success/failure modes, varying return types, different dimensions.

#### Pattern B: Settings Factory

For configuration objects with many attributes:

```python
@pytest.fixture
def mock_settings_factory():
    def create_settings(**kwargs):
        settings = MagicMock()

        # Set default structure
        settings.project = MagicMock()
        settings.neo4j = MagicMock()
        settings.chunking = MagicMock()

        # Apply defaults with kwargs overrides
        settings.project.project_name = kwargs.get("project_name", "test_project")
        settings.chunking.chunk_size = kwargs.get("chunk_size", 50)
        settings.neo4j.database_name = kwargs.get("database_name", "test_db")

        return settings

    return create_settings
```

**Use for**: Complex configuration objects, hierarchical settings, many attributes.

#### Pattern C: Real Instance Factory

For creating real objects with mock dependencies:

```python
@pytest.fixture
def mock_indexing_module_factory(
    mock_neo4j_driver,
    mock_embedding_service_factory,
    mock_settings_factory
):
    def create_module(**kwargs):
        from project_watch_mcp.infrastructure.neo4j.graphrag.indexing import IndexingModule

        settings = mock_settings_factory(**kwargs)
        embedder = mock_embedding_service_factory(
            dimensions=kwargs.get("embedding_dimensions", 384)
        )

        return IndexingModule(
            settings=settings,
            db=mock_neo4j_driver,
            embedder=embedder,
            project_name=kwargs.get("project_name", "test_project"),
            database=kwargs.get("database", "test_db"),
        )

    return create_module
```

**Use for**: Testing real business logic with controlled dependencies.

#### Pattern D: Result/Data Factory

For creating test data structures:

```python
@pytest.fixture
def mock_service_result():
    def create_result(success=True, data=None, error=None):
        result = MagicMock()
        result.is_success = success
        result.is_failure = not success

        if success:
            result.data = data
            result.unwrap = MagicMock(return_value=data)
            result.error = None
        else:
            result.data = None
            result.error = error or "Operation failed"
            result.unwrap = MagicMock(side_effect=ValueError(result.error))

        return result

    return create_result
```

**Use for**: ServiceResult mocks, query results, response objects.

### Step 4: Organize Factory Fixtures

**File Organization:**
```
tests/utils/
├── mock_services.py      # Service-layer factories
├── mock_settings.py      # Configuration factories
├── mock_drivers.py       # Infrastructure factories
└── __init__.py           # Exports (if needed)
```

**Naming Convention:**
- `mock_{thing}_factory` for mock factories
- `mock_real_{thing}_factory` for real instances with mocks
- Clear docstrings with usage examples

### Step 5: Use Factory Fixtures in Tests

**Basic Usage:**
```python
def test_with_custom_dimensions(mock_embedding_service_factory):
    service = mock_embedding_service_factory(dimensions=1536)
    result = await service.generate_embeddings(["text"])
    assert len(result.data[0]) == 1536
```

**Testing Failure Cases:**
```python
def test_handles_service_error(mock_embedding_service_factory):
    service = mock_embedding_service_factory(
        success=False,
        error_message="API rate limit"
    )
    result = await service.generate_embeddings(["text"])
    assert result.is_failure
    assert "rate limit" in result.error
```

**Combining Factories:**
```python
def test_indexing_with_custom_settings(
    mock_indexing_module_factory,
    mock_settings_factory
):
    module = mock_indexing_module_factory(
        chunk_size=100,
        project_name="custom_project",
        embedding_dimensions=1536
    )
    # Test with custom configuration
```

## Examples

### Example 1: Embedding Service Factory (From Project)

**Location:** `tests/utils/mock_services.py`

```python
@pytest.fixture
def mock_embedding_service_factory():
    """Create a factory for custom mock embedding services.

    Returns:
        callable: Function that creates embedding services with custom dimensions

    Example:
        def test_something(mock_embedding_service_factory):
            service = mock_embedding_service_factory(dimensions=1536)
            # Use service in test
    """
    def create_service(dimensions=384, success=True, error_message=None):
        """Create custom mock embedding service.

        Args:
            dimensions: Number of dimensions for embeddings
            success: Whether the service should return success
            error_message: Error message for failure cases

        Returns:
            AsyncMock: Custom embedding service
        """
        service = AsyncMock()

        if success:
            service.generate_embeddings = AsyncMock(
                return_value=MagicMock(
                    success=True,
                    data=[[0.1] * dimensions],
                )
            )
            service.get_embeddings = AsyncMock(return_value=[[0.1] * dimensions])
            service.get_embedding = AsyncMock(return_value=[0.1] * dimensions)
        else:
            service.generate_embeddings = AsyncMock(
                return_value=MagicMock(
                    success=False, error=error_message or "Embedding service error"
                )
            )
            service.get_embeddings = AsyncMock(side_effect=Exception(error_message or "Error"))
            service.get_embedding = AsyncMock(side_effect=Exception(error_message or "Error"))

        return service

    return create_service
```

**Usage in Tests:**
```python
def test_with_384_dimensions(mock_embedding_service_factory):
    service = mock_embedding_service_factory(dimensions=384)
    result = await service.generate_embeddings(["text"])
    assert len(result.data[0]) == 384

def test_with_1536_dimensions(mock_embedding_service_factory):
    service = mock_embedding_service_factory(dimensions=1536)
    result = await service.generate_embeddings(["text"])
    assert len(result.data[0]) == 1536

def test_service_failure(mock_embedding_service_factory):
    service = mock_embedding_service_factory(
        success=False,
        error_message="Rate limit exceeded"
    )
    result = await service.generate_embeddings(["text"])
    assert not result.success
    assert "Rate limit" in result.error
```

### Example 2: Settings Factory with Kwargs (From Project)

**Location:** `tests/utils/mock_settings.py`

```python
@pytest.fixture
def mock_settings_factory():
    """Create a factory for custom mock settings.

    Returns:
        callable: Function that creates settings with custom attributes

    Example:
        def test_something(mock_settings_factory):
            settings = mock_settings_factory(
                project_name="custom_project",
                chunk_size=100,
                database_name="custom_db"
            )
            # Use settings in test
    """
    def create_settings(**kwargs):
        """Create custom mock settings with specified attributes.

        Args:
            **kwargs: Attributes to set on the settings object.
                     Use dot notation for nested attributes.

        Returns:
            MagicMock: Custom settings object
        """
        settings = MagicMock()

        # Set default structure
        settings.project = MagicMock()
        settings.neo4j = MagicMock()
        settings.chunking = MagicMock()
        settings.indexing = MagicMock()

        # Apply defaults
        settings.project.project_name = kwargs.get("project_name", "test_project")
        settings.project.repository_path = Path(kwargs.get("repository_path", "/test/repo"))

        settings.neo4j.database_name = kwargs.get("database_name", "test_db")
        settings.neo4j.uri = kwargs.get("neo4j_uri", "bolt://192.168.68.122:7687")

        settings.chunking.chunk_size = kwargs.get("chunk_size", 50)
        settings.chunking.chunk_overlap = kwargs.get("chunk_overlap", 5)

        settings.indexing.batch_size = kwargs.get("batch_size", 100)
        settings.indexing.max_workers = kwargs.get("max_workers", 4)

        return settings

    return create_settings
```

**Usage in Tests:**
```python
def test_with_custom_chunk_size(mock_settings_factory):
    settings = mock_settings_factory(chunk_size=100)
    assert settings.chunking.chunk_size == 100

def test_with_multiple_overrides(mock_settings_factory):
    settings = mock_settings_factory(
        project_name="my_project",
        chunk_size=200,
        batch_size=50,
        database_name="prod_db"
    )
    assert settings.project.project_name == "my_project"
    assert settings.chunking.chunk_size == 200
    assert settings.indexing.batch_size == 50
    assert settings.neo4j.database_name == "prod_db"
```

### Example 3: Real Instance Factory with Mock Dependencies

**Location:** `tests/utils/mock_services.py`

```python
@pytest.fixture
def mock_indexing_module_factory(
    mock_neo4j_driver,
    mock_embedding_service_factory,
    mock_settings_factory
):
    """Create a factory for real IndexingModule instances with custom settings.

    Args:
        mock_neo4j_driver: Mock Neo4j driver fixture
        mock_embedding_service_factory: Mock embedding service factory
        mock_settings_factory: Mock settings factory

    Returns:
        callable: Function that creates IndexingModule instances

    Example:
        def test_something(mock_indexing_module_factory):
            module = mock_indexing_module_factory(
                chunk_size=100,
                project_name="custom_project"
            )
            # Use module in test
    """
    def create_module(**kwargs):
        """Create IndexingModule with custom settings.

        Args:
            **kwargs: Settings to override

        Returns:
            IndexingModule: Real IndexingModule instance with mocks
        """
        from project_watch_mcp.infrastructure.neo4j.graphrag.indexing import IndexingModule

        settings = mock_settings_factory(**kwargs)
        embedder = mock_embedding_service_factory(
            dimensions=kwargs.get("embedding_dimensions", 384)
        )

        return IndexingModule(
            settings=settings,
            db=mock_neo4j_driver,
            embedder=embedder,
            project_name=kwargs.get("project_name", "test_project"),
            database=kwargs.get("database", "test_db"),
        )

    return create_module
```

**Usage in Tests:**
```python
def test_indexing_with_large_chunks(mock_indexing_module_factory):
    module = mock_indexing_module_factory(chunk_size=500)
    # Test real IndexingModule logic with large chunks

def test_indexing_with_custom_embeddings(mock_indexing_module_factory):
    module = mock_indexing_module_factory(
        embedding_dimensions=1536,
        project_name="ml_project"
    )
    # Test with different embedding dimensions
```

## Requirements

- pytest (installed via project dependencies)
- unittest.mock (Python standard library)
- Understanding of pytest fixture scope
- Familiarity with closure patterns in Python

**Installation:**
```bash
# Already included in project dependencies
uv pip install -e .
```

## Factory vs Parametrize: When to Choose

### Use Factory Fixtures When:
- ✅ Need multiple parameters with complex interactions
- ✅ Creating real instances with mock dependencies
- ✅ Success/failure modes require different mock setups
- ✅ Edge cases need special configuration
- ✅ Same fixture used across multiple test files

### Use pytest.mark.parametrize When:
- ✅ Testing same code with different input values
- ✅ Simple parameter variations (1-3 parameters)
- ✅ All test cases follow same pattern
- ✅ Parameters are independent

**Example Comparison:**

```python
# ❌ WRONG: Parametrize for complex factory-like needs
@pytest.mark.parametrize("dimensions,success,error", [
    (384, True, None),
    (1536, True, None),
    (384, False, "Error"),
])
def test_embedding_service(dimensions, success, error):
    # Complex mock setup repeated in test
    service = create_complex_mock(dimensions, success, error)
    # ...

# ✅ CORRECT: Factory fixture for complex setup
def test_embedding_service_384(mock_embedding_service_factory):
    service = mock_embedding_service_factory(dimensions=384)
    # ...

def test_embedding_service_failure(mock_embedding_service_factory):
    service = mock_embedding_service_factory(success=False, error="Error")
    # ...
```

## Common Pitfalls

### Pitfall 1: Over-Parameterization

**❌ WRONG: Too many parameters**
```python
def create_service(
    param1, param2, param3, param4, param5,
    param6, param7, param8, param9, param10
):
    # Too complex!
```

**✅ CORRECT: Use kwargs or multiple factories**
```python
def create_service(**kwargs):
    # Flexible and readable
```

### Pitfall 2: Missing Defaults

**❌ WRONG: All parameters required**
```python
def create_service(dimensions, success, error_message):
    # Forces every test to specify everything
```

**✅ CORRECT: Sensible defaults**
```python
def create_service(dimensions=384, success=True, error_message=None):
    # Common case works with no args
```

### Pitfall 3: Stateful Factories

**❌ WRONG: Factory maintains state**
```python
@pytest.fixture
def mock_service_factory():
    call_count = 0  # Shared across calls!
    def create_service():
        nonlocal call_count
        call_count += 1
        # State leaks between tests
```

**✅ CORRECT: Stateless factory**
```python
@pytest.fixture
def mock_service_factory():
    def create_service(call_count=0):  # Pass as parameter
        service = AsyncMock()
        service.call_count = call_count
        return service
    return create_service
```

### Pitfall 4: Not Using Type Hints

**❌ WRONG: No type hints**
```python
def create_service(dimensions=384):
    # What type is returned?
```

**✅ CORRECT: Clear return types**
```python
def create_service(dimensions: int = 384) -> AsyncMock:
    """Create custom mock embedding service.

    Args:
        dimensions: Number of dimensions for embeddings

    Returns:
        AsyncMock: Custom embedding service
    """
```

## See Also

- **Project Examples:**
  - `/Users/dawiddutoit/projects/play/project-watch-mcp/tests/utils/mock_services.py`
  - `/Users/dawiddutoit/projects/play/project-watch-mcp/tests/utils/mock_settings.py`
  - `/Users/dawiddutoit/projects/play/project-watch-mcp/tests/utils/mock_drivers.py`

- **Related Skills:**
  - `debug-test-failures` - Debugging factory fixture issues
  - `run-quality-gates` - Validating tests using factories

- **Pytest Documentation:**
  - Fixture factories: https://docs.pytest.org/en/stable/how-to/fixtures.html#factories-as-fixtures
  - Fixture scopes: https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
