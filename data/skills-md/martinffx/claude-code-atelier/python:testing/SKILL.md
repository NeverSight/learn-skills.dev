---
name: python:testing
description: Stub-Driven TDD and layer boundary testing with pytest. Use when writing tests, deciding what to test, testing at component boundaries, or implementing test-driven development.
user-invocable: false
---

# Testing with pytest

Stub-Driven TDD and layer boundary testing patterns for Python applications.

## Core Principle: Stub-Driven TDD

Test at component boundaries, not internal implementation:

```
Router → Service → Repository → Entity → Database
   ↓        ↓           ↓          ↓
 Test    Test        Test       Test
```

Follow the **Stub → Test → Implement → Refactor** workflow:

1. **Stub** - Create function signature with `pass`
2. **Test** - Write test for expected behavior
3. **Implement** - Make test pass
4. **Refactor** - Clean up code

```python
# 1. Stub
def calculate_discount(total: Decimal) -> Decimal:
    pass

# 2. Test
def test_discount_for_large_order():
    result = calculate_discount(Decimal("150"))
    assert result == Decimal("15")

# 3. Implement
def calculate_discount(total: Decimal) -> Decimal:
    if total > 100:
        return total * Decimal("0.1")
    return Decimal("0")
```

## Layer Boundary Testing Overview

Test **what crosses layer boundaries**, not internal implementation:

- **Entity Layer**: Domain logic, validation, transformations (from_request, to_response, to_record)
- **Service Layer**: Business workflows, error handling, dependency orchestration
- **Repository Layer**: CRUD operations, query logic, entity ↔ record transformations
- **Router Layer**: Request validation, response serialization, status codes

See references/boundaries.md for comprehensive layer-specific examples.

## Entity Testing Example

Test transformations and business logic:

```python
def test_product_from_request():
    """Test creation from request"""
    request = CreateProductRequest(name="Widget", price=Decimal("9.99"))
    product = Product.from_request(request)

    assert product.name == "Widget"
    assert product.price == Decimal("9.99")
    assert isinstance(product.id, UUID)

def test_product_apply_discount():
    """Test business logic"""
    product = Product(id=uuid4(), name="Widget", price=Decimal("100"))
    discounted = product.apply_discount(Decimal("0.1"))

    assert discounted.price == Decimal("90")
```

## Service Testing Example

Test orchestration with stubbed dependencies:

```python
from unittest.mock import Mock

def test_create_product_service():
    """Test with mocked repository"""
    mock_repo = Mock()
    mock_repo.save.return_value = Product(id=uuid4(), name="Widget")

    service = ProductService(repo=mock_repo)
    result = service.create(CreateProductRequest(name="Widget", price=Decimal("9.99")))

    mock_repo.save.assert_called_once()
    assert result.name == "Widget"
```

## Repository Testing Example

Test data access with real test database:

```python
@pytest.fixture
def test_db():
    """In-memory test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def test_repository_save(test_db):
    """Test database operations"""
    repo = ProductRepository(test_db)
    product = Product(id=uuid4(), name="Widget", price=Decimal("9.99"))

    saved = repo.save(product)

    assert saved.id == product.id
    assert test_db.query(ProductRecord).count() == 1
```

## Router Testing Example

Test HTTP layer with TestClient:

```python
from fastapi.testclient import TestClient

def test_create_product_endpoint():
    """Test POST endpoint"""
    client = TestClient(app)

    response = client.post(
        "/products",
        json={"name": "Widget", "price": 9.99},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```

## Test Organization Basics

```
tests/
├── unit/
│   ├── test_entities.py      # Entity + Value object tests
│   └── test_services.py      # Service tests (with mocks)
├── integration/
│   ├── test_repositories.py  # Repository tests (with DB)
│   └── test_endpoints.py     # Router tests (with client)
└── conftest.py               # Shared fixtures
```

## Reference Documentation

For comprehensive patterns and examples, see:

- **references/boundaries.md** - Layer boundary testing patterns with complete examples for each layer
- **references/mocking.md** - Mock strategies, verification methods, and anti-patterns
- **references/pytest.md** - Configuration, fixtures, markers, parametrization, and debugging

Progressive disclosure: SKILL.md provides quick reference, references/ contain full details.
