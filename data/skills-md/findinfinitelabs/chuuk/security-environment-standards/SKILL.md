---
name: security-environment-standards
description: Security and environment configuration standards for web applications, including environment variable management, secure coding practices, and production deployment security. Use when setting up environments, configuring security, or deploying applications.
---

# Security & Environment Standards

## Authentication Model

The app uses **passwordless magic-link authentication** — no passwords, no `flask-login`, no WTForms. A time-limited token is emailed; clicking it creates an authenticated session.

```python
# app.py globals
magic_links    = {}   # {token: {'email': str, 'expires': datetime}}
active_sessions = {}  # {email: session_id} — one session per user enforced

MAGIC_LINK_EXPIRY_MINUTES = 15

def send_magic_link_email(email, magic_token, base_url) -> bool:
    # Send link via SMTP; falls back to stdout in dev (no SMTP config).
    ...
```

The `@login_required` decorator (defined in `app.py`) checks `session['authenticated']` and `active_sessions`.

## Environment Variables

```bash
# .env  (never commit — listed in .gitignore)

# Flask
FLASK_SECRET_KEY=<64-hex-chars>     # Required in production
FLASK_ENV=production                # Enables secure cookies

# Database
COSMOS_DB_CONNECTION_STRING=mongodb://...  # Full Cosmos DB connection string

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app-specific-password
SMTP_FROM=your@gmail.com

# OCR (optional)
GOOGLE_VISION_API_KEY=...

# App limits
MAX_CONTENT_LENGTH=16777216   # 16 MB
UPLOAD_FOLDER=uploads
```

## Session Security (actual app.py config)

```python
app.config['SESSION_COOKIE_SECURE']   = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7   # 7 days
```

## File Upload Security

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'txt', 'csv', 'epub'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Always use werkzeug's secure_filename
filename = secure_filename(file.filename)
```

## Regex Safety

User input used in MongoDB `$regex` must be escaped:

```python
import re
pattern = re.escape(user_input)   # prevents ReDoS
collection.find({'field': {'$regex': f'^{pattern}$'}})
```

## Secrets Management

- Never hardcode secrets in source files
- Use Azure Key Vault references for production environment variables
- `FLASK_SECRET_KEY` must be set explicitly in production; app raises `ValueError` otherwise
- `users.json` (authorised email list) is gitignored in production deployments

## Production Checklist

- [ ] `FLASK_ENV=production` (enables secure cookies)
- [ ] `FLASK_SECRET_KEY` set to 64+ hex chars
- [ ] SMTP credentials configured (magic-link delivery)
- [ ] Cosmos DB connection string from Key Vault
- [ ] `users.json` authorised users list deployed
- [ ] HTTPS enforced at load balancer / Azure Container App ingress

## Source Files

- `app.py` — auth routes, `login_required` decorator, `send_magic_link_email()`
- `config/users.json` — authorised user email list
- `deploy-chuuk.sh` — production Azure deployment script
