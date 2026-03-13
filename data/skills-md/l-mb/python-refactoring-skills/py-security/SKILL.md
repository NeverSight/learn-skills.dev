---
name: py-security
description: Security vulnerability detection and remediation for Python codebases. Identifies SQL injection, hardcoded secrets, weak cryptography, and other OWASP vulnerabilities.
status: stable
---

# Python Security Analysis and Remediation

Find and fix security vulnerabilities in Python code following Engineering Charter security principles.

## Objectives

1. Detect security vulnerabilities using automated scanners
2. Identify SQL injection risks
3. Find hardcoded secrets and credentials
4. Detect weak cryptographic practices
5. Fix vulnerabilities following secure coding patterns
6. Prevent secrets from being committed to git

## Required Tools

**Add to `[dependency-groups]` dev**: `"bandit"`, `"ruff"`

- **bandit**: AST-based security scanner
- **ruff --select S**: Built-in Bandit rules (faster alternative)

**Permissions**: Run py-quality-setup first to configure `.claude/settings.local.json` with all needed tool permissions.

## Discovery Phase

### Run Security Scanners

```bash
# Using bandit (comprehensive reports)
bandit -r . -f json -o bandit_report.json
bandit -r . -ll  # Show only medium/high severity

# Using ruff (faster, integrates with existing tooling)
ruff check . --select S
ruff check . --select S --output-format=json > security_report.json
```

### Common Vulnerability Categories

**High severity** (fix immediately):
- **S608**: SQL injection via string formatting
- **S105, S106, S107**: Hardcoded passwords, secrets, keys
- **S501, S506**: Weak SSL/TLS configuration
- **S324**: Insecure hash functions (MD5, SHA1)
- **S602, S603, S604, S605, S606, S607**: Shell injection risks

**Medium severity**:
- **S311**: Insecure random number generation
- **S301, S302, S303**: Insecure deserialization (pickle)
- **S701, S702**: Jinja2 autoescape issues

**Low severity** (consider context):
- **S101**: Use of assert (disabled in production)
- **S104**: Binding to all interfaces (0.0.0.0)

## Remediation Patterns

### SQL Injection Prevention

```python
# BEFORE - Vulnerable to SQL injection
def get_user(user_id: str) -> dict:
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()

# AFTER - Use parametrized queries
def get_user(user_id: str) -> dict:
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

# For dynamic table/column names (cannot be parametrized)
from psycopg2 import sql

def get_data(table_name: str, column: str) -> list:
    # Validate inputs first!
    allowed_tables = {"users", "orders", "products"}
    if table_name not in allowed_tables:
        raise ValueError(f"Invalid table: {table_name}")

    query = sql.SQL("SELECT {column} FROM {table}").format(
        column=sql.Identifier(column),
        table=sql.Identifier(table_name)
    )
    cursor.execute(query)
    return cursor.fetchall()
```

### Hardcoded Secrets Removal

```python
# BEFORE - Hardcoded secrets (NEVER commit these)
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgres://user:password@localhost/db"
SECRET_TOKEN = "my-secret-token-123"

# AFTER - Use environment variables
import os

API_KEY = os.environ["API_KEY"]  # Raises if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://localhost/db")  # With default
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")  # Returns None if not set

# For development, use python-dotenv
from dotenv import load_dotenv
load_dotenv()  # Loads from .env file (add .env to .gitignore!)
API_KEY = os.environ["API_KEY"]
```

### Secure Random Number Generation

```python
# BEFORE - Insecure for security-sensitive operations
import random

session_token = random.randint(100000, 999999)
api_key = ''.join(random.choices('abcdef0123456789', k=32))

# AFTER - Use secrets module for cryptographic randomness
import secrets

session_token = secrets.randbelow(900000) + 100000
api_key = secrets.token_hex(16)  # 32 hex characters
secure_password = secrets.token_urlsafe(32)  # URL-safe token
```

### Secure Cryptography

```python
# BEFORE - Weak hash functions
import hashlib

password_hash = hashlib.md5(password.encode()).hexdigest()  # Weak!
checksum = hashlib.sha1(data).hexdigest()  # Weak for security!

# AFTER - Use strong hash functions
import hashlib

# For passwords - use bcrypt or argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)
ph.verify(password_hash, password)  # Verify

# For data integrity - use SHA256 or better
checksum = hashlib.sha256(data).hexdigest()
secure_hash = hashlib.blake2b(data).hexdigest()
```

### Shell Command Injection Prevention

```python
# BEFORE - Shell injection vulnerability
import os
import subprocess

filename = user_input
os.system(f"cat {filename}")  # Dangerous!
subprocess.call(f"ls {directory}", shell=True)  # Dangerous!

# AFTER - Use subprocess with list arguments (no shell)
import subprocess
from pathlib import Path

# Validate input first
filename = user_input
if not Path(filename).exists():
    raise ValueError("File not found")

# Use list form, no shell=True
subprocess.run(["cat", filename], check=True)
subprocess.run(["ls", directory], check=True)

# Even better - use Python libraries instead of shell commands
with open(filename) as f:
    content = f.read()
```

## Git Hooks Integration

Add secret detection to git hooks (complement to py-git-hooks):

```bash
# In .git/hooks/pre-commit, add before other checks:

# Detect potential secrets
if git diff --cached | grep -qiE '(password|secret|api[_-]?key|token|credentials)'; then
    echo "⚠️  Warning: Potential secrets detected in staged changes"
    echo "Review carefully before committing"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

## Verification Checklist

- [ ] `ruff check . --select S` reports no security issues
- [ ] `bandit -r . -ll` reports no medium/high severity issues
- [ ] No hardcoded secrets in codebase (grep for password, secret, api_key, token)
- [ ] Secrets loaded from environment variables or .env file
- [ ] .env file is in .gitignore
- [ ] All SQL queries use parametrized queries
- [ ] All tests pass after security fixes

## Examples

**Example: Security audit workflow**
```
1. Scan: ruff check . --select S; bandit -r . -ll
2. Found: SQL injection (S608), hardcoded secret (S105)
3. Fix SQL: Use parametrized query with %s placeholders
4. Fix secret: Move to .env, use os.environ["API_KEY"]
5. Verify: Scans clean, tests pass
```

## Related Skills

- **Prerequisites**: py-quality-setup (configure ruff for security checks)
- **Enforcement**: py-git-hooks (add security scanning to pre-commit)
- **See also**: py-code-health (cleanup after security fixes)
