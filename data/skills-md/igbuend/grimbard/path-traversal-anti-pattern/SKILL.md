---
name: "path-traversal-anti-pattern"
description: "Security anti-pattern for path traversal vulnerabilities (CWE-22). Use when generating or reviewing code that handles file paths, reads or writes files based on user input, or serves static content. Detects joining user input to paths without proper sanitization or validation."
---

# Path Traversal Anti-Pattern

**Severity:** High

## Summary

Attackers read or write files outside intended directories by manipulating user input in file paths. Using sequences like `../` without validation allows navigation up directory trees to access `/etc/passwd`, source code, or credentials.

## The Anti-Pattern

The anti-pattern is concatenating user input into file paths without validating for directory traversal characters.

### BAD Code Example

```python
# VULNERABLE: User input joined directly to base path.
from flask import request
import os

BASE_DIR = "/var/www/uploads/"

@app.route("/files/view")
def view_file():
    # Filename from request without validation.
    filename = request.args.get("filename")

    # User input concatenated with base directory.
    # No path traversal validation.
    file_path = os.path.join(BASE_DIR, filename)

    # Attack: /files/view?filename=../../../../etc/passwd
    # Result: /var/www/uploads/../../../../etc/passwd
    # Resolves to: /etc/passwd

    # Reads and returns system password file.
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found.", 404
```

### GOOD Code Example

```python
# SECURE: Validate input and canonicalize path.
from flask import request
import os

BASE_DIR = "/var/www/uploads/"

@app.route("/files/view/secure")
def view_file_secure():
    filename = request.args.get("filename")

    # 1. Basic validation: check for malicious characters.
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename.", 400

    # 2. Construct full path.
    file_path = os.path.join(BASE_DIR, filename)

    # 3. Canonicalize: resolve symbolic links and `../` sequences.
    #    Most critical step.
    real_path = os.path.realpath(file_path)
    real_base_dir = os.path.realpath(BASE_DIR)

    # 4. Ensure resolved path within intended base directory.
    if not real_path.startswith(real_base_dir + os.sep):
        return "Access denied: Path is outside of the allowed directory.", 403

    # Safe to access file.
    try:
        with open(real_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found.", 404
```

## Detection

- **Trace user input:** Follow any user-controlled input (from request parameters, body, headers, etc.) that is used in a file operation.
- **Look for path concatenation:** Search for functions that join or concatenate strings to form file paths (e.g., `os.path.join`, `+` on strings).
- **Check for missing validation:** Verify that before being used, the input is checked for path traversal sequences (`../`, `..\`). A simple search-and-replace for `../` is not sufficient due to potential bypasses like `....//`.
- **Ensure path canonicalization:** The most important check is to see if the application resolves the final path to its absolute, canonical form and then verifies that it is still within the intended base directory.

## Prevention

- [ ] **Never trust user input:** Don't trust user-provided data in file path construction.
- [ ] **Validate input:** Use strict allowlist of known-good filenames. Otherwise disallow path traversal sequences.
- [ ] **Canonicalize paths:** Use `os.path.realpath()` (Python), `File.getCanonicalPath()` (Java) to resolve to absolute form.
- [ ] **Verify final path:** After canonicalization, ensure path starts with expected base directory. Most reliable prevention.
- [ ] **Use indirect references:** Use IDs or indices instead of filenames. User never directly controls file path.

## Related Security Patterns & Anti-Patterns

- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Path traversal is a specific, high-impact consequence of missing input validation.
- [Unrestricted File Upload Anti-Pattern](../unrestricted-file-upload/): An attacker might use path traversal to write a malicious file (like a web shell) to an executable directory on the server.
- [Command Injection Anti-Pattern](../command-injection/): Path traversal can be used in conjunction with command injection to execute programs from unexpected locations.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM07:2025 - System Prompt Leakage](https://genai.owasp.org/llmrisk/llm07-system-prompt-leakage/)
- [OWASP API Security API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)
- [CAPEC-126: Path Traversal](https://capec.mitre.org/data/definitions/126.html)
- [PortSwigger: File Path Traversal](https://portswigger.net/web-security/file-path-traversal)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
