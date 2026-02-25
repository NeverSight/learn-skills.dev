---
name: csrf-auth-debugger
description: Debug CSRF token issues and authentication problems including 403 Forbidden errors, cookie issues, JWT tokens, OAuth flows, and session management. Use when troubleshooting CSRF verification failed, 403 errors on POST requests, login not working, or token refresh issues.
allowed-tools: Read, Grep, Glob, Bash
---

# CSRF & Authentication Debugger

Analyzes and debugs CSRF and authentication issues in this project.

## Project Context

- Authentication: JWT tokens in httpOnly cookies + OAuth (Google, GitHub)
- CSRF: Django's CSRF middleware with cookie-based tokens
- OAuth library: django-allauth
- Token service: `services/auth/tokens.py`
- Frontend API: Axios with credentials and CSRF interceptor

## Authentication Architecture

```
Browser
    ↓ Request with cookies
    │ - access_token (httpOnly, JWT)
    │ - refresh_token (httpOnly, JWT)
    │ - csrftoken (readable by JS)
Django
    ↓ CsrfViewMiddleware
    ↓ JWTAuthenticationMiddleware
    ↓ View/API endpoint
```

## When to Use

- "CSRF verification failed"
- "403 Forbidden on POST/PUT/DELETE"
- "Login not working"
- "Token expired"
- "OAuth callback failing"
- "Cookies not being set"
- "X-CSRFToken header missing"

## CSRF Flow

### How CSRF Works in This Project

1. **GET `/api/v1/auth/csrf/`** - Sets `csrftoken` cookie
2. **Frontend reads cookie** - `getCookie('csrftoken')`
3. **POST/PUT/DELETE requests** - Include `X-CSRFToken` header
4. **Django validates** - Compares header to cookie

### Frontend CSRF Handling

```typescript
// frontend/src/services/api.ts
api.interceptors.request.use((config) => {
  if (['post', 'put', 'patch', 'delete'].includes(method)) {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
  }
});
```

## Common CSRF Issues

**403 "CSRF verification failed":**

1. **Missing CSRF cookie**
   ```bash
   # Check if cookie exists in browser DevTools > Application > Cookies
   # Should see: csrftoken
   ```

2. **Missing X-CSRFToken header**
   ```javascript
   // Check Network tab - request headers should include:
   // X-CSRFToken: <token value>
   ```

3. **Cookie not sent (CORS)**
   ```typescript
   // Axios must have:
   withCredentials: true
   ```

4. **Domain mismatch**
   ```python
   # settings.py - check these match your domain
   CSRF_COOKIE_DOMAIN = None  # or '.yourdomain.com'
   CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', ...]
   ```

5. **SameSite cookie issues**
   ```python
   # For cross-origin requests:
   CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' with Secure
   ```

## Common Auth Issues

**JWT token expired:**
```python
# Check token expiry in services/auth/tokens.py
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)
```

**Cookies not set after login:**
```python
# Check response has Set-Cookie headers
# Verify SameSite and Secure flags match environment
```

**OAuth callback failing:**
```bash
# Check callback URL matches exactly:
# - In Google/GitHub OAuth app settings
# - In django-allauth config
# - Including trailing slashes!
```

## Debugging Steps

### 1. Check CSRF Cookie Exists
```javascript
// Browser console
document.cookie.split(';').find(c => c.includes('csrftoken'))
```

### 2. Check Request Headers
```
Network tab > Request > Headers
Look for: X-CSRFToken: <value>
```

### 3. Check Django Logs
```bash
docker compose logs web | grep -i csrf
```

### 4. Test CSRF Endpoint
```bash
curl -c cookies.txt http://localhost:8000/api/v1/auth/csrf/
cat cookies.txt  # Should show csrftoken
```

### 5. Verify Settings
```python
# Django shell
from django.conf import settings
print(settings.CSRF_COOKIE_NAME)
print(settings.CSRF_TRUSTED_ORIGINS)
print(settings.CORS_ALLOWED_ORIGINS)
```

## Key Files to Check

```
Backend:
├── config/settings.py          # CSRF_*, CORS_*, cookie settings
├── core/auth/views.py          # Login, logout, OAuth views
├── core/views/core_views.py    # CSRF token endpoint
├── services/auth/tokens.py     # JWT token creation
└── services/auth/__init__.py   # set_auth_cookies function

Frontend:
├── src/services/api.ts         # Axios CSRF interceptor
├── src/contexts/AuthContext.tsx # Auth state management
└── src/pages/AuthPage.tsx      # Login/OAuth UI
```

## Django CSRF Settings

```python
# config/settings.py - key settings
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_HTTPONLY = False  # Must be False for JS to read
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
]
```

## Views Exempt from CSRF

Some views use `@csrf_exempt` (check if issue is with exempt view):
```bash
grep -r "csrf_exempt" core/
```

## Testing Authentication

```bash
# Login and get tokens
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"password"}'

# Use tokens for authenticated request
curl http://localhost:8000/api/v1/users/me/ \
  -b cookies.txt
```
