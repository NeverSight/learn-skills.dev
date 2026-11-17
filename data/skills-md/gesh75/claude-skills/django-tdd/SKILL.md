---
name: django-tdd
description: Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs.
origin: ECC
---

# Django Testing with TDD

Test-driven development for Django applications using pytest, factory_boy, and Django REST Framework.

## When to Activate

- Writing new Django applications
- Implementing Django REST Framework APIs
- Testing Django models, views, and serializers
- Setting up testing infrastructure for Django projects

> For generic pytest/TDD mechanics (Red-Green-Refactor discipline, fixtures vs mocks theory, parametrization, coverage interpretation), see the **python-testing** skill. This skill covers only Django-specific testing.

## TDD Workflow for Django

The Red-Green-Refactor loop applied to a Django model:

```python
# Step 1: RED - Write failing test
def test_user_creation():
    user = User.objects.create_user(email='test@example.com', password='testpass123')
    assert user.email == 'test@example.com'
    assert user.check_password('testpass123')
    assert not user.is_staff

# Step 2: GREEN - Make test pass
# Create User model or factory

# Step 3: REFACTOR - Improve while keeping tests green
```

## Setup (Django-specific)

Django test configuration is what differs from plain pytest: `DJANGO_SETTINGS_MODULE`, `--reuse-db`/`--nomigrations`, an in-memory SQLite test settings module, fast password hashers, eager Celery, and Django/DRF client fixtures (`client`, `api_client`, `authenticated_client`, `authenticated_api_client`).

Full `pytest.ini`, `config/settings/test.py`, and `conftest.py` → [reference/fixtures.md](reference/fixtures.md).

## Factory Boy

`factory_boy` replaces manual object creation for Django models — `DjangoModelFactory`, `Sequence`, `SubFactory`, `PostGenerationMethodCall('set_password', ...)`, `post_generation` for M2M, and `create_batch(n)`.

Full factory definitions and usage → [reference/factory-boy.md](reference/factory-boy.md).

## Testing Layers

| Layer | What to assert | Reference |
|-------|----------------|-----------|
| Models | field defaults, `__str__`, slug generation, `full_clean()` validation, custom manager/QuerySet methods, stock/business rules | [reference/model-view-tests.md](reference/model-view-tests.md) |
| Views | status codes, `response.context`, login-required redirects, POST creating objects | [reference/model-view-tests.md](reference/model-view-tests.md) |
| Serializers | `.data` output shape, `is_valid()`, `.errors` for field-level validation | [reference/drf-api-tests.md](reference/drf-api-tests.md) |
| API ViewSets | list/retrieve/create/update/delete status codes, auth (401/201), filtering, search via `reverse('api:...')` | [reference/drf-api-tests.md](reference/drf-api-tests.md) |
| Mocking & integration | `@patch` external gateways, `mail.outbox`, full multi-step flows | [reference/mocking-integration.md](reference/mocking-integration.md) |

## Testing Best Practices (Django-specific)

### DO

- **Use factories**: Instead of manual object creation
- **Mock external services**: Don't depend on external APIs (payment gateways, etc.)
- **Test permissions**: Ensure DRF authorization works (401/403)
- **Keep tests fast**: Use `--reuse-db` and `--nomigrations`
- **Use `mail.outbox`** with `locmem` backend to assert on sent email

### DON'T

- **Don't test Django internals**: Trust Django/DRF to work
- **Don't use the production database**: Always use the test settings module
- **Don't over-mock**: Mock only external dependencies, not your own ORM

(Generic DON'Ts — one assertion per test, no interdependent tests, don't test private methods — apply from the **python-testing** skill.)

## Coverage

```bash
# Run tests with coverage
pytest --cov=apps --cov-report=html --cov-report=term-missing
open htmlcov/index.html
```

### Coverage Goals

| Component | Target Coverage |
|-----------|-----------------|
| Models | 90%+ |
| Serializers | 85%+ |
| Views | 80%+ |
| Services | 90%+ |
| Utilities | 80%+ |
| Overall | 80%+ |

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `@pytest.mark.django_db` | Enable database access |
| `client` | Django test client |
| `api_client` | DRF API client |
| `factory.create_batch(n)` | Create multiple objects |
| `patch('module.function')` | Mock external dependencies |
| `override_settings` | Temporarily change settings |
| `force_authenticate()` | Bypass authentication in tests |
| `assertRedirects` | Check for redirects |
| `assertTemplateUsed` | Verify template usage |
| `mail.outbox` | Check sent emails |

Remember: Tests are documentation. Good tests explain how your code should work. Keep them simple, readable, and maintainable.

## Reference Files

- [reference/fixtures.md](reference/fixtures.md) — read when setting up pytest.ini, test settings, or conftest fixtures for a Django project.
- [reference/factory-boy.md](reference/factory-boy.md) — read when writing or using factory_boy factories for Django models.
- [reference/model-view-tests.md](reference/model-view-tests.md) — read when testing Django models or traditional (non-DRF) views.
- [reference/drf-api-tests.md](reference/drf-api-tests.md) — read when testing DRF serializers or API ViewSet endpoints.
- [reference/mocking-integration.md](reference/mocking-integration.md) — read when mocking external services/email or writing full-flow integration tests.
