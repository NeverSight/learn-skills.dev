---
name: "missing-security-headers-anti-pattern"
description: "Security anti-pattern for missing security headers (CWE-16). Use when generating or reviewing web application code, server configuration, or HTTP response handling. Detects missing CSP, HSTS, X-Frame-Options, and other protective headers."
---

# Missing Security Headers Anti-Pattern

**Severity:** Medium

## Summary

HTTP security headers defend against XSS, clickjacking, and man-in-the-middle attacks at the browser level. Applications failing to send these headers rely on insecure browser defaults, missing a powerful declarative security layer.

## The Anti-Pattern

The anti-pattern is omitting security headers from HTTP responses. Browsers default to permissive policies; servers must instruct stricter controls.

### BAD Code Example

```python
# VULNERABLE: A Flask application that does not set any security headers.
from flask import Flask, make_response

app = Flask(__name__)

@app.route("/")
def index():
    # Response sent with insecure default headers.
    # - No CSP: scripts from any origin can execute
    # - No X-Frame-Options: any site can iframe for clickjacking
    # - No HSTS: connection can downgrade to HTTP
    response = make_response("<h1>Welcome to the site!</h1>")
    return response

# The HTTP response would look something like this:
#
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=utf-8
# Content-Length: 29
#
# <h1>Welcome to the site!</h1>
```

### GOOD Code Example

```python
# SECURE: The application sets a strong baseline of security headers for all responses.
from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    # CSP: Prevents XSS. Allows resources only from same origin ('self').
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    # X-Frame-Options: Prevents iframe embedding, mitigates clickjacking.
    response.headers['X-Frame-Options'] = 'DENY'

    # HSTS: Instructs browser to use only HTTPS.
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # X-Content-Type-Options: Prevents MIME-sniffing.
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # Referrer-Policy: Controls referrer information sent with requests.
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.route("/")
def index_secure():
    return make_response("<h1>Welcome to the secure site!</h1>")

# The HTTP response now includes critical security controls:
#
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=utf-8
# Content-Length: 36
# Content-Security-Policy: default-src 'self'
# X-Frame-Options: DENY
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# X-Content-Type-Options: nosniff
# Referrer-Policy: strict-origin-when-cross-origin
#
# <h1>Welcome to the secure site!</h1>
```

## Detection

- **Use browser developer tools:** Open the "Network" tab, inspect a request to your site, and look at the "Response Headers" section. Check for the presence of the headers listed below.
- **Use an online scanner:** Tools like [SecurityHeaders.com](https://securityheaders.com/) can quickly scan a public website and report on its missing headers.
- **Review framework configurations:** Check your web server or framework's configuration files to see if security headers are being set globally. Many frameworks have dedicated middleware (like `Helmet` for Express.js) to handle this.

## Prevention

Implement a middleware or a global response filter in your application that adds the following headers to all outgoing responses.

- [ ] **`Content-Security-Policy` (CSP):** Most important XSS defense. Defines strict allowlist for content sources (scripts, styles, images). Start with `default-src 'self'`.
- [ ] **`Strict-Transport-Security` (HSTS):** Browser uses only HTTPS. Prevents downgrade attacks.
- [ ] **`X-Frame-Options`:** Primary clickjacking defense. Prevents iframe embedding. Set to `DENY` or `SAMEORIGIN`.
- [ ] **`X-Content-Type-Options`:** Set to `nosniff`. Prevents MIME-sniffing abuse for script execution.
- [ ] **`Referrer-Policy`:** Controls referrer information sent on navigation. Default: `strict-origin-when-cross-origin`.
- [ ] **`Permissions-Policy`:** Selectively enable/disable browser features (microphone, camera, geolocation).

## Related Security Patterns & Anti-Patterns

- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): A strong Content-Security-Policy is a critical defense-in-depth measure against XSS.
- [Open CORS Anti-Pattern](../open-cors/): Another type of security misconfiguration related to HTTP headers.

## References

- [OWASP Top 10 A02:2025 - Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [OWASP GenAI LLM02:2025 - Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [CWE-16: Configuration](https://cwe.mitre.org/data/definitions/16.html)
- [CAPEC-462: Cross-Domain Search Timing](https://capec.mitre.org/data/definitions/462.html)
- [SecurityHeaders.com](https://securityheaders.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
