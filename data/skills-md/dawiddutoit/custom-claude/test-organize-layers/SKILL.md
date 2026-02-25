---
name: test-organize-layers
description: |
  Guide test placement in correct test pyramid layer (unit/integration/e2e).
  Use when creating new test files, deciding test layer, organizing test structure,
  or determining fixture scope. Analyzes mocking patterns, dependencies, and test scope
  to recommend correct layer placement. Works with pytest test files (test_*.py).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Organize Test Layers

## Purpose

Ensure new tests are placed in the correct test pyramid layer based on dependencies, mocking patterns, and scope. Prevents anti-patterns like unit tests with real databases or e2e tests with excessive mocking.

## When to Use

Use this skill when:
- **Creating new test files** - Determining correct test layer placement
- **Deciding test layer** - Choosing between unit, integration, or e2e
- **Organizing test structure** - Structuring test directories by layer
- **Determining fixture scope** - Deciding function vs session scope fixtures
- **Reviewing test architecture** - Validating tests are in correct layers
- **Refactoring tests** - Moving tests to appropriate layers

**Trigger phrases:**
- "Where should this test go?"
- "Should this be unit or integration test?"
- "Organize test structure"
- "Test layer placement"
- "Test pyramid organization"

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Test layer placement guidance
- [When to Use](#when-to-use) - Scenarios for using this skill
- [Quick Start](#quick-start) - Fast decision tree for test placement
- [Instructions](#instructions) - Step-by-step layer determination
  - [Step 1: Identify Test Dependencies](#step-1-identify-test-dependencies) - Analyze mocking patterns
  - [Step 2: Determine Fixture Scope](#step-2-determine-fixture-scope) - Match fixtures to layers
  - [Step 3: Choose Directory Structure](#step-3-choose-directory-structure) - Place files correctly
  - [Step 4: Apply Test Pyramid Guidelines](#step-4-apply-test-pyramid-guidelines) - Follow distribution
  - [Step 5: Validate Test Placement](#step-5-validate-test-placement) - Check for anti-patterns
- [Examples](#examples) - Working examples by layer
  - [Example 1: Unit Test for Service](#example-1-unit-test-for-service) - Pure logic testing
  - [Example 2: Integration Test for Repository](#example-2-integration-test-for-repository) - Real database
  - [Example 3: E2E Test for Search Workflow](#example-3-e2e-test-for-search-workflow) - Full stack
- [Requirements](#requirements) - pytest-asyncio, Clean Architecture knowledge
- [See Also](#see-also) - Related conftest files and skills

### Supporting Resources
- [references/reference.md](./references/reference.md) - Test pyramid theory and advanced patterns

### Utility Scripts
- [Analyze Test Pyramid](./scripts/analyze_test_pyramid.py) - Analyze test distribution and compare to ideal pyramid ratios
- [Move Test](./scripts/move_test.py) - Intelligently move tests between layers with automatic import updates
- [Validate Test Placement](./scripts/validate_test_placement.py) - Find misplaced tests and suggest corrections
- [Organize Tests](./scripts/organize_tests.py) - Master orchestration script for all test organization utilities

## Quick Start

**Creating a new test? Ask yourself:**
1. Do I mock ALL external dependencies? → **Unit test** (`tests/unit/`)
2. Do I use REAL infrastructure (DB/filesystem) but mock external APIs? → **Integration test** (`tests/integration/`)
3. Do I test the FULL stack end-to-end with real services? → **E2E test** (`tests/e2e/`)

## Instructions

### Step 1: Identify Test Dependencies

Analyze what the test needs to run:

- **Unit Tests**: Mock everything external (database, filesystem, network, time)
- **Integration Tests**: Real infrastructure (Neo4j, filesystem), mock external APIs (embeddings, LLMs)
- **E2E Tests**: Real everything, test complete workflows

**Pattern Recognition:**
```python
# Unit test pattern - Mock objects
from unittest.mock import AsyncMock, Mock
mock_db = Mock(spec=Neo4jDatabase)

# Integration test pattern - Real fixtures
async def test_with_real_db(neo4j_database: Neo4jDatabase):

# E2E test pattern - Full system
async def test_workflow(search_handler, indexed_real_codebase):
```

### Step 2: Determine Fixture Scope

Match fixture scope to test layer:

**Unit Test Fixtures** (function scope):
- `mock_config` - Mock Settings object
- `temp_dir` - Temporary directory
- `mock_neo4j_rag` - Mocked Neo4jRAG
- `mock_repository_monitor` - Mocked monitor

**Integration Test Fixtures** (function scope, real resources):
- `real_settings` - Settings from environment
- `neo4j_database` - Real Neo4jDatabase instance
- `neo4j_driver` - Real Neo4j driver
- `test_database` - Database name with cleanup

**E2E Test Fixtures** (session/function scope, full stack):
- `indexed_real_codebase` - Session-level codebase indexing
- `search_handler` - Real SearchCodeHandler
- `neo4j_driver` - Connected to indexed database

### Step 3: Choose Directory Structure

Place test files following Clean Architecture layers:

```
tests/
├── unit/                          # Mock everything
│   ├── conftest.py               # Unit test fixtures
│   ├── config/                   # Domain/config tests
│   ├── application/              # Application layer tests
│   │   ├── services/
│   │   ├── commands/
│   │   └── queries/
│   ├── infrastructure/           # Infrastructure tests (mocked)
│   └── core/                     # Core logic tests
├── integration/                   # Real infrastructure, mock external APIs
│   ├── conftest.py               # Integration fixtures
│   ├── neo4j/                    # Neo4j integration tests
│   ├── infrastructure/           # Real infrastructure tests
│   └── clean_architecture/       # Cross-layer integration
└── e2e/                          # Full stack
    ├── conftest.py               # E2E fixtures
    ├── semantic_search/          # Search E2E tests
    └── test_*.py                 # Workflow tests
```

### Step 4: Apply Test Pyramid Guidelines

Follow test distribution and characteristics:

**Unit Tests (70% of tests)**:
- Fast (<10ms per test)
- No external dependencies
- Test single responsibility
- Use `@pytest.mark.unit` marker

**Integration Tests (20% of tests)**:
- Medium speed (<500ms per test)
- Real infrastructure, mocked external services
- Test component interactions
- Use `@pytest.mark.integration` marker

**E2E Tests (10% of tests)**:
- Slow (1-10s per test)
- Full system integration
- Test user workflows
- Use `@pytest.mark.e2e` marker

### Step 5: Validate Test Placement

Check test placement against patterns:

**Red Flags (Wrong Layer)**:
- ❌ Unit test with `neo4j_database` fixture → Should be integration
- ❌ Integration test with all mocks → Should be unit
- ❌ E2E test testing single method → Should be unit
- ❌ Unit test with network calls → Should be integration or e2e

**Green Flags (Correct Layer)**:
- ✅ Unit test with `Mock(spec=ServiceClass)`
- ✅ Integration test with `real_settings` and `neo4j_database`
- ✅ E2E test with `search_handler` and `indexed_real_codebase`

## Examples

### Example 1: Unit Test for Service

**Scenario**: Testing ChunkingService logic without database

```python
# tests/unit/application/services/test_chunking_service.py
from unittest.mock import Mock
import pytest
from project_watch_mcp.application.services.chunking_service import ChunkingService

@pytest.mark.unit
async def test_chunk_size_calculation(mock_config):
    """Test chunk size calculation logic (pure function)."""
    service = ChunkingService(settings=mock_config)

    # Mock dependencies
    content = "def foo():\n    pass\n" * 100

    # Test logic without external dependencies
    chunks = service.calculate_chunks(content)

    assert len(chunks) > 0
    assert all(chunk.size <= mock_config.chunking.max_chunk_lines for chunk in chunks)
```

**Why Unit**: No database, no filesystem, tests pure logic.

### Example 2: Integration Test for Repository

**Scenario**: Testing Neo4jCodeRepository with real database

```python
# tests/integration/infrastructure/neo4j/test_code_repository.py
import pytest
from project_watch_mcp.infrastructure.neo4j.code_repository import Neo4jCodeRepository

@pytest.mark.integration
async def test_store_and_retrieve_chunk(neo4j_database, real_settings):
    """Test chunk persistence in real Neo4j database."""
    repository = Neo4jCodeRepository(neo4j_database.driver, real_settings)

    # Create test chunk
    chunk = Chunk(
        chunk_hash="test_hash",
        file_path="/test/file.py",
        content="test content",
        start_line=1,
        end_line=5
    )

    # Test with REAL database
    result = await repository.store_chunk(chunk)
    assert result.success

    # Verify persistence
    retrieved = await repository.get_chunk("test_hash")
    assert retrieved.data.content == "test content"
```

**Why Integration**: Uses real Neo4j database, tests actual persistence.

### Example 3: E2E Test for Search Workflow

**Scenario**: Testing complete semantic search workflow

```python
# tests/e2e/semantic_search/test_semantic_search_methods.py
import pytest

@pytest.mark.e2e
async def test_search_for_methods(search_handler, indexed_real_codebase):
    """Test searching for methods across real indexed codebase."""
    query = SearchCodeQuery(
        query_text="chunk validation",
        project_name="project-watch-mcp",
        search_type=SearchType.SEMANTIC,
        limit=10
    )

    # Execute REAL search with REAL embeddings and REAL database
    result = await search_handler.handle(query)

    assert result.success
    assert len(result.data) > 0

    # Verify result quality (LLM usability test)
    first_result = result.data[0]
    assert "file_path" in first_result
    assert "content" in first_result
    assert first_result["score"] > 0.5
```

**Why E2E**: Full stack (indexed codebase, real embeddings, real Neo4j, real search).

## Requirements

- pytest with pytest-asyncio installed
- Understand project's Clean Architecture layers
- Access to conftest.py files in each test layer
- Familiarity with fixture scopes (function, module, session)

## See Also

- [tests/unit/conftest.py](../../../tests/unit/conftest.py) - Unit test fixtures
- [tests/integration/conftest.py](../../../tests/integration/conftest.py) - Integration fixtures
- [tests/e2e/conftest.py](../../../tests/e2e/conftest.py) - E2E fixtures
- [references/reference.md](./references/reference.md) - Test pyramid theory and advanced patterns
