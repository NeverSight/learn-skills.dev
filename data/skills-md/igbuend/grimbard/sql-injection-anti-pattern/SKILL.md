---
name: "sql-injection-anti-pattern"
description: "Security anti-pattern for SQL Injection vulnerabilities (CWE-89). Use when generating or reviewing code that constructs database queries, builds SQL statements, or handles user input in database operations. Detects string concatenation in queries and recommends parameterized queries."
---

# SQL Injection Anti-Pattern

**Severity:** Critical

## Summary

Attackers execute arbitrary SQL commands by manipulating user input. String concatenation in queries (frequently AI-generated from insecure training data) enables database compromise, data exfiltration, authentication bypass, and remote code execution.

## The Anti-Pattern

The anti-pattern is concatenating user data into SQL statements, allowing attackers to break query structure and inject malicious SQL.

### BAD Code Example

```python
# VULNERABLE: String concatenation creates injection vector.
import sqlite3

def get_user(db_connection, username):
    # User input concatenated directly into query.
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor = db_connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()

# Attack: username = "admin' OR '1'='1' --"
# Result: "SELECT * FROM users WHERE username = 'admin' OR '1'='1' --'"
# Returns all users, bypassing authentication.
```

### GOOD Code Example

```python
# SECURE: Parameterized queries prevent injection.
import sqlite3

def get_user(db_connection, username):
    # Parameters sent separately and escaped by database driver.
    # Malicious input cannot alter query logic.
    query = "SELECT * FROM users WHERE username = ?"
    cursor = db_connection.cursor()
    cursor.execute(query, (username,))
    return cursor.fetchone()

# Named parameters (preferred for clarity):
# query = "SELECT * FROM users WHERE username = :username"
# cursor.execute(query, {"username": username})
```

## Detection

- Look for string concatenation (`+`, `||`, `concat()`, f-strings, template literals) used to build SQL queries.
- Search for calls to `execute()`, `query()`, or `raw()` that take a single string variable which may contain user input.
- Check for the use of `.format()`, `%s`, or `${}` within SQL query strings.
- Review any code that dynamically constructs SQL based on user input without proper parameterization.

## Prevention

- [ ] **Use parameterized queries:** Always use prepared statements for all database operations.
- [ ] **Never concatenate user input:** Avoid direct string concatenation in SQL.
- [ ] **Use ORM libraries:** Tools with built-in SQL injection protection (SQLAlchemy, Django ORM, Hibernate).
- [ ] **Apply least privilege:** Database accounts should have minimal necessary permissions.
- [ ] **Validate input as defense-in-depth:** Not primary defense, but supplements parameterization.

## Related Security Patterns & Anti-Patterns

- [Command Injection Anti-Pattern](../command-injection/): Similar injection vulnerability but for shell commands.
- [LDAP Injection Anti-Pattern](../ldap-injection/): Injection vulnerability in LDAP queries.
- [XPath Injection Anti-Pattern](../xpath-injection/): Injection vulnerability in XML queries.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): A root cause that enables many injection attacks.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CAPEC-66: SQL Injection](https://capec.mitre.org/data/definitions/66.html)
- [PortSwigger: Sql Injection](https://portswigger.net/web-security/sql-injection)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
