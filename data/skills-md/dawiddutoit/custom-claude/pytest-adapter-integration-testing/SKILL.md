---
name: pytest-adapter-integration-testing
description: |
  Testing adapters and gateways: when to use unit test mocks vs testcontainers, mocking HTTP responses (aioresponses, responses), mocking Kafka messages, mocking ClickHouse responses, testing error paths and edge cases.

  Use when: Testing gateways and adapters, testing external service integrations, deciding between mocks and real containers, testing error handling in adapters, integration testing with real services.
allowed-tools: Read, Bash, Write
---

# Pytest Adapter Integration Testing

## Purpose

Adapters connect your application to external systems. This skill covers testing both unit-level (mocked) and integration-level (real services) scenarios.


## When to Use This Skill

Use when testing adapters and gateways with "test Shopify gateway", "mock HTTP responses", "test Kafka adapter", or "decide between mocks and containers".

Do NOT use for domain testing (use `pytest-domain-model-testing`), application layer (use `pytest-application-layer-testing`), or general mocking patterns (use `pytest-mocking-strategy`).
## Quick Start

Choose testing strategy based on scope:

```python
# UNIT TEST: Mock HTTP responses
import pytest
from aioresponses import aioresponses

async def test_shopify_gateway_unit() -> None:
    """Unit test with mocked HTTP."""
    with aioresponses() as mock_http:
        mock_http.get(
            "https://test.myshopify.com/api/orders",
            payload={"orders": [{"id": "123", "total": 100}]},
        )

        gateway = ShopifyGateway(url="https://test.myshopify.com")
        orders = await gateway.fetch_orders()

        assert len(orders) == 1


# INTEGRATION TEST: Real container
from testcontainers.kafka import KafkaContainer
import pytest

@pytest.fixture(scope="module")
def kafka_container():
    """Real Kafka for integration testing."""
    with KafkaContainer() as kafka:
        yield kafka

async def test_kafka_producer_integration(kafka_container):
    """Integration test with real Kafka."""
    producer = KafkaProducerAdapter(kafka_container)
    await producer.publish("test_topic", {"data": "value"})
    # Verify message was actually published
```

## Instructions

### Step 1: Unit Test with Mocked HTTP Responses

```python
from __future__ import annotations

from aioresponses import aioresponses
from unittest.mock import AsyncMock
import pytest

from app.extraction.adapters.shopify import ShopifyGateway


class TestShopifyGatewayUnit:
    """Unit tests with mocked HTTP responses."""

    async def test_fetch_orders_success(self) -> None:
        """Test successful order fetching."""
        # Mock Shopify API response
        shopify_response = {
            "orders": [
                {
                    "id": "12345",
                    "created_at": "2024-01-01T10:00:00Z",
                    "customer": {"name": "John Doe"},
                    "line_items": [
                        {
                            "product_id": "prod_1",
                            "title": "Laptop",
                            "quantity": 1,
                            "price": "999.99",
                        }
                    ],
                    "total_price": "999.99",
                }
            ]
        }

        with aioresponses() as mock_http:
            mock_http.get(
                "https://test.myshopify.com/admin/api/2024-01/orders.json",
                payload=shopify_response,
            )

            gateway = ShopifyGateway(
                shop_url="https://test.myshopify.com",
                access_token="test_token",
            )

            # Act
            orders = []
            async for order in await gateway.fetch_orders():
                orders.append(order)

            # Assert
            assert len(orders) == 1
            assert orders[0].customer_name == "John Doe"

    async def test_fetch_orders_with_pagination(self) -> None:
        """Test pagination handling."""
        # First page response
        page1 = {
            "orders": [{"id": "1", ...}],
            "next_page_url": "https://test.myshopify.com/api/orders?page=2",
        }

        # Second page response
        page2 = {
            "orders": [{"id": "2", ...}],
        }

        with aioresponses() as mock_http:
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                payload=page1,
            )
            mock_http.get(
                "https://test.myshopify.com/api/orders?page=2",
                payload=page2,
            )

            gateway = ShopifyGateway(...)

            orders = []
            async for order in await gateway.fetch_orders():
                orders.append(order)

            assert len(orders) == 2

    async def test_fetch_orders_handles_api_errors(self) -> None:
        """Test error handling for API failures."""
        from app.extraction.adapters.shopify import ShopifyApiException

        with aioresponses() as mock_http:
            # First request fails, second succeeds (retry)
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                status=500,
            )
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                payload={"orders": []},
            )

            gateway = ShopifyGateway(...)

            # Should succeed after retry
            orders = []
            async for order in await gateway.fetch_orders():
                orders.append(order)

            assert len(orders) == 0  # Empty but no exception

    async def test_rate_limiting_handling(self) -> None:
        """Test rate limit handling."""
        with aioresponses() as mock_http:
            # Rate limited response
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                status=429,
                headers={"Retry-After": "1"},
            )

            gateway = ShopifyGateway(...)

            # Gateway should handle 429 gracefully
            # Implementation depends on retry strategy
```

### Step 2: Mock Kafka Messages

```python
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
import pytest


@pytest.fixture
def mock_kafka_message():
    """Factory for creating mock Kafka messages."""
    def _create(key: str, value: dict) -> MagicMock:
        message = MagicMock()
        message.key.return_value = key.encode()
        message.value.return_value = json.dumps(value).encode()
        message.error.return_value = None
        return message

    return _create


@pytest.fixture
def mock_kafka_consumer(mock_kafka_message):
    """Mock Kafka consumer for unit tests."""
    mock = AsyncMock()

    # Return fake messages
    messages = [
        mock_kafka_message("order_1", {"id": "1", "total": 100}),
        mock_kafka_message("order_2", {"id": "2", "total": 200}),
    ]

    mock.consume.return_value = messages
    mock.close.return_value = None

    return mock


class TestKafkaConsumerAdapter:
    """Test Kafka consumer adapter with mocks."""

    async def test_consume_orders(self, mock_kafka_consumer) -> None:
        """Test consuming orders from Kafka."""
        adapter = KafkaConsumerAdapter(mock_kafka_consumer)

        messages = []
        async for msg in adapter.consume():
            messages.append(msg)

        assert len(messages) == 2
        assert messages[0]["id"] == "1"

    async def test_handle_deserialization_error(self, mock_kafka_consumer) -> None:
        """Test handling malformed messages."""
        # Mock message with invalid JSON
        bad_message = MagicMock()
        bad_message.value.return_value = b"invalid json"

        mock_kafka_consumer.consume.return_value = [bad_message]

        adapter = KafkaConsumerAdapter(mock_kafka_consumer)

        # Should either skip or raise, depending on implementation
        messages = []
        async for msg in adapter.consume():
            messages.append(msg)

        # Verify error was logged/handled
```

### Step 3: Mock ClickHouse Client Responses

```python
from __future__ import annotations

from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_clickhouse_client():
    """Mock ClickHouse client."""
    from clickhouse_driver import Client

    mock = MagicMock(spec=Client)

    # Mock successful query execution
    mock.execute.return_value = [
        ("Laptop", 100),
        ("Mouse", 50),
        ("Keyboard", 30),
    ]

    return mock


class TestClickHouseQueryGateway:
    """Test ClickHouse gateway with mocks."""

    def test_query_top_products(self, mock_clickhouse_client) -> None:
        """Test query execution."""
        gateway = ClickHouseQueryGateway(mock_clickhouse_client)

        results = gateway.query_top_products(limit=10)

        assert len(results) == 3
        assert results[0][0] == "Laptop"
        assert results[0][1] == 100

        # Verify correct query was executed
        mock_clickhouse_client.execute.assert_called_once()
        call_args = mock_clickhouse_client.execute.call_args
        assert "ORDER BY" in call_args[0][0]  # Query contains ORDER BY

    def test_query_empty_result(self, mock_clickhouse_client) -> None:
        """Test query with no results."""
        mock_clickhouse_client.execute.return_value = []

        gateway = ClickHouseQueryGateway(mock_clickhouse_client)

        results = gateway.query_top_products(limit=10)

        assert len(results) == 0

    def test_query_error_handling(self, mock_clickhouse_client) -> None:
        """Test error handling."""
        from clickhouse_driver import Error

        mock_clickhouse_client.execute.side_effect = Error("Connection failed")

        gateway = ClickHouseQueryGateway(mock_clickhouse_client)

        with pytest.raises(Error):
            gateway.query_top_products(limit=10)
```

### Step 4: Integration Tests with Testcontainers

```python
from __future__ import annotations

from testcontainers.kafka import KafkaContainer
from testcontainers.clickhouse import ClickHouseContainer
import pytest


@pytest.fixture(scope="module")
def kafka_container():
    """Real Kafka container for integration tests."""
    with KafkaContainer() as kafka:
        yield kafka


@pytest.fixture(scope="module")
def clickhouse_container():
    """Real ClickHouse container for integration tests."""
    with ClickHouseContainer() as ch:
        yield ch


class TestKafkaIntegration:
    """Integration tests with real Kafka."""

    async def test_produce_and_consume(self, kafka_container) -> None:
        """Test real message flow."""
        from confluent_kafka import Producer, Consumer

        # Create real producer
        producer = Producer({
            "bootstrap.servers": kafka_container.get_bootstrap_server(),
        })

        # Produce message
        producer.produce(
            "test_topic",
            key="order_1",
            value=b'{"id": "1", "total": 100}',
        )
        producer.flush()

        # Create real consumer
        consumer = Consumer({
            "bootstrap.servers": kafka_container.get_bootstrap_server(),
            "group.id": "test_group",
            "auto.offset.reset": "earliest",
        })
        consumer.subscribe(["test_topic"])

        # Consume message
        messages = []
        for _ in range(1):
            msg = consumer.poll(timeout=5)
            if msg:
                messages.append(msg.value())

        consumer.close()

        assert len(messages) == 1

    async def test_multiple_partitions(self, kafka_container) -> None:
        """Test handling multiple partitions."""
        # Create topic with multiple partitions
        # Produce messages to different partitions
        # Verify all messages are consumed
```

### Step 5: Integration Tests with Real ClickHouse

```python
def test_schema_initialization(clickhouse_container) -> None:
    """Test creating schema in real ClickHouse."""
    from clickhouse_driver import Client

    client = Client(
        host=clickhouse_container.get_container_host_ip(),
        port=clickhouse_container.get_exposed_port(8123),
    )

    # Create test database
    client.execute("CREATE DATABASE IF NOT EXISTS test_db")

    # Create table
    client.execute("""
        CREATE TABLE IF NOT EXISTS test_db.products (
            title String,
            cnt_bought UInt32,
        )
        ENGINE = MergeTree()
        ORDER BY cnt_bought DESC
    """)

    # Insert data
    client.execute(
        "INSERT INTO test_db.products VALUES",
        [("Laptop", 100), ("Mouse", 50)],
    )

    # Query data
    results = client.execute("SELECT * FROM test_db.products")

    assert len(results) == 2
    assert results[0][0] == "Mouse"  # Sorted by cnt_bought DESC

    # Cleanup
    client.execute("DROP TABLE test_db.products")
    client.execute("DROP DATABASE test_db")
```

### Step 6: Test Error Paths

```python
class TestErrorHandling:
    """Test adapter error handling."""

    async def test_timeout_handling(self) -> None:
        """Test timeout errors."""
        from aioresponses import aioresponses
        import asyncio

        with aioresponses() as mock_http:
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                exception=asyncio.TimeoutError("Request timeout"),
            )

            gateway = ShopifyGateway(...)

            with pytest.raises(asyncio.TimeoutError):
                await gateway.fetch_orders()

    async def test_connection_error(self) -> None:
        """Test connection errors."""
        from aioresponses import aioresponses

        with aioresponses() as mock_http:
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                exception=ConnectionError("Unable to connect"),
            )

            gateway = ShopifyGateway(...)

            with pytest.raises(ConnectionError):
                await gateway.fetch_orders()

    async def test_invalid_response_format(self) -> None:
        """Test handling malformed responses."""
        from aioresponses import aioresponses

        with aioresponses() as mock_http:
            mock_http.get(
                "https://test.myshopify.com/api/orders",
                payload={"invalid_format": "missing_orders_key"},
            )

            gateway = ShopifyGateway(...)

            with pytest.raises(KeyError):
                async for order in await gateway.fetch_orders():
                    pass
```

## Examples

### Example 1: Complete Adapter Unit Test

```python
class TestShopifyGatewayComplete:
    """Comprehensive adapter unit tests."""

    @pytest.mark.asyncio
    async def test_successful_order_fetch(self) -> None:
        """Happy path test."""
        with aioresponses() as mock_http:
            mock_http.get("https://api.example.com/orders", payload={
                "orders": [{"id": "1", "total": 100}]
            })

            gateway = ShopifyGateway("https://api.example.com")
            orders = [o async for o in await gateway.fetch_orders()]

            assert len(orders) == 1

    @pytest.mark.asyncio
    async def test_error_recovery(self) -> None:
        """Test retry logic."""
        with aioresponses() as mock_http:
            mock_http.get("...", status=500)
            mock_http.get("...", payload={"orders": []})

            gateway = ShopifyGateway(...)
            orders = [o async for o in await gateway.fetch_orders()]

            assert len(orders) == 0
```

### Example 2: Choose Test Strategy Matrix

```
Adapter           Unit Test (Mock)              Integration (Container)
─────────────────────────────────────────────────────────────────────
Shopify API       ✅ aioresponses               ❌ (use mock)
Kafka Producer    ✅ AsyncMock                  ✅ KafkaContainer
Kafka Consumer    ✅ AsyncMock                  ✅ KafkaContainer (preferred)
ClickHouse        ✅ MagicMock(Client)          ✅ ClickHouseContainer (preferred)
HTTP Clients      ✅ aioresponses/responses     ❌ (use mock)
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- pytest-asyncio >= 0.20.0
- aioresponses (for async HTTP mocking)
- testcontainers >= 3.7.0 (for integration tests)

## See Also

- [pytest-mocking-strategy](../pytest-mocking-strategy/SKILL.md) - Mocking with AsyncMock
- [pytest-async-testing](../pytest-async-testing/SKILL.md) - Async testing patterns
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Adapter Layer Testing"
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Section: "Mocking Strategy"
