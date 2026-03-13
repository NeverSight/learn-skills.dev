---
name: "verbose-error-messages-anti-pattern"
description: "Security anti-pattern for verbose error messages (CWE-209). Use when generating or reviewing code that handles errors, exceptions, or generates user-facing error responses. Detects stack trace exposure and detailed error information leakage to users."
---

# Verbose Error Messages Anti-Pattern

**Severity:** Medium

## Summary

Applications expose internal information (stack traces, database errors, file paths, configuration details) in error messages, enabling attackers to understand architecture, identify vulnerabilities, and craft targeted attacks. Suppress detailed errors in production.

## The Anti-Pattern

The anti-pattern is presenting raw exception messages or system errors directly to end-users.

### BAD Code Example

```python
# VULNERABLE: The application exposes raw database errors and stack traces to the user.
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/user_profile")
def user_profile():
    user_id = request.args.get("id")

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        # Imagine 'users' table does not exist or 'id' column is missing.
        # This will throw a `sqlite3.OperationalError`.
        cursor.execute(f"SELECT username, email FROM users WHERE id = {user_id}")
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return jsonify({"username": user_data[0], "email": user_data[1]})
        else:
            return "User not found", 404

    except Exception as e:
        # CRITICAL FLAW: The raw exception message is returned directly to the user.
        # This could include SQL query details, table names, column names,
        # or even parts of the application's code structure in a stack trace.
        #
        # Example output for an attacker:
        # "OperationalError: no such table: users"
        # "Traceback (most recent call last):
        #   File "/app/main.py", line 15, in user_profile
        #     cursor.execute(f"SELECT username, email FROM users WHERE id = {user_id}")
        # sqlite3.OperationalError: no such table: users"
        return f"An internal server error occurred: {str(e)}", 500
```

### GOOD Code Example

```python
# SECURE: Generic error messages are returned to the user, with detailed logging internally.
from flask import Flask, request, jsonify
import sqlite3
import logging
import traceback # To capture stack traces for internal logging

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/user_profile_secure")
def user_profile_secure():
    user_id = request.args.get("id")

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return jsonify({"username": user_data[0], "email": user_data[1]})
        else:
            return "User not found", 404

    except Exception as e:
        # 1. Log full exception details internally for debugging.
        #    Include unique error ID for correlation with user reports.
        error_id = str(uuid.uuid4())
        logging.error(f"Error ID: {error_id}. Detailed error: {e}\n{traceback.format_exc()}")

        # 2. Return generic error message to end-user.
        #    Include error ID for support reference.
        return jsonify({
            "error": "An internal server error occurred.",
            "message": "Please try again later. If the problem persists, contact support with Error ID: " + error_id
        }), 500

# Another example: Authentication error messages should be generic to prevent user enumeration.
@app.route("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not authenticate_user(username, password):
        # BAD: "User not found" or "Incorrect password". This tells attacker if username exists.
        # GOOD: Generic "Invalid credentials" message for both username not found and wrong password.
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful"}), 200
```

## Detection

- **Review error handling code:** Look for `try...except` blocks or global error handlers. Check what information is returned to the user in the `except` block.
- **Test with invalid inputs:** Deliberately trigger errors by providing malformed data, invalid IDs, or non-existent resources. Observe the error messages returned by the application.
- **Check server configurations:** Ensure that web servers (Apache, Nginx) and application frameworks (Spring, Django, Flask) are configured to suppress detailed errors and custom 500 error pages in production.

## Prevention

- [ ] **Return generic error messages to users:** Never display raw exception messages, stack traces, or system errors. Use "An unexpected error occurred" or similar.
- [ ] **Log detailed errors internally:** Log full stack traces, request details, and exception information to secure internal logging systems for debugging.
- [ ] **Use unique error IDs:** Generate a unique ID for each error and include it in user-facing messages. Enables support staff to locate detailed log entries.
- [ ] **Consolidate authentication error messages:** Return single generic message ("Invalid credentials") for all authentication failures (username not found, wrong password). Prevents user enumeration.
- [ ] **Configure custom error pages:** Implement custom 404/500 pages without exposing sensitive information.

## Related Security Patterns & Anti-Patterns

- [Debug Mode in Production Anti-Pattern](../debug-mode-production/): Debug mode often exposes verbose error messages, making it a severe risk in production.
- [Missing Authentication Anti-Pattern](../missing-authentication/): Generic authentication error messages are a key defense.

## References

- [OWASP Top 10 A02:2025 - Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [OWASP GenAI LLM02:2025 - Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
- [CWE-209: Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html)
- [CAPEC-54: Query System for Information](https://capec.mitre.org/data/definitions/54.html)
- [PortSwigger: Information Disclosure](https://portswigger.net/web-security/information-disclosure)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
