---
name: api-development
description: Build REST and RPC APIs in Frappe including whitelisted methods, authentication, and permission handling. Use when creating custom endpoints, integrating with external systems, or exposing business logic via API.
---

# Frappe API Development

Build secure, well-designed APIs using Frappe's REST and RPC patterns.

## When to use

- Creating custom RPC endpoints (`@frappe.whitelist`)
- Building REST API integrations
- Implementing webhooks for external systems
- Setting up API authentication (token, OAuth)
- Exposing business logic to frontends

## Inputs required

- API purpose (CRUD, action, integration)
- Authentication requirements (public, user, API key)
- Permission requirements per endpoint
- Request/response format expectations

## Procedure

### 0) Choose API pattern

| Need | Pattern |
|------|---------|
| DocType CRUD | Use built-in REST API |
| Custom action | RPC with `@frappe.whitelist` |
| External callback | Webhook DocType |
| Batch operations | Background job + status endpoint |

### 1) Built-in REST API (DocType CRUD)

Frappe provides automatic REST endpoints for all DocTypes:

```bash
# Create
POST /api/resource/Customer
{"customer_name": "Acme Corp"}

# Read
GET /api/resource/Customer/CUST-001

# Update
PUT /api/resource/Customer/CUST-001
{"customer_name": "Acme Corporation"}

# Delete
DELETE /api/resource/Customer/CUST-001

# List with filters
GET /api/resource/Customer?filters=[["status","=","Active"]]
```

### 2) Custom RPC endpoints

Create whitelisted methods in your app:

```python
# my_app/api.py
import frappe

@frappe.whitelist()
def process_order(order_id, action):
    """Process an order with the given action."""
    # Always verify permissions
    doc = frappe.get_doc("Sales Order", order_id)
    if not frappe.has_permission("Sales Order", "write", doc):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    # Business logic
    if action == "approve":
        doc.status = "Approved"
        doc.save()
    
    return {"status": "success", "order": doc.name}

@frappe.whitelist(allow_guest=True)
def public_endpoint():
    """Public endpoint - no auth required."""
    return {"message": "Hello, World!"}
```

Call via:
```bash
POST /api/method/my_app.api.process_order
{"order_id": "SO-001", "action": "approve"}
```

### 3) Implement authentication

**API Key + Secret (recommended for integrations):**
```bash
# Header format
Authorization: token api_key:api_secret
```

**Bearer Token:**
```bash
Authorization: Bearer <token>
```

**Session (for logged-in users):**
Automatic via cookies.

### 4) Permission checks

**ALWAYS check permissions in RPC methods:**

```python
@frappe.whitelist()
def sensitive_action(docname):
    doc = frappe.get_doc("My DocType", docname)
    
    # Check document-level permission
    if not frappe.has_permission("My DocType", "write", doc):
        frappe.throw("Not permitted", frappe.PermissionError)
    
    # Check role-based permission
    if "Manager" not in frappe.get_roles():
        frappe.throw("Manager role required")
    
    # Proceed with action
    ...
```

### 5) Input validation

```python
@frappe.whitelist()
def create_item(name, qty, price):
    # Validate required fields
    if not name:
        frappe.throw("Name is required")
    
    # Validate types
    qty = frappe.utils.cint(qty)
    price = frappe.utils.flt(price)
    
    # Validate ranges
    if qty <= 0:
        frappe.throw("Quantity must be positive")
    
    # Proceed
    ...
```

### 6) Response format

**Success response:**
```python
return {
    "status": "success",
    "data": {...}
}
```

**Error handling:**
```python
# User-facing error
frappe.throw("Validation failed", title="Error")

# Permission error
frappe.throw("Not allowed", frappe.PermissionError)

# Standard exceptions become {"exc_type": "...", "exc": "..."}
```

### 7) Background jobs for long operations

```python
@frappe.whitelist()
def start_export(filters):
    job = frappe.enqueue(
        "my_app.jobs.run_export",
        filters=filters,
        queue="long",
        timeout=600
    )
    return {"job_id": job.id}

@frappe.whitelist()
def check_job_status(job_id):
    from frappe.utils.background_jobs import get_job
    job = get_job(job_id)
    return {"status": job.get_status()}
```

## Verification

- [ ] Endpoint responds correctly to valid requests
- [ ] Permission errors returned for unauthorized access
- [ ] Input validation rejects invalid data
- [ ] Error responses are structured and helpful
- [ ] Run: `bench --site <site> console` → test endpoint manually

## Failure modes / debugging

- **Method not found**: Check module path in URL matches Python path
- **Permission denied**: Verify `@frappe.whitelist()` decorator and user permissions
- **CSRF error**: Use proper auth headers for API calls
- **500 error**: Check error logs: `bench --site <site> show-log`

## Escalation

- For OAuth integration, see [references/oauth.md](references/oauth.md)
- For webhook patterns, see [references/webhooks.md](references/webhooks.md)
- For rate limiting, see [references/rate-limiting.md](references/rate-limiting.md)

## References

- [references/rest-api.md](references/rest-api.md) - REST API details
- [references/authentication.md](references/authentication.md) - Auth patterns
- [references/permissions.md](references/permissions.md) - Permission system
- [references/webhooks.md](references/webhooks.md) - Outbound webhooks

## Guardrails

- **Always validate input**: Never trust client data; validate type, length, and format server-side
- **Use permission callbacks**: Check `frappe.has_permission()` explicitly in whitelisted methods
- **Sanitize user input**: Use `frappe.db.escape()` for SQL, avoid `eval()` and dynamic code execution
- **Handle rate limiting**: Implement rate limits for public APIs to prevent abuse
- **Return structured errors**: Use `frappe.throw()` with proper HTTP status codes

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Missing `@frappe.whitelist()` | Method returns "Method not found" error | Add decorator to expose method via API |
| Using GET for mutations | Violates REST conventions, CSRF issues | Use POST/PUT/DELETE for data changes |
| Not handling errors | 500 errors expose stack traces | Wrap in try/except, use `frappe.throw()` |
| Exposing sensitive data | Security breach | Filter response fields, check permissions |
| Missing `allow_guest=True` | Public endpoints return 403 | Add `@frappe.whitelist(allow_guest=True)` for unauthenticated access |
| SQL injection in queries | Database compromise | Use Query Builder or `frappe.db.escape()` |
