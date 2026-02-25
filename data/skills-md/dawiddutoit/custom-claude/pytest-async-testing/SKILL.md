---
name: pytest-async-testing
description: |
  Provides Complete patterns for testing async Python code with pytest: pytest-asyncio configuration, AsyncMock usage, async fixtures, testing FastAPI with AsyncClient, testing Kafka async producers/consumers, event loop and cleanup patterns.

  Use when: Testing async functions, async use cases, FastAPI endpoints, async database operations, Kafka async clients, or any async/await code patterns.
allowed-tools: Read, Bash, Write
---

# Pytest Async Testing

## Purpose

Async testing requires special handling of event loops, context managers, and async fixtures. This skill provides production-ready patterns for testing all async scenarios in modern Python.

## Quick Start

Configure pytest for auto-detection of async tests:

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # Auto-detect async tests
asyncio_default_fixture_loop_scope = "function"  # Max isolation per test
```

Then write async tests naturally:

```python
@pytest.mark.asyncio
async def test_async_function() -> None:
    """Async test with full type safety."""
    result = await fetch_data()
    assert result is not None

# With pytest-asyncio auto-mode, @pytest.mark.asyncio is optional:
async def test_auto_detected() -> None:
    """Async test without decorator."""
    result = await fetch_data()
    assert result is not None
```

## Instructions

### Step 1: Configure pytest-asyncio in pyproject.toml

```toml
[tool.pytest.ini_options]
# Auto-detect async tests (don't require @pytest.mark.asyncio)
asyncio_mode = "auto"

# Function scope: New event loop per test (maximum isolation)
asyncio_default_fixture_loop_scope = "function"

# Alternative scopes for performance:
# asyncio_default_fixture_loop_scope = "module"  # Shared per module
# asyncio_default_fixture_loop_scope = "session"  # Single for all tests
```

### Step 2: Create Async Fixtures

```python
from typing import AsyncGenerator
import pytest

# ✅ GOOD: Async fixture with proper type hints
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide async HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
        # Cleanup happens after yield

# ✅ GOOD: Async database session
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide async database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.rollback()  # Cleanup
```

### Step 3: Use AsyncMock for Mocking Async Methods

```python
from unittest.mock import AsyncMock

# ✅ GOOD: AsyncMock for single async method
@pytest.fixture
def mock_gateway() -> AsyncMock:
    """Mock async gateway."""
    mock = AsyncMock()
    mock.fetch_orders.return_value = [order1, order2]
    mock.close.return_value = None
    return mock

# ✅ GOOD: AsyncMock for async generator
@pytest.fixture
def mock_async_generator() -> AsyncMock:
    """Mock async generator."""
    mock = AsyncMock()

    async def fake_generator():
        yield item1
        yield item2
        yield item3

    mock.stream.return_value = fake_generator()
    return mock
```

### Step 4: Test Async Use Cases

```python
@pytest.mark.asyncio
async def test_extract_orders_use_case(
    mock_gateway: AsyncMock,
    mock_publisher: AsyncMock,
) -> None:
    """Test async use case with async mocks."""
    use_case = ExtractOrdersUseCase(
        gateway=mock_gateway,
        publisher=mock_publisher
    )

    result = await use_case.execute()

    assert result.orders_count == 2
    # Verify async methods were awaited
    mock_gateway.fetch_orders.assert_awaited_once()
    assert mock_publisher.publish_order.await_count == 2
```

### Step 5: Test FastAPI Endpoints with AsyncClient

```python
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for FastAPI testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_endpoint(test_client: AsyncClient) -> None:
    """Test FastAPI GET endpoint."""
    response = await test_client.get("/top-products?count=10")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10

@pytest.mark.asyncio
async def test_post_endpoint(test_client: AsyncClient) -> None:
    """Test FastAPI POST endpoint."""
    payload = {"name": "Test", "price": 99.99}
    response = await test_client.post("/products", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
```

### Step 6: Test Async Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_transaction():
    """Async context manager for transactions."""
    session = Session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

@pytest.mark.asyncio
async def test_transaction_success() -> None:
    """Test successful transaction."""
    async with database_transaction() as session:
        await session.execute("INSERT INTO orders VALUES (1, 'test')")

    # Verify commit was called

@pytest.mark.asyncio
async def test_transaction_rollback() -> None:
    """Test transaction rollback on error."""
    with pytest.raises(ValueError):
        async with database_transaction() as session:
            await session.execute("INSERT INTO orders VALUES (1, 'test')")
            raise ValueError("Simulated error")

    # Verify rollback was called
```

### Step 7: Test Async Generators

```python
from typing import AsyncIterator

async def fetch_orders_stream() -> AsyncIterator[dict]:
    """Async generator yielding orders."""
    for i in range(10):
        yield {"id": str(i), "total": 100.0 * i}

@pytest.mark.asyncio
async def test_async_generator() -> None:
    """Test async generator consumption."""
    orders = []

    async for order in fetch_orders_stream():
        orders.append(order)

    assert len(orders) == 10
    assert orders[0]["id"] == "0"
    assert orders[9]["total"] == 900.0

@pytest.mark.asyncio
async def test_async_generator_with_early_termination() -> None:
    """Test breaking out of async generator."""
    orders = []

    async for order in fetch_orders_stream():
        orders.append(order)
        if len(orders) >= 5:
            break

    assert len(orders) == 5
```

### Step 8: Test Kafka Async Clients

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_kafka_producer() -> AsyncMock:
    """Mock confluent-kafka async producer."""
    mock = AsyncMock()
    mock.produce.return_value = None
    mock.flush.return_value = 0  # All delivered
    mock.close.return_value = None
    return mock

@pytest.fixture
def mock_kafka_consumer() -> AsyncMock:
    """Mock Kafka consumer with async iteration."""
    mock = AsyncMock()

    async def fake_consume():
        yield {"key": "order_1", "value": {"id": "1"}}
        yield {"key": "order_2", "value": {"id": "2"}}

    mock.consume.return_value = fake_consume()
    return mock

@pytest.mark.asyncio
async def test_kafka_producer_integration(
    mock_kafka_producer: AsyncMock
) -> None:
    """Test async Kafka producer."""
    producer = KafkaProducerAdapter(mock_kafka_producer)

    await producer.publish("test_topic", "key", {"data": "value"})

    mock_kafka_producer.produce.assert_called_once()
    mock_kafka_producer.flush.assert_called_once()

@pytest.mark.asyncio
async def test_kafka_consumer_integration(
    mock_kafka_consumer: AsyncMock
) -> None:
    """Test async Kafka consumer."""
    consumer = KafkaConsumerAdapter(mock_kafka_consumer)

    messages = []
    async for message in consumer.consume():
        messages.append(message)

    assert len(messages) == 2
```

### Step 9: Handle Event Loop Cleanup

```python
import asyncio

@pytest.fixture
async def cleanup_tasks():
    """Ensure all async tasks are cleaned up."""
    yield

    # Cancel any pending tasks
    pending = asyncio.all_tasks()
    for task in pending:
        task.cancel()

    # Wait for cancellation to complete
    await asyncio.gather(*pending, return_exceptions=True)
```

### Step 10: Test with Timeouts for Long-Running Async Operations

```python
import pytest

@pytest.mark.asyncio
@pytest.mark.timeout(5)  # 5-second timeout
async def test_fetch_with_timeout() -> None:
    """Test that long-running operation completes in time."""
    result = await fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_with_asyncio_wait_for() -> None:
    """Test with asyncio.wait_for for timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(long_running_op(), timeout=0.1)
```

## Examples

### Example 1: Complete FastAPI Test

```python
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
import pytest

from app.reporting.infrastructure.fastapi_app import app

@pytest.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for FastAPI testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_query_use_case(monkeypatch: Any) -> AsyncMock:
    """Mock use case dependency in FastAPI."""
    mock = AsyncMock()

    from app.reporting.infrastructure import dependencies
    monkeypatch.setattr(
        dependencies,
        "get_query_use_case",
        lambda: mock
    )

    return mock

class TestTopProductsEndpoint:
    """Test reporting API endpoint."""

    @pytest.mark.asyncio
    async def test_get_top_products_success(
        self,
        test_client: AsyncClient,
        mock_query_use_case: AsyncMock,
    ) -> None:
        """Test successful response."""
        mock_query_use_case.execute.return_value = [
            ProductRanking(title="Laptop", rank=Rank(1), cnt_bought=100),
            ProductRanking(title="Mouse", rank=Rank(2), cnt_bought=50),
        ]

        response = await test_client.get("/top-products?count=10")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_top_products_unavailable(
        self,
        test_client: AsyncClient,
        mock_query_use_case: AsyncMock,
    ) -> None:
        """Test 503 when data not available."""
        from app.reporting.application.exceptions import DataNotAvailableException

        mock_query_use_case.execute.side_effect = DataNotAvailableException(
            "ClickHouse not ready"
        )

        response = await test_client.get("/top-products?count=10")

        assert response.status_code == 503
```

### Example 2: Testing Async Use Case with Streaming

```python
@pytest.mark.asyncio
async def test_extract_orders_with_stream(
    mock_gateway: AsyncMock,
    mock_publisher: AsyncMock,
) -> None:
    """Test use case that processes streaming orders."""
    # Mock async generator
    async def fake_orders():
        for i in range(100):
            yield create_test_order(order_id=str(i))

    mock_gateway.fetch_orders.return_value = fake_orders()

    use_case = ExtractOrdersUseCase(
        gateway=mock_gateway,
        publisher=mock_publisher
    )

    result = await use_case.execute()

    assert result.orders_count == 100
    assert mock_publisher.publish_order.call_count == 100
```

### Example 3: Async Fixture with Parametrization

```python
@pytest.fixture(params=["http://localhost:8000", "https://api.example.com"])
async def api_client(request: pytest.FixtureRequest) -> AsyncGenerator[AsyncClient, None]:
    """Parametrized async client for different endpoints."""
    async with AsyncClient(base_url=request.param) as client:
        yield client

@pytest.mark.asyncio
async def test_against_multiple_endpoints(api_client: AsyncClient) -> None:
    """Test runs against each endpoint."""
    response = await api_client.get("/health")
    assert response.status_code == 200
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- pytest-asyncio >= 0.20.0
- httpx (for AsyncClient)
- asyncio (standard library)

## See Also

- [pytest-mocking-strategy](../pytest-mocking-strategy/SKILL.md) - Async mocking with AsyncMock
- [pytest-configuration](../pytest-configuration/SKILL.md) - pytest setup
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Section: "Async Testing Patterns"
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Async Testing Strategy"
