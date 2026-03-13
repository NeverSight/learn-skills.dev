---
name: "missing-rate-limiting-anti-pattern"
description: "Security anti-pattern for missing rate limiting (CWE-770). Use when generating or reviewing API endpoints, authentication systems, or public-facing services. Detects absence of request throttling enabling brute force, credential stuffing, and DoS attacks."
---

# Missing Rate Limiting Anti-Pattern

**Severity:** High

## Summary

Applications fail to restrict action frequency, allowing unlimited requests to endpoints. Enables brute-force attacks, data scraping, and denial-of-service through resource-intensive requests.

## The Anti-Pattern

The anti-pattern is exposing endpoints (especially authentication/resource-intensive) without controlling request frequency per user or IP.

### BAD Code Example

```python
# VULNERABLE: The login endpoint has no rate limiting.
from flask import request, jsonify

@app.route("/api/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Endpoint callable thousands of times per minute from same IP.
    # Attacker uses password lists for brute-force/credential stuffing,
    # trying millions of passwords until finding correct one.
    if check_credentials(username, password):
        return jsonify({"status": "success", "token": generate_token(username)})
    else:
        return jsonify({"status": "failed"}), 401

# Search endpoint without rate limiting.
@app.route("/api/search")
def search():
    query = request.args.get("q")
    # Attacker rapidly hits endpoint, scraping data or causing
    # DoS through heavy database work.
    results = perform_complex_search(query)
    return jsonify(results)
```

### GOOD Code Example

```python
# SECURE: Implement rate limiting using middleware and a tracking backend like Redis.
from flask import request, jsonify
from redis import Redis
from functools import wraps

redis = Redis()

def rate_limit(limit, per, scope_func):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"rate-limit:{scope_func(request)}:{request.endpoint}"
            # Increment count for current key.
            # Expire after `per` seconds on first request in window.
            p = redis.pipeline()
            p.incr(key)
            p.expire(key, per)
            count = p.execute()[0]

            if count > limit:
                return jsonify({"error": "Rate limit exceeded"}), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Get identifier for rate limit scope (IP address).
def get_ip(request):
    return request.remote_addr

# Apply different rate limits per endpoint.
@app.route("/api/login", methods=["POST"])
@rate_limit(limit=10, per=60*5, scope_func=get_ip) # 10 requests/5min per IP
def login_secure():
    # ... login logic ...
    pass

@app.route("/api/search")
@rate_limit(limit=100, per=60, scope_func=get_ip) # 100 requests/min per IP
def search_secure():
    # ... search logic ...
    pass
```

## Detection

- **Review public endpoints:** Examine all endpoints that can be accessed without authentication. Do they have rate limiting?
- **Check authentication endpoints:** Specifically look at login, password reset, and registration endpoints. These are prime targets for brute-force attacks if not rate-limited.
- **Analyze API design:** For public APIs, check if there is a documented rate-limiting policy (e.g., in the API documentation).
- **Perform testing:** Write a simple script to hit a single endpoint in a tight loop. If you don't receive a `429 Too Many Requests` status code after a certain number of attempts, the endpoint is likely missing rate limiting.

## Prevention

- [ ] **Implement IP-based rate limiting:** All public endpoints, especially authentication/sensitive ones.
- [ ] **Implement account-based rate limiting:** Prevent authenticated users from abusing system.
- [ ] **Use appropriate algorithm:** Token Bucket, Leaky Bucket, or Fixed/Sliding Window. Most frameworks have middleware.
- [ ] **Return `429 Too Many Requests`:** Include `Retry-After` header indicating retry time.
- [ ] **Log rate limit violations:** Identify and respond to potential attacks.
- [ ] **Consider account lockouts for login:** Additional defense after failed attempts.

## Related Security Patterns & Anti-Patterns

- [Missing Authentication Anti-Pattern](../missing-authentication/): Endpoints that are missing authentication are at even greater risk if they also lack rate limiting.
- [Denial of Service (DoS):](../#) Missing rate limiting is a primary cause of application-layer DoS vulnerabilities.

## References

- [OWASP Top 10 A06:2025 - Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [OWASP API Security API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP Rate Limiting](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)
- [CWE-770: Resource Allocation Without Limits](https://cwe.mitre.org/data/definitions/770.html)
- [CAPEC-49: Password Brute Forcing](https://capec.mitre.org/data/definitions/49.html)
- [PortSwigger: Authentication](https://portswigger.net/web-security/authentication)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
