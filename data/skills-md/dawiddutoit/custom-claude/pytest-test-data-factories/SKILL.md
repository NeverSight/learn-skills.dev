---
name: pytest-test-data-factories
description: |
  Patterns for creating reusable test data: factory functions for domain objects, builder patterns for complex objects, fixture factories, parameterized test data, test data inheritance, and type-safe test data generators. Use when creating test data repeatedly, building objects with many optional fields, or generating realistic test datasets.

  Use when: Writing tests that need domain objects, creating fixtures for multiple tests, generating test data with defaults, building complex objects with optional fields, or parameterizing tests with various data.
allowed-tools: Read, Bash, Write
---

# Pytest Test Data Factories

## Purpose

Test data factories eliminate duplication and make tests more maintainable. Instead of recreating `Order` objects with the same fields in every test, factories provide sensible defaults and allow customization only where needed.

## Quick Start

Create simple factory functions in `conftest.py`:

```python
# tests/unit/conftest.py
import pytest
from datetime import datetime
from app.extraction.domain.entities import Order
from app.extraction.domain.value_objects import OrderId, Money, ProductTitle

@pytest.fixture
def create_test_order():
    """Factory fixture for creating test orders with defaults."""
    def _create(
        order_id: str = "order_123",
        customer_name: str = "Test User",
        total: float = 99.99,
    ) -> Order:
        return Order(
            order_id=OrderId(order_id),
            created_at=datetime.now(),
            customer_name=customer_name,
            line_items=[create_test_line_item()],
            total_price=Money.from_float(total),
        )

    return _create

# Usage in tests
def test_order_validation(create_test_order):
    """Use factory with defaults."""
    order = create_test_order()
    assert order.customer_name == "Test User"

def test_order_custom_name(create_test_order):
    """Override specific fields."""
    order = create_test_order(customer_name="Jane Doe")
    assert order.customer_name == "Jane Doe"
```

## Instructions

### Step 1: Create Basic Factory Fixtures

```python
# tests/unit/conftest.py
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
import pytest

from app.extraction.domain.entities import Order, LineItem
from app.extraction.domain.value_objects import OrderId, ProductId, ProductTitle, Money

@pytest.fixture
def create_test_order():
    """Factory for Order aggregate with sensible defaults."""
    def _create(
        order_id: str = "order_123",
        customer_name: str = "Test User",
        line_items: Optional[list[LineItem]] = None,
        total: Optional[float] = None,
    ) -> Order:
        if line_items is None:
            line_items = [create_test_line_item()]

        # Calculate total from line items if not provided
        if total is None:
            total = sum(
                float(item.price.amount) * item.quantity
                for item in line_items
            )

        return Order(
            order_id=OrderId(order_id),
            created_at=datetime.now(),
            customer_name=customer_name,
            line_items=line_items,
            total_price=Money.from_float(total),
        )

    return _create

@pytest.fixture
def create_test_line_item():
    """Factory for LineItem entity with defaults."""
    def _create(
        product_id: str = "prod_1",
        product_title: str = "Test Product",
        quantity: int = 1,
        price: float = 99.99,
    ) -> LineItem:
        return LineItem(
            product_id=ProductId(product_id),
            product_title=ProductTitle(product_title),
            quantity=quantity,
            price=Money.from_float(price),
        )

    return _create
```

### Step 2: Use Builder Pattern for Complex Objects

```python
class OrderBuilder:
    """Builder for creating complex Order objects."""

    def __init__(self):
        self.order_id = "order_123"
        self.customer_name = "Test User"
        self.line_items: list[LineItem] = []
        self.total: Optional[float] = None

    def with_order_id(self, order_id: str) -> OrderBuilder:
        """Set order ID."""
        self.order_id = order_id
        return self

    def with_customer_name(self, name: str) -> OrderBuilder:
        """Set customer name."""
        self.customer_name = name
        return self

    def with_line_items(self, items: list[LineItem]) -> OrderBuilder:
        """Set line items."""
        self.line_items = items
        return self

    def add_line_item(self, item: LineItem) -> OrderBuilder:
        """Add a single line item."""
        self.line_items.append(item)
        return self

    def with_total(self, total: float) -> OrderBuilder:
        """Set total price."""
        self.total = total
        return self

    def build(self) -> Order:
        """Build the Order object."""
        if not self.line_items:
            self.line_items = [
                LineItem(
                    product_id=ProductId("prod_1"),
                    product_title=ProductTitle("Default Product"),
                    quantity=1,
                    price=Money.from_float(99.99),
                )
            ]

        # Auto-calculate total if not provided
        if self.total is None:
            self.total = sum(
                float(item.price.amount) * item.quantity
                for item in self.line_items
            )

        return Order(
            order_id=OrderId(self.order_id),
            created_at=datetime.now(),
            customer_name=self.customer_name,
            line_items=self.line_items,
            total_price=Money.from_float(self.total),
        )

# Usage
def test_with_builder():
    """Build complex order with fluent API."""
    order = (OrderBuilder()
        .with_customer_name("Jane Doe")
        .add_line_item(LineItem(...))
        .add_line_item(LineItem(...))
        .build())

    assert order.customer_name == "Jane Doe"
    assert len(order.line_items) == 2
```

### Step 3: Create Fixture Factories (Fixture Factories)

```python
@pytest.fixture
def order_factory(create_test_order):
    """Fixture factory that returns the create_test_order factory."""
    return create_test_order

def test_multiple_orders(order_factory):
    """Create multiple different orders easily."""
    order1 = order_factory(order_id="order_1", customer_name="Alice")
    order2 = order_factory(order_id="order_2", customer_name="Bob")
    order3 = order_factory(order_id="order_3", customer_name="Charlie")

    assert order1.order_id.value == "order_1"
    assert order2.order_id.value == "order_2"
    assert order3.order_id.value == "order_3"
```

### Step 4: Parametrize Tests with Factory-Generated Data

```python
import pytest
from decimal import Decimal

# Factory-generated test data
ORDER_TEST_CASES = [
    ("order_1", "Alice", 100.00, 1),
    ("order_2", "Bob", 250.50, 2),
    ("order_3", "Charlie", 999.99, 3),
]

@pytest.mark.parametrize(
    "order_id,customer_name,total,item_count",
    ORDER_TEST_CASES,
    ids=["alice_order", "bob_order", "charlie_order"]
)
def test_order_creation_parametrized(
    create_test_order,
    order_id: str,
    customer_name: str,
    total: float,
    item_count: int,
) -> None:
    """Test multiple orders with different data."""
    order = create_test_order(
        order_id=order_id,
        customer_name=customer_name,
        total=total,
    )

    assert order.order_id.value == order_id
    assert order.customer_name == customer_name
    assert float(order.total_price.amount) == total
```

### Step 5: Create Mock Response Templates

```python
# tests/unit/conftest.py or tests/unit/fixtures/responses.py

@pytest.fixture
def shopify_order_response() -> dict:
    """Mock Shopify API order response."""
    return {
        "id": "12345",
        "created_at": "2024-01-01T10:00:00Z",
        "customer": {"name": "John Doe"},
        "line_items": [
            {
                "product_id": "prod_1",
                "title": "Laptop",
                "quantity": 2,
                "price": "999.99",
            }
        ],
        "total_price": "1999.98",
    }

@pytest.fixture
def kafka_message_template() -> dict:
    """Mock Kafka message format."""
    return {
        "order_id": "12345",
        "created_at": "2024-01-01T10:00:00Z",
        "customer_name": "John Doe",
        "line_items": [
            {
                "product_id": "prod_1",
                "product_title": "Laptop",
                "quantity": 2,
                "price": 999.99,
            }
        ],
        "total_price": 1999.98,
    }

@pytest.fixture
def clickhouse_query_result() -> list[tuple]:
    """Mock ClickHouse query result."""
    return [
        ("Laptop", 100),
        ("Mouse", 50),
        ("Keyboard", 30),
    ]

# Usage in tests
async def test_shopify_gateway(shopify_order_response):
    """Use mock response template."""
    with aioresponses() as mock_http:
        mock_http.get(
            "https://test.myshopify.com/admin/api/2024-01/orders.json",
            payload=shopify_order_response,
        )
        # Test code...
```

### Step 6: Create Realistic Data with Faker

```python
from faker import Faker
import pytest

@pytest.fixture
def faker_instance():
    """Provide faker instance for generating realistic data."""
    return Faker()

@pytest.fixture
def create_realistic_order(faker_instance):
    """Factory creating realistic test orders."""
    def _create(count: int = 1) -> list[Order]:
        orders = []
        for _ in range(count):
            orders.append(Order(
                order_id=OrderId(faker_instance.uuid4()),
                created_at=faker_instance.date_time(),
                customer_name=faker_instance.name(),
                line_items=[
                    LineItem(
                        product_id=ProductId(faker_instance.uuid4()),
                        product_title=ProductTitle(faker_instance.word()),
                        quantity=faker_instance.random_int(1, 10),
                        price=Money.from_float(
                            float(faker_instance.pricetag())
                        ),
                    )
                ],
                total_price=Money.from_float(
                    float(faker_instance.pricetag())
                ),
            ))
        return orders

    return _create

def test_with_realistic_data(create_realistic_order):
    """Create realistic test data."""
    orders = create_realistic_order(count=5)
    assert len(orders) == 5
    assert all(isinstance(order, Order) for order in orders)
```

### Step 7: Create Test Data Inheritance

```python
class BaseOrderFactory:
    """Base factory with common defaults."""

    def __init__(self):
        self.order_id = "order_123"
        self.customer_name = "Test User"

class VIPOrderFactory(BaseOrderFactory):
    """Factory for high-value VIP orders."""

    def __init__(self):
        super().__init__()
        self.customer_name = "VIP Customer"
        self.total = 50000.00

class DiscountedOrderFactory(BaseOrderFactory):
    """Factory for discounted orders."""

    def __init__(self):
        super().__init__()
        self.customer_name = "Discount Customer"
        self.total = 10.00

# Usage
def test_vip_order():
    """Test VIP order type."""
    factory = VIPOrderFactory()
    assert factory.total == 50000.00

def test_discounted_order():
    """Test discounted order type."""
    factory = DiscountedOrderFactory()
    assert factory.total == 10.00
```

### Step 8: Create Domain-Specific Test Data Builders

```python
class ProductRankingFactory:
    """Factory for creating ProductRanking test data."""

    @staticmethod
    def create_default() -> ProductRanking:
        """Create with default values."""
        return ProductRanking(
            title="Test Product",
            rank=Rank(1),
            cnt_bought=100,
        )

    @staticmethod
    def create_list(count: int, start_rank: int = 1) -> list[ProductRanking]:
        """Create multiple rankings."""
        return [
            ProductRanking(
                title=f"Product {i}",
                rank=Rank(i + start_rank),
                cnt_bought=100 - (i * 10),
            )
            for i in range(count)
        ]

# Usage
def test_product_rankings(mock_query_gateway):
    """Use factory to create multiple rankings."""
    rankings = ProductRankingFactory.create_list(count=5)
    mock_query_gateway.query_top_products.return_value = rankings

    assert len(rankings) == 5
    assert rankings[0].rank.value == 1
```

## Examples

### Example 1: Complete Factory Setup

```python
# tests/unit/conftest.py

from __future__ import annotations

from datetime import datetime
from typing import Optional
import pytest

from app.extraction.domain.entities import Order, LineItem
from app.extraction.domain.value_objects import OrderId, ProductId, ProductTitle, Money

@pytest.fixture
def create_test_line_item():
    """Factory for test line items."""
    def _create(
        product_id: str = "prod_1",
        title: str = "Test Product",
        quantity: int = 1,
        price: float = 99.99,
    ) -> LineItem:
        return LineItem(
            product_id=ProductId(product_id),
            product_title=ProductTitle(title),
            quantity=quantity,
            price=Money.from_float(price),
        )

    return _create

@pytest.fixture
def create_test_order(create_test_line_item):
    """Factory for test orders."""
    def _create(
        order_id: str = "order_123",
        customer_name: str = "Test User",
        items: Optional[list[LineItem]] = None,
    ) -> Order:
        if items is None:
            items = [create_test_line_item()]

        total = sum(
            float(item.price.amount) * item.quantity for item in items
        )

        return Order(
            order_id=OrderId(order_id),
            created_at=datetime.now(),
            customer_name=customer_name,
            line_items=items,
            total_price=Money.from_float(total),
        )

    return _create

# Usage
def test_order_with_defaults(create_test_order):
    """Create order with all defaults."""
    order = create_test_order()
    assert order.customer_name == "Test User"
    assert len(order.line_items) == 1

def test_order_with_multiple_items(create_test_order, create_test_line_item):
    """Create order with custom line items."""
    items = [
        create_test_line_item(title="Laptop"),
        create_test_line_item(title="Mouse"),
        create_test_line_item(title="Keyboard"),
    ]
    order = create_test_order(items=items)
    assert len(order.line_items) == 3
```

### Example 2: Builder Pattern for Complex DTOs

```python
class CreateOrderRequestBuilder:
    """Builder for CreateOrderRequest DTO."""

    def __init__(self):
        self.data = {
            "customer_name": "Test User",
            "items": [],
            "total": 0.0,
        }

    def with_customer(self, name: str) -> CreateOrderRequestBuilder:
        self.data["customer_name"] = name
        return self

    def with_item(self, title: str, price: float, qty: int = 1) -> CreateOrderRequestBuilder:
        self.data["items"].append({"title": title, "price": price, "qty": qty})
        self.data["total"] += price * qty
        return self

    def build(self) -> dict:
        return self.data

# Usage
def test_create_order_request():
    request = (CreateOrderRequestBuilder()
        .with_customer("Alice")
        .with_item("Laptop", 999.99)
        .with_item("Mouse", 29.99, qty=2)
        .build())

    assert request["customer_name"] == "Alice"
    assert len(request["items"]) == 2
    assert request["total"] == 1059.97
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- Optional: faker >= 15.0 (for realistic data)
- Domain models in your application

## See Also

- [pytest-configuration](../pytest-configuration/SKILL.md) - Pytest setup and conftest organization
- [pytest-domain-model-testing](../pytest-domain-model-testing/SKILL.md) - Testing with these factories
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Required Test Infrastructure"
