---
name: pytest-django-patterns
description: pytest-django testing patterns, Factory Boy, fixtures, and TDD workflow. Use when writing tests, creating test factories, or following TDD red-green-refactor cycle.
---

# pytest-django Testing Patterns

## TDD Workflow (RED-GREEN-REFACTOR)

**Always follow this cycle:**

1. **RED**: Write a failing test first that describes desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Clean up code while keeping tests green
4. **REPEAT**: Never write production code without a failing test

**Critical rule**: If implementing a feature or fixing a bug, write the test BEFORE touching production code.

## Essential pytest-django Patterns

### Database Access

- Use `@pytest.mark.django_db` on any test touching the database
- Apply to entire module: `pytestmark = pytest.mark.django_db`
- Transactions roll back automatically after each test

### Fixtures for Test Data

**Use Factory Boy for models, pytest fixtures for setup:**

- **Factories**: Create model instances with realistic data (`UserFactory()`)
  - Use `factory.Sequence()` for unique fields
  - Use `factory.Faker()` for realistic fake data
  - Use `factory.SubFactory()` for foreign keys
  - Use `@factory.post_generation` for M2M relationships

- **Fixtures**: Setup clients, auth state, or shared resources
  - `client` fixture: Django test client
  - Create `auth_client` fixture: `client.force_login(user)` for authenticated requests
  - Define in `conftest.py` for reuse across test files

### Test Organization

**Structure tests to mirror app structure:**
```
tests/
├── apps/
│   └── posts/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_forms.py
├── factories.py
└── conftest.py
```

**Group related tests in classes:**
- Name classes `TestComponentName` (e.g., `TestPostListView`)
- Name test methods descriptively: `test_<action>_<expected_outcome>`
- Use `@pytest.mark.parametrize` for testing multiple scenarios

## What to Test

### Views
- **Status codes**: Correct HTTP responses (200, 404, 302)
- **Authentication**: Authenticated vs anonymous behavior
- **Authorization**: User can only access their own data
- **Context data**: Correct objects passed to template
- **Side effects**: Database changes, emails sent, tasks queued
- **HTMX**: Check `HTTP_HX_REQUEST` header returns partial template

### Forms
- **Validation**: Valid data passes, invalid data fails with correct errors
- **Edge cases**: Empty fields, max lengths, unique constraints
- **Clean methods**: Custom validation logic works
- **Save behavior**: Objects created/updated correctly

### Models
- **Methods**: `__str__`, custom methods return expected values
- **Managers/QuerySets**: Custom filtering works correctly
- **Constraints**: Database-level validation enforced
- **Signals**: Pre/post save hooks execute correctly

### Celery Tasks
- **Mock external calls**: Patch HTTP requests, email sending, etc.
- **Test logic only**: Don't test actual async execution
- **Idempotency**: Running task multiple times is safe

## Django-Specific Testing Patterns

### Testing HTMX Responses

Check partial template rendered when `HX-Request` header present:
- Pass `HTTP_HX_REQUEST="true"` to client request
- Assert `response.templates` contains partial template name

### Testing Permissions

Create authenticated vs anonymous client fixtures:
- Test redirect/403 for unauthorized access
- Test success for authorized access

### Testing QuerySets

Verify efficient queries:
- Create test data with factories
- Execute query
- Assert correct objects returned/excluded
- Verify related objects loaded with `select_related()`/`prefetch_related()`

### Testing Forms with Model Instances

Pass instance to form for updates:
- `form = MyForm(data=new_data, instance=existing_obj)`
- Verify `form.save()` updates, doesn't create

## Common Patterns

**Parametrize multiple scenarios:**
Use `@pytest.mark.parametrize("input,expected", [...])` for testing various inputs

**Mock external services:**
Use `mocker.patch()` to avoid actual HTTP calls, emails, file operations

**Check database changes:**
- Assert `Model.objects.filter(...).exists()` after creation
- Assert `Model.objects.count() == expected` for deletions
- Use `refresh_from_db()` to verify updates

**Test error handling:**
- Invalid form data produces correct errors
- Failed operations return error responses
- User sees appropriate error messages

## Running Tests

```bash
uv run pytest                    # All tests
uv run pytest -x                 # Stop on first failure
uv run pytest --lf               # Run last failed
uv run pytest -x --lf            # Stop first, last failed only
uv run pytest -k "test_name"     # Run tests matching pattern
uv run pytest tests/apps/posts/  # Specific directory
uv run pytest --cov=apps         # With coverage report
```

## Common Pitfalls

- **Forgetting `@pytest.mark.django_db`**: Results in "Database access not allowed" errors
- **Not using factories**: Creating instances manually is verbose and brittle
- **Testing implementation**: Test behavior and outcomes, not internal implementation details
- **Skipping TDD**: Writing tests after code means tests follow implementation, missing edge cases
- **Over-mocking**: Mock external dependencies, not your own code
- **Testing framework code**: Don't test Django's ORM, form validation, etc. Test YOUR logic

## Setup Requirements

**In `pyproject.toml`:**
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = ["--reuse-db", "-ra"]
```

**In `conftest.py`:**
Define shared fixtures (auth_client, common factories, etc.)

## Integration with Other Skills

- **systematic-debugging**: When fixing bugs, write failing test first to reproduce
- **django-models**: Test custom managers, QuerySets, and model methods
- **django-forms**: Test form validation, clean methods, and save behavior
- **celery-patterns**: Test task logic with mocked external dependencies
