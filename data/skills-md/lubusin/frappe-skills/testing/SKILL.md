---
name: testing
description: Write and run tests for Frappe apps including unit tests, integration tests, and UI tests. Use when adding test coverage, debugging test failures, or setting up CI for Frappe projects.
---

# Frappe Testing

Write and run tests for Frappe applications using the built-in testing framework.

## When to use

- Writing unit tests for DocType controllers
- Writing integration tests for workflows and APIs
- Running existing test suites
- Debugging test failures
- Setting up CI pipelines for Frappe apps

## Inputs required

- App name to test
- Site name for test execution
- Specific module/DocType to test (optional)
- Test environment (dev site, dedicated test site)

## Procedure

### 0) Setup test environment

```bash
# Install dev dependencies
bench setup requirements --dev

# Ensure site is ready
bench --site <site> migrate
```

### 1) Run tests

```bash
# Run all tests for an app
bench --site <site> run-tests --app my_app

# Run tests for specific module
bench --site <site> run-tests --module my_app.my_module.tests

# Run tests for specific DocType
bench --site <site> run-tests --doctype "My DocType"

# Verbose output
bench --site <site> run-tests --app my_app -v

# Run single test file
bench --site <site> run-tests --module my_app.doctype.sample_doc.test_sample_doc
```

### 2) Write DocType tests

Create `test_<doctype_name>.py` alongside the DocType:

```python
# my_app/doctype/sample_doc/test_sample_doc.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestSampleDoc(FrappeTestCase):
    def setUp(self):
        # Create test data
        self.doc = frappe.get_doc({
            "doctype": "Sample Doc",
            "title": "Test Document"
        }).insert()
    
    def tearDown(self):
        # Cleanup
        frappe.delete_doc("Sample Doc", self.doc.name, force=True)
    
    def test_creation(self):
        self.assertEqual(self.doc.title, "Test Document")
    
    def test_validation(self):
        doc = frappe.get_doc({
            "doctype": "Sample Doc",
            "title": ""  # Invalid - required field
        })
        self.assertRaises(frappe.ValidationError, doc.insert)
    
    def test_workflow(self):
        self.doc.status = "Approved"
        self.doc.save()
        self.assertEqual(self.doc.status, "Approved")
```

### 3) Write API tests

```python
# my_app/tests/test_api.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestAPI(FrappeTestCase):
    def test_whitelist_method(self):
        from my_app.api import process_order
        
        # Create test order
        order = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": "_Test Customer"
        }).insert()
        
        # Test the API
        result = process_order(order.name, "approve")
        
        self.assertEqual(result["status"], "success")
        
        # Cleanup
        frappe.delete_doc("Sales Order", order.name, force=True)
    
    def test_permission_denied(self):
        # Test as restricted user
        frappe.set_user("guest@example.com")
        
        from my_app.api import sensitive_action
        self.assertRaises(frappe.PermissionError, sensitive_action, "doc-001")
        
        # Reset user
        frappe.set_user("Administrator")
```

### 4) Test permissions

```python
def test_role_permissions(self):
    # Create user with specific role
    user = frappe.get_doc({
        "doctype": "User",
        "email": "test_user@example.com",
        "roles": [{"role": "Sales User"}]
    }).insert()
    
    frappe.set_user("test_user@example.com")
    
    # Test permission
    self.assertTrue(frappe.has_permission("Sales Order", "read"))
    self.assertFalse(frappe.has_permission("Sales Order", "delete"))
    
    # Cleanup
    frappe.set_user("Administrator")
    frappe.delete_doc("User", user.name, force=True)
```

### 5) Use fixtures

```python
# my_app/doctype/sample_doc/test_records.json
[
    {
        "doctype": "Sample Doc",
        "title": "Test Record 1"
    },
    {
        "doctype": "Sample Doc",
        "title": "Test Record 2"
    }
]
```

Reference in tests:
```python
class TestSampleDoc(FrappeTestCase):
    def test_fixture_loaded(self):
        doc = frappe.get_doc("Sample Doc", "Test Record 1")
        self.assertIsNotNone(doc)
```

### 6) Run UI tests (Cypress)

```bash
# Run UI tests for an app
bench --site <site> run-ui-tests my_app

# Headless mode
bench --site <site> run-ui-tests my_app --headless
```

## Verification

- [ ] All tests pass: `bench --site <site> run-tests --app my_app`
- [ ] No test pollution (tests are isolated)
- [ ] Tests run in < 5 minutes for fast feedback
- [ ] CI pipeline runs tests on each commit

## Failure modes / debugging

- **Test not found**: Ensure filename starts with `test_` and class/method names follow conventions
- **Database errors**: Tests may not be isolated—check for missing cleanup
- **Permission errors in tests**: Use `frappe.set_user("Administrator")` in setup
- **Slow tests**: Avoid unnecessary fixtures, mock external services

## Escalation

- For complex fixtures, see [references/fixtures.md](references/fixtures.md)
- For UI testing patterns, see [references/cypress.md](references/cypress.md)
- For CI setup, see [references/ci-testing.md](references/ci-testing.md)

## References

- [references/test-patterns.md](references/test-patterns.md) - Common test patterns
- [references/fixtures.md](references/fixtures.md) - Test data management
- [references/cypress.md](references/cypress.md) - UI testing

## Guardrails

- **Use test fixtures**: Load test data via fixtures, not manual creation in each test
- **Clean up test data**: Delete created records in `tearDown()` or use `frappe.db.rollback()`
- **Mock external services**: Never call real APIs in tests; mock HTTP calls
- **Isolate tests**: Each test should be independent; no reliance on test execution order
- **Set user context explicitly**: Use `frappe.set_user()` to test as specific users

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Not using `FrappeTestCase` | Missing test setup/teardown | Extend `frappe.tests.utils.FrappeTestCase` |
| Missing db rollback | Test pollution, flaky tests | Use `frappe.db.rollback()` in tearDown or transactions |
| Flaky async tests | Intermittent failures | Use `frappe.tests.utils.run_until()` or proper async handling |
| Testing implementation not behavior | Brittle tests | Test outcomes, not internal method calls |
| Hardcoded test data | Conflicts with existing data | Use unique names like `_Test Record {uuid}` |
| Skipping permission tests | Security holes | Test with different user roles, not just Administrator |
