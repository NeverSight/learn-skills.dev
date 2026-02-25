---
name: pytest-domain-model-testing
description: |
  How to test domain models effectively: value object testing (immutability, validation), entity testing (identity, business logic), domain exception testing, aggregate testing, high coverage patterns (95%+), and testing invariants and constraints.

  Use when: Testing domain layer code, validating value objects, testing entities with business logic, ensuring domain invariants, or achieving 95%+ coverage on domain models.
allowed-tools: Read, Bash, Write
---

# Pytest Domain Model Testing

## Purpose

The domain layer contains business logic and should have near-perfect coverage (95-100%). Domain models have zero external dependencies, making them easy to test thoroughly. This skill focuses on testing pure domain logic effectively.


## When to Use This Skill

Use when testing domain models with "test value objects", "test entities", "test domain logic", or "achieve 95% domain coverage".

Do NOT use for application layer (use `pytest-application-layer-testing`), adapters (use `pytest-adapter-integration-testing`), or mocking (domain tests should use real objects).
## Quick Start

Test domain models directly without mocks:

```python
from app.extraction.domain.value_objects import ProductTitle
import pytest

def test_product_title_validation() -> None:
    """Test value object validation."""
    # ✅ Valid
    title = ProductTitle("Awesome Laptop")
    assert title.value == "Awesome Laptop"

    # ❌ Invalid: too short
    with pytest.raises(ValueError, match="must be 1-500"):
        ProductTitle("")

    # ❌ Invalid: too long
    with pytest.raises(ValueError, match="must be 1-500"):
        ProductTitle("x" * 501)
```

## Instructions

### Step 1: Test Value Objects (Immutability & Validation)

```python
from __future__ import annotations

import pytest
from app.extraction.domain.value_objects import ProductTitle, Money, OrderId

class TestProductTitle:
    """Test ProductTitle value object."""

    def test_valid_creation(self) -> None:
        """Test creating valid product title."""
        title = ProductTitle("Laptop")
        assert title.value == "Laptop"

    def test_empty_title_raises_error(self) -> None:
        """Test that empty title is invalid."""
        with pytest.raises(ValueError, match="must be 1-500 characters"):
            ProductTitle("")

    def test_too_long_title_raises_error(self) -> None:
        """Test that title over 500 chars is invalid."""
        with pytest.raises(ValueError, match="must be 1-500 characters"):
            ProductTitle("x" * 501)

    def test_boundary_exactly_500_chars(self) -> None:
        """Test boundary: exactly 500 characters is valid."""
        title = ProductTitle("x" * 500)
        assert len(title.value) == 500

    def test_immutability(self) -> None:
        """Test value object is immutable (frozen dataclass)."""
        title = ProductTitle("Laptop")

        with pytest.raises(AttributeError):
            title.value = "Mouse"  # Should fail

    def test_unicode_characters(self) -> None:
        """Test title with unicode works."""
        title = ProductTitle("Café ☕ Deluxe")
        assert title.value == "Café ☕ Deluxe"

    def test_whitespace_handling(self) -> None:
        """Test title with whitespace."""
        title = ProductTitle("  Laptop  ")
        assert title.value == "  Laptop  "  # Preserves whitespace

    def test_equality(self) -> None:
        """Test two titles with same value are equal."""
        title1 = ProductTitle("Laptop")
        title2 = ProductTitle("Laptop")
        assert title1 == title2

    def test_inequality(self) -> None:
        """Test two titles with different values are not equal."""
        title1 = ProductTitle("Laptop")
        title2 = ProductTitle("Mouse")
        assert title1 != title2

    def test_hashable(self) -> None:
        """Test value object can be hashed (for sets/dicts)."""
        title1 = ProductTitle("Laptop")
        title2 = ProductTitle("Laptop")
        title3 = ProductTitle("Mouse")

        titles_set = {title1, title2, title3}
        assert len(titles_set) == 2  # title1 and title2 are same

    def test_string_representation(self) -> None:
        """Test __str__ returns value."""
        title = ProductTitle("Laptop")
        assert str(title) == "Laptop"
```

### Step 2: Test Entities (Identity & Business Logic)

```python
from __future__ import annotations

from datetime import datetime
import pytest

from app.extraction.domain.entities import Order, LineItem
from app.extraction.domain.value_objects import OrderId, ProductId, ProductTitle, Money

class TestOrderEntity:
    """Test Order aggregate."""

    def test_valid_order_creation(self) -> None:
        """Test creating valid order."""
        order = Order(
            order_id=OrderId("123"),
            created_at=datetime.now(),
            customer_name="John",
            line_items=[
                LineItem(
                    product_id=ProductId("prod_1"),
                    product_title=ProductTitle("Laptop"),
                    quantity=1,
                    price=Money.from_float(999.99),
                )
            ],
            total_price=Money.from_float(999.99),
        )

        assert order.order_id.value == "123"
        assert order.customer_name == "John"

    def test_empty_line_items_invalid(self) -> None:
        """Test order must have at least one line item."""
        with pytest.raises(ValueError, match="must have at least one line item"):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="John",
                line_items=[],  # Invalid!
                total_price=Money.from_float(0.0),
            )

    def test_total_mismatch_invalid(self) -> None:
        """Test order total must match sum of line items."""
        with pytest.raises(ValueError, match="total mismatch"):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="John",
                line_items=[
                    LineItem(
                        product_id=ProductId("prod_1"),
                        product_title=ProductTitle("Laptop"),
                        quantity=1,
                        price=Money.from_float(999.99),
                    )
                ],
                total_price=Money.from_float(500.00),  # Wrong total!
            )

    def test_negative_quantity_invalid(self) -> None:
        """Test line item quantity must be positive."""
        with pytest.raises(ValueError, match="quantity must be positive"):
            LineItem(
                product_id=ProductId("prod_1"),
                product_title=ProductTitle("Laptop"),
                quantity=-5,  # Invalid!
                price=Money.from_float(999.99),
            )

    def test_get_product_titles_behavior(self) -> None:
        """Test domain behavior: extract product titles."""
        order = Order(
            order_id=OrderId("123"),
            created_at=datetime.now(),
            customer_name="John",
            line_items=[
                LineItem(
                    product_id=ProductId("prod_1"),
                    product_title=ProductTitle("Laptop"),
                    quantity=1,
                    price=Money.from_float(999.99),
                ),
                LineItem(
                    product_id=ProductId("prod_2"),
                    product_title=ProductTitle("Mouse"),
                    quantity=2,
                    price=Money.from_float(29.99),
                ),
            ],
            total_price=Money.from_float(1059.97),
        )

        titles = order.get_product_titles()
        assert titles == ["Laptop", "Mouse"]

    def test_order_identity_by_id(self) -> None:
        """Test orders with same ID but different data are considered same."""
        order1 = Order(
            order_id=OrderId("same_id"),
            created_at=datetime.now(),
            customer_name="John",
            line_items=[LineItem(...)],
            total_price=Money.from_float(100.0),
        )

        order2 = Order(
            order_id=OrderId("same_id"),
            created_at=datetime.now(),
            customer_name="Jane",  # Different name
            line_items=[LineItem(...)],
            total_price=Money.from_float(100.0),
        )

        # Entities with same ID are considered equal
        assert order1 == order2
```

### Step 3: Test Domain Exceptions

```python
from __future__ import annotations

import pytest
from app.extraction.domain.exceptions import (
    InvalidOrderException,
    InvalidProductException,
    ExtractionDomainException,
)

class TestDomainExceptions:
    """Test domain exception hierarchy."""

    def test_invalid_order_exception_is_domain_exception(self) -> None:
        """Test exception inheritance."""
        assert issubclass(InvalidOrderException, ExtractionDomainException)
        assert issubclass(InvalidOrderException, ValueError)

    def test_invalid_order_exception_message(self) -> None:
        """Test exception contains descriptive message."""
        with pytest.raises(InvalidOrderException, match="missing line items"):
            raise InvalidOrderException("Order is invalid: missing line items")

    def test_invalid_product_exception(self) -> None:
        """Test product validation exception."""
        with pytest.raises(InvalidProductException):
            raise InvalidProductException("Product title too long")

    def test_exception_propagation(self) -> None:
        """Test exception can be caught by base class."""
        try:
            raise InvalidOrderException("Order validation failed")
        except ExtractionDomainException as e:
            assert "validation failed" in str(e)
```

### Step 4: Test Aggregate Invariants

```python
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
import pytest

from app.extraction.domain.entities import Order, LineItem

class TestOrderInvariants:
    """Test aggregate invariants and business rules."""

    def test_invariant_at_least_one_item(self) -> None:
        """Test invariant: order must have >= 1 item."""
        with pytest.raises(ValueError):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="John",
                line_items=[],  # Violates invariant
                total_price=Money.from_float(0.0),
            )

    def test_invariant_positive_total(self) -> None:
        """Test invariant: order total must be > 0."""
        with pytest.raises(ValueError):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="John",
                line_items=[LineItem(...)],
                total_price=Money.from_float(0.0),  # Invalid!
            )

    def test_invariant_total_consistency(self) -> None:
        """Test invariant: order total = sum of line items."""
        items = [
            LineItem(..., price=Money.from_float(100.0), quantity=2),
            LineItem(..., price=Money.from_float(50.0), quantity=1),
        ]

        # Correct total
        order = Order(
            order_id=OrderId("123"),
            created_at=datetime.now(),
            customer_name="John",
            line_items=items,
            total_price=Money.from_float(250.0),  # 2*100 + 1*50
        )
        assert order is not None

        # Incorrect total
        with pytest.raises(ValueError, match="total mismatch"):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="John",
                line_items=items,
                total_price=Money.from_float(999.0),  # Wrong!
            )

    def test_invariant_customer_name_not_empty(self) -> None:
        """Test invariant: customer name cannot be empty."""
        with pytest.raises(ValueError, match="customer name"):
            Order(
                order_id=OrderId("123"),
                created_at=datetime.now(),
                customer_name="",  # Invalid!
                line_items=[LineItem(...)],
                total_price=Money.from_float(100.0),
            )
```

### Step 5: Test Domain Services

```python
from __future__ import annotations

import pytest
from decimal import Decimal

from app.extraction.domain.services import OrderCalculationService
from app.extraction.domain.value_objects import Money

class TestOrderCalculationService:
    """Test stateless domain service."""

    def test_calculate_total_from_items(self) -> None:
        """Test total calculation logic."""
        items = [
            (Decimal("100.00"), 2),  # (price, qty)
            (Decimal("50.00"), 1),
        ]

        total = OrderCalculationService.calculate_total(items)

        assert total == Decimal("250.00")

    def test_calculate_tax(self) -> None:
        """Test tax calculation."""
        subtotal = Decimal("100.00")
        tax_rate = Decimal("0.10")  # 10%

        tax = OrderCalculationService.calculate_tax(subtotal, tax_rate)

        assert tax == Decimal("10.00")

    def test_calculate_discount(self) -> None:
        """Test discount application."""
        subtotal = Decimal("100.00")
        discount_percent = Decimal("10")  # 10% off

        discounted = OrderCalculationService.apply_discount(
            subtotal,
            discount_percent
        )

        assert discounted == Decimal("90.00")
```

### Step 6: Test Complex Value Object Logic

```python
from __future__ import annotations

import pytest
from decimal import Decimal

from app.extraction.domain.value_objects import Money

class TestMoneyValueObject:
    """Test Money value object with arithmetic."""

    def test_add_money(self) -> None:
        """Test adding two money amounts."""
        money1 = Money.from_float(100.00)
        money2 = Money.from_float(50.00)

        result = money1.add(money2)

        assert result.amount == Decimal("150.00")

    def test_multiply_money(self) -> None:
        """Test multiplying money by quantity."""
        money = Money.from_float(99.99)
        quantity = 3

        result = money.multiply(quantity)

        assert result.amount == Decimal("299.97")

    def test_compare_money(self) -> None:
        """Test money comparison."""
        money1 = Money.from_float(100.00)
        money2 = Money.from_float(100.00)
        money3 = Money.from_float(50.00)

        assert money1 == money2
        assert money1 != money3
        assert money1 > money3
        assert money3 < money1

    def test_negative_money_invalid(self) -> None:
        """Test that negative money is rejected."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Money(Decimal("-100.00"))
```

### Step 7: Use Parametrization for Comprehensive Coverage

```python
from __future__ import annotations

import pytest
from app.extraction.domain.value_objects import ProductTitle

# Test data for multiple scenarios
TITLE_VALID_CASES = [
    "Single",
    "Multiple Words",
    "With Numbers 123",
    "With Special !@#$%",
    "x" * 500,  # Max length
]

TITLE_INVALID_CASES = [
    ("", "empty"),
    ("x" * 501, "too_long"),
    ("\n\t", "only_whitespace"),
]

@pytest.mark.parametrize(
    "title",
    TITLE_VALID_CASES,
    ids=[f"valid_{i}" for i in range(len(TITLE_VALID_CASES))]
)
def test_valid_titles(title: str) -> None:
    """Test all valid title formats."""
    product_title = ProductTitle(title)
    assert product_title.value == title

@pytest.mark.parametrize(
    "title,reason",
    TITLE_INVALID_CASES,
    ids=[reason for _, reason in TITLE_INVALID_CASES]
)
def test_invalid_titles(title: str, reason: str) -> None:
    """Test all invalid title formats."""
    with pytest.raises(ValueError):
        ProductTitle(title)
```

## Examples

### Example 1: Comprehensive Value Object Test

```python
class TestOrderId:
    """Comprehensive tests for OrderId value object."""

    def test_creation(self) -> None:
        oid = OrderId("order_123")
        assert oid.value == "order_123"

    def test_immutability(self) -> None:
        oid = OrderId("order_123")
        with pytest.raises(AttributeError):
            oid.value = "order_456"

    def test_equality(self) -> None:
        oid1 = OrderId("order_123")
        oid2 = OrderId("order_123")
        assert oid1 == oid2

    def test_hashable(self) -> None:
        oid1 = OrderId("order_123")
        oid2 = OrderId("order_123")
        order_ids = {oid1, oid2}
        assert len(order_ids) == 1

    def test_invalid_empty_id(self) -> None:
        with pytest.raises(ValueError):
            OrderId("")

    def test_invalid_whitespace_id(self) -> None:
        with pytest.raises(ValueError):
            OrderId("   ")

    def test_string_representation(self) -> None:
        oid = OrderId("order_123")
        assert str(oid) == "order_123"
```

### Example 2: Comprehensive Aggregate Test

```python
class TestProductRanking:
    """Test ProductRanking aggregate."""

    def test_valid_creation(self) -> None:
        ranking = ProductRanking(
            title="Laptop",
            rank=Rank(1),
            cnt_bought=100,
        )
        assert ranking.title == "Laptop"
        assert ranking.cnt_bought == 100

    def test_rank_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            ProductRanking(
                title="Laptop",
                rank=Rank(0),  # Invalid
                cnt_bought=100,
            )

    def test_count_must_be_non_negative(self) -> None:
        with pytest.raises(ValueError):
            ProductRanking(
                title="Laptop",
                rank=Rank(1),
                cnt_bought=-5,  # Invalid
            )

    def test_title_immutability(self) -> None:
        ranking = ProductRanking(
            title="Laptop",
            rank=Rank(1),
            cnt_bought=100,
        )

        with pytest.raises(AttributeError):
            ranking.title = "Mouse"  # Immutable
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- Domain models from your application
- No external dependencies for domain layer

## See Also

- [pytest-test-data-factories](../pytest-test-data-factories/SKILL.md) - Creating test data
- [pytest-mocking-strategy](../pytest-mocking-strategy/SKILL.md) - Mocking (not needed for domain tests)
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Type Safety section
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Domain Layer Testing"
