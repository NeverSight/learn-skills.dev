---
name: implement-dependency-injection
description: |
  Provides comprehensive guide for adding services to dependency injection Container using
  dependency-injector library patterns including Singleton vs Factory vs Dependency
  providers, override patterns for testing, and circular dependency detection. Use when
  creating new service, adding dependency to Container, debugging circular dependency
  errors, or wiring components for injection.
allowed-tools:
  - Read
  - Grep
  - Edit
  - MultiEdit
---

Works with container.py and container_factory.py files.
# Implement Dependency Injection

## Purpose
Guides proper integration of services into the dependency injection Container using the `dependency-injector` library. Ensures correct provider selection, prevents circular dependencies, and enables testability through override patterns.

## When to Use

Use this skill when:
- **Creating new service** - Adding a service that needs dependencies
- **Adding dependency to Container** - Wiring components for injection
- **Debugging circular dependency errors** - Resolving dependency cycles
- **Wiring components for injection** - Setting up proper dependency flow
- **Setting up test overrides** - Mocking dependencies in tests

**Trigger phrases:**
- "Add X to the dependency container"
- "Wire Y service with dependencies"
- "Fix circular dependency error"
- "Override dependency for testing"

## Quick Start
**Adding a simple service to Container:**
```python
# In container.py
my_service = providers.Singleton(
    MyService,
    settings=settings,
    dependency1=some_dependency,
)
```

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Single-sentence skill objective
- [Quick Start](#quick-start) - Immediate, copy-paste ready example
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Determine Provider Type](#step-1-determine-provider-type) - Singleton vs Factory vs Dependency
  - [Step 2: Add Service to Container](#step-2-add-service-to-container) - Container.py integration
  - [Step 3: Handle Special Cases](#step-3-handle-special-cases) - Factory functions, config extraction, circular dependencies
  - [Step 4: Override for Testing](#step-4-override-for-testing) - Test fixture patterns
  - [Step 5: Initialize in Factory](#step-5-initialize-in-factory) - MCP server initialization
- [Examples](#examples) - Concrete, working implementations
  - [Example 1: Add Repository (Singleton)](#example-1-add-repository-singleton)
  - [Example 2: Add Command Handler (Factory)](#example-2-add-command-handler-factory)
  - [Example 3: Override for Testing](#example-3-override-for-testing)
- [Requirements](#requirements) - Dependencies, files, quality checks
- [Common Pitfalls](#common-pitfalls) - Troubleshooting guide

### Supporting Resources
- [references/provider-reference.md](./references/provider-reference.md) - Complete dependency-injector API reference
- [references/circular-dependency-guide.md](./references/circular-dependency-guide.md) - Circular dependency resolution strategies
- [templates/service-template.py](./templates/service-template.py) - Service class template with DI

### Utility Scripts
- [Detect Circular Dependencies](./scripts/detect_circular_deps.py) - Detect circular dependencies in DI container
- [Generate Provider](./scripts/generate_provider.py) - Auto-generate provider code for container
- [Validate DI Patterns](./scripts/validate_di_patterns.py) - Validate dependency injection patterns in codebase

## Instructions

### Step 1: Determine Provider Type

Choose the appropriate provider based on lifecycle requirements:

**Use `providers.Singleton`:**
- Stateful services (repositories, caches)
- Expensive initialization (database connections, embedding models)
- Shared state needed across requests
- Most application/infrastructure services

**Use `providers.Factory`:**
- Request handlers (command/query handlers)
- Stateless operations
- New instance needed per invocation
- Short-lived objects

**Use `providers.Dependency`:**
- External dependencies provided at runtime
- Configuration objects (Settings)
- Infrastructure connections (neo4j_driver)
- Services from outside the container

### Step 2: Add Service to Container

**Location:** `/Users/dawiddutoit/projects/play/project-watch-mcp/src/project_watch_mcp/interfaces/mcp/container.py`

Add provider in the appropriate layer section:

```python
class Container(containers.DeclarativeContainer):
    # Configuration
    settings = providers.Dependency(instance_of=Settings)

    # Infrastructure Layer - Repositories
    my_repository = providers.Singleton(
        MyRepository,
        driver=neo4j_driver,
        settings=settings,
    )

    # Application Layer - Services
    my_service = providers.Singleton(
        MyService,
        settings=settings,
        repository=my_repository,
    )

    # Application Layer - Command Handlers
    my_handler = providers.Factory(
        MyHandler,
        service=my_service,
    )
```

**Ordering matters:** Define dependencies before dependents to avoid circular references.

### Step 3: Handle Special Cases

**Factory Functions (for complex initialization):**
```python
def create_extractor_registry(python_ext):
    """Factory function to create and configure extractor registry."""
    registry = ExtractorRegistry()
    registry.register(python_ext)
    return registry

extractor_registry = providers.Singleton(
    create_extractor_registry,
    python_ext=python_extractor,
)
```

**Extracting Config Values:**
```python
smart_chunking_service = providers.Singleton(
    SmartChunkingService,
    boundary_adjustment_lines=providers.Factory(
        lambda s: s.chunking.boundary_adjustment_lines,
        s=settings,
    ),
    settings=settings,
)
```

**Avoiding Circular Dependencies:**
- Order providers: dependencies before dependents
- Use lazy evaluation with `providers.Factory`
- Consider extracting shared dependencies to separate provider
- See `references/circular-dependency-guide.md` for resolution strategies

### Step 4: Override for Testing

**In test files (conftest.py or test methods):**
```python
@pytest.fixture
def container(real_settings, mock_driver):
    """Create container with test overrides."""
    container = Container()

    # Override dependencies
    container.settings.override(real_settings)
    container.neo4j_driver.override(mock_driver)

    return container

def test_service(container):
    """Test service from container."""
    service = container.my_service()
    assert service.settings is not None
```

### Step 5: Initialize in Factory

**For MCP server initialization:**

Update `/Users/dawiddutoit/projects/play/project-watch-mcp/src/project_watch_mcp/interfaces/mcp/container_factory.py`:

```python
def initialize_container_and_services(
    repository_monitor: RepositoryMonitor,
    neo4j_rag: Neo4jRAG,
    settings: Settings,
) -> Container:
    """Initialize container with runtime dependencies."""
    container = Container()

    # Override external dependencies
    container.settings.override(settings)
    container.neo4j_driver.override(neo4j_rag.neo4j_database.driver)
    container.repository_monitor.override(repository_monitor)

    # Initialize services with side effects
    _ = container.my_service()

    return container
```

## Examples

### Example 1: Add Repository (Singleton)
```python
# In container.py - Infrastructure Layer section

file_metadata_repository = providers.Singleton(
    FileMetadataRepository,
    driver=neo4j_driver,
    settings=settings,
)
```

**Why Singleton:** Repositories are stateful, manage connections, expensive to create.

### Example 2: Add Command Handler (Factory)
```python
# In container.py - Application Layer section

process_file_handler = providers.Factory(
    ProcessFileHandler,
    repository=file_metadata_repository,
    chunking_service=chunking_service,
    settings=settings,
)
```

**Why Factory:** Handlers are invoked per request, should be stateless.

### Example 3: Override for Testing
```python
# In tests/integration/mymodule/conftest.py

@pytest.fixture
def container(real_settings):
    container = Container()
    container.settings.override(real_settings)

    # Override with mock driver
    mock_driver = AsyncMock()
    container.neo4j_driver.override(mock_driver)

    return container

def test_handler_uses_repository(container):
    handler = container.process_file_handler()
    # handler now uses mocked driver through repository
```

## Requirements

### Dependencies
```bash
uv pip install dependency-injector
```

### Project Files
- Container definition: `src/project_watch_mcp/interfaces/mcp/container.py`
- Factory initialization: `src/project_watch_mcp/interfaces/mcp/container_factory.py`
- Test examples: `tests/integration/container/test_settings_injection.py`

### Quality Checks
After adding to container:
```bash
# Type checking (ensures proper wiring)
uv run pyright src/project_watch_mcp/interfaces/mcp/container.py

# Run tests
uv run pytest tests/integration/container/ -v
```

## Common Pitfalls

### 1. Circular Dependency Error
**Symptom:** `Error while resolving dependencies`

**Solution:** Reorder providers or use factory functions. See `references/circular-dependency-guide.md`.

### 2. Wrong Provider Type
**Symptom:** State leaking between tests or requests

**Solution:** Use Factory for handlers, Singleton for services/repositories.

### 3. Missing Override in Tests
**Symptom:** Tests fail with "Dependency not set"

**Solution:** Override all Dependency providers in test fixtures.

### 4. Optional Dependencies
**Symptom:** `def __init__(self, settings: Settings | None = None)`

**Solution:** NEVER make Settings/Config optional. Use `providers.Dependency(instance_of=Settings)` and override in tests.

## See Also
- [references/provider-reference.md](./references/provider-reference.md) - Complete dependency-injector API reference
- [references/circular-dependency-guide.md](./references/circular-dependency-guide.md) - Circular dependency resolution strategies
- [templates/service-template.py](./templates/service-template.py) - Service class template with DI
- [scripts/detect_circular_deps.py](./scripts/detect_circular_deps.py) - Detect circular dependencies utility
- [scripts/generate_provider.py](./scripts/generate_provider.py) - Generate provider code utility
- [scripts/validate_di_patterns.py](./scripts/validate_di_patterns.py) - Validate DI patterns utility
