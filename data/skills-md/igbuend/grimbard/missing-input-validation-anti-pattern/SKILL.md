---
name: "missing-input-validation-anti-pattern"
description: "Security anti-pattern for missing input validation (CWE-20). Use when generating or reviewing code that processes user input, form data, API parameters, or external data. Detects client-only validation, missing type checks, and absent length limits. Foundation vulnerability enabling most attack classes."
---

# Missing Input Validation Anti-Pattern

**Severity:** High

## Summary

Missing input validation occurs when applications fail to validate data from users or external sources before processing it. This enables SQL Injection, Cross-Site Scripting (XSS), Command Injection, and Path Traversal attacks. Treat all incoming data as untrusted. Validate against strict rules for type, length, format, and range.

## The Anti-Pattern

Trusting external input without server-side validation. Client-side validation provides no security—attackers bypass it trivially.

### BAD Code Example

```python
# VULNERABLE: Trusts user input completely, enabling SQL Injection
from flask import request
import sqlite3

@app.route("/api/products")
def search_products():
    # Takes 'category' directly from URL query string
    category = request.args.get("category")

    # Input concatenated directly into SQL query (classic SQL Injection)
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    query = f"SELECT id, name, price FROM products WHERE category = '{category}'"

    # Attacker request: /api/products?category=' OR 1=1 --
    # Resulting query: "SELECT ... FROM products WHERE category = '' OR 1=1 --'"
    # Returns ALL products, bypassing filter
    cursor.execute(query)
    products = cursor.fetchall()
    return {"products": products}
```

### GOOD Code Example

```python
# SECURE: Validates all input on server against strict allowlist
from flask import request
import sqlite3

# Strict allowlist of known-good values for 'category' parameter
ALLOWED_CATEGORIES = {"electronics", "books", "clothing", "homegoods"}

@app.route("/api/products/safe")
def search_products_safe():
    category = request.args.get("category")

    # 1. VALIDATE EXISTENCE: Check parameter provided
    if not category:
        return {"error": "Category parameter is required."}, 400

    # 2. VALIDATE AGAINST ALLOWLIST: Strongest form of input validation
    if category not in ALLOWED_CATEGORIES:
        return {"error": "Invalid category specified."}, 400

    # 3. USE PARAMETERIZED QUERIES: Safe database APIs prevent injection
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    # '?' placeholder treats input as data, not code
    query = "SELECT id, name, price FROM products WHERE category = ?"
    cursor.execute(query, (category,))
    products = cursor.fetchall()
    return {"products": products}
```

## Detection

- **Trace user input:** Follow HTTP request data (URL parameters, POST body, headers, cookies) through code. Verify validation occurs before use.
- **Find client-side-only validation:** Check for `required` HTML attributes or JavaScript validation without server-side equivalents.
- **Identify missing checks:** Find input handling without type, length, format, or range validation.

## Prevention

Apply "Validate, then Act" to all incoming data.

- [ ] **Validate server-side:** Client-side validation provides UX, not security
- [ ] **Use allowlists:** Known-good lists beat known-bad blocklists
- [ ] **Apply multi-layer validation:**
  - **Type:** Verify expected type (number vs string)
  - **Length:** Enforce min/max to prevent buffer overflows and DoS
  - **Format:** Match expected patterns (email, phone regex)
  - **Range:** Verify numerical bounds
- [ ] **Use schema validation libraries:** For JSON/XML, use Pydantic, JSON Schema, or Marshmallow

## Related Security Patterns & Anti-Patterns

Missing input validation enables most major vulnerability classes.

- [SQL Injection Anti-Pattern](../sql-injection/)
- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/)
- [Command Injection Anti-Pattern](../command-injection/)
- [Path Traversal Anti-Pattern](../path-traversal/)

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM05:2025 - Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CAPEC-153: Input Data Manipulation](https://capec.mitre.org/data/definitions/153.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
