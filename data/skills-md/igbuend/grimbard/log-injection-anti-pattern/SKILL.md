---
name: "log-injection-anti-pattern"
description: "Security anti-pattern for log injection vulnerabilities (CWE-117). Use when generating or reviewing code that writes to log files, handles logging of user input, or processes log data. Detects unsanitized data in log messages enabling log forging and CRLF injection."
---

# Log Injection Anti-Pattern

**Severity:** Medium

## Summary

Log injection occurs when attackers write arbitrary data into log files by injecting newlines (\n) and carriage returns (\r) through unsanitized user input. Attackers create fake log entries to hide malicious activity, mislead administrators, and exploit log analysis tools.

## The Anti-Pattern

Never log unsanitized user input. Attackers inject newline characters to forge log entries.

### BAD Code Example

```python
# VULNERABLE: User input logged directly without sanitization
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def user_login(username, ip_address):
    # Attacker provides username with newline character
    # Example: "j_smith\nINFO - Successful login for user: admin from IP: 10.0.0.1"
    logging.info(f"Failed login attempt for user: {username} from IP: {ip_address}")

# Attacker input:
# username = "j_smith\nINFO - 2023-10-27 10:00:00,000 - Successful login for user: admin"
# ip_address = "192.168.1.100"

# Resulting log file:
#
# 2023-10-27 09:59:59,123 - Failed login attempt for user: j_smith
# INFO - 2023-10-27 10:00:00,000 - Successful login for user: admin from IP: 192.168.1.100
#
# Attacker forged log entry making 'admin' appear logged in,
# covering tracks or triggering false alerts
```

### GOOD Code Example

```python
# SECURE: Sanitize user input before logging or use structured logging
import logging
import json

# Option 1: Sanitize by removing or encoding control characters
def sanitize_for_log(input_string):
    return input_string.replace('\n', '_').replace('\r', '_')

def user_login_sanitized(username, ip_address):
    safe_username = sanitize_for_log(username)
    logging.info(f"Failed login attempt for user: {safe_username} from IP: {ip_address}")


# Option 2 (Better): Use structured logging
# Logging library handles special character escaping automatically
logging.basicConfig(filename='app_structured.log', level=logging.INFO)

def user_login_structured(username, ip_address):
    log_data = {
        "event": "login_failure",
        "username": username, # Newline character escaped by JSON formatter
        "ip_address": ip_address
    }
    logging.info(json.dumps(log_data))

# Resulting log entry is single, valid JSON object:
# {"event": "login_failure", "username": "j_smith\nINFO - ...", "ip_address": "192.168.1.100"}
# Log analysis tools safely parse without being tricked by newline
```

## Detection

- **Find unsanitized logging:** Grep for user input in log statements:
  - `rg 'logging\.(info|warn|error).*f["\']|logging.*\+.*request\.' --type py`
  - `rg 'console\.(log|error).*\$\{|logger.*\+.*req\.' --type js`
  - `rg 'logger\.(info|warn).*\+|log\.println.*\+' --type java`
- **Identify string concatenation in logs:** Find unescaped variables:
  - `rg 'log.*%s|log.*\.format|log.*f"' --type py -A 1`
  - `rg 'log\(.*\+|logger.*template' --type js`
- **Test with CRLF injection:** Input test strings to verify sanitization:
  - `username%0aINFO - Fake log entry` (URL-encoded newline)
  - `admin\r\nSUCCESS: ` (direct CRLF)
- **Check for structured logging:** Verify JSON escaping:
  - `rg 'json\.dumps|JSON\.stringify' | rg 'log'`

## Prevention

- [ ] **Sanitize all user input:** Strip or encode newline (`\n`), carriage return (`\r`), and control characters before logging
- [ ] **Use structured logging (JSON):** Libraries automatically escape special characters, preventing log injection
- [ ] **Never log sensitive data:** Exclude passwords, API keys, or PII
- [ ] **Limit log entry length:** Prevent disk-filling DoS attacks from enormous log entries

## Related Security Patterns & Anti-Patterns

- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): Unescaped HTML characters in browser-viewed logs enable XSS
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Log injection root cause—failure to validate and sanitize user input

## References

- [OWASP Top 10 A09:2025 - Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-117: Log Injection](https://cwe.mitre.org/data/definitions/117.html)
- [CAPEC-93: Log Injection-Tampering-Forging](https://capec.mitre.org/data/definitions/93.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
