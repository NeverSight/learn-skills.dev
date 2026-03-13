---
name: "open-cors-anti-pattern"
description: "Security anti-pattern for open Cross-Origin Resource Sharing (CORS) policies (CWE-942). Use when generating or reviewing server configurations, API backends, or any code that sets CORS headers. Detects overly permissive Access-Control-Allow-Origin headers, including wildcard, null origin, and reflected origin."
---

# Open CORS Policy Anti-Pattern

**Severity:** Medium

## Summary

Misconfigured CORS policies allow any website to make authenticated requests on behalf of users. Servers responding with `Access-Control-Allow-Origin: *` or reflecting client `Origin` headers enable data theft and unauthorized actions.

## The Anti-Pattern

The anti-pattern is overly permissive `Access-Control-Allow-Origin` headers: wildcard (`*`) or reflecting client `Origin` values.

### BAD Code Example

```python
# VULNERABLE: The server reflects any Origin header, or uses a wildcard with credentials.
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    # DANGEROUS: Reflecting Origin header.
    # Attacker site (https://evil.com) can make requests.
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin

    # DANGEROUS: Wildcard with credentials.
    # Most browsers block, but critical misconfiguration.
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

@app.route("/api/user/profile")
def get_profile():
    # Endpoint for frontend, relies on session cookie.
    user = get_user_from_session()
    return jsonify(user.to_dict())

# Attack:
# 1. Logged-in user visits https://evil.com
# 2. Script fetches https://yourapp.com/api/user/profile
# 3. Permissive CORS allows request with session cookie
# 4. Server responds with user's sensitive profile
# 5. evil.com exfiltrates user data
```

### GOOD Code Example

```python
# SECURE: Maintain a strict allowlist of trusted origins.
from flask import Flask, request, jsonify

app = Flask(__name__)

# Strict allowlist of permitted origins.
ALLOWED_ORIGINS = {
    "https://www.yourapp.com",
    "https://yourapp.com",
    "https://staging.yourapp.com"
}

@app.after_request
def add_secure_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        # Set header only if origin in trusted list.
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        # Vary tells caches response depends on Origin.
        response.headers['Vary'] = 'Origin'
    return response

@app.route("/api/user/profile")
def get_profile_secure():
    user = get_user_from_session()
    return jsonify(user.to_dict())

# Script from https://evil.com: origin not in ALLOWED_ORIGINS,
# no CORS headers sent. Browser same-origin policy blocks request.
```

## Detection

- **Use browser developer tools:** Open the "Network" tab, make a cross-origin request to your API, and inspect the response headers. Look for `Access-Control-Allow-Origin`. Is it `*`? Does it match the `Origin` of your request even if that origin is untrusted?
- **Use `curl`:** Make a request and set a custom `Origin` header to see if the server reflects it:
  `curl -H "Origin: https://evil.com" -I https://yourapp.com/api/some-endpoint`
  Check if the response contains `Access-Control-Allow-Origin: https://evil.com`.
- **Review CORS configuration:** Check your application's code or framework configuration for how CORS headers are being set. Look for wildcards or reflected origins.

## Prevention

- [ ] **Maintain strict allowlist:** Most critical step. Define trusted origins explicitly.
- [ ] **Never reflect `Origin` header:** Validate against allowlist before reflecting.
- [ ] **Avoid wildcard on authenticated endpoints:** `*` unsafe for endpoints using cookies or `Authorization` headers. Only use for public, unauthenticated resources.
- [ ] **Use `Access-Control-Allow-Credentials` carefully:** Set to `true` only when necessary and only for allowlisted origins.
- [ ] **Add `Vary: Origin` header:** Tells caches response depends on Origin. Prevents cached response for trusted origin being served to malicious one.

## Related Security Patterns & Anti-Patterns

- [Missing Security Headers Anti-Pattern](../missing-security-headers/): CORS is a key part of the broader suite of security headers an application must manage.
- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): An attacker could use a permissive CORS policy to exfiltrate data stolen via an XSS attack.

## References

- [OWASP Top 10 A02:2025 - Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [OWASP GenAI LLM07:2025 - System Prompt Leakage](https://genai.owasp.org/llmrisk/llm07-system-prompt-leakage/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP CORS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html)
- [CWE-942: Permissive Cross-domain Policy with Untrusted Domains](https://cwe.mitre.org/data/definitions/942.html)
- [PortSwigger - CORS Vulnerabilities](https://portswigger.net/web-security/cors)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
