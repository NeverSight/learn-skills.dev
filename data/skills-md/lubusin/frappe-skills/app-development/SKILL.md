---
name: app-development
description: Scaffold and architect custom Frappe apps including app structure, hooks, background jobs, service layers, and production hardening. Use when creating new apps, setting up app architecture, or implementing cross-cutting patterns like caching, logging, and error handling.
---

# Frappe App Development

Scaffold, structure, and architect custom Frappe applications with production-grade patterns.

## When to use

- Creating a new custom Frappe app from scratch
- Setting up app architecture (modules, services, utils)
- Configuring `hooks.py` for events, scheduler, overrides
- Implementing background jobs and async processing
- Building service layers and domain logic patterns
- Adding caching, logging, error handling utilities
- Preparing apps for production deployment
- Managing translations, versioning, and packaging

## Inputs required

- App name and purpose
- Target Frappe version (v13+, v15+, v16+)
- Module structure (which DocTypes, APIs, services)
- Whether hooks/overrides of other apps are needed
- Background job requirements
- Production readiness needs

## Procedure

### 0) Scaffold the app

```bash
# Create the app
bench new-app my_app

# Install on site
bench --site mysite.local install-app my_app

# Verify developer mode
bench --site mysite.local console
>>> frappe.conf.developer_mode  # Must be True
```

### 1) Plan app structure

Follow the domain architecture pattern — keep DocType controllers thin and business logic in service modules:

```
my_app/
├── my_app/
│   ├── __init__.py
│   ├── hooks.py              # App hooks and configuration
│   ├── api.py                # Public API surface (RPC endpoints)
│   ├── services/             # Business logic modules
│   │   └── billing.py
│   ├── utils/                # Cross-cutting utilities
│   │   ├── cache.py
│   │   ├── errors.py
│   │   ├── logging.py
│   │   ├── permissions.py
│   │   └── validation.py
│   ├── background_jobs/      # Async job handlers
│   │   └── export_job.py
│   ├── integrations/         # External system connectors
│   │   └── payment_gateway.py
│   ├── my_module/
│   │   ├── doctype/
│   │   │   └── my_doc/
│   │   │       ├── my_doc.json
│   │   │       ├── my_doc.py
│   │   │       ├── my_doc.js
│   │   │       └── test_my_doc.py
│   │   ├── report/
│   │   └── dashboard/
│   └── translations/
│       ├── en.csv
│       └── fr.csv
├── setup.py
└── README.md
```

Use the mini-app-template in `assets/mini-app-template/` as a starting scaffold.

### 2) Configure hooks.py

```python
# hooks.py

app_name = "my_app"
app_title = "My App"
app_publisher = "My Company"

# DocType lifecycle events
doc_events = {
    "Sales Order": {
        "on_submit": "my_app.services.billing.on_order_submit",
        "on_cancel": "my_app.services.billing.on_order_cancel",
    },
    "*": {
        "after_insert": "my_app.utils.logging.log_creation",
    }
}

# Scheduled tasks
scheduler_events = {
    "daily": [
        "my_app.background_jobs.cleanup.run_daily_cleanup"
    ],
    "cron": {
        "0 */6 * * *": [
            "my_app.background_jobs.sync.sync_external_data"
        ]
    }
}

# Client-side script injection
doctype_js = {
    "Sales Order": "public/js/sales_order.js"
}

doctype_list_js = {
    "Sales Order": "public/js/sales_order_list.js"
}

# Override another app's controller (use sparingly)
# override_doctype_class = {
#     "ToDo": "my_app.overrides.custom_todo.CustomToDo"
# }

# Extend controller without full replacement (v16+, preferred)
# extend_doctype_class = {
#     "ToDo": "my_app.overrides.todo_extension.TodoExtension"
# }

# Override whitelisted methods
# override_whitelisted_methods = {
#     "frappe.client.get_list": "my_app.overrides.custom_get_list"
# }
```

### 3) Implement service layer

Keep DocType controllers thin — delegate business logic to services:

```python
# my_app/services/billing.py
import frappe

def on_order_submit(doc, method):
    """Handle order submission — called via doc_events hook."""
    if doc.grand_total > 10000:
        create_approval_request(doc)
    generate_invoice(doc)

def generate_invoice(order):
    """Create invoice from submitted order."""
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": order.customer,
        "items": [
            {"item_code": i.item_code, "qty": i.qty, "rate": i.rate}
            for i in order.items
        ]
    })
    invoice.insert()
    invoice.submit()
    return invoice
```

### 4) Set up background jobs

```python
# my_app/background_jobs/export_job.py
import frappe

def enqueue_export(filters):
    """Enqueue a long-running export job."""
    frappe.enqueue(
        "my_app.background_jobs.export_job.run_export",
        filters=filters,
        queue="long",
        timeout=600,
        is_async=True
    )

def run_export(filters):
    """Execute the export — runs in background worker."""
    data = frappe.get_all("Sales Order", filters=filters, fields=["*"])
    # Process data...
    frappe.publish_realtime("export_complete", {"count": len(data)})
```

### 5) Add cross-cutting utilities

```python
# my_app/utils/cache.py
import frappe

def get_cached_settings(key):
    """Cache expensive settings lookups."""
    value = frappe.cache().get_value(f"my_app:{key}")
    if value is None:
        value = frappe.db.get_single_value("My Settings", key)
        frappe.cache().set_value(f"my_app:{key}", value)
    return value

def invalidate_cache(key):
    frappe.cache().delete_value(f"my_app:{key}")
```

```python
# my_app/utils/errors.py
import frappe

def api_error(message, status_code=400, exc=None):
    """Consistent error response for API endpoints."""
    frappe.local.response["http_status_code"] = status_code
    frappe.throw(message, exc or frappe.ValidationError)
```

### 6) Handle translations

```python
# In Python code
frappe._("Hello World")   # Mark string for translation

# In JavaScript
__("Hello World")         # Mark string for translation
```

```bash
# Translation CSV files go in my_app/translations/
# e.g., my_app/translations/fr.csv:
# Hello World,Bonjour le monde
```

### 7) Version compatibility

| Feature | Minimum Version |
|---------|----------------|
| `extend_doctype_class` | Frappe v16+ |
| REST API v2 (`/api/v2/`) | Frappe v15+ |
| Token-based auth | Frappe v11.0.3+ |

When targeting multiple versions, guard version-specific features:

```python
import frappe

if hasattr(frappe, 'extend_doctype_class'):
    # v16+ pattern
    pass
else:
    # Fallback for older versions
    pass
```

## Verification

- [ ] App installs without errors: `bench --site <site> install-app my_app`
- [ ] Hooks fire correctly (check scheduler logs, doc events)
- [ ] Background jobs enqueue and complete
- [ ] `bench --site <site> migrate` succeeds
- [ ] Tests pass: `bench --site <site> run-tests --app my_app`

## Failure modes / debugging

- **App not found**: Check `apps.txt` and `sites/<site>/site_config.json`
- **Hooks not firing**: Verify `hooks.py` syntax; restart bench
- **Background jobs stuck**: Check worker status with `bench doctor`; verify Redis
- **Import errors**: Ensure module paths in hooks match actual Python paths
- **Developer mode off**: DocType changes won't export to files

## Escalation

- For DocType creation details → `doctype-development`
- For API endpoint patterns → `api-development`
- For Desk UI customization → `desk-customization`
- For Frappe UI frontends → `frontend-development`
- For print formats and Jinja → `printing-templates`
- For reports → `reports`
- For web forms → `web-forms`
- For testing → `testing`
- For enterprise architecture → `enterprise-patterns`
- For Docker/FM environments → `frappe-manager`

## References

- [references/app-development.md](references/app-development.md) — End-to-end app architecture
- [references/version-compat.md](references/version-compat.md) — Version compatibility notes
- [references/translations.md](references/translations.md) — Multi-language support

### Cross-references (owned by specialized skills)

- hooks.py and extension points → `doctype-development` ([hooks-extensions.md](../doctype-development/references/hooks-extensions.md))
- Python API reference → `api-development` ([python-api.md](../api-development/references/python-api.md))

## Guardrails

- **Use Frappe UI for custom frontends**: Never use vanilla JS, jQuery, or custom frameworks. Frappe UI (Vue 3 + TailwindCSS) is the ecosystem standard. See `frontend-development` for setup.
- **Follow CRM/Helpdesk patterns for CRUD apps**: Follow `ui-patterns` skill for app shell, navigation, list views, and form layouts derived from official Frappe apps.
- **Follow naming conventions**: App name must be lowercase with underscores, valid Python identifier
- **Use hooks.py for integrations**: Never monkey-patch; use doc_events, scheduler_events, boot_session hooks
- **Keep hooks.py clean**: Only configuration, no logic; import from modules
- **Maintain backwards compatibility**: Use `frappe.version` checks for cross-version support
- **Export fixtures properly**: Use `fixtures` in hooks.py for data that should sync with app

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| App not in `installed_apps` | App code not loaded | Run `bench --site <site> install-app my_app` |
| Wrong module path in hooks | Events don't fire | Verify path matches actual `my_app/module/file.py` structure |
| Duplicate hook registrations | Events fire multiple times | Check hooks.py for duplicates; use list not repeated keys |
| Editing hooks.py without restart | Changes not picked up | Run `bench restart` after hooks.py changes |
| Missing `__init__.py` files | Module import errors | Ensure every directory has `__init__.py` |
| Logic in hooks.py | Hard to test, import errors | Move logic to separate modules, import in hooks |
| Building frontend with vanilla JS/jQuery | Inconsistent with ecosystem | Use Frappe UI (Vue 3); see `frontend-development` |
| Custom app shell for CRUD apps | Inconsistent UX | Follow CRM/Helpdesk patterns for navigation and layouts |
