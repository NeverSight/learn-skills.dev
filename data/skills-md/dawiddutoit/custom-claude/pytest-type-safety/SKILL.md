---
name: pytest-type-safety
description: |
  Enforce type safety in all tests: type annotations for test functions and fixtures, mock autospec patterns, mypy configuration for tests, type-safe assertions, generic type handling in mocks. Includes protocol-based typing and cast patterns for complex scenarios.

  Use when: Writing type-safe tests, configuring mypy for test files, using protocols for mocks, enforcing type checking in CI/CD, or debugging type-related test issues.
allowed-tools: Read, Bash, Write
---

# Pytest Type Safety

## Quick Start

Add type annotations to every test function and fixture:

```python
from __future__ import annotations

from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock
import pytest

# ✅ Type annotations on fixture
@pytest.fixture
def create_test_order() -> Any:
    def _create(order_id: str = "123") -> Order:
        return Order(...)
    return _create

# ✅ Type annotations on test
@pytest.mark.asyncio
async def test_extract_orders(
    create_test_order: Any,
    mock_gateway: AsyncMock,
) -> None:
    """Test function with full type safety."""
    use_case = ExtractOrdersUseCase(gateway=mock_gateway)
    result = await use_case.execute()
    assert result is not None
```

## When to Use

- Write type-safe tests
- Configure mypy for test files
- Use protocols for mocks
- Enforce type checking in CI/CD
- Debug type-related test issues

## Key Patterns

### Test Functions

```python
def test_product_title() -> None:
    """Test product title creation."""
    title: ProductTitle = ProductTitle("Laptop")
    assert title.value == "Laptop"
```

### Fixtures

```python
@pytest.fixture
def create_test_line_item() -> Callable[..., LineItem]:
    """Factory for creating line items."""
    def _create(
        product_id: str = "prod_1",
        title: str = "Test Product",
        quantity: int = 1,
    ) -> LineItem:
        return LineItem(...)
    return _create
```

### Create_Autospec for Type-Safe Mocks

```python
from unittest.mock import create_autospec

# ✅ Mock with autospec enforces interface
def test_with_autospec() -> None:
    mock = create_autospec(ShopifyPort, instance=True)
    mock.fetch_orders.return_value = []
    # mock.typo_method() raises AttributeError
```

### Mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = true
disallow_any_unimported = false  # Allow Any from fixtures
```

### Type-Safe Assertions

```python
def test_order_type_safe(create_test_order: Any) -> None:
    order: Order = create_test_order()
    
    assert isinstance(order, Order)
    assert isinstance(order.customer_name, str)
```

## Supporting Files

| File | Purpose |
|------|---------|
| [references/type-safety-patterns.md](references/type-safety-patterns.md) | Complete patterns and CI/CD integration |

## Requirements

- Python 3.11+
- pytest >= 7.0
- mypy >= 1.7.0
- pyright >= 1.1.0 (optional)

## See Also

- [pytest-configuration](../pytest-configuration/SKILL.md) - mypy config
- [pytest-mocking-strategy](../pytest-mocking-strategy/SKILL.md) - create_autospec
