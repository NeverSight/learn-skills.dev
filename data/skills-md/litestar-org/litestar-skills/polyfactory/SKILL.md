---
name: polyfactory
description: "Auto-activate for polyfactory, ModelFactory, DataclassFactory, MsgspecFactory, AttrsFactory, Use, register_fixture, pytest plugin, __random_seed__, or coverage(). Not for production seeding."
---

# polyfactory

Polyfactory is a typed mock-data factory library: declare `ModelFactory[T]` (or `DataclassFactory`, `MsgspecFactory`, `AttrsFactory`, `TypedDictFactory`) and `.build()` returns a populated instance of `T`. The matching factory base inspects the model's annotations and supported constraints so tests do not need hand-written happy-path fixtures.

In Litestar projects, polyfactory's pytest plugin is the canonical way to feed `TestClient.post(...)` / `AsyncTestClient.put(...)` payloads. The companion skill `litestar:litestar-testing` covers the request side.

## Code Style Rules

- PEP 604 unions: `T | None`, never `Optional[T]`.
- One factory per model. Don't reuse a factory across unrelated models — clarity beats DRY when the test fails at 3am.
- Pick the right factory base by backend: `ModelFactory` (Pydantic), `DataclassFactory`, `MsgspecFactory`, `AttrsFactory`, `TypedDictFactory`. A mismatched base raises `ConfigurationException`.
- Prefer `register_fixture` over hand-rolled `@pytest.fixture` wrappers. Call it in a pytest-discovered test module or `conftest.py` so the injected fixture is collected.

## Quick Reference

### Picking the right factory base

| Model kind | Factory base | Import |
| --- | --- | --- |
| `pydantic.BaseModel` | `ModelFactory` | `from polyfactory.factories.pydantic_factory import ModelFactory` |
| `@dataclass` | `DataclassFactory` | `from polyfactory.factories import DataclassFactory` |
| `msgspec.Struct` | `MsgspecFactory` | `from polyfactory.factories.msgspec_factory import MsgspecFactory` |
| `@attrs.define` / `attr.s` | `AttrsFactory` | `from polyfactory.factories.attrs_factory import AttrsFactory` |
| `TypedDict` | `TypedDictFactory` | `from polyfactory.factories.typed_dict_factory import TypedDictFactory` |
| Beanie / Odmantic / SQLA | dedicated bases | see [factories.md](references/factories.md) |

### Defining a factory

```python
from dataclasses import dataclass
from polyfactory.factories import DataclassFactory


@dataclass
class Order:
    id: int
    customer_email: str
    total_cents: int
    status: str


class OrderFactory(DataclassFactory[Order]):
    pass


# Use it
one = OrderFactory.build()
many = OrderFactory.batch(10)
```

The single concrete generic argument lets Polyfactory infer `__model__`. `build()` returns one instance, `batch(n)` returns `list[T]`, and `coverage()` yields the smallest set of instances that covers the model's supported variants.

### Customizing fields

```python
from polyfactory import Use
from polyfactory.factories import DataclassFactory


class OrderFactory(DataclassFactory[Order]):
    # Plain literal — every build returns this exact value
    status = "pending"

    # Callable — re-evaluated per build
    customer_email = Use(lambda: "test@example.com")

    # Random choice — re-evaluated per build
    total_cents = Use(DataclassFactory.__random__.randint, 100, 10_000)
```

`Use(callable, *args, **kwargs)` is re-invoked on every `build()`, so each generated instance gets a fresh value.

Use `PostGenerated` when a field depends on values generated for the same instance:

```python
from typing import Any

from polyfactory import PostGenerated


def order_reference(name: str, values: dict[str, Any], prefix: str) -> str:
    return f"{prefix}-{values['id']}"


class OrderFactory(DataclassFactory[Order]):
    reference = PostGenerated(order_reference, "order")
```

The callback signature is `(field_name, generated_values, *args, **kwargs)`. `generated_values` contains the non-post-generated fields.

### Determinism

```python
class OrderFactory(DataclassFactory[Order]):
    __random_seed__ = 42  # same seed → same output across runs
```

Set `__random_seed__` (or `__faker__ = Faker(seed=...)` for finer Faker control) when test assertions depend on the exact generated values.

### Default factory registration

```python
class CustomerFactory(DataclassFactory[Customer]):
    __set_as_default_factory_for_type__ = True


@dataclass
class Order:
    id: int
    customer: Customer  # automatically populated by CustomerFactory.build()


class OrderFactory(DataclassFactory[Order]):
    pass
```

When `__set_as_default_factory_for_type__ = True`, polyfactory uses that factory whenever the type appears as a field on another model — no manual nesting required.

### Pytest fixture from a factory

```python
from polyfactory.pytest_plugin import register_fixture
from polyfactory.factories import DataclassFactory


@register_fixture
class OrderFactory(DataclassFactory[Order]):
    pass


def test_order_total(order_factory: type[OrderFactory]) -> None:
    order = order_factory.build()
    assert order.total_cents >= 0
```

`@register_fixture` returns the class unchanged and injects a pytest fixture into the caller's module. The fixture name is the snake-cased class name and its value is the factory class.

### Cross-model relationships

```python
from polyfactory import Use
from polyfactory.pytest_plugin import register_fixture


@register_fixture
class CustomerFactory(DataclassFactory[Customer]):
    __set_as_default_factory_for_type__ = True


@register_fixture
class OrderFactory(DataclassFactory[Order]):
    customer = Use(CustomerFactory.build)  # explicit local override
```

`__set_as_default_factory_for_type__ = True` lets Polyfactory populate nested `Customer` fields with `CustomerFactory`. Use `Use(CustomerFactory.build)` when one parent factory needs an explicit local override.

<workflow>

## Workflow

### Step 1: Pick the factory base

Match the base to your model backend (table above). A mismatched base fails during factory class creation. If your project uses multiple backends (e.g., Pydantic for HTTP DTOs + msgspec for internal events), import each base separately and don't try to share a factory across backends.

### Step 2: Define one factory per model

Subclass the appropriate base with one concrete generic argument and let Polyfactory infer `__model__`. Set `__model__` explicitly only when the generic declaration cannot identify exactly one model. Keep factories in `tests/factories.py` or `tests/<feature>/factories.py`, outside production code paths.

### Step 3: Customize only what the test cares about

If a field can take any valid value, leave it for the factory to randomize. Override (literal value or `Use(...)`) only fields the assertion depends on. Tests that pin every field defeat the purpose of using a factory.

### Step 4: Register as a pytest fixture (if used widely)

For factories used in many tests, decorate with `@register_fixture` in a pytest-discovered module and consume the snake-cased fixture name. For one-off use, call `Factory.build()` directly inline.

### Step 5: Wire cross-model relationships

Set `__set_as_default_factory_for_type__ = True` on a base factory and let nested fields be populated automatically, or use `Use(OtherFactory.build)` for a local relationship override.

### Step 6: Pin determinism only when needed

Tests that assert on specific generated values need `__random_seed__`. Tests that assert on shape or invariants (e.g., `total >= 0`) should not — leaving randomization on widens coverage across runs.

</workflow>

<guardrails>

## Guardrails

- **Use one concrete generic argument or set `__model__`.** Polyfactory infers `__model__` from `DataclassFactory[Order]`; an unparameterized concrete factory without `__model__` raises `ConfigurationException` during class creation.
- **Don't override fields you're about to assert on with random values.** Either pin the value (`status = "pending"`) or assert on shape, not both.
- **Don't reuse `__random_seed__` across factories that share a Faker instance.** They will collide and produce unexpected duplicates. Use a different seed per factory or a single shared seeded `__faker__`.
- **Use the right base for the backend.** `ModelFactory` on a `msgspec.Struct` raises `ConfigurationException`; use `MsgspecFactory`.
- **Factories belong under `tests/`.** Importing them from production modules ties test data to runtime code and is a refactor hazard.
- **`coverage()` is not a Cartesian-product generator.** It emits a minimal representative set and reuses exhausted field variants; use Hypothesis for exhaustive input-space exploration.
- **`__allow_none_optionals__` is boolean.** `True` allows random `None` values during `build()`; `False` always generates the wrapped type. It is not a probability.
- **Async methods persist data.** `create_async()` and `create_batch_async()` require `__async_persistence__` or a backend factory that supplies it. Polyfactory has no `build_async()`.

</guardrails>

<validation>

## Validation Checkpoint

Before delivering polyfactory code, verify:

- [ ] Factory base matches the model backend (Pydantic → `ModelFactory`, dataclass → `DataclassFactory`, msgspec → `MsgspecFactory`, attrs → `AttrsFactory`).
- [ ] Each factory has one concrete generic model argument or an explicit `__model__`.
- [ ] Factories live under `tests/` (or a sibling test-only module), never in production code.
- [ ] Fields overridden in the factory match what the test asserts on; fields the test does not care about are left for randomization.
- [ ] If the test asserts on exact values, `__random_seed__` is set; otherwise it is not.
- [ ] `@register_fixture` is used for factories shared across more than ~2 test files; one-offs call `.build()` inline.
- [ ] Cross-model relationships use `__set_as_default_factory_for_type__` or `Use(OtherFactory.build)`.
- [ ] `register_fixture` is invoked in a pytest-discovered module.
- [ ] Async factory calls use `create_async()` / `create_batch_async()` only when persistence is configured.

</validation>

<example>

## Example: Litestar handler test with msgspec DTOs and polyfactory

```python
# tests/factories.py
from polyfactory.factories.msgspec_factory import MsgspecFactory

from myapp.events import OrderCreatedEvent  # msgspec.Struct


class OrderCreatedEventFactory(MsgspecFactory[OrderCreatedEvent]):
    pass
```

```python
# tests/conftest.py
from polyfactory.pytest_plugin import register_fixture

from tests.factories import OrderCreatedEventFactory


register_fixture(OrderCreatedEventFactory)
```

```python
# tests/test_orders.py
from __future__ import annotations  # consumer module — fine to use future annotations

import msgspec
import pytest
from litestar.testing import AsyncTestClient

from tests.factories import OrderCreatedEventFactory


@pytest.mark.anyio
async def test_create_order_emits_event(
    client: AsyncTestClient,
    order_created_event_factory: type[OrderCreatedEventFactory],
) -> None:
    payload = order_created_event_factory.build()
    response = await client.post("/orders", json=msgspec.to_builtins(payload))

    assert response.status_code == 201
    assert response.json()["id"] == payload.id
```

The factory provides a fully-populated, validation-passing `OrderCreatedEvent`; the test focuses on the request/response contract instead of constructing fake data inline.

</example>

---

## References Index

For detailed guides, refer to the following documents in `references/`:

- **[Factories](references/factories.md)** — Per-backend factory bases, model inference, randomization control, `PostGenerated`, model coverage, persistence protocols, and SQLAlchemy 3.3 persistence behavior.
- **[Pytest integration](references/pytest-integration.md)** — `@register_fixture`, separate registration from `conftest.py`, fixture scoping and naming, collection boundaries, and async persistence.
- **[Litestar patterns](references/litestar-patterns.md)** — Using factories with `TestClient` / `AsyncTestClient`, parametrizing handler tests via `coverage()`, integrating with `litestar-testing` fixtures, msgspec DTOs, advanced-alchemy model factories, and SAQ task payload generation.

---

## Official References

- <https://github.com/litestar-org/polyfactory/tree/v3.3.0/polyfactory> — immutable v3.3.0 source
- <https://github.com/litestar-org/polyfactory/tree/v3.3.0/tests> — immutable v3.3.0 contract tests
- <https://github.com/litestar-org/polyfactory/releases/tag/v3.3.0> — v3.3.0 release
- <https://polyfactory.litestar.dev/>
- <https://polyfactory.litestar.dev/usage/index.html>
- <https://polyfactory.litestar.dev/usage/library_factories/index.html>
- <https://polyfactory.litestar.dev/usage/decorators.html>
- <https://polyfactory.litestar.dev/usage/fixtures.html>
- <https://polyfactory.litestar.dev/usage/configuration.html>
- <https://github.com/litestar-org/polyfactory>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
