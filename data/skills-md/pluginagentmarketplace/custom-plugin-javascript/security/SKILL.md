---
name: security
description: JavaScript security best practices and vulnerability prevention.
sasmp_version: "1.3.0"
bonded_agent: 08-javascript-testing-quality
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [vulnerability_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_xss_prevention

observability:
  entry_log: "Security skill activated"
  exit_log: "Security reference provided"
---

# JavaScript Security Skill

## Quick Reference Card

### XSS Prevention
```javascript
// DANGEROUS - Never do this
element.innerHTML = userInput;

// SAFE - Use textContent
element.textContent = userInput;

// SAFE - Sanitize HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// SAFE - Create elements
const div = document.createElement('div');
div.textContent = userInput;
parent.appendChild(div);
```

### Input Validation
```javascript
// Server-side validation is required
// Client-side is for UX only

function validateEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

function sanitizeInput(input) {
  return input
    .trim()
    .replace(/[<>]/g, ''); // Basic, use library for real apps
}

// Use schema validation
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150)
});

UserSchema.parse(userData); // Throws if invalid
```

### Content Security Policy
```html
<!-- In HTML head or HTTP header -->
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self';
           script-src 'self' https://trusted.com;
           style-src 'self' 'unsafe-inline';">
```

### Secure Storage
```javascript
// NEVER store sensitive data in localStorage
// Use httpOnly cookies for tokens

// If you must use localStorage:
// - Don't store tokens
// - Don't store PII
// - Encrypt if necessary

// Secure cookie settings
document.cookie = 'token=abc; Secure; HttpOnly; SameSite=Strict';
```

### CSRF Protection
```javascript
// Include CSRF token in requests
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

fetch('/api/action', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrfToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
```

### Dependency Security
```bash
# Audit dependencies
npm audit

# Fix vulnerabilities
npm audit fix

# Check specific package
npm audit --package-lock-only

# Use Snyk for deeper analysis
npx snyk test
```

## Common Vulnerabilities

| Vulnerability | Prevention |
|---------------|------------|
| XSS | Use textContent, sanitize |
| CSRF | Use tokens, SameSite cookies |
| Injection | Parameterized queries |
| Prototype pollution | Freeze prototypes |
| Open redirect | Validate URLs |

### Prototype Pollution Prevention
```javascript
// Vulnerable
function merge(target, source) {
  for (const key in source) {
    target[key] = source[key]; // Can pollute __proto__
  }
}

// Safe
function safeMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor') continue;
    target[key] = source[key];
  }
}

// Or use Object.assign / spread
const merged = { ...target, ...source };
```

## Troubleshooting

### Security Checklist

- [ ] User input sanitized
- [ ] HTTPS enforced
- [ ] CSP headers set
- [ ] Dependencies audited
- [ ] Sensitive data encrypted
- [ ] Auth tokens in httpOnly cookies
- [ ] CSRF protection enabled
- [ ] Error messages don't leak info

### Debug Approach
```javascript
// Log security events
window.addEventListener('securitypolicyviolation', (e) => {
  console.error('CSP violation:', e.blockedURI);
});

// Check for XSS vectors
const testInput = '<script>alert(1)</script>';
// If this executes, you have XSS
```

## Production Patterns

### JWT Handling
```javascript
// Store in memory, not localStorage
let accessToken = null;

async function login(credentials) {
  const response = await fetch('/api/login', {
    method: 'POST',
    credentials: 'include', // For httpOnly refresh token
    body: JSON.stringify(credentials)
  });
  const { accessToken: token } = await response.json();
  accessToken = token; // Memory only
}

// Refresh before expiry
async function refreshToken() {
  const response = await fetch('/api/refresh', {
    credentials: 'include'
  });
  const { accessToken: token } = await response.json();
  accessToken = token;
}
```

### URL Validation
```javascript
function isSafeRedirect(url) {
  try {
    const parsed = new URL(url, window.location.origin);
    return parsed.origin === window.location.origin;
  } catch {
    return false;
  }
}
```

## Related

- **Agent 08**: Testing & Quality (detailed learning)
- **Skill: ecosystem**: npm audit
- **Skill: patterns**: Secure patterns
